# Framework And Project Structure

This document describes the repository structure and the responsibility of each major directory and configuration file.

The framework is structured to support maintainable Playwright UI automation, Page Object Model components, shared framework utilities, centralized test data, reusable pytest fixtures, marker-based test organization, sequential and pytest-xdist parallel execution, pytest-html and Allure reporting, failure evidence, documentation, staged CI execution, and future framework expansion.

The `main` branch represents the stable portfolio version of the project, while `develop` and active workstream branches may contain newer validated changes before promotion.

## Current Project Structure

```text
playwright-python-qa-automation-framework/
│
├── .github/
│   └── workflows/              # GitHub Actions CI workflows
│
├── config/                     # Framework and environment configuration
├── docs/                       # Project documentation
├── framework/                  # Shared framework utilities
│   └── assertions/             # Reusable assertion helpers
├── pages/                      # Page Object Model components
├── reports/                    # Generated runtime reports and failure evidence
├── resources/                  # Static resources and supporting files
├── test_cases/                 # Manual test cases and test design documentation
├── test_data/                  # Centralized test datasets
├── tests/                      # Automated test suites
│
├── conftest.py                 # Shared pytest fixtures and failure hook
├── pytest.ini                  # Centralized pytest configuration and markers
├── pyproject.toml              # Ruff, Black, and isort configuration
├── requirements.txt            # Project dependency declaration
├── requirements-lock.txt       # Locked dependency versions
├── .gitignore                  # Git ignore rules
├── .pre-commit-config.yaml     # Local automated quality hooks
├── LICENSE                     # Project license
└── README.md                   # Project overview and documentation entry point
```

## Directory Responsibilities

### `.github/workflows/`

Contains GitHub Actions workflow definitions.

Current responsibilities:

* repository checkout
* Python 3.12 setup
* dependency installation
* separate code-quality validation
* Ruff validation
* Black validation
* isort validation
* dedicated parallel Smoke browser-test execution
* dedicated parallel Regression browser-test execution
* parallel complete unfiltered full-suite execution
* pytest-xdist worker-level execution inside browser-test jobs
* Playwright Chromium installation for browser-test jobs
* pytest-html generation
* full-suite Allure result collection
* full-suite Allure HTML report generation
* Java setup required by Allure CLI
* Allure CLI setup for the full-suite job
* job-specific artifact upload
* dedicated full-suite Allure artifact upload
* validation for `develop`
* validation for `main`
* Pull Request validation
* manual workflow execution

The job structure introduced in Phase 4B remains:

```text
quality
├── smoke
├── regression
└── full-suite
```

The `quality` job executes first.

Smoke, Regression, and full-suite depend on successful quality validation and do not depend on each other.

GitHub Actions may schedule those three browser-test jobs concurrently after `quality`.

Phase 4C adds pytest-xdist worker-level execution inside those browser jobs:

```text
quality
├── smoke
│   └── pytest-xdist workers
├── regression
│   └── pytest-xdist workers
└── full-suite
    └── pytest-xdist workers
```

Phase 4D adds reporting on top of the existing execution model:

```text
quality
├── smoke
│   └── pytest-xdist
│       └── pytest-html
├── regression
│   └── pytest-xdist
│       └── pytest-html
└── full-suite
    └── pytest-xdist
        ├── pytest-html
        ├── Allure results
        └── Allure HTML report
```

GitHub Actions job-level concurrency and pytest-xdist worker-level parallelism are separate mechanisms.

Reporting is another separate concern layered on top of test execution.

Dedicated CI jobs currently exist for:

* Smoke
* Regression

Dedicated CI jobs do not currently exist for:

* UI
* Security
* Sorting
* Navigation
* E2E

Tests carrying those markers remain part of the complete unfiltered full-suite CI execution.

Smoke and Regression remain pytest-html-focused.

The complete full-suite job is the primary CI source for the advanced Allure report.

Detailed CI behavior is documented in:

```text
docs/ci-cd-pipeline.md
```

### `config/`

Reserved for framework and environment configuration.

Potential future responsibilities include:

* environment variable handling
* base URL configuration
* browser settings
* execution configuration
* environment profiles

This directory remains intentionally minimal until approved framework maturity scope requires expansion.

Runtime environment configuration is not part of the current implemented Phase 4D scope.

Neither pytest-xdist nor Allure reporting introduces a new runtime configuration layer.

### `docs/`

Contains technical project documentation.

Current documentation includes areas such as:

* architecture
* framework and project structure
* testing strategy
* pytest marker strategy
* sequential and parallel execution strategy
* reporting strategy
* workflow
* Git branching strategy
* CI/CD
* quality tooling
* technology stack
* feature overview
* roadmap

Documentation should:

* reflect current implemented behavior
* match actual pytest marker configuration
* reflect supported sequential and parallel execution
* document pytest-html and Allure responsibilities accurately
* document failure screenshot behavior accurately
* distinguish generated runtime outputs from repository content
* distinguish implemented functionality from planned functionality
* distinguish dedicated CI marker jobs from selectively executable local suites
* distinguish GitHub Actions job concurrency from pytest-xdist worker parallelism
* avoid documenting future CI or reporting capabilities as already implemented
* avoid describing implemented pytest-xdist or Allure support as future functionality
* remain synchronized with relevant framework changes

### `framework/`

Contains shared framework-level utilities that are not owned by a specific Page Object.

Current implementation:

```text
framework/assertions/product_assertions.py
```

Current responsibilities include:

* reusable product-content assertions
* Inventory product card validation
* Product Details validation
* Cart item validation
* Checkout Overview product validation
* Checkout Overview price summary validation
* Inventory product-state validation after navigation
* product price conversion for numeric comparisons

This directory should be expanded only when repeated framework logic appears across multiple test modules or page areas.

Reusable framework helpers should not own:

* browser navigation
* Page Object interactions
* test setup
* fixture responsibilities
* reporting configuration
* failure screenshot capture

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

Current Page Object responsibilities include:

* page-specific locators
* reusable interactions
* exposing browser state needed by tests
* lightweight navigation between Page Objects
* keeping selectors out of tests where practical
* shared authenticated-page behavior through `AppPage`

Current Page Object classes include:

* `BasePage`
* `AppPage`
* `LoginPage`
* `InventoryPage`
* `ProductDetailsPage`
* `CartPage`
* `CheckoutInformationPage`
* `CheckoutOverviewPage`
* `CheckoutCompletePage`

The Page Object layer should remain focused on interactions and locators.

Assertions belong in tests or shared assertion helpers.

Reporting and screenshot responsibilities do not belong in Page Objects.

Parallel execution and Allure reporting do not change Page Object responsibility boundaries.

### `BasePage`

`BasePage` provides the minimal shared Page Object foundation.

Current responsibilities:

* storing the Playwright `Page`
* shared URL metadata through `URL`
* shared page opening behavior

`BasePage` should remain intentionally small.

It should not become a generic container for unrelated framework, reporting, or execution helpers.

### `AppPage`

`AppPage` owns shared authenticated-page behavior.

Current responsibilities include:

* Cart link access
* Cart navigation
* cart badge access
* cart badge count reading
* application menu interactions
* logout
* reset app state
* All Items navigation
* About link access
* shared product-like item locator support

Authenticated Page Objects such as Inventory, Product Details, Cart, and Checkout inherit this shared behavior.

### `LoginPage`

`LoginPage` supports:

* opening Login
* username input
* password input
* Login button interaction
* credential submission
* authentication error access
* authentication error closing
* Login UI element access
* input error icon access

`LoginPage` does not inherit authenticated behavior from `AppPage`.

### `InventoryPage`

`InventoryPage` supports:

* Inventory visibility
* product list access
* product card access
* locating products by name
* reading product names
* reading product prices
* sorting
* Product Details navigation through names
* Product Details navigation through images
* Add to cart
* Remove

`InventoryPage` inherits from `AppPage`.

### `ProductDetailsPage`

`ProductDetailsPage` supports:

* direct Product Details opening by product ID
* product content access
* Add to cart
* Remove
* Back to products
* Inventory return navigation

`ProductDetailsPage` inherits from `AppPage`.

### `CartPage`

`CartPage` supports:

* direct Cart opening
* Cart contents access
* Cart item access
* locating Cart items by product name
* item name access
* description access
* price access
* quantity access
* Remove
* Product Details navigation from Cart item name
* Continue Shopping
* return to Inventory
* Checkout access
* Checkout Information navigation

`CartPage` inherits from `AppPage`.

Cart coverage owns the transition:

```text
Cart
  ↓
Checkout Information
```

Detailed checkout behavior remains owned by Checkout tests.

### `CheckoutInformationPage`

`CheckoutInformationPage` supports:

* direct page opening where required
* customer information fields
* checkout title access
* Continue
* Cancel
* customer information submission
* navigation to Checkout Overview
* cancellation to Cart
* validation error access
* input error icon access
* closing validation errors

`CheckoutInformationPage` inherits from `AppPage`.

### `CheckoutOverviewPage`

`CheckoutOverviewPage` supports:

* summary container access
* product item access
* locating products by name
* payment information access
* shipping information access
* subtotal access
* tax access
* total access
* Cancel
* Finish
* cancellation to Inventory
* Product Details navigation
* transition to Checkout Complete

`CheckoutOverviewPage` inherits from `AppPage`.

### `CheckoutCompletePage`

`CheckoutCompletePage` supports:

* completion container access
* completion image access
* confirmation header access
* confirmation message access
* Back Home
* return navigation to Inventory

`CheckoutCompletePage` inherits from `AppPage`.

### `reports/`

Stores generated runtime outputs.

Current runtime outputs include:

* pytest-html reports
* failure screenshots
* Allure result data
* generated Allure HTML reports
* debugging outputs
* CI artifact source files

Generated files should not be committed to Git.

They are intended for:

* local debugging
* failure analysis
* execution evidence
* CI artifact publishing
* advanced execution review through Allure

Current pytest-html files include:

```text
reports/smoke-report.html
reports/regression-report.html
reports/report.html
```

Current Allure result location:

```text
reports/allure-results/
```

Current generated Allure HTML location:

```text
reports/allure-report/
```

Failure screenshots are stored under:

```text
reports/screenshots/
```

The reporting model is complementary:

```text
pytest-html
    → lightweight HTML execution reports

Allure results
    → structured advanced reporting data

Allure HTML
    → generated advanced report

failure screenshots
    → browser failure evidence

GitHub Actions artifacts
    → temporary CI distribution of runtime outputs
```

The report paths and screenshot mechanism are compatible with both sequential and pytest-xdist execution.

No sequential-only reporting exception is required for the current suite.

Detailed artifact names and retention behavior are documented in:

```text
docs/ci-cd-pipeline.md
```

### Generated Runtime Output Policy

Generated report output is not repository source content.

Relevant ignore rules include:

```text
reports/*
!reports/.gitkeep

allure-results/
allure-report/
```

The implemented Allure output locations are currently nested inside `reports/`, so they are covered by:

```text
reports/*
```

The additional root-level Allure ignore entries protect against accidental generated output if different Allure paths are used manually.

The repository should contain reporting configuration and documentation, but not generated execution output.

### `resources/`

Reserved for static resources and supporting files.

Potential future usage includes:

* sample files
* upload fixtures
* static test resources
* supporting external files

This directory remains intentionally minimal.

### `test_cases/`

Contains manual test cases and test design documentation.

Current implementation:

```text
test_cases/login-page.md
test_cases/inventory-page.md
test_cases/product-details-page.md
test_cases/cart-page.md
test_cases/checkout-page.md
```

Current responsibilities:

* manual test design
* scenario documentation
* automation candidate status
* automation status
* mapping test cases to automated modules
* documenting test scope boundaries
* documenting planned scenarios
* maintaining one test case file per covered page area

Current test case identifiers include:

* `TC-LOGIN-XXX`
* `TC-INVENTORY-XXX`
* `TC-PRODUCT-DETAILS-XXX`
* `TC-CART-XXX`
* `TC-CHECKOUT-XXX`

These identifiers are also used in pytest parametrization where practical.

Individual test case files remain the source of truth for automation status.

Phase 4D reporting does not introduce new functional test cases or require test case automation metadata changes.

### `test_data/`

Contains centralized test data.

Current implementation:

```text
test_data/login_test_data.py
test_data/product_test_data.py
test_data/checkout_test_data.py
```

Current Login data includes:

* valid credentials
* invalid credential cases
* empty credential cases
* locked out user case
* expected authentication validation messages
* protected route URL suffixes

Current product data includes:

* product IDs
* product names
* descriptions
* prices
* image paths

Current checkout data includes:

* valid customer information
* required-field validation messages
* checkout title expectations
* Checkout Overview summary labels
* Checkout Complete header expectations
* Checkout Complete message expectations

Inventory, Product Details, Cart, and Checkout tests reuse centralized product data.

A separate Cart test data module is not currently required.

Checkout has dedicated data because it introduces unique form, validation, summary, and completion values.

Centralized datasets are test inputs and do not represent shared browser state between tests or pytest-xdist workers.

### `tests/`

Contains automated test suites.

Current implementation:

```text
tests/test_login_page.py
tests/test_inventory_page.py
tests/test_product_details_page.py
tests/test_cart_page.py
tests/test_checkout_page.py
```

Current test module responsibilities:

* `test_login_page.py` — authentication validation, Login UI behavior, error-state behavior, keyboard submission, input error icons, protected-route access, and Login-related E2E checkpoint coverage
* `test_inventory_page.py` — Inventory visibility, product list and content validation, sorting, Cart actions, cart badge behavior, Product Details navigation, and Inventory-related E2E checkpoints
* `test_product_details_page.py` — Product Details content, Inventory return navigation, Add/Remove behavior, cart badge behavior, Cart navigation, and all-products coverage
* `test_cart_page.py` — empty Cart state, Cart item visibility and content, Remove behavior, cart badge behavior, Continue Shopping, Cart persistence, Product Details navigation, Checkout entry, and Cart-related E2E checkpoints
* `test_checkout_page.py` — Checkout Information validation, Checkout Overview validation, price summaries, navigation, Checkout Complete validation, and Checkout-related E2E checkpoints

The current automated modules focus on Playwright UI automation.

All current test modules must remain independently executable and must not rely on execution order or browser state produced by another test.

This requirement supports:

* sequential execution
* pytest-xdist worker-level parallel execution
* marker-based execution
* full-suite reporting
* reliable CI execution

Reporting integrations operate around test execution and do not require separate reporting-specific test modules.

Future modules may include:

* API tests
* cross-browser-specific execution only if future architecture requires dedicated ownership

API tests are not currently implemented.

## Root Configuration Files

### `conftest.py`

Contains shared pytest hooks and fixtures.

Current fixture usage includes:

* `opened_login_page`
* `standard_user`
* `logged_in_inventory_page`
* `inventory_page_with_one_product_in_cart`
* `cart_page_with_one_product`
* `checkout_step_one_page_with_one_product`
* `checkout_step_two_page_with_one_product`
* `checkout_last_step_page_with_one_product`

Current hook responsibilities include:

* detecting browser-test failures during the Pytest call phase
* capturing the existing failure screenshot
* storing the screenshot under `reports/screenshots/`
* attaching the same successfully captured PNG to Allure

Fixtures prepare deterministic state and support independent execution.

Tests should not depend on state produced by previously executed test cases.

The existing Playwright fixture model and fixture chains provide isolated setup for individual tests.

Cart, Checkout, E2E, parametrized product scenarios, and logout/re-login behavior were validated under pytest-xdist parallel execution.

### Failure Screenshot Behavior

The failure screenshot path is:

```text
reports/screenshots/
```

Screenshot filenames contain:

* the test name
* a UTC timestamp

The screenshot is captured once.

After successful capture, the same PNG file is attached to Allure as:

```text
Failure screenshot
```

when Allure result collection is active.

This avoids a second screenshot implementation.

If screenshot capture fails, there is no Allure screenshot attachment because no image file exists.

If Allure attachment fails after screenshot capture, the original screenshot remains available under `reports/screenshots/`.

This keeps the base failure evidence independent of the advanced reporting layer.

### `pytest.ini`

Contains centralized Pytest configuration.

Current responsibilities include:

* test discovery configuration
* default pytest options
* strict marker validation
* marker registration

Current executable markers are:

* `smoke`
* `regression`
* `ui`
* `security`
* `sorting`
* `navigation`
* `e2e`

Marker intent:

* `smoke` — fast representative validation of critical functionality
* `regression` — broader validation across expanded or full applicable cases
* `ui` — visibility, presentation, state, and direct UI behavior
* `security` — access control and protected-route validation
* `sorting` — product sorting behavior
* `navigation` — meaningful page transitions excluding the authentication Login → Inventory transition
* `e2e` — independent checkpoints forming the primary purchase journey

The project uses:

```text
--strict-markers
```

Markers used by automated tests must therefore be registered in `pytest.ini`.

pytest-xdist execution is enabled through command-line options such as:

```text
-n auto
```

Parallel execution is not forced globally through `pytest.ini`.

This preserves supported sequential execution.

Allure result collection is also enabled per execution through command-line arguments rather than forced globally.

API testing remains future scope and does not currently have an executable pytest marker.

Detailed marker and execution semantics are maintained in:

```text
docs/testing-strategy.md
```

### `pyproject.toml`

Contains configuration for:

* Ruff
* Black
* isort

### `.pre-commit-config.yaml`

Contains local pre-commit quality hooks.

Current hooks include:

* Ruff
* Black
* isort

### `requirements.txt`

Contains the readable project dependency declaration.

Current reporting and execution dependencies include:

* pytest-xdist
* pytest-html
* allure-pytest

The standalone Allure CLI is not a Python project dependency.

It is an external report-generation prerequisite.

### `requirements-lock.txt`

Contains locked dependency versions for reproducible:

* local setup
* CI installation

The locked dependency set includes:

```text
pytest-xdist==3.8.0
allure-pytest==2.16.0
allure-python-commons==2.16.0
```

pytest-xdist is an active Phase 4C execution capability.

Allure Pytest integration is an active Phase 4D reporting capability.

The standalone Allure CLI remains separate from the Python dependency lock.

### `.gitignore`

Defines files and directories that should not be tracked by Git.

Relevant generated-report rules include:

```text
reports/*
!reports/.gitkeep

allure-results/
allure-report/
test-results/
playwright-report/
```

The currently implemented report paths under `reports/` are therefore treated as generated runtime content.

## Current Page-Level Test Suite Structure

The project follows one manual test case file and one automated test module per covered page area.

### Login

```text
test_cases/login-page.md
        ↓
test_data/login_test_data.py
        ↓
pages/login_page.py
        ↓
tests/test_login_page.py
        ↓
explicit pytest markers and parametrization
        ↓
selective local execution
        ↓
sequential / parallel suite execution
        ↓
reporting
        ↓
CI execution
```

Depending on marker assignment, Login tests may participate in:

* dedicated parallel Smoke CI execution
* dedicated parallel Regression CI execution
* parallel complete full-suite CI execution
* complete full-suite Allure reporting

### Inventory

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
explicit pytest markers and parametrization
        ↓
selective local execution
        ↓
sequential / parallel suite execution
        ↓
reporting
        ↓
CI execution
```

Depending on marker assignment, Inventory tests may participate in:

* dedicated parallel Smoke CI execution
* dedicated parallel Regression CI execution
* parallel complete full-suite CI execution
* complete full-suite Allure reporting

### Product Details

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
explicit pytest markers and parametrization
        ↓
selective local execution
        ↓
sequential / parallel suite execution
        ↓
reporting
        ↓
CI execution
```

Depending on marker assignment, Product Details tests may participate in:

* dedicated parallel Smoke CI execution
* dedicated parallel Regression CI execution
* parallel complete full-suite CI execution
* complete full-suite Allure reporting

### Cart

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
explicit pytest markers and parametrization
        ↓
selective local execution
        ↓
sequential / parallel suite execution
        ↓
reporting
        ↓
CI execution
```

Depending on marker assignment, Cart tests may participate in:

* dedicated parallel Smoke CI execution
* dedicated parallel Regression CI execution
* parallel complete full-suite CI execution
* complete full-suite Allure reporting

### Checkout

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
explicit pytest markers and parametrization
        ↓
selective local execution
        ↓
sequential / parallel suite execution
        ↓
reporting
        ↓
CI execution
```

Depending on marker assignment, Checkout tests may participate in:

* dedicated parallel Smoke CI execution
* dedicated parallel Regression CI execution
* parallel complete full-suite CI execution
* complete full-suite Allure reporting

## Login Test Suite Structure

Current Login automation includes:

* successful login
* invalid username validation
* invalid password validation
* combined invalid username and password validation
* empty username validation
* empty password validation
* empty credentials validation
* locked out user validation
* authentication error close behavior
* Login page element visibility
* password masking
* Enter submission
* protected Inventory access
* protected Cart access
* protected Product Details access
* protected Checkout Information access
* protected Checkout Overview access
* protected Checkout Complete access
* input error icon visibility

Credential validation and selected protected-route scenarios use pytest parametrization.

## Inventory Test Suite Structure

Current Inventory automation includes:

* Inventory visibility
* product list validation
* product card validation
* Cart navigation
* representative Add to cart
* all-products Add to cart
* Add to cart → Remove state
* representative Remove
* all-products Remove
* Remove → Add to cart state
* cart badge visibility
* cart badge count updates
* cart badge disappearance
* sorting by name A to Z
* sorting by name Z to A
* sorting by price low to high
* sorting by price high to low
* Product Details navigation through all product names
* Product Details navigation through all product images
* representative Product Details navigation checkpoints

## Product Details Test Suite Structure

Current Product Details automation includes:

* representative Product Details visibility
* all-products Product Details validation
* return to Inventory
* Add to cart → Remove state
* representative Add to cart
* all-products Add to cart
* representative Remove
* all-products Remove
* Remove → Add to cart state
* cart badge visibility
* cart badge count updates
* cart badge disappearance
* representative Cart navigation
* full Product Details → Cart navigation coverage across all products

## Cart Test Suite Structure

Current Cart automation includes:

* empty Cart state
* representative Cart item visibility
* Cart item content validation
* all-products Cart content validation
* representative Remove
* all-products Remove
* cart badge removal
* cart badge decrement
* Continue Shopping
* Continue Shopping state preservation
* Cart persistence after logout and re-login
* representative Product Details navigation
* full Cart → Product Details navigation coverage across all products
* Checkout Information navigation
* E2E Cart checkpoints

Cart owns the checkout entry transition.

Detailed Checkout Information, Checkout Overview, and Checkout Complete behavior is owned by Checkout tests.

## Checkout Test Suite Structure

Current Checkout automation includes:

* Checkout Information form validation
* lightweight Smoke validation of Checkout Information form availability
* required First Name validation
* required Last Name validation
* required Postal Code validation
* input error icons
* validation error messages
* validation error close behavior
* valid-data navigation to Checkout Overview
* Checkout Information cancellation to Cart
* representative Checkout Overview product validation
* all-products Checkout Overview validation
* single-product price summary
* multiple-product price summary
* Checkout Overview cancellation
* representative Product Details navigation
* all-products Product Details navigation from Checkout Overview
* Finish transition
* Checkout Complete validation
* lightweight Smoke validation of Checkout Complete page availability
* Back Home navigation
* Checkout E2E checkpoints

## Marker-Based Test Organization

The framework uses explicit pytest markers to organize selective suites.

Current marker set:

```text
smoke
regression
ui
security
sorting
navigation
e2e
```

Markers represent independent dimensions of test intent.

They are not mutually exclusive.

Example:

```python
'@pytest.mark.smoke'
'@pytest.mark.navigation'
'@pytest.mark.e2e'
```

A test with these markers is simultaneously:

* a representative critical check
* a Navigation test
* an E2E journey checkpoint

Current sequential local suite commands include:

```bash
pytest -m smoke -v
pytest -m regression -v
pytest -m ui -v
pytest -m security -v
pytest -m sorting -v
pytest -m navigation -v
pytest -m e2e -v
```

Approved parallel suite commands include:

```bash
pytest -m smoke -n auto -v
pytest -m regression -n auto -v
pytest -n auto -v
```

Dedicated CI jobs currently exist for:

* Smoke
* Regression

UI, Security, Sorting, Navigation, and E2E remain selectively executable locally without dedicated CI jobs.

Tests carrying these markers remain included in complete full-suite CI execution.

Marker semantics, xdist distribution, and reporting are separate concerns.

pytest-xdist determines how collected tests are distributed and does not change marker assignment.

Allure consumes the results produced by the selected execution and also does not change marker assignment.

Detailed marker and execution strategy is documented in:

```text
docs/testing-strategy.md
```

## E2E Suite Structure

The E2E suite consists of independent checkpoints that collectively form the primary Sauce Demo purchase journey.

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

* prepare their own state
* use fixtures or local setup
* are independently executable
* do not depend on execution order
* do not depend on shared state created by other tests

Run the suite sequentially with:

```bash
pytest -m e2e -v
```

E2E does not currently have a dedicated CI job.

Its tests remain part of the complete full-suite CI execution.

Because full-suite CI uses pytest-xdist, individual E2E checkpoints may execute on different workers.

Because the full suite collects Allure results, the E2E checkpoints are also represented in the full-suite Allure reporting data.

Their independent checkpoint architecture is therefore part of the current parallel-safety model.

## Reporting Structure

The framework currently uses complementary reporting mechanisms.

### pytest-html

pytest-html is the lightweight HTML report solution.

Current CI report files:

```text
reports/smoke-report.html
reports/regression-report.html
reports/report.html
```

Smoke and Regression remain focused on pytest-html.

Full-suite also keeps pytest-html after Allure integration.

### Allure Result Collection

Allure Pytest integration collects structured execution data.

Current result location:

```text
reports/allure-results/
```

Sequential example:

```bash
pytest -v \
  --alluredir=reports/allure-results \
  --clean-alluredir
```

Parallel example:

```bash
pytest -n auto -v \
  --alluredir=reports/allure-results \
  --clean-alluredir
```

### Allure HTML Generation

The standalone Allure CLI converts result data into the generated HTML report.

Current command:

```bash
allure generate reports/allure-results \
  --clean \
  -o reports/allure-report
```

Current generated location:

```text
reports/allure-report/
```

The Allure CLI is an external prerequisite for HTML generation.

The Python `allure-pytest` package and the standalone Allure CLI have different responsibilities.

### Failure Screenshots

Failure screenshots are produced by the existing Pytest hook.

Current location:

```text
reports/screenshots/
```

The same captured PNG is reused as the Allure attachment when Allure result collection is active.

This keeps one screenshot capture mechanism.

### GitHub Actions Artifacts

Generated CI outputs are published through GitHub Actions artifacts.

Smoke:

```text
smoke-pytest-html-report
smoke-test-artifacts
```

Regression:

```text
regression-pytest-html-report
regression-test-artifacts
```

Full-suite:

```text
pytest-html-report
full-suite-allure-report
test-artifacts
```

The dedicated Allure artifact publishes:

```text
reports/allure-report/
```

The existing broader full-suite runtime artifact continues to publish:

```text
reports/
```

Artifact retention remains seven days.

Allure history persistence, report hosting, and GitHub Pages reporting are not implemented.

## Local And CI Execution Structure

Local validation supports:

* page-level execution
* marker-based execution
* sequential full-suite execution
* pytest-xdist parallel execution
* pytest-html reporting where required
* Allure result collection
* Allure HTML generation
* quality checks

Standard complete sequential local validation:

```bash
ruff check .
black --check .
isort . --check-only
pytest -v
```

Approved parallel execution:

```bash
pytest -m smoke -n auto -v
pytest -m regression -n auto -v
pytest -n auto -v
```

Sequential execution remains supported and can be used for normal local work, focused debugging, and failure reproduction.

Example full-suite reporting validation:

```bash
pytest -n auto -v \
  --html=reports/report.html \
  --self-contained-html \
  --alluredir=reports/allure-results \
  --clean-alluredir
```

Then:

```bash
allure generate reports/allure-results \
  --clean \
  -o reports/allure-report
```

### Phase 4B CI Structure

The GitHub Actions pipeline uses four jobs:

```text
quality
├── smoke
├── regression
└── full-suite
```

The `quality` job performs:

* repository checkout
* Python 3.12 setup
* dependency installation
* Ruff
* Black
* isort

The quality job does not install Playwright Chromium.

It does not execute browser tests or use pytest-xdist.

A failure in the quality job prevents browser-test execution.

The following jobs depend on successful `quality` validation:

* `smoke`
* `regression`
* `full-suite`

These three jobs do not depend on each other.

### Phase 4C Parallel Execution Layer

Phase 4C preserves the Phase 4B job structure and enables worker-level parallel execution inside each browser-test job.

```text
quality
├── smoke
│   └── xdist workers
├── regression
│   └── xdist workers
└── full-suite
    └── xdist workers
```

The browser jobs may be scheduled concurrently by GitHub Actions.

Inside each job, pytest-xdist independently distributes collected tests across workers.

### Phase 4D Reporting Layer

Phase 4D preserves the same job structure and adds reporting responsibilities:

```text
quality
├── smoke
│   └── xdist workers
│       └── pytest-html
├── regression
│   └── xdist workers
│       └── pytest-html
└── full-suite
    └── xdist workers
        ├── pytest-html
        ├── Allure results
        └── Allure HTML report
```

No additional browser job is introduced.

### Smoke CI Execution

The Smoke job installs Chromium and runs the approved Smoke suite.

Core command:

```bash
pytest -m smoke -n auto -v
```

The actual CI command also generates:

```text
reports/smoke-report.html
```

Smoke does not generate a dedicated Allure report.

### Regression CI Execution

The Regression job installs Chromium and runs the approved Regression suite.

Core command:

```bash
pytest -m regression -n auto -v
```

The actual CI command also generates:

```text
reports/regression-report.html
```

Regression does not generate a dedicated Allure report.

### Full-Suite CI Execution

The full-suite job installs Chromium and executes the complete unfiltered test suite.

Current command:

```bash
pytest -n auto -v \
  --html=reports/report.html \
  --self-contained-html \
  --alluredir=reports/allure-results \
  --clean-alluredir
```

The execution produces:

```text
reports/report.html
reports/allure-results/
```

The workflow then attempts to generate:

```text
reports/allure-report/
```

from the available Allure results.

The full-suite job remains the complete automated regression gate.

### Allure CI Prerequisites

The full-suite job additionally configures:

```text
Java 17
Allure CLI
```

Java is configured through:

```text
actions/setup-java@v4
```

The Allure CLI is installed with:

```bash
npm install -g allure-commandline
```

These tools are required for Allure HTML generation and are not added to Smoke or Regression.

### CI Artifacts

Browser jobs use non-conflicting artifact names.

Smoke:

```text
smoke-pytest-html-report
smoke-test-artifacts
```

Regression:

```text
regression-pytest-html-report
regression-test-artifacts
```

Full-suite:

```text
pytest-html-report
full-suite-allure-report
test-artifacts
```

Artifact upload steps use:

```yaml
if: always()
```

so available reports and runtime outputs can still be published when an executing browser-test command fails.

The Allure generation step also uses failure-tolerant workflow execution and checks for usable Allure result data before invoking the report generator.

A failed test command still fails the relevant browser job.

Reporting does not convert a failed test execution into a successful CI result.

Current artifact retention remains seven days.

Detailed CI behavior is documented in:

```text
docs/ci-cd-pipeline.md
```

## Parallel Execution And Test Isolation

Phase 4C adds pytest-xdist as an implemented execution capability without changing the page-level project structure.

The parallel model relies on existing test independence.

Current expectations include:

* tests must not depend on execution order
* tests must not consume browser state produced by previous tests
* fixture chains prepare required application state independently
* parametrized cases must remain independently executable
* E2E checkpoints must remain independent
* tests must not depend on a specific worker
* Cart and Checkout scenarios must prepare their own required state

The current suite was validated through sequential and parallel execution.

No sequential-only test exceptions were identified.

## Parallel Execution And Reporting

Phase 4D reporting operates on top of the same execution model.

Current reporting expectations include:

* pytest-html remains compatible with xdist
* Allure result collection remains compatible with xdist
* failure screenshots remain compatible with xdist
* the same failure screenshot can be attached to Allure
* Allure result collection also works with sequential execution
* no separate sequential-only reporting implementation is maintained

Execution mode and reporting mode remain separate concepts.

## Current Phase Boundaries

The current framework combines implemented Phase 4B, Phase 4C, and Phase 4D reporting behavior.

Implemented Phase 4B capabilities include:

* separate code-quality validation
* dedicated Smoke CI execution
* dedicated Regression CI execution
* complete full-suite CI execution
* explicit quality-gate dependencies
* job-specific reports and artifacts
* independent browser-job scheduling after `quality`

Implemented Phase 4C capabilities include:

* pytest-xdist as an active dependency
* validated local worker-level parallel execution
* parallel Smoke execution
* parallel Regression execution
* parallel full-suite execution
* supported sequential execution
* validated fixture and test independence
* validated parametrized and E2E independence
* xdist integration into the existing three browser-test CI jobs
* preserved Phase 4B CI structure
* preserved pytest-html and artifact behavior
* Chromium-only browser scope

Implemented Phase 4D reporting capabilities include:

* Allure Pytest integration
* local Allure result collection
* local Allure HTML generation
* Allure CLI as an HTML-generation prerequisite
* failure screenshot attachment to Allure
* reuse of the existing screenshot mechanism
* sequential reporting compatibility
* pytest-xdist reporting compatibility
* full-suite CI Allure result collection
* full-suite CI Allure HTML generation
* dedicated `full-suite-allure-report` artifact
* preservation of pytest-html
* preservation of existing artifact behavior

GitHub Actions job-level concurrency and pytest-xdist worker-level parallelism remain separate execution mechanisms.

Current Phase 4D does not implement:

* Allure history persistence
* trend history
* report hosting
* GitHub Pages reporting
* trace/video policy
* retries
* cross-browser reporting
* runtime environment configuration

Runtime environment configuration, cross-browser execution, CI matrices, and other later framework maturity capabilities remain outside the current implemented scope.

## Architecture Goals

The project structure is designed to support:

* maintainable test organization
* one automated module per covered page area
* one manual test case file per covered page area
* clear layer responsibilities
* Page Object Model
* shared authenticated behavior through `AppPage`
* reusable assertion helpers
* centralized test data
* reusable fixtures
* deterministic execution
* test independence
* sequential execution
* pytest-xdist parallel execution
* explicit marker semantics
* selective local suite execution
* pytest-html reporting
* advanced Allure reporting
* reusable failure evidence
* dedicated Smoke CI feedback
* dedicated Regression CI feedback
* complete full-suite CI validation
* staged CI quality gating
* clear separation of job-level and worker-level concurrency
* clear separation of execution and reporting concerns
* clear separation of runtime output and repository content
* test case traceability
* stable portfolio promotion

Future UI, API, cross-browser, reporting, and execution improvements should extend this foundation without weakening current responsibility boundaries.

## Structure Evolution

The project currently contains page-level automation coverage for:

* Login
* Inventory
* Product Details
* Cart
* Checkout

Implemented structure includes:

* `BasePage`
* `AppPage`
* Login Page Object
* Inventory Page Object
* Product Details Page Object
* Cart Page Object
* Checkout Page Objects
* reusable product and checkout assertions
* centralized Login data
* centralized product data
* centralized checkout data
* reusable setup fixtures
* manual test case documentation
* parametrized automated tests
* normalized marker-based categorization
* Smoke suite execution
* Regression suite execution
* UI suite execution
* Security suite execution
* Sorting suite execution
* Navigation suite execution
* independent E2E checkpoint execution
* local quality checks
* sequential Pytest execution
* pytest-xdist worker-level parallel execution
* parallel Smoke validation
* parallel Regression validation
* parallel full-suite validation
* separate CI quality validation
* dedicated parallel Smoke CI execution
* dedicated parallel Regression CI execution
* parallel complete full-suite CI validation
* pytest-html reporting
* Allure result collection
* Allure HTML generation
* screenshot capture on failure
* failure screenshot attachment to Allure
* job-specific CI artifacts
* dedicated full-suite Allure artifact

The `main` branch represents the stable portfolio version of the framework.

The `develop` branch and active workstream branches may contain newer validated changes before promotion.

Current CI structure:

```text
quality
├── smoke
│   └── pytest-xdist workers
│       └── pytest-html
├── regression
│   └── pytest-xdist workers
│       └── pytest-html
└── full-suite
    └── pytest-xdist workers
        ├── pytest-html
        ├── Allure results
        └── Allure HTML report
```

UI, Security, Sorting, Navigation, and E2E do not currently have dedicated CI jobs.

pytest-xdist parallel execution is implemented.

Allure reporting is implemented locally and in the full-suite CI reporting path.

The Phase 4D workstream should not be treated as fully completed until its remaining approved tasks and final checkpoint are completed.

Future improvements may include:

* fixture organization improvements
* environment configuration
* logging and diagnostics
* advanced reporting analytics
* API testing structure
* cross-browser execution
* Selenium comparison
* additional application areas when approved

Allure history persistence, report hosting, GitHub Pages reporting, retries, trace/video policy, runtime environment configuration, API testing, CI matrices, and cross-browser execution remain outside the current implemented Phase 4D scope.