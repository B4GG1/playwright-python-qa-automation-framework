# Features

This document lists the currently implemented and planned features of the QA automation framework.

The purpose of this file is to provide a quick overview of what the framework already supports and what will be developed in future phases.

## Currently Implemented

### Test Execution

* UI test automation using Playwright
* Pytest-based test execution
* Smoke test execution support
* Regression test execution support
* Marker-based selective test execution
* Centralized pytest configuration
* Playwright Chromium execution in CI

### Page Object Model

* Login Page Object implemented
* Centralized login page locators
* Reusable login page actions
* Error message interaction support
* Login page UI element access methods

### Test Data Management

* Centralized login test data
* Valid user test data
* Invalid login test data
* Empty credentials test data
* Locked out user test data
* Expected login error messages
* Test case IDs mapped to automated test data

### Login Page Test Coverage

The framework currently includes automated coverage for the Sauce Demo login area.

Implemented login scenarios:

* successful login with valid credentials
* login with invalid username
* login with invalid password
* login with empty username
* login with empty password
* login with empty credentials
* locked out user login attempt
* login with invalid username and invalid password
* closing error message after failed login
* login page elements visibility
* password field masking validation
* login form submission with Enter key
* direct inventory page access without login

### Test Organization

* Pytest marker-based test categorization
* Smoke, regression, UI, positive, and negative markers
* Parametrized negative login scenarios
* Parametrized test output with manual test case IDs
* Manual test case documentation under `test_cases/`
* Login test case coverage mapped to automated tests

### Fixtures And Reusable Setup

* Shared pytest fixture for opened login page
* Reusable setup for login page tests
* Screenshot capture hook on test failure

### Code Quality

* Static code analysis with Ruff
* Automated code formatting using Black
* Import standardization with isort
* Automated local quality gates using pre-commit hooks

### CI/CD

* GitHub Actions CI pipeline
* Automated dependency installation in CI
* Automated Playwright browser installation in CI
* Automated linting, formatting validation, and test execution
* CI execution on `main` and `develop`
* CI execution for pull requests targeting `main` and `develop`
* Manual CI execution using `workflow_dispatch`
* CI artifacts upload for reports and debugging outputs

### Reporting And Debugging

* HTML test report generation using pytest-html
* Test artifacts uploaded from CI
* Reports directory used for runtime outputs
* Screenshot capture on test failure
* Downloadable CI artifacts for debugging

### Repository And Documentation

* GitHub-based portfolio repository structure
* Lightweight Git branching strategy documentation
* Technical documentation structure under `docs/`
* README used as project landing page and documentation hub
* Linux-based development workflow using WSL2
* Login page manual test cases documented in Markdown
* Login page automation coverage documented and mapped to test files

## Planned Features

### Framework Architecture

* BasePage abstraction when repeated Page Object logic appears
* Reusable framework utilities
* Expanded shared pytest fixtures
* Environment-based configuration management
* Improved configuration structure for base URLs and execution settings

### Test Coverage

Planned next automation areas:

* inventory / products page validation
* product list validation
* product sorting validation
* cart functionality tests
* cart badge validation
* cart page validation
* checkout flow tests
* checkout form validation
* complete order flow
* session and logout validation
* cross-browser UI execution

### Test Organization

* Smoke and regression suite separation in CI
* Improved marker-based CI jobs
* More advanced parametrized test scenarios
* Expanded manual test case documentation for new application areas
* Improved traceability between test cases, test data, and automation

### Reporting And Diagnostics

* Improved failure diagnostics
* Better screenshot organization
* Advanced Allure reporting
* Test logs and execution evidence
* Test history and analytics

### CI/CD Improvements

* Dependency caching for faster pipeline execution
* Playwright browser caching
* JUnit XML test result publishing
* Separate smoke and regression CI jobs
* Multi-browser CI execution
* Scheduled regression runs

### Future Extensions

* API automation testing layer
* Selenium WebDriver comparison module
* Docker-based execution environment
* Parallel test execution optimization
* Jenkins pipeline integration
* Framework packaging as a reusable automation template
