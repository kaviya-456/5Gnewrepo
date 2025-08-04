from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from typing import Optional
import logging
from config.config import config

logger = logging.getLogger(__name__)

class DriverManager:
    """Manages WebDriver instances for different browsers"""
    
    def __init__(self):
        self._driver: Optional[webdriver.Remote] = None
    
    def get_driver(self, browser: Optional[str] = None) -> webdriver.Remote:
        """Get WebDriver instance for specified browser"""
        browser = browser or config.webdriver.browser
        
        if browser.lower() == "chrome":
            return self._get_chrome_driver()
        elif browser.lower() == "firefox":
            return self._get_firefox_driver()
        elif browser.lower() == "edge":
            return self._get_edge_driver()
        else:
            raise ValueError(f"Unsupported browser: {browser}")
    
    def _get_chrome_driver(self) -> webdriver.Chrome:
        """Setup and return Chrome WebDriver"""
        options = ChromeOptions()
        
        if config.webdriver.headless:
            options.add_argument("--headless")
        
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size={},{}".format(*config.webdriver.window_size))
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-notifications")
        
        if config.webdriver.download_path:
            prefs = {
                "download.default_directory": config.webdriver.download_path,
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True
            }
            options.add_experimental_option("prefs", prefs)
        
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        driver.implicitly_wait(config.webdriver.implicit_wait)
        driver.maximize_window()
        
        return driver
    
    def _get_firefox_driver(self) -> webdriver.Firefox:
        """Setup and return Firefox WebDriver"""
        options = FirefoxOptions()
        
        if config.webdriver.headless:
            options.add_argument("--headless")
        
        options.add_argument("--width={}".format(config.webdriver.window_size[0]))
        options.add_argument("--height={}".format(config.webdriver.window_size[1]))
        
        if config.webdriver.download_path:
            options.set_preference("browser.download.folderList", 2)
            options.set_preference("browser.download.dir", config.webdriver.download_path)
            options.set_preference("browser.helperApps.neverAsk.saveToDisk", 
                                 "application/octet-stream,application/pdf,text/csv")
        
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)
        
        driver.implicitly_wait(config.webdriver.implicit_wait)
        driver.maximize_window()
        
        return driver
    
    def _get_edge_driver(self) -> webdriver.Edge:
        """Setup and return Edge WebDriver"""
        options = EdgeOptions()
        
        if config.webdriver.headless:
            options.add_argument("--headless")
        
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size={},{}".format(*config.webdriver.window_size))
        
        service = EdgeService(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service, options=options)
        
        driver.implicitly_wait(config.webdriver.implicit_wait)
        driver.maximize_window()
        
        return driver
    
    def quit_driver(self):
        """Quit the WebDriver instance"""
        if self._driver:
            try:
                self._driver.quit()
                logger.info("WebDriver quit successfully")
            except Exception as e:
                logger.error(f"Error quitting WebDriver: {e}")
            finally:
                self._driver = None

# Global driver manager instance
driver_manager = DriverManager()