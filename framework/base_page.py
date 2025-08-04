from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
from typing import List, Optional, Union, Any
import logging
import time
import os
from datetime import datetime
from config.config import config

logger = logging.getLogger(__name__)

class BasePage:
    """Base page class with common selenium operations"""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, config.webdriver.explicit_wait)
        self.actions = ActionChains(driver)
    
    # Navigation methods
    def navigate_to(self, url: str):
        """Navigate to a specific URL"""
        logger.info(f"Navigating to: {url}")
        self.driver.get(url)
    
    def refresh_page(self):
        """Refresh the current page"""
        logger.info("Refreshing page")
        self.driver.refresh()
    
    def go_back(self):
        """Navigate back in browser history"""
        logger.info("Navigating back")
        self.driver.back()
    
    def go_forward(self):
        """Navigate forward in browser history"""
        logger.info("Navigating forward")
        self.driver.forward()
    
    # Element finding methods
    def find_element(self, locator: tuple, timeout: Optional[int] = None) -> WebElement:
        """Find a single element with optional timeout"""
        try:
            wait_time = timeout or config.webdriver.explicit_wait
            element = WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located(locator)
            )
            logger.debug(f"Found element: {locator}")
            return element
        except TimeoutException:
            logger.error(f"Element not found: {locator}")
            raise
    
    def find_elements(self, locator: tuple, timeout: Optional[int] = None) -> List[WebElement]:
        """Find multiple elements with optional timeout"""
        try:
            wait_time = timeout or config.webdriver.explicit_wait
            elements = WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_all_elements_located(locator)
            )
            logger.debug(f"Found {len(elements)} elements: {locator}")
            return elements
        except TimeoutException:
            logger.error(f"Elements not found: {locator}")
            return []
    
    def wait_for_element_visible(self, locator: tuple, timeout: Optional[int] = None) -> WebElement:
        """Wait for element to be visible"""
        wait_time = timeout or config.webdriver.explicit_wait
        return WebDriverWait(self.driver, wait_time).until(
            EC.visibility_of_element_located(locator)
        )
    
    def wait_for_element_clickable(self, locator: tuple, timeout: Optional[int] = None) -> WebElement:
        """Wait for element to be clickable"""
        wait_time = timeout or config.webdriver.explicit_wait
        return WebDriverWait(self.driver, wait_time).until(
            EC.element_to_be_clickable(locator)
        )
    
    def is_element_present(self, locator: tuple) -> bool:
        """Check if element is present in DOM"""
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False
    
    def is_element_visible(self, locator: tuple) -> bool:
        """Check if element is visible"""
        try:
            element = self.driver.find_element(*locator)
            return element.is_displayed()
        except NoSuchElementException:
            return False
    
    # Interaction methods
    def click(self, locator: tuple, timeout: Optional[int] = None):
        """Click on an element"""
        element = self.wait_for_element_clickable(locator, timeout)
        element.click()
        logger.info(f"Clicked element: {locator}")
    
    def double_click(self, locator: tuple, timeout: Optional[int] = None):
        """Double click on an element"""
        element = self.wait_for_element_clickable(locator, timeout)
        self.actions.double_click(element).perform()
        logger.info(f"Double clicked element: {locator}")
    
    def right_click(self, locator: tuple, timeout: Optional[int] = None):
        """Right click on an element"""
        element = self.wait_for_element_clickable(locator, timeout)
        self.actions.context_click(element).perform()
        logger.info(f"Right clicked element: {locator}")
    
    def hover(self, locator: tuple, timeout: Optional[int] = None):
        """Hover over an element"""
        element = self.wait_for_element_visible(locator, timeout)
        self.actions.move_to_element(element).perform()
        logger.info(f"Hovered over element: {locator}")
    
    def send_keys(self, locator: tuple, text: str, clear_first: bool = True, timeout: Optional[int] = None):
        """Send keys to an element"""
        element = self.wait_for_element_visible(locator, timeout)
        if clear_first:
            element.clear()
        element.send_keys(text)
        logger.info(f"Sent keys '{text}' to element: {locator}")
    
    def get_text(self, locator: tuple, timeout: Optional[int] = None) -> str:
        """Get text from an element"""
        element = self.wait_for_element_visible(locator, timeout)
        text = element.text
        logger.debug(f"Got text '{text}' from element: {locator}")
        return text
    
    def get_attribute(self, locator: tuple, attribute: str, timeout: Optional[int] = None) -> str:
        """Get attribute value from an element"""
        element = self.wait_for_element_visible(locator, timeout)
        value = element.get_attribute(attribute)
        logger.debug(f"Got attribute '{attribute}' = '{value}' from element: {locator}")
        return value
    
    # Dropdown/Select methods
    def select_dropdown_by_text(self, locator: tuple, text: str, timeout: Optional[int] = None):
        """Select dropdown option by visible text"""
        element = self.wait_for_element_visible(locator, timeout)
        select = Select(element)
        select.select_by_visible_text(text)
        logger.info(f"Selected dropdown option '{text}' for element: {locator}")
    
    def select_dropdown_by_value(self, locator: tuple, value: str, timeout: Optional[int] = None):
        """Select dropdown option by value"""
        element = self.wait_for_element_visible(locator, timeout)
        select = Select(element)
        select.select_by_value(value)
        logger.info(f"Selected dropdown value '{value}' for element: {locator}")
    
    def select_dropdown_by_index(self, locator: tuple, index: int, timeout: Optional[int] = None):
        """Select dropdown option by index"""
        element = self.wait_for_element_visible(locator, timeout)
        select = Select(element)
        select.select_by_index(index)
        logger.info(f"Selected dropdown index {index} for element: {locator}")
    
    # Window and frame methods
    def switch_to_frame(self, frame_locator: Union[tuple, str, int]):
        """Switch to a frame"""
        if isinstance(frame_locator, tuple):
            frame = self.find_element(frame_locator)
            self.driver.switch_to.frame(frame)
        else:
            self.driver.switch_to.frame(frame_locator)
        logger.info(f"Switched to frame: {frame_locator}")
    
    def switch_to_default_content(self):
        """Switch back to default content"""
        self.driver.switch_to.default_content()
        logger.info("Switched to default content")
    
    def switch_to_window(self, window_handle: str):
        """Switch to a specific window"""
        self.driver.switch_to.window(window_handle)
        logger.info(f"Switched to window: {window_handle}")
    
    def get_window_handles(self) -> List[str]:
        """Get all window handles"""
        return self.driver.window_handles
    
    # JavaScript execution
    def execute_script(self, script: str, *args) -> Any:
        """Execute JavaScript"""
        result = self.driver.execute_script(script, *args)
        logger.debug(f"Executed script: {script}")
        return result
    
    def scroll_to_element(self, locator: tuple, timeout: Optional[int] = None):
        """Scroll to an element"""
        element = self.wait_for_element_visible(locator, timeout)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        logger.info(f"Scrolled to element: {locator}")
    
    def scroll_to_top(self):
        """Scroll to top of page"""
        self.driver.execute_script("window.scrollTo(0, 0);")
        logger.info("Scrolled to top of page")
    
    def scroll_to_bottom(self):
        """Scroll to bottom of page"""
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        logger.info("Scrolled to bottom of page")
    
    # Wait methods
    def wait_for_page_load(self, timeout: Optional[int] = None):
        """Wait for page to fully load"""
        wait_time = timeout or config.webdriver.explicit_wait
        WebDriverWait(self.driver, wait_time).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )
        logger.info("Page fully loaded")
    
    def wait_for_text_in_element(self, locator: tuple, text: str, timeout: Optional[int] = None):
        """Wait for specific text to appear in element"""
        wait_time = timeout or config.webdriver.explicit_wait
        WebDriverWait(self.driver, wait_time).until(
            EC.text_to_be_present_in_element(locator, text)
        )
        logger.info(f"Text '{text}' found in element: {locator}")
    
    def wait_for_url_contains(self, url_part: str, timeout: Optional[int] = None):
        """Wait for URL to contain specific text"""
        wait_time = timeout or config.webdriver.explicit_wait
        WebDriverWait(self.driver, wait_time).until(
            EC.url_contains(url_part)
        )
        logger.info(f"URL contains: {url_part}")
    
    # Utility methods
    def take_screenshot(self, filename: Optional[str] = None) -> str:
        """Take a screenshot and return the file path"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
        
        filepath = os.path.join(config.report.screenshots_dir, filename)
        self.driver.save_screenshot(filepath)
        logger.info(f"Screenshot saved: {filepath}")
        return filepath
    
    def get_page_source(self) -> str:
        """Get page source"""
        return self.driver.page_source
    
    def get_current_url(self) -> str:
        """Get current URL"""
        return self.driver.current_url
    
    def get_page_title(self) -> str:
        """Get page title"""
        return self.driver.title
    
    def wait(self, seconds: int):
        """Wait for specified seconds"""
        time.sleep(seconds)
        logger.info(f"Waited for {seconds} seconds")