# Architecture

This document describes the current architecture of the QA automation framework.

The project follows a lightweight, modular architecture focused on readability, maintainability, traceability, deterministic execution, test independence, reporting visibility, and incremental framework growth.

The current architecture includes Page Object Model, shared authenticated-page behavior, reusable assertions, reusable pytest fixtures, centralized test data, explicit marker-based test organization, sequential and pytest-xdist parallel execution, staged CI execution, pytest-html reporting, Allure reporting, failure screenshot evidence, GitHub Actions artifacts, and technical documentation.

## Current Architecture Scope

The current framework includes:

* Pytest-based test execution
* Playwright browser automation
* pytest-xdist worker-level parallel execution
* supported sequential Pytest execution
* Page Object Model for Login, Inventory, Product Details, Cart, and Checkout
* shared `BasePage` abstraction
* shared authenticated-page behavior through `AppPage`
* reusable product and checkout assertion helpers
* reusable pytest fixtures
* centralized login, product, and checkout test data
* explicit pytest marker categorization
* strict pytest marker validation
* marker-based selective local execution
* parallel local Smoke execution
* parallel local Regression execution
* parallel local full-suite execution
* dedicated Smoke CI execution
* dedicated Regression CI execution
* complete unfiltered full-suite CI execution
* pytest-xdist execution inside existing CI browser-test jobs
* parametrized execution with manual test case IDs where practical
* independent E2E purchase-journey checkpoints
* CI execution with GitHub Actions
* separate CI code-quality validation
* code quality tooling
* pytest-html reporting
* Allure result collection
* Allure HTML report generation
* failure screenshot capture
* failure screenshot attachment to Allure
* job-specific CI artifacts
* dedicated full-suite Allure report artifact
* manual test case documentation mapped to automation
* one automated test module per covered page area
* one manual test case file per covered page area

Current automated coverage includes:

* Sauce Demo availability validation
* successful authentication
* invalid credential validation
* empty credential validation
* locked out user validation
* Login UI behavior
* authentication error handling
* protected route access
* Inventory validation
* product list and product card validation
* Inventory → Product Details navigation
* Product Details validation
* product sorting
* Cart navigation
* empty Cart validation
* Add to cart behavior
* Remove behavior
* cart badge behavior
* Cart item visibility and content
* Continue Shopping
* Cart state persistence
* Cart → Checkout Information navigation
* Checkout Information validation
* Checkout required-field validation
* Checkout error-state validation
* Checkout Overview validation
* Checkout Overview price summary validation
* Product Details navigation from Checkout Overview
* Checkout completion
* Checkout Complete validation
* Back Home navigation
* independent E2E purchase-journey checkpoints

Cart coverage owns the user action that starts on the Cart page and opens Checkout Information.

Detailed Checkout Information, Checkout Overview, and Checkout Complete behavior remains owned by Checkout tests.

## Project Layers

The framework is organized into the following layers:

```text
test_cases/
    ↓
test_data/
    ↓
tests/
    ↓
pages/
    ↓
framework/
    ↓
Playwright / Pytest / pytest-xdist
    ↓
reporting / diagnostics
    ↓
local validation / CI
```

Reporting and diagnostics currently include:

```text
pytest-html
Allure
failure screenshots
GitHub Actions artifacts
```

The layers are intentionally lightweight.

New abstractions should be introduced only when repeated behavior or clear responsibility boundaries justify them.

## `tests/`

Contains automated test suites.

Current test modules:

```text
tests/test_login_page.py
tests/test_inventory_page.py
tests/test_product_details_page.py
tests/test_cart_page.py
tests/test_checkout_page.py
```

Current responsibilities:

* describe expected application behavior
* execute test scenarios
* use Page Objects for interactions
* use Playwright assertions for browser and UI state
* use plain Python assertions for already extracted or calculated values
* use reusable assertion helpers when validation logic is shared
* use centralized test data
* use fixtures for reusable setup
* use explicit pytest markers
* preserve traceability to manual test cases where practical
* remain independent of test execution order
* remain compatible with supported sequential and parallel execution
* produce normal Pytest result data consumed by reporting integrations

Test modules should not duplicate selectors when Page Objects already expose the required interaction or state.

Test modules should not depend on state produced by another test because xdist workers may execute tests independently and in a different order from sequential execution.

Reporting integrations should not change test ownership or introduce reporting-specific test implementations.

## `pages/`

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

The Page Object layer is responsible for:

* page-specific locators
* reusable page actions
* browser interactions
* exposing UI state needed by tests
* hiding direct selector usage from tests where practical
* returning the next Page Object when navigation changes page context
* keeping shared authenticated behavior outside individual page classes

The Page Object layer should remain focused on interaction logic.

Assertions should remain in tests or reusable assertion helpers.

Reporting concerns should not be moved into Page Objects.

Parallel execution and Allure integration do not change Page Object ownership or responsibility boundaries.

## `BasePage`

`BasePage` provides the minimal shared page foundation.

Current responsibilities:

* storing the Playwright `Page`
* shared URL metadata through `URL`
* shared `open()` behavior for directly accessible pages

`BasePage` should remain intentionally small.

It should not become a generic container for unrelated framework helpers, reporting logic, or execution configuration.

## `AppPage`

`AppPage` owns shared authenticated-page behavior.

Current responsibilities:

* Cart link access
* opening Cart from authenticated pages
* cart badge access
* cart badge count reading
* application menu access
* closing the application menu
* logout
* reset app state
* All Items navigation
* About link access
* shared product-like item locators where required

`AppPage` is the correct owner for behavior shared by authenticated areas such as:

* Inventory
* Product Details
* Cart
* Checkout

Shared authenticated behavior should not be duplicated across individual Page Objects.

## `LoginPage`

`LoginPage` centralizes Login interactions.

Current responsibilities:

* opening Login
* filling username
* filling password
* clicking Login
* submitting credentials
* reading authentication errors
* closing authentication errors
* exposing Login page UI locators
* exposing input error icon locators

`LoginPage` does not inherit from `AppPage` because Login exists outside the authenticated application area.

## `InventoryPage`

`InventoryPage` centralizes Inventory interactions.

Current responsibilities include:

* Inventory container access
* product list access
* product card access
* locating products by name
* reading product names and prices
* sorting products
* opening Product Details from product names
* opening Product Details from product images
* adding products to Cart
* removing products from Cart

`InventoryPage` inherits authenticated shared behavior through `AppPage`.

## `ProductDetailsPage`

`ProductDetailsPage` centralizes Product Details interactions.

Current responsibilities include:

* opening Product Details by product ID
* accessing Product Details content
* accessing Add to cart
* accessing Remove
* adding a product to Cart
* removing a product from Cart
* accessing Back to products
* returning to Inventory

`ProductDetailsPage` inherits authenticated shared behavior through `AppPage`.

## `CartPage`

`CartPage` centralizes Cart interactions.

Current responsibilities include:

* opening Cart directly
* accessing Cart contents
* accessing Cart items
* locating Cart items by product name
* accessing Cart item name, description, price, quantity, and Remove
* removing products
* opening Product Details from Cart item names
* Continue Shopping
* returning to Inventory
* accessing Checkout
* opening Checkout Information

`CartPage` inherits authenticated shared behavior through `AppPage`.

Cart tests own the transition from Cart to Checkout Information.

Detailed checkout validation remains outside Cart ownership.

## `CheckoutInformationPage`

`CheckoutInformationPage` centralizes Checkout Information interactions.

Current responsibilities include:

* direct page opening where required
* customer information field access
* checkout title access
* Continue access
* Cancel access
* filling customer information
* continuing to Checkout Overview
* cancelling back to Cart
* checkout validation errors
* input error icons
* closing checkout validation errors

`CheckoutInformationPage` inherits authenticated shared behavior through `AppPage`.

## `CheckoutOverviewPage`

`CheckoutOverviewPage` centralizes Checkout Overview interactions.

Current responsibilities include:

* summary container access
* product item access
* locating items by product name
* payment information access
* shipping information access
* subtotal access
* tax access
* total access
* Cancel access
* Finish access
* cancelling back to Inventory
* finishing checkout
* opening Product Details from Checkout Overview

`CheckoutOverviewPage` inherits authenticated shared behavior through `AppPage`.

## `CheckoutCompletePage`

`CheckoutCompletePage` centralizes Checkout Complete interactions.

Current responsibilities include:

* completion container access
* completion image access
* completion header access
* completion message access
* Back Home access
* returning to Inventory

`CheckoutCompletePage` inherits authenticated shared behavior through `AppPage`.

## `framework/`

Contains shared framework logic that is not owned by a specific Page Object.

Current implementation:

```text
framework/assertions/product_assertions.py
```

Current responsibilities include:

* reusable product assertions
* Inventory product card validation
* Product Details validation
* Cart item validation
* Checkout Overview product validation
* Checkout Overview price summary validation
* Inventory product-state validation after navigation
* price conversion for numeric sorting and checkout calculations

Reusable assertion helpers should remain focused on validation.

They should not own:

* navigation
* browser setup
* fixtures
* reporting
* Page Object interactions

## `test_data/`

Contains centralized test data.

Current implementation:

```text
test_data/login_test_data.py
test_data/product_test_data.py
test_data/checkout_test_data.py
```

Current Login data includes:

* valid user credentials
* invalid credential cases
* empty credential cases
* locked out user case
* expected authentication validation messages
* protected route URL suffixes

Current product data includes:

* product IDs
* product names
* product descriptions
* product prices
* product image paths

Current checkout data includes:

* valid customer information
* required-field validation messages
* checkout titles
* Checkout Overview summary labels
* Checkout Complete header and message expectations

Inventory, Product Details, Cart, and Checkout tests reuse centralized product data.

Cart does not currently require a separate Cart-specific data module.

Checkout-specific data is separated because checkout introduces unique customer data, validation messages, summary labels, and completion content.

Centralized test data is read-only test input and does not represent shared runtime browser state between tests or workers.

## `conftest.py`

Contains shared pytest hooks and fixtures.

Current responsibilities include:

* screenshot capture on browser-test failure during the Pytest call phase
* Allure attachment of successfully captured failure screenshots
* `opened_login_page`
* `standard_user`
* `logged_in_inventory_page`
* `inventory_page_with_one_product_in_cart`
* `cart_page_with_one_product`
* `checkout_step_one_page_with_one_product`
* `checkout_step_two_page_with_one_product`
* `checkout_last_step_page_with_one_product`

Fixtures prepare deterministic state without making tests depend on execution order.

The current Playwright page/context flow and project fixture chains are function-scoped for test execution.

Each test therefore prepares and owns the browser/application state required for its scenario rather than consuming browser state produced by another test.

This fixture model was validated under pytest-xdist worker-level parallel execution during Phase 4C.

### Failure Screenshot Hook

The failure hook reacts only to failed test calls.

When the test has a Playwright `page` fixture, the hook creates a failure screenshot under:

```text
reports/screenshots/
```

The filename contains:

* the test name
* a UTC timestamp

The existing screenshot mechanism remains the primary capture mechanism.

Phase 4D does not introduce a second screenshot capture path.

After successful screenshot capture, the same PNG file is attached to Allure as:

```text
Failure screenshot
```

when Allure result collection is active.

The attachment uses:

```text
image/png
```

semantics through the Allure PNG attachment type.

If screenshot capture fails, the hook stops before the Allure attachment step because no screenshot file is available.

If Allure attachment fails after successful screenshot capture, the original screenshot remains available under `reports/screenshots/`.

This preserves failure evidence independently of the advanced reporting layer.

Fixture growth should follow real repeated setup needs rather than speculative abstraction.

## Fixture-Based Test Independence

Reusable fixtures support independent test execution.

For example, Checkout checkpoints prepare the required state through fixture chains rather than relying on a previously executed test.

This supports:

* deterministic execution
* isolated tests
* marker-based selective execution
* independent E2E checkpoints
* sequential execution
* pytest-xdist parallel execution
* dedicated parallel Smoke CI execution
* dedicated parallel Regression CI execution
* parallel complete full-suite CI execution
* reporting compatibility
* CI stability

Tests should not rely on shared browser state produced by earlier test cases.

Tests must also not assume:

* a specific xdist worker
* a specific test order
* a relationship between parametrized cases
* a reporting system to prepare functional state

No sequential-only test exceptions were identified during Phase 4C validation.

Phase 4D reporting does not change these independence requirements.

## `config/`

Reserved for framework and environment configuration.

Potential future usage includes:

* base URL configuration
* environment-specific settings
* browser configuration
* execution configuration

The layer remains intentionally minimal until approved framework maturity scope requires expansion.

Runtime environment configuration is not part of the current implemented Phase 4D architecture.

Neither pytest-xdist nor Allure reporting introduces a new runtime configuration layer.

## `reports/`

Stores generated runtime outputs.

Current usage includes:

* pytest-html reports
* failure screenshots
* Allure result data
* generated Allure HTML reports
* CI artifact source files

Current generated paths include:

```text
reports/smoke-report.html
reports/regression-report.html
reports/report.html
reports/screenshots/
reports/allure-results/
reports/allure-report/
```

Generated runtime outputs should not be committed to Git.

They are intended for:

* debugging
* failure analysis
* execution evidence
* CI artifacts
* local report review

### pytest-html Outputs

Current CI browser jobs generate:

```text
reports/smoke-report.html
reports/regression-report.html
reports/report.html
```

Smoke and Regression remain focused on pytest-html reporting.

The full-suite job also preserves pytest-html in addition to generating Allure data.

### Allure Result Data

Allure result collection writes structured execution data to:

```text
reports/allure-results/
```

This data is generated by `allure-pytest`.

It is runtime output rather than repository content.

### Allure HTML Report

The standalone Allure CLI generates the browsable HTML report under:

```text
reports/allure-report/
```

using result data from:

```text
reports/allure-results/
```

The CLI is a report-generation prerequisite separate from the Python `allure-pytest` dependency.

### Failure Screenshots

Failure screenshots are stored under:

```text
reports/screenshots/
```

Screenshot filenames include the test name and UTC timestamp.

When Allure result collection is active, the same successfully captured file is reused as the Allure failure attachment.

### Generated-Output Boundary

The repository ignore policy excludes generated report content.

Current relevant ignore behavior includes:

```text
reports/*
!reports/.gitkeep

allure-results/
allure-report/
```

The implemented Allure paths are nested under `reports/` and are therefore already excluded by `reports/*`.

The additional root-level Allure ignore rules also protect against accidental output produced with different paths.

Generated outputs remain outside version-controlled project content.

Detailed report and artifact naming is documented in:

```text
docs/ci-cd-pipeline.md
```

## `test_cases/`

Contains manual test case documentation.

Current files:

```text
test_cases/login-page.md
test_cases/inventory-page.md
test_cases/product-details-page.md
test_cases/cart-page.md
test_cases/checkout-page.md
```

Test cases are mapped to automation through identifiers such as:

* `TC-LOGIN-XXX`
* `TC-INVENTORY-XXX`
* `TC-PRODUCT-DETAILS-XXX`
* `TC-CART-XXX`
* `TC-CHECKOUT-XXX`

The same identifiers are also used in parametrized pytest output where practical.

Test case files remain the source of truth for individual automation status.

Phase 4D reporting does not introduce new test case automation or test case metadata changes.

## `docs/`

Contains technical documentation for:

* architecture
* framework structure
* workflow
* Git branching strategy
* testing strategy
* pytest marker strategy
* sequential and parallel execution strategy
* reporting strategy
* CI/CD
* quality tooling
* technology stack
* features
* roadmap

Documentation should reflect current implemented behavior and clearly separate it from planned functionality.

Reporting documentation should distinguish:

* pytest-html responsibilities
* Allure responsibilities
* failure screenshot responsibilities
* GitHub Actions artifact responsibilities
* generated runtime output from repository content

## Login Test Architecture

The Login test area follows:

```text
Manual Login test cases
        ↓
Centralized Login test data
        ↓
LoginPage
        ↓
Pytest Login module
        ↓
Markers and parametrization
        ↓
Selective local execution
        ↓
Sequential / parallel suite execution
        ↓
Reporting
        ↓
CI execution
```

Depending on marker assignment, Login tests may participate in:

* dedicated parallel Smoke CI execution
* dedicated parallel Regression CI execution
* parallel complete full-suite CI execution
* complete full-suite Allure reporting

Current Login coverage includes:

* successful Login
* invalid username validation
* invalid password validation
* combined invalid username and password validation
* empty username validation
* empty password validation
* empty credentials validation
* locked out user validation
* authentication error close behavior
* Login page visibility
* password masking
* Enter submission
* protected Inventory route
* protected Cart route
* protected Product Details route
* protected Checkout Information route
* protected Checkout Overview route
* protected Checkout Complete route
* input error icons

Credential-validation cases and selected protected-route scenarios use pytest parametrization.

Parametrized IDs use manual test case IDs where practical.

Parametrized Login cases remain independent and may be distributed between xdist workers.

## Inventory Test Architecture

The Inventory test area follows:

```text
Manual Inventory test cases
        ↓
Centralized product data
        ↓
InventoryPage
        ↓
Reusable logged-in fixture
        ↓
Reusable product assertions
        ↓
Pytest Inventory module
        ↓
Markers and parametrization
        ↓
Selective local execution
        ↓
Sequential / parallel suite execution
        ↓
Reporting
        ↓
CI execution
```

Depending on marker assignment, Inventory tests may participate in:

* dedicated parallel Smoke CI execution
* dedicated parallel Regression CI execution
* parallel complete full-suite CI execution
* complete full-suite Allure reporting

Current Inventory coverage includes:

* Inventory visibility
* product list validation
* product card validation
* Cart navigation
* representative Add to cart behavior
* all-products Add to cart coverage
* Add to cart → Remove state validation
* representative Remove behavior
* all-products Remove coverage
* Remove → Add to cart state validation
* cart badge visibility
* cart badge count updates
* cart badge disappearance
* sorting by name
* sorting by price
* Product Details navigation through product names
* Product Details navigation through product images
* representative navigation checkpoints
* broader all-products navigation coverage

Inventory tests reuse:

```text
test_data/product_test_data.py
```

## Product Details Test Architecture

The Product Details test area follows:

```text
Manual Product Details test cases
        ↓
Centralized product data
        ↓
ProductDetailsPage
        ↓
Reusable logged-in fixture
        ↓
Reusable product assertions
        ↓
Pytest Product Details module
        ↓
Markers and parametrization
        ↓
Selective local execution
        ↓
Sequential / parallel suite execution
        ↓
Reporting
        ↓
CI execution
```

Depending on marker assignment, Product Details tests may participate in:

* dedicated parallel Smoke CI execution
* dedicated parallel Regression CI execution
* parallel complete full-suite CI execution
* complete full-suite Allure reporting

Current Product Details coverage includes:

* representative Product Details visibility
* all-products Product Details validation
* Back to products navigation
* representative Add to cart
* all-products Add to cart
* Add to cart → Remove state
* representative Remove
* all-products Remove
* Remove → Add to cart state
* cart badge visibility
* cart badge count updates
* cart badge disappearance
* Cart navigation
* full Product Details → Cart navigation coverage across all products

## Cart Test Architecture

The Cart test area follows:

```text
Manual Cart test cases
        ↓
Centralized Login and product data
        ↓
InventoryPage / ProductDetailsPage / CartPage
        ↓
Reusable Cart setup fixtures
        ↓
Reusable product assertions
        ↓
Pytest Cart module
        ↓
Markers and parametrization
        ↓
Selective local execution
        ↓
Sequential / parallel suite execution
        ↓
Reporting
        ↓
CI execution
```

Depending on marker assignment, Cart tests may participate in:

* dedicated parallel Smoke CI execution
* dedicated parallel Regression CI execution
* parallel complete full-suite CI execution
* complete full-suite Allure reporting

Current Cart coverage includes:

* empty Cart
* representative Cart item visibility
* Cart item content validation
* all-products Cart content validation
* representative Remove behavior
* all-products Remove coverage
* cart badge removal
* cart badge decrement
* Continue Shopping
* Continue Shopping state preservation
* Cart persistence after logout and re-login
* Product Details navigation from Cart
* full Cart → Product Details navigation coverage across all products
* Cart → Checkout Information navigation
* Cart-related E2E checkpoints

Cart test state is prepared independently per test and was validated under xdist execution.

## Checkout Test Architecture

The Checkout test area follows:

```text
Manual Checkout test cases
        ↓
Centralized Checkout and product data
        ↓
Checkout Page Objects
        ↓
Reusable Checkout setup fixtures
        ↓
Reusable product and checkout assertions
        ↓
Pytest Checkout module
        ↓
Markers and parametrization
        ↓
Selective local execution
        ↓
Sequential / parallel suite execution
        ↓
Reporting
        ↓
CI execution
```

Depending on marker assignment, Checkout tests may participate in:

* dedicated parallel Smoke CI execution
* dedicated parallel Regression CI execution
* parallel complete full-suite CI execution
* complete full-suite Allure reporting

Current Checkout coverage includes:

* Checkout Information form validation
* lightweight Smoke validation of Checkout Information form availability
* required First Name validation
* required Last Name validation
* required Postal Code validation
* input error icons
* validation error messages
* validation error close behavior
* valid data transition to Checkout Overview
* Checkout Information cancellation
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
* Checkout-related E2E checkpoints

Checkout fixture chains prepare their required Cart and checkout state independently and were validated under worker-level parallel execution.

## Marker Architecture

Pytest markers provide orthogonal test categorization and selective execution.

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

Markers are not mutually exclusive.

A test may use multiple markers when it legitimately belongs to multiple suites.

Example:

```python
'@pytest.mark.smoke'
'@pytest.mark.navigation'
'@pytest.mark.e2e'
```

This represents a test that is simultaneously:

* a representative critical check
* a Navigation scenario
* an E2E journey checkpoint

Detailed marker semantics are documented in:

```text
docs/testing-strategy.md
```

### Marker Execution Responsibilities

All executable markers remain available for selective local execution.

Dedicated CI jobs currently exist for:

* `smoke`
* `regression`

Dedicated CI jobs do not currently exist for:

* `ui`
* `security`
* `sorting`
* `navigation`
* `e2e`

Tests carrying those markers are still included in complete full-suite CI execution.

Dedicated CI execution, reporting, and marker semantics are separate concerns:

* markers define test intent and selectable suites
* CI determines which marker expressions receive dedicated workflow jobs
* xdist determines how collected tests are distributed between workers
* reporting integrations consume results from the resulting execution

Parallel execution and Allure reporting do not change marker semantics or marker assignment.

## E2E Architecture

The E2E suite represents independent checkpoints that collectively form the primary purchase journey.

Logical journey:

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

E2E architecture deliberately avoids:

* shared state between test cases
* required test execution order
* one monolithic test containing the entire purchase flow

Each E2E test prepares its own required state through fixtures or local setup.

This allows:

```bash
pytest -m e2e -v
```

to execute a logical purchase-journey checkpoint suite while keeping individual tests isolated.

This independent checkpoint model also makes the E2E tests compatible with xdist execution as part of the parallel full suite.

E2E does not currently have a dedicated GitHub Actions job.

E2E tests remain part of the complete unfiltered full-suite CI execution and may therefore be distributed between xdist workers.

When full-suite Allure result collection is enabled, E2E checkpoints are represented as normal results within the advanced full-suite report.

## Reporting Architecture

The reporting architecture uses complementary tools with different responsibilities.

```text
Pytest execution
      ↓
┌──────────────────────────────┐
│ pytest-html                  │
│ lightweight HTML reporting   │
└──────────────────────────────┘

Pytest execution
      ↓
┌──────────────────────────────┐
│ allure-pytest                │
│ structured Allure results    │
└──────────────────────────────┘
      ↓
Allure CLI
      ↓
generated Allure HTML report

failed browser test
      ↓
existing screenshot hook
      ↓
reports/screenshots/*.png
      ↓
same PNG attached to Allure
```

### pytest-html Responsibility

pytest-html remains the lightweight reporting layer.

It is used in:

* Smoke CI
* Regression CI
* full-suite CI

Current paths:

```text
reports/smoke-report.html
reports/regression-report.html
reports/report.html
```

Allure does not replace pytest-html.

### Allure Result Responsibility

The Python `allure-pytest` integration collects structured result data.

Current result location:

```text
reports/allure-results/
```

Local result collection may use:

```bash
pytest -v \
  --alluredir=reports/allure-results \
  --clean-alluredir
```

or:

```bash
pytest -n auto -v \
  --alluredir=reports/allure-results \
  --clean-alluredir
```

Allure result collection is compatible with both sequential and parallel execution.

### Allure CLI Responsibility

The standalone Allure CLI converts result data into a browsable HTML report.

Current command:

```bash
allure generate reports/allure-results \
  --clean \
  -o reports/allure-report
```

Current output location:

```text
reports/allure-report/
```

The Allure CLI is separate from the Python plugin.

Installing `allure-pytest` does not itself provide the standalone HTML report generator.

### Failure Evidence Responsibility

Failure screenshots remain independent runtime evidence.

Current screenshot location:

```text
reports/screenshots/
```

The same successfully captured PNG may additionally be embedded in Allure.

This avoids duplicate browser capture logic while providing richer report context.

### Reporting Scope Boundaries

Current reporting architecture does not include:

* Allure history persistence
* trend-history storage
* hosted Allure reports
* GitHub Pages report publishing
* trace policy
* video policy
* retry architecture
* cross-browser reporting

Those capabilities remain outside the implemented Phase 4D reporting scope.

## Local And CI Execution Architecture

Local execution supports:

* sequential full-suite validation
* parallel full-suite validation
* selective marker-based validation
* parallel Smoke validation
* parallel Regression validation
* local Allure result generation
* local Allure HTML report generation

Sequential full local execution:

```bash
pytest -v
```

Parallel full local execution:

```bash
pytest -n auto -v
```

Approved parallel marker execution:

```bash
pytest -m smoke -n auto -v
pytest -m regression -n auto -v
```

Current marker suites remain selectively executable sequentially:

```bash
pytest -m smoke -v
pytest -m regression -v
pytest -m ui -v
pytest -m security -v
pytest -m sorting -v
pytest -m navigation -v
pytest -m e2e -v
```

Sequential execution remains a supported execution mode.

Parallel execution is an additional validated capability rather than a replacement for sequential execution.

Reporting is layered on top of either execution mode rather than defining a separate test implementation.

### Phase 4B CI Architecture

GitHub Actions separates code-quality validation from browser-test execution.

Current job structure:

```text
quality
├── smoke
├── regression
└── full-suite
```

The `quality` job executes first and validates:

* Ruff
* Black
* isort

The quality job does not install Playwright Chromium.

Smoke, Regression, and full-suite declare:

```yaml
needs: quality
```

After successful quality validation, the three browser jobs are independently executable and do not depend on each other.

This Phase 4B job structure remains unchanged after Phase 4C and Phase 4D.

### Phase 4C Worker-Level Execution

Phase 4C enables pytest-xdist worker-level parallelism inside the existing browser-test jobs.

Current architecture:

```text
quality
├── smoke
│   └── xdist workers
├── regression
│   └── xdist workers
└── full-suite
    └── xdist workers
```

The two concurrency layers are separate:

* GitHub Actions may schedule Smoke, Regression, and full-suite jobs concurrently after `quality`
* pytest-xdist distributes collected tests between worker processes inside each browser-test job

The `quality` job does not use xdist.

### Phase 4D Reporting Layer

Phase 4D adds reporting inside the existing execution architecture.

Current reporting model:

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
        ├── failure screenshots
        └── Allure HTML report
```

Phase 4D does not add another browser job.

### Smoke CI Execution

Smoke executes:

```bash
pytest -m smoke -n auto -v
```

The actual CI command also generates:

```text
reports/smoke-report.html
```

Smoke remains pytest-html-focused and does not generate a dedicated Allure report.

### Regression CI Execution

Regression executes:

```bash
pytest -m regression -n auto -v
```

The actual CI command also generates:

```text
reports/regression-report.html
```

Regression remains pytest-html-focused and does not generate a dedicated Allure report.

### Full-Suite CI Execution

The full-suite job executes the complete unfiltered Pytest suite:

```bash
pytest -n auto -v \
  --html=reports/report.html \
  --self-contained-html \
  --alluredir=reports/allure-results \
  --clean-alluredir
```

The full-suite job remains the complete automated regression gate.

The execution generates:

```text
reports/report.html
reports/allure-results/
```

CI then attempts to generate:

```text
reports/allure-report/
```

when usable Allure result data exists.

Smoke and Regression provide dedicated targeted feedback without replacing full-suite execution.

### Browser Execution

Playwright Chromium is installed only in browser-test jobs:

* Smoke
* Regression
* full-suite

The quality job does not prepare a browser environment.

Current local and CI browser scope remains Chromium-only.

Parallel execution and Allure reporting do not introduce a cross-browser execution architecture.

## CI Artifact Architecture

Each browser job uses non-conflicting GitHub Actions artifact names.

### Smoke

```text
smoke-pytest-html-report
smoke-test-artifacts
```

### Regression

```text
regression-pytest-html-report
regression-test-artifacts
```

### Full Suite

```text
pytest-html-report
full-suite-allure-report
test-artifacts
```

The dedicated Allure artifact publishes:

```text
reports/allure-report/
```

The existing broader full-suite artifact continues to publish:

```text
reports/
```

Artifact uploads use:

```yaml
if: always()
```

so available runtime evidence can still be published when an executing browser-test command fails.

The Allure report-generation step also uses failure-tolerant workflow control.

It checks whether usable result data exists before calling the Allure CLI.

Therefore a failed full-suite test run may still produce:

* pytest-html output
* failure screenshots
* Allure result data
* generated Allure HTML
* downloadable artifacts

The failed test command still fails the full-suite job.

Reporting does not change the quality-gate result.

Current artifact retention remains:

```text
7 days
```

Detailed CI commands, triggers, report paths, artifact names, and retention are documented in:

```text
docs/ci-cd-pipeline.md
```

## Parallel Execution Architecture

`pytest-xdist` is the worker-level parallel execution layer used by the current framework.

The implementation uses:

```text
-n auto
```

for automatic worker-count selection.

Worker count is determined by the execution environment and is not treated as a fixed architectural constant.

### Parallel-Safety Model

The current architecture relies on test independence rather than worker-specific coordination.

Parallel-safe expectations include:

* function-scoped browser/test setup
* no dependence on test order
* no browser state shared between tests
* no state handoff between E2E checkpoints
* no dependency between parametrized cases
* deterministic setup through fixtures or test-local preparation
* no assumption about which worker executes a given test

Cart, Checkout, logout/re-login persistence, E2E checkpoints, and parametrized all-product scenarios were validated under worker-level execution.

No sequential-only execution exception is required for the current suite.

### Reporting Under Parallel Execution

The reporting architecture is designed to operate with the same worker-level execution model.

Validated reporting behavior includes:

* pytest-html generation during xdist execution
* Allure result collection during xdist execution
* failure screenshot generation during xdist execution
* reuse of failure screenshots as Allure attachments
* generated Allure HTML reports based on the collected results

No separate sequential-only reporting architecture is maintained.

### Sequential Compatibility

Sequential execution remains supported.

This is important for:

* focused debugging
* failure reproduction
* standard local validation where parallelism is unnecessary
* preserving a simple baseline execution mode

The framework therefore supports both:

```text
sequential Pytest execution
parallel Pytest execution through pytest-xdist
```

without maintaining separate test implementations.

The same reporting components can be applied to either mode where needed.

## CI Execution Boundaries

The current execution architecture combines Phase 4B, Phase 4C, and implemented Phase 4D reporting capabilities.

Phase 4B includes:

* separate code-quality validation
* dedicated Smoke CI execution
* dedicated Regression CI execution
* complete full-suite CI execution
* explicit quality-gate dependencies
* job-specific reports and artifacts
* independent GitHub Actions browser jobs after `quality`

Phase 4C includes:

* validated local pytest-xdist execution
* parallel Smoke execution
* parallel Regression execution
* parallel complete full-suite execution
* xdist integration into the existing browser-test jobs
* continued sequential execution support
* validated fixture and test independence
* validated E2E and parametrized-case independence
* preservation of existing reporting and failure-artifact behavior

Phase 4D reporting includes:

* Allure Pytest integration
* local Allure result collection
* local Allure HTML generation
* failure screenshot attachment to Allure
* sequential reporting compatibility
* parallel reporting compatibility
* full-suite CI Allure result collection
* full-suite CI Allure HTML generation
* dedicated `full-suite-allure-report` artifact
* preservation of pytest-html
* preservation of existing screenshot capture
* preservation of existing artifact behavior

GitHub Actions job-level concurrency and pytest-xdist worker-level parallelism remain distinct architectural layers.

Reporting is a separate concern layered on top of test execution.

Runtime environment configuration and other later framework maturity capabilities remain outside the current implemented architecture.

## Design Direction

The framework follows a modular architecture where:

* tests describe behavior and expectations
* Page Objects handle interactions
* `BasePage` owns minimal common page behavior
* `AppPage` owns shared authenticated behavior
* assertion helpers own reusable validation logic
* test data remains externalized
* fixtures prepare deterministic reusable state
* tests remain independent across sequential and parallel execution
* manual test cases define documented scenario coverage
* markers organize selective test suites
* pytest-xdist provides worker-level parallel execution
* pytest-html provides lightweight reporting
* Allure provides advanced execution reporting
* failure screenshots provide browser evidence
* GitHub Actions artifacts preserve CI runtime evidence
* CI validates code quality before browser execution
* CI provides dedicated Smoke and Regression feedback
* CI preserves complete full-suite regression validation
* GitHub Actions job concurrency remains separate from Pytest worker concurrency
* generated runtime outputs remain separate from repository source content
* documentation describes implemented framework behavior

Future framework maturity work may improve:

* fixture organization
* environment configuration
* logging
* diagnostics
* reporting analytics

Current Phase 4D reporting does not include:

* Allure history persistence
* report hosting
* GitHub Pages reporting
* retries
* trace/video policy
* cross-browser reporting

Future API, cross-browser, Docker, Selenium, or Jenkins extensions remain separate from the current architecture.

## Architecture Principles

The framework should prioritize:

* readability
* maintainability
* deterministic execution
* test independence
* sequential and parallel execution compatibility
* reporting compatibility with both execution modes
* clear responsibility boundaries
* reusable components
* centralized test data
* traceability
* explicit marker semantics
* selective local validation
* dedicated Smoke and Regression CI feedback
* complete full-suite CI validation
* staged quality-gate execution
* clear separation of CI job concurrency and Pytest worker parallelism
* clear separation of execution from reporting
* clear separation of generated output from repository content
* incremental framework growth

The framework should avoid:

* unnecessary helper layers
* duplicated selectors
* duplicated test data
* shared test-state dependencies
* execution-order dependencies
* worker-specific test dependencies
* reporting-specific duplicate test implementations
* duplicate screenshot capture mechanisms
* mixing detailed Checkout behavior into Cart ownership
* moving page-specific behavior into generic helpers prematurely
* moving authenticated shared behavior out of `AppPage`
* treating every Playwright test as automatically belonging to `ui`
* assigning Regression mechanically to every non-Smoke test
* treating CI job-level concurrency as Pytest parallel execution
* describing pytest-xdist as future-only functionality after Phase 4C
* describing Allure as unimplemented after AQA-0096 and AQA-0097
* describing Allure history or hosted reporting as implemented
* describing future framework capabilities as already implemented

## Current Architecture Status

The current architecture supports automated page-level coverage for:

* Login
* Inventory
* Product Details
* Cart
* Checkout

Current architecture capabilities include:

* `BasePage`
* `AppPage`
* Page Object Model
* reusable assertion helpers
* centralized test data
* reusable fixtures
* test case traceability
* parametrized execution
* normalized pytest marker strategy
* Smoke execution
* Regression execution
* UI execution
* Security execution
* Sorting execution
* Navigation execution
* independent E2E checkpoint execution
* local selective validation
* sequential Pytest execution
* pytest-xdist worker-level parallel execution
* parallel Smoke validation
* parallel Regression validation
* parallel full-suite validation
* separate CI code-quality validation
* dedicated parallel Smoke CI execution
* dedicated parallel Regression CI execution
* parallel complete full-suite CI validation
* pytest-html reporting
* Allure result collection
* Allure HTML generation
* failure screenshot capture
* Allure failure screenshot attachments
* job-specific CI artifacts
* dedicated full-suite Allure artifact

Current CI architecture:

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
        ├── failure screenshots
        └── Allure HTML report
```

The `quality` job is the prerequisite gate.

Smoke, Regression, and full-suite are independent browser jobs after successful quality validation.

UI, Security, Sorting, Navigation, and E2E do not currently have dedicated CI jobs but remain selectively executable locally and participate in complete full-suite execution.

Pytest-xdist parallel execution is implemented locally and in the three existing CI browser-test jobs.

Allure reporting is implemented locally and in the complete full-suite CI reporting path.

Smoke and Regression retain their pytest-html-focused reporting behavior.

No sequential-only test or reporting exceptions were identified for the current implemented execution model.

The `main` branch represents the stable portfolio version of the project.

The `develop` branch and active workstream branches may contain newer validated changes before promotion.

The current architecture direction remains Phase 4 Framework Maturity.

Phase 4B CI Execution Strategy and Phase 4C Parallel Execution Strategy are implemented.

Phase 4D reporting capabilities implemented through the active workstream include local Allure reporting, failure screenshot integration, and full-suite CI Allure reporting.

The Phase 4D workstream should not be treated as fully completed until its remaining approved work and final checkpoint are completed.