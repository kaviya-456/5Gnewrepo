from selenium.webdriver.common.by import By
from framework.base_page import BasePage
import logging

logger = logging.getLogger(__name__)

class LoginPage(BasePage):
    """Login page object following Page Object Model pattern"""
    
    # Locators
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    REMEMBER_ME_CHECKBOX = (By.ID, "remember-me")
    FORGOT_PASSWORD_LINK = (By.LINK_TEXT, "Forgot Password?")
    ERROR_MESSAGE = (By.CLASS_NAME, "error-message")
    SUCCESS_MESSAGE = (By.CLASS_NAME, "success-message")
    LOGOUT_BUTTON = (By.ID, "logout")
    
    # Alternative locators (in case primary ones don't work)
    USERNAME_INPUT_ALT = (By.NAME, "username")
    PASSWORD_INPUT_ALT = (By.NAME, "password")
    LOGIN_BUTTON_ALT = (By.XPATH, "//button[@type='submit']")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.page_url = "/login"
    
    def navigate_to_login(self, base_url: str = None):
        """Navigate to login page"""
        from config.config import config
        url = base_url or config.test.base_url
        full_url = url.rstrip('/') + self.page_url
        self.navigate_to(full_url)
        logger.info(f"Navigated to login page: {full_url}")
    
    def enter_username(self, username: str):
        """Enter username in the username field"""
        try:
            self.send_keys(self.USERNAME_INPUT, username)
        except Exception:
            # Try alternative locator
            self.send_keys(self.USERNAME_INPUT_ALT, username)
        logger.info(f"Entered username: {username}")
    
    def enter_password(self, password: str):
        """Enter password in the password field"""
        try:
            self.send_keys(self.PASSWORD_INPUT, password)
        except Exception:
            # Try alternative locator
            self.send_keys(self.PASSWORD_INPUT_ALT, password)
        logger.info("Entered password")
    
    def click_login_button(self):
        """Click the login button"""
        try:
            self.click(self.LOGIN_BUTTON)
        except Exception:
            # Try alternative locator
            self.click(self.LOGIN_BUTTON_ALT)
        logger.info("Clicked login button")
    
    def check_remember_me(self):
        """Check the remember me checkbox"""
        self.click(self.REMEMBER_ME_CHECKBOX)
        logger.info("Checked remember me checkbox")
    
    def click_forgot_password(self):
        """Click the forgot password link"""
        self.click(self.FORGOT_PASSWORD_LINK)
        logger.info("Clicked forgot password link")
    
    def login(self, username: str, password: str, remember_me: bool = False):
        """Complete login flow"""
        logger.info(f"Logging in with username: {username}")
        self.enter_username(username)
        self.enter_password(password)
        
        if remember_me:
            self.check_remember_me()
        
        self.click_login_button()
        logger.info("Login attempt completed")
    
    def logout(self):
        """Logout if logout button is present"""
        if self.is_element_present(self.LOGOUT_BUTTON):
            self.click(self.LOGOUT_BUTTON)
            logger.info("Logged out successfully")
        else:
            logger.warning("Logout button not found")
    
    def get_error_message(self) -> str:
        """Get error message text"""
        if self.is_element_visible(self.ERROR_MESSAGE):
            message = self.get_text(self.ERROR_MESSAGE)
            logger.info(f"Error message found: {message}")
            return message
        return ""
    
    def get_success_message(self) -> str:
        """Get success message text"""
        if self.is_element_visible(self.SUCCESS_MESSAGE):
            message = self.get_text(self.SUCCESS_MESSAGE)
            logger.info(f"Success message found: {message}")
            return message
        return ""
    
    def is_logged_in(self) -> bool:
        """Check if user is logged in by looking for logout button"""
        is_logged_in = self.is_element_present(self.LOGOUT_BUTTON)
        logger.info(f"User logged in status: {is_logged_in}")
        return is_logged_in
    
    def wait_for_login_completion(self, timeout: int = 10):
        """Wait for login to complete (either success or error)"""
        try:
            # Wait for either logout button (success) or error message
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            
            WebDriverWait(self.driver, timeout).until(
                lambda driver: (
                    self.is_element_present(self.LOGOUT_BUTTON) or
                    self.is_element_visible(self.ERROR_MESSAGE) or
                    self.is_element_visible(self.SUCCESS_MESSAGE)
                )
            )
            logger.info("Login completion detected")
        except Exception as e:
            logger.error(f"Timeout waiting for login completion: {e}")
    
    def clear_login_form(self):
        """Clear username and password fields"""
        try:
            username_field = self.find_element(self.USERNAME_INPUT)
            username_field.clear()
        except Exception:
            username_field = self.find_element(self.USERNAME_INPUT_ALT)
            username_field.clear()
        
        try:
            password_field = self.find_element(self.PASSWORD_INPUT)
            password_field.clear()
        except Exception:
            password_field = self.find_element(self.PASSWORD_INPUT_ALT)
            password_field.clear()
        
        logger.info("Cleared login form fields")