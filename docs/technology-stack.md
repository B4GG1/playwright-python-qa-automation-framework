# Technology Stack

This document describes the technologies, tools, and planned integrations used in the QA automation framework.

The stack is divided into implemented technologies, installed but not fully integrated tools, and planned future extensions.

## Core Technologies

The project is currently built with:

* Python 3.12
* Pytest
* Playwright
* pytest-playwright
* Git
* GitHub
* WSL2 with Ubuntu Linux

## Test Automation

Current test automation stack:

* Playwright for browser automation
* Pytest as the test runner
* pytest-playwright for Playwright and Pytest integration
* Page Object Model for page interaction abstraction
* pytest fixtures for reusable test setup
* pytest parametrization for data-driven test scenarios
* pytest markers for test categorization

Current browser execution:

* Chromium

Current automated UI coverage:

* login page smoke validation
* positive login scenarios
* negative login scenarios
* login UI behavior
* protected inventory route access validation

Planned browser execution:

* Firefox
* WebKit
* cross-browser test execution strategy

## Page Object Model

Currently implemented:

* `LoginPage`

Current Page Object responsibilities:

* login page navigation
* username input interaction
* password input interaction
* login button interaction
* error message handling
* login page UI element locators

Planned Page Object expansion:

* InventoryPage
* CartPage
* CheckoutPage
* additional page objects as application coverage grows

## Test Data Management

Currently implemented:

* centralized login test data
* valid user cases
* invalid login cases
* empty credential cases
* locked out user cases
* expected login error messages
* login-related URL values
* test case IDs used in parametrized pytest output

Current test data location:

```text
test_data/login_test_data.py
```

Planned test data expansion:

* inventory product data
* cart scenario data
* checkout form data
* API test data
* environment-specific test data if needed

## Code Quality And Development Tooling

Current quality tools:

* Ruff for linting and static checks
* Black for code formatting
* isort for import sorting
* pre-commit for local quality gates

These tools are used to maintain consistent code style, reduce formatting-related issues, and support a professional development workflow.

Tool configuration is stored in:

```text
pyproject.toml
.pre-commit-config.yaml
pytest.ini
```

## CI/CD And Automation

Current CI tool:

* GitHub Actions

Current CI responsibilities:

* repository checkout
* Python setup
* dependency installation
* Playwright browser installation
* linting with Ruff
* formatting validation with Black
* import sorting validation with isort
* test execution with Pytest
* HTML report generation
* artifact upload

Current CI targets:

* pushes to `main`
* pushes to `develop`
* pull requests targeting `main`
* pull requests targeting `develop`
* manual workflow execution using `workflow_dispatch`

Planned CI/CD improvements:

* dependency caching
* browser caching
* JUnit XML reporting
* separate smoke and regression jobs
* multi-browser CI execution
* Docker-based execution
* advanced reporting publication

## Reporting And Debugging

Currently implemented:

* pytest-html
* CI artifact upload
* automatic screenshot capture on test failure
* reports directory for runtime outputs
* downloadable CI artifacts for debugging

Installed but not fully integrated:

* allure-pytest

Planned reporting improvements:

* advanced Allure reporting
* improved screenshot structure
* logs as CI artifacts
* test result history and analytics
* better failure diagnostics

## API Testing

Currently installed:

* requests

Current status:

* API testing layer is not implemented yet

Planned usage:

* API smoke tests
* backend validation support
* hybrid UI + API test scenarios
* test data setup or validation through API calls where appropriate

## Test Execution Optimization

Currently installed:

* pytest-xdist

Current status:

* parallel test execution is not optimized yet

Planned usage:

* faster regression execution
* parallel UI test runs
* CI execution optimization

Parallel execution will be introduced later, after the test suite grows and stability requirements are better understood.

## Version And Dependency Management

Current dependency files:

* `requirements.txt`
* `requirements-lock.txt`

Current usage:

* `requirements.txt` provides a readable list of main project dependencies
* `requirements-lock.txt` provides locked dependency versions for reproducible setup and CI execution

Planned improvements:

* consistent CI installation from locked dependency versions
* dependency update workflow
* optional dependency grouping if the project grows

## Development Environment

Current local development environment:

* Windows host system
* WSL2 with Ubuntu Linux
* Python virtual environment
* PyCharm Community
* Git and GitHub
* browser automation through Playwright

This setup supports Linux-based test execution locally while keeping the project compatible with GitHub Actions CI.

## Planned Integrations

Future planned integrations include:

* Selenium WebDriver comparison module
* Docker-based execution environment
* environment configuration management
* expanded test data management utilities
* Jenkins CI integration
* cross-browser execution support
* Allure reporting
* API testing layer
* framework packaging as a reusable automation template

## Current Stack Status

The current stack is sufficient to support a complete login page automation workstream.

Implemented technical capabilities include:

* UI automation with Playwright
* test execution with Pytest
* Page Object Model
* reusable pytest fixture
* centralized test data
* parametrized tests
* marker-based test organization
* CI validation
* HTML reporting
* screenshot capture on failure
* technical documentation

The next stack expansion will focus on additional Page Objects and test coverage for inventory, products, cart, and checkout flows.
