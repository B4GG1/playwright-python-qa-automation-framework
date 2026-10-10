# Technology Stack

This document describes the technologies, tools, framework capabilities, and planned integrations used in the QA automation project.

The stack is divided into:

* implemented technologies
* active framework integrations
* supporting development tooling
* runtime configuration and diagnostics
* execution and reporting tooling
* explicit current-scope boundaries
* planned future extensions

The `main` branch represents the stable portfolio version of the project.

The `develop` branch and active workstream branches may contain newer validated framework work before promotion to `main`.

The current stack includes the implemented Phase 5A Playwright cross-browser execution strategy:

* Chromium as the primary complete regression browser
* Firefox as a representative Smoke compatibility browser
* WebKit as a representative Smoke compatibility browser

This browser strategy expands execution coverage without introducing complete three-browser Regression or full-suite execution.

## Core Technologies

The project is currently built with:

* Python 3.12
* Pytest
* Playwright
* pytest-playwright
* pytest-xdist
* pytest-html
* allure-pytest
* Git
* GitHub
* GitHub Actions
* WSL2 with Ubuntu Linux

Python's standard library is additionally used for framework concerns such as:

* environment-variable handling
* immutable runtime settings
* URL validation
* UTC timestamps
* lightweight diagnostics logging

These technologies form the implemented UI automation, execution, runtime configuration, diagnostics, reporting, code-quality, CI, and representative cross-browser validation foundation.

## Test Automation

Current implemented test automation stack:

* Playwright for browser automation
* Pytest as the test runner
* pytest-playwright for Playwright and Pytest integration
* pytest-xdist for worker-level parallel execution
* Page Object Model for page interaction abstraction
* shared authenticated-page behavior through `AppPage`
* reusable assertion helpers
* explicit scenario-oriented pytest fixtures
* separated framework-level and scenario-level fixture responsibilities
* pytest parametrization for data-driven scenarios
* centralized test data
* centralized runtime configuration
* lightweight runtime diagnostics
* failed-test diagnostics
* explicit pytest markers
* strict marker validation
* selective marker-based execution
* sequential execution
* parallel Smoke execution
* parallel Regression execution
* parallel full-suite execution
* dedicated Chromium Smoke CI execution
* dedicated Chromium Regression CI execution
* complete Chromium full-suite CI execution
* representative Firefox Smoke CI execution
* representative WebKit Smoke CI execution
* Firefox/WebKit cross-browser Smoke matrix
* independent E2E purchase-journey checkpoints
* pytest-html reporting
* browser-specific Firefox/WebKit pytest-html reporting
* Allure result collection and HTML generation
* configurable failure screenshot evidence
* configurable Playwright trace generation
* configurable Playwright video generation
* browser-specific GitHub Actions reporting artifacts

## Current Pytest Markers

Current executable marker categories are:

* `smoke`
* `regression`
* `ui`
* `security`
* `sorting`
* `navigation`
* `e2e`

The marker strategy supports several independent dimensions of test intent.

A test may therefore use multiple markers when appropriate.

Examples:

```text
Smoke / UI
Regression / UI
Smoke / Navigation
Regression / Navigation
Smoke / Navigation / E2E
```

Current marker intent:

* `smoke` — fast representative validation of critical functionality
* `regression` — broader validation across expanded or full applicable cases
* `ui` — visibility, presentation, state, and direct UI behavior
* `security` — authentication access control and protected-route validation
* `sorting` — product sorting behavior
* `navigation` — meaningful page transitions excluding the authentication Login → Inventory transition
* `e2e` — independent checkpoints that together form the primary purchase journey

Detailed marker semantics are documented in:

```text
docs/testing-strategy.md
```

Runtime configuration, diagnostics, reporting, browser selection, and pytest-xdist distribution do not change marker meaning or assignment.

Phase 5A does not introduce a separate cross-browser marker.

The existing `smoke` marker is reused for representative Firefox and WebKit compatibility validation.

## Browser Automation

### Playwright

Playwright is the primary browser automation library.

It provides:

* browser automation
* locators
* navigation
* built-in waiting
* browser contexts
* assertions
* tracing
* video recording
* multi-browser engine support

The framework uses Playwright through the pytest-playwright integration rather than manually owning browser startup and shutdown.

The currently implemented browser-engine execution strategy covers:

* Chromium
* Firefox
* WebKit

with different validation responsibilities.

Chromium is the primary complete regression browser.

Firefox and WebKit provide representative Smoke compatibility validation.

### pytest-playwright

pytest-playwright provides the Pytest integration layer for Playwright.

The framework uses its fixture and runtime model, including:

* browser selection
* browser lifecycle
* `new_context`
* `context`
* `page`
* headed execution
* native browser runtime options
* trace capabilities
* video capabilities

Phase 4E extends this model with centralized project runtime configuration.

Phase 4F preserves the same pytest-playwright browser, trace, and video ownership model.

Phase 5A reuses the same integration to execute representative Smoke coverage on Firefox and WebKit.

The project does not manually create and own Playwright browser processes.

The project also does not implement duplicate custom trace or video lifecycle management.

## Browser Configuration

The runtime configuration layer recognizes:

```text
chromium
firefox
webkit
```

through:

```text
QA_BROWSER
```

Default:

```text
chromium
```

This allows browser-engine selection to remain centralized outside functional tests.

Explicit native pytest-playwright browser selection remains usable.

### Current Browser Validation Strategy

The implemented browser strategy is intentionally asymmetric.

#### Chromium

Chromium is the default and primary complete regression browser.

Current Chromium execution includes:

* dedicated Smoke CI
* dedicated Regression CI
* complete full-suite CI
* local sequential execution
* local pytest-xdist parallel execution
* pytest-html reporting
* complete full-suite Allure reporting in CI

Chromium CI installation:

```bash
playwright install --with-deps chromium
```

#### Firefox

Firefox is a representative Smoke compatibility browser.

Current Firefox execution includes:

* local Smoke validation
* GitHub Actions Smoke validation
* pytest-xdist worker-level execution
* browser-specific pytest-html reporting
* browser-specific CI artifacts

Firefox CI installation:

```bash
playwright install --with-deps firefox
```

Representative local execution:

```bash
QA_BROWSER=firefox pytest -m smoke -n auto -v
```

#### WebKit

WebKit is a representative Smoke compatibility browser.

Current WebKit execution includes:

* local Smoke validation
* GitHub Actions Smoke validation
* pytest-xdist worker-level execution
* browser-specific pytest-html reporting
* browser-specific CI artifacts

WebKit CI installation:

```bash
playwright install --with-deps webkit
```

Representative local execution:

```bash
QA_BROWSER=webkit pytest -m smoke -n auto -v
```

### Cross-Browser Scope Boundary

The current framework does not claim complete equal-depth coverage across all three engines.

Firefox and WebKit do not currently execute:

* the complete Regression suite
* the complete full suite
* duplicate browser-specific functional tests
* browser-specific application coverage

Phase 5A also does not introduce:

* a cross-browser pytest marker
* Firefox-specific test modules
* WebKit-specific test modules
* browser-specific application assertions
* browser-specific skip logic without a demonstrated compatibility limitation
* Selenium

The same Page Objects, fixtures, runtime configuration, assertions, and Smoke tests are reused across engines.

## Current Automated UI Coverage

Current automation includes:

* Sauce Demo availability smoke validation
* successful login validation
* invalid credential validation
* empty credential validation
* locked out user validation
* Login UI behavior
* authentication error handling
* protected Inventory route validation
* protected Cart route validation
* protected Product Details route validation
* protected Checkout Information route validation
* protected Checkout Overview route validation
* protected Checkout Complete route validation
* Inventory page validation
* product list validation
* product card content validation
* Inventory → Product Details navigation
* Product Details validation
* Product Details Add to cart behavior
* Product Details Remove behavior
* product sorting
* Cart page validation
* empty Cart validation
* Add to cart behavior from Inventory and Product Details
* cart badge validation
* Cart item visibility and content validation
* Remove behavior from Inventory, Product Details, and Cart
* Continue Shopping navigation
* Cart state persistence after logout and re-login
* Cart → Checkout Information navigation
* Checkout Information form validation
* Checkout required-field validation
* Checkout error-state behavior
* Checkout Overview product validation
* Checkout Overview price summary validation
* Checkout Overview cancellation
* Product Details navigation from Checkout Overview
* Finish navigation to Checkout Complete
* Checkout Complete confirmation validation
* Back Home navigation
* independent primary purchase E2E checkpoints

The functional coverage is shared by the browser execution strategy.

Phase 5A changes where representative Smoke scenarios execute rather than introducing new product-facing functional coverage.

## Page Object Model

Currently implemented:

* `BasePage`
* `AppPage`
* `LoginPage`
* `InventoryPage`
* `ProductDetailsPage`
* `CartPage`
* `CheckoutInformationPage`
* `CheckoutOverviewPage`
* `CheckoutCompletePage`

### BasePage

`BasePage` provides:

* shared Playwright `Page` storage
* application-relative `ROUTE` metadata
* runtime URL composition
* shared direct page opening behavior

Application URLs are composed from:

```text
settings.base_url + PageObject.ROUTE + optional suffix
```

This means the target application origin is not hardcoded independently in each Page Object.

The configured origin is provided by:

```text
QA_BASE_URL
```

through:

```text
config/settings.py
```

### AppPage

`AppPage` provides shared authenticated application behavior.

Current responsibilities include:

* Cart access
* cart badge access
* application menu interaction
* logout
* reset app state
* All Items navigation
* About link access
* reusable product-like item behavior where appropriate

### Page-Specific Responsibilities

Current Page Object responsibilities include:

* Login navigation
* username input
* password input
* Login submission
* authentication error handling
* Login UI locator access
* Inventory visibility and product access
* Inventory product sorting
* Product Details navigation
* Product Details content access
* Inventory Cart actions
* Product Details Cart actions
* Cart item lookup
* Cart item content access
* Cart item removal
* Continue Shopping
* Checkout entry
* Checkout Information interaction
* Checkout validation errors
* Checkout Overview content
* Checkout Overview price summary access
* Checkout cancellation
* Product Details navigation from Checkout Overview
* Finish action
* Checkout Complete confirmation
* Back Home navigation

Page Objects should not independently own:

* environment-variable parsing
* browser lifecycle configuration
* browser-specific execution branching without demonstrated need
* runtime diagnostic hooks
* failure diagnostics
* reporting setup
* trace configuration
* video configuration
* screenshot policy parsing

Those concerns belong to the runtime, diagnostics, Pytest integration, and execution layers.

The current Phase 5A implementation does not require browser-specific Page Object behavior.

## Reusable Assertions

Currently implemented:

```text
framework/assertions/product_assertions.py
```

Current reusable assertion responsibilities include:

* Inventory product card validation
* Product Details validation
* Cart item validation
* Checkout Overview product validation
* Checkout Overview price summary validation
* Inventory product-state validation after navigation
* product price conversion for numeric sorting and checkout calculations

Reusable assertion helpers remain focused on validation logic.

They should not own:

* navigation
* browser setup
* fixture setup
* runtime configuration
* browser-specific execution branching without demonstrated need
* diagnostics
* reporting configuration
* screenshot capture
* trace recording
* video recording

Phase 5A does not require browser-specific assertion helpers.

## Test Data Management

Currently implemented:

* centralized login test data
* centralized product test data
* centralized checkout test data
* valid user credentials
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
* valid checkout customer data
* checkout required-field validation messages
* checkout page title expectations
* Checkout Overview summary expectations
* Checkout Complete expectations
* deterministic product data shared across Inventory, Product Details, Cart, and Checkout tests
* manual test case IDs in parametrized output where practical

Current files:

```text
test_data/login_test_data.py
test_data/product_test_data.py
test_data/checkout_test_data.py
```

Centralized test data represents reusable test input.

It does not create shared browser state between tests or xdist workers.

Runtime configuration is a separate concern and is not stored in test data modules.

Browser selection is runtime configuration rather than browser-specific test data.

Diagnostics are also separate from test data.

Potential future test-data expansion may include:

* API-specific datasets
* additional approved UI datasets
* environment-specific functional data if explicitly required by future scope

## Fixture Technology And Responsibility

Pytest fixtures provide reusable test setup.

Phase 4F establishes two explicit fixture and Pytest integration locations.

Framework-level Pytest integration remains in:

```text
conftest.py
```

Application scenario fixtures are located in:

```text
tests/conftest.py
```

### Root `conftest.py`

Current framework-level responsibilities include:

* project runtime configuration integration
* pytest-playwright browser option integration
* headed/headless integration
* Playwright trace policy integration
* Playwright video policy integration
* Playwright assertion timeout setup
* BrowserContext action timeout setup
* BrowserContext navigation timeout setup
* runtime diagnostic header
* failed-test diagnostics
* custom failure screenshot handling
* Allure failure screenshot attachment

The project-level `context` fixture uses pytest-playwright's:

```text
new_context
```

fixture rather than implementing its own browser lifecycle.

The same framework integration is reused for Chromium, Firefox, and WebKit execution.

### `tests/conftest.py`

Current application scenario fixtures are:

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

These fixtures provide deterministic application states for:

* Login
* authenticated Inventory
* Cart preparation
* Checkout Information preparation
* Checkout Overview preparation
* Checkout Complete preparation
* independent E2E checkpoints

Fixture names remain explicit and scenario-oriented.

The existing function-scoped model remains compatible with sequential and pytest-xdist worker-level execution.

The same scenario fixtures are reused across supported browser engines.

Phase 4F does not introduce:

* generic fixture factories
* dependency-injection infrastructure
* autouse fixture redesign
* multi-layer fixture packages
* fixture scope redesign

Phase 5A does not introduce:

* Firefox-specific fixtures
* WebKit-specific fixtures
* browser-specific fixture branches

## Runtime Configuration

Phase 4E provides centralized environment-based runtime configuration through:

```text
config/settings.py
```

The configuration layer is responsible for:

* runtime defaults
* environment-variable loading
* normalization
* validation
* exposing immutable settings to the framework

Current supported environment variables are:

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

Phase 4F does not introduce additional runtime environment variables.

Phase 5A reuses the existing `QA_BROWSER` configuration rather than adding another browser-selection mechanism.

## Base URL Configuration

`QA_BASE_URL` controls the application origin.

Default:

```text
https://www.saucedemo.com
```

The configured value must:

* use HTTP or HTTPS
* contain a valid host
* represent only the application origin
* not contain credentials
* not contain query parameters
* not contain a fragment
* not contain whitespace
* contain a valid port if a port is supplied

A trailing slash is normalized away.

Example:

```bash
QA_BASE_URL="http://localhost:8000" pytest -m smoke -v
```

The configured base URL is consumed by `BasePage`.

Tests and Page Objects therefore do not need environment-specific URL modifications.

## Headed And Headless Configuration

`QA_HEADED` controls headed versus headless execution.

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

Example:

```bash
QA_HEADED=true pytest -m smoke -v
```

The native pytest-playwright `--headed` option remains usable.

Current CI explicitly uses:

```text
QA_HEADED=false
```

for Chromium, Firefox, and WebKit browser-test execution.

CI therefore remains headless.

## Playwright Timeout Configuration

### Action And Navigation Timeout

Configured through:

```text
QA_TIMEOUT_MS
```

Default:

```text
30000
```

The value is applied as:

* Playwright default action timeout
* Playwright default navigation timeout

Example:

```bash
QA_TIMEOUT_MS=45000 pytest -m regression -v
```

### Assertion Timeout

Configured through:

```text
QA_EXPECT_TIMEOUT_MS
```

Default:

```text
5000
```

The value configures Playwright `expect()` assertions.

Example:

```bash
QA_EXPECT_TIMEOUT_MS=7000 pytest -m smoke -v
```

Both timeout settings require non-negative integer values expressed in milliseconds.

A value of `0` is accepted and follows Playwright timeout semantics.

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

When a browser test fails during the Pytest `call` phase and a Playwright page is available:

* the screenshot hook captures one PNG
* the file is written under `reports/screenshots/`
* the same PNG is attached to Allure when Allure result collection is active
* the successful screenshot path is included in the Phase 4F failed-test diagnostic summary

The framework does not introduce a duplicate pytest-playwright screenshot implementation.

When:

```text
QA_SCREENSHOT_POLICY=off
```

the custom screenshot is not written and the corresponding Allure screenshot attachment is not created.

Setup and teardown failures continue to receive Phase 4F failed-test diagnostics but do not trigger this custom screenshot mechanism.

The same screenshot policy is used during Chromium, Firefox, and WebKit CI browser execution.

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

Trace recording uses pytest-playwright / Playwright capabilities.

The project does not implement a custom trace recorder.

When enabled, generated trace output uses pytest-playwright runtime artifact storage rooted under:

```text
test-results/
```

Representative output:

```text
trace.zip
```

Explicit native pytest-playwright trace options remain usable and take precedence when explicitly supplied.

Phase 4F does not change trace lifecycle ownership.

Phase 5A does not change trace lifecycle ownership.

Trace remains disabled in current CI by default for all browser-test executions.

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

Video recording uses pytest-playwright / Playwright capabilities.

The project does not implement a custom video recorder.

Generated runtime output uses the pytest-playwright artifact structure rooted under:

```text
test-results/
```

Representative output:

```text
video.webm
```

Explicit native pytest-playwright video options remain usable and take precedence when explicitly supplied.

Phase 4F does not change video lifecycle ownership.

Phase 5A does not change video lifecycle ownership.

Video remains disabled in current CI by default for all browser-test executions.

## Runtime Configuration Validation

Focused runtime configuration validation is implemented in:

```text
tests/test_runtime_config.py
```

The tests cover:

* default values
* base URL normalization
* invalid base URLs
* browser normalization
* invalid browser values
* headed boolean parsing
* invalid headed values
* timeout parsing
* invalid timeout values
* screenshot policy values
* trace policy values
* video policy values
* invalid artifact policy values

The browser configuration tests validate:

* Chromium
* Firefox
* WebKit

Invalid explicit runtime values fail early.

The framework does not silently replace an invalid explicit value with a default.

Phase 5A uses this existing validated browser configuration surface.

## Runtime Configuration Boundaries

The current runtime configuration layer does not implement:

* named environment profiles
* automatic `.env` loading
* device emulation
* mobile emulation
* browser channels
* slow-motion configuration
* retries

Cross-browser CI execution itself is now implemented through Phase 5A and consumes the existing runtime browser setting.

The runtime configuration layer still does not define:

* complete Firefox Regression responsibility
* complete WebKit Regression responsibility
* complete Firefox full-suite responsibility
* complete WebKit full-suite responsibility

Phase 4F diagnostics and fixture responsibility cleanup are implemented separately from runtime configuration.

Runtime configuration should remain focused on approved execution concerns.

## Runtime Diagnostics

Phase 4F adds lightweight diagnostic support through:

```text
framework/diagnostics.py
```

and framework-level Pytest hooks in:

```text
conftest.py
```

The diagnostics module uses Python's standard:

```text
logging
```

module.

No additional logging package is required.

### Runtime Summary

The effective runtime summary is emitted through:

```text
pytest_report_header
```

Current runtime summary fields are:

* application base URL
* browser
* headed/headless mode
* action/navigation timeout
* assertion timeout
* screenshot policy
* trace policy
* video policy

Representative output:

```text
[runtime] base_url=... | browser=... | mode=... | action_navigation_timeout_ms=... | assertion_timeout_ms=... | screenshot=... | trace=... | video=...
```

The summary reflects effective runtime values after applicable project configuration and native pytest-playwright command-line options have been resolved.

The same diagnostic mechanism applies to Chromium, Firefox, and WebKit execution.

During pytest-xdist execution, worker processes do not emit duplicate runtime summaries.

### Failed-Test Diagnostics

Failed-test summaries support failed Pytest reports from:

```text
setup
call
teardown
```

Each summary includes:

* Pytest node ID
* failure phase

When a Playwright page is available, the framework also attempts to include:

* current page URL

When a custom screenshot has been captured successfully, the framework additionally includes:

* screenshot path

Representative output:

```text
[failure] test=<node-id> | phase=<phase> | url=<current-url> | screenshot=<path>
```

Optional fields are included only when the corresponding values are available.

### Diagnostic Error Reporting

Diagnostic evidence collection can itself fail.

Current diagnostic operations include:

```text
page-url
screenshot
allure-attachment
```

Representative output:

```text
[diagnostic-error] operation=<operation> | test=<node-id> | phase=<phase> | error=<error>
```

Diagnostic errors are:

* emitted through the project diagnostics logger
* added to the failed Pytest report diagnostic sections

The diagnostics logger is named:

```text
qa_automation.diagnostics
```

The project does not configure persistent project log files.

## Diagnostic Scope Boundaries

The current diagnostics layer does not implement:

* persistent project log files
* browser console capture
* network capture
* custom network tracing
* HTML dumps
* page-source dumps
* automatic trace enablement
* automatic video enablement
* retries
* hosted diagnostic reporting
* additional diagnostic-specific CI jobs

Trace and video remain pytest-playwright-owned capabilities.

Phase 5A does not introduce browser-specific diagnostic implementations.

## Code Quality And Development Tooling

Current quality tools:

* Ruff
* Black
* isort
* pre-commit

Responsibilities:

* static analysis
* formatting
* import organization
* automated local quality gates
* dedicated CI quality validation

Tool configuration is stored in:

```text
pyproject.toml
.pre-commit-config.yaml
pytest.ini
```

Current configured tools include:

```text
Ruff
Black
isort
```

Standard local quality validation:

```bash
ruff check .
black --check .
isort . --check-only
pytest -v
```

The same Ruff, Black, and isort checks execute in the dedicated CI `quality` job.

The quality job does not:

* run browser tests
* install Playwright browsers
* use pytest-xdist
* require browser runtime configuration

Phase 4F did not introduce an additional code-quality tool.

Phase 5A also does not introduce another code-quality tool.

## Test Execution Strategy

The project supports both sequential and pytest-xdist worker-level parallel execution.

### Sequential Full Suite

```bash
pytest -v
```

Sequential execution remains supported for:

* standard local development
* focused debugging
* failure reproduction
* controlled diagnostics validation
* validation where parallel execution is unnecessary

The default browser is Chromium.

### Parallel Full Suite

```bash
pytest -n auto -v
```

`-n auto` delegates worker-count selection to pytest-xdist.

The complete unfiltered suite executes through pytest-xdist in the Chromium GitHub Actions `full-suite` job.

### Marker-Based Local Execution

Sequential:

```bash
pytest -m smoke -v
pytest -m regression -v
pytest -m ui -v
pytest -m security -v
pytest -m sorting -v
pytest -m navigation -v
pytest -m e2e -v
```

Approved Chromium parallel commands:

```bash
pytest -m smoke -n auto -v
pytest -m regression -n auto -v
pytest -n auto -v
```

Approved representative cross-browser Smoke commands:

```bash
QA_BROWSER=firefox pytest -m smoke -n auto -v
QA_BROWSER=webkit pytest -m smoke -n auto -v
```

Useful combinations:

```bash
pytest -m "smoke and ui" -v
pytest -m "regression and ui" -v
pytest -m "smoke and navigation" -v
pytest -m "regression and navigation" -v
```

Marker expressions may also be scoped to a module.

Example:

```bash
pytest tests/test_checkout_page.py -m e2e -v
```

Dedicated Chromium CI marker jobs currently exist for:

* `smoke`
* `regression`

The existing Smoke suite is additionally executed on:

* Firefox
* WebKit

through the dedicated cross-browser matrix.

The following markers do not currently have dedicated CI jobs:

* `ui`
* `security`
* `sorting`
* `navigation`
* `e2e`

Tests carrying those markers still participate in complete Chromium full-suite CI execution.

Tests that also carry `smoke` additionally participate in Firefox and WebKit representative compatibility validation.

## Runtime-Aware Local Execution

Runtime environment variables can be combined with normal Pytest execution.

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

Representative Firefox execution:

```bash
QA_BROWSER=firefox pytest -m smoke -n auto -v
```

Representative WebKit execution:

```bash
QA_BROWSER=webkit pytest -m smoke -n auto -v
```

Phase 4F runtime diagnostics automatically display the effective configuration during normal Pytest execution.

No additional diagnostics command is required.

## Parallel-Safety Model

Current worker-level execution relies on:

* function-scoped Playwright browser state
* independent test preparation
* independent scenario fixture chains
* no test-order dependencies
* no state created by one test being consumed by another
* independent parametrized cases
* independent E2E checkpoints
* process-level runtime configuration
* diagnostics that do not depend on shared cross-worker state

Phase 4F fixture responsibility separation preserves this model.

Phase 5A reuses the same worker-safety model on Firefox and WebKit Smoke execution.

The current suite remains compatible with:

* sequential execution
* pytest-xdist worker-level execution
* representative Chromium Smoke execution
* representative Firefox Smoke execution
* representative WebKit Smoke execution

No sequential-only test or diagnostic exception is required.

No browser-specific fixture or state-management exception was required for Phase 5A.

## GitHub Actions

GitHub Actions provides the implemented CI platform.

Current job structure:

```text
quality
├── smoke [Chromium]
├── regression [Chromium]
├── full-suite [Chromium]
└── cross-browser-smoke
    ├── Firefox
    └── WebKit
```

The `quality` job executes first.

Chromium Smoke, Chromium Regression, Chromium full-suite, Firefox Smoke, and WebKit Smoke all require successful quality validation.

The browser-test executions do not depend on each other.

Phase 4C adds pytest-xdist inside browser-test jobs.

Phase 4D adds Allure reporting to the Chromium full-suite job.

Phase 4E adds explicit runtime configuration to browser-test jobs.

Phase 4F adds diagnostics through the existing Pytest execution path.

Phase 5A adds representative Firefox and WebKit Smoke execution through a dedicated matrix.

## CI Runtime Defaults

Current Chromium Smoke, Regression, and full-suite jobs use:

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

The Firefox/WebKit `cross-browser-smoke` matrix uses the same runtime settings except that:

```text
QA_BROWSER=${{ matrix.browser }}
```

resolves to:

```text
firefox
```

or:

```text
webkit
```

The current CI execution model is:

* Chromium Smoke
* Chromium Regression
* Chromium complete full suite
* Firefox representative Smoke
* WebKit representative Smoke
* headless
* pytest-xdist parallel
* screenshot-on-failure enabled
* trace disabled by default
* video disabled by default
* Phase 4F runtime diagnostics active through Pytest

The current implementation does not add:

* complete Firefox Regression
* complete WebKit Regression
* complete Firefox full-suite execution
* complete WebKit full-suite execution
* workflow-dispatch runtime forms
* secrets for these non-secret defaults
* retries
* default trace retention
* default video retention
* diagnostic-specific environment variables

## Smoke Job

The dedicated `smoke` job is the Chromium Smoke execution path.

It:

* depends on `quality`
* installs dependencies
* resolves explicit runtime defaults
* installs Chromium
* executes Smoke through pytest-xdist
* emits Phase 4F runtime diagnostics through normal Pytest execution
* generates a self-contained pytest-html report
* uploads Smoke-specific artifacts

Core command:

```bash
pytest -m smoke -n auto -v
```

Report:

```text
reports/smoke-report.html
```

Chromium Smoke remains pytest-html-focused.

It does not generate a dedicated Allure report.

## Regression Job

The dedicated `regression` job is the Chromium Regression execution path.

It:

* depends on `quality`
* installs dependencies
* resolves explicit runtime defaults
* installs Chromium
* executes Regression through pytest-xdist
* emits Phase 4F runtime diagnostics through normal Pytest execution
* generates a self-contained pytest-html report
* uploads Regression-specific artifacts

Core command:

```bash
pytest -m regression -n auto -v
```

Report:

```text
reports/regression-report.html
```

Chromium Regression remains pytest-html-focused.

It does not generate a dedicated Allure report.

## Full-Suite Job

The `full-suite` job is the complete Chromium regression gate.

It:

* depends on `quality`
* installs dependencies
* resolves explicit runtime defaults
* configures Java 17
* installs the Allure CLI
* installs Chromium
* executes the complete unfiltered suite through pytest-xdist
* emits Phase 4F diagnostics through normal Pytest execution
* generates pytest-html
* collects Allure result data
* generates the Allure HTML report when usable results exist
* uploads full-suite artifacts
* uploads the dedicated Allure report artifact

Current command:

```bash
pytest -n auto -v \
  --html=reports/report.html \
  --self-contained-html \
  --alluredir=reports/allure-results \
  --clean-alluredir
```

Outputs:

```text
reports/report.html
reports/allure-results/
reports/allure-report/
```

The full-suite job remains the complete CI regression gate.

Chromium Smoke and Regression provide targeted feedback but do not replace it.

Firefox and WebKit Smoke provide additional representative compatibility feedback but do not replace it.

## Cross-Browser Smoke Job

The `cross-browser-smoke` job provides representative Firefox and WebKit validation through a matrix.

Current matrix:

```text
firefox
webkit
```

The matrix uses:

```yaml
needs: quality

strategy:
  fail-fast: false
  matrix:
    browser:
      - firefox
      - webkit
```

Each matrix execution:

* installs project dependencies
* uses `QA_BROWSER=${{ matrix.browser }}`
* installs only its current browser engine
* executes the existing Smoke suite
* uses pytest-xdist with `-n auto`
* runs headless
* uses the same runtime timeout and artifact policies
* emits Phase 4F runtime diagnostics
* generates a browser-specific pytest-html report
* uploads browser-specific artifacts

Browser installation:

```bash
playwright install --with-deps ${{ matrix.browser }}
```

Core command:

```bash
pytest -m smoke -n auto -v
```

Report path:

```text
reports/${{ matrix.browser }}-smoke-report.html
```

Resolved report paths:

```text
reports/firefox-smoke-report.html
reports/webkit-smoke-report.html
```

Chromium is intentionally excluded from this matrix because it already has dedicated Smoke, Regression, and full-suite jobs.

Firefox and WebKit do not generate dedicated Allure reports.

## Allure CI Prerequisites

The Chromium full-suite job uses:

* Java 17
* Allure CLI

Java setup:

```text
actions/setup-java@v4
```

Distribution:

```text
Temurin 17
```

Allure CLI installation:

```bash
npm install -g allure-commandline
allure --version
```

These prerequisites are needed only for converting Allure result data into an HTML report.

They are not required in:

* Chromium Smoke
* Chromium Regression
* Firefox Smoke
* WebKit Smoke

Phase 4F diagnostics do not require Java or Allure CLI.

## CI Dependencies And Concurrency

All browser-test jobs use:

```yaml
needs: quality
```

After successful quality validation, GitHub Actions may execute:

```text
smoke [Chromium]
regression [Chromium]
full-suite [Chromium]
cross-browser-smoke (firefox)
cross-browser-smoke (webkit)
```

independently.

The Firefox and WebKit executions originate from the same matrix definition.

The matrix uses:

```yaml
fail-fast: false
```

so one cross-browser failure does not cancel the other browser execution.

This is GitHub Actions job-level and matrix-level concurrency.

Inside each browser execution, pytest-xdist distributes tests between workers.

This is worker-level parallelism.

The execution layers are distinct:

```text
quality
├── smoke [Chromium]
│   └── xdist workers
├── regression [Chromium]
│   └── xdist workers
├── full-suite [Chromium]
│   └── xdist workers
└── cross-browser-smoke
    ├── Firefox
    │   └── xdist workers
    └── WebKit
        └── xdist workers
```

Reporting, runtime configuration, and diagnostics are layered on top of this model.

They do not create another execution layer.

## Current CI Targets

The workflow runs automatically for:

* pushes to `main`
* pushes to `develop`
* Pull Requests targeting `main`
* Pull Requests targeting `develop`

The workflow can also run manually through:

```text
workflow_dispatch
```

Regular pushes to feature, refactor, fix, or documentation branches do not automatically trigger CI unless the branch participates in a Pull Request targeting `main` or `develop`, or the workflow is manually started.

## Workflow Permissions

Current GitHub Actions permissions:

```yaml
permissions:
  contents: read
```

No elevated repository permissions are required for the current workflow.

Runtime defaults and browser matrix values are non-secret values and do not require GitHub Actions secrets.

## Reporting And Debugging

Currently implemented:

* Pytest console output
* Phase 4F runtime summary
* Phase 4F failed-test summaries
* Phase 4F diagnostic-error reporting
* pytest-html
* self-contained HTML reports
* Chromium Smoke pytest-html reporting
* Chromium Regression pytest-html reporting
* Chromium full-suite pytest-html reporting
* Firefox Smoke pytest-html reporting
* WebKit Smoke pytest-html reporting
* allure-pytest result collection
* local Allure HTML generation
* Chromium full-suite CI Allure result collection
* Chromium full-suite CI Allure HTML generation
* configurable screenshot capture on failed test calls
* screenshot path diagnostics
* Allure screenshot attachments
* configurable trace generation
* configurable video generation
* `reports/` runtime output
* pytest-playwright `test-results/` diagnostic output
* GitHub Actions artifacts
* separate artifacts for Chromium Smoke, Chromium Regression, Chromium full-suite, Firefox Smoke, and WebKit Smoke
* reporting and diagnostics behavior compatible with parallel execution

## pytest-html

pytest-html remains the lightweight reporting solution.

Current Chromium CI paths:

```text
reports/smoke-report.html
reports/regression-report.html
reports/report.html
```

Current cross-browser Smoke paths:

```text
reports/firefox-smoke-report.html
reports/webkit-smoke-report.html
```

Chromium Smoke, Chromium Regression, Chromium full-suite, Firefox Smoke, and WebKit Smoke retain pytest-html reporting.

Allure does not replace pytest-html.

Phase 4F diagnostics also do not replace pytest-html.

## Allure Pytest Integration

`allure-pytest` provides Pytest-side result generation.

Current result location:

```text
reports/allure-results/
```

Sequential collection:

```bash
pytest -v \
  --alluredir=reports/allure-results \
  --clean-alluredir
```

Parallel collection:

```bash
pytest -n auto -v \
  --alluredir=reports/allure-results \
  --clean-alluredir
```

The existing project screenshot is reused as the Allure failure screenshot attachment when applicable.

The current CI Allure responsibility remains with the complete Chromium `full-suite` job.

Firefox and WebKit Smoke do not currently generate dedicated Allure results or reports.

## Allure CLI

The standalone Allure CLI converts result data into a browsable HTML report.

Command:

```bash
allure generate reports/allure-results \
  --clean \
  -o reports/allure-report
```

Output:

```text
reports/allure-report/
```

The Allure CLI is an external prerequisite.

It is separate from the Python `allure-pytest` package.

## GitHub Actions Artifacts

Current Chromium Smoke artifacts:

```text
smoke-pytest-html-report
smoke-test-artifacts
```

Current Chromium Regression artifacts:

```text
regression-pytest-html-report
regression-test-artifacts
```

Current Chromium full-suite artifacts:

```text
pytest-html-report
full-suite-allure-report
test-artifacts
```

Current Firefox Smoke artifacts:

```text
firefox-smoke-pytest-html-report
firefox-smoke-test-artifacts
```

Current WebKit Smoke artifacts:

```text
webkit-smoke-pytest-html-report
webkit-smoke-test-artifacts
```

The dedicated Chromium Allure artifact publishes:

```text
reports/allure-report/
```

The broader Chromium full-suite runtime artifact publishes:

```text
reports/
```

The Firefox and WebKit broader runtime artifacts also publish their own matrix execution:

```text
reports/
```

Browser-specific artifact names keep the Firefox and WebKit matrix outputs independent.

Artifact upload steps use:

```yaml
if: always()
```

This allows available reports and runtime outputs to be published even when an executing browser-test command fails.

Current artifact retention:

```text
7 days
```

Trace and video are disabled in CI by default and therefore are not currently uploaded as dedicated CI artifacts.

Phase 4F does not add a persistent diagnostics artifact.

## Generated Runtime Output

Generated reports and persistent diagnostic evidence are runtime output.

Current generated locations include:

```text
reports/
reports/screenshots/
reports/allure-results/
reports/allure-report/
test-results/
playwright-report/
```

Generated output is not repository source content and should not be committed.

This includes:

* pytest-html reports
* Firefox and WebKit browser-specific pytest-html reports
* Allure result files
* generated Allure HTML reports
* failure screenshots
* trace ZIP files
* recorded video files
* other Playwright execution artifacts

Phase 4F runtime and failed-test summaries do not create another persistent output directory.

Persistent project diagnostic log files are not implemented.

## Reporting And Diagnostic Scope Boundaries

Currently not implemented:

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
* retries
* Firefox Allure reporting in CI
* WebKit Allure reporting in CI
* complete three-browser full-suite reporting
* default trace retention in CI
* default video retention in CI

Trace and video runtime policies themselves are implemented.

They remain disabled by default.

Phase 4F runtime and failed-test diagnostics are implemented.

Phase 5A browser-specific pytest-html reporting is implemented.

## API Testing

Currently installed:

* `requests`

Current status:

* API testing is not implemented
* API tests are not part of the current suite
* `api` is not a current executable pytest marker

Potential future API usage may include:

* API smoke validation
* backend validation
* hybrid UI and API scenarios
* API-based test data setup
* API-based test data cleanup

The presence of `requests` prepares the framework for possible future API work.

It does not mean an API testing layer currently exists.

## Test Execution Optimization

Currently implemented:

* pytest-xdist

Current status:

* worker-level parallel Pytest execution is implemented locally
* worker-level parallel execution is implemented in Chromium Smoke CI
* worker-level parallel execution is implemented in Chromium Regression CI
* worker-level parallel execution is implemented in Chromium full-suite CI
* worker-level parallel execution is implemented in Firefox Smoke CI
* worker-level parallel execution is implemented in WebKit Smoke CI
* sequential execution remains supported
* runtime configuration is compatible with both execution modes
* Phase 4F diagnostics are compatible with both execution modes
* application scenario fixtures remain compatible with worker-level execution

Approved primary Chromium parallel commands:

```bash
pytest -m smoke -n auto -v
pytest -m regression -n auto -v
pytest -n auto -v
```

Approved representative additional-browser commands:

```bash
QA_BROWSER=firefox pytest -m smoke -n auto -v
QA_BROWSER=webkit pytest -m smoke -n auto -v
```

Parallel-safety validation covers:

* fixture isolation
* browser-state isolation
* Cart and Checkout state assumptions
* logout and re-login persistence
* E2E checkpoint independence
* parametrized scenario independence
* failure screenshot behavior
* report output behavior
* runtime configuration
* Phase 4F fixture separation
* Phase 4F diagnostic behavior
* representative Firefox Smoke execution
* representative WebKit Smoke execution

No sequential-only test exception is required.

No browser-specific parallel execution exception was required for Phase 5A.

GitHub Actions job concurrency, matrix expansion, and pytest-xdist worker concurrency remain distinct mechanisms.

## Version And Dependency Management

Current dependency files:

* `requirements.txt`
* `requirements-lock.txt`

Current usage:

* `requirements.txt` provides the readable dependency declaration
* `requirements-lock.txt` provides locked dependency versions for reproducible local and CI installation

Direct dependencies declared in `requirements.txt` are:

```text
pytest
playwright
pytest-playwright
requests
allure-pytest
pytest-html
pytest-xdist
ruff
black
isort
pre-commit
```

Currently integrated dependencies include:

* `pytest`
* `playwright`
* `pytest-playwright`
* `allure-pytest`
* `pytest-html`
* `pytest-xdist`
* `ruff`
* `black`
* `isort`
* `pre-commit`

Installed for future expansion:

* `requests`

Installed dependencies should not be treated as implemented framework capabilities unless actively integrated.

Specifically:

* pytest-xdist is an implemented execution capability
* allure-pytest is an implemented reporting capability
* pytest-playwright is an implemented Playwright/Pytest and runtime integration capability
* requests does not mean API automation is implemented

Phase 4F diagnostics rely on Python's built-in `logging` module and therefore do not require an additional Python package.

Phase 5A reuses existing Playwright, pytest-playwright, pytest-xdist, and pytest-html dependencies and does not require an additional Python package.

The standalone Allure CLI is not managed through the Python dependency files.

It remains a separate prerequisite for Allure HTML generation.

Potential future dependency-management improvements may include:

* dependency update automation
* optional dependency grouping if the project grows

## Development Environment

Current documented local development environment includes:

* Windows host
* WSL2 with Ubuntu Linux
* Python virtual environment
* PyCharm Community
* Git
* GitHub
* Playwright
* Chromium
* Firefox
* WebKit
* Pytest
* pytest-playwright
* pytest-xdist
* pytest-html
* allure-pytest
* standalone Allure CLI when local Allure HTML generation is required

This setup supports Linux-based local sequential and parallel execution while remaining aligned with GitHub Actions.

Chromium is used for complete local and CI regression validation.

Firefox and WebKit are used for representative Smoke compatibility validation.

Runtime configuration uses normal process environment variables and does not require `.env` file support.

Phase 4F diagnostics require no external logging service or persistent logging installation.

## Current Phase Boundaries

### Phase 4B — CI Execution Strategy

Implemented:

* separate CI quality validation
* dedicated Smoke CI execution
* dedicated Regression CI execution
* complete full-suite CI execution
* explicit quality-gate dependencies
* job-specific pytest-html reports
* job-specific GitHub Actions artifacts
* independent browser-job scheduling after `quality`

These statements describe the Phase 4B implementation scope.

### Phase 4C — Parallel Execution

Implemented:

* pytest-xdist worker-level execution
* local parallel execution
* supported sequential execution
* fixture and browser-state isolation validation
* Cart and Checkout parallel-safety validation
* parametrized and E2E independence
* parallel Smoke CI
* parallel Regression CI
* parallel full-suite CI
* preservation of Phase 4B job structure
* preservation of pytest-html reports and artifacts
* Chromium-only CI browser execution for the Phase 4C workstream

GitHub Actions job-level concurrency and pytest-xdist worker-level parallelism remain separate mechanisms.

No sequential-only test exception is required.

Phase 5A later reuses the same xdist execution model for Firefox and WebKit Smoke validation.

### Phase 4D — Reporting Upgrade

Implemented:

* allure-pytest integration
* local Allure result collection
* local Allure HTML generation
* Allure CLI as an HTML-generation prerequisite
* failure screenshot attachment to Allure
* reuse of the existing screenshot mechanism
* sequential reporting compatibility
* pytest-xdist reporting compatibility
* full-suite Allure result collection in CI
* full-suite Allure HTML generation in CI
* dedicated `full-suite-allure-report` artifact
* preservation of pytest-html
* preservation of existing browser-test artifacts
* generated reporting output outside repository source content
* Chromium-only browser scope for the Phase 4D reporting workstream

Phase 4D did not implement:

* Allure history persistence
* trend-history storage
* report hosting
* GitHub Pages reporting
* retries
* cross-browser reporting

These statements describe the Phase 4D workstream boundary.

Phase 5A later adds browser-specific pytest-html reporting for Firefox and WebKit Smoke while preserving Chromium full-suite Allure responsibility.

Trace/video runtime policy and environment-driven execution configuration were added in Phase 4E.

### Phase 4E — Runtime Configuration

Implemented:

* centralized `config/settings.py`
* environment-based runtime configuration
* configurable application base URL
* configurable browser engine
* configurable headed/headless execution
* configurable action and navigation timeout
* configurable assertion timeout
* configurable screenshot policy
* configurable trace policy
* configurable video policy
* normalization of string values
* predictable boolean parsing
* timeout validation
* base URL validation
* fail-fast invalid explicit configuration
* focused runtime configuration tests
* integration with `BasePage`
* integration with pytest-playwright through root `conftest.py`
* preservation of native pytest-playwright runtime options where applicable
* explicit runtime defaults in Smoke, Regression, and full-suite CI jobs
* preservation of Chromium-only CI for the Phase 4E workstream
* preservation of Phase 4B–4D job topology
* preservation of parallel execution
* preservation of pytest-html and Allure reporting
* preservation of existing CI artifact names and retention

Phase 4E did not implement:

* named environment profiles
* `.env` loading
* CI browser matrices
* Firefox or WebKit CI installation
* cross-browser CI compatibility claims
* device emulation
* browser channels
* retries

These statements describe the Phase 4E implementation boundary.

Phase 5A later consumes the browser-engine configuration capability already implemented in Phase 4E.

Phase 4E remains the implemented runtime configuration foundation.

### Phase 4F — Diagnostics And Fixture Cleanup

Implemented:

* `framework/diagnostics.py`
* runtime summary formatting
* failed-test summary formatting
* diagnostic error formatting
* lightweight project diagnostics logger
* effective runtime summary through `pytest_report_header`
* base URL visibility
* effective browser visibility
* headed/headless mode visibility
* action/navigation timeout visibility
* assertion timeout visibility
* screenshot policy visibility
* trace policy visibility
* video policy visibility
* suppression of duplicated runtime summaries on pytest-xdist workers
* failed-test Pytest node ID reporting
* `setup`, `call`, and `teardown` failure-phase reporting
* current page URL reporting when a Playwright page is available
* custom screenshot path reporting after successful screenshot capture
* diagnostic error reporting for page URL retrieval
* diagnostic error reporting for screenshot creation
* diagnostic error reporting for Allure attachment
* framework-level Pytest integration retained in root `conftest.py`
* application scenario fixtures separated into `tests/conftest.py`
* explicit scenario fixture naming
* preserved function-scoped fixture model
* preserved pytest-playwright browser lifecycle
* preserved pytest-playwright trace lifecycle
* preserved pytest-playwright video lifecycle
* preserved custom screenshot implementation
* preserved Allure failure screenshot reuse
* preserved existing reporting architecture
* preserved existing Phase 4 CI topology
* sequential execution compatibility
* pytest-xdist execution compatibility

Phase 4F did not implement:

* persistent project log files
* browser console capture
* network capture
* custom network tracing
* HTML or page-source dumps
* automatic trace enablement
* automatic video enablement
* retries
* new CI jobs
* generic fixture factories
* dependency-injection infrastructure
* autouse fixture redesign
* multi-layer fixture packages
* fixture scope redesign

These statements describe the Phase 4F implementation boundary.

Phase 5A later reuses the same diagnostics and fixture responsibilities for Firefox and WebKit Smoke validation.

### Phase 5A — Playwright Cross-Browser Validation

Implemented:

* Chromium retained as the primary complete regression browser
* existing Chromium Smoke execution preserved
* existing Chromium Regression execution preserved
* existing Chromium complete full-suite execution preserved
* local Firefox Smoke validation
* local WebKit Smoke validation
* dedicated Firefox/WebKit `cross-browser-smoke` CI matrix
* matrix limited to Firefox and WebKit
* `needs: quality`
* `fail-fast: false`
* selected-engine-only Playwright installation
* reuse of the existing `smoke` marker
* reuse of existing functional test modules
* reuse of existing Page Objects
* reuse of existing application scenario fixtures
* reuse of centralized runtime configuration
* `QA_BROWSER` supplied from the matrix browser value
* pytest-xdist `-n auto` execution
* browser-specific Firefox pytest-html report
* browser-specific WebKit pytest-html report
* independent Firefox artifact names
* independent WebKit artifact names
* preservation of Chromium full-suite Allure reporting
* preservation of Phase 4F diagnostics
* preservation of existing failure screenshot policy

Phase 5A does not implement:

* complete Firefox Regression
* complete WebKit Regression
* complete Firefox full-suite execution
* complete WebKit full-suite execution
* complete three-browser regression parity
* a new cross-browser marker
* duplicate Firefox-specific tests
* duplicate WebKit-specific tests
* browser-specific application coverage
* Selenium
* browser-specific conditionals or skips without a demonstrated compatibility limitation

Formal Phase 5A roadmap completion remains owned by the dedicated closing checkpoint task.

## Phase 4F Validation Status

Final Phase 4F validation confirmed:

```text
Smoke: 31 passed
Regression: 109 passed
Full sequential: 236 passed
Full pytest-xdist: 236 passed
Ruff: passed
Black check: passed
isort: passed
```

Controlled failure validation after fixture responsibility separation additionally confirmed:

* runtime header
* failure phase
* Pytest node ID
* current page URL
* screenshot diagnostic path

Phase 4F does not require an additional technology dependency beyond the existing stack.

## Phase 5A Validation Status

Phase 5A local validation confirmed:

```text
Firefox Smoke: 31 passed
WebKit Smoke: 31 passed
Chromium full-suite: 236 passed
Ruff: passed
Black check: passed
isort: passed
```

No Firefox- or WebKit-specific compatibility workaround was required.

GitHub Actions validation confirmed successful execution of:

* `quality`
* Chromium `smoke`
* Chromium `regression`
* Chromium `full-suite`
* `cross-browser-smoke (firefox)`
* `cross-browser-smoke (webkit)`

This validates the implemented Phase 5A browser responsibility model without expanding complete Regression or full-suite execution beyond Chromium.

## Planned Integrations

Potential future integrations include:

* Selenium WebDriver comparison
* Docker-based execution
* named environment profiles
* `.env` loading if explicitly approved
* expanded test data utilities
* Jenkins CI integration
* complete Firefox or WebKit Regression/full-suite execution if future scope requires it
* advanced Allure history and analytics
* hosted reporting
* API testing
* reusable framework packaging
* persistent structured logging if future requirements justify it
* additional browser diagnostic evidence if explicitly approved

The following are no longer future-only capabilities because they are implemented in Phase 5A:

* Firefox Smoke CI execution
* WebKit Smoke CI execution
* Firefox/WebKit CI matrix execution
* browser-specific Firefox/WebKit pytest-html reports
* browser-specific Firefox/WebKit GitHub Actions artifacts
* representative Playwright cross-browser compatibility validation

These integrations and future extensions should not be described as implemented until their corresponding project scope is completed and validated.

## Current Stack Status

The current technology stack supports automated functional coverage for:

* Login
* Inventory
* Product Details
* Cart
* Checkout

Current implemented technical capabilities include:

* UI automation with Playwright
* pytest-playwright integration
* Chromium as the default browser
* Chromium as the primary complete regression browser
* Firefox representative Smoke compatibility validation
* WebKit representative Smoke compatibility validation
* Chromium, Firefox, and WebKit runtime engine selection
* Pytest test execution
* pytest-xdist worker-level parallel execution
* supported sequential execution
* Page Object Model
* shared authenticated-page behavior through `AppPage`
* reusable assertions
* explicit scenario-oriented fixtures
* separated framework and scenario fixture responsibilities
* centralized test data
* centralized runtime configuration
* parametrization
* normalized marker organization
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
* local Firefox Smoke execution
* local WebKit Smoke execution
* local quality checks
* runtime application URL overrides
* browser runtime selection
* headed/headless runtime selection
* Playwright timeout configuration
* assertion timeout configuration
* failure screenshot policy
* trace policy
* video policy
* runtime value validation
* effective runtime diagnostic summary
* pytest-xdist runtime-header de-duplication
* failed-test node ID diagnostics
* setup/call/teardown failure-phase diagnostics
* current URL diagnostics when available
* custom screenshot path diagnostics
* diagnostic error reporting
* Python standard-library diagnostics logging
* GitHub Actions CI
* dedicated CI quality validation
* dedicated parallel Chromium Smoke CI
* dedicated parallel Chromium Regression CI
* parallel complete Chromium full-suite CI
* representative parallel Firefox Smoke CI
* representative parallel WebKit Smoke CI
* Firefox/WebKit cross-browser Smoke matrix
* explicit CI runtime defaults
* Phase 4F diagnostics through existing Pytest execution
* pytest-html reporting
* Firefox browser-specific pytest-html reporting
* WebKit browser-specific pytest-html reporting
* Allure result collection
* Allure HTML generation
* sequential and parallel Allure compatibility
* screenshot capture on failed test calls
* failure screenshot attachment to Allure
* optional Playwright trace generation
* optional Playwright video generation
* pytest-playwright trace and video ownership
* Chromium job-specific CI artifacts
* Firefox browser-specific CI artifacts
* WebKit browser-specific CI artifacts
* dedicated full-suite Allure report artifact
* generated runtime output isolation
* technical documentation

Current CI execution model:

```text
runtime defaults
        ↓
Phase 4F runtime diagnostics
        ↓
quality
├── smoke [Chromium]
│   └── pytest-xdist workers
│       └── pytest-html
├── regression [Chromium]
│   └── pytest-xdist workers
│       └── pytest-html
├── full-suite [Chromium]
│   └── pytest-xdist workers
│       ├── pytest-html
│       ├── Allure results
│       ├── failure screenshots
│       └── Allure HTML report
└── cross-browser-smoke
    ├── Firefox
    │   └── pytest-xdist workers
    │       └── pytest-html
    └── WebKit
        └── pytest-xdist workers
            └── pytest-html
```

UI, Security, Sorting, Navigation, and E2E remain selectively executable without dedicated CI jobs.

Parallel execution with pytest-xdist is implemented locally and in all browser-test CI executions.

Allure reporting is implemented locally and in the complete Chromium full-suite CI reporting path.

Runtime configuration is implemented locally and integrated across Chromium, Firefox, and WebKit execution.

Phase 4F diagnostics are implemented locally and operate through the existing Pytest execution path across browser-test CI execution.

Framework-level Pytest integration is separated from application scenario fixtures.

Current CI is headless.

Chromium remains the primary complete regression browser.

Firefox and WebKit execute representative Smoke validation only.

Trace and video policies are implemented but disabled in CI by default.

The following are not currently implemented:

* Allure history persistence
* hosted reporting
* named environment profiles
* automatic `.env` loading
* API testing
* Docker execution
* complete Firefox Regression
* complete WebKit Regression
* complete Firefox full-suite execution
* complete WebKit full-suite execution
* complete three-browser regression parity
* retries
* device emulation
* persistent project log files
* browser console capture
* network capture
* HTML or page-source dumps
* automatic trace enablement
* automatic video enablement
* generic fixture factories
* dependency-injection infrastructure
* autouse fixture redesign
* multi-layer fixture packages
* fixture scope redesign
* Selenium execution

The `main` branch remains the stable portfolio version of the project.

The `develop` branch and active workstream branches may contain newer validated changes before promotion.

Future stack expansion should remain clearly separated from currently implemented capabilities.