# Framework And Project Structure

This document describes the repository structure and the responsibility of each major directory and configuration file.

The framework is structured to support maintainable Playwright UI automation, Page Object Model components, shared framework utilities, centralized test data, reusable pytest fixtures, centralized runtime configuration, marker-based test organization, sequential and pytest-xdist parallel execution, pytest-html and Allure reporting, configurable failure evidence, optional Playwright trace and video output, documentation, staged CI execution, and future framework expansion.

The `main` branch represents the stable portfolio version of the project, while `develop` and active workstream branches may contain newer validated changes before promotion.

## Current Project Structure

```text
playwright-python-qa-automation-framework/
│
├── .github/
│   └── workflows/              # GitHub Actions CI workflows
│
├── config/                     # Centralized runtime configuration
├── docs/                       # Project documentation
├── framework/                  # Shared framework utilities
│   └── assertions/             # Reusable assertion helpers
├── pages/                      # Page Object Model components
├── reports/                    # Generated reports and failure evidence
├── resources/                  # Static resources and supporting files
├── test_cases/                 # Manual test cases and test design documentation
├── test_data/                  # Centralized test datasets
├── tests/                      # Automated and configuration-focused tests
│
├── conftest.py                 # Shared pytest runtime integration, hooks, and fixtures
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
* explicit Phase 4E runtime defaults for browser-test jobs
* pytest-html generation
* full-suite Allure result collection
* full-suite Allure HTML report generation
* Java setup required by Allure CLI
* Allure CLI setup for the full-suite job
* job-specific artifact upload
* dedicated full-suite Allure artifact upload
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

Phase 4C adds pytest-xdist worker-level execution inside those browser jobs:

```text
quality
├── smoke
│   └── pytest-xdist workers
├── regression
│   └── pytest-xdist workers
└── full-suite
    └── pytest-xdist workers
```

Phase 4D adds reporting on top of the existing execution model:

```text
quality
├── smoke
│   └── pytest-xdist
│       └── pytest-html
├── regression
│   └── pytest-xdist
│       └── pytest-html
└── full-suite
    └── pytest-xdist
        ├── pytest-html
        ├── Allure results
        └── Allure HTML report
```

Phase 4E adds explicit runtime configuration to the existing browser-test jobs without changing their topology:

```text
Phase 4E runtime defaults
        ↓
quality
├── smoke
├── regression
└── full-suite
```

Current browser-job runtime defaults are:

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

GitHub Actions job-level concurrency and pytest-xdist worker-level parallelism are separate mechanisms.

Reporting and runtime configuration are also separate concerns layered on top of test execution.

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

Smoke and Regression remain pytest-html-focused.

The complete full-suite job is the primary CI source for the advanced Allure report.

The CI browser scope remains intentionally Chromium-only.

The workflow does not currently introduce:

* browser matrices
* Firefox CI installation
* WebKit CI installation
* cross-browser CI execution
* retries
* `continue-on-error`
* trace retention by default
* video retention by default

Detailed CI behavior is documented in:

```text
docs/ci-cd-pipeline.md
```

### `config/`

Contains centralized runtime configuration.

Current implementation:

```text
config/settings.py
```

Current responsibilities include:

* environment-variable handling
* approved runtime defaults
* application base URL configuration
* browser selection
* headed/headless configuration
* Playwright action and navigation timeout configuration
* Playwright assertion timeout configuration
* screenshot policy
* trace policy
* video policy
* input normalization
* invalid-value validation
* immutable runtime settings exposed to the framework

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

#### Base URL

`QA_BASE_URL` controls the application origin used by Page Objects through `BasePage`.

The default is:

```text
https://www.saucedemo.com
```

Accepted values must:

* use `http` or `https`
* contain a valid host
* represent only the application origin
* not contain credentials
* not contain query parameters
* not contain a fragment
* not contain whitespace
* contain a valid port if a port is provided

A trailing slash is normalized away.

#### Browser

`QA_BROWSER` supports:

```text
chromium
firefox
webkit
```

Browser values are normalized by trimming surrounding whitespace and converting to lowercase.

The configuration layer recognizes the three Playwright engines.

This does not mean all three are installed or validated in every execution environment.

Current CI remains Chromium-only.

Explicit native pytest-playwright `--browser` usage remains supported.

#### Headed / Headless

`QA_HEADED` accepts:

```text
true
1
yes
on

false
0
no
off
```

Values are case-insensitive after normalization.

The default is:

```text
false
```

The native pytest-playwright `--headed` option also remains usable.

#### Timeouts

`QA_TIMEOUT_MS` controls:

* default Playwright action timeout
* default Playwright navigation timeout

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

A value of `0` is accepted.

#### Screenshot Policy

`QA_SCREENSHOT_POLICY` supports:

```text
only-on-failure
off
```

Default:

```text
only-on-failure
```

This policy controls the existing custom failure screenshot mechanism and its Allure attachment behavior.

It does not create a second project-level screenshot implementation.

#### Trace And Video Policies

`QA_TRACE_POLICY` and `QA_VIDEO_POLICY` support:

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

Trace and video use pytest-playwright / Playwright-supported mechanisms rather than custom project recording implementations.

Explicit native pytest-playwright trace and video command-line options remain usable.

#### Invalid Configuration

Invalid explicit runtime values raise configuration errors before normal test execution proceeds.

Examples include:

* unsupported browser values
* unsupported screenshot, trace, or video policies
* invalid boolean values
* negative timeout values
* non-integer timeout values
* malformed application base URLs

The error identifies the affected environment variable.

#### Configuration Boundaries

The current runtime configuration layer does not implement:

* named environment profiles
* automatic `.env` loading
* CI browser matrices
* cross-browser CI
* device emulation
* mobile emulation
* browser channels
* slow motion configuration
* retries
* Phase 4F logging redesign
* Phase 4F fixture cleanup

The `config/` layer should remain focused on approved runtime configuration rather than becoming a generic container for unrelated framework logic.

### `docs/`

Contains technical project documentation.

Current documentation includes areas such as:

* architecture
* framework and project structure
* testing strategy
* pytest marker strategy
* sequential and parallel execution strategy
* runtime configuration strategy
* reporting strategy
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
* document runtime configuration accurately
* document pytest-html and Allure responsibilities accurately
* document failure screenshot behavior accurately
* distinguish Playwright trace/video runtime output from repository content
* distinguish generated runtime outputs from repository content
* distinguish implemented functionality from planned functionality
* distinguish dedicated CI marker jobs from selectively executable local suites
* distinguish GitHub Actions job concurrency from pytest-xdist worker parallelism
* distinguish locally supported browser configuration from Chromium-only CI
* avoid documenting future CI or reporting capabilities as already implemented
* avoid describing implemented pytest-xdist, Allure, or runtime configuration support as future functionality
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
* runtime configuration parsing
* reporting configuration
* failure screenshot capture

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
* declaring application-relative `ROUTE` values where direct navigation is supported

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

Reporting, runtime parsing, browser lifecycle ownership, and screenshot responsibilities do not belong in Page Objects.

Parallel execution, Allure reporting, and Phase 4E runtime configuration do not change Page Object responsibility boundaries.

### `BasePage`

`BasePage` provides the minimal shared Page Object foundation.

Current responsibilities:

* storing the Playwright `Page`
* shared application-relative route metadata through `ROUTE`
* composing runtime URLs through `settings.base_url`
* shared page opening behavior

Current URL composition follows:

```text
settings.base_url + PageObject.ROUTE + optional suffix
```

The application origin is therefore not duplicated across Page Objects.

Changing `QA_BASE_URL` changes the application origin without requiring changes to tests or Page Objects.

`BasePage` should remain intentionally small.

It should not become a generic container for unrelated framework, reporting, browser lifecycle, or runtime parsing helpers.

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

* opening Login through the configured application base URL
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

Stores generated reporting and failure-evidence runtime outputs.

Current runtime outputs include:

* pytest-html reports
* failure screenshots
* Allure result data
* generated Allure HTML reports
* debugging outputs
* CI artifact source files

Generated files should not be committed to Git.

They are intended for:

* local debugging
* failure analysis
* execution evidence
* CI artifact publishing
* advanced execution review through Allure

Current pytest-html files include:

```text
reports/smoke-report.html
reports/regression-report.html
reports/report.html
```

Current Allure result location:

```text
reports/allure-results/
```

Current generated Allure HTML location:

```text
reports/allure-report/
```

Failure screenshots are stored under:

```text
reports/screenshots/
```

when failure screenshot policy is enabled.

The reporting model is complementary:

```text
pytest-html
    → lightweight HTML execution reports

Allure results
    → structured advanced reporting data

Allure HTML
    → generated advanced report

failure screenshots
    → browser failure evidence

GitHub Actions artifacts
    → temporary CI distribution of runtime outputs
```

Playwright trace and video files are generated separately through pytest-playwright under its runtime artifact structure rather than under the project `reports/` structure.

The report paths and screenshot mechanism are compatible with both sequential and pytest-xdist execution.

No sequential-only reporting exception is required for the current suite.

Detailed artifact names and retention behavior are documented in:

```text
docs/ci-cd-pipeline.md
```

### Playwright Runtime Artifacts

When enabled through runtime configuration, pytest-playwright may create diagnostic output under:

```text
test-results/
```

Current policies are controlled by:

```text
QA_TRACE_POLICY
QA_VIDEO_POLICY
```

Generated files may include:

```text
trace.zip
video.webm
```

Trace and video remain disabled by default.

These files are runtime outputs and are not repository source content.

### Generated Runtime Output Policy

Generated report and Playwright artifact output is not repository source content.

Relevant ignore rules include:

```text
reports/*
!reports/.gitkeep

allure-results/
allure-report/
test-results/
playwright-report/
```

The implemented Allure output locations are currently nested inside `reports/`, so they are covered by:

```text
reports/*
```

The additional root-level Allure ignore entries protect against accidental generated output if different Allure paths are used manually.

`test-results/` protects pytest-playwright runtime artifact output such as trace and video files.

The repository should contain reporting and runtime configuration, but not generated execution output.

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

Phase 4D reporting and Phase 4E runtime configuration do not introduce new functional test cases or require test case automation metadata changes.

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

Runtime configuration is not test data and is owned separately by `config/settings.py`.

### `tests/`

Contains automated test suites and focused configuration validation.

Current functional test modules:

```text
tests/test_login_page.py
tests/test_inventory_page.py
tests/test_product_details_page.py
tests/test_cart_page.py
tests/test_checkout_page.py
```

Runtime configuration validation:

```text
tests/test_runtime_config.py
```

Current test module responsibilities:

* `test_login_page.py` — authentication validation, Login UI behavior, error-state behavior, keyboard submission, input error icons, protected-route access, and Login-related E2E checkpoint coverage
* `test_inventory_page.py` — Inventory visibility, product list and content validation, sorting, Cart actions, cart badge behavior, Product Details navigation, and Inventory-related E2E checkpoints
* `test_product_details_page.py` — Product Details content, Inventory return navigation, Add/Remove behavior, cart badge behavior, Cart navigation, and all-products coverage
* `test_cart_page.py` — empty Cart state, Cart item visibility and content, Remove behavior, cart badge behavior, Continue Shopping, Cart persistence, Product Details navigation, Checkout entry, and Cart-related E2E checkpoints
* `test_checkout_page.py` — Checkout Information validation, Checkout Overview validation, price summaries, navigation, Checkout Complete validation, and Checkout-related E2E checkpoints
* `test_runtime_config.py` — runtime defaults, normalization, supported values, and invalid configuration behavior

The current automated functional modules focus on Playwright UI automation.

All functional test modules must remain independently executable and must not rely on execution order or browser state produced by another test.

This requirement supports:

* sequential execution
* pytest-xdist worker-level parallel execution
* marker-based execution
* runtime overrides
* full-suite reporting
* reliable CI execution

Runtime configuration should remain external to functional test logic.

Reporting integrations operate around test execution and do not require separate reporting-specific test modules.

Future modules may include:

* API tests
* cross-browser-specific execution only if future architecture requires dedicated ownership

API tests are not currently implemented.

## Root Configuration Files

### `conftest.py`

Contains shared pytest runtime integration, hooks, and fixtures.

Current runtime responsibilities include:

* loading centralized runtime settings
* applying configured browser selection to pytest-playwright when no explicit native browser option is supplied
* preserving explicit native pytest-playwright browser options
* applying configured headed execution
* applying configured trace policy unless an explicit native trace option is supplied
* applying configured video policy unless an explicit native video option is supplied
* configuring Playwright assertion timeout
* creating contexts through pytest-playwright `new_context`
* applying action timeout to created browser contexts
* applying navigation timeout to created browser contexts
* controlling custom failure screenshot behavior through screenshot policy

Current fixture usage includes:

* `opened_login_page`
* `standard_user`
* `logged_in_inventory_page`
* `inventory_page_with_one_product_in_cart`
* `cart_page_with_one_product`
* `checkout_step_one_page_with_one_product`
* `checkout_step_two_page_with_one_product`
* `checkout_last_step_page_with_one_product`

Current hook responsibilities include:

* detecting browser-test failures during the Pytest call phase
* checking the configured screenshot policy
* capturing the existing failure screenshot when enabled
* storing the screenshot under `reports/screenshots/`
* attaching the same successfully captured PNG to Allure

The framework uses the existing pytest-playwright browser and context model.

It does not manually start or own Playwright browser processes.

The project-level `context` fixture extends pytest-playwright's `new_context` flow to apply the approved runtime timeout values.

Fixtures prepare deterministic state and support independent execution.

Tests should not depend on state produced by previously executed test cases.

The existing Playwright fixture model and fixture chains provide isolated setup for individual tests.

Cart, Checkout, E2E, parametrized product scenarios, and logout/re-login behavior were validated under pytest-xdist parallel execution.

### Failure Screenshot Behavior

The default screenshot policy is:

```text
QA_SCREENSHOT_POLICY=only-on-failure
```

The failure screenshot path is:

```text
reports/screenshots/
```

Screenshot filenames contain:

* the test name
* a UTC timestamp

The screenshot hook reacts to failed test-call reports.

It does not capture screenshots for setup-phase or teardown-phase failures.

The screenshot is captured once.

After successful capture, the same PNG file is attached to Allure as:

```text
Failure screenshot
```

when Allure result collection is active.

This avoids a second screenshot implementation.

When:

```text
QA_SCREENSHOT_POLICY=off
```

the custom screenshot is not written and the corresponding Allure screenshot attachment is not created.

If screenshot capture fails, there is no Allure screenshot attachment because no image file exists.

If Allure attachment fails after screenshot capture, the original screenshot remains available under `reports/screenshots/`.

This keeps the base failure evidence independent of the advanced reporting layer.

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

The project uses:

```text
--strict-markers
```

Markers used by automated tests must therefore be registered in `pytest.ini`.

pytest-xdist execution is enabled through command-line options such as:

```text
-n auto
```

Parallel execution is not forced globally through `pytest.ini`.

This preserves supported sequential execution.

Allure result collection is also enabled per execution through command-line arguments rather than forced globally.

Phase 4E runtime settings are provided by environment variables and `config/settings.py` rather than being hardcoded into `pytest.ini`.

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

Current execution and reporting dependencies include:

* pytest
* pytest-playwright
* pytest-xdist
* pytest-html
* allure-pytest

The standalone Allure CLI is not a Python project dependency.

It is an external report-generation prerequisite.

### `requirements-lock.txt`

Contains locked dependency versions for reproducible:

* local setup
* CI installation

The locked dependency set includes the active Playwright/Pytest execution, parallelization, reporting, and quality-tool dependencies.

pytest-playwright provides the Playwright/Pytest integration used by the runtime configuration layer.

pytest-xdist is an active Phase 4C execution capability.

Allure Pytest integration is an active Phase 4D reporting capability.

The standalone Allure CLI remains separate from the Python dependency lock.

### `.gitignore`

Defines files and directories that should not be tracked by Git.

Relevant generated-output rules include:

```text
reports/*
!reports/.gitkeep

allure-results/
allure-report/
test-results/
playwright-report/
```

The currently implemented report paths under `reports/` are therefore treated as generated runtime content.

pytest-playwright trace and video output under `test-results/` is also treated as generated runtime content.

## Current Page-Level Test Suite Structure

The project follows one manual test case file and one automated functional test module per covered page area.

Runtime configuration is applied as a cross-cutting execution concern and does not change page-level test ownership.

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
runtime configuration
        ↓
reporting
        ↓
CI execution
```

Depending on marker assignment, Login tests may participate in:

* dedicated parallel Smoke CI execution
* dedicated parallel Regression CI execution
* parallel complete full-suite CI execution
* complete full-suite Allure reporting

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
runtime configuration
        ↓
reporting
        ↓
CI execution
```

Depending on marker assignment, Inventory tests may participate in:

* dedicated parallel Smoke CI execution
* dedicated parallel Regression CI execution
* parallel complete full-suite CI execution
* complete full-suite Allure reporting

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
runtime configuration
        ↓
reporting
        ↓
CI execution
```

Depending on marker assignment, Product Details tests may participate in:

* dedicated parallel Smoke CI execution
* dedicated parallel Regression CI execution
* parallel complete full-suite CI execution
* complete full-suite Allure reporting

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
runtime configuration
        ↓
reporting
        ↓
CI execution
```

Depending on marker assignment, Cart tests may participate in:

* dedicated parallel Smoke CI execution
* dedicated parallel Regression CI execution
* parallel complete full-suite CI execution
* complete full-suite Allure reporting

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
runtime configuration
        ↓
reporting
        ↓
CI execution
```

Depending on marker assignment, Checkout tests may participate in:

* dedicated parallel Smoke CI execution
* dedicated parallel Regression CI execution
* parallel complete full-suite CI execution
* complete full-suite Allure reporting

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

Approved parallel suite commands include:

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

Marker semantics, runtime configuration, xdist distribution, and reporting are separate concerns.

pytest-xdist determines how collected tests are distributed and does not change marker assignment.

Runtime configuration determines approved execution behavior and does not change marker assignment.

Allure consumes the results produced by the selected execution and also does not change marker assignment.

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

Because the full suite collects Allure results, the E2E checkpoints are also represented in the full-suite Allure reporting data.

Their independent checkpoint architecture is therefore part of the current parallel-safety model.

Runtime configuration applies to E2E execution in the same way as to the remaining functional suites.

## Reporting Structure

The framework currently uses complementary reporting and diagnostic mechanisms.

### pytest-html

pytest-html is the lightweight HTML report solution.

Current CI report files:

```text
reports/smoke-report.html
reports/regression-report.html
reports/report.html
```

Smoke and Regression remain focused on pytest-html.

Full-suite also keeps pytest-html after Allure integration.

### Allure Result Collection

Allure Pytest integration collects structured execution data.

Current result location:

```text
reports/allure-results/
```

Sequential example:

```bash
pytest -v \
  --alluredir=reports/allure-results \
  --clean-alluredir
```

Parallel example:

```bash
pytest -n auto -v \
  --alluredir=reports/allure-results \
  --clean-alluredir
```

### Allure HTML Generation

The standalone Allure CLI converts result data into the generated HTML report.

Current command:

```bash
allure generate reports/allure-results \
  --clean \
  -o reports/allure-report
```

Current generated location:

```text
reports/allure-report/
```

The Allure CLI is an external prerequisite for HTML generation.

The Python `allure-pytest` package and the standalone Allure CLI have different responsibilities.

### Failure Screenshots

Failure screenshots are produced by the existing Pytest hook when:

```text
QA_SCREENSHOT_POLICY=only-on-failure
```

and the failure occurs during the Pytest call phase.

Current location:

```text
reports/screenshots/
```

The same captured PNG is reused as the Allure attachment when Allure result collection is active.

This keeps one screenshot capture mechanism.

When:

```text
QA_SCREENSHOT_POLICY=off
```

the custom screenshot and corresponding Allure screenshot attachment are disabled.

### Trace And Video

Trace and video are optional runtime diagnostics provided through pytest-playwright / Playwright.

Current runtime policies:

```text
QA_TRACE_POLICY
QA_VIDEO_POLICY
```

Supported values:

```text
off
retain-on-failure
on
```

Both default to:

```text
off
```

When enabled, runtime files are generated under pytest-playwright's artifact structure rooted under:

```text
test-results/
```

Generated files may include:

```text
trace.zip
video.webm
```

The project does not maintain custom trace or video recording implementations.

### GitHub Actions Artifacts

Generated CI outputs are published through GitHub Actions artifacts.

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
full-suite-allure-report
test-artifacts
```

The dedicated Allure artifact publishes:

```text
reports/allure-report/
```

The existing broader full-suite runtime artifact continues to publish:

```text
reports/
```

Artifact retention remains seven days.

Trace and video are disabled in CI by default and are not introduced as default retained CI artifacts.

Allure history persistence, report hosting, and GitHub Pages reporting are not implemented.

## Local And CI Execution Structure

Local validation supports:

* page-level execution
* marker-based execution
* sequential full-suite execution
* pytest-xdist parallel execution
* environment-based runtime overrides
* pytest-html reporting where required
* Allure result collection
* Allure HTML generation
* optional screenshot, trace, and video policy overrides
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

Example runtime override:

```bash
QA_BROWSER=chromium \
QA_HEADED=false \
QA_TIMEOUT_MS=45000 \
QA_EXPECT_TIMEOUT_MS=7000 \
QA_TRACE_POLICY=retain-on-failure \
pytest -m smoke -n auto -v
```

Example full-suite reporting validation:

```bash
pytest -n auto -v \
  --html=reports/report.html \
  --self-contained-html \
  --alluredir=reports/allure-results \
  --clean-alluredir
```

Then:

```bash
allure generate reports/allure-results \
  --clean \
  -o reports/allure-report
```

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

### Phase 4D Reporting Layer

Phase 4D preserves the same job structure and adds reporting responsibilities:

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
        └── Allure HTML report
```

No additional browser job is introduced.

### Phase 4E Runtime Configuration Layer

Phase 4E preserves the existing Phase 4B–4D execution and reporting structure while adding centralized runtime values.

The browser jobs use:

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

These defaults match the approved local configuration.

Phase 4E does not introduce:

* new CI jobs
* browser matrices
* Firefox or WebKit CI installation
* cross-browser CI execution
* retries
* `continue-on-error`
* trace or video retention by default

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

Smoke does not generate a dedicated Allure report.

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

Regression does not generate a dedicated Allure report.

### Full-Suite CI Execution

The full-suite job installs Chromium and executes the complete unfiltered test suite.

Current command:

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

The workflow then attempts to generate:

```text
reports/allure-report/
```

from the available Allure results.

The full-suite job remains the complete automated regression gate.

### Allure CI Prerequisites

The full-suite job additionally configures:

```text
Java 17
Allure CLI
```

Java is configured through:

```text
actions/setup-java@v4
```

The Allure CLI is installed with:

```bash
npm install -g allure-commandline
```

These tools are required for Allure HTML generation and are not added to Smoke or Regression.

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
full-suite-allure-report
test-artifacts
```

Artifact upload steps use:

```yaml
if: always()
```

so available reports and runtime outputs can still be published when an executing browser-test command fails.

The Allure generation step checks for usable Allure result data before invoking the report generator.

A failed test command still fails the relevant browser job.

Reporting does not convert a failed test execution into a successful CI result.

Current artifact retention remains seven days.

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
* runtime configuration must remain process-level execution configuration rather than test-to-test state

The current suite was validated through sequential and parallel execution.

No sequential-only test exceptions were identified.

## Parallel Execution And Reporting

Phase 4D reporting operates on top of the same execution model.

Current reporting expectations include:

* pytest-html remains compatible with xdist
* Allure result collection remains compatible with xdist
* failure screenshots remain compatible with xdist
* the same failure screenshot can be attached to Allure
* Allure result collection also works with sequential execution
* no separate sequential-only reporting implementation is maintained

Execution mode and reporting mode remain separate concepts.

Phase 4E runtime configuration also applies to both sequential and parallel execution without requiring separate test implementations.

## Current Phase Boundaries

The current framework combines implemented Phase 4B, Phase 4C, Phase 4D, and Phase 4E behavior.

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
* preserved pytest-html and artifact behavior
* Chromium-only CI browser scope

Implemented Phase 4D reporting capabilities include:

* Allure Pytest integration
* local Allure result collection
* local Allure HTML generation
* Allure CLI as an HTML-generation prerequisite
* failure screenshot attachment to Allure
* reuse of the existing screenshot mechanism
* sequential reporting compatibility
* pytest-xdist reporting compatibility
* full-suite CI Allure result collection
* full-suite CI Allure HTML generation
* dedicated `full-suite-allure-report` artifact
* preservation of pytest-html
* preservation of existing artifact behavior

Implemented Phase 4E runtime configuration capabilities include:

* centralized runtime configuration through `config/settings.py`
* configurable application base URL
* browser selection
* headed/headless configuration
* action/navigation timeout configuration
* assertion timeout configuration
* screenshot policy
* trace policy
* video policy
* environment-variable normalization
* fail-fast invalid configuration handling
* integration with pytest-playwright native runtime mechanisms
* preservation of explicit native browser/trace/video command-line options where applicable
* explicit runtime defaults in Smoke, Regression, and full-suite CI jobs
* preservation of Chromium-only CI execution
* preservation of the existing CI topology and reporting architecture

GitHub Actions job-level concurrency and pytest-xdist worker-level parallelism remain separate execution mechanisms.

Reporting and runtime configuration are separate concerns layered on top of test execution.

The current Phase 4E implementation does not introduce:

* named environment profiles
* automatic `.env` loading
* browser matrices
* cross-browser CI
* Firefox or WebKit CI installation
* device emulation
* retries
* Phase 4F logging or fixture cleanup

Formal Phase 4E completion in `docs/roadmap.md` remains deferred to the dedicated Phase 4E checkpoint.

## Architecture Goals

The project structure is designed to support:

* maintainable test organization
* one automated functional module per covered page area
* one manual test case file per covered page area
* clear layer responsibilities
* Page Object Model
* shared authenticated behavior through `AppPage`
* reusable assertion helpers
* centralized test data
* reusable fixtures
* centralized runtime configuration
* environment-based execution overrides
* fail-fast invalid configuration handling
* deterministic execution
* test independence
* sequential execution
* pytest-xdist parallel execution
* explicit marker semantics
* selective local suite execution
* pytest-html reporting
* advanced Allure reporting
* configurable failure screenshot evidence
* optional Playwright trace and video generation
* dedicated Smoke CI feedback
* dedicated Regression CI feedback
* complete full-suite CI validation
* staged CI quality gating
* explicit CI runtime defaults
* clear separation of job-level and worker-level concurrency
* clear separation of runtime configuration and test logic
* clear separation of execution and reporting concerns
* clear separation of runtime output and repository content
* test case traceability
* stable portfolio promotion

Future UI, API, cross-browser, reporting, diagnostics, and execution improvements should extend this foundation without weakening current responsibility boundaries.

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
* focused runtime configuration tests
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
* centralized runtime configuration
* configurable base URL
* configurable browser selection
* configurable headed/headless execution
* configurable Playwright timeouts
* configurable screenshot policy
* configurable trace policy
* configurable video policy
* invalid configuration validation
* separate CI quality validation
* dedicated parallel Smoke CI execution
* dedicated parallel Regression CI execution
* parallel complete full-suite CI validation
* explicit CI runtime defaults
* Chromium-only CI execution
* pytest-html reporting
* Allure result collection
* Allure HTML generation
* screenshot capture on failure
* failure screenshot attachment to Allure
* optional trace generation
* optional video generation
* job-specific CI artifacts
* dedicated full-suite Allure artifact

The `main` branch represents the stable portfolio version of the framework.

The `develop` branch and active workstream branches may contain newer validated changes before promotion.

Current CI structure:

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

UI, Security, Sorting, Navigation, and E2E do not currently have dedicated CI jobs.

pytest-xdist parallel execution is implemented.

Allure reporting is implemented locally and in the full-suite CI reporting path.

Runtime configuration is implemented locally and integrated into the three browser-test CI jobs.

Current CI remains Chromium-only and headless by default.

Trace and video policies are implemented but disabled by default.

Phase 4E implementation through AQA-0100–AQA-0103 is integrated into `develop`.

Formal Phase 4E roadmap completion remains deferred to the dedicated Phase 4E checkpoint.

Future improvements may include:

* fixture organization improvements
* lightweight logging
* failed-test diagnostics
* diagnostic quality review
* advanced reporting analytics
* API testing structure
* cross-browser execution
* Selenium comparison
* additional application areas when approved

Allure history persistence, report hosting, GitHub Pages reporting, retries, named environment profiles, automatic `.env` loading, API testing, CI browser matrices, and cross-browser CI execution remain outside the current implemented scope.