# Architecture

This document describes the current architecture of the QA automation framework.

The project follows a lightweight, modular architecture focused on readability, maintainability, and incremental framework growth. The architecture is intentionally simple at this stage, but already includes Page Object Model, reusable pytest fixtures, centralized test data, marker-based test organization, CI execution, and technical documentation.

## Current Architecture Scope

The current framework includes:

* Pytest-based test execution
* Playwright browser automation
* Page Object Model for login page
* reusable pytest fixtures
* centralized login test data
* marker-based test categorization
* CI execution with GitHub Actions
* code quality tooling
* HTML reporting and CI artifacts
* screenshot capture on test failure
* manual test case documentation mapped to automated tests

The current automated coverage focuses on the Sauce Demo login page and related authentication behavior.

## Project Layers

The framework is organized into the following layers.

### `tests/`

Contains automated test suites.

Current login-related test modules include:

* `test_smoke_login.py` — basic smoke validation
* `test_login_positive.py` — positive login scenarios
* `test_login_negative.py` — negative login scenarios
* `test_login_ui.py` — login page UI behavior
* `test_login_access_control.py` — protected route access validation

Tests should focus on behavior and assertions, while reusable page interactions should be handled by Page Object classes.

### `pages/`

Contains Page Object Model classes.

Current implementation:

* `LoginPage`

The Page Object layer is responsible for:

* page-specific locators
* reusable page actions
* interaction methods
* hiding direct selector usage from tests where practical

Tests may still use direct Playwright assertions when validating behavior outside the current Page Object scope, for example inventory page visibility before a dedicated InventoryPage object exists.

### `test_data/`

Contains centralized test data used by automated tests.

Current login test data includes:

* valid user cases
* invalid login cases
* empty credential cases
* locked out user cases
* expected error messages
* inventory URL suffix used in login-related assertions

The goal of this layer is to keep test data separate from test logic and support pytest parametrization.

### `conftest.py`

Contains shared pytest configuration, hooks, and fixtures.

Current responsibilities:

* screenshot capture on test failure
* reusable `opened_login_page` fixture

The `opened_login_page` fixture prepares a ready-to-use `LoginPage` instance with the login page already opened.

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

Manual test cases are mapped to automated tests through `TC-LOGIN-XXX` identifiers. These identifiers are also used in parametrized pytest output where practical.

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
Centralized test data
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

### Markers

Tests are categorized using pytest markers such as:

* `smoke`
* `regression`
* `ui`
* `positive`
* `negative`

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

* additional Page Object classes for inventory, cart, and checkout areas
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

The architecture is no longer only a setup foundation. It now contains the first complete functional automation workstream for the login page.

The next architecture step is to extend the same principles to additional application areas, starting with inventory, products, cart, and checkout coverage.
