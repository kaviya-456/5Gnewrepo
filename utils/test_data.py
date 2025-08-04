import json
import csv
import os
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)

class TestDataManager:
    """Manages test data from various sources"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self._ensure_data_directory()
    
    def _ensure_data_directory(self):
        """Ensure data directory exists"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            logger.info(f"Created data directory: {self.data_dir}")
    
    def load_json_data(self, filename: str) -> Dict[str, Any]:
        """Load test data from JSON file"""
        filepath = os.path.join(self.data_dir, filename)
        
        if not os.path.exists(filepath):
            logger.warning(f"JSON file not found: {filepath}")
            return {}
        
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                data = json.load(file)
                logger.info(f"Loaded JSON data from: {filepath}")
                return data
        except Exception as e:
            logger.error(f"Error loading JSON data from {filepath}: {e}")
            return {}
    
    def save_json_data(self, data: Dict[str, Any], filename: str):
        """Save test data to JSON file"""
        filepath = os.path.join(self.data_dir, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=2, ensure_ascii=False)
                logger.info(f"Saved JSON data to: {filepath}")
        except Exception as e:
            logger.error(f"Error saving JSON data to {filepath}: {e}")
    
    def load_csv_data(self, filename: str) -> List[Dict[str, str]]:
        """Load test data from CSV file"""
        filepath = os.path.join(self.data_dir, filename)
        
        if not os.path.exists(filepath):
            logger.warning(f"CSV file not found: {filepath}")
            return []
        
        try:
            data = []
            with open(filepath, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    data.append(row)
                logger.info(f"Loaded CSV data from: {filepath} ({len(data)} rows)")
                return data
        except Exception as e:
            logger.error(f"Error loading CSV data from {filepath}: {e}")
            return []
    
    def save_csv_data(self, data: List[Dict[str, str]], filename: str):
        """Save test data to CSV file"""
        if not data:
            logger.warning("No data to save to CSV")
            return
        
        filepath = os.path.join(self.data_dir, filename)
        
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as file:
                fieldnames = data[0].keys()
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
                logger.info(f"Saved CSV data to: {filepath} ({len(data)} rows)")
        except Exception as e:
            logger.error(f"Error saving CSV data to {filepath}: {e}")
    
    def get_user_credentials(self, user_type: str = "default") -> Dict[str, str]:
        """Get user credentials from test data"""
        credentials_data = self.load_json_data("credentials.json")
        
        if user_type in credentials_data:
            return credentials_data[user_type]
        
        # Default credentials if specific type not found
        return {
            "username": "valid_user",
            "password": "valid_password"
        }
    
    def get_test_urls(self) -> Dict[str, str]:
        """Get test URLs from configuration"""
        urls_data = self.load_json_data("urls.json")
        
        if urls_data:
            return urls_data
        
        # Default URLs if file not found
        return {
            "base_url": "https://example.com",
            "login_url": "https://example.com/login",
            "dashboard_url": "https://example.com/dashboard",
            "api_url": "https://api.example.com"
        }
    
    def get_form_data(self, form_name: str = "default") -> Dict[str, Any]:
        """Get form test data"""
        form_data = self.load_json_data("form_data.json")
        
        if form_name in form_data:
            return form_data[form_name]
        
        # Default form data
        return {
            "text_input": "Test text",
            "email": "test@example.com",
            "password": "TestPassword123!",
            "textarea": "This is a test message",
            "dropdown_value": "option1",
            "checkbox": True,
            "radio": "option1"
        }

# Sample test data files content
SAMPLE_CREDENTIALS = {
    "valid_user": {
        "username": "testuser@example.com",
        "password": "SecurePassword123!"
    },
    "admin_user": {
        "username": "admin@example.com",
        "password": "AdminPass456!"
    },
    "invalid_user": {
        "username": "invalid@example.com",
        "password": "wrongpassword"
    }
}

SAMPLE_URLS = {
    "production": {
        "base_url": "https://app.example.com",
        "api_url": "https://api.example.com"
    },
    "staging": {
        "base_url": "https://staging.example.com",
        "api_url": "https://api-staging.example.com"
    },
    "development": {
        "base_url": "https://dev.example.com",
        "api_url": "https://api-dev.example.com"
    }
}

SAMPLE_FORM_DATA = {
    "registration": {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "password": "SecurePass123!",
        "confirm_password": "SecurePass123!",
        "phone": "+1234567890",
        "country": "United States",
        "terms_accepted": True
    },
    "contact": {
        "name": "Test User",
        "email": "test@example.com",
        "subject": "Test Inquiry",
        "message": "This is a test message for contact form validation.",
        "priority": "normal"
    },
    "profile": {
        "display_name": "Test User",
        "bio": "Software tester with automation experience",
        "website": "https://testuser.example.com",
        "location": "Test City, TC",
        "notifications_enabled": True
    }
}

def create_sample_data_files():
    """Create sample test data files"""
    data_manager = TestDataManager()
    
    # Create sample files
    data_manager.save_json_data(SAMPLE_CREDENTIALS, "credentials.json")
    data_manager.save_json_data(SAMPLE_URLS, "urls.json")
    data_manager.save_json_data(SAMPLE_FORM_DATA, "form_data.json")
    
    # Create sample CSV data
    csv_data = [
        {"username": "user1@example.com", "password": "pass1", "role": "user"},
        {"username": "user2@example.com", "password": "pass2", "role": "user"},
        {"username": "admin@example.com", "password": "adminpass", "role": "admin"}
    ]
    data_manager.save_csv_data(csv_data, "users.csv")
    
    logger.info("Sample test data files created")

# Global test data manager instance
test_data = TestDataManager()