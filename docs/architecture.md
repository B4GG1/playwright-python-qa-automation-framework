# Architecture

This document describes the current architecture of the QA automation framework.

The project follows a lightweight, modular architecture focused on readability, maintainability, and incremental framework growth. The architecture is intentionally simple at this stage, but already includes Page Object Model, reusable pytest fixtures, centralized test data, marker-based test organization, CI execution, reporting support, screenshot capture, and technical documentation.

## Current Architecture Scope

The current framework includes:

* Pytest-based test execution
* Playwright browser automation
* Page Object Model for login, inventory, product details, and cart pages
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
* protected route access validation
* inventory page availability
* product list and product card validation
* product details navigation
* product sorting
* cart page navigation
* empty cart state
* add-to-cart behavior
* cart badge behavior
* cart item visibility and content validation
* remove-from-cart behavior
* continue shopping navigation
* cart state persistence after logout and re-login

Checkout coverage is planned for a later workstream.

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
* `test_cart_page.py` — cart page, add-to-cart, cart badge, cart content, remove-from-cart, continue shopping, and cart persistence tests

Tests should focus on behavior and assertions, while reusable page interactions should be handled by Page Object classes.

### `pages/`

Contains Page Object Model classes.

Current implementation:

* `LoginPage`
* `InventoryPage`
* `ProductDetailsPage`
* `CartPage`

The Page Object layer is responsible for:

* page-specific locators
* reusable page actions
* interaction methods
* hiding direct selector usage from tests where practical
* returning the next Page Object when navigation changes the current page context

The current Page Object implementation remains intentionally lightweight. A shared BasePage abstraction has not been introduced yet because repeated page-level behavior is still limited and does not justify an additional inheritance layer.

### `test_data/`

Contains centralized test data used by automated tests.

Current login test data includes:

* valid user cases
* invalid login cases
* empty credential cases
* locked out user cases
* expected error messages
* protected route URL suffixes used in login-related assertions

Current inventory test data includes:

* product IDs
* product names
* product descriptions
* product prices
* product image paths

Cart tests intentionally reuse existing login and inventory product test data instead of introducing a separate cart-specific test data file. This keeps cart scenarios deterministic while avoiding unnecessary duplication.

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
* `cart.md`

Manual test cases are mapped to automated tests through identifiers such as:

* `TC-LOGIN-XXX`
* `TC-INVENTORY-XXX`
* `TC-CART-XXX`

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
* framework and project structure

## Current Login Test Architecture

The login test suite is built around the following structure:

```text
Manual login test cases
        ↓
Centralized login test data
        ↓
LoginPage Page Object
        ↓
Pytest login test modules
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
* protected route access validation

### Parametrization

Negative login scenarios and protected route scenarios use pytest parametrization to execute the same test logic against multiple data cases.

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
* adding products to the cart from inventory product cards
* removing products from the cart from inventory product cards
* accessing cart link and cart badge
* opening the cart page
* opening the application menu
* logging out from the inventory page

`InventoryPage` acts as the main authenticated landing page object and provides navigation entry points into product details and cart flows.

### ProductDetailsPage

`ProductDetailsPage` centralizes product details page interactions such as:

* opening a product details page by product ID
* accessing product name
* accessing product description
* accessing product price
* accessing product image
* accessing Add to cart button
* accessing Remove button
* adding a product to the cart from the product details page
* removing a product from the cart from the product details page
* accessing Back to products button
* returning to the inventory page
* opening the cart page
* accessing cart badge

### Reusable Fixture

The `logged_in_inventory_page` fixture prepares a logged-in user session and returns an `InventoryPage` instance.

This reduces repeated login setup in inventory, product details, and cart-related tests.

### Test Data

Inventory product data is centralized in `test_data/inventory_test_data.py`.

This supports:

* product list validation
* product card validation
* product details validation
* product sorting validation
* deterministic cart product selection
* parametrized execution across all product data where useful

### Helper Assertions

Inventory tests use small private helper functions inside the test module to reduce duplication when validating repeated product content.

These helpers keep assertions in the test layer while avoiding unnecessary duplication across product card and product details scenarios.

## Current Cart Test Architecture

The cart test suite is built around the following structure:

```text
Manual cart test cases
        ↓
Existing login and inventory product test data
        ↓
InventoryPage, ProductDetailsPage, and CartPage Page Objects
        ↓
Reusable logged-in inventory fixture
        ↓
Pytest cart test module
        ↓
Markers and parametrization
        ↓
CI execution and reports
```

### CartPage

`CartPage` centralizes cart page interactions such as:

* opening the cart page directly
* accessing the cart contents container
* accessing the cart list
* accessing cart items
* locating cart item cards by product name
* accessing cart item name, description, price, quantity, and Remove button
* removing a product from the cart
* opening product details from a cart item name
* accessing Continue Shopping button
* returning from the cart page to the inventory page
* accessing Checkout button
* accessing cart link and cart badge

Checkout-related locators are available in `CartPage`, but checkout behavior remains outside the current cart workstream test scope.

### InventoryPage And ProductDetailsPage In Cart Scenarios

Cart tests reuse `InventoryPage` and `ProductDetailsPage` for cart-related actions that originate outside the cart page.

`InventoryPage` is used for:

* adding products to the cart from inventory cards
* validating inventory-side Add to cart and Remove button states
* validating cart badge behavior from the header
* opening the cart page
* logging out during cart persistence scenarios

`ProductDetailsPage` is used for:

* adding a product to the cart from the product details page
* validating product-details-side Add to cart and Remove button states
* opening the cart from product details when needed

### Reusable Fixture

The cart test module uses `logged_in_inventory_page` as its main setup fixture.

This keeps cart tests focused on cart behavior while avoiding repeated login steps.

### Test Data

Cart tests intentionally use:

* valid user data from `test_data/login_test_data.py`
* deterministic product data from `test_data/inventory_test_data.py`

No separate cart test data module is currently required.

### Cart Scope Boundaries

The current cart workstream covers:

* cart page availability
* empty cart state
* adding products to cart
* inventory-side cart button behavior
* cart badge behavior
* cart item visibility
* cart item content validation
* removing products from cart
* navigation between cart and inventory page
* cart state persistence after logout and re-login
* product-details-side Add to cart and Remove button behavior

The current cart workstream does not cover:

* checkout flow
* browser restart persistence
* storage clearing
* cross-user cart persistence
* multi-user cart behavior
* logout from multiple page locations

These exclusions keep the cart workstream focused and prevent it from expanding into checkout or session-management scope that belongs to later tasks.

## Markers

Tests are categorized using pytest markers such as:

* `smoke`
* `regression`
* `ui`
* `positive`
* `negative`
* `sorting`
* `navigation`

Markers allow selective test execution for different validation needs.

## Design Direction

The framework follows a modular architecture where:

* tests describe behavior and assertions,
* Page Objects handle page interactions,
* test data is externalized from test logic,
* fixtures prepare reusable test setup,
* documentation tracks test design and coverage,
* CI validates the project automatically.

Near-term architecture direction includes:

* completing final stabilization of the cart workstream before merge preparation
* extending automation coverage into checkout in a separate workstream
* keeping checkout scope separate from cart scope
* introducing BasePage only when repeated page-level behavior justifies it
* improving fixture organization only when the number of reusable setup flows grows
* enhancing reporting and diagnostics incrementally
* expanding API testing in a later project phase
* adding a future Selenium comparison module only after the Playwright framework is mature enough

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

The project should avoid:

* premature BasePage abstraction
* unnecessary helper layers
* duplicated selectors in tests when a Page Object method already exists
* test data duplication across workstreams
* mixing checkout behavior into cart tests
* expanding a workstream beyond its approved scope only because it is technically possible

## Current Architecture Status

The architecture is no longer only a setup foundation. It now contains three functional automation workstreams:

* Login Page Automation Workstream
* Inventory And Products Automation Workstream
* Cart Automation Workstream

The current branch contains completed cart automation coverage and is undergoing final review and stabilization before the next project step.

The next architecture step is to extend the same principles to check out coverage while avoiding unnecessary early abstractions and keeping checkout scenarios separated from cart scope.
