# Technology Stack

This document describes the technologies, tools, framework capabilities, and planned integrations used in the QA automation project.

The stack is divided into:

* implemented technologies
* active framework integrations
* supporting development tooling
* explicit current-scope boundaries
* planned future extensions

The `main` branch represents the stable portfolio version of the project.

The `develop` branch and active workstream branches may contain newer validated framework maturity work before promotion to `main`.

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

These technologies form the implemented UI automation, execution, runtime configuration, reporting, and CI foundation.

## Test Automation

Current implemented test automation stack:

* Playwright for browser automation
* Pytest as the test runner
* pytest-playwright for Playwright and Pytest integration
* pytest-xdist for worker-level parallel execution
* Page Object Model for page interaction abstraction
* shared authenticated-page behavior through `AppPage`
* reusable assertion helpers
* pytest fixtures for reusable setup
* pytest parametrization for data-driven scenarios
* centralized test data
* centralized runtime configuration
* explicit pytest markers
* strict marker validation
* selective marker-based execution
* sequential execution
* parallel Smoke execution
* parallel Regression execution
* parallel full-suite execution
* dedicated Smoke CI execution
* dedicated Regression CI execution
* complete full-suite CI execution
* independent E2E purchase-journey checkpoints
* pytest-html reporting
* Allure result collection and HTML generation
* configurable failure screenshot evidence
* configurable Playwright trace generation
* configurable Playwright video generation

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

Runtime configuration does not change marker meaning or assignment.

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

### pytest-playwright

pytest-playwright provides the Pytest integration layer for Playwright.

The framework uses its existing fixture and runtime model, including:

* browser selection
* browser lifecycle
* `new_context`
* `context`
* `page`
* native browser runtime options
* trace capabilities
* video capabilities

Phase 4E extends this model rather than replacing it.

The project does not manually create and own Playwright browser processes.

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

This means the framework can resolve Playwright browser-engine configuration through the centralized runtime layer.

It does not mean that all supported engines are installed or validated in every execution environment.

### Current CI Browser Scope

GitHub Actions remains intentionally Chromium-only.

Current CI installation:

```bash
playwright install --with-deps chromium
```

CI does not currently install:

* Firefox
* WebKit

The current framework therefore does not claim validated cross-browser CI compatibility.

Explicit native pytest-playwright browser selection remains usable.

A local execution may use another supported engine when that browser is installed in the local Playwright environment.

Cross-browser CI, browser matrices, and broader compatibility validation remain future extensions.

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
* reporting setup
* trace configuration
* video configuration
* screenshot policy parsing

Those concerns belong to the runtime and Pytest integration layers.

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
* reporting configuration
* screenshot capture
* trace recording
* video recording

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

Potential future test-data expansion may include:

* API-specific datasets
* additional approved UI datasets
* environment-specific functional data if explicitly required by future scope

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

and remains headless.

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

When a browser test fails during the Pytest call phase:

* the screenshot hook captures one PNG
* the file is written under `reports/screenshots/`
* the same PNG is attached to Allure when Allure result collection is active

The framework does not introduce a duplicate pytest-playwright screenshot implementation.

When:

```text
QA_SCREENSHOT_POLICY=off
```

the custom screenshot is not written and the corresponding Allure screenshot attachment is not created.

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

Invalid explicit runtime values fail early.

The framework does not silently replace an invalid explicit value with a default.

## Runtime Configuration Boundaries

The current runtime configuration layer does not implement:

* named environment profiles
* automatic `.env` loading
* CI browser matrices
* cross-browser CI execution
* device emulation
* mobile emulation
* browser channels
* slow-motion configuration
* retries
* Phase 4F logging redesign
* Phase 4F fixture cleanup

Runtime configuration should remain focused on approved execution concerns.

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
* install Chromium
* use pytest-xdist
* require browser runtime configuration

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
* validation where parallel execution is unnecessary

### Parallel Full Suite

```bash
pytest -n auto -v
```

`-n auto` delegates worker-count selection to pytest-xdist.

The complete unfiltered suite executes through pytest-xdist in the GitHub Actions `full-suite` job.

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

Approved parallel commands:

```bash
pytest -m smoke -n auto -v
pytest -m regression -n auto -v
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

Dedicated CI marker jobs currently exist only for:

* `smoke`
* `regression`

The following markers do not currently have dedicated CI jobs:

* `ui`
* `security`
* `sorting`
* `navigation`
* `e2e`

Tests carrying those markers still participate in complete full-suite CI execution.

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

These values alter execution configuration without changing functional test code.

Runtime configuration is compatible with:

* sequential execution
* marker-based execution
* pytest-xdist execution
* pytest-html
* Allure result collection

## Parallel-Safety Expectations

The execution model relies on test independence.

Validated expectations include:

* tests do not depend on execution order
* tests do not depend on state created by previous tests
* Playwright browser state remains isolated through the existing fixture model
* Cart and Checkout scenarios prepare their own required state
* parametrized scenarios remain independently executable
* E2E checkpoints remain independently executable
* tests do not depend on a specific xdist worker
* runtime configuration is process-level execution configuration rather than test-to-test shared state

No sequential-only test exceptions were identified during Phase 4C validation.

## E2E Execution Model

The current `e2e` suite represents independent checkpoints that collectively form the primary purchase journey.

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
* prepare required state through fixtures or test setup
* do not depend on test execution order
* do not share state produced by previous tests

Run:

```bash
pytest -m e2e -v
```

E2E currently remains a selectively executable marker suite without a dedicated GitHub Actions job.

Its tests remain included in complete full-suite CI execution and may execute on different xdist workers.

When the full-suite job collects Allure results, E2E tests are represented in the advanced full-suite report.

Runtime configuration applies to E2E in the same way as to the remaining Pytest suites.

## CI/CD And Automation

Current CI technology:

* GitHub Actions

The current CI execution model combines:

* Phase 4B CI structure
* Phase 4C parallel execution
* Phase 4D reporting
* Phase 4E runtime configuration

Current job structure:

```text
quality
├── smoke
├── regression
└── full-suite
```

## Quality Job

The `quality` job is the prerequisite CI quality gate.

Current responsibilities:

* repository checkout
* Python 3.12 setup
* dependency installation from `requirements-lock.txt`
* Ruff validation
* Black validation
* isort validation

Commands:

```bash
ruff check .
black --check .
isort . --check-only
```

The quality job does not install Chromium or execute browser tests.

If `quality` fails, Smoke, Regression, and full-suite do not execute.

## CI Browser Runtime Defaults

The three browser-test jobs use:

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

These values match the approved local runtime defaults.

The CI execution model remains:

* Chromium-only
* headless
* pytest-xdist parallel
* screenshot-on-failure enabled
* trace disabled by default
* video disabled by default

Phase 4E does not add:

* CI matrices
* additional browser installations
* workflow-dispatch runtime forms
* secrets for these non-secret defaults
* retries
* default trace retention
* default video retention

## Smoke Job

The dedicated Smoke job:

* depends on `quality`
* installs dependencies
* resolves explicit Phase 4E runtime defaults
* installs Chromium
* executes Smoke through pytest-xdist
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

Smoke remains pytest-html-focused.

It does not generate a dedicated Allure report.

## Regression Job

The dedicated Regression job:

* depends on `quality`
* installs dependencies
* resolves explicit Phase 4E runtime defaults
* installs Chromium
* executes Regression through pytest-xdist
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

Regression remains pytest-html-focused.

It does not generate a dedicated Allure report.

## Full-Suite Job

The `full-suite` job:

* depends on `quality`
* installs dependencies
* resolves explicit Phase 4E runtime defaults
* configures Java 17
* installs the Allure CLI
* installs Chromium
* executes the complete unfiltered suite through pytest-xdist
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

Smoke and Regression provide targeted feedback but do not replace it.

## Allure CI Prerequisites

The full-suite job uses:

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

They are not required in Smoke or Regression.

## CI Dependencies And Concurrency

All browser jobs use:

```yaml
needs: quality
```

Smoke, Regression, and full-suite do not depend on each other.

GitHub Actions may therefore schedule them concurrently after successful quality validation.

This is job-level concurrency.

Inside each browser job, pytest-xdist distributes tests between workers.

This is worker-level parallelism.

The two execution layers are distinct:

```text
quality
├── smoke
│   └── xdist workers
├── regression
│   └── xdist workers
└── full-suite
    └── xdist workers
```

Reporting and runtime configuration are layered on top of this model.

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

Runtime defaults are non-secret values and do not require GitHub Actions secrets.

## Reporting And Debugging

Currently implemented:

* Pytest console output
* pytest-html
* self-contained HTML reports
* allure-pytest result collection
* local Allure HTML generation
* full-suite CI Allure result collection
* full-suite CI Allure HTML generation
* configurable screenshot capture on test failure
* Allure screenshot attachments
* configurable trace generation
* configurable video generation
* `reports/` runtime output
* pytest-playwright `test-results/` diagnostic output
* GitHub Actions artifacts
* separate artifacts for Smoke, Regression, and full-suite
* reporting behavior compatible with parallel execution

## pytest-html

pytest-html remains the lightweight reporting solution.

Current CI paths:

```text
reports/smoke-report.html
reports/regression-report.html
reports/report.html
```

Smoke, Regression, and full-suite retain pytest-html reporting.

Allure does not replace it.

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

The broader full-suite runtime artifact publishes:

```text
reports/
```

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

## Generated Runtime Output

Generated reports and diagnostic evidence are runtime output.

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
* Allure result files
* generated Allure HTML reports
* failure screenshots
* trace ZIP files
* recorded video files
* other Playwright execution artifacts

## Reporting Scope Boundaries

Currently not implemented:

* Allure history persistence
* trend-history storage
* hosted Allure reports
* GitHub Pages reporting
* retries
* cross-browser reporting
* default trace retention in CI
* default video retention in CI

Trace and video runtime policies themselves are implemented.

They remain disabled by default.

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
* worker-level parallel execution is implemented in Smoke CI
* worker-level parallel execution is implemented in Regression CI
* worker-level parallel execution is implemented in full-suite CI
* sequential execution remains supported
* runtime configuration is compatible with both execution modes

Approved parallel commands:

```bash
pytest -m smoke -n auto -v
pytest -m regression -n auto -v
pytest -n auto -v
```

Phase 4C parallel-safety validation covered:

* fixture isolation
* browser-state isolation
* Cart and Checkout state assumptions
* logout and re-login persistence
* E2E checkpoint independence
* parametrized scenario independence
* failure screenshot behavior
* report output behavior

No sequential-only test exceptions were identified.

GitHub Actions job concurrency and pytest-xdist worker concurrency remain distinct mechanisms.

## Version And Dependency Management

Current dependency files:

* `requirements.txt`
* `requirements-lock.txt`

Current usage:

* `requirements.txt` provides the readable dependency declaration
* `requirements-lock.txt` provides locked dependency versions for reproducible local and CI installation

Main installed dependencies include:

* `pytest`
* `playwright`
* `pytest-playwright`
* `requests`
* `allure-pytest`
* `pytest-html`
* `pytest-xdist`
* `ruff`
* `black`
* `isort`
* `pre-commit`

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

The standalone Allure CLI is not managed through the Python dependency files.

It remains a separate prerequisite for Allure HTML generation.

Potential future dependency-management improvements may include:

* dependency update automation
* optional dependency grouping if the project grows

## Development Environment

Current local development environment includes:

* Windows host
* WSL2 with Ubuntu Linux
* Python virtual environment
* PyCharm Community
* Git
* GitHub
* Playwright
* Pytest
* pytest-playwright
* pytest-xdist
* pytest-html
* allure-pytest
* standalone Allure CLI when local Allure HTML generation is required

This setup supports Linux-based local sequential and parallel execution while remaining aligned with GitHub Actions.

Runtime configuration uses normal process environment variables and does not require `.env` file support.

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

### Phase 4C — Parallel Execution

Implemented:

* pytest-xdist worker-level execution
* local parallel execution
* supported sequential fallback
* fixture and browser-state isolation validation
* Cart and Checkout parallel-safety validation
* parametrized and E2E independence
* parallel Smoke CI
* parallel Regression CI
* parallel full-suite CI
* preservation of Phase 4B job structure
* preservation of pytest-html reports and artifacts
* Chromium-only CI browser execution

GitHub Actions job-level concurrency and pytest-xdist worker-level parallelism remain separate mechanisms.

No sequential-only test exceptions were identified.

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

Phase 4D does not implement:

* Allure history persistence
* trend-history storage
* report hosting
* GitHub Pages reporting
* retries
* cross-browser reporting

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
* integration with pytest-playwright through `conftest.py`
* preservation of native pytest-playwright runtime options where applicable
* explicit runtime defaults in Smoke, Regression, and full-suite CI jobs
* preservation of Chromium-only CI
* preservation of Phase 4B–4D job topology
* preservation of parallel execution
* preservation of pytest-html and Allure reporting
* preservation of existing CI artifact names and retention

Phase 4E does not implement:

* named environment profiles
* `.env` loading
* CI browser matrices
* Firefox or WebKit CI installation
* cross-browser CI compatibility claims
* device emulation
* browser channels
* retries
* Phase 4F logging redesign
* Phase 4F fixture cleanup

Formal Phase 4E completion in `docs/roadmap.md` remains deferred to the dedicated Phase 4E checkpoint.

## Planned Integrations

Potential future integrations include:

* Selenium WebDriver comparison
* Docker-based execution
* named environment profiles
* `.env` loading if explicitly approved
* expanded test data utilities
* Jenkins CI integration
* cross-browser CI execution
* browser matrices
* advanced Allure history and analytics
* hosted reporting
* API testing
* reusable framework packaging

These integrations are future extensions and should not be described as implemented until they are added, validated, and documented.

## Current Stack Status

The current technology stack supports automated coverage for:

* Login
* Inventory
* Product Details
* Cart
* Checkout

Current implemented technical capabilities include:

* UI automation with Playwright
* pytest-playwright integration
* Chromium as the default and current CI browser
* recognition of Chromium, Firefox, and WebKit runtime engine values
* Pytest test execution
* pytest-xdist worker-level parallel execution
* supported sequential execution
* Page Object Model
* shared authenticated-page behavior through `AppPage`
* reusable assertions
* reusable fixtures
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
* GitHub Actions CI
* dedicated CI quality validation
* dedicated parallel Smoke CI
* dedicated parallel Regression CI
* parallel complete full-suite CI
* explicit Phase 4E CI runtime defaults
* pytest-html reporting
* Allure result collection
* Allure HTML generation
* sequential and parallel Allure compatibility
* screenshot capture on failure
* failure screenshot attachment to Allure
* optional Playwright trace generation
* optional Playwright video generation
* job-specific CI artifacts
* dedicated full-suite Allure report artifact
* generated runtime output isolation
* technical documentation

Current CI execution model:

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

UI, Security, Sorting, Navigation, and E2E remain selectively executable without dedicated CI jobs.

Parallel execution with pytest-xdist is implemented locally and in all three browser-test CI jobs.

Allure reporting is implemented locally and in the complete full-suite CI reporting path.

Runtime configuration is implemented locally and integrated into Smoke, Regression, and full-suite CI execution.

Current CI remains intentionally Chromium-only and headless.

Trace and video policies are implemented but disabled in CI by default.

The following are not currently implemented:

* Allure history persistence
* hosted reporting
* named environment profiles
* automatic `.env` loading
* API testing
* Docker execution
* CI browser matrices
* retries
* device emulation
* cross-browser CI execution
* Phase 4F logging and fixture cleanup

The `main` branch remains the stable portfolio version of the project.

The `develop` branch and active workstream branches may contain newer validated changes before promotion.

Future stack expansion should remain clearly separated from currently implemented capabilities.