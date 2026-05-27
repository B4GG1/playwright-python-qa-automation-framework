# Technology Stack

This document describes the technologies, tools, and planned integrations used in the QA automation framework.
The stack is divided into implemented technologies, installed but not fully integrated tools, and planned future extensions.

## Core Technologies

The project is currently built with:

- Python 3.12
- Pytest
- Playwright
- pytest-playwright
- Git
- GitHub
- WSL2 with Ubuntu Linux

## Test Automation

Current test automation stack:

- Playwright for browser automation
- Pytest as the test runner
- pytest-playwright for Playwright and Pytest integration

Current browser execution:

- Chromium

Planned browser execution:

- Firefox
- WebKit
- cross-browser test execution strategy

## Code Quality And Development Tooling

Current quality tools:

- Ruff for linting and static checks
- Black for code formatting
- isort for import sorting
- pre-commit for local quality gates

These tools are used to maintain consistent code style and reduce formatting-related issues.

## CI/CD And Automation

Current CI tool:

- GitHub Actions

Current CI responsibilities:

- repository checkout
- Python setup
- dependency installation
- Playwright browser installation
- linting
- formatting validation
- import sorting validation
- test execution
- artifact upload

Planned CI/CD improvements:

- dependency caching
- browser caching
- JUnit XML reporting
- multi-browser CI execution
- Docker-based execution
- advanced reporting publication

## Reporting And Debugging

Currently implemented:

- pytest-html
- CI artifact upload
- automatic screenshot capture on test failure

Installed but not fully integrated:

- allure-pytest

Planned reporting improvements:

- advanced Allure reporting
- improved screenshot structure
- logs as CI artifacts
- test result history and analytics

## API Testing

Currently installed:

- requests

Current status:

- API testing layer is not implemented yet

Planned usage:

- API smoke tests
- backend validation support
- hybrid UI + API test scenarios

## Test Execution Optimization

Currently installed:

- pytest-xdist

Current status:

- parallel test execution is not optimized yet

Planned usage:

- faster regression execution
- parallel UI test runs
- CI execution optimization

## Planned Integrations

Future planned integrations include:

- Selenium WebDriver comparison module
- Docker-based execution environment
- environment configuration management
- test data management utilities
- Jenkins CI integration
- cross-browser execution support