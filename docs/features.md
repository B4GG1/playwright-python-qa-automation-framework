# Features

This document lists the currently implemented and planned features of the QA automation framework.
The purpose of this file is to provide a quick overview of what the framework already supports and what will be developed in future phases.

## Currently Implemented

### Test Execution

- UI test automation using Playwright
- Pytest-based test execution
- Smoke test execution support
- Centralized pytest configuration
- Playwright Chromium execution in CI

### Code Quality

- Static code analysis with Ruff
- Automated code formatting using Black
- Import standardization with isort
- Automated local quality gates using pre-commit hooks

### CI/CD

- GitHub Actions CI pipeline
- Automated dependency installation in CI
- Automated Playwright browser installation in CI
- Automated linting, formatting validation, and test execution
- CI execution on `main` and `develop`
- Manual CI execution using `workflow_dispatch`

### Reporting And Debugging

- HTML test report generation using pytest-html
- Test artifacts uploaded from CI
- Reports directory used for runtime outputs
- Screenshot capture on test failure
- Downloadable CI artifacts for debugging

### Repository And Documentation

- GitHub-based portfolio repository structure
- Lightweight Git branching strategy documentation
- Technical documentation structure under `docs/`
- README used as project landing page and documentation hub
- Linux-based development workflow using WSL2

## Planned Features

### Framework Architecture

- Page Object Model implementation
- BasePage abstraction
- Reusable framework utilities
- Shared pytest fixtures
- Centralized test data management
- Environment-based configuration management

### Test Coverage

- Positive login scenarios
- Negative login scenarios
- Inventory / products page validation
- Cart functionality tests
- Checkout flow tests
- Session and logout validation
- Cross-browser UI execution

### Test Organization

- Pytest marker-based test categorization
- Smoke and regression suite separation
- Parametrized test scenarios
- Manual test case documentation under `test_cases/`

### Reporting And Diagnostics

- Improved failure diagnostics
- Better screenshot organization
- Advanced Allure reporting
- Test logs and execution evidence
- Test history and analytics

### Future Extensions

- API automation testing layer
- Selenium WebDriver comparison module
- Docker-based execution environment
- Parallel test execution optimization
- Jenkins pipeline integration
- Framework packaging as a reusable automation template