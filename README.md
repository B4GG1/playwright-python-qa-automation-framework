# Playwright Python QA Automation Framework

## Table of Contents

* [Project Overview](#project-overview)
* [Current Status](#current-status)
* [System Under Test](#system-under-test)
* [Implemented Coverage](#implemented-coverage)
* [Test Suite Strategy](#test-suite-strategy)
* [Technology Stack](#technology-stack)
* [Getting Started](#getting-started)
* [Running Tests](#running-tests)
* [Runtime Configuration](#runtime-configuration)
* [Diagnostics And Fixture Organization](#diagnostics-and-fixture-organization)
* [Quality Checks](#quality-checks)
* [CI Execution](#ci-execution)
* [Reports And Artifacts](#reports-and-artifacts)
* [Documentation](#documentation)
* [Roadmap](#roadmap)
* [Navigation Notes](#navigation-notes)

## Project Overview

This repository contains a QA Automation Framework built primarily with Playwright, Pytest, and Python.

The project serves as both a practical automation engineering playground and a portfolio-oriented framework designed to showcase modern test automation practices, framework architecture, tooling integration, and quality engineering workflows.

The framework currently focuses on Playwright-based UI automation and is developed with a strong emphasis on:

* maintainable framework architecture
* readable test organization
* Page Object Model
* shared authenticated-page behavior
* reusable assertion helpers
* centralized test data
* explicit scenario-oriented pytest fixtures
* separated framework-level Pytest hooks and application scenario fixtures
* pytest parametrization
* marker-based test execution
* representative Smoke and broader Regression coverage
* independent end-to-end journey checkpoints
* pytest-xdist worker-level parallel execution
* automated quality validation
* dedicated Smoke and Regression CI execution
* complete full-suite CI validation
* parallel browser-test execution inside Pytest CI processes
* complementary pytest-html and Allure reporting
* failure screenshot evidence
* configurable Playwright trace and video generation
* centralized environment-based runtime configuration
* configurable base URL, browser mode, timeouts, and artifact policies
* explicit CI runtime defaults
* lightweight runtime diagnostics
* failed-test diagnostic context
* clear diagnostic ownership between Pytest, project screenshot handling, Allure, and pytest-playwright
* GitHub Actions reporting artifacts
* reproducible development environment
* CI-backed Pull Request workflow
* debugging and reporting capabilities
* traceability between manual test cases and automated tests

The long-term goal of the project is to evolve into a production-style automation framework demonstrating both practical QA automation skills and software engineering best practices.

## Current Status

Current stable portfolio phase:

```text
Phase 3 completed — Products, Cart, And Checkout Coverage
```

Stable portfolio snapshot:

```text
Completed Phase 3 state promoted to main as the current portfolio version
```

The `main` branch represents the polished portfolio version of the completed Phase 3 project state.

The `develop` branch remains the integration branch and may contain newer framework maturity work after this README is read from `main`.

Current Phase 4 framework maturity progress includes:

* Phase 4A marker strategy normalization
* explicit Smoke and Regression suite definitions
* normalized executable pytest markers
* Phase 4B CI execution strategy
* separate code-quality validation
* dedicated Smoke CI execution
* dedicated Regression CI execution
* preserved complete full-suite CI execution
* job-specific reports and artifacts
* Phase 4C local parallel execution validation
* pytest-xdist worker-level parallel execution
* parallel Smoke execution
* parallel Regression execution
* parallel full-suite execution
* pytest-xdist integration into existing CI browser-test jobs
* Phase 4D reporting upgrade
* local Allure result generation
* local Allure HTML report generation
* failure screenshot attachments in Allure
* full-suite Allure reporting in GitHub Actions
* dedicated full-suite Allure report artifact
* preserved pytest-html reporting for Smoke, Regression, and full-suite execution
* Phase 4E centralized runtime configuration
* environment-based application base URL configuration
* runtime browser and headed/headless configuration
* configurable Playwright action, navigation, and assertion timeouts
* configurable screenshot, trace, and video policies
* explicit Chromium-only runtime defaults in GitHub Actions browser-test jobs
* validation and normalization of runtime environment-variable values
* final Phase 4E runtime, reporting, sequential, parallel, and CI validation
* Phase 4E roadmap synchronization and completion
* Phase 4F lightweight runtime diagnostics
* effective runtime configuration summary in Pytest output
* failed-test diagnostics containing test identity and failure phase
* current Playwright page URL in failure diagnostics when available
* failure screenshot path reporting when project screenshot capture succeeds
* explicit diagnostic errors for URL, screenshot, and Allure attachment failures
* preserved project screenshot and Allure attachment behavior
* preserved pytest-playwright ownership of trace and video lifecycle
* framework-level Pytest responsibilities separated from application scenario fixtures
* scenario-oriented fixtures moved to `tests/conftest.py`
* sequential and pytest-xdist compatibility validated after fixture cleanup
* Phase 4F diagnostics and fixture strategy documented

The current framework includes completed automation coverage for:

* login and authentication behavior
* authentication error handling
* login UI behavior
* protected route access validation
* protected checkout route access validation
* inventory page visibility and product listing behavior
* product card content validation
* inventory-side Product Details navigation
* Product Details page validation
* product sorting
* Cart navigation
* add-to-cart behavior from Inventory and Product Details
* cart badge behavior
* cart product content validation
* remove-from-cart behavior from Inventory, Product Details, and Cart
* Continue Shopping navigation
* cart state persistence after logout and re-login
* Cart → Checkout Information navigation
* Checkout Information form validation
* checkout required-field validation
* checkout error-state behavior
* Checkout Overview validation
* Checkout Overview price summary validation
* Product Details navigation from Checkout Overview
* checkout Finish behavior
* Checkout Complete confirmation validation
* Back Home navigation after order completion
* primary purchase journey validation through independent E2E checkpoints

Completed Login automation coverage includes:

* manual Login test cases
* `LoginPage` Page Object Model
* reusable Login Page fixture
* centralized login test data
* successful login validation
* invalid credential validation
* empty credential validation
* locked out user validation
* UI validation scenarios
* protected Inventory route validation
* protected Cart route validation
* protected Product Details route validation
* protected Checkout Information route validation
* protected Checkout Overview route validation
* protected Checkout Complete route validation
* input error icon validation after failed login
* pytest parametrization
* normalized pytest marker usage
* GitHub Actions CI validation
* HTML reporting and CI artifacts

Completed Inventory automation coverage includes:

* manual Inventory test cases
* `InventoryPage` Page Object Model
* centralized product test data
* Inventory page visibility validation
* product list validation
* product card content validation
* Product Details navigation through product names
* Product Details navigation through product images
* product sorting validation
* Inventory-side add-to-cart and remove-from-cart validation
* cart badge validation from Inventory actions
* representative Smoke coverage
* broader Regression coverage
* Navigation coverage
* Sorting coverage
* E2E purchase-flow checkpoint coverage

Completed Product Details automation coverage includes:

* manual Product Details test cases
* `ProductDetailsPage` Page Object Model
* Product Details content validation
* return navigation to Inventory
* Product Details-side add-to-cart validation
* Product Details-side remove-from-cart validation
* cart badge validation from Product Details actions
* Cart navigation from Product Details
* all-products Product Details coverage using centralized product data
* representative and broader product coverage

Completed Cart automation coverage includes:

* manual Cart test cases
* `CartPage` Page Object Model
* empty Cart state validation
* added product visibility validation
* Cart product content validation
* remove-from-cart validation
* cart badge decrement and removal validation
* Continue Shopping navigation
* Continue Shopping cart-state preservation
* Product Details navigation from Cart item name
* Checkout Information navigation from Cart
* cart state persistence after logout and re-login
* all-products Cart visibility and remove-from-cart coverage
* representative E2E Cart checkpoint validation

Completed Checkout automation coverage includes:

* manual Checkout test cases
* checkout Page Objects
* centralized checkout test data
* reusable checkout setup fixtures
* Checkout Information form validation
* required customer field validation
* checkout error message validation
* checkout input error icon validation
* checkout error close behavior
* Checkout Information submission with valid data
* Checkout Information cancellation back to Cart
* Checkout Overview selected product validation
* all-products Checkout Overview validation
* Checkout Overview price summary validation
* Checkout Overview cancellation back to Inventory
* Product Details navigation from Checkout Overview
* all-products Product Details navigation from Checkout Overview
* checkout Finish validation
* Checkout Complete confirmation validation
* Back Home navigation after order completion
* multiple independent checkpoints forming the primary E2E purchase journey

Completed Phase 3 finalization includes:

* one automated test module per covered page area
* one manual test case file per covered page area
* `BasePage` and `AppPage` structure alignment
* shared authenticated-page behavior through `AppPage`
* reusable product and checkout assertion helpers
* fixture naming and reuse review
* navigation return type review
* test case metadata cleanup
* documentation synchronization
* final local quality validation
* final full pytest validation
* PR review, CI validation, and squash merge into `develop`
* stable Phase 3 portfolio promotion to `main`

The current roadmap direction is Phase 4 Framework Maturity.

## System Under Test

The framework is built and validated against:

* **Application:** Sauce Demo
* **Default URL:** `https://www.saucedemo.com`

The default application origin is provided by the centralized runtime configuration layer.

Local execution may override the application origin through:

```text
QA_BASE_URL
```

without modifying tests or Page Objects.

Sauce Demo is used as the primary System Under Test because it is a stable, publicly available web application suitable for UI automation practice.

It provides realistic e-commerce-style flows including:

* authentication
* product listing
* Product Details
* cart operations
* checkout
* order completion

This makes it suitable for demonstrating multi-page test automation and scalable framework design.

## Implemented Coverage

Current automated coverage includes Login, Inventory, Product Details, Cart, and Checkout-related behavior.

Detailed test case definitions are stored under the `test_cases/` directory.

The README provides only a high-level coverage overview to keep the project entry point readable and maintainable.

| Workstream                      | Status    | Covered Areas                                                                                                                           | Test Case Documentation                                               |
|---------------------------------|-----------|-----------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------|
| Login Page Automation           | Completed | authentication, credential validation, UI behavior, protected route access, protected checkout routes                                   | [Login Page Test Cases](test_cases/login-page.md)                     |
| Inventory Page Automation       | Completed | Inventory visibility, product list, product content, sorting, Product Details navigation, Inventory-side Cart actions                   | [Inventory Page Test Cases](test_cases/inventory-page.md)             |
| Product Details Page Automation | Completed | product content, return navigation, Product Details-side Cart actions, cart badge behavior, Cart navigation                             | [Product Details Page Test Cases](test_cases/product-details-page.md) |
| Cart Page Automation            | Completed | empty Cart, Cart content, item removal, cart badge behavior, Continue Shopping, persistence, Product Details navigation, Checkout entry | [Cart Page Test Cases](test_cases/cart-page.md)                       |
| Checkout Flow Automation        | Completed | Checkout Information, field validation, Checkout Overview, price summaries, Product Details navigation, completion flow                 | [Checkout Page Test Cases](test_cases/checkout-page.md)               |

Current automated test areas include:

* authentication tests
* login UI tests
* protected route access tests
* Inventory tests
* Product Details tests
* Sorting tests
* Cart tests
* cart badge tests
* cart item content tests
* cart persistence tests
* Checkout Information tests
* Checkout Overview tests
* checkout price summary tests
* Checkout Complete tests
* Navigation tests
* Security tests
* primary purchase E2E checkpoint tests
* shared page-level behavior validation through reusable Page Objects

Some manual test case files also contain documented `Planned` scenarios that do not yet have dedicated automated tests.

The individual test case files remain the source of truth for automation status.

Future automated test areas may include:

* broader end-to-end journey coverage beyond the current primary purchase checkpoints
* API-level tests
* cross-browser UI tests
* additional approved edge-case or known-defect coverage

## Test Suite Strategy

Pytest markers are used to provide selective test execution without changing test independence.

Current executable marker suites are:

* `smoke`
* `regression`
* `ui`
* `security`
* `sorting`
* `navigation`
* `e2e`

Markers describe different dimensions of test intent and are not mutually exclusive.

A test may therefore belong to several suites when appropriate.

Examples include:

* `Smoke / UI`
* `Regression / UI`
* `Smoke / Navigation`
* `Regression / Navigation`
* `Smoke / Navigation / E2E`

The main strategy is:

* **Smoke** — fast representative validation of critical functionality
* **Regression** — broader or deeper validation across expanded applicable cases
* **UI** — visibility, presentation, state, and direct UI behavior
* **Security** — authentication access control and protected routes
* **Sorting** — product sorting behavior
* **Navigation** — meaningful page transitions, excluding the authentication Login → Inventory transition
* **E2E** — independent checkpoints that together form the primary purchase journey

The E2E suite does not depend on test execution order or shared state.

Each E2E checkpoint prepares its own required state through fixtures or test setup and can execute independently.

Application scenario fixtures remain explicit and scenario-oriented.

Current reusable scenario fixtures are defined under:

```text
tests/conftest.py
```

while the repository-level:

```text
conftest.py
```

is reserved for framework-wide Pytest configuration, runtime integration, Playwright context configuration, and failure diagnostics.

The automated suite has also been validated with `pytest-xdist` worker-level parallel execution.

Parallel execution preserves the same test-independence expectations:

* tests do not depend on execution order
* tests do not depend on state produced by another test
* Playwright browser state is isolated through the existing test fixture model
* parametrized scenarios remain independently executable
* E2E checkpoints remain independently executable
* Cart and Checkout scenarios prepare their own required state
* application scenario fixtures remain usable under worker-level execution
* framework-level runtime and diagnostic hooks remain compatible with xdist execution

No sequential-only test exceptions were identified during Phase 4C or Phase 4F parallel-safety validation.

Sequential execution remains supported.

Runtime configuration and Phase 4F diagnostics do not change marker semantics, suite ownership, test independence, or the supported sequential/parallel execution models.

Current CI uses dedicated jobs for:

* Smoke
* Regression

The following marker suites remain selectively executable locally and do not currently have dedicated CI jobs:

* UI
* Security
* Sorting
* Navigation
* E2E

Tests carrying these markers are still included in the complete unfiltered full-suite CI execution.

Detailed marker definitions, assignment rules, parallel execution behavior, runtime configuration behavior, fixture ownership, diagnostic behavior, and examples are documented in:

* [Testing Strategy](docs/testing-strategy.md)

## Technology Stack

### Core Technologies

* Python 3.12
* Pytest
* Playwright
* pytest-playwright
* pytest-xdist
* Git
* GitHub
* GitHub Actions
* WSL2 with Ubuntu Linux

### Code Quality

* Ruff
* Black
* isort
* pre-commit

### Runtime Configuration

* centralized configuration through `config/settings.py`
* environment-variable runtime overrides
* configurable application base URL
* configurable Playwright browser selection
* configurable headed/headless execution
* configurable action and navigation timeout
* configurable Playwright assertion timeout
* configurable screenshot policy
* configurable trace policy
* configurable video policy
* fail-fast validation for invalid runtime values

### Diagnostics

* lightweight project diagnostics through `framework/diagnostics.py`
* named Python logger for diagnostic-operation errors
* effective runtime configuration summary in Pytest session output
* failed-test diagnostic summaries
* test node ID and failure-phase reporting
* current Playwright page URL reporting when available
* successful project screenshot path reporting
* explicit diagnostic errors for page URL, screenshot, and Allure attachment failures
* sequential and pytest-xdist compatible diagnostic output

### Reporting And Debugging

* pytest-html
* Allure Pytest integration
* Allure CLI for local HTML report generation
* screenshots on test failure
* failure screenshot attachments in Allure
* optional Playwright trace generation
* optional Playwright video generation
* GitHub Actions reporting artifacts

### CI

* GitHub Actions
* dedicated quality validation
* parallel Smoke suite execution
* parallel Regression suite execution
* parallel complete full-suite execution
* full-suite Allure result collection and HTML report generation
* explicit runtime defaults for browser-test jobs
* Chromium-only browser installation and execution
* runtime and failure diagnostic output visible through normal Pytest execution logs

### Installed For Future Expansion

* requests

The currently implemented framework focuses on Playwright-based UI automation.

Pytest parallel execution with `pytest-xdist` is implemented locally and in the existing CI browser-test jobs.

Allure reporting is implemented locally and in the complete full-suite CI job while pytest-html remains the lightweight report format used across the existing reporting workflow.

Runtime configuration is implemented through environment variables and the centralized `config/settings.py` module.

Phase 4F diagnostics use lightweight console/report output and the standard Python logging API for diagnostic-operation errors.

The diagnostics layer does not introduce persistent project log files.

Application scenario fixtures are maintained separately from framework-wide Pytest integration through `tests/conftest.py` and the repository-level `conftest.py`.

The current configuration layer does not load `.env` files or implement named environment profiles.

API testing, Docker-based execution, Jenkins integration, Selenium comparison, cross-browser CI execution, browser matrices, device emulation, Allure history persistence, persistent log files, browser console capture, network capture beyond existing Playwright trace behavior, and hosted report publishing remain outside the current implemented framework scope.

## Getting Started

### Prerequisites

Before setting up the framework, ensure the following tools are installed:

* Python 3.12+
* Git
* WSL2 with Ubuntu Linux or another compatible Linux environment
* IDE or editor of choice
* Playwright-supported browser dependencies
* Allure CLI available on `PATH` when local Allure HTML report generation is required

The Python-side Allure integration is installed through the project dependencies.

The standalone Allure CLI is required only for converting generated Allure result data into a readable local HTML report.

Verify the CLI with:

```bash
allure --version
```

### 1. Clone Repository

```bash
git clone git@github.com:B4GG1/playwright-python-qa-automation-framework.git
cd playwright-python-qa-automation-framework
```

### 2. Create Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Project Dependencies

Recommended installation from locked dependency versions:

```bash
pip install -r requirements-lock.txt
```

Alternative installation from the main dependency list:

```bash
pip install -r requirements.txt
```

### 4. Install Playwright Browser

For local Linux or WSL2 setup:

```bash
playwright install --with-deps chromium
```

If system dependencies are already installed:

```bash
playwright install chromium
```

Chromium is the currently validated project and CI browser.

The runtime configuration layer recognizes Playwright browser engines, but the current CI pipeline remains intentionally Chromium-only and does not install Firefox or WebKit.

## Running Tests

Run the complete automated test suite sequentially:

```bash
pytest -v
```

Sequential execution remains fully supported.

When no runtime environment variables are supplied, the framework uses the approved runtime defaults documented in the [Runtime Configuration](#runtime-configuration) section.

### Parallel Execution

The approved local parallel execution strategy uses `pytest-xdist` with automatic worker selection.

Run the complete automated suite in parallel:

```bash
pytest -n auto -v
```

Run Smoke in parallel:

```bash
pytest -m smoke -n auto -v
```

Run Regression in parallel:

```bash
pytest -m regression -n auto -v
```

The current suite was validated under worker-level parallel execution without identified sequential-only exceptions.

Parallel execution does not change marker semantics, test ownership, runtime configuration semantics, diagnostic semantics, fixture ownership, or test independence requirements.

### Allure Reporting

Allure result collection is compatible with both sequential and pytest-xdist parallel execution.

Run the complete suite sequentially and collect Allure results:

```bash
pytest -v \
  --alluredir=reports/allure-results \
  --clean-alluredir
```

Run the complete suite in parallel and collect Allure results:

```bash
pytest -n auto -v \
  --alluredir=reports/allure-results \
  --clean-alluredir
```

Generate the local Allure HTML report:

```bash
allure generate reports/allure-results \
  --clean \
  -o reports/allure-report
```

Current local Allure output locations:

```text
reports/allure-results/
reports/allure-report/
```

The generated report can then be opened locally using the installed Allure tooling or inspected directly from the generated report directory.

Allure complements the existing pytest-html reporting strategy rather than replacing it.

### Marker Suites

Run Smoke sequentially:

```bash
pytest -m smoke -v
```

Run Regression sequentially:

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

Run the primary purchase E2E checkpoint suite:

```bash
pytest -m e2e -v
```

### Combined Marker Execution

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

Detailed marker semantics and additional execution patterns are documented in [Testing Strategy](docs/testing-strategy.md).

### Page-Level Test Modules

Run Login tests:

```bash
pytest tests/test_login_page.py -v
```

Run Inventory tests:

```bash
pytest tests/test_inventory_page.py -v
```

Run Product Details tests:

```bash
pytest tests/test_product_details_page.py -v
```

Run Cart tests:

```bash
pytest tests/test_cart_page.py -v
```

Run Checkout tests:

```bash
pytest tests/test_checkout_page.py -v
```

Markers can also be combined with module-level execution.

Example:

```bash
pytest tests/test_checkout_page.py -m e2e -v
```

### Full Page-Level Validation

For complete current page-level coverage validation:

```bash
pytest -v tests/test_login_page.py
pytest -v tests/test_inventory_page.py
pytest -v tests/test_product_details_page.py
pytest -v tests/test_cart_page.py
pytest -v tests/test_checkout_page.py
pytest -v
```

Marker-based commands remain useful for selective local validation.

Smoke and Regression are additionally executed as dedicated GitHub Actions jobs.

The complete unfiltered suite remains the full-suite CI regression gate.

The Smoke, Regression, and full-suite CI jobs execute their selected tests through `pytest-xdist`.

## Runtime Configuration

Phase 4E provides centralized environment-based runtime configuration through:

```text
config/settings.py
```

The configuration layer allows execution behavior to be changed without editing automated tests or Page Objects.

Current supported environment variables are:

| Environment Variable   | Default                     | Supported Values / Behavior                         |
|------------------------|-----------------------------|-----------------------------------------------------|
| `QA_BASE_URL`          | `https://www.saucedemo.com` | HTTP or HTTPS application origin                    |
| `QA_BROWSER`           | `chromium`                  | `chromium`, `firefox`, `webkit`                     |
| `QA_HEADED`            | `false`                     | `true`, `false`, `1`, `0`, `yes`, `no`, `on`, `off` |
| `QA_TIMEOUT_MS`        | `30000`                     | non-negative integer in milliseconds                |
| `QA_EXPECT_TIMEOUT_MS` | `5000`                      | non-negative integer in milliseconds                |
| `QA_SCREENSHOT_POLICY` | `only-on-failure`           | `only-on-failure`, `off`                            |
| `QA_TRACE_POLICY`      | `off`                       | `off`, `retain-on-failure`, `on`                    |
| `QA_VIDEO_POLICY`      | `off`                       | `off`, `retain-on-failure`, `on`                    |

String-based browser and policy values are normalized by trimming surrounding whitespace and converting supported values to lowercase.

### Base URL

The default application origin is:

```text
https://www.saucedemo.com
```

Page Objects define relative `ROUTE` values and combine them with the configured base URL through `BasePage`.

This allows the target application origin to change without editing Page Objects or tests.

Example:

```bash
QA_BASE_URL="http://localhost:8000" pytest -m smoke -v
```

The configured base URL must:

* use `http` or `https`
* contain a valid host
* represent only the application origin rather than a nested application path
* not contain credentials
* not contain query parameters
* not contain a fragment
* not contain whitespace
* use a valid port when a port is supplied

A trailing `/` on the origin is normalized away.

Examples of accepted values include:

```text
https://example.com
https://example.com/
http://localhost:8000
```

### Browser Configuration

The default browser is:

```text
chromium
```

Supported runtime values are:

```text
chromium
firefox
webkit
```

Example:

```bash
QA_BROWSER=chromium pytest -m smoke -v
```

The configuration layer recognizes the three Playwright browser engines.

This does not mean that all three browsers are installed or validated in every execution environment.

The current project CI installs and runs Chromium only.

Cross-browser CI and browser matrices are not currently implemented.

Explicit native pytest-playwright browser options remain usable.

When an explicit native `--browser` option is provided, it is not silently replaced by the project environment configuration.

### Headed And Headless Execution

The default execution mode is headless:

```text
QA_HEADED=false
```

To request headed local execution:

```bash
QA_HEADED=true pytest -m smoke -v
```

Supported true values are:

```text
true
1
yes
on
```

Supported false values are:

```text
false
0
no
off
```

Values are case-insensitive after normalization.

The native pytest-playwright `--headed` option also remains available.

The current CI browser-test jobs explicitly use:

```text
QA_HEADED=false
```

and therefore remain headless.

### Action And Navigation Timeout

The default Playwright action and navigation timeout is:

```text
QA_TIMEOUT_MS=30000
```

This value is applied to each created Playwright browser context as both:

* the default action timeout
* the default navigation timeout

Example:

```bash
QA_TIMEOUT_MS=45000 pytest -m regression -v
```

Timeout values must be non-negative integer numbers of milliseconds.

A value of `0` is accepted and follows Playwright timeout semantics.

### Assertion Timeout

The default Playwright assertion timeout is:

```text
QA_EXPECT_TIMEOUT_MS=5000
```

Example:

```bash
QA_EXPECT_TIMEOUT_MS=7000 pytest -m smoke -v
```

This value configures the Playwright `expect()` assertion timeout.

As with the action/navigation timeout, the configured value must be a non-negative integer number of milliseconds.

### Screenshot Policy

The default screenshot policy is:

```text
QA_SCREENSHOT_POLICY=only-on-failure
```

Supported values are:

```text
only-on-failure
off
```

The default preserves the project failure screenshot mechanism.

When a browser test fails during the Pytest test-call phase:

* the existing hook captures a screenshot
* the screenshot is written under `reports/screenshots/`
* the successful screenshot path is included in failed-test diagnostic context
* the same PNG is attached to Allure as `Failure screenshot` when Allure result collection is active

The project does not create a second project-level screenshot implementation through pytest-playwright.

To disable the custom failure screenshot behavior:

```bash
QA_SCREENSHOT_POLICY=off pytest -m smoke -v
```

When screenshot policy is `off`:

* the custom failure screenshot is not written
* no project screenshot path is added to failure diagnostics
* the corresponding Allure `Failure screenshot` attachment is not created

### Trace Policy

The default trace policy is:

```text
QA_TRACE_POLICY=off
```

Supported values are:

```text
off
retain-on-failure
on
```

Example:

```bash
QA_TRACE_POLICY=retain-on-failure pytest -m regression -v
```

Trace generation uses pytest-playwright / Playwright artifact capabilities rather than a custom project recording implementation.

When enabled, pytest-playwright runtime trace output is generated under its runtime artifact structure, currently rooted under:

```text
test-results/
```

Explicit native pytest-playwright tracing options remain usable and take precedence when supplied directly on the command line.

### Video Policy

The default video policy is:

```text
QA_VIDEO_POLICY=off
```

Supported values are:

```text
off
retain-on-failure
on
```

Example:

```bash
QA_VIDEO_POLICY=on pytest tests/test_login_page.py -v
```

Video recording uses pytest-playwright / Playwright capabilities rather than a custom project recording implementation.

When enabled, generated video output is written under the pytest-playwright runtime artifact structure, currently rooted under:

```text
test-results/
```

Explicit native pytest-playwright video options remain usable and take precedence when supplied directly on the command line.

### Combined Runtime Overrides

Environment variables may be combined for a single execution.

Example:

```bash
QA_BASE_URL="https://www.saucedemo.com" \
QA_BROWSER="chromium" \
QA_HEADED="false" \
QA_TIMEOUT_MS="45000" \
QA_EXPECT_TIMEOUT_MS="7000" \
QA_SCREENSHOT_POLICY="only-on-failure" \
QA_TRACE_POLICY="retain-on-failure" \
QA_VIDEO_POLICY="off" \
pytest -m smoke -n auto -v
```

The override applies only to the process environment in which the command is executed.

No test or Page Object modification is required.

### Invalid Runtime Configuration

Explicit invalid environment-variable values fail early with a configuration error.

Examples of invalid configuration include:

* unsupported browser names
* unsupported artifact policy values
* invalid boolean values
* negative timeouts
* non-integer timeout values
* malformed application origins

The resulting error identifies the affected environment variable.

This fail-fast behavior prevents tests from running with silently invalid runtime configuration.

### Runtime Configuration Boundaries

The current runtime configuration layer does not implement:

* named environment profiles
* automatic `.env` file loading
* browser matrices
* cross-browser CI execution
* Firefox or WebKit installation in CI
* device emulation
* browser channels
* mobile emulation
* slow motion execution configuration
* retries

The configuration layer intentionally focuses on the currently approved runtime surface.

Diagnostics consume the effective runtime configuration but do not expand or redefine the configuration API.

## Diagnostics And Fixture Organization

Phase 4F provides lightweight runtime and failed-test diagnostics while establishing a clearer responsibility boundary between framework-wide Pytest integration and application scenario fixtures.

### Diagnostics Utility

Project diagnostic helpers are located in:

```text
framework/diagnostics.py
```

The module provides:

* formatting of the effective runtime summary
* formatting of failed-test diagnostic context
* formatting of diagnostic-operation errors
* a named Python logger:

```text
qa_automation.diagnostics
```

The logger is used for diagnostic-operation errors.

The project does not configure persistent file logging or create project log files.

### Runtime Diagnostic Summary

The repository-level Pytest integration exposes the effective runtime configuration through the normal Pytest session header.

A typical summary has the form:

```text
[runtime] base_url=https://www.saucedemo.com | browser=chromium | mode=headless | action_navigation_timeout_ms=30000 | assertion_timeout_ms=5000 | screenshot=only-on-failure | trace=off | video=off
```

The summary surfaces:

* effective base URL
* effective browser value
* headed or headless execution mode
* action and navigation timeout
* Playwright assertion timeout
* project screenshot policy
* pytest-playwright trace policy
* pytest-playwright video policy

This output reflects the effective configuration after environment and supported command-line precedence rules are applied.

Under pytest-xdist execution, the framework avoids emitting a duplicate runtime header from every worker.

### Failed-Test Diagnostic Context

Failed Pytest execution phases receive a dedicated diagnostic section.

The diagnostic summary identifies:

* Pytest node ID
* failure phase:
  * `setup`
  * `call`
  * `teardown`
* current Playwright page URL when a usable `page` fixture is available
* successful project screenshot path when a screenshot is captured

Example:

```text
[failure] test=tests/test_example.py::test_example[chromium] | phase=call | url=https://www.saucedemo.com/ | screenshot=reports/screenshots/test_example.png
```

Failure diagnostics do not replace the original Pytest exception.

The original test, fixture, or teardown failure remains the primary failure.

If a diagnostic operation itself fails, the framework records explicit context for operations such as:

```text
page-url
screenshot
allure-attachment
```

without intentionally replacing the original test failure.

### Screenshot And Allure Responsibility

Project screenshot behavior remains intentionally narrow.

When:

```text
QA_SCREENSHOT_POLICY=only-on-failure
```

and a browser test fails during the `call` phase:

* the existing project hook captures one PNG
* the PNG is written under `reports/screenshots/`
* the successful path is included in failure diagnostics
* Allure reuses the same PNG as `Failure screenshot` when Allure result collection is active

No duplicate screenshot mechanism is introduced.

When:

```text
QA_SCREENSHOT_POLICY=off
```

both the project failure screenshot and its corresponding Allure screenshot attachment are disabled.

Setup and teardown failures still receive diagnostic test and phase context, but the project screenshot mechanism remains limited to failed `call` phases.

### Trace And Video Responsibility

Trace and video lifecycle remains owned by pytest-playwright.

Runtime configuration maps the project policies to pytest-playwright runtime options.

The project diagnostic layer does not:

* manually start tracing
* manually stop tracing
* manually create trace archives
* manually start video recording
* manually stop video recording
* automatically enable tracing after a failure
* automatically enable video after a failure

Trace and video therefore remain independent runtime policies controlled through:

```text
QA_TRACE_POLICY
QA_VIDEO_POLICY
```

or explicit supported pytest-playwright command-line options.

### Pytest Responsibility Boundary

The repository-level:

```text
conftest.py
```

owns framework-wide responsibilities:

* supported runtime configuration integration
* runtime configuration precedence handling
* Playwright assertion timeout configuration
* Playwright browser-context timeout configuration
* Pytest runtime header
* failed-test diagnostic hook
* project failure screenshot integration
* Allure reuse of the existing project screenshot

Application scenario fixtures are located in:

```text
tests/conftest.py
```

Current explicit scenario-oriented fixtures include:

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

These fixtures preserve the existing scenario preparation behavior and their original function scope.

The fixture cleanup does not introduce:

* autouse scenario fixtures
* generic fixture factories
* dependency-injection containers
* fixture registration frameworks
* additional fixture package layers solely to reduce file size
* changed Page Object ownership
* changed test scenario ownership

### Sequential And Parallel Compatibility

The Phase 4F diagnostic and fixture organization has been validated with:

* sequential execution
* pytest-xdist worker-level parallel execution
* Smoke execution
* Regression execution
* complete full-suite execution

The same scenario fixtures remain available to existing test consumers without behavioral rewrites.

Framework runtime and failure diagnostics remain functional under the supported execution models.

### Diagnostic Scope Boundaries

The current diagnostic implementation deliberately does not provide:

* persistent project log files
* automatic HTML or page-source dumps
* browser console capture
* browser console log persistence
* network request or response capture
* HAR generation
* custom network tracing
* new diagnostic artifact types
* automatic trace enablement on failure
* automatic video enablement on failure
* automatic retries
* hosted reports
* GitHub Pages report publishing

Playwright trace functionality remains the only currently implemented trace-level browser diagnostic mechanism and is owned by pytest-playwright.

## Quality Checks

Run Ruff linting:

```bash
ruff check .
```

Check formatting with Black:

```bash
black --check .
```

Check import sorting with isort:

```bash
isort . --check-only
```

Run all main local validation checks:

```bash
ruff check .
black --check .
isort . --check-only
pytest -v
```

If formatting changes are needed:

```bash
black .
isort .
```

Run pre-commit hooks manually:

```bash
pre-commit run --all-files
```

Install pre-commit hooks:

```bash
pre-commit install
```

## CI Execution

The current GitHub Actions pipeline combines:

* the Phase 4B CI job structure
* the Phase 4C Pytest parallel execution strategy
* the Phase 4D reporting strategy
* the Phase 4E runtime configuration strategy
* the Phase 4F runtime and failure diagnostic behavior

Current job structure:

```text
quality
├── smoke
├── regression
└── full-suite
```

The `quality` job runs first and validates:

* Ruff
* Black
* isort

It does not install Playwright Chromium, execute browser tests, or use `pytest-xdist`.

After successful quality validation, the following browser jobs are independently executable:

* `smoke`
* `regression`
* `full-suite`

GitHub Actions may schedule these three independent jobs concurrently.

Inside each browser-test job, Pytest additionally distributes collected tests across xdist workers.

These are two separate concurrency layers:

* **GitHub Actions job-level concurrency** — Smoke, Regression, and full-suite may run as separate jobs at the same time after `quality`
* **Pytest worker-level parallelism** — `pytest-xdist` distributes tests across workers inside each browser-test job

Smoke executes:

```bash
pytest -m smoke -n auto -v
```

The actual CI command also generates its existing self-contained pytest HTML report:

```bash
pytest -m smoke -n auto -v --html=reports/smoke-report.html --self-contained-html
```

Regression executes:

```bash
pytest -m regression -n auto -v
```

The actual CI command also generates its existing self-contained pytest HTML report:

```bash
pytest -m regression -n auto -v --html=reports/regression-report.html --self-contained-html
```

Smoke and Regression intentionally remain focused pytest-html reporting jobs and do not generate duplicate Allure reports.

The full-suite job executes the complete unfiltered suite through pytest-xdist while generating both pytest-html output and Allure result data:

```bash
pytest -n auto -v \
  --html=reports/report.html \
  --self-contained-html \
  --alluredir=reports/allure-results \
  --clean-alluredir
```

The full-suite job then generates the Allure HTML report from:

```text
reports/allure-results/
```

into:

```text
reports/allure-report/
```

using:

```bash
allure generate reports/allure-results \
  --clean \
  -o reports/allure-report
```

The CI workflow attempts Allure report generation whenever usable result data exists, including after failed test execution.

All three browser jobs install Playwright Chromium.

The full-suite job additionally prepares the Allure CLI required for HTML report generation.

### CI Runtime Configuration

Smoke, Regression, and full-suite use explicit runtime defaults:

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

These CI defaults intentionally match the approved local runtime defaults.

This keeps CI execution explicit and predictable while using the same runtime configuration implementation as local execution.

Current CI behavior therefore remains:

* Chromium-only
* headless
* pytest-xdist parallel
* screenshot-on-failure enabled
* tracing disabled by default
* video disabled by default
* runtime configuration summary available in normal Pytest output
* failed-test diagnostic context available when a browser-test execution fails

Phase 4F does not change the CI topology.

It reuses the normal Pytest execution path, so runtime and failure diagnostic information becomes visible in CI logs without introducing a dedicated logging service or diagnostic job.

The CI workflow does not introduce:

* browser matrices
* Firefox installation
* WebKit installation
* cross-browser validation
* retries
* `continue-on-error`
* trace retention by default
* video retention by default
* automatic trace enablement after failure
* automatic video enablement after failure
* persistent diagnostic log artifacts
* secrets for non-secret runtime values

The current CI browser scope remains intentionally Chromium-only.

The workflow runs automatically for:

* pushes to `main`
* pushes to `develop`
* Pull Requests targeting `main`
* Pull Requests targeting `develop`

It can also be started manually through `workflow_dispatch`.

Runtime configuration and diagnostics do not introduce additional browser jobs or change the existing CI topology.

Detailed CI job behavior, dependencies, xdist execution, runtime defaults, diagnostic visibility, commands, artifacts, and failure handling are documented in:

* [CI/CD Pipeline](docs/ci-cd-pipeline.md)

## Reports And Artifacts

The framework uses complementary reporting and failure-evidence mechanisms:

* **pytest console output** — immediate execution feedback and effective runtime summary
* **failure diagnostic sections** — failed-test identity, failure phase, optional page URL, and successful screenshot path
* **pytest-html** — lightweight self-contained HTML reporting
* **Allure** — richer reporting for local complete-suite runs and the CI full-suite job
* **failure screenshots** — browser evidence captured when a test fails during the test call phase
* **Playwright traces** — optional runtime diagnostic artifacts controlled by `QA_TRACE_POLICY`
* **Playwright videos** — optional runtime diagnostic artifacts controlled by `QA_VIDEO_POLICY`
* **GitHub Actions artifacts** — retained CI report and failure-evidence outputs

Runtime diagnostics themselves are console/report context and do not create a separate project artifact type.

Local generated reporting output is stored under:

```text
reports/
```

Current pytest-html output examples include:

```text
reports/smoke-report.html
reports/regression-report.html
reports/report.html
```

Current Allure output locations are:

```text
reports/allure-results/
reports/allure-report/
```

Failure screenshots are stored under:

```text
reports/screenshots/
```

when:

```text
QA_SCREENSHOT_POLICY=only-on-failure
```

and a browser test fails during the test-call phase.

When screenshot capture succeeds for a failed browser test:

* the existing screenshot file remains the project failure evidence
* the path is included in failure diagnostics
* the same PNG is attached to Allure when Allure result collection is active

This reuses the same captured PNG rather than introducing a second screenshot mechanism.

When:

```text
QA_SCREENSHOT_POLICY=off
```

the custom screenshot and corresponding Allure screenshot attachment are disabled.

Failed setup or teardown phases still receive failed-test diagnostic context when Pytest reports those failures.

When trace or video generation is enabled, pytest-playwright-generated diagnostic files are written under its runtime artifact structure, currently rooted under:

```text
test-results/
```

Trace and video are disabled by default locally and in CI.

The project diagnostics layer does not automatically enable trace or video when a test fails.

The report, screenshot, Allure, trace, video, runtime diagnostic, and fixture behavior is compatible with the approved pytest-xdist parallel execution model.

Sequential execution remains supported.

Generated reports, screenshots, traces, videos, Allure results, Allure HTML output, cache files, and other runtime artifacts should not be committed to Git.

The repository ignore policy keeps generated runtime output outside version-controlled project content.

The current CI strategy keeps Smoke and Regression focused on their existing pytest-html reports.

Current Smoke artifacts:

* `smoke-pytest-html-report`
* `smoke-test-artifacts`

Current Regression artifacts:

* `regression-pytest-html-report`
* `regression-test-artifacts`

The full-suite job provides both the existing pytest-html artifacts and the advanced Allure report.

Current full-suite artifacts:

* `pytest-html-report`
* `full-suite-allure-report`
* `test-artifacts`

The dedicated Allure artifact contains the generated HTML report from:

```text
reports/allure-report/
```

The existing `test-artifacts` upload continues to preserve the broader `reports/` runtime output behavior.

Artifact uploads use separate names between jobs to avoid conflicts.

Available browser-job reports and artifacts are uploaded with `if: always()` even when test execution fails.

Artifact retention remains seven days.

Trace and video retention in CI is not enabled by default because both runtime policies default to `off`.

Allure history persistence, persistent project logging, report hosting, and GitHub Pages reporting are not currently implemented.

Detailed artifact paths, retention, runtime policy behavior, diagnostic behavior, parallel execution behavior, and CI handling are documented in:

* [CI/CD Pipeline](docs/ci-cd-pipeline.md)

## Documentation

Extended project documentation is stored in the `docs/` directory so that the README can remain a high-level entry point.

### Core Documentation

* [Architecture](docs/architecture.md)
  Overview of framework architecture, layers, runtime configuration, diagnostics, fixture responsibility boundaries, execution isolation, reporting responsibilities, and design direction.

* [Framework And Project Structure](docs/framework-and-project-structure.md)
  Explanation of folder structure, framework-level Pytest responsibilities, scenario fixture ownership, configuration ownership, repository organization, runtime outputs, and parallel-execution considerations.

* [Technology Stack](docs/technology-stack.md)
  Overview of implemented and planned technologies, including runtime configuration, lightweight diagnostics, reporting, and parallel execution.

### Engineering Workflow

* [Git Branching Strategy](docs/git-branching-strategy.md)
  Branching model, merge strategy, and repository workflow standards.

* [Workflow](docs/workflow.md)
  Day-to-day workflow for branches, commits, Pull Requests, local validation, sequential and parallel execution, runtime overrides, diagnostics, reporting, marker execution, and CI responsibilities.

* [CI/CD Pipeline](docs/ci-cd-pipeline.md)
  Current GitHub Actions quality gate, runtime defaults, parallel Smoke and Regression jobs, parallel complete full-suite execution, runtime and failed-test diagnostic visibility, pytest-html and Allure reporting, artifacts, triggers, and CI maturity boundaries.

* [Quality Tooling](docs/quality-tooling.md)
  Ruff, Black, isort, pre-commit, Pytest, pytest-xdist, Playwright runtime configuration, project diagnostics, reporting integrations, and local/CI quality gates.

### Testing And Planning

* [Testing Strategy](docs/testing-strategy.md)
  Detailed test design, marker semantics, sequential and parallel suite execution strategy, runtime configuration behavior, diagnostic behavior, reporting behavior, E2E checkpoint model, fixture responsibility boundaries, parametrization, and validation approach.

* [Features Overview](docs/features.md)
  Implemented and planned framework capabilities, including current Phase 4F diagnostics and fixture organization.

* [Roadmap](docs/roadmap.md)
  Project phases and long-term framework direction.

### Test Case Documentation

* [Login Page Test Cases](test_cases/login-page.md)
  Manual Login test cases mapped to automation coverage.

* [Inventory Page Test Cases](test_cases/inventory-page.md)
  Manual Inventory test cases mapped to automation coverage.

* [Product Details Page Test Cases](test_cases/product-details-page.md)
  Manual Product Details test cases mapped to automation coverage.

* [Cart Page Test Cases](test_cases/cart-page.md)
  Manual Cart test cases mapped to automation coverage.

* [Checkout Page Test Cases](test_cases/checkout-page.md)
  Manual Checkout test cases mapped to automation coverage.

## Roadmap

Current roadmap direction:

* **Phase 1:** Foundation — completed
* **Phase 2:** Login Page Automation Workstream — completed
* **Phase 2 Checkpoint:** Documentation review and Phase 3 preparation — completed
* **Phase 3A:** Inventory And Products Automation Workstream — completed
* **Phase 3B:** Cart Automation Workstream — completed
* **Phase 3C:** Structure Cleanup, Coverage Completion, And Documentation Sync — completed
* **Phase 3D:** Checkout Automation Workstream — completed
* **Phase 3 Completion Review:** completed
* **Phase 3 Portfolio Promotion:** completed Phase 3 state promoted to `main`
* **Phase 4:** Framework Maturity — in progress
* **Phase 4A:** Marker Strategy And Test Suite Organization — implemented
* **Phase 4B:** CI Execution Strategy — implemented
* **Phase 4C:** Parallel Execution — implemented
* **Phase 4D:** Reporting Upgrade — implemented
* **Phase 4E:** Runtime Configuration — completed
* **Phase 4F:** Diagnostics And Fixture Cleanup — completed
* **Phase 5:** Advanced Extensions — future

Current Phase 4 work focuses on framework maturity rather than expanding page-level functional coverage.

Phase 4A established the current marker and suite strategy.

Phase 4B introduced:

* separate CI quality validation
* dedicated Smoke CI execution
* dedicated Regression CI execution
* preserved complete full-suite execution
* clearer CI reports and artifacts

Phase 4C introduced:

* validated local `pytest-xdist` worker-level parallel execution
* parallel Smoke execution
* parallel Regression execution
* parallel complete full-suite execution
* sequential execution as a supported fallback
* validation of existing fixture and test independence under parallel execution
* xdist integration into the existing Smoke, Regression, and full-suite CI jobs
* preservation of existing HTML reports and CI artifacts
* explicit separation between GitHub Actions job-level concurrency and Pytest worker-level parallelism

No sequential-only test exceptions were identified during Phase 4C validation.

Phase 4D introduced:

* Allure result collection for local complete-suite execution
* local Allure HTML report generation
* reuse of existing failure screenshots as Allure attachments
* compatibility with sequential and pytest-xdist parallel execution
* preservation of pytest-html as the lightweight reporting layer
* full-suite Allure result collection in GitHub Actions
* full-suite Allure HTML report generation in CI
* dedicated `full-suite-allure-report` GitHub Actions artifact
* preservation of existing Smoke and Regression pytest-html reporting
* generated reporting output kept outside version-controlled repository content

Phase 4E introduced:

* centralized runtime configuration through `config/settings.py`
* environment-based application base URL configuration
* runtime browser selection
* headed/headless execution configuration
* Playwright action and navigation timeout configuration
* Playwright assertion timeout configuration
* configurable failure screenshot policy
* configurable Playwright trace policy
* configurable Playwright video policy
* normalization and validation of environment-variable values
* fail-fast behavior for invalid explicit configuration
* integration with the existing pytest-playwright fixture model
* preservation of explicit native pytest-playwright runtime options
* environment-based execution overrides without editing tests or Page Objects
* explicit runtime defaults in Smoke, Regression, and full-suite CI jobs
* preservation of Chromium-only CI execution
* preservation of the existing Phase 4B–4D CI, parallelization, reporting, and artifact architecture

Current runtime defaults are:

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

The Phase 4E implementation does not introduce environment profiles, `.env` loading, browser matrices, cross-browser CI, device emulation, or retries.

Phase 4E was completed through AQA-0105 after final local runtime-configuration validation, sequential and pytest-xdist parallel suite validation, controlled artifact-policy validation, pytest-html and Allure reporting validation, successful GitHub Actions validation, and roadmap synchronization.

Phase 4F introduced:

* lightweight diagnostics through `framework/diagnostics.py`
* effective runtime configuration summary in Pytest output
* diagnostic output for the effective base URL
* diagnostic output for browser and headed/headless mode
* diagnostic output for action/navigation and assertion timeouts
* diagnostic output for screenshot, trace, and video policies
* failed-test summaries containing the Pytest node ID
* failed-test summaries containing the failed execution phase
* current Playwright page URL reporting when available
* successful project screenshot path reporting when available
* explicit diagnostic errors for page URL retrieval, screenshot capture, and Allure attachment failures
* preservation of the original test or fixture failure as the primary failure
* preservation of the existing project screenshot implementation
* reuse of the same captured PNG for the Allure `Failure screenshot` attachment
* preservation of `QA_SCREENSHOT_POLICY=off` behavior
* preservation of pytest-playwright ownership of trace and video lifecycle
* no automatic trace or video enablement after failures
* separation of framework-level Pytest responsibilities into the repository-level `conftest.py`
* separation of application scenario fixtures into `tests/conftest.py`
* preserved explicit fixture names and scenario behavior
* preserved fixture function scopes
* no autouse redesign
* no generic fixture framework
* no dependency-injection layer
* no unnecessary fixture package hierarchy
* compatibility with sequential execution
* compatibility with pytest-xdist parallel execution
* successful Smoke and Regression validation after fixture separation
* successful complete sequential and parallel suite validation after fixture separation
* documentation synchronization with the final diagnostics and fixture strategy

Phase 4F deliberately does not introduce:

* persistent project log files
* browser console capture
* automatic page-source or HTML dumps
* network request or response capture
* custom network tracing
* new diagnostic artifact types
* automatic trace enablement
* automatic video enablement
* retries
* hosted reports
* GitHub Pages report publishing
* a new CI topology

Phase 4F completes the Diagnostics And Fixture Cleanup workstream required before the broader Phase 4 checkpoint.

The Phase 4 checkpoint itself remains a separate project milestone and is not represented as completed by this documentation update.

Future extension areas include:

* API-level testing
* hybrid UI and API scenarios
* cross-browser execution
* Docker-based execution
* Selenium comparison
* Jenkins integration
* advanced test analytics

The detailed and authoritative roadmap is maintained in [docs/roadmap.md](docs/roadmap.md).

## Navigation Notes

* Clickable links point directly to Markdown files in the repository.
* GitHub automatically renders `.md` files.
* Extended documentation is version-controlled alongside the framework.
* Detailed test strategy, runtime configuration behavior, diagnostic behavior, fixture ownership, reporting behavior, and parallel execution remain in `docs/testing-strategy.md`.
* Detailed CI runtime defaults, diagnostic visibility, reporting, and artifact behavior remain in `docs/ci-cd-pipeline.md`.
* Detailed manual test cases remain under `test_cases/`.
* Runtime reports, Allure outputs, screenshots, traces, and videos are ignored by Git and handled as local outputs or CI artifacts.
* The project diagnostic layer does not create persistent project log files.