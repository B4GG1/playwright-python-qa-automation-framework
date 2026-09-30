# Architecture

This document describes the current architecture of the QA automation framework.

The project follows a lightweight, modular architecture focused on readability, maintainability, traceability, deterministic execution, test independence, configurable runtime behavior, reporting visibility, and incremental framework growth.

The current architecture includes Page Object Model, shared authenticated-page behavior, reusable assertions, reusable pytest fixtures, centralized test data, centralized runtime configuration, explicit marker-based test organization, sequential and pytest-xdist parallel execution, staged CI execution, pytest-html reporting, Allure reporting, configurable failure screenshots, optional Playwright trace and video generation, GitHub Actions artifacts, and technical documentation.

## Current Architecture Scope

The current framework includes:

* Pytest-based test execution
* Playwright browser automation
* pytest-playwright integration
* pytest-xdist worker-level parallel execution
* supported sequential Pytest execution
* Page Object Model for Login, Inventory, Product Details, Cart, and Checkout
* shared `BasePage` abstraction
* shared authenticated-page behavior through `AppPage`
* reusable product and checkout assertion helpers
* reusable pytest fixtures
* centralized login, product, and checkout test data
* centralized runtime configuration through `config/settings.py`
* environment-based application base URL configuration
* runtime browser selection
* headed/headless execution configuration
* Playwright action and navigation timeout configuration
* Playwright assertion timeout configuration
* configurable screenshot policy
* configurable trace policy
* configurable video policy
* fail-fast runtime configuration validation
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
* explicit runtime defaults in browser-test CI jobs
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
* optional Playwright trace generation
* optional Playwright video generation
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

The framework is organized into the following primary layers:

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
Playwright / Pytest / pytest-playwright / pytest-xdist
    ↓
reporting / diagnostics
    ↓
local validation / CI
```

Runtime configuration is a cross-cutting framework concern:

```text
environment variables
        ↓
config/settings.py
        ↓
┌───────────────────────┬─────────────────────────┐
│ BasePage              │ conftest.py             │
│ base URL composition  │ browser/runtime policy  │
└───────────────────────┴─────────────────────────┘
        ↓
Playwright / pytest-playwright execution
```

Reporting and diagnostics currently include:

```text
pytest-html
Allure
failure screenshots
optional Playwright traces
optional Playwright videos
GitHub Actions artifacts
```

The layers are intentionally lightweight.

New abstractions should be introduced only when repeated behavior or clear responsibility boundaries justify them.

## `tests/`

Contains automated test suites.

Current functional test modules:

```text
tests/test_login_page.py
tests/test_inventory_page.py
tests/test_product_details_page.py
tests/test_cart_page.py
tests/test_checkout_page.py
```

Runtime configuration validation is additionally covered by:

```text
tests/test_runtime_config.py
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
* operate without embedding environment-specific runtime configuration
* produce normal Pytest result data consumed by reporting integrations

Test modules should not duplicate selectors when Page Objects already expose the required interaction or state.

Test modules should not depend on state produced by another test because xdist workers may execute tests independently and in a different order from sequential execution.

Tests should not hardcode runtime configuration that belongs to `config/settings.py`.

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
* defining relative application routes where direct page opening is supported

The Page Object layer should remain focused on interaction logic.

Assertions should remain in tests or reusable assertion helpers.

Reporting concerns should not be moved into Page Objects.

Runtime browser ownership, timeout configuration, artifact policies, and environment-variable parsing should not be implemented independently inside Page Objects.

Parallel execution, reporting, and runtime configuration do not change Page Object ownership or responsibility boundaries.

## `BasePage`

`BasePage` provides the minimal shared page foundation.

Current responsibilities:

* storing the Playwright `Page`
* providing shared relative route metadata through `ROUTE`
* composing application URLs from `settings.base_url`, `ROUTE`, and an optional suffix
* providing shared `open()` behavior for directly accessible pages

Current URL composition follows:

```text
settings.base_url + PageObject.ROUTE + optional suffix
```

The default application origin is supplied by the runtime configuration layer rather than hardcoded separately in each Page Object.

This allows `QA_BASE_URL` to change the application origin without modifying tests or Page Objects.

`BasePage` should remain intentionally small.

It should not become a generic container for unrelated framework helpers, reporting logic, browser lifecycle management, or runtime configuration parsing.

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

* opening Login through the configured application base URL
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
* runtime configuration
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

Runtime configuration is also not test data and is owned by `config/settings.py`.

## `conftest.py`

Contains shared pytest hooks, runtime integration, and fixtures.

Current runtime responsibilities include:

* loading the centralized runtime settings
* applying configured browser selection to pytest-playwright when no explicit native browser option is provided
* applying configured headed mode
* preserving explicit native pytest-playwright browser options
* applying configured trace policy unless an explicit native tracing option was provided
* applying configured video policy unless an explicit native video option was provided
* configuring the Playwright assertion timeout
* creating browser contexts through pytest-playwright's existing `new_context` fixture
* applying default Playwright action timeout to created contexts
* applying default Playwright navigation timeout to created contexts
* controlling the custom failure screenshot mechanism through screenshot policy

Current fixture responsibilities include:

* `opened_login_page`
* `standard_user`
* `logged_in_inventory_page`
* `inventory_page_with_one_product_in_cart`
* `cart_page_with_one_product`
* `checkout_step_one_page_with_one_product`
* `checkout_step_two_page_with_one_product`
* `checkout_last_step_page_with_one_product`

The framework does not manually start or own Playwright browser processes.

Browser lifecycle remains based on the pytest-playwright fixture model.

The project-level `context` fixture extends the existing pytest-playwright `new_context` path only to apply approved runtime timeout configuration.

Fixtures prepare deterministic state without making tests depend on execution order.

The current Playwright page/context flow and project fixture chains remain function-scoped for test execution.

Each test therefore prepares and owns the browser/application state required for its scenario rather than consuming browser state produced by another test.

This fixture model was validated under pytest-xdist worker-level parallel execution during Phase 4C and remained compatible with Phase 4E runtime configuration integration.

### Failure Screenshot Hook

The failure hook reacts only to failed Pytest test-call reports.

It does not capture screenshots for setup-phase or teardown-phase failures.

When:

```text
QA_SCREENSHOT_POLICY=only-on-failure
```

and the failed test has a Playwright `page` fixture, the hook creates a failure screenshot under:

```text
reports/screenshots/
```

The filename contains:

* the test name
* a UTC timestamp

The existing screenshot mechanism remains the primary project-level screenshot capture mechanism.

Phase 4E does not introduce a second project-level screenshot implementation through pytest-playwright.

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

When:

```text
QA_SCREENSHOT_POLICY=off
```

the custom failure screenshot is not written and the corresponding Allure screenshot attachment is not created.

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
* runtime-configuration compatibility
* CI stability

Tests should not rely on shared browser state produced by earlier test cases.

Tests must also not assume:

* a specific xdist worker
* a specific test order
* a relationship between parametrized cases
* a reporting system to prepare functional state
* a runtime configuration value hardcoded inside a test

No sequential-only test exceptions were identified during Phase 4C validation.

Phase 4D reporting and Phase 4E runtime configuration do not change these independence requirements.

## `config/`

Contains centralized framework runtime configuration.

Current implementation:

```text
config/settings.py
```

The configuration layer owns:

* reading approved environment variables
* default runtime values
* normalization
* validation
* immutable runtime settings exposed to the framework

Current environment variables are:

```text
QA_BASE_URL
QA_BROWSER
QA_HEADED
QA_TIMEOUT_MS
QA_EXPECT_TIMEOUT_MS
QA_SCREENSHOT_POLICY
QA_TRACE_POLICY
QA_VIDEO_POLICY
```

Current defaults are:

```text
QA_BASE_URL=https://www.saucedemo.com
QA_BROWSER=chromium
QA_HEADED=false
QA_TIMEOUT_MS=30000
QA_EXPECT_TIMEOUT_MS=5000
QA_SCREENSHOT_POLICY=only-on-failure
QA_TRACE_POLICY=off
QA_VIDEO_POLICY=off
```

### Base URL Configuration

`QA_BASE_URL` controls the application origin used by `BasePage`.

The default is:

```text
https://www.saucedemo.com
```

The value must:

* use `http` or `https`
* contain a valid host
* contain only the application origin
* not contain credentials
* not contain query parameters
* not contain a fragment
* not contain whitespace
* use a valid port when a port is supplied

A trailing slash is normalized away.

### Browser Configuration

`QA_BROWSER` supports:

```text
chromium
firefox
webkit
```

Browser values are normalized by trimming surrounding whitespace and converting to lowercase.

The configuration layer recognizes Playwright browser engines.

Recognition of Firefox and WebKit does not mean that they are installed or validated in every execution environment.

Current CI remains intentionally Chromium-only.

When an explicit native pytest-playwright `--browser` option is supplied, the project configuration does not silently replace it.

### Headed Configuration

`QA_HEADED` supports predictable boolean parsing.

Accepted true values:

```text
true
1
yes
on
```

Accepted false values:

```text
false
0
no
off
```

Boolean values are case-insensitive after normalization.

The default remains:

```text
false
```

The native pytest-playwright `--headed` option also remains usable.

### Timeout Configuration

`QA_TIMEOUT_MS` controls:

* Playwright default action timeout
* Playwright default navigation timeout

Default:

```text
30000
```

`QA_EXPECT_TIMEOUT_MS` controls the Playwright assertion timeout.

Default:

```text
5000
```

Timeout values must be non-negative integers representing milliseconds.

A value of `0` is accepted and follows Playwright timeout semantics.

### Screenshot Policy

`QA_SCREENSHOT_POLICY` supports:

```text
only-on-failure
off
```

Default:

```text
only-on-failure
```

This policy controls the existing custom screenshot and Allure attachment behavior rather than creating a duplicate screenshot implementation.

### Trace And Video Policies

Both `QA_TRACE_POLICY` and `QA_VIDEO_POLICY` support:

```text
off
retain-on-failure
on
```

Defaults:

```text
QA_TRACE_POLICY=off
QA_VIDEO_POLICY=off
```

Trace and video use pytest-playwright / Playwright-supported artifact mechanisms.

They are not implemented through custom recording logic.

Explicit native pytest-playwright tracing or video options remain usable and take precedence when supplied directly on the command line.

### Invalid Configuration

Invalid explicit environment-variable values raise configuration errors before normal test execution proceeds.

Invalid values include, for example:

* unsupported browser names
* unsupported artifact policy values
* invalid boolean values
* negative timeout values
* non-integer timeout values
* malformed base URLs

The configuration error identifies the affected environment variable.

This prevents silently falling back from invalid explicit runtime configuration.

### Runtime Configuration Boundaries

The current configuration architecture does not implement:

* named environment profiles
* automatic `.env` loading
* browser matrices
* cross-browser CI execution
* device emulation
* browser channels
* mobile emulation
* slow motion configuration
* retries
* Phase 4F logging redesign
* Phase 4F fixture cleanup

Runtime configuration should remain focused on approved execution concerns rather than becoming a generic container for unrelated framework behavior.

## `reports/`

Stores generated reporting and failure-evidence runtime outputs.

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

when screenshot policy is enabled and a browser test fails during the Pytest call phase.

Screenshot filenames include the test name and UTC timestamp.

When Allure result collection is active, the same successfully captured file is reused as the Allure failure attachment.

### Playwright Trace And Video Outputs

When trace or video generation is enabled, pytest-playwright-generated runtime output is written under its artifact structure, currently rooted under:

```text
test-results/
```

Depending on the selected policy, generated output may include:

```text
trace.zip
video.webm
```

Trace and video remain disabled by default.

They are runtime diagnostic outputs and should not be committed to Git.

### Generated-Output Boundary

The repository ignore policy excludes generated reporting and Playwright runtime artifact content.

Relevant generated areas include:

```text
reports/
test-results/
allure-results/
allure-report/
```

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

Phase 4D reporting and Phase 4E runtime configuration do not introduce new test case automation or test case metadata changes.

## `docs/`

Contains technical documentation for:

* architecture
* framework structure
* workflow
* Git branching strategy
* testing strategy
* pytest marker strategy
* sequential and parallel execution strategy
* runtime configuration strategy
* reporting strategy
* CI/CD
* quality tooling
* technology stack
* features
* roadmap

Documentation should reflect current implemented behavior and clearly separate it from planned functionality.

Runtime configuration documentation should distinguish:

* supported environment variables
* approved defaults
* accepted values
* normalization and validation behavior
* local overrides
* native pytest-playwright CLI behavior
* local capabilities from CI boundaries

Reporting documentation should distinguish:

* pytest-html responsibilities
* Allure responsibilities
* failure screenshot responsibilities
* Playwright trace and video responsibilities
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

Runtime configuration is applied outside the Login test module and therefore does not change Login test ownership or test design.

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

Dedicated CI execution, reporting, runtime configuration, and marker semantics are separate concerns:

* markers define test intent and selectable suites
* runtime configuration defines execution settings
* CI determines which marker expressions receive dedicated workflow jobs
* xdist determines how collected tests are distributed between workers
* reporting integrations consume results from the resulting execution

Parallel execution, reporting, and runtime configuration do not change marker semantics or marker assignment.

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

Runtime environment overrides apply to E2E execution in the same way as to other Pytest suites.

## Reporting And Diagnostic Architecture

The reporting and diagnostic architecture uses complementary tools with different responsibilities.

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

failed browser test call
      ↓
QA_SCREENSHOT_POLICY
      ↓
existing screenshot hook
      ↓
reports/screenshots/*.png
      ↓
same PNG attached to Allure

pytest-playwright execution
      ↓
QA_TRACE_POLICY / QA_VIDEO_POLICY
      ↓
optional trace.zip / video.webm
      ↓
test-results/
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

This avoids duplicate screenshot capture logic while providing richer report context.

Screenshot generation can be disabled through:

```text
QA_SCREENSHOT_POLICY=off
```

### Trace And Video Responsibility

Trace and video generation use pytest-playwright / Playwright-supported capabilities.

Current policies:

```text
QA_TRACE_POLICY
QA_VIDEO_POLICY
```

Both default to:

```text
off
```

Supported values are:

```text
off
retain-on-failure
on
```

When enabled, generated files use pytest-playwright's runtime artifact structure under `test-results/`.

The framework does not implement custom trace or video recording logic.

### Reporting And Diagnostic Scope Boundaries

Current reporting and diagnostic architecture does not include:

* Allure history persistence
* trend-history storage
* hosted Allure reports
* GitHub Pages report publishing
* retry architecture
* cross-browser reporting
* Phase 4F logging redesign
* Phase 4F diagnostic redesign

Trace and video policies are implemented, but remain disabled by default.

## Local And CI Execution Architecture

Local execution supports:

* sequential full-suite validation
* parallel full-suite validation
* selective marker-based validation
* parallel Smoke validation
* parallel Regression validation
* local Allure result generation
* local Allure HTML report generation
* environment-based runtime overrides
* optional screenshot, trace, and video policy overrides

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

Runtime values may be overridden for a single process.

Example:

```bash
QA_BROWSER=chromium \
QA_HEADED=false \
QA_TIMEOUT_MS=45000 \
QA_EXPECT_TIMEOUT_MS=7000 \
QA_TRACE_POLICY=retain-on-failure \
pytest -m smoke -n auto -v
```

Sequential execution remains a supported execution mode.

Parallel execution is an additional validated capability rather than a replacement for sequential execution.

Reporting and runtime configuration are layered on top of execution rather than defining separate test implementations.

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

This Phase 4B job structure remains unchanged after Phase 4C, Phase 4D, and Phase 4E.

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

### Phase 4E Runtime Configuration Layer

Phase 4E adds environment-based runtime configuration without changing the established test-suite or CI topology.

Conceptually:

```text
environment variables
        ↓
config/settings.py
        ↓
conftest.py / BasePage
        ↓
quality
├── smoke
├── regression
└── full-suite
```

Runtime configuration controls:

* application base URL
* browser selection
* headed/headless execution
* Playwright action and navigation timeout
* Playwright assertion timeout
* screenshot policy
* trace policy
* video policy

The three browser CI jobs use explicit defaults:

```text
QA_BASE_URL=https://www.saucedemo.com
QA_BROWSER=chromium
QA_HEADED=false
QA_TIMEOUT_MS=30000
QA_EXPECT_TIMEOUT_MS=5000
QA_SCREENSHOT_POLICY=only-on-failure
QA_TRACE_POLICY=off
QA_VIDEO_POLICY=off
```

These values intentionally match the approved local defaults.

The `quality` job does not require browser runtime configuration.

Phase 4E does not introduce:

* another browser job
* a browser matrix
* Firefox CI installation
* WebKit CI installation
* cross-browser CI execution
* retries
* `continue-on-error`
* trace or video retention by default

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

The runtime configuration parser recognizes:

```text
chromium
firefox
webkit
```

but current CI installation and validation remain Chromium-only.

Local use of another configured Playwright engine requires that browser to be installed in the local environment.

No browser matrix or cross-browser CI architecture is currently implemented.

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

The Allure report-generation step also checks whether usable result data exists before calling the Allure CLI.

Therefore a failed full-suite test run may still produce:

* pytest-html output
* failure screenshots when screenshot policy allows them
* Allure result data
* generated Allure HTML
* downloadable artifacts

The failed test command still fails the full-suite job.

Reporting does not change the quality-gate result.

Current artifact retention remains:

```text
7 days
```

Trace and video remain disabled in CI by default and therefore are not introduced as default retained CI artifacts by Phase 4E.

Detailed CI commands, triggers, runtime defaults, report paths, artifact names, and retention are documented in:

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
* runtime configuration treated as process-level execution configuration rather than shared test state

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

The same runtime configuration and reporting components can be applied to either mode where appropriate.

## CI Execution Boundaries

The current execution architecture combines Phase 4B, Phase 4C, Phase 4D, and Phase 4E capabilities.

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

Phase 4D includes:

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

Phase 4E includes:

* centralized environment-based runtime configuration
* configurable application base URL
* browser selection
* headed/headless configuration
* action/navigation timeout configuration
* assertion timeout configuration
* configurable screenshot policy
* configurable trace policy
* configurable video policy
* invalid configuration validation
* integration with pytest-playwright native runtime behavior
* explicit CI runtime defaults
* preservation of Chromium-only CI execution
* preservation of the existing CI topology

GitHub Actions job-level concurrency and pytest-xdist worker-level parallelism remain distinct architectural layers.

Reporting is a separate concern layered on top of test execution.

Runtime configuration is another separate concern and does not redefine test ownership, marker semantics, or reporting ownership.

The current architecture does not implement:

* named environment profiles
* automatic `.env` loading
* cross-browser CI
* browser matrices
* device emulation
* retries
* Phase 4F logging and fixture cleanup

## Design Direction

The framework follows a modular architecture where:

* tests describe behavior and expectations
* Page Objects handle interactions
* `BasePage` owns minimal common page behavior and runtime base URL composition
* `AppPage` owns shared authenticated behavior
* assertion helpers own reusable validation logic
* test data remains externalized
* `config/settings.py` owns approved runtime configuration parsing, defaults, normalization, and validation
* `conftest.py` bridges approved runtime settings into pytest-playwright execution
* fixtures prepare deterministic reusable state
* tests remain independent across sequential and parallel execution
* manual test cases define documented scenario coverage
* markers organize selective test suites
* pytest-xdist provides worker-level parallel execution
* pytest-html provides lightweight reporting
* Allure provides advanced execution reporting
* failure screenshots provide configurable browser evidence
* pytest-playwright provides optional trace and video artifact mechanisms
* GitHub Actions artifacts preserve CI runtime evidence
* CI validates code quality before browser execution
* CI provides dedicated Smoke and Regression feedback
* CI preserves complete full-suite regression validation
* CI uses explicit Phase 4E runtime defaults
* GitHub Actions job concurrency remains separate from Pytest worker concurrency
* generated runtime outputs remain separate from repository source content
* documentation describes implemented framework behavior

Future framework maturity work may improve:

* fixture organization
* lightweight logging
* failed-test diagnostics
* diagnostic quality and defaults

Possible future runtime expansion may include:

* named environment profiles
* additional execution environments
* broader browser execution strategy

Those capabilities should be introduced only through approved future scope.

Current implemented reporting and runtime configuration do not include:

* Allure history persistence
* report hosting
* GitHub Pages reporting
* retries
* cross-browser CI
* browser matrices
* device emulation
* automatic `.env` loading

Future API, cross-browser, Docker, Selenium, or Jenkins extensions remain separate from the current architecture.

## Architecture Principles

The framework should prioritize:

* readability
* maintainability
* deterministic execution
* test independence
* sequential and parallel execution compatibility
* explicit runtime configuration
* fail-fast invalid configuration behavior
* reporting compatibility with supported execution modes
* clear responsibility boundaries
* reusable components
* centralized test data
* centralized runtime settings
* traceability
* explicit marker semantics
* selective local validation
* dedicated Smoke and Regression CI feedback
* complete full-suite CI validation
* staged quality-gate execution
* clear separation of CI job concurrency and Pytest worker parallelism
* clear separation of execution configuration from test logic
* clear separation of execution from reporting
* clear separation of generated output from repository content
* incremental framework growth

The framework should avoid:

* unnecessary helper layers
* duplicated selectors
* duplicated test data
* duplicated runtime configuration logic
* hardcoded environment-specific application origins in tests or Page Objects
* shared test-state dependencies
* execution-order dependencies
* worker-specific test dependencies
* reporting-specific duplicate test implementations
* duplicate screenshot capture mechanisms
* custom trace/video recording when pytest-playwright already provides the required mechanism
* mixing detailed Checkout behavior into Cart ownership
* moving page-specific behavior into generic helpers prematurely
* moving authenticated shared behavior out of `AppPage`
* treating every Playwright test as automatically belonging to `ui`
* assigning Regression mechanically to every non-Smoke test
* treating CI job-level concurrency as Pytest parallel execution
* describing pytest-xdist as future-only functionality after Phase 4C
* describing Allure as unimplemented after Phase 4D
* describing runtime configuration as unimplemented after AQA-0100–AQA-0103
* describing Allure history or hosted reporting as implemented
* describing cross-browser CI as implemented
* describing environment profiles or `.env` loading as implemented
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
* centralized runtime configuration
* configurable application base URL
* runtime browser selection
* headed/headless configuration
* Playwright action/navigation timeout configuration
* Playwright assertion timeout configuration
* configurable failure screenshot policy
* configurable trace policy
* configurable video policy
* runtime configuration validation and normalization
* native pytest-playwright runtime option compatibility
* separate CI code-quality validation
* dedicated parallel Smoke CI execution
* dedicated parallel Regression CI execution
* parallel complete full-suite CI validation
* explicit CI runtime defaults
* Chromium-only CI execution
* pytest-html reporting
* Allure result collection
* Allure HTML generation
* failure screenshot capture
* Allure failure screenshot attachments
* optional Playwright trace generation
* optional Playwright video generation
* job-specific CI artifacts
* dedicated full-suite Allure artifact

Current CI architecture:

```text
Phase 4E runtime defaults
        ↓
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

Runtime configuration is implemented locally and integrated into the three browser-test CI jobs.

Current CI remains Chromium-only, headless by default, and uses explicit Phase 4E runtime defaults.

Trace and video are available as runtime policies but remain disabled by default.

No sequential-only test or reporting exceptions were identified for the current implemented execution model.

The `main` branch represents the stable portfolio version of the project.

The `develop` branch and active workstream branches may contain newer validated changes before promotion.

The current architecture direction remains Phase 4 Framework Maturity.

Phase 4B CI Execution Strategy, Phase 4C Parallel Execution Strategy, and Phase 4D Reporting Upgrade are implemented.

Phase 4E runtime configuration implementation through AQA-0100–AQA-0103 is integrated into `develop`.

Formal Phase 4E roadmap completion remains deferred to the dedicated Phase 4E checkpoint rather than being declared by this architecture document.