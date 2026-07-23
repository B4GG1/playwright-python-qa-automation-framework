# Testing Strategy

This document defines the testing approach for the QA automation framework.

The current focus is UI automation testing for the Sauce Demo application using Playwright and Pytest. The project follows an iterative testing strategy: manual test design is created before or alongside automation, selected scenarios are automated, and repeated interactions are gradually refactored into reusable framework components.

## System Under Test

* Application: Sauce Demo
* URL: `https://www.saucedemo.com/`

Sauce Demo is used as a stable training application for practicing UI automation, test design, Page Object Model, test data management, parametrization, CI validation, and framework development.

## Testing Approach

The project follows a progressive testing approach:

1. Identify test scenarios manually.
2. Write clear test cases.
3. Decide which scenarios should be automated.
4. Prepare test data when needed.
5. Implement automated tests using Playwright and Pytest.
6. Refactor repeated interactions into Page Object Model components.
7. Extract shared authenticated-page behavior when it is reused across pages.
8. Extract reusable assertions when the same validation logic is needed across multiple page areas.
9. Use fixtures to reduce repeated setup.
10. Use parametrization for repeated data-driven scenarios.
11. Categorize tests with pytest markers.
12. Validate tests locally and in CI.
13. Update documentation when test coverage changes.

This approach supports both QA thinking and automation engineering practice.

## Test Case Design

Test cases should be documented before or alongside automation work.

Recommended location:

```
test_cases/
```

Each test case should include:

* test case ID
* title
* preconditions
* test data
* steps
* expected result
* test type
* priority
* automation candidate status
* automation status when implemented
* reference to automated test file when applicable

Current implemented test case documentation:

```
test_cases/login-page.md
test_cases/inventory-page.md
test_cases/product-details-page.md
test_cases/cart-page.md
test_cases/checkout-page.md
```

Current test case identifiers include:

* `TC-LOGIN-XXX`
* `TC-INVENTORY-XXX`
* `TC-PRODUCT-DETAILS-XXX`
* `TC-CART-XXX`
* `TC-CHECKOUT-XXX`

These identifiers are also used in parametrized pytest output where practical.

## Current Automated Test Modules

Current automated test modules follow the one test file per covered page area principle:

```
tests/test_login_page.py
tests/test_inventory_page.py
tests/test_product_details_page.py
tests/test_cart_page.py
tests/test_checkout_page.py
```

Each automated test module maps to the corresponding manual test case file:

| Automated Test Module                | Manual Test Case File                | Test Case ID Range             |
|--------------------------------------|--------------------------------------|--------------------------------|
| `tests/test_login_page.py`           | `test_cases/login-page.md`           | `TC-LOGIN-001`–`019`           |
| `tests/test_inventory_page.py`       | `test_cases/inventory-page.md`       | `TC-INVENTORY-001`–`022`       |
| `tests/test_product_details_page.py` | `test_cases/product-details-page.md` | `TC-PRODUCT-DETAILS-001`–`014` |
| `tests/test_cart_page.py`            | `test_cases/cart-page.md`            | `TC-CART-001`–`014`            |
| `tests/test_checkout_page.py`        | `test_cases/checkout-page.md`        | `TC-CHECKOUT-001`–`018`        |

## Current Test Coverage

The current automated test coverage focuses on Sauce Demo Login, Inventory, Product Details, Cart, and Checkout page behavior.

Implemented login coverage includes:

* successful login with valid credentials
* login with invalid username
* login with invalid password
* login with empty username
* login with empty password
* login with empty credentials
* locked out user login attempt
* login with invalid username and invalid password
* error message close behavior
* login page elements visibility
* password field masking validation
* login form submission with Enter key
* direct inventory page access without login
* direct cart page access without login
* direct item details page access without login
* direct checkout information page access without login
* direct checkout overview page access without login
* direct checkout complete page access without login
* input error icon visibility after failed login

Implemented inventory coverage includes:

* inventory page visibility after successful login
* product list visibility
* product card content validation
* cart page navigation from inventory page
* product add-to-cart from inventory page
* inventory-side Add to cart button changing to Remove
* cart badge visibility after adding one product
* cart badge count update after adding multiple products
* product sorting by name A to Z
* product sorting by name Z to A
* product sorting by price low to high
* product sorting by price high to low
* product details navigation from inventory product name for all products
* product details navigation from inventory product image for all products
* all-products add-to-cart coverage from inventory page
* inventory-side remove-from-cart behavior
* inventory-side Remove button changing back to Add to cart
* cart badge count update after removing one of multiple products
* cart badge disappearance after removing the last product
* all-products remove-from-cart coverage from inventory page
* product details navigation from product name for an example product
* product details navigation from product image for an example product

Implemented product details coverage includes:

* product details content visibility for a selected product
* product details content matching centralized product test data for all products
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

Implemented cart coverage includes:

* empty cart state before adding products
* added product visibility on cart page
* cart product content matching added product data
* product remove-from-cart from cart page
* cart badge removal after removing the last product
* Continue Shopping navigation from cart page to inventory page
* cart state persistence after logout and re-login
* all-products cart visibility coverage
* cart product content validation for each product
* cart badge decrement after removing one of multiple products
* product details navigation from cart item name
* Continue Shopping cart state preservation
* all-products remove-from-cart coverage from cart page
* checkout information page navigation from the cart page with product in cart

Implemented checkout coverage includes:

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

## Test Types

### Smoke Tests

Smoke tests validate the most critical application flows and should execute quickly.

Current examples:

* login page basic UI availability
* successful login with valid credentials
* inventory page visibility after successful login
* product list visibility
* cart page can be opened from the inventory page
* product can be added to cart from inventory page
* product can be removed from cart page
* product details content is displayed for a selected product
* product can be added to cart from product details page
* product can be removed from cart from product details page
* checkout button opens checkout information page with product in cart
* checkout information form displays required customer fields
* checkout information form continues to overview when valid data is provided
* checkout overview displays selected product
* checkout overview price summary is correct for one product
* finish button completes checkout and opens order confirmation page

### Regression Tests

Regression tests validate that existing functionality continues to work after changes.

Current examples:

* negative login scenarios
* empty credential validation
* locked out user validation
* error message behavior
* protected route access validation
* protected checkout route access validation
* product card content validation
* product details navigation
* product details content validation
* product sorting behavior
* cart badge behavior
* cart item content validation
* add-to-cart and remove-from-cart behavior from inventory page
* add-to-cart and remove-from-cart behavior from product details page
* add-to-cart and remove-from-cart behavior from cart page
* cart state persistence after logout and re-login
* Continue Shopping cart state preservation
* checkout information required field validation
* checkout information error message close behavior
* checkout overview product summary validation
* checkout overview price summary validation
* checkout overview cancellation behavior
* checkout complete page confirmation validation
* Back Home navigation after order completion

### UI Tests

UI tests validate user-facing browser behavior using Playwright.

Current examples:

* login form visibility
* password field configuration
* error message visibility
* error message close behavior
* input error icon visibility
* inventory page visibility after login
* product list visibility
* product card content visibility
* product details page visibility
* product sorting behavior
* cart page visibility
* cart item visibility
* cart badge visibility
* Add to cart and Remove button visibility
* Continue Shopping navigation behavior
* checkout information form visibility
* checkout information field validation messages
* checkout information input error icon visibility
* checkout overview product item visibility
* checkout overview price summary visibility
* checkout complete page confirmation visibility

### Positive Tests

Positive tests validate expected successful user behavior.

Current examples:

* valid user can log in successfully
* valid user can submit login form using Enter key
* product details can be opened from product name
* product details can be opened from product image
* user can return from product details page to inventory page
* user can add products to the cart
* user can remove products from the cart
* user can open the cart page from authenticated pages
* cart state persists after logout and re-login
* user can continue from checkout information to checkout overview with valid customer data
* user can complete checkout from checkout overview
* user can return home after order completion

### Negative Tests

Negative tests validate error handling and invalid user behavior.

Current examples:

* invalid login
* empty required login fields
* locked out user access
* direct protected route access without login
* empty required checkout information fields

### Access Control Tests

Access control tests validate that protected application areas cannot be accessed without proper authentication.

Current examples:

* unauthenticated user cannot directly access the inventory page
* unauthenticated user cannot directly access the cart page
* unauthenticated user cannot directly access an item details page
* unauthenticated user cannot directly access the checkout information page
* unauthenticated user cannot directly access the checkout overview page
* unauthenticated user cannot directly access the checkout complete page

### Sorting Tests

Sorting tests validate that product ordering changes correctly after selecting sorting options.

Current examples:

* products can be sorted by name A to Z
* products can be sorted by name Z to A
* products can be sorted by price low to high
* products can be sorted by price high to low

Sorting tests use plain Python assertions for comparing extracted product names and converted product prices.

### Navigation Tests

Navigation tests validate page transitions and user navigation paths.

Current examples:

* cart page can be opened from the inventory page
* cart page can be opened from the product details page
* product details can be opened from inventory product names
* product details can be opened from inventory product images
* product details can be opened from cart item names
* product details can be opened from checkout overview item names
* user can return from product details page to inventory page
* user can return from cart page to inventory page
* Continue Shopping returns the user from the cart page to the inventory page while preserving cart state
* Checkout button opens checkout information page from the cart page with product in cart
* checkout information Cancel button returns the user to the cart page while preserving cart state
* checkout overview Cancel button returns the user to the inventory page while preserving cart state
* Back Home returns the user to the inventory page after order completion

### End-to-End Tests

End-to-end tests validate complete user journeys across multiple pages.

Current examples:

* log in, add product to cart from inventory, and verify it on the cart page
* log in, open product details, add product to cart, and verify cart state
* add product to cart, log out, log in again, and verify cart state is preserved
* add multiple products, remove one product, and verify badge/cart state
* add product to cart, open checkout, submit customer information, finish checkout, and verify order completion
* complete checkout and return to inventory page with Back Home

## Test Design Principles

Automated tests should follow:

* Arrange / Act / Assert structure
* clear and descriptive test names
* stable assertions
* reusable Page Objects
* shared authenticated-page behavior where appropriate
* reusable assertion helpers where validation is shared across page areas
* externalized test data where useful
* no hardcoded waits
* independent test execution
* readable failure output
* clear mapping to manual test cases where practical

Tests should focus on behavior, while page-specific UI interactions should be handled by Page Object classes.

## Page Object Model Strategy

Page Object Model is used to separate test logic from page interaction logic.

Current implementation:

```
pages/base_page.py
pages/app_page.py
pages/login_page.py
pages/inventory_page.py
pages/product_details_page.py
pages/cart_page.py
pages/checkout_page.py
```

The `BasePage` object is responsible for:

* storing the Playwright `Page` instance
* storing page URL metadata where applicable
* opening the page URL through a shared `open()` method

The `AppPage` object is responsible for shared authenticated-page behavior, including:

* opening the cart page from authenticated page headers
* accessing the cart link
* accessing the cart badge
* opening the application menu
* logging out
* resetting app state
* opening the All Items page
* opening the About link
* exposing shared product-card/product-item locator helpers where reused by authenticated pages

The `LoginPage` object is responsible for:

* opening the login page
* filling username and password
* clicking the login button
* submitting login credentials
* reading error messages
* closing error messages
* exposing login page UI locators where needed
* exposing input error icon locators

The `InventoryPage` object is responsible for:

* exposing inventory page locators
* accessing the product list
* accessing product cards
* reading product names and prices
* sorting products
* opening product details from product name
* opening product details from product image
* adding products to the cart from inventory product cards
* removing products from the cart from inventory product cards

The `ProductDetailsPage` object is responsible for:

* exposing product details page locators
* exposing product details content locators
* exposing Add to cart and Remove button locators
* adding a product to the cart from the product details page
* removing a product from the cart from the product details page
* exposing the Back to products button
* returning from product details page to inventory page

The `CartPage` object is responsible for:

* opening the cart page
* exposing cart page locators
* accessing the cart contents container
* accessing the cart list
* accessing cart item cards
* locating cart items by product name
* reading cart item name, description, price, and quantity
* exposing Remove button locators
* removing products from the cart
* opening product details from cart item name
* exposing Continue Shopping button
* returning from cart page to inventory page
* exposing Checkout button locators
* opening checkout step one from the cart page

The `CheckoutInformationPage` object is responsible for:

* opening the checkout information page where direct navigation is required
* exposing checkout information form locators
* exposing First Name, Last Name, and Postal Code inputs
* exposing Continue and Cancel buttons
* filling customer information
* submitting checkout information
* exposing validation error message locators
* closing checkout information validation errors
* exposing input error icon locators
* returning from checkout information page to the cart page

The `CheckoutOverviewPage` object is responsible for:

* exposing checkout overview page locators
* accessing checkout overview product item cards
* locating checkout overview items by product name
* accessing checkout overview item name, description, price, and quantity
* exposing payment, shipping, item total, tax, and total summary locators
* exposing Cancel and Finish buttons
* returning from checkout overview page to inventory page
* opening product details from checkout overview item name
* completing checkout

The `CheckoutCompletePage` object is responsible for:

* exposing checkout complete page locators
* exposing completion header and message locators
* exposing Back Home button locators
* returning from checkout complete page to inventory page

Page Objects should be introduced when they reduce duplication and improve readability.

## Reusable Assertion Strategy

Reusable assertions are used when the same product-related or checkout-related validation appears across multiple page areas.

Current reusable assertion helper location:

```
framework/assertions/product_assertions.py
```

Current reusable product assertions support:

* inventory product card content validation
* product details content validation
* cart product item content validation
* checkout overview product item content validation
* checkout overview price summary validation
* inventory product state validation after checkout-related navigation
* price string conversion for numeric sorting and checkout summary assertions

Reusable assertion helpers should stay focused on shared validation logic. They should not contain navigation logic, test setup logic, or Page Object responsibilities.

## Fixture Strategy

Fixtures are used to prepare reusable test setup.

Current fixtures:

```
opened_login_page
standard_user
logged_in_inventory_page
inventory_page_with_one_product_in_cart
cart_page_with_one_product
checkout_step_one_page_with_one_product
checkout_step_two_page_with_one_product
checkout_last_step_page_with_one_product
```

The `opened_login_page` fixture:

* creates a `LoginPage` instance
* opens the login page
* returns a ready-to-use Page Object for login-related tests

The `standard_user` fixture:

* returns the primary valid user credentials from centralized login test data

The `logged_in_inventory_page` fixture:

* uses valid user credentials
* logs in through the login page
* returns a ready-to-use `InventoryPage` instance

The `inventory_page_with_one_product_in_cart` fixture:

* starts from a logged-in inventory page
* adds one deterministic product from centralized product test data to the cart
* returns the inventory page and selected product data

The `cart_page_with_one_product` fixture:

* starts from an inventory page with one product already in the cart
* opens the cart page
* returns the cart page and selected product data

The `checkout_step_one_page_with_one_product` fixture:

* starts from a cart page with one product already in the cart
* opens the checkout information page
* returns the checkout information page and selected product data

The `checkout_step_two_page_with_one_product` fixture:

* starts from checkout step one with one product already in the cart
* submits valid checkout customer information
* returns the checkout overview page and selected product data

The `checkout_last_step_page_with_one_product` fixture:

* starts from checkout overview with one product already in the cart
* finishes checkout
* returns the checkout complete page and selected product data

Fixtures should be added when setup logic becomes repeated across multiple tests.

Avoid creating too many fixtures too early. Fixture growth should follow real framework needs.

## Test Data Strategy

Test data should be separated from test logic when it improves readability, maintainability, or parametrization.

Current test data location:

```
test_data/login_test_data.py
test_data/product_test_data.py
test_data/checkout_test_data.py
```

Current login test data includes:

* valid user cases
* invalid login cases
* empty credential cases
* locked out user cases
* expected error messages
* protected route URL suffixes

Current product test data includes:

* product IDs
* product names
* product descriptions
* product prices
* product image paths

Current checkout test data includes:

* valid checkout customer information
* checkout required field error messages
* checkout page title expectations
* checkout overview summary label expectations
* checkout completion header and message expectations

Inventory, product details, cart, and checkout tests reuse:

* valid user data from login test data
* deterministic product data from product test data

A separate cart test data module is not needed at the current stage because cart tests reuse existing product and user data without introducing unique cart-only datasets.

A separate checkout test data module is used because checkout introduces checkout-specific customer data, required field messages, page title expectations, summary labels, and completion text.

Test data should support:

* clear test intent
* reduced hardcoding
* parametrized execution
* traceability to manual test case IDs

## Parametrization Strategy

Parametrization is used for repeated scenarios with the same test flow and different input data.

Current parametrized areas:

* invalid login scenarios
* empty credential scenarios
* locked out user scenario
* positive login user case
* protected route access scenarios, including checkout protected routes
* inventory product card validation
* product details navigation from inventory product name
* product details navigation from inventory product image
* product details content validation for all products
* add-to-cart and remove-from-cart checks across all products
* cart item content validation across all products
* checkout overview item validation across product data
* checkout overview product details navigation across product data
* selected single-case tests where test case ID visibility in `pytest -v` is desired

Parametrized test IDs should use manual test case IDs where practical, for example:

```
TC-LOGIN-002
TC-LOGIN-003
TC-LOGIN-004
TC-INVENTORY-001
TC-INVENTORY-013
TC-INVENTORY-015
TC-PRODUCT-DETAILS-002
TC-PRODUCT-DETAILS-014
TC-CART-001
TC-CART-009
TC-CART-013
TC-CHECKOUT-010
TC-CHECKOUT-015
```

This improves traceability between:

* manual test cases
* automated tests
* terminal output
* CI logs
* test reports

## Marker Strategy

Pytest markers are used to categorize tests.

Current markers:

* `smoke`
* `regression`
* `ui`
* `api`
* `e2e`
* `positive`
* `negative`
* `sorting`
* `navigation`

Example marker commands:

```
pytest -m smoke -v
pytest -m regression -v
pytest -m positive -v
pytest -m negative -v
pytest -m sorting -v
pytest -m navigation -v
pytest -m e2e -v
pytest -m "ui and smoke" -v
pytest -m "ui and regression" -v
pytest -m "ui and sorting" -v
pytest -m "ui and navigation" -v
```

Markers should be used consistently to support selective local and CI execution.

## Assertion Strategy

Assertions should be stable, meaningful, and focused on user-observable behavior where possible.

Current assertion examples:

* page URL matches expected page
* element is visible
* element is hidden
* error message text matches expected value
* password input has `type="password"`
* protected route redirects unauthenticated user to login page
* inventory page container is visible
* product list is visible
* product card content matches expected product data
* product details page content matches selected product data
* product names match expected sorted order
* product prices match expected sorted order after numeric conversion
* cart badge is visible
* cart badge text matches expected count
* cart badge is hidden when cart becomes empty
* cart item is visible
* cart item content matches added product data
* cart item quantity matches expected value
* Add to cart button changes to Remove
* Remove button changes cart state
* cart state remains visible after logout and re-login
* checkout information form is visible
* checkout required field error message matches expected value
* checkout information input error icons are visible
* checkout overview product content matches expected product data
* checkout overview item total matches selected product prices
* checkout overview total equals item total plus tax
* checkout complete header matches expected confirmation text
* checkout complete message matches expected confirmation text

Use Playwright assertions for UI/browser state when possible because they include built-in waiting behavior.

Use plain Python assertions when comparing simple values, such as extracted text, product names, converted prices, expected error message strings, checkout summary values, or sorted lists.

Use reusable assertion helpers when the same product-content or checkout-summary assertions are shared across test modules.

## Automation Priority

Automation should focus on:

* repeatable scenarios
* critical user flows
* regression-prone functionality
* stable application behavior
* high-value validation
* scenarios that benefit from CI execution
* scenarios with clear expected results and stable selectors

Not every possible case should be automated.

Some scenarios may remain manual or exploratory if automation would be unstable, low-value, or overly complex.

## Scope Boundaries

The project uses scope boundaries to keep workstreams focused and maintainable.

Current page-level automation boundaries:

* login behavior is included
* inventory behavior is included
* product details behavior is included
* cart behavior is included
* checkout behavior is included as dedicated Checkout Page coverage
* cart-owned checkout entry behavior is included in Cart Page coverage
* checkout protected route access validation is included in Login Page coverage
* browser restart persistence is excluded
* storage clearing is excluded
* cross-user cart persistence is excluded
* multi-user cart behavior is excluded
* logout from multiple page locations is excluded unless explicitly scoped

Cart Page coverage should not own detailed checkout information form behavior, checkout overview validation, or checkout completion validation. These scenarios belong to Checkout Page coverage.

## Reporting And Debugging

Test execution generates:

* pytest console output
* HTML reports using pytest-html
* screenshots on failure
* CI artifacts uploaded by GitHub Actions

Generated reports and screenshots should not be committed to Git.

They should be used as:

* local debugging outputs
* CI artifacts
* failure analysis evidence

## Local Validation Strategy

Recommended full local validation:

```
ruff check .
black --check .
isort . --check-only
pytest -v
```

Recommended validation when login tests are changed:

```
pytest -v tests/test_login_page.py
pytest -m negative -v
pytest -m "ui and smoke" -v
```

Recommended validation when inventory tests are changed:

```
pytest -v tests/test_inventory_page.py
pytest -m sorting -v
pytest -m "ui and sorting" -v
```

Recommended validation when product details tests are changed:

```
pytest -v tests/test_product_details_page.py
pytest -m navigation -v
pytest -m "ui and regression" -v
```

Recommended validation when cart tests are changed:

```
pytest -v tests/test_cart_page.py
pytest -m navigation -v
pytest -m "ui and navigation" -v
pytest -m "ui and regression" -v
```

Recommended validation when checkout tests are changed:

```
pytest -v tests/test_checkout_page.py
pytest -m e2e -v
pytest -m navigation -v
pytest -m "ui and regression" -v
pytest -m "ui and navigation" -v
```

For checkpoint or stabilization tasks, run relevant scoped modules and full validation when possible:

```
pytest -v tests/test_login_page.py
pytest -v tests/test_inventory_page.py
pytest -v tests/test_product_details_page.py
pytest -v tests/test_cart_page.py
pytest -v tests/test_checkout_page.py
pytest -v
```

The full test suite should still pass before a workstream is considered ready for merge unless a scoped validation exception is explicitly accepted.

## CI Validation Strategy

GitHub Actions validates the project automatically on:

* pushes to `main`
* pushes to `develop`
* pull requests targeting `main`
* pull requests targeting `develop`
* manual workflow execution

The CI pipeline should validate:

* dependency installation
* Playwright browser installation
* linting
* formatting
* import sorting
* test execution
* HTML report generation
* artifact upload

Failing tests or quality checks should block merging.

## Future Improvements

Planned improvements:

* broader end-to-end scenarios
* API testing layer
* multi-browser execution
* smoke and regression CI job separation
* marker-based CI job separation
* Allure reporting integration
* improved diagnostics and logs
* environment-based configuration
