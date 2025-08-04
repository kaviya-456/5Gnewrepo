import pytest
import logging
import os
import shutil
from datetime import datetime
from selenium.webdriver.remote.webdriver import WebDriver
from framework.driver_manager import driver_manager
from config.config import config
from utils.logger import setup_logging
from utils.test_data import create_sample_data_files

logger = logging.getLogger(__name__)

def pytest_configure(config_obj):
    """Called after command line options have been parsed"""
    # Setup logging
    setup_logging()
    
    # Create sample test data files if they don't exist
    try:
        create_sample_data_files()
    except Exception as e:
        logger.warning(f"Could not create sample data files: {e}")
    
    logger.info("Pytest configuration completed")

def pytest_sessionstart(session):
    """Called after the Session object has been created"""
    logger.info("=== Test Session Started ===")
    logger.info(f"Environment: {config.test.environment}")
    logger.info(f"Base URL: {config.test.base_url}")
    logger.info(f"Browser: {config.webdriver.browser}")
    logger.info(f"Headless: {config.webdriver.headless}")

def pytest_sessionfinish(session, exitstatus):
    """Called after whole test run finished"""
    logger.info(f"=== Test Session Finished with exit status: {exitstatus} ===")

@pytest.fixture(scope="session")
def browser_config():
    """Session-scoped fixture providing browser configuration"""
    return {
        "browser": config.webdriver.browser,
        "headless": config.webdriver.headless,
        "window_size": config.webdriver.window_size,
        "implicit_wait": config.webdriver.implicit_wait,
        "explicit_wait": config.webdriver.explicit_wait
    }

@pytest.fixture(scope="function")
def driver():
    """Function-scoped fixture providing WebDriver instance"""
    driver_instance = None
    try:
        driver_instance = driver_manager.get_driver()
        logger.info(f"WebDriver created: {type(driver_instance).__name__}")
        yield driver_instance
    finally:
        if driver_instance:
            try:
                driver_instance.quit()
                logger.info("WebDriver quit successfully")
            except Exception as e:
                logger.error(f"Error quitting WebDriver: {e}")

@pytest.fixture(scope="function")
def driver_with_login(driver):
    """Function-scoped fixture providing WebDriver with login"""
    from pages.login_page import LoginPage
    from utils.test_data import test_data
    
    login_page = LoginPage(driver)
    credentials = test_data.get_user_credentials("valid_user")
    
    # Navigate to login page and login
    login_page.navigate_to_login()
    login_page.login(credentials["username"], credentials["password"])
    login_page.wait_for_login_completion()
    
    if login_page.is_logged_in():
        logger.info("Successfully logged in for test")
    else:
        logger.warning("Login may have failed")
    
    yield driver

@pytest.fixture(scope="function")
def screenshot_on_failure(request, driver):
    """Fixture to take screenshot on test failure"""
    yield
    
    if request.node.rep_call.failed and config.test.screenshot_on_failure:
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            test_name = request.node.name.replace("[", "_").replace("]", "_")
            screenshot_name = f"failure_{test_name}_{timestamp}.png"
            screenshot_path = os.path.join(config.report.screenshots_dir, screenshot_name)
            
            driver.save_screenshot(screenshot_path)
            logger.info(f"Screenshot saved on failure: {screenshot_path}")
            
            # Attach to allure report if available
            try:
                import allure
                allure.attach.file(screenshot_path, name="Failure Screenshot", 
                                 attachment_type=allure.attachment_type.PNG)
            except ImportError:
                pass
        except Exception as e:
            logger.error(f"Failed to take screenshot on failure: {e}")

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test results for screenshot fixture"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)

@pytest.fixture(scope="function")
def test_data_manager():
    """Fixture providing test data manager"""
    from utils.test_data import test_data
    return test_data

@pytest.fixture(scope="session", autouse=True)
def cleanup_reports():
    """Clean up old report files at session start"""
    try:
        # Clean screenshots older than 7 days
        screenshots_dir = config.report.screenshots_dir
        if os.path.exists(screenshots_dir):
            cutoff_time = datetime.now().timestamp() - (7 * 24 * 60 * 60)  # 7 days
            for filename in os.listdir(screenshots_dir):
                filepath = os.path.join(screenshots_dir, filename)
                if os.path.isfile(filepath) and os.path.getmtime(filepath) < cutoff_time:
                    os.remove(filepath)
                    logger.debug(f"Removed old screenshot: {filename}")
        
        # Clean logs older than 30 days
        logs_dir = config.report.logs_dir
        if os.path.exists(logs_dir):
            cutoff_time = datetime.now().timestamp() - (30 * 24 * 60 * 60)  # 30 days
            for filename in os.listdir(logs_dir):
                filepath = os.path.join(logs_dir, filename)
                if os.path.isfile(filepath) and os.path.getmtime(filepath) < cutoff_time:
                    os.remove(filepath)
                    logger.debug(f"Removed old log: {filename}")
                    
    except Exception as e:
        logger.warning(f"Error during cleanup: {e}")

@pytest.fixture(params=["chrome", "firefox"])
def multi_browser_driver(request):
    """Parametrized fixture for multi-browser testing"""
    original_browser = config.webdriver.browser
    config.webdriver.browser = request.param
    
    driver_instance = None
    try:
        driver_instance = driver_manager.get_driver()
        logger.info(f"Multi-browser WebDriver created: {request.param}")
        yield driver_instance
    finally:
        if driver_instance:
            driver_instance.quit()
        config.webdriver.browser = original_browser

@pytest.fixture
def page_load_timeout():
    """Fixture providing page load timeout"""
    return config.webdriver.explicit_wait

# Pytest markers
def pytest_configure(config):
    """Register custom markers"""
    config.addinivalue_line("markers", "smoke: mark test as smoke test")
    config.addinivalue_line("markers", "regression: mark test as regression test")
    config.addinivalue_line("markers", "login: mark test as login related")
    config.addinivalue_line("markers", "navigation: mark test as navigation related")
    config.addinivalue_line("markers", "forms: mark test as form related")
    config.addinivalue_line("markers", "slow: mark test as slow running")
    config.addinivalue_line("markers", "critical: mark test as critical")

# Command line options
def pytest_addoption(parser):
    """Add custom command line options"""
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser to use for testing (chrome, firefox, edge)"
    )
    parser.addoption(
        "--headless",
        action="store_true",
        help="Run browser in headless mode"
    )
    parser.addoption(
        "--base-url",
        action="store",
        help="Base URL for testing"
    )
    parser.addoption(
        "--environment",
        action="store",
        default="test",
        help="Environment to test against (dev, test, staging, prod)"
    )

@pytest.fixture(scope="session", autouse=True)
def configure_from_cli(request):
    """Configure settings from command line options"""
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    base_url = request.config.getoption("--base-url")
    environment = request.config.getoption("--environment")
    
    if browser:
        config.webdriver.browser = browser
    if headless:
        config.webdriver.headless = True
    if base_url:
        config.test.base_url = base_url
    if environment:
        config.test.environment = environment
    
    logger.info(f"Configuration updated from CLI: browser={browser}, headless={headless}")

# Test result collection
test_results = []

@pytest.hookimpl(tryfirst=True)
def pytest_runtest_logreport(report):
    """Collect test results"""
    if report.when == 'call':
        test_results.append({
            'name': report.nodeid,
            'outcome': report.outcome,
            'duration': report.duration,
            'timestamp': datetime.now().isoformat()
        })

@pytest.fixture(scope="session")
def get_test_results():
    """Fixture to access collected test results"""
    return test_results