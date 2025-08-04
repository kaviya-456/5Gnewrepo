#!/usr/bin/env python3
"""
Main test runner script for Selenium automation framework
Provides easy command-line interface for running tests with various options
"""

import argparse
import os
import sys
import subprocess
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Optional

# Add current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from config.config import config
from utils.logger import setup_logging
from utils.test_data import create_sample_data_files

logger = logging.getLogger(__name__)

class TestRunner:
    """Main test runner class"""
    
    def __init__(self):
        self.setup_logging()
        self.ensure_dependencies()
    
    def setup_logging(self):
        """Setup logging for the test runner"""
        setup_logging()
        logger.info("Test runner initialized")
    
    def ensure_dependencies(self):
        """Ensure all dependencies are available"""
        try:
            import selenium
            import pytest
            logger.info("All dependencies are available")
        except ImportError as e:
            logger.error(f"Missing dependency: {e}")
            logger.info("Please install dependencies: pip install -r requirements.txt")
            sys.exit(1)
    
    def create_test_data(self):
        """Create sample test data files"""
        try:
            create_sample_data_files()
            logger.info("Test data files created/updated")
        except Exception as e:
            logger.warning(f"Could not create test data files: {e}")
    
    def run_tests(self, 
                  test_path: Optional[str] = None,
                  browser: str = "chrome",
                  headless: bool = False,
                  environment: str = "test",
                  base_url: Optional[str] = None,
                  markers: Optional[List[str]] = None,
                  parallel: bool = False,
                  workers: int = 4,
                  report_format: str = "html",
                  verbose: bool = True,
                  dry_run: bool = False,
                  **kwargs) -> int:
        """
        Run tests with specified parameters
        
        Args:
            test_path: Path to specific test file or directory
            browser: Browser to use (chrome, firefox, edge)
            headless: Run browser in headless mode
            environment: Environment to test against
            base_url: Base URL for testing
            markers: Test markers to include/exclude
            parallel: Run tests in parallel
            workers: Number of parallel workers
            report_format: Report format (html, allure, both)
            verbose: Verbose output
            dry_run: Just show what would be executed
            
        Returns:
            Exit code (0 for success, non-zero for failure)
        """
        
        # Build pytest command
        cmd = ["python", "-m", "pytest"]
        
        # Add test path
        if test_path:
            cmd.append(test_path)
        else:
            cmd.append("tests/")
        
        # Add browser configuration
        cmd.extend(["--browser", browser])
        if headless:
            cmd.append("--headless")
        
        # Add environment configuration
        cmd.extend(["--environment", environment])
        if base_url:
            cmd.extend(["--base-url", base_url])
        
        # Add markers
        if markers:
            for marker in markers:
                if marker.startswith("-"):
                    cmd.extend(["-m", f"not {marker[1:]}"])
                else:
                    cmd.extend(["-m", marker])
        
        # Add parallel execution
        if parallel:
            cmd.extend(["-n", str(workers)])
        
        # Add reporting
        if report_format in ["html", "both"]:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_file = f"reports/report_{timestamp}.html"
            cmd.extend(["--html", report_file, "--self-contained-html"])
        
        if report_format in ["allure", "both"]:
            cmd.extend(["--alluredir", "reports/allure-results"])
        
        # Add verbosity
        if verbose:
            cmd.append("-v")
        else:
            cmd.append("-q")
        
        # Add any additional pytest arguments
        for key, value in kwargs.items():
            if value is True:
                cmd.append(f"--{key.replace('_', '-')}")
            elif value is not False and value is not None:
                cmd.extend([f"--{key.replace('_', '-')}", str(value)])
        
        logger.info(f"Running command: {' '.join(cmd)}")
        
        if dry_run:
            print("DRY RUN - Command that would be executed:")
            print(' '.join(cmd))
            return 0
        
        # Execute command
        try:
            result = subprocess.run(cmd, cwd=Path(__file__).parent)
            return result.returncode
        except KeyboardInterrupt:
            logger.info("Test execution interrupted by user")
            return 130
        except Exception as e:
            logger.error(f"Error running tests: {e}")
            return 1
    
    def install_dependencies(self):
        """Install required dependencies"""
        logger.info("Installing dependencies...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                         check=True)
            logger.info("Dependencies installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to install dependencies: {e}")
            return False
    
    def setup_environment(self):
        """Setup test environment"""
        logger.info("Setting up test environment...")
        
        # Create necessary directories
        config._create_directories()
        
        # Create sample data files
        self.create_test_data()
        
        logger.info("Environment setup complete")
    
    def generate_allure_report(self):
        """Generate Allure report"""
        try:
            subprocess.run(["allure", "generate", "reports/allure-results", 
                          "-o", "reports/allure-report", "--clean"], check=True)
            logger.info("Allure report generated in reports/allure-report/")
            return True
        except subprocess.CalledProcessError:
            logger.error("Failed to generate Allure report. Is Allure installed?")
            return False
        except FileNotFoundError:
            logger.error("Allure command not found. Please install Allure.")
            return False
    
    def serve_allure_report(self):
        """Serve Allure report"""
        try:
            subprocess.run(["allure", "serve", "reports/allure-results"])
        except FileNotFoundError:
            logger.error("Allure command not found. Please install Allure.")
            return False

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Selenium Test Automation Runner")
    
    # Test execution options
    parser.add_argument("test_path", nargs="?", help="Path to test file or directory")
    parser.add_argument("--browser", choices=["chrome", "firefox", "edge"], 
                       default="chrome", help="Browser to use")
    parser.add_argument("--headless", action="store_true", help="Run in headless mode")
    parser.add_argument("--environment", default="test", 
                       help="Environment to test against")
    parser.add_argument("--base-url", help="Base URL for testing")
    
    # Test filtering
    parser.add_argument("-m", "--markers", nargs="+", 
                       help="Test markers to include/exclude (prefix with - to exclude)")
    parser.add_argument("--smoke", action="store_true", help="Run smoke tests only")
    parser.add_argument("--regression", action="store_true", help="Run regression tests only")
    
    # Execution options
    parser.add_argument("--parallel", action="store_true", help="Run tests in parallel")
    parser.add_argument("--workers", type=int, default=4, 
                       help="Number of parallel workers")
    parser.add_argument("--verbose", action="store_true", default=True, 
                       help="Verbose output")
    parser.add_argument("--quiet", action="store_true", help="Quiet output")
    
    # Reporting
    parser.add_argument("--report", choices=["html", "allure", "both"], 
                       default="html", help="Report format")
    parser.add_argument("--generate-allure", action="store_true", 
                       help="Generate Allure report after tests")
    parser.add_argument("--serve-allure", action="store_true", 
                       help="Serve Allure report")
    
    # Setup options
    parser.add_argument("--install-deps", action="store_true", 
                       help="Install dependencies")
    parser.add_argument("--setup", action="store_true", 
                       help="Setup test environment")
    parser.add_argument("--create-data", action="store_true", 
                       help="Create sample test data files")
    
    # Debug options
    parser.add_argument("--dry-run", action="store_true", 
                       help="Show what would be executed without running")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    
    args = parser.parse_args()
    
    # Initialize test runner
    runner = TestRunner()
    
    # Handle setup commands
    if args.install_deps:
        success = runner.install_dependencies()
        return 0 if success else 1
    
    if args.setup:
        runner.setup_environment()
        return 0
    
    if args.create_data:
        runner.create_test_data()
        return 0
    
    if args.serve_allure:
        runner.serve_allure_report()
        return 0
    
    # Process markers
    markers = args.markers or []
    if args.smoke:
        markers.append("smoke")
    if args.regression:
        markers.append("regression")
    
    # Run tests
    exit_code = runner.run_tests(
        test_path=args.test_path,
        browser=args.browser,
        headless=args.headless,
        environment=args.environment,
        base_url=args.base_url,
        markers=markers,
        parallel=args.parallel,
        workers=args.workers,
        report_format=args.report,
        verbose=args.verbose and not args.quiet,
        dry_run=args.dry_run
    )
    
    # Generate Allure report if requested
    if args.generate_allure and not args.dry_run:
        runner.generate_allure_report()
    
    return exit_code

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)