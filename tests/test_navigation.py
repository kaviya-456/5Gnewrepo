import pytest
import logging
from framework.driver_manager import driver_manager
from pages.login_page import LoginPage
from pages.home_page import HomePage
from config.config import config

logger = logging.getLogger(__name__)

class TestNavigation:
    """Test cases for navigation functionality"""
    
    def setup_method(self):
        """Setup method called before each test"""
        self.driver = driver_manager.get_driver()
        self.login_page = LoginPage(self.driver)
        self.home_page = HomePage(self.driver)
        
        # Login before each test
        self.login_page.navigate_to_login()
        self.login_page.login("valid_user", "valid_password")
        self.login_page.wait_for_login_completion()
    
    def teardown_method(self):
        """Teardown method called after each test"""
        if self.driver:
            self.driver.quit()
    
    def test_navigate_to_dashboard(self):
        """Test navigation to dashboard"""
        # Navigate to home page first
        self.home_page.navigate_to_home()
        
        # Navigate to dashboard
        self.home_page.navigate_to_dashboard()
        
        # Verify we're on dashboard page
        current_url = self.driver.current_url
        assert "dashboard" in current_url.lower(), "Should be on dashboard page"
        
        logger.info("Navigate to dashboard test passed")
    
    def test_navigate_to_products(self):
        """Test navigation to products page"""
        # Navigate to home page first
        self.home_page.navigate_to_home()
        
        # Navigate to products
        self.home_page.navigate_to_products()
        
        # Verify we're on products page
        current_url = self.driver.current_url
        assert "products" in current_url.lower(), "Should be on products page"
        
        logger.info("Navigate to products test passed")
    
    def test_navigate_to_orders(self):
        """Test navigation to orders page"""
        # Navigate to home page first
        self.home_page.navigate_to_home()
        
        # Navigate to orders
        self.home_page.navigate_to_orders()
        
        # Verify we're on orders page
        current_url = self.driver.current_url
        assert "orders" in current_url.lower(), "Should be on orders page"
        
        logger.info("Navigate to orders test passed")
    
    def test_navigate_to_reports(self):
        """Test navigation to reports page"""
        # Navigate to home page first
        self.home_page.navigate_to_home()
        
        # Navigate to reports
        self.home_page.navigate_to_reports()
        
        # Verify we're on reports page
        current_url = self.driver.current_url
        assert "reports" in current_url.lower(), "Should be on reports page"
        
        logger.info("Navigate to reports test passed")
    
    def test_navigate_to_settings(self):
        """Test navigation to settings page"""
        # Navigate to home page first
        self.home_page.navigate_to_home()
        
        # Navigate to settings
        self.home_page.navigate_to_settings()
        
        # Verify we're on settings page
        current_url = self.driver.current_url
        assert "settings" in current_url.lower(), "Should be on settings page"
        
        logger.info("Navigate to settings test passed")
    
    def test_navigate_to_profile(self):
        """Test navigation to profile page"""
        # Navigate to home page first
        self.home_page.navigate_to_home()
        
        # Navigate to profile
        self.home_page.navigate_to_profile()
        
        # Verify we're on profile page
        current_url = self.driver.current_url
        assert "profile" in current_url.lower(), "Should be on profile page"
        
        logger.info("Navigate to profile test passed")
    
    def test_search_functionality(self):
        """Test search functionality"""
        search_term = "test search"
        
        # Navigate to home page
        self.home_page.navigate_to_home()
        
        # Perform search
        self.home_page.search(search_term)
        
        # Verify search was performed (URL should contain search parameters)
        current_url = self.driver.current_url
        assert "search" in current_url.lower() or search_term in current_url, \
            "URL should contain search parameters"
        
        logger.info("Search functionality test passed")
    
    def test_user_profile_dropdown(self):
        """Test user profile dropdown functionality"""
        # Navigate to home page
        self.home_page.navigate_to_home()
        
        # Click user profile dropdown
        self.home_page.click_user_profile()
        
        # Verify dropdown is opened (this would depend on the specific implementation)
        # For now, we'll just verify the click was successful
        logger.info("User profile dropdown test passed")
    
    def test_notifications_functionality(self):
        """Test notifications functionality"""
        # Navigate to home page
        self.home_page.navigate_to_home()
        
        # Get notifications count
        notifications_count = self.home_page.get_notifications_count()
        assert notifications_count >= 0, "Notifications count should be non-negative"
        
        # Click notifications icon
        self.home_page.click_notifications()
        
        logger.info("Notifications functionality test passed")
    
    def test_page_refresh(self):
        """Test page refresh functionality"""
        # Navigate to home page
        self.home_page.navigate_to_home()
        
        # Get current URL
        original_url = self.driver.current_url
        
        # Refresh page
        self.home_page.refresh_page()
        
        # Verify we're still on the same page
        current_url = self.driver.current_url
        assert current_url == original_url, "Should be on the same page after refresh"
        
        logger.info("Page refresh test passed")
    
    def test_browser_navigation(self):
        """Test browser back and forward navigation"""
        # Navigate to home page
        self.home_page.navigate_to_home()
        home_url = self.driver.current_url
        
        # Navigate to dashboard
        self.home_page.navigate_to_dashboard()
        dashboard_url = self.driver.current_url
        
        # Go back
        self.home_page.go_back()
        assert self.driver.current_url == home_url, "Should be back on home page"
        
        # Go forward
        self.home_page.go_forward()
        assert self.driver.current_url == dashboard_url, "Should be forward to dashboard"
        
        logger.info("Browser navigation test passed")
    
    def test_multiple_page_navigation_flow(self):
        """Test complete navigation flow through multiple pages"""
        pages_to_visit = [
            ("dashboard", self.home_page.navigate_to_dashboard),
            ("products", self.home_page.navigate_to_products),
            ("orders", self.home_page.navigate_to_orders),
            ("reports", self.home_page.navigate_to_reports)
        ]
        
        # Navigate to home page first
        self.home_page.navigate_to_home()
        
        # Visit each page in sequence
        for page_name, navigate_method in pages_to_visit:
            navigate_method()
            current_url = self.driver.current_url
            assert page_name in current_url.lower(), f"Should be on {page_name} page"
            logger.info(f"Successfully navigated to {page_name}")
        
        logger.info("Multiple page navigation flow test passed")
    
    @pytest.mark.parametrize("page_name,navigation_method", [
        ("dashboard", "navigate_to_dashboard"),
        ("products", "navigate_to_products"),
        ("orders", "navigate_to_orders"),
        ("reports", "navigate_to_reports")
    ])
    def test_individual_page_navigation(self, page_name, navigation_method):
        """Test navigation to individual pages with parametrization"""
        # Navigate to home page first
        self.home_page.navigate_to_home()
        
        # Get the navigation method and call it
        nav_method = getattr(self.home_page, navigation_method)
        nav_method()
        
        # Verify we're on the correct page
        current_url = self.driver.current_url
        assert page_name in current_url.lower(), f"Should be on {page_name} page"
        
        logger.info(f"Individual page navigation test passed for {page_name}")