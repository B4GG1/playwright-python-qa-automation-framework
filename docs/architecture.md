# Architecture

This document describes the current architecture of the QA automation framework.

The project follows a lightweight, modular architecture focused on readability, maintainability, traceability, deterministic execution, test independence, configurable runtime behavior, diagnostic visibility, reporting visibility, representative browser-engine compatibility validation, and incremental framework growth.

The current architecture includes Page Object Model, shared authenticated-page behavior, reusable assertions, reusable pytest fixtures, centralized test data, centralized runtime configuration, lightweight runtime and failed-test diagnostics, explicit framework-hook and scenario-fixture responsibility boundaries, explicit marker-based test organization, sequential and pytest-xdist parallel execution, staged CI execution, pytest-html reporting, Allure reporting, configurable failure screenshots, optional Playwright trace and video generation, representative Firefox and WebKit Smoke validation, browser-specific CI reporting artifacts, GitHub Actions artifacts, and technical documentation.

Chromium remains the primary complete regression browser.

Firefox and WebKit provide representative Smoke compatibility validation through the existing functional test suite.

The architecture does not duplicate test ownership per browser engine and does not claim complete three-browser Regression or full-suite coverage.

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
* explicit separation of framework-level pytest integration from application scenario fixtures
* centralized login, product, and checkout test data
* centralized runtime configuration through `config/settings.py`
* environment-based application base URL configuration
* runtime browser selection
* support for Chromium, Firefox, and WebKit runtime browser values
* Chromium as the primary complete regression browser
* Firefox as a representative Smoke compatibility browser
* WebKit as a representative Smoke compatibility browser
* headed/headless execution configuration
* Playwright action and navigation timeout configuration
* Playwright assertion timeout configuration
* configurable screenshot policy
* configurable trace policy
* configurable video policy
* fail-fast runtime configuration validation
* lightweight runtime diagnostics
* effective runtime summary through `pytest_report_header`
* non-duplicated runtime summary under pytest-xdist worker execution
* failed-test diagnostic context for setup, call, and teardown failures
* failed-test node ID reporting
* failed-test phase reporting
* current page URL reporting when a Playwright page is available
* custom screenshot path reporting after successful screenshot capture
* diagnostic error reporting for page URL retrieval, screenshot creation, and Allure attachment failures
* project diagnostics formatting through `framework/diagnostics.py`
* explicit pytest marker categorization
* strict pytest marker validation
* marker-based selective local execution
* parallel local Smoke execution
* parallel local Regression execution
* parallel local full-suite execution
* local Firefox Smoke execution
* local WebKit Smoke execution
* dedicated Chromium Smoke CI execution
* dedicated Chromium Regression CI execution
* complete unfiltered Chromium full-suite CI execution
* dedicated Firefox/WebKit cross-browser Smoke matrix
* representative Firefox Smoke CI execution
* representative WebKit Smoke CI execution
* pytest-xdist execution inside all current browser-test CI executions
* explicit runtime defaults in browser-test CI jobs
* browser-specific Firefox and WebKit pytest-html reports
* browser-specific Firefox and WebKit GitHub Actions artifacts
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

Phase 5A changes execution coverage rather than product-facing test ownership.

The same Smoke scenarios covering Login, Inventory, Product Details, Cart, and Checkout are reused for representative Firefox and WebKit compatibility validation.

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
│ BasePage              │ root conftest.py        │
│ base URL composition  │ browser/runtime policy  │
└───────────────────────┴─────────────────────────┘
        ↓
Playwright / pytest-playwright execution
        ↓
Chromium / Firefox / WebKit
```

Browser execution responsibility is intentionally asymmetric:

```text
Chromium
├── Smoke
├── Regression
└── complete full suite

Firefox
└── representative Smoke

WebKit
└── representative Smoke
```

Pytest responsibility is separated between framework integration and application scenario setup:

```text
root conftest.py
framework-level pytest integration
        │
        ├── runtime configuration
        ├── browser selection integration
        ├── runtime diagnostics
        ├── BrowserContext timeout configuration
        ├── failed-test diagnostics
        └── screenshot / Allure failure integration

tests/conftest.py
application scenario fixtures
        │
        └── deterministic page and application state preparation
```

Reporting and diagnostics currently include:

```text
runtime summary
failed-test diagnostic context
pytest-html
browser-specific pytest-html
Allure
failure screenshots
optional Playwright traces
optional Playwright videos
GitHub Actions artifacts
```

The layers are intentionally lightweight.

New abstractions should be introduced only when repeated behavior or clear responsibility boundaries justify them.

Browser compatibility should reuse existing architecture by default rather than creating parallel browser-specific framework layers.

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
* remain compatible with supported browser-engine execution
* operate without embedding environment-specific runtime configuration
* remain browser-neutral unless a genuine engine limitation is demonstrated
* produce normal Pytest result data consumed by reporting and diagnostic integrations

Test modules should not duplicate selectors when Page Objects already expose the required interaction or state.

Test modules should not depend on state produced by another test because xdist workers may execute tests independently and in a different order from sequential execution.

Tests should not hardcode runtime configuration that belongs to `config/settings.py`.

Tests should not duplicate Firefox- or WebKit-specific versions of existing functional coverage merely to support cross-browser execution.

Reporting, diagnostic, and browser-execution integrations should not change test ownership or introduce execution-specific test implementations.

Phase 5A therefore reuses the same functional test modules on all currently validated browser engines.

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

Reporting and diagnostics concerns should not be moved into Page Objects.

Runtime browser ownership, timeout configuration, artifact policies, diagnostics, and environment-variable parsing should not be implemented independently inside Page Objects.

Browser-specific branches should not be introduced unless a genuine compatibility requirement is demonstrated.

Parallel execution, reporting, diagnostics, runtime configuration, and Phase 5A cross-browser execution do not change Page Object ownership or responsibility boundaries.

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

It should not become a generic container for unrelated framework helpers, reporting logic, diagnostic logic, browser lifecycle management, browser-specific conditionals, or runtime configuration parsing.

Phase 5A does not change `BasePage` responsibility.

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

The same authenticated behavior is reused during Chromium, Firefox, and WebKit execution.

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

Login behavior remains browser-neutral in the implemented architecture.

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

No Firefox- or WebKit-specific Inventory abstraction is required.

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

The same Page Object is reused across all current browser engines.

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

Cross-browser execution does not change this ownership boundary.

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
framework/diagnostics.py
```

### Reusable Assertion Responsibility

Current assertion responsibilities include:

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
* browser selection
* browser-specific conditional behavior without demonstrated need
* fixtures
* runtime configuration
* diagnostics
* reporting
* Page Object interactions

The same assertion helpers are reused during Chromium, Firefox, and WebKit execution.

### Diagnostic Responsibility

`framework/diagnostics.py` owns lightweight diagnostic formatting and the project diagnostics logger.

Current responsibilities include:

* runtime summary formatting
* failed-test summary formatting
* diagnostic error formatting
* project diagnostics logger definition
* diagnostic error logging

Runtime summary formatting supports effective values for:

* application base URL
* browser
* headed/headless mode
* Playwright action and navigation timeout
* Playwright assertion timeout
* screenshot policy
* trace policy
* video policy

Failed-test summary formatting supports:

* Pytest node ID
* failure phase
* current page URL when available
* custom screenshot path when available

Diagnostic errors identify:

* failed diagnostic operation
* Pytest node ID
* failure phase
* underlying exception information

The diagnostics module does not own:

* browser lifecycle
* browser selection
* Page Object behavior
* scenario setup
* screenshot lifecycle
* trace lifecycle
* video lifecycle
* Allure lifecycle
* persistent log files

Artifact ownership remains with the corresponding integration layer.

The same diagnostic formatting is used regardless of the selected Playwright browser engine.

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

Browser engine selection is runtime configuration and should not create separate browser-specific functional test data.

## Root `conftest.py`

The root `conftest.py` contains framework-level Pytest hooks and runtime integration.

Current responsibilities include:

* loading and applying centralized runtime settings
* applying configured browser selection to pytest-playwright when no explicit native browser option is provided
* applying configured headed mode
* preserving explicit native pytest-playwright browser options
* applying configured trace policy unless an explicit native tracing option was provided
* applying configured video policy unless an explicit native video option was provided
* configuring the Playwright assertion timeout
* emitting the effective runtime diagnostic header
* suppressing duplicate runtime headers from pytest-xdist workers
* creating browser contexts through pytest-playwright's existing `new_context` fixture
* applying default Playwright action timeout to created contexts
* applying default Playwright navigation timeout to created contexts
* processing failed Pytest reports
* collecting failed-test diagnostic context
* controlling the custom failure screenshot mechanism through screenshot policy
* attaching successfully captured custom screenshots to Allure
* reporting diagnostic-operation errors

Application scenario fixtures are not owned by the root `conftest.py`.

They are defined separately in `tests/conftest.py`.

The framework does not manually start or own Playwright browser processes.

Browser lifecycle remains based on the pytest-playwright fixture model.

The project-level `context` fixture extends the existing pytest-playwright `new_context` path only to apply approved runtime timeout configuration.

The same root integration supports Chromium, Firefox, and WebKit execution.

No browser-specific root fixture implementation was required for Phase 5A.

### Runtime Diagnostic Header

The root `conftest.py` uses:

```text
pytest_report_header
```

to emit one lightweight runtime summary before normal test execution output.

The summary represents effective runtime values for:

```text
base_url
browser
mode
action/navigation timeout
assertion timeout
screenshot policy
trace policy
video policy
```

Conceptually:

```text
[runtime] base_url=... | browser=... | mode=... | ...
```

Browser, headed mode, trace policy, and video policy reflect the effective pytest-playwright configuration after project settings and explicit native command-line options have been resolved.

The header therefore exposes whether the current execution uses:

```text
chromium
firefox
webkit
```

without requiring browser-specific diagnostic logic.

During pytest-xdist execution, worker processes do not emit duplicate runtime summaries.

The controlling Pytest process provides the execution-level runtime summary.

### Failed-Test Diagnostic Hook

The root Pytest report hook provides failed-test context for:

```text
setup
call
teardown
```

Every failed report receives at least:

* Pytest node ID
* failure phase

When the Playwright `page` fixture is available, the hook additionally attempts to report:

* current page URL

When the custom screenshot mechanism successfully creates a screenshot, the hook additionally reports:

* screenshot path

Conceptually:

```text
[failure] test=... | phase=... | url=... | screenshot=...
```

URL and screenshot fields remain optional.

This keeps failure diagnostics applicable to both browser and non-browser setup/teardown failures.

Browser engine selection does not change the diagnostic ownership model.

### Diagnostic Error Handling

Diagnostic collection can itself fail.

Current operations include:

```text
page-url
screenshot
allure-attachment
```

Diagnostic errors are formatted by `framework/diagnostics.py`, emitted through the project diagnostics logger, and added to the failed Pytest report's diagnostic sections.

Conceptually:

```text
[diagnostic-error] operation=... | test=... | phase=... | error=...
```

A diagnostic-operation failure does not create a persistent project log file.

Phase 4F uses lightweight runtime diagnostics rather than introducing a persistent logging subsystem.

Phase 5A does not change this design.

### Failure Screenshot And Allure Integration

Custom project screenshot ownership remains in the root failed-test integration.

When:

```text
QA_SCREENSHOT_POLICY=only-on-failure
```

and a failed test-call report has a Playwright `page` fixture, the hook creates a failure screenshot under:

```text
reports/screenshots/
```

Screenshot capture applies only to the failed `call` phase.

Setup-phase and teardown-phase failures still receive failed-test diagnostic context, but they do not trigger the custom project screenshot.

The screenshot filename contains:

* the test name
* a UTC timestamp

The existing screenshot mechanism remains the primary project-level screenshot capture mechanism.

Phase 4F and Phase 5A do not introduce a second screenshot implementation.

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

If screenshot capture fails, the diagnostic error is reported and no screenshot path is added because no screenshot file was created.

If Allure attachment fails after successful screenshot capture, the original screenshot remains available under `reports/screenshots/`, its path remains available in failed-test diagnostics, and the attachment error is reported separately.

This preserves failure evidence independently of the advanced reporting layer.

Firefox and WebKit Smoke execution reuse the same screenshot mechanism.

## `tests/conftest.py`

`tests/conftest.py` contains application scenario fixtures used by functional test modules.

Current fixtures include:

* `opened_login_page`
* `standard_user`
* `logged_in_inventory_page`
* `inventory_page_with_one_product_in_cart`
* `cart_page_with_one_product`
* `checkout_step_one_page_with_one_product`
* `checkout_step_two_page_with_one_product`
* `checkout_last_step_page_with_one_product`

These fixtures prepare explicit application states such as:

* opened Login
* authenticated Inventory
* Inventory with one product in Cart
* Cart with one product
* Checkout Information with one product
* Checkout Overview with one product
* Checkout Complete after finishing the prepared checkout flow

Fixture names remain explicit and scenario-oriented.

The current fixture architecture does not introduce:

* a generic fixture factory
* a dependency-injection layer
* an autouse fixture redesign
* a multi-layer fixture package
* fixture scope redesign

The current Playwright page/context flow and project scenario fixture chains remain function-scoped for test execution.

Fixture growth should follow real repeated setup needs rather than speculative abstraction.

Framework-level Pytest behavior remains in the root `conftest.py`.

Application scenario setup remains in `tests/conftest.py`.

This responsibility boundary reduces coupling between framework hooks and functional test preparation while preserving the existing fixture API consumed by tests.

Firefox and WebKit use the same scenario fixtures as Chromium.

No browser-specific application fixture layer is implemented.

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
* dedicated parallel Chromium Smoke CI execution
* dedicated parallel Chromium Regression CI execution
* parallel complete Chromium full-suite CI execution
* representative parallel Firefox Smoke CI execution
* representative parallel WebKit Smoke CI execution
* reporting compatibility
* diagnostic compatibility
* runtime-configuration compatibility
* browser-engine compatibility validation
* CI stability

Tests should not rely on shared browser state produced by earlier test cases.

Tests must also not assume:

* a specific xdist worker
* a specific test order
* a relationship between parametrized cases
* a specific Playwright engine beyond approved test intent
* a reporting system to prepare functional state
* a diagnostic system to prepare functional state
* a runtime configuration value hardcoded inside a test

No sequential-only test exceptions were identified during Phase 4C validation.

No browser-specific fixture or state-management exception was required during Phase 5A validation.

Phase 4D reporting, Phase 4E runtime configuration, Phase 4F diagnostics and fixture separation, and Phase 5A cross-browser Smoke execution do not change these independence requirements.

The separated root and test-level `conftest.py` responsibilities remain compatible with sequential, pytest-xdist, Chromium, Firefox, and WebKit Smoke execution.

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

The configuration layer recognizes all three Playwright browser engines used by the current execution strategy.

Default:

```text
chromium
```

Current browser responsibility:

```text
Chromium
    → Smoke
    → Regression
    → complete full suite

Firefox
    → representative Smoke

WebKit
    → representative Smoke
```

The same runtime configuration surface is used locally and in GitHub Actions.

Current Chromium CI jobs explicitly use:

```text
QA_BROWSER=chromium
```

The Phase 5A cross-browser matrix supplies:

```text
QA_BROWSER=${{ matrix.browser }}
```

which resolves to:

```text
firefox
```

or:

```text
webkit
```

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

All current CI browser execution remains headless.

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

The same timeout architecture applies to Chromium, Firefox, and WebKit.

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

The policy applies to current browser-test execution regardless of engine.

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

Current CI keeps both policies disabled for Chromium, Firefox, and WebKit execution.

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
* device emulation
* browser channels
* mobile emulation
* slow motion configuration
* retries

Cross-browser CI execution is implemented separately through the Phase 5A GitHub Actions matrix and consumes the existing `QA_BROWSER` setting.

The configuration architecture itself does not define:

* complete Firefox Regression execution
* complete WebKit Regression execution
* complete Firefox full-suite execution
* complete WebKit full-suite execution

Runtime diagnostics are a separate framework responsibility implemented through `framework/diagnostics.py` and root Pytest hooks rather than through additional configuration profiles.

Runtime configuration should remain focused on approved execution concerns rather than becoming a generic container for unrelated framework behavior.

## `reports/`

Stores generated reporting and failure-evidence runtime outputs.

Current usage includes:

* Chromium pytest-html reports
* Firefox Smoke pytest-html report
* WebKit Smoke pytest-html report
* failure screenshots
* Allure result data
* generated Allure HTML reports
* CI artifact source files

Current generated paths include:

```text
reports/smoke-report.html
reports/regression-report.html
reports/report.html
reports/firefox-smoke-report.html
reports/webkit-smoke-report.html
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

Phase 4F runtime and failed-test summaries do not introduce another persistent output directory.

Diagnostic summaries are lightweight Pytest runtime/report context rather than standalone log files.

### pytest-html Outputs

Current Chromium CI jobs generate:

```text
reports/smoke-report.html
reports/regression-report.html
reports/report.html
```

Current cross-browser Smoke CI generates:

```text
reports/firefox-smoke-report.html
reports/webkit-smoke-report.html
```

Chromium Smoke and Regression remain focused on pytest-html reporting.

Firefox and WebKit Smoke also use pytest-html reporting.

The Chromium full-suite job preserves pytest-html in addition to generating Allure data.

### Allure Result Data

Allure result collection writes structured execution data to:

```text
reports/allure-results/
```

This data is generated by `allure-pytest`.

It is runtime output rather than repository content.

The current CI Allure result responsibility remains with the Chromium `full-suite` job.

Firefox and WebKit Smoke do not generate dedicated Allure result sets.

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

The CI Allure HTML report remains part of the complete Chromium full-suite reporting path.

### Failure Screenshots

Failure screenshots are stored under:

```text
reports/screenshots/
```

when screenshot policy is enabled and a browser test fails during the Pytest call phase.

Screenshot filenames include the test name and UTC timestamp.

When Allure result collection is active, the same successfully captured file is reused as the Allure failure attachment.

The successfully created screenshot path is also available to the Phase 4F failed-test diagnostic summary.

Firefox and WebKit Smoke execution reuse the same screenshot architecture.

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

Phase 4F and Phase 5A do not take ownership of the trace or video lifecycle.

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

Phase 4D reporting, Phase 4E runtime configuration, Phase 4F diagnostics and fixture cleanup, and Phase 5A cross-browser execution do not introduce new product-facing test case automation.

Phase 5A reuses existing automated Smoke scenarios on additional browser engines and therefore does not require browser-specific test case files or automation metadata updates.

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
* diagnostics strategy
* fixture responsibility boundaries
* reporting strategy
* cross-browser execution strategy
* CI/CD
* quality tooling
* technology stack
* features
* roadmap

Documentation should reflect current implemented behavior and clearly separate it from unimplemented functionality.

Runtime configuration documentation should distinguish:

* supported environment variables
* approved defaults
* accepted values
* normalization and validation behavior
* local overrides
* native pytest-playwright CLI behavior
* local capabilities from CI responsibilities

Reporting and diagnostic documentation should distinguish:

* runtime diagnostic responsibilities
* failed-test diagnostic responsibilities
* pytest-html responsibilities
* Allure responsibilities
* custom failure screenshot responsibilities
* Playwright trace and video responsibilities
* GitHub Actions artifact responsibilities
* generated runtime output from repository content
* lightweight diagnostics from persistent logging

Cross-browser documentation should distinguish:

* Chromium complete regression responsibility
* Firefox representative Smoke responsibility
* WebKit representative Smoke responsibility
* browser runtime selection from marker semantics
* representative compatibility validation from complete multi-browser regression coverage

Fixture documentation should distinguish:

* root framework-level Pytest integration
* application scenario fixtures under `tests/conftest.py`

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
Chromium / representative cross-browser execution
        ↓
Diagnostics / reporting
        ↓
CI execution
```

Runtime configuration and framework diagnostics are applied outside the Login test module and therefore do not change Login test ownership or test design.

Depending on marker assignment, Login tests may participate in:

* dedicated parallel Chromium Smoke CI execution
* dedicated parallel Chromium Regression CI execution
* parallel complete Chromium full-suite CI execution
* representative Firefox Smoke CI execution when carrying `smoke`
* representative WebKit Smoke CI execution when carrying `smoke`
* complete Chromium full-suite Allure reporting

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

Representative Login Smoke scenarios are reused across the supported browser engines.

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
Chromium / representative cross-browser execution
        ↓
Diagnostics / reporting
        ↓
CI execution
```

Depending on marker assignment, Inventory tests may participate in:

* dedicated parallel Chromium Smoke CI execution
* dedicated parallel Chromium Regression CI execution
* parallel complete Chromium full-suite CI execution
* representative Firefox Smoke CI execution when carrying `smoke`
* representative WebKit Smoke CI execution when carrying `smoke`
* complete Chromium full-suite Allure reporting

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

Application scenario fixtures used by Inventory tests are provided through `tests/conftest.py`.

Representative Inventory Smoke scenarios remain browser-neutral.

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
Chromium / representative cross-browser execution
        ↓
Diagnostics / reporting
        ↓
CI execution
```

Depending on marker assignment, Product Details tests may participate in:

* dedicated parallel Chromium Smoke CI execution
* dedicated parallel Chromium Regression CI execution
* parallel complete Chromium full-suite CI execution
* representative Firefox Smoke CI execution when carrying `smoke`
* representative WebKit Smoke CI execution when carrying `smoke`
* complete Chromium full-suite Allure reporting

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

Phase 5A does not introduce separate Product Details test modules per browser.

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
Chromium / representative cross-browser execution
        ↓
Diagnostics / reporting
        ↓
CI execution
```

Depending on marker assignment, Cart tests may participate in:

* dedicated parallel Chromium Smoke CI execution
* dedicated parallel Chromium Regression CI execution
* parallel complete Chromium full-suite CI execution
* representative Firefox Smoke CI execution when carrying `smoke`
* representative WebKit Smoke CI execution when carrying `smoke`
* complete Chromium full-suite Allure reporting

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

Cart test state is prepared independently per test through application scenario fixtures under `tests/conftest.py` and was validated under xdist execution.

The same representative Smoke scenarios are reused for Firefox and WebKit compatibility validation.

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
Chromium / representative cross-browser execution
        ↓
Diagnostics / reporting
        ↓
CI execution
```

Depending on marker assignment, Checkout tests may participate in:

* dedicated parallel Chromium Smoke CI execution
* dedicated parallel Chromium Regression CI execution
* parallel complete Chromium full-suite CI execution
* representative Firefox Smoke CI execution when carrying `smoke`
* representative WebKit Smoke CI execution when carrying `smoke`
* complete Chromium full-suite Allure reporting

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

Checkout fixture chains prepare their required Cart and checkout state independently through `tests/conftest.py` and were validated under worker-level parallel execution.

Representative Checkout Smoke checkpoints are reused in Firefox and WebKit validation without browser-specific Checkout ownership.

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

Phase 5A does not introduce a cross-browser marker.

Browser engine selection and marker assignment are separate architectural concerns.

The existing `smoke` marker defines the representative suite reused by Firefox and WebKit.

### Marker Execution Responsibilities

All executable markers remain available for selective local execution.

Dedicated Chromium marker-filtered CI jobs currently exist for:

* `smoke`
* `regression`

The existing `smoke` suite additionally executes through the Phase 5A cross-browser matrix on:

* Firefox
* WebKit

Dedicated CI jobs do not currently exist for:

* `ui`
* `security`
* `sorting`
* `navigation`
* `e2e`

Tests carrying those markers are still included in complete Chromium full-suite CI execution.

Tests that also carry `smoke` additionally participate in representative Firefox and WebKit validation.

Dedicated CI execution, browser selection, diagnostics, reporting, runtime configuration, and marker semantics are separate concerns:

* markers define test intent and selectable suites
* runtime configuration defines execution settings
* `QA_BROWSER` selects the Playwright engine
* CI determines which marker expressions receive dedicated workflow jobs
* the Phase 5A matrix determines the additional browser engines used for Smoke
* xdist determines how collected tests are distributed between workers
* diagnostics provide runtime and failed-test context
* reporting integrations consume results from the resulting execution

Parallel execution, cross-browser execution, diagnostics, reporting, and runtime configuration do not change marker semantics or marker assignment.

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

Each E2E test prepares its own required state through scenario fixtures or local setup.

This allows:

```bash
pytest -m e2e -v
```

to execute a logical purchase-journey checkpoint suite while keeping individual tests isolated.

This independent checkpoint model also makes the E2E tests compatible with xdist execution as part of the parallel full suite.

E2E does not currently have a dedicated GitHub Actions job.

E2E tests remain part of the complete unfiltered Chromium full-suite CI execution and may therefore be distributed between xdist workers.

E2E checkpoints that also carry the `smoke` marker participate in representative Firefox and WebKit compatibility validation.

When Chromium full-suite Allure result collection is enabled, E2E checkpoints are represented as normal results within the advanced full-suite report.

Runtime environment overrides and Phase 4F diagnostics apply to E2E execution in the same way as to other Pytest suites.

## Reporting And Diagnostic Architecture

The reporting and diagnostic architecture uses complementary mechanisms with different responsibilities.

Runtime diagnostics provide execution context without creating persistent log files:

```text
Pytest startup
      ↓
pytest_report_header
      ↓
effective runtime values
      ↓
[runtime] summary
```

Under pytest-xdist:

```text
controller process
      ↓
[runtime] summary

worker processes
      ↓
no duplicate runtime summary
```

Failed-test diagnostics provide contextual information for each failed report:

```text
failed Pytest report
setup / call / teardown
      ↓
root pytest_runtest_makereport
      ↓
┌──────────────────────────────┐
│ node ID                      │
│ failure phase                │
│ current URL when available   │
│ screenshot path when created │
└──────────────────────────────┘
      ↓
[failure] summary
```

Diagnostic-operation errors follow:

```text
diagnostic operation failure
      ↓
framework/diagnostics.py
      ↓
project diagnostics logger
      +
Pytest failure diagnostics section
```

Traditional reporting remains complementary:

```text
Pytest execution
      ↓
┌──────────────────────────────┐
│ pytest-html                  │
│ lightweight HTML reporting   │
└──────────────────────────────┘

Chromium full-suite execution
      ↓
┌──────────────────────────────┐
│ allure-pytest                │
│ structured Allure results    │
└──────────────────────────────┘
      ↓
Allure CLI
      ↓
generated Allure HTML report
```

Custom screenshot evidence follows:

```text
failed browser test call
      ↓
QA_SCREENSHOT_POLICY
      ↓
root failure hook
      ↓
reports/screenshots/*.png
      ↓
same PNG attached to Allure
when Allure collection is active
      +
screenshot path added to failure diagnostics
```

Trace and video remain pytest-playwright-owned:

```text
pytest-playwright execution
      ↓
QA_TRACE_POLICY / QA_VIDEO_POLICY
      ↓
optional trace.zip / video.webm
      ↓
test-results/
```

Cross-browser reporting follows:

```text
Firefox Smoke
      ↓
reports/firefox-smoke-report.html
      ↓
Firefox-specific GitHub Actions artifacts

WebKit Smoke
      ↓
reports/webkit-smoke-report.html
      ↓
WebKit-specific GitHub Actions artifacts
```

### Runtime Diagnostic Responsibility

The runtime diagnostic header communicates effective values for:

* base URL
* browser
* headed/headless mode
* action/navigation timeout
* assertion timeout
* screenshot policy
* trace policy
* video policy

It is designed for immediate execution visibility rather than persistent historical logging.

The header is compatible with:

* Chromium
* Firefox
* WebKit
* sequential execution
* pytest-xdist execution

Pytest-xdist workers do not duplicate the header.

### Failed-Test Diagnostic Responsibility

Failed-test diagnostics identify:

* Pytest node ID
* setup, call, or teardown failure phase

When the Playwright page is available, diagnostics also attempt to identify:

* current URL

When a custom project screenshot is successfully created, diagnostics identify:

* screenshot path

The diagnostic summary therefore remains useful even for setup or teardown failures where screenshot capture is intentionally not performed.

The same diagnostic responsibility applies to all current browser engines.

### Diagnostic Error Responsibility

Diagnostic errors are explicitly reported for:

* page URL retrieval
* screenshot creation
* Allure attachment

The project diagnostics logger is lightweight.

Phase 4F does not configure or write persistent project log files.

Diagnostic errors are also attached to the failed Pytest report as diagnostic sections so that a diagnostic failure is visible together with the test failure context.

### pytest-html Responsibility

pytest-html remains the lightweight reporting layer.

It is used in:

* Chromium Smoke CI
* Chromium Regression CI
* Chromium full-suite CI
* Firefox Smoke CI
* WebKit Smoke CI

Current Chromium paths:

```text
reports/smoke-report.html
reports/regression-report.html
reports/report.html
```

Current Firefox/WebKit paths:

```text
reports/firefox-smoke-report.html
reports/webkit-smoke-report.html
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

The current CI responsibility for Allure result collection remains the complete Chromium `full-suite` job.

Firefox and WebKit Smoke do not currently have independent Allure result-collection responsibility.

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

The CI Allure CLI is used only by the Chromium full-suite job.

### Failure Evidence Responsibility

Failure screenshots remain independent runtime evidence.

Current screenshot location:

```text
reports/screenshots/
```

The same successfully captured PNG may additionally be embedded in Allure when Allure result collection is active.

This avoids duplicate screenshot capture logic while providing richer report context.

Screenshot generation can be disabled through:

```text
QA_SCREENSHOT_POLICY=off
```

When disabled, both the project screenshot and its corresponding Allure failure screenshot attachment are disabled.

Firefox and WebKit Smoke use the same failure-evidence mechanism.

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

Phase 5A does not introduce separate trace/video architecture per browser.

### Reporting And Diagnostic Scope Boundaries

Current reporting and diagnostic architecture does not include:

* persistent project log files
* browser console capture
* network capture
* custom network tracing outside existing Playwright trace support
* HTML or page-source dumps
* automatic trace enablement
* automatic video enablement
* Allure history persistence
* trend-history storage
* hosted Allure reports
* GitHub Pages report publishing
* retry architecture
* Firefox-specific Allure reporting in CI
* WebKit-specific Allure reporting in CI
* complete three-browser full-suite reporting
* new CI topology for diagnostics

Trace and video policies are implemented, but remain disabled by default.

Browser-specific pytest-html reporting for Firefox and WebKit is implemented.

## Local And CI Execution Architecture

Local execution supports:

* sequential full-suite validation
* parallel full-suite validation
* selective marker-based validation
* parallel Chromium Smoke validation
* parallel Chromium Regression validation
* local Firefox Smoke validation
* local WebKit Smoke validation
* local Allure result generation
* local Allure HTML report generation
* environment-based runtime overrides
* lightweight runtime diagnostics
* failed-test diagnostic context
* optional screenshot, trace, and video policy overrides

Sequential full local execution:

```bash
pytest -v
```

Parallel full local Chromium execution:

```bash
pytest -n auto -v
```

Approved Chromium parallel marker execution:

```bash
pytest -m smoke -n auto -v
pytest -m regression -n auto -v
```

Approved representative cross-browser execution:

```bash
QA_BROWSER=firefox pytest -m smoke -n auto -v
QA_BROWSER=webkit pytest -m smoke -n auto -v
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

Cross-browser Smoke validation is an additional compatibility layer rather than a replacement for Chromium complete regression validation.

Diagnostics, reporting, runtime configuration, and browser selection are layered on top of execution rather than defining separate functional test implementations.

### Phase 4B CI Architecture

Phase 4B established separation of code-quality validation from browser-test execution.

The Phase 4B job structure at the time of implementation was:

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

The quality job does not install Playwright browsers.

Smoke, Regression, and full-suite declare:

```yaml
needs: quality
```

After successful quality validation, the three browser jobs are independently executable and do not depend on each other.

That structure remains the Chromium foundation of the current pipeline.

Phase 5A later adds a separate Firefox/WebKit matrix without replacing the existing Chromium jobs.

### Phase 4C Worker-Level Execution

Phase 4C enables pytest-xdist worker-level parallelism inside the existing Chromium browser-test jobs.

The Phase 4C architecture was:

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

Phase 5A later reuses the same xdist model inside Firefox and WebKit Smoke matrix executions.

### Phase 4D Reporting Layer

Phase 4D adds reporting inside the existing Phase 4 execution architecture.

The Phase 4D reporting model was:

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

Phase 4D did not add another browser job.

Phase 5A later adds browser-specific pytest-html reporting for representative Firefox and WebKit Smoke execution while preserving the Chromium full-suite Allure responsibility.

### Phase 4E Runtime Configuration Layer

Phase 4E adds environment-based runtime configuration without changing the established Phase 4 test-suite or CI topology.

Conceptually:

```text
environment variables
        ↓
config/settings.py
        ↓
root conftest.py / BasePage
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

The Phase 4 browser CI jobs use explicit defaults:

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

Phase 4E did not introduce:

* another browser job
* a browser matrix
* Firefox CI installation
* WebKit CI installation
* cross-browser CI execution
* retries
* `continue-on-error`
* trace or video retention by default

Those statements describe the Phase 4E implementation boundary.

Phase 5A later consumes the `QA_BROWSER` capability implemented in Phase 4E.

### Phase 4F Diagnostics And Fixture Responsibility Layer

Phase 4F adds lightweight diagnostics and separates framework-level Pytest responsibilities from application scenario fixtures.

Conceptually:

```text
config/settings.py
        ↓
root conftest.py
├── runtime integration
├── runtime diagnostic header
├── BrowserContext timeout configuration
├── failed-test diagnostics
└── screenshot / Allure failure integration

framework/diagnostics.py
├── runtime summary formatting
├── failure summary formatting
├── diagnostic error formatting
└── diagnostics logger

tests/conftest.py
└── application scenario fixtures
```

Phase 4F diagnostics provide:

* one effective runtime summary
* xdist worker-header suppression
* failed-test node ID
* failed-test setup/call/teardown phase
* current URL when a page is available
* screenshot path after successful custom screenshot capture
* diagnostic error reporting for URL retrieval, screenshot creation, and Allure attachment

Phase 4F fixture cleanup preserves existing explicit scenario fixture names and their functional behavior while moving them out of the framework-level root `conftest.py`.

Phase 4F does not change:

* Pytest marker semantics
* test ownership
* Page Object ownership
* runtime configuration variables
* fixture scopes
* browser lifecycle ownership
* pytest-playwright trace lifecycle
* pytest-playwright video lifecycle
* custom screenshot policy semantics

The Phase 4F architecture remains compatible with sequential and pytest-xdist execution.

Phase 5A later reuses the same diagnostics and fixture responsibility model for Firefox and WebKit Smoke execution.

### Phase 5A Cross-Browser Execution Layer

Phase 5A extends the mature Chromium execution model with representative browser-engine compatibility validation.

Current architecture:

```text
quality
├── smoke [Chromium]
│   └── xdist workers
│       └── pytest-html
├── regression [Chromium]
│   └── xdist workers
│       └── pytest-html
├── full-suite [Chromium]
│   └── xdist workers
│       ├── pytest-html
│       ├── Allure results
│       ├── failure screenshots
│       └── Allure HTML report
└── cross-browser-smoke
    ├── Firefox
    │   └── xdist workers
    │       └── browser-specific pytest-html
    └── WebKit
        └── xdist workers
            └── browser-specific pytest-html
```

The matrix is limited to:

```text
firefox
webkit
```

Chromium is not duplicated in the matrix because it already has dedicated Smoke, Regression, and full-suite execution.

The cross-browser job:

* depends on `quality`
* uses `fail-fast: false`
* supplies `QA_BROWSER` from `matrix.browser`
* installs only the selected browser engine
* runs headless
* executes the existing Smoke suite
* uses pytest-xdist with `-n auto`
* reuses existing Page Objects
* reuses existing fixtures
* reuses existing assertions
* reuses Phase 4F diagnostics
* generates a browser-specific pytest-html report
* publishes browser-specific GitHub Actions artifacts

Phase 5A does not introduce:

* a new marker
* duplicate browser-specific functional tests
* duplicate Page Object hierarchies
* Firefox-specific fixtures
* WebKit-specific fixtures
* complete Firefox Regression
* complete WebKit Regression
* complete Firefox full-suite execution
* complete WebKit full-suite execution
* Selenium
* browser-specific conditional logic without a demonstrated limitation

### Smoke CI Execution

The dedicated `smoke` job is the Chromium Smoke execution path.

Smoke executes:

```bash
pytest -m smoke -n auto -v
```

The actual CI command also generates:

```text
reports/smoke-report.html
```

Chromium Smoke remains pytest-html-focused and does not generate a dedicated Allure report.

The Phase 4F runtime header and failure diagnostics are available through the normal Pytest execution path without requiring another CI job.

### Regression CI Execution

The dedicated `regression` job is the Chromium Regression execution path.

Regression executes:

```bash
pytest -m regression -n auto -v
```

The actual CI command also generates:

```text
reports/regression-report.html
```

Chromium Regression remains pytest-html-focused and does not generate a dedicated Allure report.

The Phase 4F runtime header and failure diagnostics are available through the normal Pytest execution path without requiring another CI job.

### Full-Suite CI Execution

The `full-suite` job is the complete Chromium regression gate.

It executes the complete unfiltered Pytest suite:

```bash
pytest -n auto -v \
  --html=reports/report.html \
  --self-contained-html \
  --alluredir=reports/allure-results \
  --clean-alluredir
```

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

Chromium Smoke and Regression provide dedicated targeted feedback without replacing complete full-suite execution.

Firefox and WebKit Smoke provide representative compatibility feedback without replacing Chromium complete regression responsibility.

Phase 4F diagnostics operate within the same full-suite execution and do not introduce another reporting or browser job.

### Browser Execution

Current Playwright browser installation responsibility is:

```text
smoke [Chromium]
    → playwright install --with-deps chromium

regression [Chromium]
    → playwright install --with-deps chromium

full-suite [Chromium]
    → playwright install --with-deps chromium

cross-browser-smoke [Firefox]
    → playwright install --with-deps firefox

cross-browser-smoke [WebKit]
    → playwright install --with-deps webkit
```

The `quality` job does not prepare a browser environment.

The runtime configuration parser recognizes:

```text
chromium
firefox
webkit
```

and all three engines are now used by the implemented execution strategy.

Browser responsibility remains intentionally asymmetric:

```text
Chromium
    → complete regression responsibility

Firefox
    → representative Smoke compatibility

WebKit
    → representative Smoke compatibility
```

No complete three-browser Regression or full-suite architecture is currently implemented.

## CI Artifact Architecture

Each browser execution uses non-conflicting GitHub Actions artifact names.

### Smoke

Chromium Smoke artifacts:

```text
smoke-pytest-html-report
smoke-test-artifacts
```

HTML report:

```text
reports/smoke-report.html
```

### Regression

Chromium Regression artifacts:

```text
regression-pytest-html-report
regression-test-artifacts
```

HTML report:

```text
reports/regression-report.html
```

### Full Suite

Chromium full-suite artifacts:

```text
pytest-html-report
full-suite-allure-report
test-artifacts
```

The dedicated Allure artifact publishes:

```text
reports/allure-report/
```

The broader full-suite artifact continues to publish:

```text
reports/
```

### Cross-Browser Smoke

Firefox artifacts:

```text
firefox-smoke-pytest-html-report
firefox-smoke-test-artifacts
```

Firefox HTML report:

```text
reports/firefox-smoke-report.html
```

WebKit artifacts:

```text
webkit-smoke-pytest-html-report
webkit-smoke-test-artifacts
```

WebKit HTML report:

```text
reports/webkit-smoke-report.html
```

The browser-specific artifact names prevent matrix-output collisions.

Firefox and WebKit broader runtime artifacts each publish their own:

```text
reports/
```

directory from the corresponding isolated matrix runner.

Artifact uploads use:

```yaml
if: always()
```

so available runtime evidence can still be published when an executing browser-test command fails.

The Chromium Allure report-generation step also checks whether usable result data exists before calling the Allure CLI.

Therefore a failed browser-test run may still produce relevant available evidence such as:

* pytest-html output
* failure screenshots when screenshot policy allows them
* downloadable artifacts
* Phase 4F failed-test diagnostic context

A failed Chromium full-suite run may additionally produce:

* Allure result data
* generated Allure HTML

The failed test command still fails its corresponding job.

Reporting and diagnostics do not change the quality-gate result.

Current artifact retention remains:

```text
7 days
```

Trace and video remain disabled in CI by default and therefore are not introduced as default retained CI artifacts.

Phase 4F does not introduce persistent diagnostic log files or another diagnostic artifact package.

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

Current parallel browser-test execution includes:

* Chromium Smoke
* Chromium Regression
* Chromium complete full suite
* Firefox representative Smoke
* WebKit representative Smoke

### Parallel-Safety Model

The current architecture relies on test independence rather than worker-specific coordination.

Parallel-safe expectations include:

* function-scoped browser/test setup
* function-scoped application scenario fixture chains
* no dependence on test order
* no browser state shared between tests
* no state handoff between E2E checkpoints
* no dependency between parametrized cases
* deterministic setup through fixtures or test-local preparation
* no assumption about which worker executes a given test
* runtime configuration treated as process-level execution configuration rather than shared test state
* framework diagnostics treated as execution context rather than functional test state
* no browser-specific shared state
* browser engine selection treated as execution configuration rather than test-state ownership

Cart, Checkout, logout/re-login persistence, E2E checkpoints, and parametrized all-product scenarios were validated under worker-level execution.

The Phase 4F fixture responsibility separation was also validated with pytest-xdist execution.

Phase 5A Firefox and WebKit Smoke execution was validated using the same worker-level model.

No sequential-only execution exception is required for the current suite.

No browser-specific parallel-execution exception is required.

### Diagnostics Under Parallel Execution

Phase 4F diagnostics are designed for the same worker-level execution model.

The runtime summary is emitted by the controlling Pytest process and suppressed on xdist workers.

This prevents the runtime header from being repeated once per worker.

Failed-test diagnostics remain associated with the corresponding failed report and identify the affected test through its node ID and phase.

The diagnostic architecture does not require worker-specific persistent state or cross-worker coordination.

The same behavior applies to Chromium, Firefox, and WebKit execution.

### Reporting Under Parallel Execution

The reporting architecture is designed to operate with the same worker-level execution model.

Validated reporting behavior includes:

* pytest-html generation during Chromium xdist execution
* browser-specific pytest-html generation during Firefox Smoke xdist execution
* browser-specific pytest-html generation during WebKit Smoke xdist execution
* Allure result collection during Chromium full-suite xdist execution
* failure screenshot generation during xdist execution
* reuse of failure screenshots as Allure attachments where Allure collection is active
* generated Allure HTML reports based on Chromium full-suite results
* Phase 4F failure diagnostics alongside the existing reporting path

No separate sequential-only reporting or diagnostic architecture is maintained.

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

Browser selection is independent of the sequential/parallel distinction.

The same runtime configuration, diagnostics, fixtures, Page Objects, assertions, and reporting components can be applied across supported execution modes where appropriate.

## CI Execution Boundaries

The current execution architecture combines Phase 4B, Phase 4C, Phase 4D, Phase 4E, Phase 4F, and Phase 5A capabilities.

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
* Chromium-only CI execution for the Phase 4E workstream
* preservation of the Phase 4 CI topology

Phase 4F includes:

* lightweight runtime diagnostics
* effective runtime summary through `pytest_report_header`
* pytest-xdist worker-header suppression
* failed-test node ID diagnostics
* setup/call/teardown failure-phase diagnostics
* current page URL diagnostics when a page is available
* custom screenshot path diagnostics after successful screenshot capture
* diagnostic error reporting for page URL retrieval
* diagnostic error reporting for screenshot creation
* diagnostic error reporting for Allure attachment
* shared diagnostic formatting through `framework/diagnostics.py`
* project diagnostics logger without persistent log files
* separation of framework-level root `conftest.py` responsibilities
* application scenario fixtures under `tests/conftest.py`
* preservation of existing explicit scenario fixture names
* preservation of existing fixture scopes
* preservation of pytest-playwright trace and video ownership
* preservation of the Phase 4 CI topology
* validated sequential execution compatibility
* validated pytest-xdist execution compatibility

Phase 5A includes:

* Chromium retained as the primary complete regression browser
* preservation of Chromium Smoke
* preservation of Chromium Regression
* preservation of Chromium complete full-suite execution
* local Firefox Smoke validation
* local WebKit Smoke validation
* dedicated Firefox/WebKit `cross-browser-smoke` matrix
* `needs: quality`
* `fail-fast: false`
* `QA_BROWSER` supplied from the matrix value
* selected-engine-only browser installation
* reuse of the existing `smoke` marker
* reuse of existing functional tests
* reuse of existing fixtures
* reuse of existing Page Objects
* reuse of existing assertions
* pytest-xdist execution through `-n auto`
* browser-specific Firefox pytest-html reporting
* browser-specific WebKit pytest-html reporting
* independent browser-specific artifacts
* preservation of Chromium full-suite Allure ownership
* preservation of Phase 4F diagnostics
* preservation of failure screenshot behavior

GitHub Actions job-level concurrency, GitHub Actions matrix expansion, and pytest-xdist worker-level parallelism remain distinct architectural layers.

Reporting is a separate concern layered on top of test execution.

Runtime configuration is another separate concern and does not redefine test ownership, marker semantics, reporting ownership, or diagnostic ownership.

Browser selection is an execution concern and does not create separate functional test ownership.

Diagnostics provide execution context and failure information without redefining functional test behavior.

The current architecture does not implement:

* named environment profiles
* automatic `.env` loading
* complete Firefox Regression
* complete WebKit Regression
* complete Firefox full-suite execution
* complete WebKit full-suite execution
* complete three-browser regression parity
* device emulation
* retries
* persistent diagnostic log files
* browser console capture
* network capture
* HTML or page-source dumps
* custom trace or video lifecycle
* Selenium execution

## Design Direction

The framework follows a modular architecture where:

* tests describe behavior and expectations
* Page Objects handle interactions
* `BasePage` owns minimal common page behavior and runtime base URL composition
* `AppPage` owns shared authenticated behavior
* assertion helpers own reusable validation logic
* test data remains externalized
* `config/settings.py` owns approved runtime configuration parsing, defaults, normalization, and validation
* root `conftest.py` bridges approved runtime settings into pytest-playwright execution
* root `conftest.py` owns framework-level runtime diagnostics and failure integration
* `framework/diagnostics.py` owns shared diagnostic formatting and the project diagnostics logger
* `tests/conftest.py` owns application scenario fixtures
* fixtures prepare deterministic reusable state
* tests remain independent across sequential and parallel execution
* tests remain browser-neutral unless a genuine limitation is demonstrated
* manual test cases define documented scenario coverage
* markers organize selective test suites
* pytest-xdist provides worker-level parallel execution
* pytest-html provides lightweight reporting
* Allure provides advanced Chromium full-suite execution reporting
* failure screenshots provide configurable browser evidence
* pytest-playwright provides optional trace and video artifact mechanisms
* GitHub Actions artifacts preserve CI runtime evidence
* CI validates code quality before browser execution
* CI provides dedicated Chromium Smoke and Regression feedback
* CI preserves complete Chromium full-suite regression validation
* CI provides representative Firefox and WebKit Smoke compatibility validation
* CI uses explicit runtime defaults
* lightweight Phase 4F diagnostics provide runtime and failure context without persistent log files
* GitHub Actions job concurrency remains separate from Pytest worker concurrency
* GitHub Actions matrix expansion remains separate from Pytest worker concurrency
* generated runtime outputs remain separate from repository source content
* documentation describes implemented framework behavior

Possible future runtime expansion may include:

* named environment profiles
* additional execution environments
* complete additional-browser Regression execution if future scope justifies it
* complete additional-browser full-suite execution if future scope justifies it

Possible future diagnostic expansion should be introduced only through separately approved scope.

Current implemented reporting, diagnostics, runtime configuration, and browser strategy do not include:

* Allure history persistence
* report hosting
* GitHub Pages reporting
* retries
* complete Firefox Regression
* complete WebKit Regression
* complete Firefox full-suite execution
* complete WebKit full-suite execution
* device emulation
* automatic `.env` loading
* persistent log files
* browser console capture
* network capture
* HTML or page-source dumps
* custom trace or video lifecycle
* Selenium

Future API, Docker, Selenium, or Jenkins extensions remain separate from the current architecture.

## Architecture Principles

The framework should prioritize:

* readability
* maintainability
* deterministic execution
* test independence
* sequential and parallel execution compatibility
* browser-engine-neutral test behavior where practical
* explicit runtime configuration
* fail-fast invalid configuration behavior
* lightweight runtime diagnostics
* useful failed-test context
* diagnostic compatibility with supported execution modes
* reporting compatibility with supported execution modes
* representative browser-engine compatibility validation
* clear responsibility boundaries
* explicit separation of framework hooks from application scenario fixtures
* reusable components
* centralized test data
* centralized runtime settings
* traceability
* explicit marker semantics
* selective local validation
* dedicated Chromium Smoke and Regression CI feedback
* complete Chromium full-suite CI validation
* representative Firefox and WebKit Smoke CI validation
* staged quality-gate execution
* clear separation of CI job concurrency and Pytest worker parallelism
* clear separation of matrix expansion and Pytest worker parallelism
* clear separation of browser selection from test semantics
* clear separation of execution configuration from test logic
* clear separation of diagnostics from functional test logic
* clear separation of execution from reporting
* clear separation of generated output from repository content
* preservation of native pytest-playwright artifact ownership
* incremental framework growth

The framework should avoid:

* unnecessary helper layers
* duplicated selectors
* duplicated test data
* duplicated runtime configuration logic
* duplicated diagnostic formatting
* duplicated browser-specific functional tests
* duplicated browser-specific Page Object hierarchies
* hardcoded environment-specific application origins in tests or Page Objects
* browser-specific conditional logic without demonstrated need
* shared test-state dependencies
* execution-order dependencies
* worker-specific test dependencies
* worker-duplicated runtime summaries
* reporting-specific duplicate test implementations
* diagnostic-specific duplicate test implementations
* duplicate screenshot capture mechanisms
* custom trace/video recording when pytest-playwright already provides the required mechanism
* persistent logging without approved scope
* placing application scenario fixtures in the framework-level root `conftest.py`
* moving framework-level Pytest hooks into application scenario fixture modules
* mixing detailed Checkout behavior into Cart ownership
* moving page-specific behavior into generic helpers prematurely
* moving authenticated shared behavior out of `AppPage`
* treating every Playwright test as automatically belonging to `ui`
* assigning Regression mechanically to every non-Smoke test
* creating a cross-browser marker solely for browser execution
* treating browser selection as functional test categorization
* treating representative cross-browser Smoke as complete three-browser regression
* treating CI job-level concurrency as Pytest parallel execution
* treating GitHub Actions matrix expansion as Pytest parallel execution
* describing pytest-xdist as future-only functionality after Phase 4C
* describing Allure as unimplemented after Phase 4D
* describing Phase 4E runtime configuration as incomplete
* describing Phase 4F diagnostics or fixture separation as future-only functionality
* describing Phase 5A representative cross-browser Smoke validation as future-only functionality
* describing Allure history or hosted reporting as implemented
* describing persistent diagnostic logs as implemented
* describing browser console or network capture as implemented
* describing complete Firefox/WebKit Regression or full-suite execution as implemented
* describing environment profiles or `.env` loading as implemented
* describing Selenium as implemented
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
* reusable application scenario fixtures
* separated framework-level and scenario-level fixture responsibilities
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
* local Firefox Smoke validation
* local WebKit Smoke validation
* centralized runtime configuration
* configurable application base URL
* runtime Chromium/Firefox/WebKit browser selection
* headed/headless configuration
* Playwright action/navigation timeout configuration
* Playwright assertion timeout configuration
* configurable failure screenshot policy
* configurable trace policy
* configurable video policy
* runtime configuration validation and normalization
* native pytest-playwright runtime option compatibility
* lightweight runtime diagnostic header
* effective runtime value visibility
* non-duplicated runtime summary under pytest-xdist
* failed-test node ID diagnostics
* setup/call/teardown failure-phase diagnostics
* current URL diagnostics when a Playwright page is available
* custom screenshot path diagnostics
* diagnostic error reporting
* shared diagnostic formatting through `framework/diagnostics.py`
* lightweight project diagnostics logger
* separate CI code-quality validation
* dedicated parallel Chromium Smoke CI execution
* dedicated parallel Chromium Regression CI execution
* parallel complete Chromium full-suite CI validation
* representative parallel Firefox Smoke CI execution
* representative parallel WebKit Smoke CI execution
* Firefox/WebKit `cross-browser-smoke` matrix
* explicit CI runtime defaults
* pytest-html reporting
* browser-specific Firefox pytest-html reporting
* browser-specific WebKit pytest-html reporting
* Allure result collection
* Allure HTML generation
* failure screenshot capture
* Allure failure screenshot attachments
* optional Playwright trace generation
* optional Playwright video generation
* Chromium job-specific CI artifacts
* Firefox browser-specific CI artifacts
* WebKit browser-specific CI artifacts
* dedicated full-suite Allure artifact

Current CI architecture:

```text
runtime defaults
        ↓
Phase 4F runtime diagnostics
        ↓
quality
├── smoke [Chromium]
│   └── xdist workers
│       └── pytest-html
├── regression [Chromium]
│   └── xdist workers
│       └── pytest-html
├── full-suite [Chromium]
│   └── xdist workers
│       ├── pytest-html
│       ├── Allure results
│       ├── failure screenshots
│       └── Allure HTML report
└── cross-browser-smoke
    ├── Firefox
    │   └── xdist workers
    │       └── pytest-html
    └── WebKit
        └── xdist workers
            └── pytest-html
```

The `quality` job is the prerequisite gate.

Chromium Smoke, Chromium Regression, Chromium full-suite, Firefox Smoke, and WebKit Smoke are independent browser-test executions after successful quality validation.

The Firefox and WebKit executions originate from one matrix definition with:

```text
fail-fast: false
```

UI, Security, Sorting, Navigation, and E2E do not currently have dedicated CI jobs but remain selectively executable locally and participate in complete Chromium full-suite execution.

Smoke-tagged tests additionally participate in representative Firefox and WebKit compatibility validation.

Pytest-xdist parallel execution is implemented locally and in all current browser-test CI executions.

Allure reporting is implemented locally and in the complete Chromium full-suite CI reporting path.

Chromium Smoke, Chromium Regression, Firefox Smoke, and WebKit Smoke remain pytest-html-focused.

Runtime configuration is implemented locally and integrated across Chromium, Firefox, and WebKit execution.

Phase 4F runtime diagnostics operate through the existing Pytest execution path and do not require additional CI jobs.

Failed-test diagnostic context covers setup, call, and teardown failures.

Custom project screenshots remain limited to failed call-phase reports when the screenshot policy allows capture.

Trace and video lifecycle remains owned by pytest-playwright and is not reimplemented by Phase 4F or Phase 5A.

Application scenario fixtures are separated into `tests/conftest.py`, while the root `conftest.py` remains responsible for framework-level runtime and failure integration.

Current CI is headless by default and uses explicit runtime configuration.

Chromium remains the primary complete regression browser.

Firefox and WebKit provide representative Smoke compatibility validation only.

Trace and video are available as runtime policies but remain disabled in CI by default.

No sequential-only test, diagnostic, or reporting exceptions were identified for the current implemented execution model.

No Firefox- or WebKit-specific functional compatibility workaround was required for the current Phase 5A implementation.

The `main` branch represents the stable portfolio version of the project.

The `develop` branch and active workstream branches may contain newer validated changes before promotion.

The current architecture includes the completed Phase 4 Framework Maturity foundation and the implemented Phase 5A Playwright cross-browser execution strategy.

Phase 4B CI Execution Strategy, Phase 4C Parallel Execution Strategy, Phase 4D Reporting Upgrade, Phase 4E Runtime Configuration, Phase 4F Diagnostics And Fixture Cleanup, and the Phase 5A representative Firefox/WebKit Smoke execution layer are implemented in the current framework architecture.

Formal Phase 5A roadmap completion remains owned by the dedicated Phase 5A closing checkpoint task.