#!/bin/bash

# Selenium Test Automation Runner Script
# This script provides easy commands for running selenium tests

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
BROWSER="chrome"
ENVIRONMENT="test"
WORKERS=4
REPORT_FORMAT="html"

# Function to print colored output
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to install dependencies
install_dependencies() {
    print_info "Installing Python dependencies..."
    pip install -r requirements.txt
    print_success "Dependencies installed successfully"
}

# Function to setup environment
setup_environment() {
    print_info "Setting up test environment..."
    
    # Create virtual environment if it doesn't exist
    if [ ! -d "venv" ]; then
        print_info "Creating virtual environment..."
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Install dependencies
    install_dependencies
    
    # Setup test data
    python run_tests.py --create-data
    
    print_success "Environment setup complete"
}

# Function to run smoke tests
run_smoke_tests() {
    print_info "Running smoke tests..."
    python run_tests.py --smoke --browser="$BROWSER" --environment="$ENVIRONMENT"
}

# Function to run regression tests
run_regression_tests() {
    print_info "Running regression tests..."
    python run_tests.py --regression --browser="$BROWSER" --environment="$ENVIRONMENT"
}

# Function to run all tests
run_all_tests() {
    print_info "Running all tests..."
    python run_tests.py --browser="$BROWSER" --environment="$ENVIRONMENT" --report="$REPORT_FORMAT"
}

# Function to run tests in parallel
run_parallel_tests() {
    print_info "Running tests in parallel with $WORKERS workers..."
    python run_tests.py --parallel --workers="$WORKERS" --browser="$BROWSER" --environment="$ENVIRONMENT"
}

# Function to run specific test
run_specific_test() {
    local test_path="$1"
    print_info "Running specific test: $test_path"
    python run_tests.py "$test_path" --browser="$BROWSER" --environment="$ENVIRONMENT"
}

# Function to run tests in headless mode
run_headless_tests() {
    print_info "Running tests in headless mode..."
    python run_tests.py --headless --browser="$BROWSER" --environment="$ENVIRONMENT"
}

# Function to generate and serve Allure report
serve_allure_report() {
    if command_exists allure; then
        print_info "Generating and serving Allure report..."
        python run_tests.py --generate-allure
        allure serve reports/allure-results
    else
        print_error "Allure is not installed. Please install Allure to generate reports."
        print_info "Installation: https://docs.qameta.io/allure/#_installing_a_commandline"
    fi
}

# Function to clean reports
clean_reports() {
    print_info "Cleaning old reports..."
    rm -rf reports/screenshots/*
    rm -rf reports/logs/*
    rm -rf reports/allure-results/*
    rm -rf reports/allure-report/*
    rm -f reports/*.html
    print_success "Reports cleaned"
}

# Function to run multi-browser tests
run_multi_browser_tests() {
    local browsers=("chrome" "firefox")
    
    for browser in "${browsers[@]}"; do
        print_info "Running tests with $browser..."
        python run_tests.py --browser="$browser" --environment="$ENVIRONMENT" --report="both"
    done
}

# Function to run CI/CD tests
run_ci_tests() {
    print_info "Running CI/CD optimized tests..."
    python run_tests.py --headless --parallel --workers="$WORKERS" \
        --browser="chrome" --environment="$ENVIRONMENT" \
        --report="both" -m "not slow"
}

# Function to show help
show_help() {
    echo "Selenium Test Automation Runner"
    echo ""
    echo "Usage: $0 [COMMAND] [OPTIONS]"
    echo ""
    echo "Commands:"
    echo "  setup                 Setup test environment"
    echo "  install-deps          Install Python dependencies"
    echo "  smoke                 Run smoke tests"
    echo "  regression            Run regression tests"
    echo "  all                   Run all tests"
    echo "  parallel              Run tests in parallel"
    echo "  headless              Run tests in headless mode"
    echo "  multi-browser         Run tests across multiple browsers"
    echo "  ci                    Run CI/CD optimized tests"
    echo "  allure                Generate and serve Allure report"
    echo "  clean                 Clean old reports"
    echo "  help                  Show this help message"
    echo ""
    echo "Options:"
    echo "  --browser=BROWSER     Browser to use (chrome, firefox, edge) [default: chrome]"
    echo "  --environment=ENV     Environment to test against [default: test]"
    echo "  --workers=NUM         Number of parallel workers [default: 4]"
    echo "  --report=FORMAT       Report format (html, allure, both) [default: html]"
    echo ""
    echo "Examples:"
    echo "  $0 setup"
    echo "  $0 smoke --browser=firefox"
    echo "  $0 parallel --workers=8"
    echo "  $0 all --environment=staging"
    echo "  $0 tests/test_login.py"
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --browser=*)
            BROWSER="${1#*=}"
            shift
            ;;
        --environment=*)
            ENVIRONMENT="${1#*=}"
            shift
            ;;
        --workers=*)
            WORKERS="${1#*=}"
            shift
            ;;
        --report=*)
            REPORT_FORMAT="${1#*=}"
            shift
            ;;
        *)
            COMMAND="$1"
            shift
            ;;
    esac
done

# Main execution
case "${COMMAND:-help}" in
    setup)
        setup_environment
        ;;
    install-deps)
        install_dependencies
        ;;
    smoke)
        run_smoke_tests
        ;;
    regression)
        run_regression_tests
        ;;
    all)
        run_all_tests
        ;;
    parallel)
        run_parallel_tests
        ;;
    headless)
        run_headless_tests
        ;;
    multi-browser)
        run_multi_browser_tests
        ;;
    ci)
        run_ci_tests
        ;;
    allure)
        serve_allure_report
        ;;
    clean)
        clean_reports
        ;;
    help)
        show_help
        ;;
    tests/*)
        run_specific_test "$COMMAND"
        ;;
    *)
        print_error "Unknown command: $COMMAND"
        show_help
        exit 1
        ;;
esac