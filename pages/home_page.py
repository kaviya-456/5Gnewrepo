from selenium.webdriver.common.by import By
from framework.base_page import BasePage
import logging

logger = logging.getLogger(__name__)

class HomePage(BasePage):
    """Home page object following Page Object Model pattern"""
    
    # Locators
    WELCOME_MESSAGE = (By.CLASS_NAME, "welcome-message")
    USER_PROFILE_DROPDOWN = (By.ID, "user-profile")
    NAVIGATION_MENU = (By.CLASS_NAME, "navigation-menu")
    SEARCH_BOX = (By.ID, "search")
    SEARCH_BUTTON = (By.ID, "search-button")
    LOGOUT_LINK = (By.LINK_TEXT, "Logout")
    SETTINGS_LINK = (By.LINK_TEXT, "Settings")
    PROFILE_LINK = (By.LINK_TEXT, "Profile")
    NOTIFICATIONS_ICON = (By.CLASS_NAME, "notifications-icon")
    NOTIFICATIONS_COUNT = (By.CLASS_NAME, "notification-count")
    
    # Content sections
    MAIN_CONTENT = (By.ID, "main-content")
    SIDEBAR = (By.ID, "sidebar")
    FOOTER = (By.TAG_NAME, "footer")
    
    # Navigation links
    HOME_LINK = (By.LINK_TEXT, "Home")
    DASHBOARD_LINK = (By.LINK_TEXT, "Dashboard")
    PRODUCTS_LINK = (By.LINK_TEXT, "Products")
    ORDERS_LINK = (By.LINK_TEXT, "Orders")
    REPORTS_LINK = (By.LINK_TEXT, "Reports")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.page_url = "/home"
    
    def navigate_to_home(self, base_url: str = None):
        """Navigate to home page"""
        from config.config import config
        url = base_url or config.test.base_url
        full_url = url.rstrip('/') + self.page_url
        self.navigate_to(full_url)
        logger.info(f"Navigated to home page: {full_url}")
    
    def get_welcome_message(self) -> str:
        """Get welcome message text"""
        if self.is_element_visible(self.WELCOME_MESSAGE):
            message = self.get_text(self.WELCOME_MESSAGE)
            logger.info(f"Welcome message: {message}")
            return message
        return ""
    
    def search(self, search_term: str):
        """Perform search"""
        self.send_keys(self.SEARCH_BOX, search_term)
        self.click(self.SEARCH_BUTTON)
        logger.info(f"Searched for: {search_term}")
    
    def click_user_profile(self):
        """Click user profile dropdown"""
        self.click(self.USER_PROFILE_DROPDOWN)
        logger.info("Clicked user profile dropdown")
    
    def navigate_to_dashboard(self):
        """Navigate to dashboard"""
        self.click(self.DASHBOARD_LINK)
        logger.info("Navigated to dashboard")
    
    def navigate_to_products(self):
        """Navigate to products page"""
        self.click(self.PRODUCTS_LINK)
        logger.info("Navigated to products")
    
    def navigate_to_orders(self):
        """Navigate to orders page"""
        self.click(self.ORDERS_LINK)
        logger.info("Navigated to orders")
    
    def navigate_to_reports(self):
        """Navigate to reports page"""
        self.click(self.REPORTS_LINK)
        logger.info("Navigated to reports")
    
    def navigate_to_settings(self):
        """Navigate to settings page"""
        self.click_user_profile()
        self.click(self.SETTINGS_LINK)
        logger.info("Navigated to settings")
    
    def navigate_to_profile(self):
        """Navigate to profile page"""
        self.click_user_profile()
        self.click(self.PROFILE_LINK)
        logger.info("Navigated to profile")
    
    def logout(self):
        """Logout from the application"""
        self.click_user_profile()
        self.click(self.LOGOUT_LINK)
        logger.info("Logged out from application")
    
    def get_notifications_count(self) -> int:
        """Get number of notifications"""
        if self.is_element_visible(self.NOTIFICATIONS_COUNT):
            count_text = self.get_text(self.NOTIFICATIONS_COUNT)
            try:
                count = int(count_text)
                logger.info(f"Notifications count: {count}")
                return count
            except ValueError:
                logger.warning(f"Could not parse notifications count: {count_text}")
        return 0
    
    def click_notifications(self):
        """Click notifications icon"""
        self.click(self.NOTIFICATIONS_ICON)
        logger.info("Clicked notifications icon")
    
    def is_page_loaded(self) -> bool:
        """Check if home page is properly loaded"""
        return (
            self.is_element_visible(self.MAIN_CONTENT) and
            self.is_element_visible(self.NAVIGATION_MENU)
        )
    
    def wait_for_page_load_complete(self, timeout: int = 10):
        """Wait for home page to load completely"""
        self.wait_for_element_visible(self.MAIN_CONTENT, timeout)
        self.wait_for_element_visible(self.NAVIGATION_MENU, timeout)
        logger.info("Home page loaded completely")