# Framework And Project Structure

This document describes the repository structure and the responsibility of each major directory and configuration file.

The framework is structured to support scalable UI automation, Page Object Model components, test data management, reporting, documentation, and future CI/CD expansion while maintaining readability and modularity.

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

* CI pipeline execution
* dependency installation
* code quality checks
* test execution
* HTML report generation
* artifact upload

### `config/`

Reserved for framework and environment configuration.

Potential future responsibility:

* environment variables handling
* base URLs
* browser settings
* execution configuration
* test environment profiles

This directory is currently intentionally minimal.

### `docs/`

Contains technical project documentation.

Examples:

* architecture documentation
* workflow documentation
* CI/CD documentation
* quality tooling documentation
* testing strategy
* roadmap
* framework structure documentation

### `framework/`

Reserved for shared framework-level utilities and base components.

Potential future responsibility:

* BasePage abstraction
* shared helpers
* reusable assertions
* reporting utilities
* logging utilities
* common framework logic

This directory is currently intentionally minimal and should only be expanded when repeated framework logic appears.

### `pages/`

Contains Page Object Model classes.

Current implementation:

* `login_page.py`
* `inventory_page.py`
* `product_details_page.py`

Current responsibility:

* page-specific locators
* page interaction methods
* reusable UI actions
* separation of page interaction logic from test logic
* lightweight navigation between Page Objects when a user action opens a different page

The current Page Object layer includes:

* `LoginPage`, which supports login page interactions, error message handling, and access to login page UI elements
* `InventoryPage`, which supports inventory page visibility, product list access, product card access, product sorting, and opening product details
* `ProductDetailsPage`, which supports product details validation and returning to the inventory page

### `reports/`

Stores runtime test outputs.

Examples:

* HTML reports
* screenshots
* logs
* CI artifact sources

Generated report files should not be committed to Git. They are intended for local debugging and CI artifact publishing.

### `resources/`

Reserved for static resources and supporting files.

Possible future usage:

* sample files
* upload test files
* static fixtures
* external resources used by tests

This directory is currently intentionally minimal.

### `test_cases/`

Contains manual test cases and test design notes.

Current implementation:

* `login-page.md`
* `inventory-products.md`

Current responsibility:

* manual test case documentation
* test design before automation
* mapping manual test cases to automated test files
* documenting automation coverage status

Current test case identifiers include:

* `TC-LOGIN-XXX`
* `TC-INVENTORY-XXX`

These identifiers are also reflected in parametrized pytest output where practical.

### `test_data/`

Contains externalized test data.

Current implementation:

* `login_test_data.py`
* `inventory_test_data.py`

Current responsibility:

* valid login user data
* invalid login cases
* empty credentials cases
* locked out user cases
* expected login error messages
* login-related URL values
* inventory product IDs
* inventory product names
* inventory product descriptions
* inventory product prices
* inventory product image paths
* test case IDs for parametrized tests where practical

This directory keeps test data separate from test logic and supports pytest parametrization.

### `tests/`

Contains automated test suites.

Current test modules:

* `test_smoke_login.py` — basic smoke validation
* `test_login_positive.py` — positive login scenarios
* `test_login_negative.py` — negative login scenarios
* `test_login_ui.py` — login page UI behavior
* `test_login_access_control.py` — protected route access validation
* `test_inventory_page.py` — inventory page, product cards, product details navigation, and product sorting validation

Planned future test modules may include:

* cart tests
* checkout tests
* API tests
* broader regression suites

## Root Configuration Files

### `conftest.py`

Contains shared Pytest hooks, fixtures, and test execution configuration.

Current usage:

* screenshot capture on test failure
* reusable `opened_login_page` fixture
* reusable `logged_in_inventory_page` fixture

The `opened_login_page` fixture prepares a `LoginPage` instance and opens the login page before a test starts.

The `logged_in_inventory_page` fixture logs in with a valid user and returns an `InventoryPage` instance for inventory and product-related tests.

### `pytest.ini`

Contains Pytest configuration.

Current usage:

* test discovery settings
* marker definitions
* default Pytest options
* strict marker validation

Current markers include:

* `smoke`
* `regression`
* `ui`
* `api`
* `e2e`
* `positive`
* `negative`
* `sorting`

### `pyproject.toml`

Contains tool configuration.

Current usage:

* Ruff configuration
* Black configuration
* isort configuration

### `.pre-commit-config.yaml`

Contains pre-commit hook configuration.

Current usage:

* Ruff
* Black
* isort

### `requirements.txt`

Contains the main project dependency list.

This file is used as a readable dependency declaration.

### `requirements-lock.txt`

Contains locked dependency versions.

This file supports reproducible local and CI dependency installation.

## Current Login Test Suite Structure

The login automation workstream is organized as follows:

```text
test_cases/login-page.md
        ↓
test_data/login_test_data.py
        ↓
pages/login_page.py
        ↓
tests/test_smoke_login.py
tests/test_login_positive.py
tests/test_login_negative.py
tests/test_login_ui.py
tests/test_login_access_control.py
        ↓
pytest markers and parametrized output
        ↓
GitHub Actions CI validation
```

## Current Inventory And Products Test Suite Structure

The inventory and products automation workstream is organized as follows:

```text
test_cases/inventory-products.md
        ↓
test_data/inventory_test_data.py
        ↓
pages/inventory_page.py
pages/product_details_page.py
        ↓
tests/test_inventory_page.py
        ↓
pytest markers and parametrized output
        ↓
GitHub Actions CI validation
```

## Architecture Goals

The project structure is designed to support:

* maintainable test organization
* clear separation of framework layers
* reusable automation components
* scalable Page Object Model implementation
* centralized test configuration
* centralized test data
* reusable pytest fixtures
* CI/CD-ready development workflow
* readable and consistent test structure
* traceability between manual test cases and automated tests
* future UI and API automation expansion

## Structure Evolution

The project has moved beyond the initial foundation stage and now contains two complete automation workstreams:

* Login Page Automation Workstream
* Inventory And Products Automation Workstream

Implemented structure currently includes:

* concrete LoginPage Page Object
* concrete InventoryPage Page Object
* concrete ProductDetailsPage Page Object
* centralized login test data
* centralized inventory product test data
* reusable opened login page fixture
* reusable logged-in inventory page fixture
* login test case documentation
* inventory and products test case documentation
* parametrized login tests
* parametrized inventory product tests
* marker-based test categorization
* login UI and access-control coverage
* inventory page, product details, and product sorting coverage

Future improvements will include:

* additional Page Object classes for cart and checkout pages
* reusable BasePage abstraction when justified
* expanded fixture organization
* reporting utilities
* API testing structure
* Selenium comparison module
* additional test suites for future application areas
