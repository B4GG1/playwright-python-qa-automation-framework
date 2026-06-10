# Architecture

This document describes the current architecture of the QA automation framework.

The project follows a lightweight, modular architecture focused on readability, maintainability, and incremental framework growth. The architecture is intentionally simple at this stage, but already includes Page Object Model, reusable pytest fixtures, centralized test data, marker-based test organization, CI execution, reporting support, screenshot capture, and technical documentation.

## Current Architecture Scope

The current framework includes:

* Pytest-based test execution
* Playwright browser automation
* Page Object Model for login, inventory, and product details pages
* reusable pytest fixtures
* centralized login and inventory product test data
* marker-based test categorization
* parametrized test execution with manual test case IDs
* CI execution with GitHub Actions
* code quality tooling
* HTML reporting and CI artifacts
* screenshot capture on test failure
* manual test case documentation mapped to automated tests

The current automated coverage focuses on:

* Sauce Demo login page and authentication behavior
* inventory page availability
* product list and product card validation
* product details navigation
* product sorting

Cart and checkout coverage are planned for later workstreams.

## Project Layers

The framework is organized into the following layers.

### `tests/`

Contains automated test suites.

Current test modules include:

* `test_smoke_login.py` — basic smoke validation
* `test_login_positive.py` — positive login scenarios
* `test_login_negative.py` — negative login scenarios
* `test_login_ui.py` — login page UI behavior
* `test_login_access_control.py` — protected route access validation
* `test_inventory_page.py` — inventory page, product cards, product details navigation, and product sorting tests

Tests should focus on behavior and assertions, while reusable page interactions should be handled by Page Object classes.

### `pages/`

Contains Page Object Model classes.

Current implementation:

* `LoginPage`
* `InventoryPage`
* `ProductDetailsPage`

The Page Object layer is responsible for:

* page-specific locators
* reusable page actions
* interaction methods
* hiding direct selector usage from tests where practical
* returning the next Page Object when navigation changes the current page context

The current Page Object implementation remains intentionally lightweight. A shared BasePage abstraction has not been introduced yet because repeated page-level behavior is still limited.

### `test_data/`

Contains centralized test data used by automated tests.

Current login test data includes:

* valid user cases
* invalid login cases
* empty credential cases
* locked out user cases
* expected error messages
* inventory URL suffix used in login-related assertions

Current inventory test data includes:

* product IDs
* product names
* product descriptions
* product prices
* product image paths

The goal of this layer is to keep test data separate from test logic and support pytest parametrization.

### `conftest.py`

Contains shared pytest configuration, hooks, and fixtures.

Current responsibilities:

* screenshot capture on test failure
* reusable `opened_login_page` fixture
* reusable `logged_in_inventory_page` fixture

The `opened_login_page` fixture prepares a ready-to-use `LoginPage` instance with the login page already opened.

The `logged_in_inventory_page` fixture logs in with a valid user and returns a ready-to-use `InventoryPage` instance.

### `framework/`

Reserved for shared framework utilities, base classes, helpers, and reusable infrastructure code.

This layer is currently intentionally minimal. It may be expanded later when repeated logic appears across multiple Page Objects or test modules.

Potential future usage:

* BasePage abstraction
* custom assertion helpers
* logging utilities
* reporting helpers
* shared wait/diagnostic utilities

### `config/`

Reserved for framework and environment configuration.

Potential future usage:

* base URLs
* environment-specific settings
* browser configuration
* execution configuration

### `reports/`

Stores generated runtime reports, screenshots, and debugging artifacts.

Runtime files are ignored by Git and published through CI artifacts when needed.

Current usage includes:

* pytest HTML reports
* screenshots from failed tests

### `test_cases/`

Contains manual test case documentation.

Current implementation:

* `login-page.md`
* `inventory-products.md`

Manual test cases are mapped to automated tests through identifiers such as:

* `TC-LOGIN-XXX`
* `TC-INVENTORY-XXX`

These identifiers are also used in parametrized pytest output where practical.

### `docs/`

Contains technical documentation related to:

* architecture
* workflow
* testing strategy
* CI/CD pipeline
* quality tooling
* technology stack
* roadmap

## Current Login Test Architecture

The login test suite is built around the following structure:

```text
Manual test cases
        ↓
Centralized login test data
        ↓
LoginPage Page Object
        ↓
Pytest test modules
        ↓
Markers and parametrization
        ↓
CI execution and reports
```

### LoginPage

`LoginPage` centralizes login page interactions such as:

* opening the login page
* filling username
* filling password
* clicking the login button
* reading error messages
* closing error messages
* exposing relevant login page locators

### Reusable Fixture

The `opened_login_page` fixture reduces repeated setup in login-related tests.

Instead of each test manually creating and opening the login page, tests can receive a ready-to-use `LoginPage` instance.

### Test Data

Login-related data is centralized in `test_data/login_test_data.py`.

This supports:

* readable tests
* reduced hardcoding
* consistent expected error messages
* parametrized test execution
* mapping automated tests to manual test cases

### Parametrization

Negative login scenarios use pytest parametrization to execute the same test logic against multiple data cases.

Parametrized IDs are based on manual test case IDs, such as:

* `TC-LOGIN-002`
* `TC-LOGIN-003`
* `TC-LOGIN-004`

This improves traceability between documentation, test output, and automated coverage.

## Current Inventory And Products Test Architecture

The inventory and products test suite is built around the following structure:

```text
Manual inventory test cases
        ↓
Centralized inventory product test data
        ↓
InventoryPage and ProductDetailsPage Page Objects
        ↓
Reusable logged-in inventory fixture
        ↓
Pytest inventory test module
        ↓
Markers and parametrization
        ↓
CI execution and reports
```

### InventoryPage

`InventoryPage` centralizes inventory page interactions such as:

* accessing the inventory container
* accessing the product list
* accessing product cards
* reading product names and prices
* sorting products
* opening product details from product name
* opening product details from product image
* exposing cart-related locators for future workstreams

### ProductDetailsPage

`ProductDetailsPage` centralizes product details page interactions such as:

* accessing product name
* accessing product description
* accessing product price
* accessing product image
* accessing Add to cart button
* accessing Back to products button
* returning to the inventory page

### Reusable Fixture

The `logged_in_inventory_page` fixture prepares a logged-in user session and returns an `InventoryPage` instance.

This reduces repeated login setup in inventory and product-related tests.

### Test Data

Inventory product data is centralized in `test_data/inventory_test_data.py`.

This supports:

* product list validation
* product card validation
* product details validation
* product sorting validation
* parametrized execution across all product data where useful

### Helper Assertions

Inventory tests use small private helper functions inside the test module to reduce duplication when validating repeated product content.

These helpers keep assertions in the test layer while avoiding unnecessary duplication across product card and product details scenarios.

## Markers

Tests are categorized using pytest markers such as:

* `smoke`
* `regression`
* `ui`
* `positive`
* `negative`
* `sorting`

Markers allow selective test execution for different validation needs.

## Design Direction

The framework follows a modular architecture where:

* tests describe behavior and assertions,
* Page Objects handle page interactions,
* test data is externalized from test logic,
* fixtures prepare reusable test setup,
* documentation tracks test design and coverage,
* CI validates the project automatically.

Planned architecture improvements include:

* additional Page Object classes for cart and checkout areas
* BasePage abstraction when repeated page behavior appears
* improved fixture organization
* enhanced reporting and diagnostics
* API testing layer
* future Selenium comparison module
* environment-based configuration

## Architecture Principles

The framework should prioritize:

* readability
* maintainability
* clear separation of responsibilities
* reusable components
* stable and deterministic test execution
* traceability between manual test cases and automated tests
* CI/CD compatibility
* incremental improvement over unnecessary early complexity

## Current Architecture Status

The architecture is no longer only a setup foundation. It now contains two complete functional automation workstreams:

* Login Page Automation Workstream
* Inventory And Products Automation Workstream

The next architecture step is to extend the same principles to cart and checkout coverage while avoiding unnecessary early abstractions.
