# Selenium Test Automation Framework

A comprehensive, production-ready Selenium automation framework built with Python, featuring Page Object Model, parallel execution, detailed reporting, and CI/CD integration.

## 🚀 Features

- **Page Object Model (POM)** - Maintainable and scalable test structure
- **Multi-browser Support** - Chrome, Firefox, Edge with automatic driver management
- **Parallel Execution** - Run tests in parallel for faster execution
- **Rich Reporting** - HTML reports, Allure integration, screenshots on failure
- **Configuration Management** - Environment-based configuration with .env support
- **Test Data Management** - JSON/CSV data management with sample data
- **CI/CD Ready** - GitHub Actions workflow included
- **Logging** - Comprehensive logging with file and console output
- **Cross-platform** - Works on Windows, macOS, and Linux

## 📁 Project Structure

```
selenium-automation/
├── config/                 # Configuration management
│   ├── __init__.py
│   └── config.py
├── framework/              # Core framework components
│   ├── __init__.py
│   ├── base_page.py       # Base page class with common methods
│   └── driver_manager.py  # WebDriver management
├── pages/                  # Page Object Model classes
│   ├── __init__.py
│   ├── login_page.py
│   └── home_page.py
├── tests/                  # Test cases
│   ├── __init__.py
│   ├── test_login.py
│   ├── test_navigation.py
│   └── test_forms.py
├── utils/                  # Utility functions
│   ├── __init__.py
│   ├── logger.py
│   └── test_data.py
├── data/                   # Test data files (auto-created)
│   ├── credentials.json
│   ├── urls.json
│   └── form_data.json
├── reports/                # Test reports and artifacts
│   ├── screenshots/
│   ├── logs/
│   ├── allure-results/
│   └── allure-report/
├── .github/workflows/      # CI/CD workflows
│   └── test.yml
├── conftest.py            # Pytest configuration and fixtures
├── pytest.ini            # Pytest settings
├── requirements.txt       # Python dependencies
├── run_tests.py          # Main test runner script
├── run_tests.sh          # Shell script for easy execution
├── .env.example          # Environment variables example
└── README.md             # This file
```

## 🛠️ Installation

### Prerequisites

- Python 3.8+ 
- pip (Python package manager)
- Git

### Quick Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd selenium-automation
   ```

2. **Create virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup environment:**
   ```bash
   python run_tests.py --setup
   ```

5. **Copy and configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your specific configuration
   ```

## 🏃‍♂️ Quick Start

### Using Python Script

```bash
# Run all tests
python run_tests.py

# Run specific test suite
python run_tests.py --smoke
python run_tests.py --regression

# Run with specific browser
python run_tests.py --browser firefox --headless

# Run tests in parallel
python run_tests.py --parallel --workers 4

# Run specific test file
python run_tests.py tests/test_login.py
```

### Using Shell Script (Linux/macOS)

```bash
# Make script executable
chmod +x run_tests.sh

# Run tests
./run_tests.sh smoke
./run_tests.sh regression
./run_tests.sh all --browser=firefox
./run_tests.sh parallel --workers=8
```

### Using pytest directly

```bash
# Basic execution
pytest tests/

# With custom options
pytest tests/ --browser chrome --headless --environment staging

# Run with markers
pytest -m smoke
pytest -m "login and not slow"

# Parallel execution
pytest -n 4 tests/
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

```env
# Application URLs
BASE_URL=https://your-app.com
ENVIRONMENT=test

# WebDriver Configuration
BROWSER=chrome
HEADLESS=false
IMPLICIT_WAIT=10
EXPLICIT_WAIT=20

# Test Configuration
SCREENSHOT_ON_FAILURE=true
RETRY_FAILED_TESTS=2
```

### Browser Configuration

The framework supports multiple browsers with automatic driver management:

- **Chrome** (default)
- **Firefox**
- **Edge**

WebDriver binaries are automatically downloaded and managed using `webdriver-manager`.

### Test Data Configuration

Test data is managed through JSON/CSV files in the `data/` directory:

```python
# Access test data in tests
from utils.test_data import test_data

credentials = test_data.get_user_credentials("valid_user")
form_data = test_data.get_form_data("registration")
```

## 📝 Writing Tests

### Page Object Example

```python
# pages/login_page.py
from selenium.webdriver.common.by import By
from framework.base_page import BasePage

class LoginPage(BasePage):
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    
    def login(self, username, password):
        self.send_keys(self.USERNAME_INPUT, username)
        self.send_keys(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)
```

### Test Example

```python
# tests/test_login.py
import pytest
from pages.login_page import LoginPage

class TestLogin:
    def test_valid_login(self, driver):
        login_page = LoginPage(driver)
        login_page.navigate_to_login()
        login_page.login("testuser", "password123")
        assert login_page.is_logged_in()
```

### Available Fixtures

- `driver` - WebDriver instance
- `driver_with_login` - Pre-authenticated WebDriver
- `test_data_manager` - Test data access
- `browser_config` - Browser configuration
- `screenshot_on_failure` - Automatic failure screenshots

## 📊 Reporting

### HTML Reports

HTML reports are generated automatically and include:
- Test execution summary
- Failed test details
- Screenshots of failures
- Execution logs

### Allure Reports

For advanced reporting with Allure:

```bash
# Install Allure (macOS)
brew install allure

# Install Allure (Linux)
# Follow: https://docs.qameta.io/allure/#_installing_a_commandline

# Generate and serve report
python run_tests.py --report allure --generate-allure
allure serve reports/allure-results
```

### Screenshots

Screenshots are automatically captured on test failures and saved to `reports/screenshots/`.

## 🔧 Advanced Usage

### Parallel Execution

```bash
# Run tests in parallel with 4 workers
python run_tests.py --parallel --workers 4

# Use pytest-xdist directly
pytest -n auto tests/
```

### Custom Markers

```bash
# Run only smoke tests
pytest -m smoke

# Run regression tests excluding slow ones
pytest -m "regression and not slow"

# Skip CI-specific tests
pytest -m "not skip_ci"
```

### Multi-browser Testing

```python
@pytest.mark.parametrize("browser", ["chrome", "firefox"])
def test_cross_browser(browser):
    # Test will run on both browsers
    pass
```

### Environment-specific Testing

```bash
# Test against different environments
python run_tests.py --environment staging --base-url https://staging.example.com
python run_tests.py --environment production --base-url https://app.example.com
```

## 🔄 CI/CD Integration

### GitHub Actions

The included workflow (`.github/workflows/test.yml`) provides:

- Multi-Python version testing (3.8, 3.9, 3.10, 3.11)
- Multi-browser testing (Chrome, Firefox)
- Parallel test execution
- Security scanning with Safety and Bandit
- Code quality checks with flake8, black, isort
- Automatic report generation
- Artifact uploads for test results

### Triggering CI Tests

```bash
# Manual trigger with full test suite
git commit -m "feat: new feature [full-test]"

# Daily scheduled runs (configured in workflow)
# Runs at 2 AM UTC every day
```

### Custom CI Commands

```bash
# CI-optimized test run
python run_tests.py --headless --parallel --browser chrome -m "not slow"
```

## 🐛 Troubleshooting

### Common Issues

1. **WebDriver Issues**
   ```bash
   # Clear WebDriver cache
   rm -rf ~/.wdm
   
   # Reinstall webdriver-manager
   pip uninstall webdriver-manager
   pip install webdriver-manager
   ```

2. **Browser Not Found**
   ```bash
   # Install Chrome (Ubuntu)
   wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
   sudo apt-get update
   sudo apt-get install google-chrome-stable
   
   # Install Firefox (Ubuntu)
   sudo apt-get install firefox
   ```

3. **Permission Issues**
   ```bash
   # Make scripts executable
   chmod +x run_tests.sh
   ```

4. **Port Already in Use**
   ```bash
   # Kill processes using port 4444 (Selenium Grid)
   sudo lsof -ti:4444 | xargs kill -9
   ```

### Debug Mode

```bash
# Enable verbose logging
python run_tests.py --debug

# Dry run to see commands
python run_tests.py --dry-run

# Run single test with maximum verbosity
pytest tests/test_login.py::TestLogin::test_valid_login -v -s
```

## 📚 Best Practices

### Test Organization

1. **Group related tests** in classes
2. **Use descriptive test names**
3. **Keep tests independent** and idempotent
4. **Use appropriate markers** for test categorization

### Page Objects

1. **Keep locators at class level**
2. **Implement reusable methods**
3. **Use meaningful method names**
4. **Handle waits appropriately**

### Data Management

1. **Separate test data** from test logic
2. **Use environment-specific data**
3. **Avoid hardcoded values**
4. **Implement data cleanup**

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Make your changes
4. Run tests: `python run_tests.py --smoke`
5. Commit changes: `git commit -m "feat: add new feature"`
6. Push to branch: `git push origin feature/new-feature`
7. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

- **Documentation**: Check this README and inline code comments
- **Issues**: Create GitHub issues for bugs or feature requests
- **Discussions**: Use GitHub Discussions for questions

## 🔗 Useful Links

- [Selenium Documentation](https://selenium-python.readthedocs.io/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Allure Framework](https://docs.qameta.io/allure/)
- [WebDriver Manager](https://github.com/SergeyPirogov/webdriver_manager)

---

**Happy Testing! 🎉**