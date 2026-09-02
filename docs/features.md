# Features

This document lists the currently implemented and planned features of the QA automation framework.

The purpose of this file is to provide a concise overview of what the framework currently supports and what remains planned for future development.

The implemented feature set reflects the current framework state on the active development branch. The `main` branch represents the stable portfolio version, while `develop` and active workstream branches may contain newer validated changes before promotion.

The current implemented scope focuses on UI automation with Playwright and Pytest.

API testing, Selenium comparison, Docker-based execution, Jenkins integration, cross-browser execution, parallel execution, and advanced reporting remain future extensions unless explicitly described as implemented below.

## Currently Implemented

### Test Execution

* UI automation using Playwright
* Pytest-based test execution
* Chromium browser execution
* centralized pytest configuration
* strict pytest marker validation
* marker-based selective local execution
* full automated test suite execution
* full automated test suite execution in CI

Current executable pytest markers:

* `smoke`
* `regression`
* `ui`
* `security`
* `sorting`
* `navigation`
* `e2e`

Current suite capabilities include:

* representative Smoke validation
* broader Regression validation
* direct UI behavior validation
* protected-route Security validation
* product Sorting validation
* page-transition Navigation validation
* independent E2E purchase-journey checkpoint validation

Detailed marker semantics are documented in:

```text
docs/testing-strategy.md
```

### Page Object Model

Current Page Object Model implementation includes:

* `BasePage`
* `AppPage`
* `LoginPage`
* `InventoryPage`
* `ProductDetailsPage`
* `CartPage`
* `CheckoutInformationPage`
* `CheckoutOverviewPage`
* `CheckoutCompletePage`

Current Page Object capabilities include:

* shared page initialization
* shared direct-page opening behavior
* shared authenticated-page behavior
* centralized page-specific locators
* reusable page actions
* Login interactions
* Inventory interactions
* Product Details interactions
* Cart interactions
* Checkout Information interactions
* Checkout Overview interactions
* Checkout Complete interactions
* authenticated header Cart access
* cart badge access
* application menu interactions
* logout
* reset app state
* All Items navigation
* About link access
* Add to cart behavior
* Remove behavior
* Continue Shopping
* checkout entry
* checkout cancellation
* checkout completion
* Back Home navigation
* lightweight Page Object transitions after navigation

### Reusable Assertions

Current reusable assertion support includes:

* reusable product assertion helpers
* Inventory product card content validation
* Product Details content validation
* Cart item content validation
* Checkout Overview product content validation
* Checkout Overview price summary validation
* Inventory product state validation after navigation
* product price conversion for numeric comparisons

Current shared assertion implementation:

```text
framework/assertions/product_assertions.py
```

Reusable assertion helpers remain focused on shared validation logic rather than navigation or test setup.

### Test Data Management

Current centralized test data includes:

* login test data
* product test data
* checkout test data
* standard valid user credentials
* invalid credential cases
* empty credential cases
* locked out user case
* expected authentication validation messages
* protected route URL suffixes
* product IDs
* product names
* product descriptions
* product prices
* product image paths
* valid checkout customer information
* checkout required-field validation messages
* checkout page title expectations
* Checkout Overview summary expectations
* Checkout Complete content expectations
* manual test case IDs used in parametrized output where practical

Current test data files:

```text
test_data/login_test_data.py
test_data/product_test_data.py
test_data/checkout_test_data.py
```

Inventory, Product Details, Cart, and Checkout tests reuse centralized product data instead of introducing unnecessary page-specific datasets.

### Login Page Test Coverage

Current Login automation includes:

* successful login with valid credentials
* invalid username validation
* invalid password validation
* combined invalid username and password validation
* empty username validation
* empty password validation
* empty credentials validation
* locked out user validation
* authentication error message validation
* authentication error close behavior
* login page element visibility
* password masking validation
* Login submission using Enter
* input error icon validation
* protected Inventory route access validation
* protected Cart route access validation
* protected Product Details route access validation
* protected Checkout Information route access validation
* protected Checkout Overview route access validation
* protected Checkout Complete route access validation
* lightweight Sauce Demo availability validation

### Inventory Page Test Coverage

Current Inventory automation includes:

* Inventory page visibility
* product list validation
* product card content validation
* representative Add to cart behavior
* all-products Add to cart coverage
* Add to cart → Remove button state validation
* representative Remove behavior
* all-products Remove coverage
* Remove → Add to cart button state validation
* cart badge visibility
* cart badge count updates
* cart badge disappearance
* Cart navigation
* product sorting by name A to Z
* product sorting by name Z to A
* product sorting by price low to high
* product sorting by price high to low
* Product Details navigation through product names
* Product Details navigation through product images
* representative Product Details navigation checkpoints
* broader all-products navigation coverage

### Product Details Page Test Coverage

Current Product Details automation includes:

* representative Product Details visibility
* all-products Product Details content validation
* Back to products navigation
* representative Add to cart behavior
* all-products Add to cart coverage
* Add to cart → Remove state validation
* representative Remove behavior
* all-products Remove coverage
* Remove → Add to cart state validation
* cart badge visibility
* cart badge count updates
* cart badge disappearance
* Cart navigation from Product Details

Full Product Details → Cart navigation coverage for every product remains documented as planned.

### Cart Page Test Coverage

Current Cart automation includes:

* initial empty Cart validation
* representative added-product visibility
* representative Cart item content validation
* all-products Cart content validation
* representative Remove behavior
* all-products Remove coverage
* cart badge removal after removing the last item
* cart badge decrement after removing one of multiple items
* Continue Shopping navigation
* Continue Shopping cart-state preservation
* Cart state persistence after logout and re-login
* representative Product Details navigation from Cart
* Checkout Information navigation from Cart
* E2E Cart checkpoints

Full Cart → Product Details navigation coverage for every product remains documented as planned.

### Checkout Page Test Coverage

Current Checkout automation includes:

* Checkout Information form validation
* required First Name validation
* required Last Name validation
* required Postal Code validation
* checkout input error icon validation
* checkout error message validation
* checkout error close behavior
* valid Checkout Information submission
* Checkout Information → Checkout Overview navigation
* Checkout Information cancellation back to Cart
* representative Checkout Overview product validation
* all-products Checkout Overview validation
* single-product price summary validation
* multiple-product price summary validation
* Checkout Overview cancellation back to Inventory
* representative Product Details navigation from Checkout Overview
* all-products Product Details navigation from Checkout Overview
* Finish navigation to Checkout Complete
* Checkout Complete content validation
* Back Home navigation to Inventory
* independent Checkout-related E2E checkpoints

Dedicated lightweight Smoke scenarios documented as `Planned` remain outside current automated coverage.

### Primary Purchase E2E Coverage

The framework currently provides an E2E marker suite representing independent checkpoints of the primary Sauce Demo purchase journey.

The logical journey covers:

```text
Login
  ↓
Inventory
  ↓
Product selection
  ↓
Cart
  ↓
Checkout Information
  ↓
Checkout Overview
  ↓
Checkout Complete
  ↓
Back Home
  ↓
Inventory
```

E2E tests:

* are independently executable
* prepare their own state
* use fixtures or test-local setup
* do not depend on execution order
* do not share state between test cases

Run the suite with:

```bash
pytest -m e2e -v
```

### Test Organization

Current test organization includes:

* one automated test module per covered page area
* one manual test case file per covered page area
* explicit pytest marker decorators
* centralized marker registration
* strict marker validation
* marker-based selective execution
* parametrized credential validation scenarios
* parametrized protected-route scenarios
* parametrized Inventory scenarios
* parametrized Product Details scenarios
* parametrized Cart scenarios
* parametrized Checkout scenarios where appropriate
* test case IDs in pytest parametrization where practical
* traceability between test case documentation and automation

Current automated test modules:

```text
tests/test_login_page.py
tests/test_inventory_page.py
tests/test_product_details_page.py
tests/test_cart_page.py
tests/test_checkout_page.py
```

Current manual test case files:

```text
test_cases/login-page.md
test_cases/inventory-page.md
test_cases/product-details-page.md
test_cases/cart-page.md
test_cases/checkout-page.md
```

Current marker registration:

```text
smoke
regression
ui
security
sorting
navigation
e2e
```

### Fixtures And Reusable Setup

Current shared pytest fixtures include:

* opened Login page fixture
* standard user fixture
* logged-in Inventory fixture
* Inventory fixture with one product in Cart
* Cart fixture with one product
* Checkout Information fixture with one product
* Checkout Overview fixture with one product
* Checkout Complete fixture with one product

Reusable fixture setup supports:

* authentication setup
* product selection
* Cart preparation
* Checkout preparation
* isolated test execution
* independent E2E checkpoints

### Code Quality

Current code quality capabilities include:

* Ruff static analysis
* Black formatting validation
* isort import validation
* pre-commit local quality hooks
* local full-suite validation
* CI quality gates

Standard local validation:

```bash
ruff check .
black --check .
isort . --check-only
pytest -v
```

### Selective Marker Validation

Current local marker execution includes:

```bash
pytest -m smoke -v
pytest -m regression -v
pytest -m ui -v
pytest -m security -v
pytest -m sorting -v
pytest -m navigation -v
pytest -m e2e -v
```

Common combinations include:

```bash
pytest -m "smoke and ui" -v
pytest -m "regression and ui" -v
pytest -m "smoke and navigation" -v
pytest -m "regression and navigation" -v
```

Marker suites are primarily intended for selective local validation.

### CI/CD

Current CI capabilities include:

* GitHub Actions
* automated repository checkout
* Python 3.12 setup
* dependency installation
* Playwright Chromium installation
* Ruff validation
* Black validation
* isort validation
* full Pytest execution
* pytest HTML report generation
* report artifact upload
* debugging artifact upload
* explicit artifact retention
* CI execution on pushes to `main`
* CI execution on pushes to `develop`
* CI execution for Pull Requests targeting `main`
* CI execution for Pull Requests targeting `develop`
* manual execution through `workflow_dispatch`
* minimal workflow permissions using `contents: read`

The current CI pipeline executes the complete automated test suite.

Separate marker-based CI jobs are not currently implemented.

### Reporting And Debugging

Current reporting and debugging support includes:

* pytest console output
* pytest-html
* self-contained HTML reports in CI
* screenshots on test failure
* `reports/` runtime output directory
* GitHub Actions artifact upload
* downloadable CI execution artifacts

Generated runtime outputs are not intended to be committed to Git.

### Repository And Documentation

Current repository documentation includes:

* README project entry point
* architecture documentation
* framework structure documentation
* testing strategy
* marker execution strategy
* workflow documentation
* Git branching strategy
* CI/CD documentation
* quality tooling documentation
* technology stack documentation
* roadmap documentation
* feature documentation
* manual test case documentation

Current automation documentation maintains traceability between:

```text
manual test case
      ↓
test case ID
      ↓
automated test
      ↓
pytest markers
      ↓
selective local suite execution
      ↓
full-suite CI validation
```

## Planned Features

### Framework Architecture

Possible future framework improvements include:

* environment-based configuration
* improved execution configuration
* additional reusable fixtures when justified
* additional framework utilities when repeated logic appears
* additional Page Objects when new application areas require them
* improved diagnostics
* logging utilities

### Test Coverage

Potential future automation areas include:

* broader end-to-end journey coverage beyond current checkpoints
* broader session and logout coverage where justified
* additional approved edge cases
* known-defect coverage where appropriate
* API-level testing
* hybrid UI and API scenarios
* cross-browser execution

### Test Organization

Possible future improvements include:

* marker-based CI job separation
* dedicated Smoke CI execution
* dedicated Regression CI execution
* additional suite-specific CI execution where justified
* parallel execution
* expanded traceability
* additional parametrized scenarios where useful

The current normalized marker strategy is already implemented locally.

Future work should improve CI execution and scalability rather than reintroduce obsolete marker categories.

### Reporting And Diagnostics

Possible future improvements include:

* Allure reporting
* improved screenshot organization
* structured logging
* richer failure diagnostics
* test history
* execution analytics
* JUnit XML output

### CI/CD Improvements

Possible future CI improvements include:

* dependency caching
* Playwright browser caching
* separate Smoke execution
* separate Regression execution
* selected marker-based jobs
* parallel execution
* multi-browser execution
* scheduled regression execution
* JUnit XML publishing
* improved reporting integrations

These features are not currently implemented.

### API Testing

The `requests` dependency is installed for future API automation.

Potential API scope includes:

* API smoke tests
* backend validation
* API-based test data setup
* API-based test data cleanup
* hybrid UI and API scenarios

API testing is not currently implemented and `api` is not a current executable pytest marker.

### Parallel Execution

`pytest-xdist` is installed for future execution optimization.

Parallel execution is not currently part of the default local or CI workflow.

Potential future usage includes:

* faster Regression execution
* parallel UI execution
* CI runtime optimization

### Cross-Browser Execution

Current execution uses Chromium.

Potential future browsers include:

* Firefox
* WebKit

Cross-browser execution is not currently part of the implemented framework or CI strategy.

### Future Extensions

Potential long-term extensions include:

* Selenium WebDriver comparison
* Docker-based execution
* Jenkins integration
* reusable framework packaging
* advanced execution analytics

## Current Feature Status

The implemented framework currently demonstrates:

* Playwright UI automation
* Pytest
* Page Object Model
* shared authenticated-page behavior
* reusable assertion helpers
* centralized test data
* reusable fixtures
* parametrization
* test case traceability
* normalized marker strategy
* Smoke execution
* Regression execution
* UI execution
* Security execution
* Sorting execution
* Navigation execution
* independent E2E checkpoint execution
* code quality tooling
* pre-commit validation
* GitHub Actions CI
* full-suite CI execution
* HTML reporting
* screenshots on failure
* CI artifacts
* Git branching workflow
* technical project documentation

Planned technologies and features should remain clearly separated from this implemented scope until they are approved, implemented, validated, and documented.
