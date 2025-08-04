import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@dataclass
class WebDriverConfig:
    """Configuration for WebDriver settings"""
    browser: str = "chrome"
    headless: bool = False
    implicit_wait: int = 10
    explicit_wait: int = 20
    window_size: tuple = (1920, 1080)
    download_path: Optional[str] = None
    
@dataclass
class TestConfig:
    """Configuration for test execution"""
    base_url: str = os.getenv("BASE_URL", "https://example.com")
    environment: str = os.getenv("ENVIRONMENT", "test")
    screenshot_on_failure: bool = True
    video_recording: bool = False
    retry_failed_tests: int = 2
    
@dataclass
class ReportConfig:
    """Configuration for test reporting"""
    reports_dir: str = "reports"
    screenshots_dir: str = "reports/screenshots"
    logs_dir: str = "reports/logs"
    allure_results_dir: str = "reports/allure-results"
    
class Config:
    """Main configuration class"""
    def __init__(self):
        self.webdriver = WebDriverConfig()
        self.test = TestConfig()
        self.report = ReportConfig()
        
        # Create directories if they don't exist
        self._create_directories()
    
    def _create_directories(self):
        """Create necessary directories for reports and logs"""
        directories = [
            self.report.reports_dir,
            self.report.screenshots_dir,
            self.report.logs_dir,
            self.report.allure_results_dir
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
    
    def update_config_from_env(self):
        """Update configuration from environment variables"""
        # WebDriver config
        self.webdriver.browser = os.getenv("BROWSER", self.webdriver.browser)
        self.webdriver.headless = os.getenv("HEADLESS", "false").lower() == "true"
        self.webdriver.implicit_wait = int(os.getenv("IMPLICIT_WAIT", self.webdriver.implicit_wait))
        
        # Test config
        self.test.base_url = os.getenv("BASE_URL", self.test.base_url)
        self.test.environment = os.getenv("ENVIRONMENT", self.test.environment)
        
# Global configuration instance
config = Config()
config.update_config_from_env()