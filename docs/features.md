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
* representative Playwright cross-browser validation
* reproducible Docker-based Playwright execution
* controlled visual regression testing

The implemented browser strategy uses:

* Chromium as the primary complete regression browser
* Firefox as a representative Smoke compatibility browser
* WebKit as a representative Smoke compatibility browser

API testing, Selenium comparison, Jenkins integration, Allure history persistence, hosted reporting, environment profiles, retries, and persistent diagnostic logging remain future extensions unless explicitly described as implemented below.

Phase 5B Docker-based Playwright execution is implemented and is part of the current framework feature set.

Phase 5C Visual Regression Testing is also implemented through AQA-0118–AQA-0120. It adds Pillow-based PNG comparison, approved Chromium baselines, isolated visual checkpoints, explicit baseline refresh, controlled defect demonstration, and a dedicated Docker-based visual CI job. Formal Phase 5C roadmap completion remains reserved for AQA-0122.

# Currently Implemented

## Test Execution

Current execution capabilities include:

* UI automation using Playwright
* Pytest-based test execution
* pytest-playwright integration
* Chromium as the default browser
* Chromium as the primary complete regression browser
* representative Firefox Smoke validation
* representative WebKit Smoke validation
* centralized pytest configuration
* strict pytest marker validation
* marker-based selective local execution
* sequential local Pytest execution
* pytest-xdist worker-level parallel execution
* parallel Smoke execution
* parallel Regression execution
* parallel full-suite execution
* local Firefox Smoke execution
* local WebKit Smoke execution
* Docker-based Playwright execution
* sequential Pytest execution inside Docker
* pytest-xdist parallel execution inside Docker
* reuse of existing `QA_*` runtime configuration inside Docker
* Chromium Smoke validation inside Docker
* Firefox Smoke validation inside Docker through `QA_BROWSER=firefox`
* host-persistent reports and browser artifacts through bind mounts
* dedicated Chromium Smoke CI execution
* dedicated Chromium Regression CI execution
* complete unfiltered Chromium automated test-suite execution
* complete Chromium automated test-suite execution in CI
* dedicated Firefox/WebKit cross-browser Smoke matrix
* representative Firefox Smoke CI execution
* representative WebKit Smoke CI execution
* pytest-xdist execution inside all current functional browser-test CI executions
* centralized environment-based runtime configuration
* lightweight runtime diagnostics
* failed-test diagnostic context
* browser-specific Firefox/WebKit pytest-html reporting
* browser-specific Firefox/WebKit CI artifacts
* dedicated visual regression test suite outside the normal functional `tests/` collection
* dedicated Chromium-only `visual` marker execution
* sequential visual regression execution without pytest-xdist
* canonical Docker-based visual execution
* dedicated Docker-based Chromium visual regression CI execution

Current executable pytest markers:

* `smoke`
* `regression`
* `ui`
* `security`
* `sorting`
* `navigation`
* `e2e`
* `visual`

Current suite capabilities include:

* representative Smoke validation
* controlled screenshot-regression validation through selected visual checkpoints
* broader Regression validation
* direct UI behavior validation
* protected-route Security validation
* product Sorting validation
* page-transition Navigation validation
* independent E2E purchase-journey checkpoint validation
* supported sequential execution
* validated worker-level parallel execution
* representative browser-engine compatibility validation

Approved primary Chromium parallel execution commands:

```bash
pytest -m smoke -n auto -v
pytest -m regression -n auto -v
pytest -n auto -v
```

Approved representative cross-browser commands:

```bash
QA_BROWSER=firefox pytest -m smoke -n auto -v
QA_BROWSER=webkit pytest -m smoke -n auto -v
```

Sequential execution remains supported:

```bash
pytest -m smoke -v
pytest -m regression -v
pytest -v
```

The dedicated visual suite is intentionally isolated from the normal functional collection. `pytest.ini` keeps `testpaths = tests`, while visual checks live under `visual_tests/` and are selected explicitly.

Detailed marker and execution semantics are documented in:

```text
docs/testing-strategy.md
```

Phase 5A does not introduce a new cross-browser pytest marker.

The existing `smoke` suite provides the representative Firefox and WebKit validation surface.

The `visual` marker is Chromium-only and does not participate in the Firefox/WebKit cross-browser matrix.

## Containerized Playwright Execution

Phase 5B adds a reproducible Docker execution path for the existing Playwright/Pytest framework.

The containerized execution path complements:

* local WSL/Linux execution
* native functional GitHub Actions execution

It does not replace either of them.

Phase 5C additionally reuses the same Dockerfile for one dedicated visual regression GitHub Actions job. Existing functional CI jobs remain native.

The repository-root `Dockerfile` uses the official Playwright Python image:

```text
mcr.microsoft.com/playwright/python:v1.60.0-noble
```

The image version is aligned with:

```text
playwright==1.60.0
```

in:

```text
requirements-lock.txt
```

The Docker image installs the project's locked Python dependencies but does not run a separate `playwright install` step because the official Playwright image already provides the corresponding browser binaries and Linux browser dependencies.

Build command:

```bash
docker build -t playwright-qa-framework:local .
```

Validated sequential Chromium Smoke execution:

```bash
docker run --rm --init --ipc=host \
  playwright-qa-framework:local \
  -m smoke -v
```

Validated pytest-xdist execution includes both explicit worker counts and `-n auto`.

Example controlled automatic-worker execution:

```bash
docker run --rm --init --ipc=host \
  -e PYTEST_XDIST_AUTO_NUM_WORKERS=2 \
  playwright-qa-framework:local \
  -m smoke -n auto -v
```

The Docker environment reuses the existing runtime configuration surface.

Example Firefox execution:

```bash
docker run --rm --init --ipc=host \
  -e QA_BROWSER=firefox \
  playwright-qa-framework:local \
  -m smoke -v
```

No Docker-specific equivalents of the existing `QA_*` variables are introduced.

The same configuration surface remains responsible for:

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

Validated Docker browser execution includes:

* Chromium Smoke
* Firefox Smoke through `QA_BROWSER=firefox`

The Playwright image also contains WebKit, but Phase 5B does not claim a separately validated Docker WebKit execution.

Generated output that must survive container removal is persisted through bind mounts.

Validated host-persistent artifact categories include:

* pytest-html reports
* raw Allure result data
* failure screenshots
* Playwright traces
* Playwright videos

Relevant host output locations include:

```text
reports/
allure-results/
test-results/
```

When running the container with the current WSL/Linux user's UID and GID:

```bash
--user "$(id -u):$(id -g)"
```

Pytest cache can be redirected to:

```bash
-o cache_dir=/tmp/pytest_cache
```

to avoid write-permission warnings under `/app`.

Recommended Docker runtime flags are:

```text
--rm
--init
--ipc=host
```

The Docker image includes `allure-pytest`, allowing raw Allure result data to be generated during container execution.

The image does not package:

* the standalone Allure CLI
* Java for Allure HTML generation
* Node.js for Allure CLI installation

Allure HTML generation therefore remains outside the Docker image.

The existing functional GitHub Actions jobs continue to execute natively on GitHub-hosted Ubuntu runners.

Those native jobs:

* install Python dependencies directly
* install the selected Playwright browser directly
* invoke Pytest directly
* publish GitHub Actions artifacts directly

Phase 5C adds one exception: the dedicated `visual-regression` job builds the existing project Docker image and runs only the isolated visual suite inside it.

Phase 5B itself did not implement:

* Docker Compose
* Kubernetes
* Dockerized Sauce Demo
* Selenium
* visual regression
* Docker-specific functional tests
* Docker-specific CI jobs
* a Docker-specific runtime configuration layer

Those statements describe the Phase 5B implementation boundary. Phase 5C later adds visual regression and reuses the unchanged Phase 5B Docker execution environment for its dedicated CI job.

Docker is therefore an additional reproducible execution path around the existing framework rather than a replacement for the current local or CI execution models.

## Visual Regression Testing

Phase 5C implements controlled visual regression as a separate validation capability alongside functional UI assertions.

Functional tests continue to verify application behavior and state through Playwright locators, assertions, Page Objects, fixtures, and reusable assertion helpers. Visual regression verifies selected rendered UI checkpoints against reviewed PNG baselines.

Current visual regression implementation includes:

* dedicated `framework/visual_regression.py` comparison responsibility
* Pillow-based PNG loading and pixel comparison
* image-size validation
* changed-pixel counting and changed-region bounds
* generated magenta-highlighted diff PNGs on mismatch
* failure when an approved baseline is missing
* dedicated `visual_tests/` suite outside the normal functional `tests/` collection
* dedicated `visual` Pytest marker
* approved Chromium baseline ownership under `visual_baselines/chromium/`
* generated actual screenshots under `reports/visual/actual/`
* generated diff screenshots under `reports/visual/diff/`
* explicit baseline refresh through `--update-visual-baselines`
* Chromium-only and headless execution guard
* fixed visual rendering conditions
* canonical Docker-based execution
* dedicated Docker-based visual CI job
* independent visual artifact upload

### Visual Regression Versus Functional Assertions

Visual comparison does not replace functional assertions.

The selected visual checkpoints first prepare and validate meaningful application state with normal Playwright assertions. Screenshot comparison then adds presentation-level regression detection for that already-valid state.

```text
functional assertions
    → behavior and application state

visual regression
    → rendered UI appearance at selected checkpoints
```

### Visual Regression Versus Failure Screenshots

The visual screenshot lifecycle is separate from the existing failure screenshot mechanism.

Failure screenshots:

* are controlled by `QA_SCREENSHOT_POLICY`
* are captured by the root Pytest failure integration
* are diagnostic evidence for failed test calls
* are stored under `reports/screenshots/`
* may be attached to Allure

Visual screenshots:

* are captured intentionally by `visual_tests/`
* are produced for selected visual checkpoints
* are compared against approved baselines
* write actual images under `reports/visual/actual/`
* write mismatch diffs under `reports/visual/diff/`
* are independent of the failure screenshot policy

### Approved Visual Checkpoints

The permanent visual suite currently validates two approved `standard_user` states:

* Inventory default page
* Cart containing one **Sauce Labs Backpack**

Approved baselines:

```text
visual_baselines/chromium/inventory-default.png
visual_baselines/chromium/cart-one-product.png
```

These files are reviewed repository assets. Generated actual and diff files are runtime outputs and are not committed.

### Canonical Visual Environment

Canonical visual execution uses:

* repository `Dockerfile`
* `mcr.microsoft.com/playwright/python:v1.60.0-noble`
* Playwright 1.60.0 from `requirements-lock.txt`
* Chromium only
* headless mode
* 1280 × 720 viewport
* device scale factor 1
* light color scheme
* reduced motion
* disabled screenshot animations
* hidden caret
* CSS screenshot scale
* PNG screenshot format
* decoded product images before capture
* sequential execution without pytest-xdist

`visual_tests/conftest.py` rejects Firefox, WebKit, mixed/non-Chromium browser selection, and headed execution. This protects Chromium baselines from accidental cross-browser comparison or refresh.

### Visual Execution

Focused direct execution:

```bash
python -m pytest visual_tests -m visual --browser chromium -v
```

Canonical comparison:

```bash
docker build -t playwright-qa-framework:visual .

mkdir -p reports/visual

docker run --rm --init --ipc=host \
  -v "$PWD/visual_baselines:/app/visual_baselines:ro" \
  -v "$PWD/reports/visual:/app/reports/visual" \
  -e QA_BASE_URL=https://www.saucedemo.com \
  -e QA_BROWSER=chromium \
  -e QA_HEADED=false \
  playwright-qa-framework:visual \
  visual_tests -m visual --browser chromium -v
```

The baseline mount is read-only during normal comparison.

### Explicit Baseline Refresh

Approved baselines are never refreshed implicitly.

Intentional maintenance requires `--update-visual-baselines`, a writable baseline mount in the canonical Docker environment, and human review of the changed PNGs before commit.

CI never runs baseline refresh.

### Controlled `visual_user` Mismatch Validation

`test_data/login_test_data.py` contains separate `VISUAL_USER` credentials for controlled visual-regression validation.

AQA-0119 used `visual_user` for a one-off comparison against the approved `standard_user` Inventory baseline. That deliberate validation produced:

```text
43,909 differing pixels
4.76% of the image
```

and generated:

```text
reports/visual/diff/inventory-visual-user.png
```

This proves that the comparison mechanism detects a meaningful visual change.

`visual_user` is not included in `VALID_USER_CASES`, is not a permanent visual test, and is not an intentionally failing CI test.

### Visual Regression CI

AQA-0120 adds a dedicated `visual-regression` GitHub Actions job.

The job:

* depends on `quality`
* runs on `ubuntu-24.04`
* builds the existing repository Dockerfile
* executes only the dedicated visual suite
* uses Chromium
* runs headless
* executes sequentially
* mounts approved baselines read-only
* mounts `reports/visual/` to preserve generated evidence
* never refreshes baselines
* has no Firefox/WebKit visual matrix

Generated visual evidence is uploaded independently as:

```text
visual-regression-artifacts
```

with `if: always()` and seven-day retention.

AQA-0120 CI validation completed successfully with all seven workflow job executions passing and the visual artifact upload verified.

Formal Phase 5C roadmap completion remains reserved for AQA-0122.

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

Representative Firefox execution:

```bash
QA_BROWSER=firefox pytest -m smoke -n auto -v
```

Representative WebKit execution:

```bash
QA_BROWSER=webkit pytest -m smoke -n auto -v
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

All three engines are now used by the implemented execution strategy, but they have different responsibilities.

Current browser responsibilities are:

```text
Chromium
├── Smoke
├── Regression
├── complete functional full suite
└── dedicated visual regression

Firefox
└── representative Smoke

WebKit
└── representative Smoke
```

Chromium remains the primary complete regression browser.

Firefox and WebKit provide representative compatibility validation through the existing Smoke suite.

Visual regression remains intentionally Chromium-only and does not introduce Firefox/WebKit visual baselines or a visual browser matrix.

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

Current functional Chromium, Firefox, and WebKit CI browser execution explicitly uses:

```text
QA_HEADED=false
```

and therefore remains headless.

The dedicated visual CI job also explicitly enforces headless Chromium execution.

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

The same timeout model applies to Chromium, Firefox, and WebKit execution.

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

The framework does not create a second **failure-diagnostic** screenshot implementation through pytest-playwright.

Phase 5C visual checkpoint screenshots are a separate regression-testing responsibility and are not controlled by `QA_SCREENSHOT_POLICY`.

Setup-phase and teardown-phase failures receive failed-test diagnostic context but do not trigger the custom project screenshot.

When:

```text
QA_SCREENSHOT_POLICY=off
```

the project:

* does not write the custom failure PNG
* does not create the corresponding Allure screenshot attachment

The same screenshot policy applies to Chromium, Firefox, and WebKit browser execution.

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

Current CI leaves trace disabled for Chromium, Firefox, and WebKit execution.

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

Current CI leaves video disabled for Chromium, Firefox, and WebKit execution.

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
* device emulation
* mobile emulation
* browser channels
* slow-motion configuration
* retries

Cross-browser CI execution is implemented separately through the Phase 5A GitHub Actions matrix.

That matrix consumes the existing:

```text
QA_BROWSER
```

configuration rather than introducing another runtime configuration system.

The runtime configuration layer itself does not define:

* complete Firefox Regression responsibility
* complete WebKit Regression responsibility
* complete Firefox full-suite responsibility
* complete WebKit full-suite responsibility

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

The same diagnostics architecture is reused across Chromium, Firefox, and WebKit execution.

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

The custom failure screenshot remains the only project-owned **failure-diagnostic** screenshot lifecycle.

Phase 5C visual regression owns a separate intentional screenshot-comparison lifecycle under `visual_tests/`.

Phase 5A does not introduce browser-specific diagnostic implementations.

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

The same Page Objects are reused across Chromium, Firefox, and WebKit execution.

Phase 5A does not introduce browser-specific Page Object hierarchies.

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
* browser-specific execution branching without demonstrated need

The same assertion helpers are reused across the supported browser engines.

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
* separate `VISUAL_USER` credentials used only for controlled visual mismatch validation

Current files:

```text
test_data/login_test_data.py
test_data/product_test_data.py
test_data/checkout_test_data.py
```

Inventory, Product Details, Cart, and Checkout tests reuse centralized product data.

Centralized test data represents reusable test input and does not create shared browser state between tests or xdist workers.

Runtime configuration is not test data.

Browser selection is runtime configuration and does not require browser-specific functional test data.

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

Smoke-tagged Login coverage participates in representative Firefox and WebKit validation.

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

Smoke-tagged Inventory coverage participates in representative Firefox and WebKit validation.

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

Smoke-tagged Product Details coverage participates in representative Firefox and WebKit validation.

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

Smoke-tagged Cart coverage participates in representative Firefox and WebKit validation.

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

Smoke-tagged Checkout coverage participates in representative Firefox and WebKit validation.

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

Its tests still participate in complete Chromium full-suite CI execution.

Because Chromium full-suite CI uses pytest-xdist, individual E2E checkpoints may execute on different workers while remaining independent.

Because Chromium full-suite collects Allure results, E2E checkpoints also participate in the advanced full-suite report.

E2E checkpoints that also carry `smoke` additionally participate in representative Firefox and WebKit Smoke execution.

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
* compatibility with representative cross-browser Smoke execution
* order-independent functional test design
* separation of framework-level Pytest integration from application scenario fixtures
* dedicated `visual_tests/` suite outside normal functional test collection
* version-controlled Chromium visual baselines under `visual_baselines/chromium/`

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

Dedicated visual regression suite:

```text
visual_tests/test_visual_checkpoints.py
visual_tests/conftest.py
```

Approved visual baseline assets:

```text
visual_baselines/chromium/inventory-default.png
visual_baselines/chromium/cart-one-product.png
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
visual
```

There is no dedicated cross-browser marker.

`visual` is not a cross-browser marker. It classifies the isolated visual regression suite, whose execution is intentionally Chromium-only.

Browser selection is an execution concern rather than a functional test categorization concern.

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
* representative Chromium Smoke execution
* representative Firefox Smoke execution
* representative WebKit Smoke execution

Fixture names remain explicit and scenario-oriented.

The project does not introduce:

* a generic fixture factory
* a dependency-injection layer
* an autouse fixture redesign
* a multi-layer fixture package
* fixture scope redesign
* browser-specific scenario fixture packages

The project uses the pytest-playwright fixture/runtime model.

The project-level browser context fixture remains a framework-level fixture in the root `conftest.py`.

It extends pytest-playwright's `new_context` fixture to apply approved runtime timeout values.

Application scenario fixtures remain function-scoped and prepare deterministic application state independently for each scenario.

Tests do not rely on state produced by previous tests.

Current fixture chains, Cart and Checkout scenarios, logout/re-login persistence, parametrized scenarios, and E2E checkpoints remain compatible with sequential and parallel execution.

The Phase 4F fixture responsibility separation was validated without changing the fixture API consumed by functional tests.

Phase 5A reused the same fixture architecture on Firefox and WebKit without browser-specific fixture changes.

No sequential-only test exceptions are required for the current execution model.

No browser-specific fixture exception was required for Phase 5A.

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

Representative cross-browser validation:

```bash
QA_BROWSER=firefox pytest -m smoke -n auto -v
QA_BROWSER=webkit pytest -m smoke -n auto -v
```

Focused runtime configuration validation:

```bash
pytest tests/test_runtime_config.py
```

Phase 4F implementation was validated with:

* Smoke execution
* Regression execution
* full sequential execution
* full pytest-xdist execution
* Ruff
* Black check
* isort

Phase 5A validation additionally confirmed:

* Firefox Smoke
* WebKit Smoke
* Chromium complete full suite
* Ruff
* Black check
* isort

Phase 5C validation additionally confirmed:

* canonical Docker image build
* approved visual baseline generation and normal comparison
* controlled `visual_user` mismatch detection and diff generation
* Chromium-only guard behavior
* dedicated Docker-based visual CI execution
* independent `visual-regression-artifacts` upload
* complete seven-job GitHub Actions workflow success
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
python -m pytest visual_tests -m visual --browser chromium -v
```

Common combinations include:

```bash
pytest -m "smoke and ui" -v
pytest -m "regression and ui" -v
pytest -m "smoke and navigation" -v
pytest -m "regression and navigation" -v
```

Smoke and Regression also support Chromium parallel execution:

```bash
pytest -m smoke -n auto -v
pytest -m regression -n auto -v
```

Smoke additionally supports representative Firefox and WebKit execution:

```bash
QA_BROWSER=firefox pytest -m smoke -n auto -v
QA_BROWSER=webkit pytest -m smoke -n auto -v
```

Smoke and Regression have dedicated Chromium GitHub Actions jobs.

The existing Smoke suite additionally executes through the Phase 5A matrix on:

* Firefox
* WebKit

UI, Security, Sorting, Navigation, and E2E remain selectively executable without dedicated CI jobs.

`visual` is intentionally different: it has its own isolated Docker-based Chromium CI job.

Tests assigned to those markers still run through complete Chromium full-suite CI execution.

Tests that also carry `smoke` additionally participate in representative Firefox and WebKit compatibility validation.

Parallel execution changes test distribution rather than marker semantics.

Runtime configuration changes execution settings rather than marker semantics.

Browser selection changes the Playwright execution engine rather than marker semantics.

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
* dedicated parallel Chromium Smoke browser-test execution
* dedicated parallel Chromium Regression browser-test execution
* parallel complete unfiltered Chromium full-suite execution
* representative parallel Firefox Smoke execution
* representative parallel WebKit Smoke execution
* dedicated Firefox/WebKit cross-browser Smoke matrix
* dedicated Docker-based Chromium visual regression job
* pytest-xdist worker-level parallel execution in all functional browser-test CI executions
* sequential visual regression execution without pytest-xdist
* Chromium browser installation for Chromium jobs
* selected Firefox installation for the Firefox matrix execution
* selected WebKit installation for the WebKit matrix execution
* explicit browser-test runtime defaults
* headless browser execution
* explicit timeout defaults
* default failure screenshot policy
* trace disabled by default
* video disabled by default
* Chromium pytest-html report generation
* Firefox browser-specific pytest-html report generation
* WebKit browser-specific pytest-html report generation
* Allure result collection in Chromium full-suite
* Allure HTML generation in Chromium full-suite
* Java setup for Allure CLI
* Allure CLI setup
* Chromium Smoke-specific report and artifact upload
* Chromium Regression-specific report and artifact upload
* Chromium full-suite pytest-html artifact upload
* dedicated Chromium full-suite Allure report artifact
* broader Chromium full-suite runtime artifact
* browser-specific Firefox artifact upload
* browser-specific WebKit artifact upload
* independent `visual-regression-artifacts` upload
* visual artifact upload through `if: always()`
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
├── smoke [Chromium, native]
├── regression [Chromium, native]
├── full-suite [Chromium, native]
├── cross-browser-smoke [native]
│   ├── Firefox
│   └── WebKit
└── visual-regression [Chromium, Docker]
```

The `quality` job runs first.

It validates:

```bash
ruff check .
black --check .
isort . --check-only
```

The quality job:

* does not install Playwright browsers
* does not execute browser tests
* does not use pytest-xdist
* does not require browser runtime configuration

All functional browser-test jobs and the visual regression job depend on successful quality validation.

The Chromium Smoke, Regression, and full-suite jobs do not depend on each other.

Firefox and WebKit are expanded from one `cross-browser-smoke` matrix.

The matrix uses:

```yaml
fail-fast: false
```

GitHub Actions may therefore schedule independent functional and visual executions concurrently after `quality`.

Phase 4F diagnostics operate through the existing Pytest execution path.

Phase 5A extends the workflow without replacing the existing Chromium topology.

Phase 5C adds one separate Docker-based visual job without moving the existing functional jobs into Docker.

## CI Runtime Defaults

Chromium Smoke, Regression, and full-suite use:

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

The Firefox/WebKit matrix uses the same runtime strategy except:

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

The current functional CI model is:

* Chromium as the primary complete regression browser
* Firefox as a representative Smoke compatibility browser
* WebKit as a representative Smoke compatibility browser
* headless
* pytest-xdist parallel

The visual CI model is:

* Chromium only
* Docker-based
* headless
* sequential
* fixed rendering configuration
* read-only approved baselines
* screenshots on failed test calls enabled
* trace disabled by default
* video disabled by default
* Phase 4F diagnostics active through normal Pytest execution

CI does not currently introduce:

* complete Firefox Regression
* complete WebKit Regression
* complete Firefox full-suite execution
* complete WebKit full-suite execution
* retries
* runtime configuration forms in `workflow_dispatch`
* secrets for non-secret runtime values
* default trace retention
* default video retention
* diagnostic-specific CI jobs
* Firefox visual regression
* WebKit visual regression
* a multi-browser visual matrix
* automatic CI baseline refresh

## Smoke CI

The dedicated `smoke` job is the Chromium Smoke path.

Core command:

```bash
pytest -m smoke -n auto -v
```

The actual CI command additionally generates:

```text
reports/smoke-report.html
```

Chromium Smoke remains focused on pytest-html reporting.

It does not generate a dedicated Allure report.

Runtime diagnostics are available through the normal Pytest execution path.

## Regression CI

The dedicated `regression` job is the Chromium Regression path.

Core command:

```bash
pytest -m regression -n auto -v
```

The actual CI command additionally generates:

```text
reports/regression-report.html
```

Chromium Regression remains focused on pytest-html reporting.

It does not generate a dedicated Allure report.

Runtime diagnostics are available through the normal Pytest execution path.

## Full-Suite CI

The `full-suite` job executes the complete unfiltered Chromium test collection:

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

Firefox and WebKit representative Smoke execution supplements rather than replaces this complete Chromium regression gate.

## Cross-Browser Smoke CI

The `cross-browser-smoke` job executes representative compatibility validation for:

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

* uses `QA_BROWSER=${{ matrix.browser }}`
* installs only the selected browser engine
* runs headless
* executes the existing `smoke` marker
* uses pytest-xdist with `-n auto`
* reuses existing Page Objects
* reuses existing fixtures
* reuses existing assertions
* reuses Phase 4F diagnostics
* generates a browser-specific pytest-html report
* uploads browser-specific artifacts

Browser installation:

```bash
playwright install --with-deps ${{ matrix.browser }}
```

Core execution:

```bash
pytest -m smoke -n auto -v
```

Reports:

```text
reports/firefox-smoke-report.html
reports/webkit-smoke-report.html
```

Chromium is intentionally excluded from this matrix because it already has dedicated Smoke, Regression, and complete full-suite jobs.

Firefox and WebKit do not generate dedicated Allure reports.

## Visual Regression CI

The dedicated `visual-regression` job executes the approved Phase 5C visual suite separately from all functional browser jobs.

Core execution characteristics:

```text
runner: ubuntu-24.04
environment: existing project Docker image
browser: Chromium
mode: headless
suite: visual_tests/
marker: visual
parallelism: sequential
baseline access: read-only
```

The job depends on `quality` and then runs independently of Smoke, Regression, full-suite, Firefox Smoke, and WebKit Smoke.

It does not use `-n auto` and does not participate in the Firefox/WebKit matrix.

Permanent CI validation uses only the approved `standard_user` checkpoints.

The one-off `visual_user` mismatch validation is intentionally excluded from permanent CI.

## CI Concurrency Model

GitHub Actions job-level concurrency, GitHub Actions matrix expansion, and pytest-xdist worker-level parallelism are separate mechanisms.

Conceptually:

```text
runtime defaults
        ↓
Phase 4F runtime diagnostics
        ↓
quality
├── smoke [Chromium, native]
│   └── xdist workers
│       └── pytest-html
├── regression [Chromium, native]
│   └── xdist workers
│       └── pytest-html
├── full-suite [Chromium, native]
│   └── xdist workers
│       ├── pytest-html
│       ├── Allure results
│       └── Allure HTML report
├── cross-browser-smoke [native]
│   ├── Firefox
│   │   └── xdist workers
│   │       └── browser-specific pytest-html
│   └── WebKit
│       └── xdist workers
│           └── browser-specific pytest-html
└── visual-regression [Chromium, Docker]
    └── sequential visual checkpoints
```

Runtime configuration, diagnostics, and reporting are layered on top of test execution.

They do not introduce additional concurrency models.

Visual regression deliberately avoids the pytest-xdist worker layer and executes sequentially.

The runtime diagnostic header is emitted by the controlling Pytest process rather than being duplicated by each xdist worker.

The following marker suites do not currently have dedicated CI jobs:

* UI
* Security
* Sorting
* Navigation
* E2E

The `visual` marker is excluded from this list because it has a dedicated visual CI job.

Tests that also carry `smoke` may nevertheless participate in representative Firefox/WebKit validation.

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
* Firefox browser-specific pytest-html reporting
* WebKit browser-specific pytest-html reporting
* Allure Pytest integration
* local Allure result collection
* local Allure HTML generation
* Chromium full-suite CI Allure result collection
* Chromium full-suite CI Allure HTML generation
* configurable screenshots on failed test calls
* failure screenshot attachment to Allure
* configurable Playwright trace generation
* configurable Playwright video generation
* `reports/` runtime output
* `test-results/` Playwright diagnostic output
* Chromium job-specific GitHub Actions artifacts
* Firefox browser-specific GitHub Actions artifacts
* WebKit browser-specific GitHub Actions artifacts
* visual actual screenshot artifacts
* visual diff screenshot artifacts
* dedicated `visual-regression-artifacts`
* downloadable CI artifacts

The reporting and diagnostic mechanisms have complementary responsibilities:

* **Phase 4F runtime diagnostics** — effective execution context
* **Phase 4F failed-test diagnostics** — test identity, failure phase, available URL, screenshot path, and diagnostic-operation errors
* **pytest-html** — lightweight execution reports
* **browser-specific pytest-html** — Firefox and WebKit Smoke execution reports
* **Allure** — richer structured reporting and advanced Chromium full-suite reporting
* **failure screenshots** — direct browser evidence for failed test calls
* **visual actual/diff screenshots** — intentional visual regression evidence separate from failure screenshots
* **Playwright traces** — optional execution diagnostics owned by pytest-playwright
* **Playwright videos** — optional browser recording diagnostics owned by pytest-playwright
* **GitHub Actions artifacts** — temporary storage and distribution of generated CI outputs

Phase 4F diagnostics are lightweight console/report context.

They do not create persistent diagnostic log files.

## Current Reporting Paths

Chromium pytest-html:

```text
reports/smoke-report.html
reports/regression-report.html
reports/report.html
```

Firefox/WebKit Smoke pytest-html:

```text
reports/firefox-smoke-report.html
reports/webkit-smoke-report.html
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

Visual regression runtime output:

```text
reports/visual/actual/
reports/visual/diff/
```

Approved visual baselines are repository content:

```text
visual_baselines/chromium/
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

The current CI Allure responsibility remains with the complete Chromium full-suite job.

Firefox and WebKit Smoke remain pytest-html-focused.

## CI Reporting Artifacts

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

Current visual regression artifact:

```text
visual-regression-artifacts
```

It uploads generated content from:

```text
reports/visual/
```

and uses `if: always()` so available actual/diff evidence can still be retained after a visual test failure.

The dedicated Chromium full-suite Allure artifact publishes:

```text
reports/allure-report/
```

The broader Chromium full-suite artifact publishes:

```text
reports/
```

Each Firefox/WebKit broader runtime artifact independently publishes:

```text
reports/
```

from its own matrix execution environment.

Browser-specific artifact names prevent Firefox and WebKit output collisions.

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

A failing required test still fails its browser execution.

The cross-browser matrix uses:

```text
fail-fast: false
```

so one Firefox/WebKit execution does not automatically cancel the other.

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
reports/visual/actual/
reports/visual/diff/
test-results/
playwright-report/
```

Browser-specific Firefox/WebKit pytest-html reports are also generated under:

```text
reports/
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
* cross-browser execution strategy
* visual regression strategy
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
browser selection
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

* dedicated parallel Chromium Smoke CI execution
* dedicated parallel Chromium Regression CI execution
* parallel complete Chromium full-suite CI execution
* representative Firefox Smoke CI execution when carrying `smoke`
* representative WebKit Smoke CI execution when carrying `smoke`
* complete Chromium full-suite Allure reporting

Phase 5A execution expansion does not introduce new product-facing test case coverage and therefore does not require browser-specific test case metadata.

Phase 5C visual regression adds presentation-level checkpoints for already automated application states. It does not automate a new functional test case and therefore does not require new functional test case metadata or coverage-table entries.

# Planned Features

## Framework Architecture

Possible future framework improvements include:

* additional reusable fixtures when justified by repeated scenario setup
* additional framework utilities when repeated logic appears
* additional Page Objects when new application areas require them
* further responsibility separation when justified by actual framework growth

Centralized runtime configuration is already implemented and should not be described as future functionality.

Phase 4F diagnostics and fixture responsibility separation are also implemented and should not be described as future functionality.

Phase 5A representative Playwright cross-browser Smoke validation is implemented and should not be described as future functionality.

Phase 5B containerized Playwright execution is also implemented and should not be described as future functionality.

Phase 5C visual regression testing is implemented and should not be described as future functionality. Formal Phase 5C roadmap completion remains reserved for AQA-0122.

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

Cross-browser CI already consumes the existing `QA_BROWSER` setting and does not require an additional configuration layer.

## Test Coverage

Potential future automation areas include:

* broader end-to-end journey coverage beyond current checkpoints
* broader session and logout coverage where justified
* additional approved edge cases
* known-defect coverage where appropriate
* API-level testing
* hybrid UI/API scenarios
* expanded Firefox or WebKit Regression coverage only if future requirements justify it
* expanded Firefox or WebKit full-suite coverage only if future requirements justify it
* additional visual checkpoints only where future risk justifies the maintenance cost
* browser-specific visual baselines only if a future approved strategy intentionally expands beyond Chromium

Representative Firefox and WebKit Smoke compatibility validation is already implemented.

## Test Organization

Possible future improvements include:

* additional suite-specific CI execution where justified
* expanded traceability
* additional parametrized scenarios where useful
* additional reusable scenario fixtures when repeated setup justifies them

Already implemented:

* normalized marker strategy
* dedicated Chromium Smoke CI
* dedicated Chromium Regression CI
* pytest-xdist worker-level parallel execution
* independent E2E checkpoint design
* separated framework-level and application scenario fixture responsibilities
* reuse of the existing `smoke` marker for Firefox/WebKit representative validation
* browser-neutral functional test modules across the current Playwright engines
* dedicated isolated `visual` suite
* explicit visual baseline ownership and refresh workflow

Future work should improve scalability and feedback without reintroducing obsolete marker categories, order-dependent test design, unnecessary fixture abstraction layers, or duplicate browser-specific test modules.

## Reporting And Diagnostics

Current Allure reporting, failure screenshot policy, trace policy, video policy, runtime diagnostics, failed-test diagnostics, diagnostic error reporting, browser-specific Firefox/WebKit pytest-html reporting, and Phase 5C visual actual/diff evidence are implemented and should not be described as future-only functionality.

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
* dedicated Firefox Allure CI reporting
* dedicated WebKit Allure CI reporting

## CI/CD Improvements

Possible future CI improvements include:

* dependency caching
* Playwright browser caching
* additional marker-based jobs where justified
* scheduled regression execution
* JUnit XML publishing
* additional reporting integrations
* expanded additional-browser Regression execution if future scope justifies it
* expanded additional-browser full-suite execution if future scope justifies it

Already implemented:

* dedicated Chromium Smoke and Regression jobs
* complete Chromium full-suite job
* Firefox/WebKit cross-browser Smoke matrix
* selected-engine-only matrix installation
* pytest-xdist execution
* pytest-html reporting
* browser-specific Firefox/WebKit pytest-html reporting
* Chromium full-suite Allure reporting
* explicit runtime defaults
* Phase 4F diagnostics operating through the existing Pytest execution path
* browser-specific Firefox/WebKit artifact publication
* dedicated Docker-based Chromium visual regression job
* independent `visual-regression-artifacts`

The Chromium Smoke, Regression, full-suite, Firefox Smoke, WebKit Smoke, and visual regression executions may be scheduled independently after `quality`.

Inside each functional browser execution, pytest-xdist distributes collected tests between workers.

The visual regression job remains sequential.

GitHub Actions job scheduling, matrix expansion, and pytest-xdist worker distribution remain separate execution concepts.

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

Current approved Chromium commands:

```bash
pytest -m smoke -n auto -v
pytest -m regression -n auto -v
pytest -n auto -v
```

Representative Firefox/WebKit commands:

```bash
QA_BROWSER=firefox pytest -m smoke -n auto -v
QA_BROWSER=webkit pytest -m smoke -n auto -v
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
* representative Firefox Smoke execution
* representative WebKit Smoke execution

No sequential-only exception is required for the normal functional suites, diagnostics, or reporting model.

Visual regression is intentionally sequential by design and is not part of the pytest-xdist functional execution model.

No browser-specific compatibility workaround was required for Phase 5A.

GitHub Actions job concurrency, GitHub Actions matrix expansion, and pytest-xdist worker concurrency remain distinct execution layers.

## Advanced Reporting Extensions

Allure reporting is currently implemented through:

* `allure-pytest`
* local result generation
* local HTML generation
* Chromium full-suite CI result generation
* Chromium full-suite CI HTML generation
* failure screenshot attachments
* dedicated GitHub Actions Allure artifact publication

Current output locations:

```text
reports/allure-results/
reports/allure-report/
```

Firefox and WebKit Smoke additionally provide browser-specific pytest-html reports:

```text
reports/firefox-smoke-report.html
reports/webkit-smoke-report.html
```

Possible future capabilities include:

* history persistence
* trend analytics
* hosted reports
* GitHub Pages publishing
* richer metadata
* additional report analytics
* dedicated additional-browser Allure reporting if future scope requires it

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

The implemented Playwright browser strategy is:

```text
Chromium
├── Smoke
├── Regression
├── complete functional full suite
└── dedicated visual regression

Firefox
└── representative Smoke

WebKit
└── representative Smoke
```

Representative local execution:

```bash
QA_BROWSER=firefox pytest -m smoke -n auto -v
QA_BROWSER=webkit pytest -m smoke -n auto -v
```

Representative CI execution uses the dedicated:

```text
cross-browser-smoke
```

matrix with:

```text
firefox
webkit
```

Each matrix execution installs only its selected engine and executes:

```bash
pytest -m smoke -n auto -v
```

Current cross-browser capabilities include:

* local Firefox Smoke validation
* local WebKit Smoke validation
* Firefox Smoke CI execution
* WebKit Smoke CI execution
* one Firefox/WebKit GitHub Actions matrix
* `fail-fast: false`
* reuse of the existing `smoke` marker
* reuse of existing Page Objects
* reuse of existing fixtures
* reuse of existing assertions
* pytest-xdist execution
* browser-specific pytest-html reports
* browser-specific CI artifact names

The framework does not currently provide:

* complete Firefox Regression
* complete WebKit Regression
* complete Firefox full-suite execution
* complete WebKit full-suite execution
* complete three-browser regression parity
* duplicate Firefox-specific functional test modules
* duplicate WebKit-specific functional test modules
* a cross-browser pytest marker
* browser-specific fixture packages
* Selenium execution
* Firefox visual baselines or visual CI execution
* WebKit visual baselines or visual CI execution
* a visual browser matrix

Chromium remains the primary complete regression browser.

Firefox and WebKit provide representative compatibility validation rather than complete regression parity.

## Future Extensions

Potential long-term extensions include:

* Selenium WebDriver comparison
* Jenkins integration
* reusable framework packaging
* advanced execution analytics
* expanded additional-browser regression execution if future requirements justify it

Selenium remains outside the current Playwright cross-browser implementation.

Docker-based Playwright execution is already implemented through Phase 5B and is not a future extension.

Controlled visual regression is already implemented through Phase 5C and is not a future-only capability.

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
* local Firefox Smoke execution
* local WebKit Smoke execution
* repository-root Docker execution environment
* official pinned Playwright Python Docker image
* Playwright Docker image alignment with `requirements-lock.txt`
* sequential Docker Pytest execution
* pytest-xdist Docker execution
* Docker reuse of existing `QA_*` runtime configuration
* Docker browser selection through `QA_BROWSER`
* validated Chromium Smoke execution inside Docker
* validated Firefox Smoke execution inside Docker
* host-persistent Docker reports and browser artifacts through bind mounts
* raw Allure result generation inside Docker
* Allure HTML generation outside the Docker image
* centralized runtime configuration
* base URL runtime overrides
* browser runtime selection
* Chromium/Firefox/WebKit runtime support
* Chromium as the primary complete regression browser
* Firefox representative Smoke compatibility validation
* WebKit representative Smoke compatibility validation
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
* dedicated parallel Chromium Smoke CI execution
* dedicated parallel Chromium Regression CI execution
* parallel complete Chromium full-suite CI execution
* representative parallel Firefox Smoke CI execution
* representative parallel WebKit Smoke CI execution
* dedicated Firefox/WebKit `cross-browser-smoke` matrix
* selected-engine-only Firefox/WebKit installation
* explicit CI runtime defaults
* pytest-html reporting
* browser-specific Firefox pytest-html reporting
* browser-specific WebKit pytest-html reporting
* Allure result collection
* Allure HTML generation
* sequential and parallel Allure compatibility
* screenshots on failure
* failure screenshot attachments in Allure
* optional trace generation
* optional video generation
* pytest-playwright ownership of trace and video lifecycle
* Chromium job-specific CI artifacts
* Firefox browser-specific CI artifacts
* WebKit browser-specific CI artifacts
* dedicated full-suite Allure report artifact
* Pillow-based visual regression comparison
* dedicated `visual_tests/` suite
* dedicated `visual` marker
* approved Chromium PNG baselines
* explicit visual baseline refresh workflow
* generated visual actual screenshots
* generated visual diff screenshots
* Chromium-only/headless visual execution guard
* canonical Docker visual execution
* dedicated Docker-based Chromium `visual-regression` CI job
* independent `visual-regression-artifacts`
* controlled `visual_user` mismatch validation
* generated runtime output isolation
* Git branching workflow
* technical project documentation

Current CI execution, diagnostics, and reporting model:

```text
runtime defaults
        ↓
Phase 4F runtime diagnostics
        ↓
quality
├── smoke [Chromium, native]
│   └── pytest-xdist workers
│       └── pytest-html
├── regression [Chromium, native]
│   └── pytest-xdist workers
│       └── pytest-html
├── full-suite [Chromium, native]
│   └── pytest-xdist workers
│       ├── pytest-html
│       ├── Allure results
│       ├── failure screenshots
│       └── Allure HTML report
├── cross-browser-smoke [native]
│   ├── Firefox
│   │   └── pytest-xdist workers
│   │       └── browser-specific pytest-html
│   └── WebKit
│       └── pytest-xdist workers
│           └── browser-specific pytest-html
└── visual-regression [Chromium, Docker]
    └── sequential visual checkpoints
```

The `quality` job is the prerequisite and does not use browser execution or pytest-xdist.

Chromium Smoke, Chromium Regression, Chromium full-suite, Firefox Smoke, WebKit Smoke, and visual regression are independently executable after successful quality validation.

Firefox and WebKit originate from the same matrix with:

```text
fail-fast: false
```

UI, Security, Sorting, Navigation, and E2E do not currently have dedicated CI jobs.

Tests carrying those markers still participate in the complete Chromium full suite.

Tests that also carry `smoke` additionally participate in representative Firefox and WebKit validation.

Phase 4C pytest-xdist parallel execution is implemented.

Phase 4D reporting is implemented.

Phase 4E Runtime Configuration is implemented.

Phase 4F Diagnostics And Fixture Cleanup is implemented.

Phase 5A representative Playwright cross-browser Smoke validation is implemented.

Phase 5B containerized Playwright execution is implemented.

Phase 5C visual regression testing is implemented.

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

Implemented Phase 5A capabilities include:

* Chromium preserved as the primary complete regression browser
* local Firefox Smoke validation
* local WebKit Smoke validation
* Firefox Smoke CI execution
* WebKit Smoke CI execution
* Firefox/WebKit cross-browser Smoke matrix
* reuse of the existing `smoke` marker
* reuse of existing functional tests
* reuse of existing Page Objects
* reuse of existing fixtures
* reuse of existing assertions
* pytest-xdist execution
* browser-specific pytest-html reporting
* browser-specific CI artifacts
* preservation of Chromium full-suite Allure reporting
* preservation of Phase 4F diagnostics
* no required browser-specific compatibility workaround

Phase 5A validation confirmed:

```text
Firefox Smoke: 31 passed
WebKit Smoke: 31 passed
Chromium full-suite: 236 passed
Ruff: passed
Black check: passed
isort: passed
```

GitHub Actions validation confirmed successful:

* `quality`
* Chromium `smoke`
* Chromium `regression`
* Chromium `full-suite`
* `cross-browser-smoke (firefox)`
* `cross-browser-smoke (webkit)`

Implemented Phase 5B capabilities include:

* repository-root `Dockerfile`
* repository-root `.dockerignore`
* official `mcr.microsoft.com/playwright/python:v1.60.0-noble` base image
* Playwright version alignment with `requirements-lock.txt`
* dependency installation from the locked requirements file
* Docker build-layer reuse through lockfile-first dependency installation
* sequential Pytest execution inside Docker
* pytest-xdist parallel execution inside Docker
* reuse of the existing `QA_*` runtime configuration
* Chromium browser execution inside Docker
* Firefox browser execution through `QA_BROWSER=firefox`
* pytest-html persistence through bind mounts
* raw Allure result persistence through bind mounts
* failure screenshot persistence through bind mounts
* Playwright trace persistence through bind mounts
* Playwright video persistence through bind mounts
* optional host UID/GID mapping for generated artifact ownership
* Pytest cache redirection to `/tmp/pytest_cache` when running as the host UID/GID
* recommended `--rm`, `--init`, and `--ipc=host` runtime flags
* raw Allure result generation without adding the standalone Allure CLI, Java, or Node.js to the image
* preserved native GitHub Actions execution
* no Docker-specific functional CI topology

Phase 5B validation confirmed:

```text
Docker image build: passed
Chromium Smoke sequential: 31 passed
Chromium Smoke parallel: 31 passed
Firefox Smoke: 31 passed
pytest-html persistence: passed
Allure raw result persistence: passed
Playwright trace persistence: passed
Playwright video persistence: passed
failure screenshot persistence: passed
Ruff: passed
Black check: passed
isort: passed
```

General Phase 5B Docker execution remains separate from the native functional CI jobs; Phase 5C reuses the same image only for the dedicated visual regression job.

Implemented Phase 5C capabilities include:

* dedicated Pillow-based image comparison in `framework/visual_regression.py`
* approved Chromium visual baselines
* `inventory-default.png`
* `cart-one-product.png`
* isolated `visual_tests/` execution
* registered `visual` Pytest marker
* fixed Chromium visual rendering conditions
* Chromium-only/headless visual guard
* explicit baseline refresh through `--update-visual-baselines`
* separation of visual screenshots from failure screenshots
* generated actual screenshots under `reports/visual/actual/`
* generated diff screenshots under `reports/visual/diff/`
* controlled `visual_user` mismatch demonstration
* no permanent intentionally failing visual test
* no Firefox/WebKit visual matrix
* dedicated Docker-based `visual-regression` CI job
* read-only baseline mounting in CI
* independent `visual-regression-artifacts`
* `if: always()` visual artifact upload
* successful seven-job GitHub Actions validation

Phase 5C validation confirmed:

```text
approved visual checkpoints: passed
controlled visual_user mismatch detection: passed
full functional pytest suite after visual integration: 244 passed
Ruff: passed
Black check: passed
isort: passed
GitHub Actions workflow after AQA-0120: 7/7 job executions passed
visual-regression-artifacts upload: verified
```

Formal Phase 5C roadmap completion remains reserved for AQA-0122.

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
* complete Firefox Regression
* complete WebKit Regression
* complete Firefox full-suite execution
* complete WebKit full-suite execution
* complete three-browser regression parity
* retries
* device emulation
* Selenium execution

Phase 5A representative cross-browser execution, Phase 5B containerized Playwright execution, and Phase 5C visual regression testing are implemented framework capabilities.

Phase 5B was formally closed through AQA-0117. Formal Phase 5C roadmap completion remains owned by AQA-0122.