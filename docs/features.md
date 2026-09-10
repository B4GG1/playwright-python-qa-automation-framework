# Features

This document lists the currently implemented and planned features of the QA automation framework.

The purpose of this file is to provide a concise overview of what the framework currently supports and what remains planned for future development.

The implemented feature set reflects the current framework state on the active development branch. The `main` branch represents the stable portfolio version, while `develop` and active workstream branches may contain newer validated changes before promotion.

The current implemented scope focuses on UI automation with Playwright and Pytest.

API testing, Selenium comparison, Docker-based execution, Jenkins integration, cross-browser execution, and advanced Allure reporting remain future extensions unless explicitly described as implemented below.

## Currently Implemented

### Test Execution

* UI automation using Playwright
* Pytest-based test execution
* Chromium browser execution
* centralized pytest configuration
* strict pytest marker validation
* marker-based selective local execution
* sequential local Pytest execution
* pytest-xdist worker-level parallel execution
* parallel Smoke execution
* parallel Regression execution
* parallel full-suite execution
* dedicated Smoke CI execution
* dedicated Regression CI execution
* complete full automated test suite execution
* complete full automated test suite execution in CI
* pytest-xdist execution inside existing CI browser-test jobs

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
* supported sequential execution
* validated worker-level parallel execution

Approved parallel execution commands:

```bash
pytest -m smoke -n auto -v
pytest -m regression -n auto -v
pytest -n auto -v
```

Sequential execution remains supported:

```bash
pytest -m smoke -v
pytest -m regression -v
pytest -v
```

Detailed marker and execution semantics are documented in:

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

Centralized test data represents reusable test input and does not create shared browser state between tests or xdist workers.

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
* representative Cart navigation from Product Details
* full Product Details → Cart navigation coverage across all products

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
* full Cart → Product Details navigation coverage across all products
* Checkout Information navigation from Cart
* E2E Cart checkpoints

### Checkout Page Test Coverage

Current Checkout automation includes:

* Checkout Information form validation
* lightweight Smoke validation of Checkout Information form availability
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
* lightweight Smoke validation of Checkout Complete page availability
* Back Home navigation to Inventory
* independent Checkout-related E2E checkpoints

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

Run the suite sequentially with:

```bash
pytest -m e2e -v
```

E2E does not currently have a dedicated CI job.

Its tests still participate in complete full-suite CI execution.

Because the full-suite CI job executes through pytest-xdist, E2E checkpoints may be distributed between workers while remaining independent.

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
* compatibility with sequential and parallel execution
* order-independent test design

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
* sequential execution
* pytest-xdist worker-level execution

Tests do not rely on state produced by previous tests.

Current fixture chains, Cart and Checkout scenarios, logout/re-login persistence, parametrized scenarios, and E2E checkpoints were validated under parallel execution.

No sequential-only test exceptions were identified during Phase 4C validation.

### Code Quality

Current code quality capabilities include:

* Ruff static analysis
* Black formatting validation
* isort import validation
* pre-commit local quality hooks
* local full-suite validation
* dedicated CI quality validation
* CI quality gates

Standard sequential local validation:

```bash
ruff check .
black --check .
isort . --check-only
pytest -v
```

Parallel execution validation is additionally available through:

```bash
pytest -m smoke -n auto -v
pytest -m regression -n auto -v
pytest -n auto -v
```

### Selective Marker Validation

All current marker suites remain available for selective local execution:

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

Smoke and Regression also support the approved parallel commands:

```bash
pytest -m smoke -n auto -v
pytest -m regression -n auto -v
```

Smoke and Regression additionally have dedicated GitHub Actions CI jobs.

UI, Security, Sorting, Navigation, and E2E remain selectively executable without dedicated CI jobs.

Tests assigned to those markers still run through complete full-suite CI execution.

Parallel execution changes test distribution, not marker semantics.

### CI/CD

Current CI capabilities include:

* GitHub Actions
* automated repository checkout
* Python 3.12 setup
* dependency installation
* separate code-quality validation
* Ruff validation
* Black validation
* isort validation
* dedicated parallel Smoke browser-test execution
* dedicated parallel Regression browser-test execution
* parallel complete unfiltered full-suite execution
* pytest-xdist worker-level parallel execution
* Playwright Chromium installation in browser-test jobs
* pytest HTML report generation
* Smoke-specific report and artifact upload
* Regression-specific report and artifact upload
* full-suite report and artifact upload
* explicit artifact retention
* CI execution on pushes to `main`
* CI execution on pushes to `develop`
* CI execution for Pull Requests targeting `main`
* CI execution for Pull Requests targeting `develop`
* manual execution through `workflow_dispatch`
* minimal workflow permissions using `contents: read`

Current CI job structure:

```text
quality
├── smoke
├── regression
└── full-suite
```

The `quality` job runs first.

It validates:

```bash
ruff check .
black --check .
isort . --check-only
```

The quality job does not install Playwright Chromium and does not use pytest-xdist.

Smoke, Regression, and full-suite depend on successful quality validation and do not depend on each other.

GitHub Actions may schedule those browser jobs concurrently after `quality`.

The dedicated Smoke job executes:

```bash
pytest -m smoke -n auto -v
```

The dedicated Regression job executes:

```bash
pytest -m regression -n auto -v
```

The full-suite job executes the complete unfiltered test collection:

```bash
pytest -n auto -v
```

The full-suite job remains the complete CI regression gate.

GitHub Actions job-level concurrency and pytest-xdist worker-level parallelism are separate mechanisms.

Conceptually:

```text
quality
├── smoke
│   └── xdist workers
├── regression
│   └── xdist workers
└── full-suite
    └── xdist workers
```

The following marker suites do not currently have dedicated CI jobs:

* UI
* Security
* Sorting
* Navigation
* E2E

### Reporting And Debugging

Current reporting and debugging support includes:

* pytest console output
* pytest-html
* self-contained HTML reports in CI
* screenshots on test failure
* `reports/` runtime output directory
* job-specific GitHub Actions artifact upload
* downloadable CI execution artifacts

Current Smoke artifact names:

```text
smoke-pytest-html-report
smoke-test-artifacts
```

Current Regression artifact names:

```text
regression-pytest-html-report
regression-test-artifacts
```

Current full-suite artifact names:

```text
pytest-html-report
test-artifacts
```

Artifact upload steps use `if: always()` so available browser-test outputs can still be published when an executing test command fails.

Current artifact retention remains seven days.

The existing report, screenshot, and artifact behavior was preserved and validated after pytest-xdist integration.

No sequential-only reporting exception was identified during current Phase 4C validation.

Generated runtime outputs are not intended to be committed to Git.

### Repository And Documentation

Current repository documentation includes:

* README project entry point
* architecture documentation
* framework structure documentation
* testing strategy
* marker execution strategy
* parallel execution strategy
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
selective suite execution
      ↓
sequential / parallel execution
      ↓
CI execution
```

Depending on marker assignment, automated tests may participate in:

* dedicated parallel Smoke CI execution
* dedicated parallel Regression CI execution
* parallel complete full-suite CI execution

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

* additional suite-specific CI execution where justified
* expanded traceability
* additional parametrized scenarios where useful

The current normalized marker strategy is implemented.

Dedicated Smoke and Regression CI execution is implemented.

Pytest-xdist worker-level parallel execution is also implemented locally and in the existing CI browser-test jobs.

Future work should improve execution scalability and feedback without reintroducing obsolete marker categories.

### Reporting And Diagnostics

Possible future improvements include:

* Allure reporting
* improved screenshot organization
* structured logging
* richer failure diagnostics
* test history
* execution analytics
* JUnit XML output

Advanced Allure reporting is not currently implemented.

### CI/CD Improvements

Possible future CI improvements include:

* dependency caching
* Playwright browser caching
* additional marker-based jobs where justified
* multi-browser execution
* scheduled regression execution
* JUnit XML publishing
* improved reporting integrations

Dedicated Smoke and Regression jobs and pytest-xdist execution are already part of the current implementation.

The independent Smoke, Regression, and full-suite GitHub Actions jobs may be scheduled concurrently after `quality`.

Inside each browser job, pytest-xdist additionally distributes collected tests between workers.

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

`pytest-xdist` is an implemented execution capability.

Current approved local parallel commands are:

```bash
pytest -m smoke -n auto -v
pytest -m regression -n auto -v
pytest -n auto -v
```

The existing Smoke, Regression, and full-suite GitHub Actions browser jobs also execute through pytest-xdist.

Current CI commands use the same worker-level strategy together with existing HTML reporting.

Sequential execution remains supported:

```bash
pytest -m smoke -v
pytest -m regression -v
pytest -v
```

The current suite was validated for:

* fixture isolation
* browser-state independence
* Cart and Checkout state preparation
* logout and re-login behavior
* E2E checkpoint independence
* parametrized scenario independence
* report and failure-screenshot compatibility

No sequential-only test exceptions were identified during Phase 4C validation.

GitHub Actions job concurrency and pytest-xdist worker concurrency remain distinct execution layers.

Current parallel execution remains Chromium-only and does not introduce cross-browser parallelization or CI matrices.

### Advanced Reporting

`allure-pytest` is installed but Allure reporting is not currently part of the active reporting workflow.

Current reporting uses:

* pytest-html
* screenshots on failure
* GitHub Actions artifacts

Advanced Allure reporting belongs to future Phase 4D scope.

### Cross-Browser Execution

Current execution uses Chromium.

Potential future browsers include:

* Firefox
* WebKit

Cross-browser execution is not currently part of the implemented framework or CI strategy.

Current pytest-xdist support parallelizes the existing Chromium-based test execution and should not be interpreted as cross-browser parallel execution.

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
* pytest-xdist worker-level parallel execution
* supported sequential execution
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
* selective local marker execution
* parallel local Smoke execution
* parallel local Regression execution
* parallel local full-suite execution
* code quality tooling
* pre-commit validation
* GitHub Actions CI
* separate CI quality validation
* dedicated parallel Smoke CI execution
* dedicated parallel Regression CI execution
* parallel complete full-suite CI execution
* pytest HTML reporting
* screenshots on failure
* job-specific CI artifacts
* Git branching workflow
* technical project documentation

Current CI execution model:

```text
quality
├── smoke
│   └── pytest-xdist workers
├── regression
│   └── pytest-xdist workers
└── full-suite
    └── pytest-xdist workers
```

The `quality` job is the prerequisite and does not use browser execution or pytest-xdist.

Smoke, Regression, and full-suite remain separate GitHub Actions jobs and may execute concurrently after successful quality validation.

UI, Security, Sorting, Navigation, and E2E do not currently have dedicated CI jobs.

Phase 4C pytest-xdist parallel execution is implemented.

Advanced Allure reporting, runtime environment configuration, cross-browser execution, Docker-based execution, CI matrices, and other later framework maturity capabilities remain outside the current implemented scope.

Planned technologies and features should remain clearly separated from the implemented scope until they are approved, implemented, validated, and documented.
