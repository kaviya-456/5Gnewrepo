import pytest
import logging
from framework.driver_manager import driver_manager
from pages.login_page import LoginPage
from pages.home_page import HomePage
from config.config import config

logger = logging.getLogger(__name__)

class TestLogin:
    """Test cases for login functionality"""
    
    def setup_method(self):
        """Setup method called before each test"""
        self.driver = driver_manager.get_driver()
        self.login_page = LoginPage(self.driver)
        self.home_page = HomePage(self.driver)
    
    def teardown_method(self):
        """Teardown method called after each test"""
        if self.driver:
            self.driver.quit()
    
    def test_valid_login(self):
        """Test login with valid credentials"""
        # Test data
        username = "valid_user"
        password = "valid_password"
        
        # Navigate to login page
        self.login_page.navigate_to_login()
        
        # Perform login
        self.login_page.login(username, password)
        
        # Wait for login completion
        self.login_page.wait_for_login_completion()
        
        # Verify successful login
        assert self.login_page.is_logged_in(), "Login should be successful"
        
        # Verify we're on home page
        assert "home" in self.driver.current_url.lower() or self.home_page.is_page_loaded()
        
        logger.info("Valid login test passed")
    
    def test_invalid_username(self):
        """Test login with invalid username"""
        # Test data
        username = "invalid_user"
        password = "valid_password"
        
        # Navigate to login page
        self.login_page.navigate_to_login()
        
        # Perform login
        self.login_page.login(username, password)
        
        # Wait for login completion
        self.login_page.wait_for_login_completion()
        
        # Verify login failed
        assert not self.login_page.is_logged_in(), "Login should fail with invalid username"
        
        # Verify error message is displayed
        error_message = self.login_page.get_error_message()
        assert error_message != "", "Error message should be displayed"
        
        logger.info("Invalid username test passed")
    
    def test_invalid_password(self):
        """Test login with invalid password"""
        # Test data
        username = "valid_user"
        password = "invalid_password"
        
        # Navigate to login page
        self.login_page.navigate_to_login()
        
        # Perform login
        self.login_page.login(username, password)
        
        # Wait for login completion
        self.login_page.wait_for_login_completion()
        
        # Verify login failed
        assert not self.login_page.is_logged_in(), "Login should fail with invalid password"
        
        # Verify error message is displayed
        error_message = self.login_page.get_error_message()
        assert error_message != "", "Error message should be displayed"
        
        logger.info("Invalid password test passed")
    
    def test_empty_credentials(self):
        """Test login with empty credentials"""
        # Navigate to login page
        self.login_page.navigate_to_login()
        
        # Attempt login with empty fields
        self.login_page.click_login_button()
        
        # Verify login failed
        assert not self.login_page.is_logged_in(), "Login should fail with empty credentials"
        
        logger.info("Empty credentials test passed")
    
    def test_remember_me_functionality(self):
        """Test remember me checkbox functionality"""
        # Test data
        username = "valid_user"
        password = "valid_password"
        
        # Navigate to login page
        self.login_page.navigate_to_login()
        
        # Perform login with remember me checked
        self.login_page.login(username, password, remember_me=True)
        
        # Wait for login completion
        self.login_page.wait_for_login_completion()
        
        # Verify successful login
        assert self.login_page.is_logged_in(), "Login should be successful with remember me"
        
        logger.info("Remember me functionality test passed")
    
    def test_logout_functionality(self):
        """Test logout functionality"""
        # Test data
        username = "valid_user"
        password = "valid_password"
        
        # Navigate to login page and login
        self.login_page.navigate_to_login()
        self.login_page.login(username, password)
        self.login_page.wait_for_login_completion()
        
        # Verify we're logged in
        assert self.login_page.is_logged_in(), "Should be logged in before logout"
        
        # Perform logout
        self.login_page.logout()
        
        # Verify we're logged out
        assert not self.login_page.is_logged_in(), "Should be logged out after logout"
        
        logger.info("Logout functionality test passed")
    
    @pytest.mark.parametrize("username,password,expected", [
        ("user1", "pass1", False),
        ("user2", "pass2", False),
        ("", "", False),
        ("valid_user", "valid_password", True)
    ])
    def test_login_with_multiple_credentials(self, username, password, expected):
        """Test login with multiple sets of credentials"""
        # Navigate to login page
        self.login_page.navigate_to_login()
        
        # Perform login
        self.login_page.login(username, password)
        
        # Wait for login completion
        self.login_page.wait_for_login_completion()
        
        # Verify result matches expected outcome
        is_logged_in = self.login_page.is_logged_in()
        assert is_logged_in == expected, f"Login result for {username}/{password} should be {expected}"
        
        logger.info(f"Multiple credentials test passed for {username}")
    
    def test_forgot_password_link(self):
        """Test forgot password link functionality"""
        # Navigate to login page
        self.login_page.navigate_to_login()
        
        # Click forgot password link
        self.login_page.click_forgot_password()
        
        # Verify we're redirected to forgot password page
        current_url = self.driver.current_url
        assert "forgot" in current_url.lower() or "reset" in current_url.lower(), \
            "Should be redirected to forgot password page"
        
        logger.info("Forgot password link test passed")
    
    def test_login_form_validation(self):
        """Test login form field validation"""
        # Navigate to login page
        self.login_page.navigate_to_login()
        
        # Test username field
        self.login_page.enter_username("test_user")
        username_value = self.login_page.get_attribute(self.login_page.USERNAME_INPUT, "value")
        assert username_value == "test_user", "Username should be entered correctly"
        
        # Test password field
        self.login_page.enter_password("test_password")
        # Note: Password field value might not be readable for security reasons
        
        # Clear form and verify
        self.login_page.clear_login_form()
        username_value = self.login_page.get_attribute(self.login_page.USERNAME_INPUT, "value")
        assert username_value == "", "Username field should be cleared"
        
        logger.info("Login form validation test passed")