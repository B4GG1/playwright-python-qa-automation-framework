# Framework And Project Structure

This document describes the repository structure and the responsibility of each major directory and configuration file.
The framework is structured to support scalable UI automation, test data management, reporting, documentation, and future CI/CD expansion while maintaining readability and modularity.

## Current Project Structure

```text
playwright-python-qa-automation-framework/
│
├── .github/
│   └── workflows/              # GitHub Actions CI workflows
│
├── config/                     # Framework and environment configuration
├── docs/                       # Project documentation
├── framework/                  # Shared framework utilities and core infrastructure
├── pages/                      # Page Object Model components
├── reports/                    # Runtime test reports, screenshots, and execution artifacts
├── resources/                  # Static resources and supporting files
├── test_cases/                 # Manual test cases and test design documentation
├── test_data/                  # Externalized test datasets and test inputs
├── tests/                      # Automated test suites
│
├── conftest.py                 # Shared pytest fixtures and hooks
├── pytest.ini                  # Centralized pytest configuration
├── pyproject.toml              # Ruff, Black, and isort configuration
├── requirements.txt            # Project dependencies
├── requirements-lock.txt       # Locked dependency versions
├── .gitignore                  # Git ignore rules
├── .pre-commit-config.yaml     # Automated local quality hooks configuration
├── LICENSE                     # Project license
└── README.md                   # Project overview and documentation entry point
```

## Directory Responsibilities

### `.github/workflows/`

Contains GitHub Actions workflow definitions.

Current responsibility:

- CI pipeline execution
- dependency installation
- quality checks
- test execution
- artifact upload

### `config/`

Reserved for framework and environment configuration.

Planned responsibility:

- environment variables handling
- base URLs
- browser settings
- execution configuration

### `docs/`

Contains technical project documentation.

Examples:

- architecture documentation
- workflow documentation
- CI/CD documentation
- quality tooling documentation
- testing strategy
- roadmap

### `framework/`

Reserved for shared framework-level utilities and base components.

Planned responsibility:

- BasePage abstraction
- shared helpers
- reusable assertions
- reporting utilities
- common framework logic

### `pages/`

Reserved for Page Object Model classes.

Planned responsibility:

- page-specific locators
- page interaction methods
- reusable UI actions
- separation of page logic from test logic

### `reports/`

Stores runtime test outputs.

Examples:

- HTML reports
- screenshots
- logs
- CI artifact sources

Generated report files should not be committed to Git. They are intended for local debugging and CI artifact publishing.

### `resources/`

Reserved for static resources and supporting files.

Possible future usage:

- sample files
- upload test files
- static fixtures
- external resources used by tests

### `test_cases/`

Contains manual test cases and test design notes.

This directory supports QA analysis before automation implementation.

Planned usage:

- login page test cases
- inventory page test cases
- cart test cases
- checkout test cases
- regression test ideas

### `test_data/`

Reserved for externalized test data.

Planned usage:

- user credentials
- input datasets
- parametrized test data
- reusable static test values

### `tests/`

Contains automated test suites.

Current usage:

- smoke tests

Planned usage:

- login tests
- inventory tests
- cart tests
- checkout tests
- API tests
- regression suites

## Root Configuration Files

### `conftest.py`

Contains shared Pytest hooks, fixtures, and test execution configuration.

Current usage:

- screenshot capture on test failure

### `pytest.ini`

Contains Pytest configuration.

Current usage:

- test discovery settings
- marker definitions
- default Pytest options

### `pyproject.toml`

Contains tool configuration.

Current usage:

- Ruff configuration
- Black configuration
- isort configuration

### `.pre-commit-config.yaml`

Contains pre-commit hook configuration.

Current usage:

- Ruff
- Ruff format
- Black
- isort

## Architecture Goals

The project structure is designed to support:

- maintainable test organization
- clear separation of framework layers
- reusable automation components
- scalable Page Object Model implementation
- centralized test configuration
- CI/CD-ready development workflow
- readable and consistent test structure
- future UI and API automation expansion

## Structure Evolution

The current structure represents the foundation stage of the framework.

Future improvements will include:

- concrete Page Object classes
- reusable BasePage abstraction
- test data modules
- test case documentation
- fixture expansion
- reporting utilities
- additional test suites