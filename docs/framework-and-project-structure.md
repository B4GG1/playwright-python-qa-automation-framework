# Framework And Project Structure

This document describes the repository structure and the responsibility of each major directory and configuration file.

The framework is structured to support maintainable Playwright UI automation, Page Object Model components, shared framework utilities, centralized test data, reusable pytest fixtures, marker-based test organization, sequential and pytest-xdist parallel execution, reporting, documentation, staged CI execution, and future framework expansion.

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
├── reports/                    # Runtime reports, screenshots, and artifacts
├── resources/                  # Static resources and supporting files
├── test_cases/                 # Manual test cases and test design documentation
├── test_data/                  # Centralized test datasets
├── tests/                      # Automated test suites
│
├── conftest.py                 # Shared pytest fixtures and hooks
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
* HTML report generation
* job-specific artifact upload
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

Phase 4C adds a second execution layer inside those jobs:

```text
quality
├── smoke
│   └── pytest-xdist workers
├── regression
│   └── pytest-xdist workers
└── full-suite
    └── pytest-xdist workers
```

GitHub Actions job-level concurrency and pytest-xdist worker-level parallelism are separate mechanisms.

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

Runtime environment configuration is not part of the current implemented Phase 4C scope.

pytest-xdist parallel execution does not introduce a new runtime configuration layer.

### `docs/`

Contains technical project documentation.

Current documentation includes areas such as:

* architecture
* framework and project structure
* testing strategy
* pytest marker strategy
* sequential and parallel execution strategy
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
* distinguish implemented functionality from planned functionality
* distinguish dedicated CI marker jobs from selectively executable local suites
* distinguish GitHub Actions job concurrency from pytest-xdist worker parallelism
* avoid documenting future CI capabilities as already implemented
* avoid describing implemented pytest-xdist support as future functionality
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

Parallel execution does not change Page Object responsibility boundaries.

### `BasePage`

`BasePage` provides the minimal shared Page Object foundation.

Current responsibilities:

* storing the Playwright `Page`
* shared URL metadata through `URL`
* shared page opening behavior

`BasePage` should remain intentionally small.

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

Examples include:

* pytest HTML reports
* screenshots
* debugging outputs
* CI artifact source files

Generated files should not be committed to Git.

They are intended for:

* local debugging
* failure analysis
* execution evidence
* CI artifact publishing

Current CI browser jobs generate separate report outputs for:

* Smoke
* Regression
* full-suite

Current report files include:

```text
reports/smoke-report.html
reports/regression-report.html
reports/report.html
```

Failure screenshots are stored under:

```text
reports/screenshots/
```

The existing report paths and failure screenshot mechanism were retained after pytest-xdist integration.

Parallel validation confirmed that the current report and screenshot structure does not require a sequential-only exception for the current suite.

Detailed artifact names and retention behavior are documented in `docs/ci-cd-pipeline.md`.

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

This requirement supports both sequential execution and pytest-xdist worker-level parallel execution.

Future modules may include:

* API tests
* cross-browser-specific execution only if future architecture requires dedicated ownership

API tests are not currently implemented.

## Root Configuration Files

### `conftest.py`

Contains shared pytest hooks and fixtures.

Current usage includes:

* screenshot capture on test failure
* `opened_login_page`
* `standard_user`
* `logged_in_inventory_page`
* `inventory_page_with_one_product_in_cart`
* `cart_page_with_one_product`
* `checkout_step_one_page_with_one_product`
* `checkout_step_two_page_with_one_product`
* `checkout_last_step_page_with_one_product`

Fixtures prepare deterministic state and support independent execution.

Tests should not depend on state produced by previously executed test cases.

The existing Playwright fixture model and fixture chains provide isolated setup for individual tests.

Cart, Checkout, E2E, parametrized product scenarios, and logout/re-login behavior were validated under pytest-xdist parallel execution.

No fixture change was required during Phase 4C stabilization.

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

The project uses `--strict-markers`.

Markers used by automated tests must therefore be registered in `pytest.ini`.

pytest-xdist execution is enabled through command-line options such as `-n auto`; parallel execution is not forced globally through `pytest.ini`.

This preserves supported sequential execution.

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

`pytest-xdist` is included as an implemented execution dependency.

### `requirements-lock.txt`

Contains locked dependency versions for reproducible:

* local setup
* CI installation

The locked dependency set includes:

```text
pytest-xdist==3.8.0
```

pytest-xdist is an active Phase 4C execution capability.

Advanced Allure reporting remains outside the current implemented reporting workflow and belongs to Phase 4D.

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
CI execution
```

Depending on marker assignment, Login tests may participate in:

* dedicated parallel Smoke CI execution
* dedicated parallel Regression CI execution
* parallel complete full-suite CI execution

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
CI execution
```

Depending on marker assignment, Inventory tests may participate in:

* dedicated parallel Smoke CI execution
* dedicated parallel Regression CI execution
* parallel complete full-suite CI execution

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
CI execution
```

Depending on marker assignment, Product Details tests may participate in:

* dedicated parallel Smoke CI execution
* dedicated parallel Regression CI execution
* parallel complete full-suite CI execution

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
CI execution
```

Depending on marker assignment, Cart tests may participate in:

* dedicated parallel Smoke CI execution
* dedicated parallel Regression CI execution
* parallel complete full-suite CI execution

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
CI execution
```

Depending on marker assignment, Checkout tests may participate in:

* dedicated parallel Smoke CI execution
* dedicated parallel Regression CI execution
* parallel complete full-suite CI execution

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

Approved Phase 4C parallel suite commands include:

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

Marker semantics and parallel execution are separate concerns.

pytest-xdist determines how collected tests are distributed and does not change marker assignment.

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

Their independent checkpoint architecture is therefore part of the current parallel-safety model.

## Local And CI Execution Structure

Local validation supports:

* page-level execution
* marker-based execution
* sequential full-suite execution
* pytest-xdist parallel execution
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

### Full-Suite CI Execution

The full-suite job installs Chromium and executes the complete unfiltered test suite.

Core command:

```bash
pytest -n auto -v
```

The actual CI command also generates:

```text
reports/report.html
```

The full-suite job remains the complete automated regression gate.

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
test-artifacts
```

Artifact upload steps use `if: always()` so available reports and runtime outputs can still be published when an executing browser-test command fails.

Current artifact retention remains seven days.

The report and artifact model was preserved when pytest-xdist execution was introduced.

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

The current suite was validated through:

```bash
pytest -n auto -v
pytest -m smoke -n auto -v
pytest -m regression -n auto -v
pytest -v
```

The validation confirmed that no stabilization change was required for the current fixture and test structure.

No sequential-only exceptions were identified.

## Current Phase Boundaries

The current execution model combines completed Phase 4B and Phase 4C behavior.

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
* preserved report and artifact behavior
* Chromium-only browser scope

GitHub Actions job-level concurrency and pytest-xdist worker-level parallelism are separate execution mechanisms.

Advanced Allure reporting belongs to Phase 4D and is not currently implemented.

Current reporting uses:

* pytest-html
* screenshots on failure
* GitHub Actions artifacts

Runtime environment configuration, cross-browser execution, CI matrices, and other later framework maturity capabilities remain outside the current implemented Phase 4C scope.

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
* dedicated Smoke CI feedback
* dedicated Regression CI feedback
* complete full-suite CI validation
* staged CI quality gating
* clear separation of job-level and worker-level concurrency
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
* HTML reporting
* screenshot capture on failure
* job-specific CI artifacts

The `main` branch represents the stable portfolio version of the framework.

The `develop` branch and active workstream branches may contain newer validated changes before promotion.

Current CI structure:

```text
quality
├── smoke
│   └── pytest-xdist workers
├── regression
│   └── pytest-xdist workers
└── full-suite
    └── pytest-xdist workers
```

UI, Security, Sorting, Navigation, and E2E do not currently have dedicated CI jobs.

pytest-xdist parallel execution is implemented.

Advanced Allure reporting, runtime environment configuration, API testing, CI matrices, and cross-browser execution remain outside the current implemented scope.

Future improvements may include:

* fixture organization improvements
* environment configuration
* logging and diagnostics
* reporting improvements
* Phase 4D Allure reporting
* API testing structure
* cross-browser execution
* Selenium comparison
* additional application areas when approved
