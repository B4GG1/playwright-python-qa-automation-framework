# Testing Strategy

This document defines the testing approach for the QA automation framework.

The current focus is UI automation testing for the Sauce Demo application using Playwright and Pytest. The project follows an iterative testing strategy: manual test design is created before or alongside automation, selected scenarios are automated, and repeated interactions are gradually refactored into reusable framework components.

The strategy documented here reflects the current implemented test structure and normalized pytest marker behavior. The `main` branch represents the stable portfolio version, while `develop` and active workstream branches may contain newer validated changes before they are promoted to `main`.

## System Under Test

* Application: Sauce Demo
* URL: `https://www.saucedemo.com/`

Sauce Demo is used as a stable training application for practicing UI automation, test design, Page Object Model, test data management, parametrization, selective suite execution, CI validation, and framework development.

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
11. Categorize tests with explicit pytest markers.
12. Validate relevant marker suites and test modules locally.
13. Validate the full test suite locally and in CI when required.
14. Update test case and project documentation when coverage or strategy changes.
15. Promote stable validated snapshots from `develop` to `main` when they are ready for portfolio presentation.

This approach supports both QA thinking and automation engineering practice.

## Test Case Design

Test cases should be documented before or alongside automation work.

Recommended location:

```text
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
* automation status
* reference to automated test file when applicable

Current test case documentation:

```text
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

A documented test case may be marked as `Planned` before dedicated automation is implemented. The corresponding test case file remains the authoritative source for individual automation status.

## Current Automated Test Modules

Current automated test modules follow the one-test-file-per-covered-page-area principle:

```text
tests/test_login_page.py
tests/test_inventory_page.py
tests/test_product_details_page.py
tests/test_cart_page.py
tests/test_checkout_page.py
```

Each automated test module maps to the corresponding manual test case file:

| Automated Test Module                | Manual Test Case File                | Documented Test Case Range     |
| ------------------------------------ | ------------------------------------ | ------------------------------ |
| `tests/test_login_page.py`           | `test_cases/login-page.md`           | `TC-LOGIN-001`–`019`           |
| `tests/test_inventory_page.py`       | `test_cases/inventory-page.md`       | `TC-INVENTORY-001`–`022`       |
| `tests/test_product_details_page.py` | `test_cases/product-details-page.md` | `TC-PRODUCT-DETAILS-001`–`015` |
| `tests/test_cart_page.py`            | `test_cases/cart-page.md`            | `TC-CART-001`–`013`            |
| `tests/test_checkout_page.py`        | `test_cases/checkout-page.md`        | `TC-CHECKOUT-001`–`020`        |

Some documented scenarios are intentionally still planned:

* `TC-PRODUCT-DETAILS-015`
* `TC-CART-013`
* `TC-CHECKOUT-002`
* `TC-CHECKOUT-019`

Their test case files should be checked before treating the complete documented range as fully automated.

## Current Test Coverage

The current automated test coverage focuses on Sauce Demo Login, Inventory, Product Details, Cart, and Checkout behavior.

### Login Coverage

Implemented login coverage includes:

* successful login with valid credentials
* invalid username validation
* invalid password validation
* empty username validation
* empty password validation
* empty credentials validation
* locked out user validation
* combined invalid username and password validation
* error message close behavior
* login page elements visibility
* password field masking validation
* login form submission with Enter key
* protected inventory route access validation
* protected cart route access validation
* protected product details route access validation
* protected checkout information route access validation
* protected checkout overview route access validation
* protected checkout complete route access validation
* input error icon visibility after failed login
* lightweight Sauce Demo smoke availability check

### Inventory Coverage

Implemented inventory coverage includes:

* inventory page visibility after successful login
* product list validation
* product card content validation
* cart page navigation
* representative add-to-cart flow
* Add to cart and Remove button state validation
* cart badge visibility and count validation
* product sorting by name
* product sorting by price
* product details navigation through product names
* product details navigation through product images
* all-products add-to-cart coverage
* representative remove-from-cart flow
* all-products remove-from-cart coverage
* representative and full product-navigation coverage

### Product Details Coverage

Implemented product details coverage includes:

* representative product details visibility
* all-products product details validation
* return navigation to inventory
* Add to cart and Remove button state validation
* representative add-to-cart behavior
* all-products add-to-cart coverage
* representative remove-from-cart behavior
* all-products remove-from-cart coverage
* cart badge visibility and count behavior
* cart navigation from product details

Full Product Details → Cart navigation coverage for every product is documented separately and remains planned.

### Cart Coverage

Implemented cart coverage includes:

* initial empty-cart state
* representative cart item visibility and content
* representative remove-from-cart behavior
* cart badge removal after removing the last item
* Continue Shopping navigation
* cart state persistence after logout and re-login
* all-products cart content validation
* cart badge decrement behavior
* representative Product Details navigation from cart item name
* Continue Shopping cart-state preservation
* all-products remove-from-cart coverage
* checkout information page navigation

Full Cart → Product Details navigation coverage for every product is documented separately and remains planned.

### Checkout Coverage

Implemented checkout coverage includes:

* detailed checkout information form validation
* required First Name validation
* required Last Name validation
* required Postal Code validation
* checkout input error icon validation
* checkout error message close behavior
* valid customer information transition to Checkout Overview
* checkout information cancellation back to Cart
* representative Checkout Overview product validation
* all-products Checkout Overview validation
* representative price summary validation
* multiple-product price summary validation
* checkout overview cancellation back to Inventory
* representative Product Details navigation from Checkout Overview
* all-products Product Details navigation from Checkout Overview
* Finish transition to Checkout Complete
* detailed checkout completion content validation
* Back Home navigation to Inventory

Dedicated lightweight smoke validation of the Checkout Information form and Checkout Complete page is documented and remains planned.

## Marker Strategy

Pytest markers are used to create meaningful, selectively executable test suites.

Markers describe different dimensions of test intent. They are not mutually exclusive.

A test may therefore legitimately use several markers when it belongs to several suites.

For example:

```python
@pytest.mark.smoke
@pytest.mark.navigation
@pytest.mark.e2e
```

This means the same test is:

* a representative critical smoke check
* a navigation scenario
* a checkpoint in the primary end-to-end purchase journey

Running any matching marker selection should collect that test.

Current executable markers are:

* `smoke`
* `regression`
* `ui`
* `e2e`
* `security`
* `sorting`
* `navigation`

Marker definitions are registered in:

```text
pytest.ini
```

The registered marker definitions are the configuration-level source of truth. Test modules and test case metadata should remain aligned with those definitions.

### Smoke

`smoke` identifies fast representative validation of critical functionality.

Smoke coverage should answer whether an important feature or flow works at a representative level without attempting to validate every applicable variant.

Typical smoke patterns include:

* successful login
* representative invalid login handling
* core page availability
* representative add-to-cart or remove-from-cart behavior
* representative page navigation
* representative cart content validation
* critical checkout flow checkpoints

Where both representative and broader coverage exist, the representative scenario should normally be Smoke while the expanded counterpart should normally be Regression.

A Smoke marker should not automatically imply Regression.

### Regression

`regression` identifies broader validation across expanded or full applicable cases.

Regression coverage is used when a scenario intentionally validates more depth than the representative Smoke equivalent.

Typical regression patterns include:

* additional credential validation variants
* detailed UI state validation
* validation across every product
* multiple-product behavior
* full navigation coverage across all applicable products
* detailed cart state transitions
* detailed checkout field validation
* detailed checkout completion content validation

Regression is not a default marker for every test that is not Smoke. Dedicated categories such as `security`, `sorting`, or `navigation` may stand alone when they already describe the scenario accurately.

### UI

`ui` identifies tests whose primary validation includes visibility, presentation, UI state, or direct behavior of user-interface elements.

Typical UI validations include:

* form element visibility
* error message visibility and content
* error icon visibility
* button state changes
* product card content
* cart badge state
* Checkout Overview content
* completion page content

A Playwright test does not automatically require the `ui` marker.

Tests whose primary purpose is navigation, sorting, access control, or another dedicated behavior do not need `ui` unless direct UI state or presentation is also a meaningful part of the validation.

### Security

`security` identifies access-control and protected-route tests.

Current Security coverage validates that an unauthenticated user cannot directly access protected application areas.

Current protected routes include:

* Inventory
* Cart
* Product Details
* Checkout Information
* Checkout Overview
* Checkout Complete

These tests are currently owned by Login coverage because authentication state determines access to the protected application areas.

Security is a dedicated marker and does not need to be combined with Regression simply to make the test part of a broader suite.

### Sorting

`sorting` identifies product sorting behavior.

Current Sorting coverage validates:

* product name A to Z
* product name Z to A
* product price low to high
* product price high to low

Sorting tests use deterministic product data and plain Python comparisons for extracted product names and numeric product prices.

Sorting is a dedicated marker and does not automatically require `ui` or `regression`.

### Navigation

`navigation` identifies meaningful page transitions.

Current examples include:

* Inventory → Cart
* Inventory → Product Details
* Product Details → Inventory
* Product Details → Cart
* Cart → Inventory
* Cart → Product Details
* Cart → Checkout Information
* Checkout Information → Cart
* Checkout Information → Checkout Overview
* Checkout Overview → Inventory
* Checkout Overview → Product Details
* Checkout Overview → Checkout Complete
* Checkout Complete → Inventory

The authentication transition from Login to Inventory is intentionally excluded from the Navigation suite.

Navigation may be combined with Smoke or Regression depending on whether the test validates one representative transition or broader applicable coverage.

Navigation may also be combined with UI when meaningful UI state is validated together with the transition.

### End-to-End

`e2e` identifies tests forming the complete primary purchase journey through checkout completion and return to Inventory.

The E2E suite is intentionally implemented as a collection of independent checkpoint tests rather than one state-sharing monolithic test.

Each checkpoint:

* can run independently
* prepares its own state through fixtures or setup
* validates one important part of the purchase journey
* does not depend on execution order
* does not share browser state with another E2E checkpoint

Running:

```bash
pytest -m e2e -v
```

collects the current automated checkpoints that together represent the primary purchase journey.

Current automated E2E checkpoints include:

1. successful login to Inventory — `TC-LOGIN-001`
2. representative product add-to-cart flow from Inventory — `TC-INVENTORY-005`
3. representative cart content validation — `TC-CART-002`
4. Cart → Checkout Information — `TC-CART-012`
5. Checkout Information → Checkout Overview — `TC-CHECKOUT-008`
6. representative selected product validation on Checkout Overview — `TC-CHECKOUT-010`
7. representative price summary validation — `TC-CHECKOUT-012`
8. Finish → Checkout Complete — `TC-CHECKOUT-017`
9. Back Home → Inventory — `TC-CHECKOUT-020`

`TC-CHECKOUT-019` is documented as an additional E2E completion-page smoke checkpoint but remains planned until dedicated automation is implemented.

The E2E marker therefore describes membership in the logical primary journey, not whether an individual test executes every page of the journey itself.

## Marker Assignment Principles

Markers should be assigned according to test intent rather than mechanically.

The following principles apply:

* marker dimensions are orthogonal and valid combinations are expected
* Smoke represents fast representative coverage
* Regression represents broader or deeper applicable coverage
* Smoke and Regression should not automatically be applied together
* UI is used when direct UI presentation, visibility, state, or behavior is materially validated
* Security is used for protected-route and access-control coverage
* Sorting is used for product sorting behavior
* Navigation is used for meaningful page transitions
* E2E is used for checkpoints forming the primary purchase journey
* dedicated marker categories may stand alone
* a test should not receive Regression only because it is not Smoke
* markers should remain explicit and readable in test code
* parameter-level marker assignment is acceptable when individual parametrized cases belong to different suites

## Marker-Based Suite Execution

Run the complete test suite:

```bash
pytest -v
```

Run Smoke:

```bash
pytest -m smoke -v
```

Run Regression:

```bash
pytest -m regression -v
```

Run UI:

```bash
pytest -m ui -v
```

Run Security:

```bash
pytest -m security -v
```

Run Sorting:

```bash
pytest -m sorting -v
```

Run Navigation:

```bash
pytest -m navigation -v
```

Run the primary E2E checkpoint suite:

```bash
pytest -m e2e -v
```

Markers can be combined using normal pytest marker expressions.

Run Smoke UI tests:

```bash
pytest -m "smoke and ui" -v
```

Run Regression UI tests:

```bash
pytest -m "regression and ui" -v
```

Run representative Smoke navigation tests:

```bash
pytest -m "smoke and navigation" -v
```

Run broader Regression navigation tests:

```bash
pytest -m "regression and navigation" -v
```

Marker expressions can also be scoped to one module.

Example:

```bash
pytest tests/test_checkout_page.py -m e2e -v
```

This is useful when validating one workstream without executing every matching test in the repository.

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
* explicit marker intent
* clear mapping to manual test cases where practical

Tests should focus on behavior, while page-specific UI interactions should be handled by Page Object classes.

## Page Object Model Strategy

Page Object Model is used to separate test logic from page interaction logic.

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

The `BasePage` object is responsible for:

* storing the Playwright `Page` instance
* storing page URL metadata where applicable
* opening page URLs through a shared `open()` method

The `AppPage` object is responsible for shared authenticated-page behavior, including:

* cart access
* cart badge access
* application menu access
* logout
* reset app state
* All Items navigation
* About navigation
* shared authenticated product-item helpers where reused

The `LoginPage` object is responsible for login form interaction and login-specific UI state.

The `InventoryPage` object is responsible for inventory content, sorting, Inventory-side cart actions, and Inventory-owned navigation.

The `ProductDetailsPage` object is responsible for product details content, Product Details-side cart actions, return navigation, and authenticated shared navigation inherited through the application page layer.

The `CartPage` object is responsible for cart contents, cart item interaction, product removal, Continue Shopping, Product Details navigation, and checkout entry.

The checkout Page Objects are split by checkout stage:

* `CheckoutInformationPage`
* `CheckoutOverviewPage`
* `CheckoutCompletePage`

They own checkout form interaction, checkout summary behavior, checkout completion behavior, and checkout-stage navigation.

Page Objects should be introduced or expanded when they reduce duplication and improve readability.

## Reusable Assertion Strategy

Reusable assertions are used when the same product-related or checkout-related validation appears across multiple page areas.

Current reusable assertion helper location:

```text
framework/assertions/product_assertions.py
```

Current reusable product and checkout assertions support:

* inventory product card validation
* product details validation
* cart item validation
* Checkout Overview item validation
* Checkout Overview price summary validation
* inventory product state validation after checkout-related navigation
* price string conversion for numeric sorting and checkout summary assertions

Reusable assertion helpers should remain focused on shared validation logic.

They should not contain:

* navigation logic
* test setup logic
* fixture responsibilities
* Page Object responsibilities

## Fixture Strategy

Fixtures are used to prepare reusable and isolated test setup.

Current fixtures include:

```text
opened_login_page
standard_user
logged_in_inventory_page
inventory_page_with_one_product_in_cart
cart_page_with_one_product
checkout_step_one_page_with_one_product
checkout_step_two_page_with_one_product
checkout_last_step_page_with_one_product
```

The fixtures progressively prepare common application states while allowing each test to remain independently executable.

Examples:

* `opened_login_page` prepares the login page
* `logged_in_inventory_page` authenticates the standard user
* `inventory_page_with_one_product_in_cart` prepares Inventory with one deterministic product in the cart
* `cart_page_with_one_product` prepares the Cart with one product
* `checkout_step_one_page_with_one_product` prepares Checkout Information
* `checkout_step_two_page_with_one_product` prepares Checkout Overview
* `checkout_last_step_page_with_one_product` prepares Checkout Complete

This fixture structure is especially important for the E2E checkpoint strategy because E2E tests must not rely on state created by another test.

Fixtures should be added when setup logic becomes meaningfully repeated.

Avoid unnecessary fixture growth when a scenario is clearer with direct setup.

## Test Data Strategy

Test data should be separated from test logic when it improves readability, maintainability, or parametrization.

Current test data location:

```text
test_data/login_test_data.py
test_data/product_test_data.py
test_data/checkout_test_data.py
```

Current login test data includes:

* valid user cases
* invalid credential cases
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
* checkout required-field error messages
* checkout page title expectations
* Checkout Overview summary label expectations
* checkout completion header and message expectations

Inventory, Product Details, Cart, and Checkout tests reuse centralized user and product data.

A separate cart test data module is not needed at the current stage because Cart tests reuse existing product and user data without introducing unique Cart-only datasets.

Test data should support:

* clear test intent
* reduced hardcoding
* parametrized execution
* traceability to manual test case IDs

## Parametrization Strategy

Parametrization is used for repeated scenarios with the same test flow and different input data.

Current parametrized areas include:

* valid login cases
* invalid credential cases
* empty credential cases
* locked out user cases
* protected route access
* inventory product validation
* Inventory → Product Details navigation
* Product Details validation across all products
* add-to-cart and remove-from-cart coverage across product data
* cart item validation across product data
* Checkout Overview item validation
* Checkout Overview → Product Details navigation
* selected single-case tests where test case ID visibility in `pytest -v` is useful

Parametrized test IDs should use manual test case IDs where practical.

Examples:

```text
TC-LOGIN-002
TC-INVENTORY-013-0
TC-PRODUCT-DETAILS-002-0
TC-CART-011-0
TC-CHECKOUT-011-0
TC-CHECKOUT-016-0
```

The exact suffix depends on centralized product IDs used by the test data.

Meaningful parametrized IDs improve traceability between:

* manual test cases
* automated tests
* terminal output
* CI logs
* reports

Individual `pytest.param()` cases may receive different markers when one representative dataset belongs to Smoke and remaining datasets belong to Regression.

## Assertion Strategy

Assertions should be stable, meaningful, and focused on user-observable behavior where possible.

Current assertion patterns include:

* page URL matches expected destination
* element is visible
* element is hidden
* error message matches expected text
* password input uses the expected field type
* protected routes redirect unauthenticated users to Login
* inventory product content matches centralized product data
* product details content matches centralized product data
* sorted product names match expected order
* converted product prices match expected order
* cart badge state matches expected cart state
* cart item content matches selected product data
* Add to cart and Remove button states match cart state
* cart state persists where explicitly expected
* checkout field validation matches expected errors
* Checkout Overview product content matches expected data
* Checkout Overview price calculations match selected products
* checkout completion content matches expected values

Use Playwright assertions for browser and UI state when possible because they include built-in waiting behavior.

Use plain Python assertions when comparing extracted or calculated values such as:

* product names
* product prices
* sorted lists
* calculated checkout totals

Use reusable assertion helpers when the same meaningful validation is shared across multiple tests or page areas.

## Automation Priority

Automation should focus on:

* repeatable scenarios
* critical user flows
* regression-prone functionality
* stable application behavior
* high-value validation
* scenarios that benefit from repeated local or CI execution
* scenarios with clear expected results and stable selectors

Not every possible scenario needs dedicated automation.

Some scenarios may remain manual, exploratory, or planned when automation would currently add limited value or when the scenario belongs to later approved scope.

## Scope Boundaries

The project uses explicit scope boundaries to keep workstreams focused and maintainable.

Current page-level automation boundaries include:

* Login behavior belongs to Login coverage.
* Authentication-based protected-route validation belongs to Login coverage.
* Inventory behavior belongs to Inventory coverage.
* Product Details behavior belongs to Product Details coverage.
* Cart behavior belongs to Cart coverage.
* Cart → Checkout Information entry belongs to Cart coverage.
* Checkout Information, Checkout Overview, and Checkout Complete behavior belong to Checkout coverage.

Current excluded areas include:

* browser restart persistence
* storage clearing behavior
* cross-user cart persistence
* multi-user cart behavior
* unapproved edge-case expansion

Cart coverage should not own detailed Checkout Information, Checkout Overview, or Checkout Complete validation.

## Reporting And Debugging

Test execution generates:

* pytest console output
* HTML reports through pytest-html
* screenshots on failure
* CI artifacts uploaded by GitHub Actions

Generated reports and screenshots should not be committed to Git.

They are runtime outputs used for:

* local debugging
* failure analysis
* CI review
* execution evidence

## Local Validation Strategy

Recommended full local validation:

```bash
ruff check .
black --check .
isort . --check-only
pytest -v
```

For normal implementation work, run the relevant test module before the full suite where useful.

### Login Changes

```bash
pytest -v tests/test_login_page.py
pytest -m security -v
pytest -m "smoke and ui" -v
pytest -m "regression and ui" -v
```

### Inventory Changes

```bash
pytest -v tests/test_inventory_page.py
pytest -m sorting -v
pytest tests/test_inventory_page.py -m navigation -v
```

### Product Details Changes

```bash
pytest -v tests/test_product_details_page.py
pytest tests/test_product_details_page.py -m navigation -v
pytest tests/test_product_details_page.py -m regression -v
```

### Cart Changes

```bash
pytest -v tests/test_cart_page.py
pytest tests/test_cart_page.py -m navigation -v
pytest tests/test_cart_page.py -m regression -v
```

### Checkout Changes

```bash
pytest -v tests/test_checkout_page.py
pytest tests/test_checkout_page.py -m navigation -v
pytest tests/test_checkout_page.py -m regression -v
```

### Primary Purchase Journey Changes

When changes affect checkpoints in the main purchase journey, run:

```bash
pytest -m e2e -v
```

This validates the complete logical checkpoint suite across the covered page areas.

For checkpoint, stabilization, or portfolio-promotion tasks, run relevant scoped modules and full validation when possible:

```bash
pytest -v tests/test_login_page.py
pytest -v tests/test_inventory_page.py
pytest -v tests/test_product_details_page.py
pytest -v tests/test_cart_page.py
pytest -v tests/test_checkout_page.py
pytest -v
```

The full test suite should pass before a workstream is considered ready for merge unless a scoped validation exception is explicitly accepted.

## CI Validation Strategy

GitHub Actions currently validates the project automatically according to the configured workflow triggers.

The current CI pipeline validates:

* dependency installation
* Playwright browser installation
* linting
* formatting
* import sorting
* full pytest execution
* HTML report generation
* artifact upload

The current CI test execution is not split into separate marker-based jobs.

Marker-based commands documented in this strategy are primarily intended for selective local execution and validation.

Future CI marker separation should only be documented as implemented after the corresponding workflow changes are introduced and validated.

Failing tests or quality checks should block merging.

## Portfolio Promotion Validation

Before promoting `develop` to `main`, validate that:

* the full test suite passes locally when possible
* CI on the promotion Pull Request passes
* implemented test coverage is accurately described
* planned coverage is not described as already automated
* test case documentation remains aligned with automated test modules
* marker definitions remain aligned with test usage
* generated reports, screenshots, cache files, and virtual environment files are not tracked
* the promoted state is suitable as a stable portfolio snapshot

After promotion, `main` should represent the polished portfolio version of the project.

Future implementation work should continue from `develop`.

## Future Improvements

Planned improvements include:

* broader framework maturity work
* API testing layer
* multi-browser execution
* marker-based CI job separation where justified
* smoke and regression CI job separation where justified
* Allure reporting integration
* improved diagnostics and logs
* environment-based configuration

Future capabilities should not be described as implemented until their corresponding project tasks are completed and validated.
