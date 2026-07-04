# Architecture

This document describes the current architecture of the QA automation framework.

The project follows a lightweight, modular architecture focused on readability, maintainability, traceability, and incremental framework growth. The architecture is intentionally practical: it includes Page Object Model, shared authenticated-page behavior, reusable product assertions, reusable pytest fixtures, centralized test data, marker-based test organization, CI execution, reporting support, screenshot capture, and technical documentation.

## Current Architecture Scope

The current framework includes:

* Pytest-based test execution
* Playwright browser automation
* Page Object Model for Login, Inventory, Product Details, and Cart pages
* shared `BasePage` abstraction
* shared authenticated-page behavior through `AppPage`
* reusable product assertion helpers
* reusable pytest fixtures
* centralized login and product test data
* marker-based test categorization
* parametrized test execution with manual test case IDs where practical
* CI execution with GitHub Actions
* code quality tooling
* HTML reporting and CI artifacts
* screenshot capture on test failure
* manual test case documentation mapped to automated tests
* one automated test module per covered page area
* one manual test case file per covered page area

The current automated coverage focuses on:

* Sauce Demo login page and authentication behavior
* protected route access validation
* inventory page availability
* product list and product card validation
* inventory-side product details navigation
* product details page validation
* product sorting
* cart page navigation
* empty cart state
* add-to-cart behavior from inventory and product details pages
* cart badge behavior
* cart item visibility and content validation
* remove-from-cart behavior from inventory, product details, and cart pages
* Continue Shopping navigation
* cart state persistence after logout and re-login

Checkout coverage is intentionally excluded from the current page-level Login, Inventory, Product Details, and Cart scope and is planned for a later workstream.

## Project Layers

The framework is organized into the following layers.

### `tests/`

Contains automated test suites.

Current test modules follow the one test file per covered page area principle:

```text
tests/test_login_page.py
tests/test_inventory_page.py
tests/test_product_details_page.py
tests/test_cart_page.py
```

Current responsibilities:

* tests describe behavior and expected results
* tests use Page Objects for interactions
* tests use Playwright assertions for UI/browser state
* tests use plain Python assertions for already extracted data comparisons
* tests use reusable assertion helpers when the same product-content validation is shared across page areas
* tests use centralized test data instead of hardcoded repeated data
* tests keep traceability to manual test cases where practical

Test modules should not duplicate selectors when a Page Object method already exposes the interaction or locator.

### `pages/`

Contains Page Object Model classes.

Current implementation:

```text
pages/base_page.py
pages/app_page.py
pages/login_page.py
pages/inventory_page.py
pages/product_details_page.py
pages/cart_page.py
```

The Page Object layer is responsible for:

* page-specific locators
* reusable page actions
* interaction methods
* hiding direct selector usage from tests where practical
* returning the next Page Object when navigation changes the current page context
* keeping shared authenticated-page behavior out of individual page classes when it is reused across pages

The Page Object layer should remain focused on page interaction logic. It should not contain test assertions except when exposing locator or state methods that tests assert against.

### `BasePage`

`BasePage` provides the minimal shared page foundation.

Current responsibilities:

* store the Playwright `Page` instance
* provide shared URL metadata through `URL`
* provide shared `open()` behavior for pages with direct URL navigation

`BasePage` should stay intentionally small. It should not become a dumping ground for unrelated helpers.

### `AppPage`

`AppPage` represents shared authenticated-page behavior.

Current responsibilities:

* cart link access
* opening the cart page from authenticated page headers
* cart badge access
* cart badge count reading
* burger menu access
* closing the application menu
* logout support
* reset app state support
* All Items navigation support
* About link access
* shared product-like item locators used by authenticated page areas

`AppPage` is the correct owner for behavior that is shared by authenticated pages such as Inventory, Product Details, and Cart.

### `LoginPage`

`LoginPage` centralizes login page interactions such as:

* opening the login page
* filling username
* filling password
* clicking the login button
* submitting credentials
* reading error messages
* closing error messages
* exposing relevant login page locators
* exposing input error icon locators

`LoginPage` does not inherit authenticated shared behavior because the login page is outside the authenticated application area.

### `InventoryPage`

`InventoryPage` centralizes inventory page interactions such as:

* accessing the inventory container
* accessing the product list
* accessing product cards
* locating product cards by product name
* reading product names and prices
* sorting products
* opening product details from product name
* opening product details from product image
* adding products to the cart from inventory product cards
* removing products from the cart from inventory product cards

`InventoryPage` inherits shared authenticated behavior through `AppPage`.

### `ProductDetailsPage`

`ProductDetailsPage` centralizes product details page interactions such as:

* opening a product details page by product ID
* accessing product details content
* accessing Add to cart and Remove buttons
* adding a product to the cart from the product details page
* removing a product from the cart from the product details page
* accessing the Back to products button
* returning to the inventory page

`ProductDetailsPage` inherits shared authenticated behavior through `AppPage`.

### `CartPage`

`CartPage` centralizes cart page interactions such as:

* opening the cart page directly
* accessing the cart contents container
* accessing the cart list
* accessing cart item cards
* locating cart item cards by product name
* accessing cart item name, description, price, quantity, and Remove button
* removing a product from the cart
* opening product details from a cart item name
* accessing Continue Shopping button
* returning from the cart page to the inventory page
* exposing Checkout button locators without validating checkout behavior in the current cart scope

`CartPage` inherits shared authenticated behavior through `AppPage`.

Checkout-related locators may exist in `CartPage`, but checkout behavior remains outside the current cart workstream test scope.

## `framework/`

Contains shared framework utilities that are not owned by a specific Page Object.

Current implementation:

```text
framework/assertions/product_assertions.py
```

Current responsibilities:

* reusable product text/content assertions
* inventory product card content validation
* product details content validation
* cart item content validation
* price string conversion for numeric sorting assertions

Reusable assertion helpers should stay focused on shared validation logic. They should not contain page navigation, test setup, or Page Object responsibilities.

## `test_data/`

Contains centralized test data used by automated tests.

Current implementation:

```text
test_data/login_test_data.py
test_data/product_test_data.py
```

Current login test data includes:

* valid user cases
* invalid login cases
* empty credential cases
* locked out user cases
* expected error messages
* protected route URL suffixes used in login-related assertions

Current product test data includes:

* product IDs
* product names
* product descriptions
* product prices
* product image paths

Inventory, Product Details, and Cart tests intentionally reuse centralized product test data instead of introducing page-specific product datasets too early.

Cart tests intentionally reuse existing login and product test data instead of introducing a separate cart-specific test data file. This keeps cart scenarios deterministic while avoiding unnecessary duplication.

The goal of this layer is to keep test data separate from test logic and support pytest parametrization.

## `conftest.py`

Contains shared pytest configuration, hooks, and fixtures.

Current responsibilities:

* screenshot capture on test failure
* reusable `opened_login_page` fixture
* reusable `standard_user` fixture
* reusable `logged_in_inventory_page` fixture
* reusable `inventory_page_with_one_product_in_cart` fixture
* reusable `cart_page_with_one_product` fixture

The `opened_login_page` fixture prepares a ready-to-use `LoginPage` instance with the login page already opened.

The `standard_user` fixture returns the primary valid user credentials from centralized login test data.

The `logged_in_inventory_page` fixture logs in with a valid user and returns a ready-to-use `InventoryPage` instance.

The `inventory_page_with_one_product_in_cart` fixture starts from a logged-in inventory page, adds one deterministic product to the cart, and returns the inventory page with selected product data.

The `cart_page_with_one_product` fixture starts from an inventory page with one product already in the cart, opens the cart page, and returns the cart page with selected product data.

Fixtures should be added when setup logic becomes repeated across multiple tests. Fixture growth should follow real framework needs.

## `config/`

Reserved for framework and environment configuration.

Potential future usage:

* base URLs
* environment-specific settings
* browser configuration
* execution configuration

This layer is intentionally minimal at the current stage.

## `reports/`

Stores generated runtime reports, screenshots, and debugging artifacts.

Runtime files are ignored by Git and published through CI artifacts when needed.

Current usage includes:

* pytest HTML reports
* screenshots from failed tests
* CI artifact sources

Generated files from this directory should not be committed.

## `test_cases/`

Contains manual test case documentation.

Current implementation:

```text
test_cases/login-page.md
test_cases/inventory-page.md
test_cases/product-details-page.md
test_cases/cart-page.md
```

Manual test cases are mapped to automated tests through identifiers such as:

* `TC-LOGIN-XXX`
* `TC-INVENTORY-XXX`
* `TC-PRODUCT-DETAILS-XXX`
* `TC-CART-XXX`

These identifiers are also used in parametrized pytest output where practical.

The project currently follows one manual test case file per covered page area.

## `docs/`

Contains technical documentation related to:

* architecture
* workflow
* testing strategy
* CI/CD pipeline
* quality tooling
* technology stack
* roadmap
* framework and project structure
* feature overview

Documentation should reflect the current project state after each workstream, cleanup, or checkpoint task.

## Current Login Test Architecture

The login test suite is built around the following structure:

```text
Manual login test cases
        ↓
Centralized login test data
        ↓
LoginPage Page Object
        ↓
Pytest login page test module
        ↓
Markers and parametrization
        ↓
CI execution and reports
```

### Login Coverage

The login automation area covers:

* successful login
* invalid username
* invalid password
* empty username
* empty password
* empty credentials
* locked out user
* invalid username and invalid password
* error message close behavior
* login page element visibility
* password field masking validation
* Enter key form submission
* protected inventory route access
* protected cart route access
* protected item details route access
* input error icon visibility after failed login

Protected route validation currently includes direct access checks for:

* inventory page
* cart page
* item details page

### Login Test Data

Login-related data is centralized in `test_data/login_test_data.py`.

This supports:

* readable tests
* reduced hardcoding
* consistent expected error messages
* parametrized test execution
* mapping automated tests to manual test cases
* protected route access validation

### Login Parametrization

Negative login scenarios and protected route scenarios use pytest parametrization to execute the same test logic against multiple data cases.

Parametrized IDs are based on manual test case IDs where practical, such as:

* `TC-LOGIN-002`
* `TC-LOGIN-003`
* `TC-LOGIN-004`

This improves traceability between documentation, test output, and automated coverage.

## Current Inventory Test Architecture

The inventory test suite is built around the following structure:

```text
Manual inventory test cases
        ↓
Centralized product test data
        ↓
InventoryPage Page Object
        ↓
Reusable logged-in inventory fixture
        ↓
Reusable product assertions where applicable
        ↓
Pytest inventory test module
        ↓
Markers and parametrization
        ↓
CI execution and reports
```

### Inventory Coverage

The inventory automation area covers:

* inventory page availability
* product list visibility
* product card content validation
* cart page navigation from inventory
* inventory-side add-to-cart behavior
* inventory-side Add to cart button changing to Remove
* cart badge visibility after adding one product
* cart badge count update after adding multiple products
* product sorting by name A to Z
* product sorting by name Z to A
* product sorting by price low to high
* product sorting by price high to low
* product details navigation from product name for all products
* product details navigation from product image for all products
* all-products add-to-cart coverage from inventory page
* inventory-side remove-from-cart behavior
* inventory-side Remove button changing back to Add to cart
* cart badge count update after removing one of multiple products
* cart badge disappearance after removing the last product
* all-products remove-from-cart coverage from inventory page
* smoke product details navigation from product name
* smoke product details navigation from product image

### Inventory Test Data

Inventory tests use centralized product data from `test_data/product_test_data.py`.

This supports:

* product list validation
* product card validation
* deterministic product details navigation
* product sorting validation
* deterministic cart product selection
* parametrized execution across all product data where useful

## Current Product Details Test Architecture

The product details test suite is built around the following structure:

```text
Manual product details test cases
        ↓
Centralized product test data
        ↓
ProductDetailsPage Page Object
        ↓
Reusable logged-in inventory fixture
        ↓
Reusable product assertions
        ↓
Pytest product details test module
        ↓
Markers and parametrization
        ↓
CI execution and reports
```

### Product Details Coverage

The product details automation area covers:

* product details content visibility for a selected product
* product details content matching centralized product data for all products
* return navigation from product details page to inventory page
* product-details-side Add to cart button changing to Remove
* product add-to-cart from product details page
* all-products add-to-cart coverage from product details page
* product remove-from-cart from product details page
* product-details-side Remove button changing back to Add to cart
* cart badge visibility after adding a product from product details page
* cart badge count update when adding from product details with a non-empty cart
* cart badge count update after removing one of multiple products from product details page
* cart badge disappearance after removing the last product from product details page
* cart page navigation from product details page
* all-products remove-from-cart coverage from product details page

### Product Details Test Data

Product Details tests use centralized product data from `test_data/product_test_data.py`.

This supports:

* product details content validation
* product details URL validation
* deterministic add-to-cart and remove-from-cart checks
* parametrized all-products execution where useful

## Current Cart Test Architecture

The cart test suite is built around the following structure:

```text
Manual cart test cases
        ↓
Centralized login and product test data
        ↓
InventoryPage, ProductDetailsPage, and CartPage Page Objects
        ↓
Reusable logged-in inventory and cart setup fixtures
        ↓
Reusable product assertions
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

### InventoryPage And ProductDetailsPage In Cart Scenarios

Cart tests reuse `InventoryPage` and `ProductDetailsPage` for cart-related actions that originate outside the cart page.

`InventoryPage` is used for:

* adding products to the cart from inventory cards
* validating inventory-side Add to cart and Remove button states
* validating cart badge behavior from the header
* opening the cart page
* logging out during cart persistence scenarios

`ProductDetailsPage` is used for:

* reaching cart-related states from product details flows where required
* preserving page-level navigation ownership between Product Details and Cart areas

### Cart Coverage

The cart automation area covers:

* cart page availability
* empty cart state
* added product visibility on cart page
* cart product content validation
* removing products from cart page
* cart badge removal after removing the last product
* Continue Shopping navigation
* cart state persistence after logout and re-login
* all-products cart visibility coverage
* cart item content validation for each product
* cart badge decrement after removing one of multiple products
* product details navigation from cart item name
* Continue Shopping cart state preservation
* all-products remove-from-cart coverage from cart page

### Cart Test Data

Cart tests intentionally use:

* valid user data from `test_data/login_test_data.py`
* deterministic product data from `test_data/product_test_data.py`

No separate cart test data module is currently required.

### Cart Scope Boundaries

The current cart scope covers:

* cart page availability
* empty cart state
* adding products to cart
* cart badge behavior
* cart item visibility
* cart item content validation
* removing products from cart
* navigation between cart and inventory page
* cart state persistence after logout and re-login
* product details navigation from cart item name

The current cart scope does not cover:

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

The current CI pipeline runs the full test suite. Marker-based execution is mainly used for local scoped validation and may be expanded into separate CI jobs later.

## Design Direction

The framework follows a modular architecture where:

* tests describe behavior and assertions
* Page Objects handle page interactions
* `BasePage` owns minimal common page behavior
* `AppPage` owns shared authenticated-page behavior
* reusable assertion helpers own repeated validation logic
* test data is externalized from test logic
* fixtures prepare reusable test setup
* documentation tracks test design and coverage
* CI validates the project automatically

Near-term architecture direction includes:

* completing final validation and documentation sync for Phase 3C
* keeping the current Login, Inventory, Product Details, and Cart structure stable before PR
* extending automation coverage into checkout in a separate workstream
* keeping checkout scope separate from cart scope
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

* unnecessary helper layers
* duplicated selectors in tests when a Page Object method already exists
* test data duplication across workstreams
* mixing checkout behavior into cart tests
* expanding a workstream beyond its approved scope only because it is technically possible
* moving page-specific interactions into generic helpers too early
* moving shared authenticated behavior back into individual page classes when it belongs in `AppPage`

## Current Architecture Status

The architecture is no longer only a setup foundation. It now contains completed page-level automation coverage for:

* Login Page
* Inventory Page
* Product Details Page
* Cart Page

The current architecture includes:

* `BasePage` for minimal shared page foundation
* `AppPage` for authenticated shared behavior
* Page Objects for Login, Inventory, Product Details, and Cart areas
* reusable product assertion helpers
* centralized login and product test data
* reusable pytest fixtures
* one automated test module per covered page area
* one manual test case file per covered page area
* marker-based test categorization
* parametrized test coverage with manual test case IDs where practical
* CI quality and full test validation
* HTML reporting and screenshot capture on failure

The current branch is undergoing Phase 3C final validation and documentation sync before PR readiness.

The next architecture step is to extend the same principles to check out coverage while avoiding unnecessary scope expansion and keeping checkout scenarios separated from cart behavior.
