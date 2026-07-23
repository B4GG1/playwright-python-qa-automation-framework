# Framework And Project Structure

This document describes the repository structure and the responsibility of each major directory and configuration file.

The framework is structured to support scalable UI automation, Page Object Model components, shared framework utilities, test data management, reporting, documentation, CI execution, and future framework expansion while maintaining readability and modularity.

## Current Project Structure

```text
playwright-python-qa-automation-framework/
│
├── .github/
│   └── workflows/              # GitHub Actions CI workflows
│
├── config/                     # Framework and environment configuration
├── docs/                       # Project documentation
├── framework/                  # Shared framework utilities and reusable assertions
│   └── assertions/             # Shared assertion helpers
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
* Playwright Chromium browser installation
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
* technology stack documentation
* feature overview documentation

### `framework/`

Contains shared framework-level utilities, reusable assertions, and common framework logic that is not owned by a specific Page Object.

Current implementation:

```text
framework/assertions/product_assertions.py
```

Current responsibility:

* reusable product-content assertions
* inventory product card content validation helpers
* product details content validation helpers
* cart item content validation helpers
* checkout overview product item content validation helpers
* checkout overview price summary validation helpers
* shared product price conversion helper for numeric sorting and checkout summary assertions

This directory should only be expanded when repeated framework logic appears across multiple test modules or page areas.

Reusable framework helpers should not contain page navigation, test setup, or Page Object responsibilities.

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
pages/checkout_page.py
```

Current responsibility:

* page-specific locators
* page interaction methods
* reusable UI actions
* separation of page interaction logic from test logic
* lightweight navigation between Page Objects when a user action opens a different page
* shared authenticated-page behavior through `AppPage`

The current Page Object layer includes:

* `BasePage`, which stores the Playwright `Page` instance, page URL metadata where applicable, and shared page opening behavior
* `AppPage`, which owns shared authenticated-page behavior such as cart link access, cart badge access, application menu interactions, logout, reset app state, All Items navigation, About link access, and shared product locator helpers
* `LoginPage`, which supports login page interactions, error message handling, input error icon access, and login page UI elements
* `InventoryPage`, which supports inventory page visibility, product list access, product card access, product sorting, product details navigation, and inventory-side product add/remove actions
* `ProductDetailsPage`, which supports product details content access, product details cart actions, Back to products navigation, and product-details-side add/remove state
* `CartPage`, which supports cart page availability, cart contents access, cart item lookup, cart item content access, remove-from-cart actions, product details navigation from cart item name, Continue Shopping navigation, checkout button access, cart-owned checkout step one navigation, and cart badge behavior
* `CheckoutInformationPage`, which supports checkout information form fields, validation errors, input error icons, customer information submission, checkout step one cancellation, and transition to checkout overview
* `CheckoutOverviewPage`, which supports checkout overview product items, payment/shipping/price summary locators, checkout overview cancellation, product details navigation from overview item names, and finishing checkout
* `CheckoutCompletePage`, which supports order confirmation content, checkout completion state, and Back Home navigation after order completion

The Page Object layer should remain focused on interactions and locators. Test assertions should remain in tests or reusable assertion helpers when shared across page areas.

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

```text
test_cases/login-page.md
test_cases/inventory-page.md
test_cases/product-details-page.md
test_cases/cart-page.md
test_cases/checkout-page.md
```

Current responsibility:

* manual test case documentation
* test design before and alongside automation
* mapping manual test cases to automated test files
* documenting automation coverage status
* documenting scope boundaries for each application area
* keeping one test case file per covered page area

Current test case identifiers include:

* `TC-LOGIN-XXX`
* `TC-INVENTORY-XXX`
* `TC-PRODUCT-DETAILS-XXX`
* `TC-CART-XXX`
* `TC-CHECKOUT-XXX`

These identifiers are also reflected in parametrized pytest output where practical.

### `test_data/`

Contains externalized test data.

Current implementation:

```text
test_data/login_test_data.py
test_data/product_test_data.py
test_data/checkout_test_data.py
```

Current responsibility:

* valid login user data
* invalid login cases
* empty credentials cases
* locked out user cases
* expected login error messages
* protected route URL suffixes
* product IDs
* product names
* product descriptions
* product prices
* product image paths
* valid checkout customer information
* checkout required field error messages
* checkout step title expectations
* checkout overview summary label expectations
* checkout completion header and message expectations
* deterministic product data reused by inventory, product details, cart, and checkout tests
* test case IDs for parametrized tests where practical

This directory keeps test data separate from test logic and supports pytest parametrization.

Inventory, Product Details, Cart, and Checkout tests intentionally reuse centralized product data instead of introducing page-specific product datasets too early.

A separate cart test data module is not needed at the current stage because cart tests reuse existing product and user data without introducing unique cart-only datasets.

A separate checkout test data module is used because checkout introduces checkout-specific customer data, validation messages, page titles, summary labels, and completion text.

### `tests/`

Contains automated test suites.

Current test modules follow the one test file per covered page area principle:

```text
tests/test_login_page.py
tests/test_inventory_page.py
tests/test_product_details_page.py
tests/test_cart_page.py
tests/test_checkout_page.py
```

Current test module responsibilities:

* `test_login_page.py` — login page scenarios, negative login handling, login UI behavior, keyboard submission, input error icons, and protected route access validation including checkout protected routes
* `test_inventory_page.py` — inventory page visibility, product list validation, product card content, sorting, cart actions from inventory, cart badge behavior, and product details navigation from inventory product cards
* `test_product_details_page.py` — product details content, return navigation, add/remove actions from product details, cart badge behavior, cart navigation from product details, and all-products product details coverage
* `test_cart_page.py` — cart empty state, added product visibility, cart item content, remove actions, cart badge behavior, Continue Shopping navigation, cart state persistence, all-products cart checks, product details navigation from cart item name, and cart-owned checkout entry navigation
* `test_checkout_page.py` — checkout information form validation, checkout information error state validation, checkout information cancellation, checkout overview product and price summary validation, checkout overview cancellation, product details navigation from checkout overview, checkout finish action, checkout complete confirmation validation, and Back Home navigation after order completion

Planned future test modules may include:

* API tests
* broader regression suites
* cross-browser execution suites if needed

## Root Configuration Files

### `conftest.py`

Contains shared Pytest hooks, fixtures, and test execution configuration.

Current usage:

* screenshot capture on test failure
* reusable `opened_login_page` fixture
* reusable `standard_user` fixture
* reusable `logged_in_inventory_page` fixture
* reusable `inventory_page_with_one_product_in_cart` fixture
* reusable `cart_page_with_one_product` fixture
* reusable `checkout_step_one_page_with_one_product` fixture
* reusable `checkout_step_two_page_with_one_product` fixture
* reusable `checkout_last_step_page_with_one_product` fixture

The `opened_login_page` fixture prepares a `LoginPage` instance and opens the login page before a test starts.

The `standard_user` fixture returns the primary valid user credentials from centralized login test data.

The `logged_in_inventory_page` fixture logs in with a valid user and returns an `InventoryPage` instance for inventory, product-details, cart-related, and checkout-related tests.

The `inventory_page_with_one_product_in_cart` fixture starts from a logged-in inventory page, adds one deterministic product to the cart, and returns the inventory page together with selected product data.

The `cart_page_with_one_product` fixture starts from an inventory page with one product already in the cart, opens the cart page, and returns the cart page together with selected product data.

The `checkout_step_one_page_with_one_product` fixture starts from a cart page with one product already in the cart, opens the checkout information page, and returns the checkout information page together with selected product data.

The `checkout_step_two_page_with_one_product` fixture starts from checkout step one with one product already in the cart, submits valid checkout customer information, and returns the checkout overview page together with selected product data.

The `checkout_last_step_page_with_one_product` fixture starts from checkout overview with one product already in the cart, finishes checkout, and returns the checkout complete page together with selected product data.

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
* `navigation`

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

## Current Page-Level Test Suite Structure

The current page-level automation structure is organized around one manual test case file and one automated test module per covered page area.

```text
test_cases/login-page.md
        ↓
test_data/login_test_data.py
        ↓
pages/login_page.py
        ↓
tests/test_login_page.py
        ↓
pytest markers and parametrized output
        ↓
GitHub Actions CI validation
```

```text
test_cases/inventory-page.md
        ↓
test_data/product_test_data.py
        ↓
pages/app_page.py
pages/inventory_page.py
framework/assertions/product_assertions.py
        ↓
tests/test_inventory_page.py
        ↓
pytest markers and parametrized output
        ↓
GitHub Actions CI validation
```

```text
test_cases/product-details-page.md
        ↓
test_data/product_test_data.py
        ↓
pages/app_page.py
pages/product_details_page.py
framework/assertions/product_assertions.py
        ↓
tests/test_product_details_page.py
        ↓
pytest markers and parametrized output
        ↓
GitHub Actions CI validation
```

```text
test_cases/cart-page.md
        ↓
test_data/login_test_data.py
test_data/product_test_data.py
        ↓
pages/app_page.py
pages/inventory_page.py
pages/product_details_page.py
pages/cart_page.py
pages/checkout_page.py
framework/assertions/product_assertions.py
        ↓
tests/test_cart_page.py
        ↓
pytest markers and parametrized output
        ↓
GitHub Actions CI validation
```

```text
test_cases/checkout-page.md
        ↓
test_data/login_test_data.py
test_data/product_test_data.py
test_data/checkout_test_data.py
        ↓
pages/app_page.py
pages/inventory_page.py
pages/cart_page.py
pages/product_details_page.py
pages/checkout_page.py
framework/assertions/product_assertions.py
        ↓
tests/test_checkout_page.py
        ↓
pytest markers and parametrized output
        ↓
GitHub Actions CI validation
```

## Current Login Test Suite Structure

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
* protected checkout information route access
* protected checkout overview route access
* protected checkout complete route access
* input error icon visibility after failed login

Protected route validation currently includes direct access checks for:

* inventory page
* cart page
* item details page
* checkout information page
* checkout overview page
* checkout complete page

## Current Inventory Test Suite Structure

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

## Current Product Details Test Suite Structure

The product details automation area covers:

* product details content visibility for a selected product
* product details content matching centralized product data for all products
* return navigation from product details page to inventory page
* product-details-side Add to cart button changing to Remove
* product add-to-cart from product details page
* all-products add-to-cart coverage from product details page
* product remove-from-cart from product details page
* product-details-side Remove button changing back to Add to cart
* cart badge visibility after adding from product details page
* cart badge count update when cart is not empty
* cart badge count update after removing one of multiple products from product details page
* cart badge disappearance after removing the last product from product details page
* cart page navigation from product details page
* all-products remove-from-cart coverage from product details page

## Current Cart Test Suite Structure

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
* checkout information page navigation from the cart page with product in cart

Cart coverage owns the checkout entry point from the cart page. Detailed checkout information form behavior, checkout overview behavior, and order completion behavior are owned by Checkout Page coverage.

## Current Checkout Test Suite Structure

The checkout automation area covers:

* checkout information form displays required customer fields
* checkout information form requires first name
* checkout information form requires last name
* checkout information form requires postal code
* input error icons are displayed after failed checkout information submission
* checkout information error message can be closed after validation failure
* checkout information form continues to overview when valid data is provided
* checkout information cancel returns to cart and preserves cart item
* checkout overview displays selected product
* checkout overview displays each selected product
* checkout overview price summary is correct for one product
* checkout overview price summary is correct for multiple products
* checkout overview cancel returns to inventory page
* product details can be opened from checkout overview item name
* product details can be opened from checkout overview item name for each product
* finish button completes checkout and opens order confirmation page
* checkout complete page displays order confirmation message
* Back Home returns to inventory page after order completion

## Architecture Goals

The project structure is designed to support:

* maintainable test organization
* one automated test module per covered page area
* one manual test case file per covered page area
* clear separation of framework layers
* reusable automation components
* scalable Page Object Model implementation
* shared authenticated-page behavior through `AppPage`
* reusable product and checkout assertion helpers
* centralized test configuration
* centralized test data
* reusable pytest fixtures
* CI/CD-ready development workflow
* readable and consistent test structure
* traceability between manual test cases and automated tests
* future UI and API automation expansion

## Structure Evolution

The project has moved beyond the initial foundation stage and now contains completed page-level automation coverage for:

* Login Page
* Inventory Page
* Product Details Page
* Cart Page
* Checkout Page

Implemented structure currently includes:

* shared `BasePage` abstraction
* shared authenticated `AppPage` abstraction
* concrete `LoginPage` Page Object
* concrete `InventoryPage` Page Object
* concrete `ProductDetailsPage` Page Object
* concrete `CartPage` Page Object
* concrete checkout Page Objects
* reusable product and checkout assertion helpers
* centralized login test data
* centralized product test data
* centralized checkout test data
* reusable opened login page fixture
* reusable standard user fixture
* reusable logged-in inventory page fixture
* reusable inventory page with one product in cart fixture
* reusable cart page with one product fixture
* reusable checkout step one page with one product fixture
* reusable checkout step two page with one product fixture
* reusable checkout complete page with one product fixture
* login test case documentation
* inventory test case documentation
* product details test case documentation
* cart test case documentation
* checkout test case documentation
* parametrized login tests
* parametrized inventory product tests
* parametrized product details tests
* parametrized cart tests
* parametrized checkout tests
* marker-based test categorization
* login UI and access-control coverage
* inventory page, product details navigation, and product sorting coverage
* product details content, add/remove, cart badge, and cart navigation coverage
* cart page, cart item, cart badge, remove-from-cart, continue shopping, cart persistence, and checkout entry coverage
* checkout information form, checkout overview, checkout completion, and checkout navigation coverage
* GitHub Actions CI validation
* pytest HTML reporting
* screenshot capture on test failure
* local and CI quality checks

Future improvements will include:

* expanded fixture organization when setup flows grow
* reporting utilities
* API testing structure
* Selenium comparison module
* additional test suites for future application areas
