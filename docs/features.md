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
* CI validation

API testing, Selenium comparison, Docker-based execution, Jenkins integration, cross-browser CI execution, Allure history persistence, hosted reporting, environment profiles, and Phase 4F diagnostics work remain future extensions unless explicitly described as implemented below.

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

The policies preserve the existing Phase 4D reporting architecture.

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

* the existing screenshot hook captures one PNG
* the file is stored under `reports/screenshots/`
* when Allure result collection is active, the same PNG is attached as `Failure screenshot`

The framework does not create a second project-level screenshot implementation through pytest-playwright.

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
* Phase 4F logging redesign
* Phase 4F fixture cleanup

These capabilities remain outside the current Phase 4E scope.

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
* use fixtures or test-local setup
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

Runtime configuration applies to E2E tests in the same way as the remaining Pytest suites.

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

The project uses the pytest-playwright fixture/runtime model.

The project-level browser context fixture extends pytest-playwright's `new_context` fixture to apply approved runtime timeout values.

Tests do not rely on state produced by previous tests.

Current fixture chains, Cart and Checkout scenarios, logout/re-login persistence, parametrized scenarios, and E2E checkpoints have been validated under parallel execution.

No sequential-only test exceptions were identified during Phase 4C validation.

Phase 4F may review fixture organization later.

Phase 4E does not redesign fixture ownership.

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

## CI Concurrency Model

GitHub Actions job-level concurrency and pytest-xdist worker-level parallelism are separate mechanisms.

Conceptually:

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
        └── Allure HTML report
```

Runtime configuration and reporting are layered on top of test execution.

They do not introduce additional concurrency models.

The following marker suites do not currently have dedicated CI jobs:

* UI
* Security
* Sorting
* Navigation
* E2E

## Reporting And Debugging

Current reporting and debugging support includes:

* Pytest console output
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

* **pytest-html** — lightweight execution reports
* **Allure** — richer structured reporting and advanced full-suite reporting
* **failure screenshots** — direct browser evidence for failed test calls
* **Playwright traces** — optional execution diagnostics
* **Playwright videos** — optional browser recording diagnostics
* **GitHub Actions artifacts** — temporary storage and distribution of generated CI outputs

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

## Repository And Documentation

Current repository documentation includes:

* README project entry point
* architecture documentation
* framework structure documentation
* testing strategy
* marker execution strategy
* parallel execution strategy
* runtime configuration strategy
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

* additional reusable fixtures when justified
* additional framework utilities when repeated logic appears
* additional Page Objects when new application areas require them
* lightweight logging improvements
* richer failed-test diagnostics
* fixture organization review

Centralized runtime configuration is already implemented and should not be described as future functionality.

Phase 4F may later review diagnostics and fixture organization.

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

The current Phase 4E configuration surface should remain the documented source of current functionality until future approved work expands it.

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

Already implemented:

* normalized marker strategy
* dedicated Smoke CI
* dedicated Regression CI
* pytest-xdist worker-level parallel execution
* independent E2E checkpoint design

Future work should improve scalability and feedback without reintroducing obsolete marker categories or order-dependent test design.

## Reporting And Diagnostics

Current Allure reporting, screenshot policy, trace policy, and video policy are implemented and should not be described as future-only functionality.

Possible future reporting and diagnostic improvements include:

* improved screenshot organization
* structured logging
* richer failure diagnostics
* Allure history persistence
* trend reporting
* execution analytics
* JUnit XML output
* hosted report publishing

The following are not currently implemented:

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

The independent Smoke, Regression, and full-suite jobs may be scheduled concurrently after `quality`.

Inside each browser job, pytest-xdist distributes collected tests between workers.

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

No sequential-only test or reporting exceptions were identified for the current execution model.

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
* job-specific CI artifacts
* dedicated full-suite Allure report artifact
* generated runtime output isolation
* Git branching workflow
* technical project documentation

Current CI execution and reporting model:

```text
Phase 4E runtime defaults
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
        └── Allure HTML report
```

The `quality` job is the prerequisite and does not use browser execution or pytest-xdist.

Smoke, Regression, and full-suite remain separate GitHub Actions jobs and may execute concurrently after successful quality validation.

UI, Security, Sorting, Navigation, and E2E do not currently have dedicated CI jobs.

Phase 4C pytest-xdist parallel execution is implemented.

Phase 4D reporting is implemented.

Phase 4E Runtime Configuration was completed through AQA-0105.

Implemented Phase 4E capabilities include:

* centralized environment configuration
* runtime base URL
* browser selection
* headed/headless configuration
* Playwright timeouts
* assertion timeout
* screenshot policy
* trace policy
* video policy
* invalid configuration validation
* pytest-playwright integration
* explicit CI runtime defaults
* validated sequential execution
* validated pytest-xdist parallel execution
* validated failure screenshot and Allure attachment behavior
* validated screenshot-disabled behavior
* validated representative trace and video generation
* validated pytest-html and Allure reporting
* successful final GitHub Actions validation
* synchronized Phase 4E roadmap completion

The following remain outside the current implemented scope:

* named environment profiles
* automatic `.env` loading
* Allure history persistence
* report hosting
* GitHub Pages reporting
* API testing
* Docker-based execution
* browser matrices
* cross-browser CI
* retries
* device emulation
* Phase 4F logging and fixture cleanup