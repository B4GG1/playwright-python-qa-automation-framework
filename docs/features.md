# Features

This document lists the currently implemented and planned features of the QA automation framework.

The purpose of this file is to provide a concise overview of what the framework currently supports and what remains planned for future development.

The implemented feature set reflects the current framework state on the active development branch.

The `main` branch represents the stable portfolio version, while `develop` and active workstream branches may contain newer validated changes before promotion.

The current implemented scope focuses on UI automation with Playwright and Pytest together with framework maturity capabilities for:

* test organization
* parallel execution
* reporting
* runtime configuration
* runtime diagnostics
* fixture responsibility separation
* CI validation

API testing, Selenium comparison, Docker-based execution, Jenkins integration, cross-browser CI execution, Allure history persistence, hosted reporting, environment profiles, retries, and persistent diagnostic logging remain future extensions unless explicitly described as implemented below.

# Currently Implemented

## Test Execution

Current execution capabilities include:

* UI automation using Playwright
* Pytest-based test execution
* pytest-playwright integration
* Chromium as the default browser
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
* complete unfiltered automated test-suite execution
* complete automated test-suite execution in CI
* pytest-xdist execution inside existing CI browser-test jobs
* centralized environment-based runtime configuration
* lightweight runtime diagnostics
* failed-test diagnostic context

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

## Runtime Configuration

Phase 4E provides centralized runtime configuration through:

```text
config/settings.py
```

Current runtime configuration features include:

* environment-variable configuration
* application base URL configuration
* browser selection
* headed/headless execution
* Playwright action timeout configuration
* Playwright navigation timeout configuration
* Playwright assertion timeout configuration
* failure screenshot policy
* Playwright trace policy
* Playwright video policy
* normalization of string configuration values
* predictable boolean parsing
* timeout validation
* base URL validation
* fail-fast invalid configuration behavior
* focused runtime configuration tests
* integration with existing pytest-playwright fixtures and runtime options
* explicit runtime defaults in browser-test CI jobs

Current environment variables:

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

Current defaults:

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

Runtime configuration allows execution behavior to change without editing functional tests or Page Objects.

Example:

```bash
QA_BROWSER=chromium \
QA_HEADED=false \
QA_TIMEOUT_MS=45000 \
QA_EXPECT_TIMEOUT_MS=7000 \
QA_TRACE_POLICY=retain-on-failure \
pytest -m smoke -n auto -v
```

Focused configuration validation is implemented in:

```text
tests/test_runtime_config.py
```

## Application Base URL Configuration

The default application origin is:

```text
https://www.saucedemo.com
```

It can be overridden through:

```text
QA_BASE_URL
```

Example:

```bash
QA_BASE_URL="http://localhost:8000" pytest -m smoke -v
```

The configuration layer validates that the supplied value:

* uses `http` or `https`
* contains a valid host
* represents only an application origin
* does not contain credentials
* does not contain query parameters
* does not contain a fragment
* does not contain whitespace
* contains a valid port when a port is supplied

A trailing slash is normalized away.

Page Objects define application-relative `ROUTE` values.

`BasePage` combines those routes with:

```text
settings.base_url
```

This removes environment-specific application origins from individual tests and Page Objects.

## Browser Runtime Configuration

Browser selection is controlled through:

```text
QA_BROWSER
```

Supported configuration values are:

```text
chromium
firefox
webkit
```

Default:

```text
chromium
```

Browser values are normalized before validation.

Example:

```bash
QA_BROWSER=chromium pytest -m smoke -v
```

The configuration layer recognizes all three Playwright engines.

This does not mean that all three engines are installed or validated in every execution environment.

Current GitHub Actions execution remains Chromium-only.

Explicit native pytest-playwright browser selection remains usable.

When an explicit `--browser` option is supplied, the project runtime configuration does not silently replace it.

## Headed And Headless Execution

Headed/headless execution is controlled through:

```text
QA_HEADED
```

Default:

```text
false
```

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

Values are case-insensitive after normalization.

Example headed local execution:

```bash
QA_HEADED=true pytest -m smoke -v
```

The native pytest-playwright:

```text
--headed
```

option remains usable.

Current CI explicitly uses:

```text
QA_HEADED=false
```

and therefore remains headless.

## Timeout Configuration

Action and navigation timeout configuration:

```text
QA_TIMEOUT_MS
```

Default:

```text
30000
```

This value is applied to Playwright browser contexts as:

* default action timeout
* default navigation timeout

Example:

```bash
QA_TIMEOUT_MS=45000 pytest -m regression -v
```

Assertion timeout configuration:

```text
QA_EXPECT_TIMEOUT_MS
```

Default:

```text
5000
```

Example:

```bash
QA_EXPECT_TIMEOUT_MS=7000 pytest -m smoke -v
```

Timeout values:

* are expressed in milliseconds
* must be non-negative integers
* may use `0`, following Playwright timeout semantics

## Artifact Runtime Policies

Phase 4E provides configurable runtime policies for:

* failure screenshots
* Playwright traces
* Playwright videos

The policies preserve the existing reporting architecture.

They do not introduce custom duplicate trace or video implementations.

## Screenshot Policy

Configured through:

```text
QA_SCREENSHOT_POLICY
```

Supported values:

```text
only-on-failure
off
```

Default:

```text
only-on-failure
```

The default preserves the existing project-level failure screenshot mechanism.

When a browser test fails during the Pytest call phase:

* the custom screenshot hook captures one PNG when a Playwright page is available
* the file is stored under `reports/screenshots/`
* when Allure result collection is active, the same PNG is attached as `Failure screenshot`
* the successfully created screenshot path is included in the Phase 4F failed-test diagnostic summary

The framework does not create a second project-level screenshot implementation through pytest-playwright.

Setup-phase and teardown-phase failures receive failed-test diagnostic context but do not trigger the custom project screenshot.

When:

```text
QA_SCREENSHOT_POLICY=off
```

the project:

* does not write the custom failure PNG
* does not create the corresponding Allure screenshot attachment

## Trace Policy

Configured through:

```text
QA_TRACE_POLICY
```

Supported values:

```text
off
retain-on-failure
on
```

Default:

```text
off
```

Example:

```bash
QA_TRACE_POLICY=retain-on-failure pytest -m regression -v
```

Trace generation uses pytest-playwright / Playwright-supported runtime capabilities.

The project does not implement custom trace recording logic.

When enabled, trace output is generated through pytest-playwright's runtime artifact structure rooted under:

```text
test-results/
```

Representative trace output:

```text
trace.zip
```

Explicit native pytest-playwright trace options remain usable and take precedence when explicitly supplied.

## Video Policy

Configured through:

```text
QA_VIDEO_POLICY
```

Supported values:

```text
off
retain-on-failure
on
```

Default:

```text
off
```

Example:

```bash
QA_VIDEO_POLICY=on pytest tests/test_login_page.py -v
```

Video generation uses pytest-playwright / Playwright-supported capabilities.

The project does not implement custom video recording logic.

When enabled, runtime output is generated under:

```text
test-results/
```

Representative output:

```text
video.webm
```

Explicit native pytest-playwright video options remain usable and take precedence when explicitly supplied.

## Invalid Runtime Configuration

Explicit invalid runtime configuration fails early.

Examples include:

* unsupported browser values
* invalid boolean values
* negative timeout values
* non-integer timeout values
* malformed application base URLs
* unsupported screenshot policy values
* unsupported trace policy values
* unsupported video policy values

Configuration errors identify the affected environment variable.

Invalid explicit configuration is not silently replaced with a default value.

## Runtime Configuration Scope Boundaries

The current runtime configuration implementation does not include:

* named environment profiles
* automatic `.env` loading
* browser matrices
* cross-browser CI execution
* Firefox CI installation
* WebKit CI installation
* device emulation
* mobile emulation
* browser channels
* slow-motion configuration
* retries

Runtime diagnostics are implemented separately from runtime configuration and do not introduce additional environment variables.

## Runtime Diagnostics

Phase 4F provides lightweight runtime and failed-test diagnostics without introducing persistent log files.

Shared diagnostic formatting is implemented in:

```text
framework/diagnostics.py
```

Current diagnostic capabilities include:

* runtime summary formatting
* failed-test summary formatting
* diagnostic error formatting
* project diagnostics logger
* integration with Pytest execution through the root `conftest.py`

### Runtime Summary

The effective runtime summary is emitted through:

```text
pytest_report_header
```

The summary displays:

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

Representative output follows:

```text
[runtime] base_url=... | browser=... | mode=... | action_navigation_timeout_ms=... | assertion_timeout_ms=... | screenshot=... | trace=... | video=...
```

The displayed values represent the effective runtime configuration after project settings and applicable native pytest-playwright command-line options have been resolved.

During pytest-xdist execution, worker processes do not emit duplicate runtime summaries.

The controlling Pytest process therefore provides one concise runtime header rather than one copy per worker.

### Failed-Test Diagnostic Context

Failed-test diagnostics apply to failed reports from:

```text
setup
call
teardown
```

Each failed-test summary identifies:

* Pytest node ID
* failure phase

When a Playwright page is available, the summary also includes:

* current page URL

When the custom project screenshot is successfully created, the summary also includes:

* screenshot path

Representative output follows:

```text
[failure] test=<node-id> | phase=<setup|call|teardown> | url=<current-url> | screenshot=<path>
```

URL and screenshot fields are included only when the corresponding values are available.

This provides useful failure context without assuming that every failure has a usable Playwright page or screenshot.

### Diagnostic Error Reporting

Errors produced while collecting diagnostic evidence are reported through the Phase 4F diagnostics mechanism.

Current covered operations are:

* page URL retrieval
* screenshot creation
* Allure screenshot attachment

Representative output follows:

```text
[diagnostic-error] operation=<operation> | test=<node-id> | phase=<phase> | error=<error>
```

Diagnostic errors are emitted through the project diagnostics logger and added to the failed Pytest report diagnostic sections.

A diagnostic error does not create a persistent project log file.

If screenshot creation fails, no screenshot path is reported.

If Allure attachment fails after successful screenshot creation, the screenshot remains available under `reports/screenshots/` and its path remains available in the failed-test diagnostic summary.

## Diagnostic Scope Boundaries

The current Phase 4F diagnostic implementation does not include:

* persistent project log files
* browser console capture
* network capture
* custom network tracing outside existing Playwright trace support
* HTML or page-source dumps
* automatic trace enablement
* automatic video enablement
* retries
* new CI jobs for diagnostics
* hosted diagnostic reports

Playwright trace and video lifecycle remains owned by pytest-playwright.

The custom project screenshot remains the only project-owned screenshot lifecycle.

## Page Object Model

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
* application-relative route definitions
* runtime base URL composition
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
* authenticated Cart access
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

Page Objects do not independently parse runtime environment variables.

Browser runtime configuration remains outside the Page Object layer.

Diagnostic responsibilities also remain outside Page Objects.

## Reusable Assertions

Current reusable assertion support includes:

* reusable product assertion helpers
* Inventory product card validation
* Product Details validation
* Cart item validation
* Checkout Overview product validation
* Checkout Overview price summary validation
* Inventory product-state validation after navigation
* product price conversion for numeric comparisons

Current shared implementation:

```text
framework/assertions/product_assertions.py
```

Reusable assertion helpers remain focused on validation rather than:

* navigation
* browser setup
* fixture setup
* runtime configuration
* diagnostics
* reporting configuration

## Test Data Management

Current centralized test data includes:

* login test data
* product test data
* checkout test data
* standard valid user credentials
* invalid credential cases
* empty credential cases
* locked out user case
* authentication validation messages
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

Current files:

```text
test_data/login_test_data.py
test_data/product_test_data.py
test_data/checkout_test_data.py
```

Inventory, Product Details, Cart, and Checkout tests reuse centralized product data.

Centralized test data represents reusable test input and does not create shared browser state between tests or xdist workers.

Runtime configuration is not test data.

## Login Page Test Coverage

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
* Login page element visibility
* password masking validation
* Login submission using Enter
* input error icon validation
* protected Inventory route validation
* protected Cart route validation
* protected Product Details route validation
* protected Checkout Information route validation
* protected Checkout Overview route validation
* protected Checkout Complete route validation
* lightweight Sauce Demo availability validation

## Inventory Page Test Coverage

Current Inventory automation includes:

* Inventory page visibility
* product list validation
* product card content validation
* representative Add to cart behavior
* all-products Add to cart coverage
* Add to cart → Remove state validation
* representative Remove behavior
* all-products Remove coverage
* Remove → Add to cart state validation
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

## Product Details Page Test Coverage

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
* representative Cart navigation
* full Product Details → Cart navigation coverage across all products

## Cart Page Test Coverage

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

## Checkout Page Test Coverage

Current Checkout automation includes:

* Checkout Information form validation
* lightweight Smoke validation of Checkout Information availability
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
* lightweight Smoke validation of Checkout Complete availability
* Back Home navigation to Inventory
* independent Checkout-related E2E checkpoints

## Primary Purchase E2E Coverage

The framework provides an `e2e` marker suite representing independent checkpoints of the primary Sauce Demo purchase journey.

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

E2E tests:

* are independently executable
* prepare their own state
* use scenario fixtures or test-local setup
* do not depend on execution order
* do not share state between test cases

Run sequentially:

```bash
pytest -m e2e -v
```

E2E does not currently have a dedicated CI job.

Its tests still participate in complete full-suite CI execution.

Because full-suite CI uses pytest-xdist, individual E2E checkpoints may execute on different workers while remaining independent.

Because full-suite collects Allure results, E2E checkpoints also participate in the advanced full-suite report.

Runtime configuration and Phase 4F diagnostics apply to E2E tests in the same way as the remaining Pytest suites.

## Test Organization

Current test organization includes:

* one automated functional module per covered page area
* one manual test case file per covered page area
* one focused runtime configuration test module
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
* parametrized runtime configuration validation
* test case IDs in product-facing parametrized tests where practical
* traceability between test case documentation and automation
* compatibility with sequential and parallel execution
* order-independent functional test design
* separation of framework-level Pytest integration from application scenario fixtures

Current functional modules:

```text
tests/test_login_page.py
tests/test_inventory_page.py
tests/test_product_details_page.py
tests/test_cart_page.py
tests/test_checkout_page.py
```

Framework configuration validation:

```text
tests/test_runtime_config.py
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

## Fixtures And Reusable Setup

Phase 4F separates framework-level Pytest responsibilities from application scenario fixtures.

The root:

```text
conftest.py
```

contains framework-level responsibilities including:

* pytest runtime configuration
* runtime diagnostic header
* pytest-playwright browser configuration integration
* Playwright BrowserContext timeout configuration
* failed-test diagnostic hook
* custom failure screenshot integration
* Allure failure screenshot integration

Application scenario fixtures are defined in:

```text
tests/conftest.py
```

Current scenario fixtures are:

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

These fixtures provide:

* opened Login state
* standard valid-user data
* authenticated Inventory state
* Inventory state with one selected product in Cart
* Cart state with one product
* Checkout Information state with one product
* Checkout Overview state with one product
* Checkout Complete state after the prepared checkout flow

Reusable fixture setup supports:

* authentication setup
* product selection
* Cart preparation
* Checkout preparation
* isolated test execution
* independent E2E checkpoints
* sequential execution
* pytest-xdist worker-level execution

Fixture names remain explicit and scenario-oriented.

The project does not introduce:

* a generic fixture factory
* a dependency-injection layer
* an autouse fixture redesign
* a multi-layer fixture package
* fixture scope redesign

The project uses the pytest-playwright fixture/runtime model.

The project-level browser context fixture remains a framework-level fixture in the root `conftest.py`.

It extends pytest-playwright's `new_context` fixture to apply approved runtime timeout values.

Application scenario fixtures remain function-scoped and prepare deterministic application state independently for each scenario.

Tests do not rely on state produced by previous tests.

Current fixture chains, Cart and Checkout scenarios, logout/re-login persistence, parametrized scenarios, and E2E checkpoints remain compatible with sequential and parallel execution.

The Phase 4F fixture responsibility separation was validated without changing the fixture API consumed by functional tests.

No sequential-only test exceptions are required for the current execution model.

## Code Quality

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

Focused runtime configuration validation:

```bash
pytest tests/test_runtime_config.py
```

Phase 4F implementation has been validated with:

* Smoke execution
* Regression execution
* full sequential execution
* full pytest-xdist execution
* Ruff
* Black check
* isort

Controlled failure validation also confirmed continued runtime and failed-test diagnostic behavior after fixture responsibility separation.

## Selective Marker Validation

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

Smoke and Regression also support:

```bash
pytest -m smoke -n auto -v
pytest -m regression -n auto -v
```

Smoke and Regression additionally have dedicated GitHub Actions jobs.

UI, Security, Sorting, Navigation, and E2E remain selectively executable without dedicated CI jobs.

Tests assigned to those markers still run through complete full-suite CI execution.

Parallel execution changes test distribution rather than marker semantics.

Runtime configuration changes execution settings rather than marker semantics.

Diagnostics provide execution and failure context rather than marker semantics.

## CI/CD

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
* Chromium-only browser installation
* explicit Phase 4E browser runtime defaults
* headless browser execution
* explicit timeout defaults
* default failure screenshot policy
* trace disabled by default
* video disabled by default
* pytest-html report generation
* Allure result collection in full-suite
* Allure HTML generation in full-suite
* Java setup for Allure CLI
* Allure CLI setup
* Smoke-specific report and artifact upload
* Regression-specific report and artifact upload
* full-suite pytest-html artifact upload
* dedicated full-suite Allure report artifact
* broader full-suite runtime artifact
* seven-day artifact retention
* CI execution on pushes to `main`
* CI execution on pushes to `develop`
* CI execution for Pull Requests targeting `main`
* CI execution for Pull Requests targeting `develop`
* manual execution through `workflow_dispatch`
* minimal workflow permissions using `contents: read`

Current CI structure:

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

The quality job:

* does not install Chromium
* does not execute browser tests
* does not use pytest-xdist
* does not require browser runtime configuration

Smoke, Regression, and full-suite depend on successful quality validation.

They do not depend on each other.

GitHub Actions may schedule them concurrently after `quality`.

Phase 4F does not introduce another CI job or change this topology.

## CI Runtime Defaults

Smoke, Regression, and full-suite use:

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

These defaults match the approved local runtime defaults.

The CI model remains:

* Chromium-only
* headless
* pytest-xdist parallel
* screenshots on failed test calls enabled
* trace disabled by default
* video disabled by default

CI does not currently introduce:

* browser matrices
* Firefox installation
* WebKit installation
* retries
* runtime configuration forms in `workflow_dispatch`
* secrets for non-secret runtime values
* default trace retention
* default video retention
* diagnostic-specific CI jobs

## Smoke CI

Core command:

```bash
pytest -m smoke -n auto -v
```

The actual CI command additionally generates:

```text
reports/smoke-report.html
```

Smoke remains focused on pytest-html reporting.

It does not generate a dedicated Allure report.

Runtime diagnostics are available through the normal Pytest execution path.

## Regression CI

Core command:

```bash
pytest -m regression -n auto -v
```

The actual CI command additionally generates:

```text
reports/regression-report.html
```

Regression remains focused on pytest-html reporting.

It does not generate a dedicated Allure report.

Runtime diagnostics are available through the normal Pytest execution path.

## Full-Suite CI

The full-suite job executes the complete unfiltered test collection:

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

CI then attempts to generate:

```text
reports/allure-report/
```

when usable Allure results exist.

The full-suite job remains:

* the complete CI regression gate
* the main CI source for advanced Allure reporting

Phase 4F diagnostics operate inside the same Pytest execution path and do not introduce a second reporting pipeline.

## CI Concurrency Model

GitHub Actions job-level concurrency and pytest-xdist worker-level parallelism are separate mechanisms.

Conceptually:

```text
Phase 4E runtime defaults
        ↓
Phase 4F runtime diagnostics
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
        └── Allure HTML report
```

Runtime configuration, diagnostics, and reporting are layered on top of test execution.

They do not introduce additional concurrency models.

The runtime diagnostic header is emitted by the controlling Pytest process rather than being duplicated by each xdist worker.

The following marker suites do not currently have dedicated CI jobs:

* UI
* Security
* Sorting
* Navigation
* E2E

## Reporting And Debugging

Current reporting and debugging support includes:

* Pytest console output
* lightweight effective runtime summary
* failed-test node ID diagnostics
* failed-test setup/call/teardown phase diagnostics
* current page URL diagnostics when available
* custom screenshot path diagnostics when available
* diagnostic error reporting
* pytest-html
* self-contained pytest-html reports
* Allure Pytest integration
* local Allure result collection
* local Allure HTML generation
* full-suite CI Allure result collection
* full-suite CI Allure HTML generation
* configurable screenshots on failed test calls
* failure screenshot attachment to Allure
* configurable Playwright trace generation
* configurable Playwright video generation
* `reports/` runtime output
* `test-results/` Playwright diagnostic output
* job-specific GitHub Actions artifacts
* downloadable CI artifacts

The reporting and diagnostic mechanisms have complementary responsibilities:

* **Phase 4F runtime diagnostics** — effective execution context
* **Phase 4F failed-test diagnostics** — test identity, failure phase, available URL, screenshot path, and diagnostic-operation errors
* **pytest-html** — lightweight execution reports
* **Allure** — richer structured reporting and advanced full-suite reporting
* **failure screenshots** — direct browser evidence for failed test calls
* **Playwright traces** — optional execution diagnostics owned by pytest-playwright
* **Playwright videos** — optional browser recording diagnostics owned by pytest-playwright
* **GitHub Actions artifacts** — temporary storage and distribution of generated CI outputs

Phase 4F diagnostics are lightweight console/report context.

They do not create persistent diagnostic log files.

## Current Reporting Paths

pytest-html:

```text
reports/smoke-report.html
reports/regression-report.html
reports/report.html
```

Allure:

```text
reports/allure-results/
reports/allure-report/
```

Failure screenshots:

```text
reports/screenshots/
```

Optional pytest-playwright trace/video outputs:

```text
test-results/
```

Runtime summaries and failure diagnostic summaries do not introduce an additional persistent report directory.

## Local Allure Reporting

Collect sequentially:

```bash
pytest -v \
  --alluredir=reports/allure-results \
  --clean-alluredir
```

Collect through pytest-xdist:

```bash
pytest -n auto -v \
  --alluredir=reports/allure-results \
  --clean-alluredir
```

Generate the HTML report:

```bash
allure generate reports/allure-results \
  --clean \
  -o reports/allure-report
```

The standalone Allure CLI must be installed and available on `PATH`.

`allure-pytest` handles result collection.

The Allure CLI handles HTML generation.

Phase 4F diagnostics remain independent from Allure report generation.

## CI Reporting Artifacts

Current Smoke artifacts:

```text
smoke-pytest-html-report
smoke-test-artifacts
```

Current Regression artifacts:

```text
regression-pytest-html-report
regression-test-artifacts
```

Current full-suite artifacts:

```text
pytest-html-report
full-suite-allure-report
test-artifacts
```

The dedicated Allure artifact publishes:

```text
reports/allure-report/
```

The broader full-suite artifact publishes:

```text
reports/
```

Artifact upload steps use:

```yaml
if: always()
```

so available browser-test outputs can still be published when an executing test command fails.

Current retention:

```text
7 days
```

Reporting does not change the CI failure result.

A failing required test still fails its browser job.

Trace and video are disabled by default in CI and are not currently uploaded as dedicated CI artifacts.

Phase 4F does not add a persistent diagnostics artifact.

## Generated Runtime Outputs

Generated reporting and diagnostic outputs are runtime content.

Current generated locations include:

```text
reports/
reports/screenshots/
reports/allure-results/
reports/allure-report/
test-results/
playwright-report/
```

These outputs are intended for:

* local debugging
* failure investigation
* execution evidence
* CI artifact publication

They are not intended to be committed to Git.

The repository ignore policy protects generated report, Allure, and Playwright artifact locations.

Phase 4F runtime summaries and failed-test summaries do not create additional persistent project output locations.

## Repository And Documentation

Current repository documentation includes:

* README project entry point
* architecture documentation
* framework structure documentation
* testing strategy
* marker execution strategy
* parallel execution strategy
* runtime configuration strategy
* diagnostics strategy
* fixture responsibility strategy
* reporting strategy
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
runtime configuration
      ↓
sequential / parallel execution
      ↓
runtime / failure diagnostics
      ↓
reporting
      ↓
CI execution
```

Depending on marker assignment, automated tests may participate in:

* dedicated parallel Smoke CI execution
* dedicated parallel Regression CI execution
* parallel complete full-suite CI execution
* complete full-suite Allure reporting

# Planned Features

## Framework Architecture

Possible future framework improvements include:

* additional reusable fixtures when justified by repeated scenario setup
* additional framework utilities when repeated logic appears
* additional Page Objects when new application areas require them
* further responsibility separation when justified by actual framework growth

Centralized runtime configuration is already implemented and should not be described as future functionality.

Phase 4F diagnostics and fixture responsibility separation are also implemented and should not be described as future functionality.

Future fixture work should be driven by concrete reuse requirements rather than introducing a generic fixture factory, dependency-injection layer, autouse redesign, multi-layer fixture package, or scope redesign without an approved need.

## Runtime Configuration Extensions

Possible future runtime configuration extensions include:

* named environment profiles
* `.env` file loading if explicitly approved
* environment-specific configuration grouping
* device emulation
* browser channels
* mobile emulation
* slow-motion configuration

None of these capabilities are currently implemented.

The current Phase 4E configuration surface remains the documented source of current runtime configuration functionality.

## Test Coverage

Potential future automation areas include:

* broader end-to-end journey coverage beyond current checkpoints
* broader session and logout coverage where justified
* additional approved edge cases
* known-defect coverage where appropriate
* API-level testing
* hybrid UI/API scenarios
* cross-browser validation when explicitly approved

## Test Organization

Possible future improvements include:

* additional suite-specific CI execution where justified
* expanded traceability
* additional parametrized scenarios where useful
* additional reusable scenario fixtures when repeated setup justifies them

Already implemented:

* normalized marker strategy
* dedicated Smoke CI
* dedicated Regression CI
* pytest-xdist worker-level parallel execution
* independent E2E checkpoint design
* separated framework-level and application scenario fixture responsibilities

Future work should improve scalability and feedback without reintroducing obsolete marker categories, order-dependent test design, or unnecessary fixture abstraction layers.

## Reporting And Diagnostics

Current Allure reporting, screenshot policy, trace policy, video policy, runtime diagnostics, failed-test diagnostics, and diagnostic error reporting are implemented and should not be described as future-only functionality.

Possible future reporting and diagnostic improvements include:

* improved screenshot organization
* persistent structured logging if explicitly justified
* Allure history persistence
* trend reporting
* execution analytics
* JUnit XML output
* hosted report publishing

The following are not currently implemented:

* persistent project log files
* browser console capture
* network capture
* HTML or page-source dumps
* automatic trace enablement
* automatic video enablement
* Allure history persistence
* trend-history storage
* hosted Allure reports
* GitHub Pages reporting
* default trace retention in CI
* default video retention in CI
* retry-based diagnostics

## CI/CD Improvements

Possible future CI improvements include:

* dependency caching
* Playwright browser caching
* additional marker-based jobs where justified
* multi-browser execution
* browser matrices
* scheduled regression execution
* JUnit XML publishing
* additional reporting integrations

Already implemented:

* dedicated Smoke and Regression jobs
* pytest-xdist execution
* pytest-html reporting
* full-suite Allure reporting
* explicit Phase 4E runtime defaults
* Phase 4F diagnostics operating through the existing Pytest execution path

The independent Smoke, Regression, and full-suite jobs may be scheduled concurrently after `quality`.

Inside each browser job, pytest-xdist distributes collected tests between workers.

Phase 4F does not introduce another CI topology or another concurrency layer.

## API Testing

The `requests` dependency is installed for possible future API automation.

Potential scope includes:

* API smoke tests
* backend validation
* API-based test data setup
* API-based test data cleanup
* hybrid UI/API scenarios

API testing is not currently implemented.

`api` is not a current executable pytest marker.

## Parallel Execution

pytest-xdist is an implemented execution capability.

Current approved commands:

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

The current suite has been validated for:

* fixture isolation
* browser-state independence
* Cart and Checkout state preparation
* logout and re-login behavior
* E2E checkpoint independence
* parametrized scenario independence
* pytest-html compatibility
* Allure compatibility
* failure screenshot compatibility
* runtime configuration compatibility
* Phase 4F runtime diagnostic compatibility
* Phase 4F failed-test diagnostic compatibility
* separated framework and scenario fixture responsibilities

No sequential-only test, diagnostic, or reporting exceptions are required for the current execution model.

GitHub Actions job concurrency and pytest-xdist worker concurrency remain distinct execution layers.

## Advanced Reporting Extensions

Allure reporting is currently implemented through:

* `allure-pytest`
* local result generation
* local HTML generation
* full-suite CI result generation
* full-suite CI HTML generation
* failure screenshot attachments
* dedicated GitHub Actions Allure artifact publication

Current output locations:

```text
reports/allure-results/
reports/allure-report/
```

Possible future capabilities include:

* history persistence
* trend analytics
* hosted reports
* GitHub Pages publishing
* richer metadata
* additional report analytics

These extensions should not be described as implemented until their approved scope is completed.

Phase 4F runtime and failed-test diagnostics are separate from these possible advanced Allure extensions.

## Cross-Browser Execution

Current default browser:

```text
chromium
```

Current runtime configuration recognizes:

```text
chromium
firefox
webkit
```

A configured non-Chromium engine can be selected locally when the corresponding Playwright browser is installed.

Current CI remains Chromium-only.

The framework does not currently provide:

* cross-browser CI
* a browser matrix
* Firefox CI execution
* WebKit CI execution
* validated cross-browser compatibility claims

pytest-xdist parallelization of Chromium tests should not be interpreted as cross-browser parallel execution.

## Future Extensions

Potential long-term extensions include:

* Selenium WebDriver comparison
* Docker-based execution
* Jenkins integration
* reusable framework packaging
* advanced execution analytics

# Current Feature Status

The implemented framework currently demonstrates:

* Playwright UI automation
* pytest-playwright integration
* Pytest
* pytest-xdist worker-level parallel execution
* supported sequential execution
* Page Object Model
* application-relative Page Object routing
* runtime base URL composition
* shared authenticated-page behavior
* reusable assertion helpers
* centralized test data
* reusable application scenario fixtures
* separated framework-level and scenario-level fixture responsibilities
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
* centralized runtime configuration
* base URL runtime overrides
* browser runtime selection
* headed/headless runtime selection
* Playwright action/navigation timeout configuration
* Playwright assertion timeout configuration
* fail-fast configuration validation
* configurable failure screenshot policy
* configurable trace policy
* configurable video policy
* focused runtime configuration tests
* lightweight runtime diagnostic summary
* effective runtime value visibility
* pytest-xdist runtime-header de-duplication
* failed-test node ID diagnostics
* setup/call/teardown failure-phase diagnostics
* current URL diagnostics when a Playwright page is available
* custom screenshot path diagnostics
* diagnostic error reporting for page URL retrieval
* diagnostic error reporting for screenshot creation
* diagnostic error reporting for Allure attachment
* shared diagnostics formatting through `framework/diagnostics.py`
* project diagnostics logger without persistent project log files
* code quality tooling
* pre-commit validation
* GitHub Actions CI
* separate CI quality validation
* dedicated parallel Smoke CI execution
* dedicated parallel Regression CI execution
* parallel complete full-suite CI execution
* explicit Phase 4E CI runtime defaults
* Chromium-only CI execution
* pytest-html reporting
* Allure result collection
* Allure HTML generation
* sequential and parallel Allure compatibility
* screenshots on failure
* failure screenshot attachments in Allure
* optional trace generation
* optional video generation
* pytest-playwright ownership of trace and video lifecycle
* job-specific CI artifacts
* dedicated full-suite Allure report artifact
* generated runtime output isolation
* Git branching workflow
* technical project documentation

Current CI execution, diagnostics, and reporting model:

```text
Phase 4E runtime defaults
        ↓
Phase 4F runtime diagnostics
        ↓
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
        ├── failure screenshots
        └── Allure HTML report
```

The `quality` job is the prerequisite and does not use browser execution or pytest-xdist.

Smoke, Regression, and full-suite remain separate GitHub Actions jobs and may execute concurrently after successful quality validation.

UI, Security, Sorting, Navigation, and E2E do not currently have dedicated CI jobs.

Phase 4C pytest-xdist parallel execution is implemented.

Phase 4D reporting is implemented.

Phase 4E Runtime Configuration is implemented.

Phase 4F Diagnostics And Fixture Cleanup is implemented.

Implemented Phase 4F capabilities include:

* lightweight runtime diagnostics
* effective runtime summary through `pytest_report_header`
* runtime base URL visibility
* browser visibility
* headed/headless mode visibility
* action/navigation timeout visibility
* assertion timeout visibility
* screenshot policy visibility
* trace policy visibility
* video policy visibility
* runtime-header suppression on pytest-xdist workers
* failed-test node ID reporting
* setup/call/teardown failure-phase reporting
* current URL reporting when a Playwright page is available
* custom screenshot path reporting after successful capture
* diagnostic error reporting for page URL retrieval
* diagnostic error reporting for screenshot creation
* diagnostic error reporting for Allure attachment
* diagnostics formatting through `framework/diagnostics.py`
* lightweight project diagnostics logger
* framework-level Pytest responsibilities in root `conftest.py`
* application scenario fixtures in `tests/conftest.py`
* preserved explicit scenario fixture names
* preserved fixture scopes
* preserved pytest-playwright browser lifecycle
* preserved pytest-playwright trace lifecycle
* preserved pytest-playwright video lifecycle
* preserved custom screenshot behavior
* preserved Allure failure screenshot reuse
* validated sequential execution compatibility
* validated pytest-xdist execution compatibility
* validated runtime header behavior
* validated failed-test phase reporting
* validated failed-test node ID reporting
* validated current URL reporting
* validated screenshot diagnostic path reporting
* Ruff validation
* Black check validation
* isort validation

The following remain outside the current implemented scope:

* named environment profiles
* automatic `.env` loading
* persistent project log files
* browser console capture
* network capture
* HTML or page-source dumps
* automatic trace enablement
* automatic video enablement
* Allure history persistence
* report hosting
* GitHub Pages reporting
* API testing
* Docker-based execution
* browser matrices
* cross-browser CI
* retries
* device emulation