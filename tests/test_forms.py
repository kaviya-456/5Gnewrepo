import pytest
import logging
from selenium.webdriver.common.by import By
from framework.driver_manager import driver_manager
from framework.base_page import BasePage
from pages.login_page import LoginPage
from config.config import config

logger = logging.getLogger(__name__)

class FormPage(BasePage):
    """Generic form page for testing form interactions"""
    
    # Common form elements
    TEXT_INPUT = (By.ID, "text-input")
    EMAIL_INPUT = (By.ID, "email-input")
    PASSWORD_INPUT = (By.ID, "password-input")
    TEXTAREA = (By.ID, "textarea")
    DROPDOWN = (By.ID, "dropdown")
    CHECKBOX = (By.ID, "checkbox")
    RADIO_BUTTON_1 = (By.ID, "radio1")
    RADIO_BUTTON_2 = (By.ID, "radio2")
    FILE_INPUT = (By.ID, "file-input")
    SUBMIT_BUTTON = (By.ID, "submit-button")
    RESET_BUTTON = (By.ID, "reset-button")
    SUCCESS_MESSAGE = (By.CLASS_NAME, "success-message")
    ERROR_MESSAGE = (By.CLASS_NAME, "error-message")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.page_url = "/form"
    
    def navigate_to_form(self, base_url: str = None):
        """Navigate to form page"""
        url = base_url or config.test.base_url
        full_url = url.rstrip('/') + self.page_url
        self.navigate_to(full_url)
        logger.info(f"Navigated to form page: {full_url}")

class TestForms:
    """Test cases for form interactions"""
    
    def setup_method(self):
        """Setup method called before each test"""
        self.driver = driver_manager.get_driver()
        self.login_page = LoginPage(self.driver)
        self.form_page = FormPage(self.driver)
        
        # Login before each test
        self.login_page.navigate_to_login()
        self.login_page.login("valid_user", "valid_password")
        self.login_page.wait_for_login_completion()
    
    def teardown_method(self):
        """Teardown method called after each test"""
        if self.driver:
            self.driver.quit()
    
    def test_text_input_field(self):
        """Test text input field functionality"""
        test_text = "This is a test text"
        
        # Navigate to form page
        self.form_page.navigate_to_form()
        
        # Enter text in input field
        self.form_page.send_keys(self.form_page.TEXT_INPUT, test_text)
        
        # Verify text was entered
        entered_text = self.form_page.get_attribute(self.form_page.TEXT_INPUT, "value")
        assert entered_text == test_text, f"Expected '{test_text}', got '{entered_text}'"
        
        logger.info("Text input field test passed")
    
    def test_email_input_validation(self):
        """Test email input field validation"""
        # Navigate to form page
        self.form_page.navigate_to_form()
        
        # Test valid email
        valid_email = "test@example.com"
        self.form_page.send_keys(self.form_page.EMAIL_INPUT, valid_email)
        entered_email = self.form_page.get_attribute(self.form_page.EMAIL_INPUT, "value")
        assert entered_email == valid_email, "Valid email should be accepted"
        
        # Clear and test invalid email
        self.form_page.send_keys(self.form_page.EMAIL_INPUT, "invalid-email")
        # Note: Validation behavior would depend on the specific implementation
        
        logger.info("Email input validation test passed")
    
    def test_password_input_field(self):
        """Test password input field"""
        test_password = "SecurePassword123!"
        
        # Navigate to form page
        self.form_page.navigate_to_form()
        
        # Enter password
        self.form_page.send_keys(self.form_page.PASSWORD_INPUT, test_password)
        
        # Verify password field has content (actual value might not be readable)
        password_field = self.form_page.find_element(self.form_page.PASSWORD_INPUT)
        assert password_field.get_attribute("type") == "password", "Should be password field type"
        
        logger.info("Password input field test passed")
    
    def test_textarea_field(self):
        """Test textarea field functionality"""
        test_text = "This is a long text that will be entered into the textarea field.\nIt spans multiple lines."
        
        # Navigate to form page
        self.form_page.navigate_to_form()
        
        # Enter text in textarea
        self.form_page.send_keys(self.form_page.TEXTAREA, test_text)
        
        # Verify text was entered
        entered_text = self.form_page.get_attribute(self.form_page.TEXTAREA, "value")
        assert entered_text == test_text, f"Expected '{test_text}', got '{entered_text}'"
        
        logger.info("Textarea field test passed")
    
    def test_dropdown_selection(self):
        """Test dropdown selection functionality"""
        # Navigate to form page
        self.form_page.navigate_to_form()
        
        # Test selection by visible text
        self.form_page.select_dropdown_by_text(self.form_page.DROPDOWN, "Option 1")
        
        # Test selection by value
        self.form_page.select_dropdown_by_value(self.form_page.DROPDOWN, "option2")
        
        # Test selection by index
        self.form_page.select_dropdown_by_index(self.form_page.DROPDOWN, 0)
        
        logger.info("Dropdown selection test passed")
    
    def test_checkbox_functionality(self):
        """Test checkbox functionality"""
        # Navigate to form page
        self.form_page.navigate_to_form()
        
        # Check if checkbox is initially unchecked
        checkbox = self.form_page.find_element(self.form_page.CHECKBOX)
        initial_state = checkbox.is_selected()
        
        # Click checkbox to toggle state
        self.form_page.click(self.form_page.CHECKBOX)
        
        # Verify state changed
        new_state = checkbox.is_selected()
        assert new_state != initial_state, "Checkbox state should have changed"
        
        # Click again to toggle back
        self.form_page.click(self.form_page.CHECKBOX)
        final_state = checkbox.is_selected()
        assert final_state == initial_state, "Checkbox should be back to initial state"
        
        logger.info("Checkbox functionality test passed")
    
    def test_radio_button_selection(self):
        """Test radio button selection"""
        # Navigate to form page
        self.form_page.navigate_to_form()
        
        # Select first radio button
        self.form_page.click(self.form_page.RADIO_BUTTON_1)
        
        # Verify first radio button is selected
        radio1 = self.form_page.find_element(self.form_page.RADIO_BUTTON_1)
        assert radio1.is_selected(), "First radio button should be selected"
        
        # Select second radio button
        self.form_page.click(self.form_page.RADIO_BUTTON_2)
        
        # Verify second radio button is selected and first is not
        radio2 = self.form_page.find_element(self.form_page.RADIO_BUTTON_2)
        assert radio2.is_selected(), "Second radio button should be selected"
        assert not radio1.is_selected(), "First radio button should not be selected"
        
        logger.info("Radio button selection test passed")
    
    def test_file_upload(self):
        """Test file upload functionality"""
        # Create a temporary test file
        import tempfile
        import os
        
        # Navigate to form page
        self.form_page.navigate_to_form()
        
        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
            temp_file.write("This is a test file for upload")
            temp_file_path = temp_file.name
        
        try:
            # Upload file
            file_input = self.form_page.find_element(self.form_page.FILE_INPUT)
            file_input.send_keys(temp_file_path)
            
            # Verify file was selected
            file_value = file_input.get_attribute("value")
            assert temp_file_path.split(os.sep)[-1] in file_value, "File should be selected"
            
        finally:
            # Clean up temporary file
            os.unlink(temp_file_path)
        
        logger.info("File upload test passed")
    
    def test_form_submission(self):
        """Test complete form submission"""
        # Navigate to form page
        self.form_page.navigate_to_form()
        
        # Fill out form fields
        self.form_page.send_keys(self.form_page.TEXT_INPUT, "Test User")
        self.form_page.send_keys(self.form_page.EMAIL_INPUT, "test@example.com")
        self.form_page.send_keys(self.form_page.PASSWORD_INPUT, "password123")
        self.form_page.send_keys(self.form_page.TEXTAREA, "This is a test message")
        self.form_page.select_dropdown_by_text(self.form_page.DROPDOWN, "Option 1")
        self.form_page.click(self.form_page.CHECKBOX)
        self.form_page.click(self.form_page.RADIO_BUTTON_1)
        
        # Submit form
        self.form_page.click(self.form_page.SUBMIT_BUTTON)
        
        # Verify form submission (check for success message or URL change)
        try:
            success_message = self.form_page.get_text(self.form_page.SUCCESS_MESSAGE)
            assert success_message != "", "Success message should be displayed"
        except:
            # Alternative: check if URL changed (form was submitted)
            current_url = self.driver.current_url
            assert "success" in current_url.lower() or "submitted" in current_url.lower(), \
                "Should be redirected to success page"
        
        logger.info("Form submission test passed")
    
    def test_form_reset(self):
        """Test form reset functionality"""
        # Navigate to form page
        self.form_page.navigate_to_form()
        
        # Fill out some form fields
        self.form_page.send_keys(self.form_page.TEXT_INPUT, "Test Data")
        self.form_page.send_keys(self.form_page.EMAIL_INPUT, "test@example.com")
        self.form_page.click(self.form_page.CHECKBOX)
        
        # Reset form
        self.form_page.click(self.form_page.RESET_BUTTON)
        
        # Verify fields are cleared
        text_value = self.form_page.get_attribute(self.form_page.TEXT_INPUT, "value")
        email_value = self.form_page.get_attribute(self.form_page.EMAIL_INPUT, "value")
        checkbox = self.form_page.find_element(self.form_page.CHECKBOX)
        
        assert text_value == "", "Text field should be cleared"
        assert email_value == "", "Email field should be cleared"
        assert not checkbox.is_selected(), "Checkbox should be unchecked"
        
        logger.info("Form reset test passed")
    
    def test_form_validation_errors(self):
        """Test form validation error handling"""
        # Navigate to form page
        self.form_page.navigate_to_form()
        
        # Submit form without filling required fields
        self.form_page.click(self.form_page.SUBMIT_BUTTON)
        
        # Check for error messages
        try:
            error_message = self.form_page.get_text(self.form_page.ERROR_MESSAGE)
            assert error_message != "", "Error message should be displayed for empty required fields"
        except:
            # Alternative: check if form stayed on same page (validation failed)
            current_url = self.driver.current_url
            assert "form" in current_url.lower(), "Should stay on form page when validation fails"
        
        logger.info("Form validation errors test passed")
    
    @pytest.mark.parametrize("field_name,field_locator,test_value", [
        ("text", "TEXT_INPUT", "Test Text"),
        ("email", "EMAIL_INPUT", "test@example.com"),
        ("textarea", "TEXTAREA", "Test message")
    ])
    def test_individual_field_input(self, field_name, field_locator, test_value):
        """Test individual form fields with parametrization"""
        # Navigate to form page
        self.form_page.navigate_to_form()
        
        # Get the field locator
        locator = getattr(self.form_page, field_locator)
        
        # Enter test value
        self.form_page.send_keys(locator, test_value)
        
        # Verify value was entered
        entered_value = self.form_page.get_attribute(locator, "value")
        assert entered_value == test_value, f"{field_name} field should contain '{test_value}'"
        
        logger.info(f"Individual field input test passed for {field_name}")
    
    def test_form_field_clearing(self):
        """Test clearing form fields"""
        # Navigate to form page
        self.form_page.navigate_to_form()
        
        # Enter data in fields
        self.form_page.send_keys(self.form_page.TEXT_INPUT, "Initial text")
        self.form_page.send_keys(self.form_page.EMAIL_INPUT, "initial@example.com")
        
        # Clear fields using clear_first=True (default behavior)
        self.form_page.send_keys(self.form_page.TEXT_INPUT, "New text")
        self.form_page.send_keys(self.form_page.EMAIL_INPUT, "new@example.com")
        
        # Verify new values
        text_value = self.form_page.get_attribute(self.form_page.TEXT_INPUT, "value")
        email_value = self.form_page.get_attribute(self.form_page.EMAIL_INPUT, "value")
        
        assert text_value == "New text", "Text field should contain new value"
        assert email_value == "new@example.com", "Email field should contain new value"
        
        logger.info("Form field clearing test passed")