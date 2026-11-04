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
* [Docker Execution](#docker-execution)
* [Visual Regression Testing](#visual-regression-testing)
* [Selenium WebDriver E2E Showcase](#selenium-webdriver-e2e-showcase)
* [Runtime Configuration](#runtime-configuration)
* [Diagnostics And Fixture Organization](#diagnostics-and-fixture-organization)
* [Quality Checks](#quality-checks)
* [CI Execution](#ci-execution)
* [Reports And Artifacts](#reports-and-artifacts)
* [Documentation](#documentation)
* [Roadmap](#roadmap)
* [Navigation Notes](#navigation-notes)

## Project Overview

This repository contains a QA Automation Framework built primarily with Playwright, Pytest, and Python, with a deliberately limited Selenium WebDriver capability for a representative secondary E2E showcase.

The project serves as both a practical automation engineering playground and a portfolio-oriented framework designed to showcase modern test automation practices, framework architecture, tooling integration, and quality engineering workflows.

The framework remains primarily focused on Playwright-based UI automation while also demonstrating a separate Chrome-only Selenium WebDriver E2E capability. It is developed with a strong emphasis on:

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
* reproducible Docker-based Playwright test execution alongside local WSL/Linux and native GitHub Actions
* automated quality validation
* dedicated Smoke and Regression CI execution
* complete full-suite CI validation
* representative cross-browser Smoke validation on Firefox and WebKit
* deterministic Chromium-only visual regression checkpoints with dedicated Docker-based CI validation
* a deliberately limited Selenium WebDriver 4.51.0 purchase-flow showcase on Chrome
* an isolated Selenium Page Object layer under `selenium_pages/`
* isolated Selenium execution under `selenium_tests/`, outside the default Playwright `testpaths = tests` collection
* Chromium as the primary complete Playwright regression browser
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

Completed Phase 4 framework maturity scope includes:

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

Phase 5 implementation is in progress.

Implemented Phase 5A cross-browser execution behavior includes:

* Chromium remains the primary browser for Smoke, Regression, and complete full-suite execution
* Firefox executes the existing representative Smoke suite
* WebKit executes the existing representative Smoke suite
* Firefox and WebKit do not execute the complete Regression suite or complete full suite
* the existing `smoke` marker is reused without introducing browser-specific test modules or markers
* cross-browser Smoke execution uses `pytest-xdist` with automatic worker selection
* Firefox and WebKit produce independent browser-specific pytest-html reports and GitHub Actions artifacts
* the same centralized runtime configuration mechanism selects Chromium, Firefox, or WebKit

The Phase 5B containerized Playwright execution functionality implemented in AQA-0115 is complete and available on the current development branch. It provides:

* an official Playwright Python Docker base image pinned to `mcr.microsoft.com/playwright/python:v1.60.0-noble`, aligned with `playwright==1.60.0` in `requirements-lock.txt`
* a repository-root `Dockerfile` and `.dockerignore` for reproducible environment builds without copying local virtual environments, generated artifacts, or `.env` files
* sequential and pytest-xdist parallel execution of existing tests without Docker-specific test logic
* runtime overrides through the existing `QA_*` configuration, including browser selection
* host-persistent pytest-html, Allure results, failure screenshots, Playwright traces, and videos through bind mounts
* an additional execution path that does not replace native GitHub Actions CI or the local WSL/Linux workflow

Phase 5B has been formally completed through AQA-0117. The same Docker image is reused in Phase 5C for a dedicated visual regression CI job without containerizing existing native functional jobs.

Phase 5C Visual Regression Testing is implemented through AQA-0118–AQA-0120: Pillow PNG comparison, two reviewed `standard_user` checkpoints, Chromium baselines, an isolated `visual_tests/` suite, explicit baseline refresh, controlled `visual_user` mismatch evidence, and one Docker-based GitHub Actions visual job. Phase 5C was validated against the seven-execution CI topology that existed before the Selenium job was added.

Phase 5D Selenium WebDriver E2E Showcase is implemented through AQA-0123–AQA-0125. It adds Selenium 4.51.0 with built-in Selenium Manager, a Chrome-only WebDriver fixture, a separate `selenium_pages/` Page Object layer, isolated `selenium_tests/`, one representative purchase journey expressed as eight independent E2E tests, shared engine-independent credentials/product/customer data, explicit Selenium waits, deterministic browser cleanup, and one dedicated native Selenium CI execution. The resulting GitHub Actions topology now has eight executions. Formal Phase 5D status in `docs/roadmap.md` remains `Future` until the AQA-0127 closing checkpoint.

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

Phase 4 Framework Maturity is complete. Phase 5 Advanced Browser Automation And Execution remains in progress, with Phase 5A cross-browser Smoke validation, Phase 5B Docker execution, Phase 5C visual regression, and the Phase 5D Selenium WebDriver E2E showcase implemented.

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
* Selenium WebDriver purchase-flow showcase checkpoints
* shared page-level behavior validation through reusable Page Objects

Some manual test case files also contain documented `Planned` scenarios that do not yet have dedicated automated tests.

The individual test case files remain the source of truth for Playwright page-level automation status.

The separate Selenium showcase reuses the same application behavior and engine-independent test data without duplicating the complete Playwright regression suite. Its representative purchase journey covers Login → Inventory → Product Details → Cart → Checkout Information → Checkout Overview → Checkout Complete → Inventory through eight independent Selenium E2E tests under `selenium_tests/`.

The existing representative Playwright Smoke coverage is validated across Chromium, Firefox, and WebKit.

This cross-browser execution expands browser-engine compatibility validation without introducing additional functional test cases or complete three-browser Regression coverage.

Future automated test areas may include:

* broader end-to-end journey coverage beyond the current primary purchase checkpoints
* API-level tests
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
* `visual` (dedicated `visual_tests/` only; excluded from default `tests/` collection)
* `selenium` (dedicated `selenium_tests/` only; excluded from default `tests/` collection)

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
* **Selenium** — tests executed through the dedicated Selenium WebDriver layer rather than pytest-playwright

The Playwright and Selenium E2E checks do not depend on test execution order or state produced by another test.

Each Playwright E2E checkpoint prepares its own required state through Playwright fixtures or test setup. The Selenium showcase follows the same independence principle: every Selenium E2E test receives a fresh Chrome WebDriver session and fixture-built prerequisite state.

Application scenario fixtures remain explicit and scenario-oriented.

Current reusable scenario fixtures are defined under:

```text
tests/conftest.py
```

The dedicated Selenium scenario fixtures are defined separately under:

```text
selenium_tests/conftest.py
```

They own Chrome WebDriver creation and cleanup plus Selenium-specific prerequisite state. They reuse engine-independent data from `test_data/` but do not reuse Playwright Page Objects or Playwright browser fixtures.

The repository-level:

```text
conftest.py
```

remains reserved for framework-wide Pytest configuration, runtime integration, Playwright context configuration, and failure diagnostics.

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

Current CI uses dedicated Playwright Chromium jobs for:

* Smoke
* Regression
* complete full-suite execution

A dedicated Playwright cross-browser Smoke matrix additionally executes the existing Smoke suite on:

* Firefox
* WebKit

The isolated Selenium showcase has its own dedicated native `selenium-e2e` CI job on Chrome and executes:

```bash
pytest selenium_tests -m "selenium and e2e" -v
```

The following Playwright marker suites remain selectively executable locally and do not currently have dedicated CI jobs:

* UI
* Security
* Sorting
* Navigation
* E2E

Tests carrying those Playwright markers are still included in the complete unfiltered Chromium full-suite CI execution. Selenium tests remain outside that default collection because `pytest.ini` keeps `testpaths = tests`; they are collected only when `selenium_tests/` is explicitly targeted.

Detailed marker definitions, assignment rules, parallel execution behavior, runtime configuration behavior, fixture ownership, diagnostic behavior, and examples are documented in:

* [Testing Strategy](docs/testing-strategy.md)

## Technology Stack

### Core Technologies

* Python 3.12
* Pytest
* Playwright
* pytest-playwright
* Selenium WebDriver 4.51.0
* pytest-xdist
* Git
* GitHub
* GitHub Actions
* WSL2 with Ubuntu Linux
* Docker Engine / Docker Desktop for optional containerized execution
* official Playwright Python Docker image `mcr.microsoft.com/playwright/python:v1.60.0-noble`
* Pillow for PNG visual comparison and highlighted pixel-difference evidence

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
* version-controlled approved visual baselines and separate generated actual/diff PNG evidence

### CI

* GitHub Actions
* dedicated quality validation
* Chromium Smoke execution
* Chromium Regression execution
* Chromium complete full-suite execution
* representative Firefox Smoke execution
* representative WebKit Smoke execution
* Firefox/WebKit cross-browser matrix execution
* dedicated sequential Docker/Chromium `visual-regression` CI job using existing project Dockerfile
* independent `visual-regression-artifacts` upload, including on failure
* dedicated native `selenium-e2e` execution on system Chrome
* built-in Selenium Manager for ChromeDriver discovery/lifecycle
* dedicated `selenium-e2e-pytest-html-report` artifact
* pytest-xdist worker-level parallel execution in Playwright functional browser-test jobs (visual and Selenium validation are sequential)
* full-suite Allure result collection and HTML report generation on Chromium
* browser-specific pytest-html reports for Firefox and WebKit Smoke validation
* independent browser-specific GitHub Actions artifacts
* explicit runtime defaults for browser-test jobs
* runtime and failure diagnostic output visible through normal Pytest execution logs

### Installed For Future Expansion

* requests

The currently implemented framework remains Playwright-first for primary functional regression and cross-browser coverage, while Selenium WebDriver is implemented as a deliberately limited secondary Chrome-only E2E showcase.

Pytest parallel execution with `pytest-xdist` is implemented locally and in the existing CI browser-test jobs.

Allure reporting is implemented locally and in the complete full-suite CI job while pytest-html remains the lightweight report format used across the existing reporting workflow.

Runtime configuration is implemented through environment variables and the centralized `config/settings.py` module.

Phase 4F diagnostics use lightweight console/report output and the standard Python logging API for diagnostic-operation errors.

The diagnostics layer does not introduce persistent project log files.

Application scenario fixtures are maintained separately from framework-wide Pytest integration through `tests/conftest.py` and the repository-level `conftest.py`.

The current configuration layer does not load `.env` files or implement named environment profiles.

Docker execution is an additional reproducible test-running option using the same Pytest configuration and `QA_*` runtime settings. Existing functional GitHub Actions browser-test jobs continue to execute natively; only the Phase 5C visual regression job builds and runs the existing Docker image.

API testing, Jenkins integration, complete Firefox/WebKit Regression execution, complete Firefox/WebKit full-suite execution, complete Selenium regression duplication, Selenium Grid, a Selenium cross-browser matrix, generic shared Playwright/Selenium Page Object abstractions, device emulation, Allure history persistence, persistent log files, browser console capture, network capture beyond existing Playwright trace behavior, and hosted report publishing remain outside the current implemented framework scope.

## Getting Started

### Prerequisites

Before setting up the framework, ensure the following tools are installed:

* Python 3.12+
* Git
* WSL2 with Ubuntu Linux or another compatible Linux environment
* IDE or editor of choice
* Playwright-supported browser dependencies
* Google Chrome when executing the Selenium WebDriver showcase locally
* Allure CLI available on `PATH` when local Allure HTML report generation is required

For the alternative Docker execution path, install Docker Engine or Docker Desktop with working Linux-container support and access to the Docker daemon. Docker builds and runs the required Python and Playwright environment inside the image; a host Python virtual environment and separate host Playwright browser installation are not required for this path.

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

### 4. Install Playwright Browsers

For the complete currently validated local browser set on Linux or WSL2:

```bash
playwright install --with-deps chromium firefox webkit
```

If system dependencies are already installed:

```bash
playwright install chromium firefox webkit
```

Chromium remains the primary browser for complete Regression and full-suite validation.

Firefox and WebKit are additionally validated through the representative Smoke suite.

The framework therefore provides implemented compatibility validation across the three Playwright browser engines without claiming complete three-browser Regression coverage.

Selenium is installed through the project dependency files and does not require a separately pinned ChromeDriver package. `webdriver.Chrome()` uses Selenium Manager to resolve the compatible driver automatically. The implemented Phase 5D Selenium scope is Chrome-only.

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

Run representative Smoke validation on Firefox:

```bash
QA_BROWSER=firefox pytest -m smoke -n auto -v
```

Run representative Smoke validation on WebKit:

```bash
QA_BROWSER=webkit pytest -m smoke -n auto -v
```

Chromium remains the primary complete regression browser.

Firefox and WebKit reuse the same Smoke suite for representative browser-engine compatibility validation rather than executing complete Regression or full-suite coverage.

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

The default `pytest -v` and marker commands above use `testpaths = tests`, so they do not collect the isolated Selenium suite. Run the Selenium WebDriver showcase explicitly:

```bash
pytest selenium_tests -m "selenium and e2e" -v
```

Run the complete Selenium directory, including the WebDriver lifecycle check:

```bash
pytest selenium_tests -v
```

Selenium execution is intentionally sequential; the showcase does not use `pytest-xdist`.

Chromium Smoke and Regression are executed as dedicated GitHub Actions jobs.

The complete unfiltered Chromium suite remains the full-suite CI regression gate.

Firefox and WebKit additionally execute the existing Smoke suite through the dedicated cross-browser CI matrix.

Existing Playwright functional browser-test CI executions use `pytest-xdist` with automatic worker selection. The separate visual regression job and Selenium E2E job use sequential execution.

## Docker Execution

Phase 5B containerized Playwright execution is implemented through the repository-root [`Dockerfile`](Dockerfile) and [`.dockerignore`](.dockerignore). It complements local WSL/Linux execution and does not replace native functional GitHub Actions jobs. Phase 5C reuses that image for one dedicated visual CI job. All commands below are run from the repository root in a Linux/WSL shell with a working Docker Engine.

### Image Build And Execution Model

The Dockerfile uses `mcr.microsoft.com/playwright/python:v1.60.0-noble` as its base image, matching `playwright==1.60.0` in `requirements-lock.txt`. The official image provides the Playwright browser binaries and required Linux system dependencies; the Python dependencies, including Playwright and Pytest, are installed from the locked requirements. The Dockerfile copies the lockfile before the rest of the source so unchanged dependencies can reuse Docker build cache. No separate `playwright install` step is needed inside this image.

Build the image after cloning the repository or whenever changed project files need to be included in the image:

```bash
docker build -t playwright-qa-framework:local .
```

The build includes a snapshot of the source allowed by `.dockerignore`. Changing a test, fixture, Page Object, or locked dependency does not update an existing image; rebuild it when the container must execute the new code. Changing test selection or `QA_*` values at runtime does not require a rebuild.

The image defines `ENTRYPOINT ["python", "-m", "pytest"]` and default arguments `CMD ["-v"]`. Running the image without arguments executes the full configured Pytest suite. To run the representative Chromium Smoke suite sequentially:

```bash
docker run --rm --init --ipc=host playwright-qa-framework:local -m smoke -v
```

The recommended runtime flags are `--rm` (remove the stopped container), `--init` (handle child processes and signals), and `--ipc=host` (share the Docker host's IPC namespace, recommended for Chromium in this Linux-container setup). Use these flags only in a trusted local execution environment. The application under test remains the externally hosted Sauce Demo site; it is not started by Docker.

### Parallel Execution And Browser Configuration

The image includes `pytest-xdist` and supports the existing marker selection and Pytest options. For a controlled `-n auto` run with two workers:

```bash
docker run --rm --init --ipc=host \
  -e PYTEST_XDIST_AUTO_NUM_WORKERS=2 \
  playwright-qa-framework:local -m smoke -n auto -v
```

`-n auto` uses pytest-xdist automatic worker selection; `PYTEST_XDIST_AUTO_NUM_WORKERS=2` explicitly limits that example to two workers. The container also accepts the same `QA_*` environment variables as local Pytest. For example, the existing runtime configuration selects Firefox without building a separate image:

```bash
docker run --rm --init --ipc=host \
  -e QA_BROWSER=firefox \
  playwright-qa-framework:local -m smoke -v
```

The supported configuration surface is `QA_BASE_URL`, `QA_BROWSER`, `QA_HEADED`, `QA_TIMEOUT_MS`, `QA_EXPECT_TIMEOUT_MS`, `QA_SCREENSHOT_POLICY`, `QA_TRACE_POLICY`, and `QA_VIDEO_POLICY`. Use `docker run -e NAME=value` for the required overrides. Chromium and Firefox Smoke execution have been validated in Docker; WebKit is included in the pinned Playwright browser image and supported by the same framework configuration, but is not presented as a separately validated Docker run. The validated browser runs were headless; headed mode would require additional display integration.

### Persistent Reports And Browser Artifacts

A container's own writable filesystem is removed with `--rm`. Use bind mounts to keep reports on the WSL/Linux host. The project uses `reports/` for pytest-html and project failure screenshots, `allure-results/` for raw Allure output in the example below, and `test-results/` for pytest-playwright traces and videos. Prepare these host directories first:

```bash
mkdir -p reports allure-results test-results
```

The following example combines the supported runtime settings and output locations in one invocation:

```bash
docker run --rm --init --ipc=host \
  --user "$(id -u):$(id -g)" \
  -e QA_TRACE_POLICY=on \
  -e QA_VIDEO_POLICY=on \
  -v "$(pwd)/reports:/app/reports" \
  -v "$(pwd)/allure-results:/app/allure-results" \
  -v "$(pwd)/test-results:/app/test-results" \
  playwright-qa-framework:local \
  -m smoke -v \
  -o cache_dir=/tmp/pytest_cache \
  --html=reports/docker-smoke.html --self-contained-html \
  --alluredir=allure-results/docker-smoke \
  --output=test-results/docker-smoke
```

`--user "$(id -u):$(id -g)"` creates mounted output files with the current WSL/Linux user's UID and GID instead of `root`. With this setting, `-o cache_dir=/tmp/pytest_cache` directs the temporary Pytest cache away from `/app`, which is not writable by the mapped user. The cache is disposable; reports are retained through the mounts. The full command is an example combining separately validated options, not a claim of an additional end-to-end validation run.

With `QA_TRACE_POLICY=on` and `QA_VIDEO_POLICY=on`, pytest-playwright generates `trace.zip` and `video.webm` under the selected `test-results/` output. With the default `QA_SCREENSHOT_POLICY=only-on-failure`, the project's custom screenshot handler writes failed-test call-phase screenshots to `reports/screenshots/` when a Playwright page is available. For regular runs, trace/video may remain `off` or use `retain-on-failure` as supported by the existing runtime configuration.

The `allure-pytest` dependency writes raw result data inside the container. **Allure HTML generation is performed outside the image** using the standalone Allure CLI where it is installed; this image does not install the Allure CLI, Java, or Node.js. For example, on a host with Allure CLI available:

```bash
allure generate allure-results/docker-smoke --clean -o allure-report/docker-smoke
```

Generated runtime results remain ignored artifacts rather than version-controlled files. The same framework also runs directly through Python/Pytest on WSL/Linux. Phase 5B introduced the reusable Docker path, and Phase 5C subsequently reused it in a dedicated Chromium visual regression GitHub Actions job. The original native Playwright CI jobs remain native. Docker Compose and Kubernetes are not introduced by either workstream; Selenium is implemented separately in Phase 5D and is not part of the Docker execution path.

## Visual Regression Testing

Phase 5C adds strict rendered-PNG comparison to complement functional Playwright UI assertions. Functional tests verify expected behavior, page navigation and element state. Visual checkpoints compare selected rendered pages with reviewed screenshot baselines and reveal presentation differences that locator assertions alone may miss.

Visual regression is separate from the project's **failure screenshot** mechanism. The root `conftest.py` captures diagnostic screenshots of failed test calls according to `QA_SCREENSHOT_POLICY`. In contrast, the visual suite deliberately captures actual images on every checkpoint run; `framework/visual_regression.py` compares these with approved PNG files using Pillow (`PIL.Image` and `ImageChops`), reports changed-pixel counts and bounds, and creates magenta-highlighted diff PNGs for content mismatches. A missing baseline produces an error; an ordinary run never creates or approves a baseline.

### Two Approved Checkpoints

`visual_tests/test_visual_checkpoints.py` contains exactly two permanently passing `standard_user` checks:

* **Inventory default** — the logged-in Inventory page with its six products.
* **Cart with one product** — a Cart containing exactly one **Sauce Labs Backpack**.

The reviewed, version-controlled baselines are:

```text
visual_baselines/chromium/inventory-default.png
visual_baselines/chromium/cart-one-product.png
```

Run-generated images and difference evidence belong under Git-ignored paths:

```text
reports/visual/actual/inventory-default.png
reports/visual/actual/cart-one-product.png
reports/visual/diff/inventory-default.png    # generated on mismatch
reports/visual/diff/cart-one-product.png     # generated on mismatch
```

Baseline ownership and runtime evidence ownership are intentionally separate: a baseline update is a deliberate, reviewed Git change; actual and diff outputs are temporary local/CI artifacts, not committed test fixtures.

### Canonical Docker/Chromium Execution

The canonical screenshot environment is the existing project Docker image based on `mcr.microsoft.com/playwright/python:v1.60.0-noble` with locked Playwright 1.60.0. Visual screenshots use **Chromium only**, headless, a **1280 × 720** viewport, device scale factor **1**, light color scheme, reduced motion, CSS screenshot scale, PNG format, disabled screenshot animations and hidden caret. The visual tests also wait for product images to decode before capture.

`visual_tests/conftest.py` rejects Firefox, WebKit, mixed browser selections and headed mode before running the dedicated suite. This applies to both normal comparison and explicit baseline refresh; there is no visual Firefox/WebKit matrix. Normal functional tests continue to use the existing `QA_BROWSER` choices.

Build from the repository root, then run the same read-only baseline comparison used by CI:

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

The `visual` marker is registered in `pytest.ini`. `testpaths = tests` keeps `visual_tests/` out of ordinary Smoke, Regression and full-suite collection. Invoke visual tests explicitly; no `pytest-xdist` workers are used. A direct invocation is `python -m pytest visual_tests -m visual --browser chromium -v`, but baseline approval and canonical comparisons use the pinned Docker environment.

### Explicit Baseline Maintenance

To intentionally regenerate the approved Chromium screenshots **in the canonical Docker environment**, use a writable baseline mount and the explicit `--update-visual-baselines` flag:

```bash
docker run --rm --init --ipc=host \
  -v "$PWD/visual_baselines:/app/visual_baselines" \
  -v "$PWD/reports/visual:/app/reports/visual" \
  -e QA_BASE_URL=https://www.saucedemo.com \
  -e QA_BROWSER=chromium \
  -e QA_HEADED=false \
  playwright-qa-framework:visual \
  visual_tests -m visual --browser chromium --update-visual-baselines -v
```

Rebuild the image before this command if project sources have changed. **Always inspect both regenerated PNGs and their Git diff before approving a baseline change.** Do not pass `--update-visual-baselines` in CI. CI mounts baselines as `:ro`, so it cannot overwrite the approved PNGs.

### Controlled `visual_user` Demonstration

The separate `VISUAL_USER` entry in `test_data/login_test_data.py` was used during AQA-0119 for a **one-off**, deliberately mismatching Inventory capture against the approved `standard_user` baseline. It detected **43,909 differing pixels (4.76%)** and produced `reports/visual/diff/inventory-visual-user.png`. That check is not a permanent Pytest case; `visual_user` is not added to the functional `VALID_USER_CASES` parametrization, and deliberately failing visual validation is not executed in CI.

Exact-pixel comparison can also surface small rendering differences: an intermittent three-pixel local Inventory mismatch was observed during AQA-0120 without changing the comparator tolerance or refreshing the baseline. Both permanent checkpoints subsequently passed in the canonical Docker setup, and the dedicated GitHub Actions visual job passed as part of the seven-execution topology that existed before Phase 5D added the Selenium execution.


## Selenium WebDriver E2E Showcase

Phase 5D adds a deliberately limited Selenium WebDriver capability alongside the primary Playwright framework.

The implementation is intentionally comparative rather than duplicative:

* Playwright remains the primary framework for page-level functional coverage, complete Chromium regression, representative Firefox/WebKit Smoke compatibility validation, Docker execution, visual regression, diagnostics, traces, videos, and the broader regression architecture.
* Selenium provides one representative Chrome-only purchase-flow showcase implemented through its own Page Object layer, fixtures, explicit waits, and CI execution.
* The two browser-automation stacks share engine-independent application data where appropriate but do not share browser-specific Page Objects or browser fixtures.

### Implemented Selenium Scope

The Selenium dependency is pinned to:

```text
selenium==4.51.0
```

The Phase 5D implementation uses:

* Google Chrome only
* Selenium's built-in Selenium Manager through `webdriver.Chrome()`
* no separately managed or repository-pinned ChromeDriver binary
* headless Chrome through `--headless=new`
* a fixed `1280x720` browser window
* one fresh WebDriver instance per test
* deterministic `driver.quit()` cleanup in fixture teardown
* explicit Selenium waits
* shared application base URL and timeout values from `config/settings.py`
* shared credentials, product data, and checkout customer data from `test_data/`

The Selenium implementation is organized separately from Playwright:

```text
selenium_pages/
├── base_page.py
├── login_page.py
├── inventory_page.py
├── product_details_page.py
├── cart_page.py
└── checkout_page.py

selenium_tests/
├── conftest.py
├── test_webdriver_lifecycle.py
└── test_purchase_e2e.py
```

This separation is intentional. Existing Playwright Page Objects under `pages/` are not redesigned into a generic Playwright/Selenium abstraction.

### Selenium Page Objects And Explicit Waits

`selenium_pages/base_page.py` provides the common Selenium Page Object foundation.

`SeleniumBasePage` owns:

* the shared WebDriver reference
* route-based URL construction using `settings.base_url`
* page opening through `driver.get(...)`
* explicit visibility waits
* explicit clickability waits
* explicit exact-URL waits

Selenium waits use `WebDriverWait` with the configured `QA_EXPECT_TIMEOUT_MS` value. `StaleElementReferenceException` is ignored during the wait polling loop so transient Sauce Demo re-renders can be retried instead of failing immediately.

The individual Selenium Page Objects expose application-specific behavior for:

* Login
* Inventory
* Product Details
* Cart
* Checkout Information
* Checkout Overview
* Checkout Complete

The Selenium implementation does not use implicit waits.

### WebDriver Lifecycle

The function-scoped `selenium_driver` fixture in `selenium_tests/conftest.py` creates Chrome through:

`python`
```
webdriver.Chrome(options=options)
```

Selenium Manager resolves the compatible driver automatically.

The fixture configures:

```text
--headless=new
--window-size=1280,720
```

and applies the shared page-load timeout through:

```text
QA_TIMEOUT_MS
```

Browser cleanup is guaranteed through fixture teardown:

`python`
```
try:
    yield driver
finally:
    driver.quit()
```

The dedicated `selenium_tests/test_webdriver_lifecycle.py` check verifies that Chrome WebDriver can open the configured application origin.

### Representative Purchase Journey

The Selenium showcase represents one complete Sauce Demo purchase journey, but the current implementation intentionally expresses that journey as **eight independent E2E tests** rather than one long monolithic test.

The checkpoints are:

1. valid user Login opens Inventory
2. Inventory product navigation opens the expected Product Details page
3. adding the selected product from Product Details makes it visible in Cart
4. Cart opens Checkout Information
5. valid customer data opens Checkout Overview
6. Checkout Overview displays the expected product and order summary
7. Finish displays the expected order confirmation
8. Back Home returns to Inventory

All eight tests are marked with both:

```text
selenium
e2e
```

Each test receives a fresh browser session. Fixture chains reconstruct only the prerequisite application state needed for the behavior under test. Where the same session state can be preserved safely, prerequisite fixtures may navigate directly to the required route instead of repeatedly retesting an earlier UI transition.

This structure keeps each major transition/checkpoint independently diagnosable while still demonstrating the complete purchase flow across the showcase.

### Shared Engine-Independent Test Data

The Selenium fixtures reuse the existing project test data instead of duplicating credentials or expected product/customer values.

Current shared sources include:

```text
test_data/login_test_data.py
test_data/product_test_data.py
test_data/checkout_test_data.py
```

The Selenium showcase currently uses:

* the first valid user from `VALID_USER_CASES`
* the first product from `LIST_OF_PRODUCTS`
* `VALID_CHECKOUT_CUSTOMER`
* existing checkout confirmation and order-summary expectations

This sharing is limited to engine-independent application data. Browser automation code remains separate between Playwright and Selenium.

### Selenium Collection And Local Execution

`pytest.ini` intentionally keeps:

```text
testpaths = tests
```

Therefore, neither `selenium_tests/` nor `visual_tests/` is collected by the ordinary default Playwright suite.

The dedicated Selenium marker is registered as:

```text
selenium: Selenium WebDriver execution tests
```

Run the complete Selenium directory:

```bash
pytest selenium_tests -v
```

Run only the representative Selenium purchase-flow E2E checks:

```bash
pytest selenium_tests -m "selenium and e2e" -v
```

The Selenium showcase is executed sequentially. It does not use `pytest-xdist`.

### Selenium Runtime Configuration Boundary

Phase 5D reuses the centralized settings only where they are engine-independent or directly applicable to Selenium:

* `QA_BASE_URL` — application origin used by Selenium Page Objects
* `QA_TIMEOUT_MS` — Selenium page-load timeout
* `QA_EXPECT_TIMEOUT_MS` — Selenium explicit-wait timeout

The Playwright-specific runtime controls are not used to select or configure the Selenium browser fixture:

* `QA_BROWSER`
* `QA_HEADED`
* `QA_SCREENSHOT_POLICY`
* `QA_TRACE_POLICY`
* `QA_VIDEO_POLICY`

The Selenium fixture explicitly creates Chrome in headless mode for the implemented Phase 5D scope.

Local execution normally uses the shared default:

```text
QA_EXPECT_TIMEOUT_MS=5000
```

The dedicated Selenium CI job overrides it with:

```text
QA_EXPECT_TIMEOUT_MS=15000
```

to provide a larger explicit-wait budget on GitHub-hosted runners without changing the Playwright jobs.

### Selenium Scope Boundaries

Phase 5D deliberately does **not** implement:

* complete Selenium duplication of the Playwright regression suite
* Selenium Grid
* a Selenium Firefox/Edge/WebKit cross-browser matrix
* generic shared Playwright/Selenium Page Object abstractions
* replacement of Playwright
* a second complete regression architecture
* Selenium visual regression
* Selenium trace/video functionality
* pytest-xdist parallel Selenium execution

Playwright remains the project's primary regression and cross-browser framework. Selenium exists as a separate, representative automation capability demonstrating WebDriver lifecycle management, explicit waits, Page Object design, fixture-driven state preparation, shared application data, and native CI execution.

## Runtime Configuration

Phase 4E provides centralized environment-based runtime configuration through:

```text
config/settings.py
```

The configuration layer allows supported execution behavior to be changed without editing automated tests or Page Objects. These same `QA_*` variables can be passed into Docker containers using `docker run -e`, with no separate Docker-specific configuration layer.

The Playwright framework consumes the complete supported runtime surface. The Selenium showcase reuses only `QA_BASE_URL`, `QA_TIMEOUT_MS`, and `QA_EXPECT_TIMEOUT_MS`; its browser remains explicitly Chrome and headless within the Selenium fixture.

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

`QA_BROWSER`, `QA_HEADED`, `QA_SCREENSHOT_POLICY`, `QA_TRACE_POLICY`, and `QA_VIDEO_POLICY` are Playwright runtime controls. They do not select or configure the Selenium WebDriver fixture.

### Base URL

The default application origin is:

```text
https://www.saucedemo.com
```

Playwright Page Objects define relative `ROUTE` values and combine them with the configured base URL through `BasePage`. Selenium Page Objects use the same application origin through their separate `SeleniumBasePage`.

This allows the target application origin to change without editing either browser-automation Page Object layer or its tests.

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

The configuration layer recognizes all three Playwright browser engines.

`QA_BROWSER` applies to Playwright execution only. Phase 5D Selenium execution does not use this setting to select a WebDriver browser; its implemented scope explicitly creates Google Chrome.

The implemented Playwright browser validation strategy is intentionally asymmetric:

* Chromium is the primary browser and executes Smoke, Regression, and the complete full suite
* Firefox executes representative Smoke validation
* WebKit executes representative Smoke validation

Firefox and WebKit compatibility validation reuses the existing `smoke` marker and does not introduce browser-specific test modules or a dedicated cross-browser marker.

Example Firefox Smoke execution:

```bash
QA_BROWSER=firefox pytest -m smoke -n auto -v
```

Example WebKit Smoke execution:

```bash
QA_BROWSER=webkit pytest -m smoke -n auto -v
```

Cross-browser Smoke validation does not imply complete Regression or full-suite execution on all three engines.

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

The Playwright CI browser-test jobs explicitly use:

```text
QA_HEADED=false
```

and therefore remain headless.

The Selenium fixture also runs headless, but does so directly through the Chrome option `--headless=new` rather than through `QA_HEADED`.

### Action And Navigation Timeout

The default Playwright action and navigation timeout is:

```text
QA_TIMEOUT_MS=30000
```

This value is applied to each created Playwright browser context as both:

* the default action timeout
* the default navigation timeout

The Selenium fixture reuses the same `QA_TIMEOUT_MS` value as the WebDriver page-load timeout through `driver.set_page_load_timeout(...)`.

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

The separate Selenium Page Object layer reuses the same setting as its `WebDriverWait` timeout. Local Selenium execution therefore uses the default 5000 ms explicit-wait budget unless overridden. The dedicated Selenium CI job uses `QA_EXPECT_TIMEOUT_MS=15000` to provide additional tolerance on GitHub-hosted runners without changing the Playwright jobs.

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

Playwright trace functionality remains the only currently implemented trace-level browser diagnostic mechanism and is owned by pytest-playwright. The Selenium showcase does not implement Selenium-specific trace/video capture or a separate screenshot diagnostic layer.

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

Run the main local quality and Playwright functional validation checks:

```bash
ruff check .
black --check .
isort . --check-only
pytest -v
```

Validate the isolated Selenium E2E showcase separately:

```bash
pytest selenium_tests -m "selenium and e2e" -v
```

Because `testpaths = tests`, the default `pytest -v` command does not collect `selenium_tests/` or `visual_tests/`.

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

GitHub Actions preserves the existing native Playwright functional jobs, keeps the dedicated Docker-based Phase 5C visual regression execution, and adds one independent native Phase 5D Selenium E2E execution. All executions run on GitHub-hosted Ubuntu runners.

The current GitHub Actions pipeline combines:

* the Phase 4B CI job structure
* the Phase 4C Pytest parallel execution strategy
* the Phase 4D reporting strategy
* the Phase 4E runtime configuration strategy
* the Phase 4F runtime and failure diagnostic behavior
* the Phase 5A representative cross-browser Smoke validation strategy
* the Phase 5C dedicated Docker/Chromium visual regression validation strategy
* the Phase 5D dedicated native Selenium/Chrome E2E validation strategy

The workflow now produces eight CI executions after `quality` and matrix expansion:

```text
quality
├── smoke [Playwright Chromium, native]
├── regression [Playwright Chromium, native]
├── full-suite [Playwright Chromium, native]
├── cross-browser-smoke [Playwright, native]
│   ├── Firefox
│   └── WebKit
├── visual-regression [Playwright Chromium, Docker]
└── selenium-e2e [Selenium Chrome, native]
```

The `quality` job runs first and validates:

* Ruff
* Black
* isort

It does not install Playwright browsers, execute browser tests, or use `pytest-xdist`.

After successful quality validation, the browser-test jobs may execute independently.

### Chromium Execution

Chromium remains the primary complete Playwright regression browser.

The primary Playwright Chromium CI jobs are:

* `smoke`
* `regression`
* `full-suite`

Smoke executes:

```bash
pytest -m smoke -n auto -v
```

The actual CI command also generates its self-contained pytest-html report:

```bash
pytest -m smoke -n auto -v --html=reports/smoke-report.html --self-contained-html
```

Regression executes:

```bash
pytest -m regression -n auto -v
```

The actual CI command also generates its self-contained pytest-html report:

```bash
pytest -m regression -n auto -v --html=reports/regression-report.html --self-contained-html
```

Smoke and Regression intentionally remain focused pytest-html reporting jobs and do not generate duplicate Allure reports.

The full-suite job executes the complete unfiltered Playwright suite through pytest-xdist while generating both pytest-html output and Allure result data:

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

The full-suite job additionally prepares the Allure CLI required for HTML report generation.

### Firefox And WebKit Cross-Browser Smoke Validation

Phase 5A adds the dedicated `cross-browser-smoke` matrix limited to:

```text
firefox
webkit
```

Chromium is intentionally not duplicated in this matrix because it already has dedicated Smoke, Regression, and full-suite jobs.

Each matrix execution:

* depends on `quality`
* installs only its selected Playwright browser engine
* executes headless
* uses the existing centralized runtime configuration
* reuses the existing `smoke` marker
* uses `pytest-xdist` with `-n auto`
* generates a browser-specific self-contained pytest-html report
* uploads browser-specific GitHub Actions artifacts

The cross-browser Smoke execution uses:

```bash
pytest -m smoke -n auto -v
```

with the browser-specific HTML output configured in GitHub Actions as:

```text
reports/${{ matrix.browser }}-smoke-report.html
```

The effective browser is supplied through the existing `QA_BROWSER` runtime configuration from the matrix value.

Firefox and WebKit provide representative Playwright browser-engine compatibility validation.

They do not execute:

* the complete Regression suite
* the complete full suite
* duplicate browser-specific test modules
* a separate cross-browser marker

### Selenium E2E Chrome Validation

Phase 5D adds the dedicated native:

```text
selenium-e2e
```

job.

It:

* depends on `quality`
* runs on `ubuntu-24.04`
* uses Python 3.12
* installs the locked project dependencies
* uses the system Google Chrome available on the GitHub-hosted runner
* relies on Selenium Manager rather than installing a third-party driver manager
* targets only `selenium_tests/`
* selects the `selenium and e2e` classification
* runs sequentially without `pytest-xdist`
* generates a dedicated self-contained pytest-html report
* uploads the Selenium report with `if: always()`

The execution command is:

```bash
pytest selenium_tests -m "selenium and e2e" -v \
  --html=reports/selenium-e2e-report.html \
  --self-contained-html
```

The Selenium job does not install Playwright browser binaries and does not participate in the Playwright Firefox/WebKit matrix.

The successful Phase 5D CI validation executed all eight Selenium E2E checkpoints and preserved the seven pre-existing CI executions unchanged.

### CI Runtime Configuration

The Playwright Chromium Smoke, Regression, and full-suite jobs use:

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

The Firefox and WebKit matrix uses the same Playwright runtime configuration except that `QA_BROWSER` is supplied from the matrix browser value.

The dedicated Selenium E2E job uses only the runtime values that apply to its implementation:

```text
QA_BASE_URL=https://www.saucedemo.com
QA_TIMEOUT_MS=30000
QA_EXPECT_TIMEOUT_MS=15000
```

`QA_EXPECT_TIMEOUT_MS=15000` is intentionally scoped to the Selenium CI job to provide a larger explicit-wait budget on GitHub-hosted runners. The Playwright jobs retain their 5000 ms assertion timeout.

All current browser automation CI execution remains headless.

The current execution strategy therefore is:

* dedicated sequential Docker/Chromium visual regression independent of functional suites
* Playwright Chromium Smoke
* Playwright Chromium Regression
* Playwright Chromium complete full suite
* Playwright Firefox representative Smoke
* Playwright WebKit representative Smoke
* dedicated sequential Selenium Chrome E2E showcase
* pytest-xdist parallel execution in Playwright functional browser-test jobs only
* sequential visual and Selenium execution
* Playwright screenshot-on-failure enabled
* Playwright tracing disabled by default
* Playwright video disabled by default
* runtime configuration summaries available in normal Pytest output
* failed-test diagnostic context available through the shared Pytest integration

GitHub Actions job scheduling, matrix expansion, pytest-xdist worker execution, Docker execution, and Selenium sequential execution remain separate concurrency/execution concerns.

GitHub Actions may execute independent jobs concurrently after `quality`. `pytest-xdist` distributes tests inside the Playwright functional browser-test jobs, `visual-regression` runs its two screenshot checkpoints sequentially inside Docker, and `selenium-e2e` runs its Selenium tests sequentially in native Chrome.

The workflow runs automatically for:

* pushes to `main`
* pushes to `develop`
* Pull Requests targeting `main`
* Pull Requests targeting `develop`

It can also be started manually through `workflow_dispatch`.

The Phase 5A Playwright cross-browser strategy itself still does not introduce:

* complete Firefox Regression
* complete WebKit Regression
* Firefox complete full-suite execution
* WebKit complete full-suite execution
* browser-specific application test coverage
* browser-specific test modules
* browser-specific skip logic
* retries
* `continue-on-error`
* automatic trace enablement after failure
* automatic video enablement after failure

Selenium is implemented separately through Phase 5D and does not expand the Phase 5A browser matrix.

Detailed CI job behavior, dependencies, xdist execution, Selenium execution, runtime defaults, diagnostic visibility, commands, artifacts, and failure handling are documented in:

* [CI/CD Pipeline](docs/ci-cd-pipeline.md)


## Reports And Artifacts

The framework uses complementary reporting and failure-evidence mechanisms across local WSL/Linux, Docker and GitHub Actions. Local Docker runs preserve output through bind mounts; the dedicated visual Docker CI job uploads its mounted `reports/visual/` directory as an independent GitHub Actions artifact, while the native Selenium CI job publishes its own self-contained pytest-html report. See [Docker Execution](#docker-execution), [Visual Regression Testing](#visual-regression-testing), and [Selenium WebDriver E2E Showcase](#selenium-webdriver-e2e-showcase).

The framework uses complementary reporting and failure-evidence mechanisms:

* **pytest console output** — immediate execution feedback and effective runtime summary
* **failure diagnostic sections** — failed-test identity, failure phase, optional page URL, and successful screenshot path
* **pytest-html** — lightweight self-contained HTML reporting
* **Allure** — richer reporting for local complete-suite runs and the CI full-suite job
* **failure screenshots** — browser evidence captured when a test fails during the test call phase
* **visual actual/diff screenshots** — dedicated baseline-comparison evidence, independent of ordinary failure diagnostics
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
reports/firefox-smoke-report.html
reports/webkit-smoke-report.html
reports/selenium-e2e-report.html
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

Failed setup or teardown phases still receive diagnostic test and phase context when Pytest reports those failures.

When trace or video generation is enabled, pytest-playwright-generated diagnostic files are written under its runtime artifact structure, currently rooted under:

```text
test-results/
```

Trace and video are disabled by default locally and in CI.

The project diagnostics layer does not automatically enable trace or video when a test fails.

The Playwright report, screenshot, Allure, trace, video, runtime diagnostic, and fixture behavior is compatible with the approved pytest-xdist parallel execution model.

Sequential execution remains supported. Selenium uses its own sequential execution path and dedicated pytest-html report.

Generated reports, screenshots, traces, videos, Allure results, Allure HTML output, cache files, and other runtime artifacts should not be committed to Git.

The repository ignore policy keeps generated runtime output outside version-controlled project content.

The current CI strategy keeps Chromium Smoke and Regression focused on their existing pytest-html reports.

Current Chromium Smoke artifacts:

* `smoke-pytest-html-report`
* `smoke-test-artifacts`

Current cross-browser Smoke artifacts:

Firefox:

* `firefox-smoke-pytest-html-report`
* `firefox-smoke-test-artifacts`

WebKit:

* `webkit-smoke-pytest-html-report`
* `webkit-smoke-test-artifacts`

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

The existing `test-artifacts` upload continues to preserve the broader functional `reports/` runtime output.

The Docker-based visual job publishes **`visual-regression-artifacts`** from `reports/visual/` using `if: always()`, `if-no-files-found: warn`, and seven-day retention. Passing runs retain actual screenshot PNGs; mismatches additionally generate diff PNG evidence. Baseline files remain under version control and are mounted read-only for CI comparison. The upload and visual job were verified in successful GitHub Actions run `39772869541` (AQA-0120).

The native Selenium job publishes **`selenium-e2e-pytest-html-report`** from:

```text
reports/selenium-e2e-report.html
```

using `if: always()`, `if-no-files-found: warn`, and seven-day retention. Phase 5D CI validation confirmed successful upload together with a passing eight-test Selenium E2E run.

Artifact uploads use separate names between jobs and browser engines to avoid conflicts.

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
  Overview of Playwright-first framework architecture, the isolated Selenium Page Object layer, runtime configuration, diagnostics, fixture responsibility boundaries, execution isolation, reporting responsibilities, and design direction.

* [Framework And Project Structure](docs/framework-and-project-structure.md)
  Explanation of folder structure, Playwright and Selenium test/POM separation, framework-level Pytest responsibilities, scenario fixture ownership, configuration ownership, repository organization, runtime outputs, and execution-model considerations.

* [Technology Stack](docs/technology-stack.md)
  Overview of implemented and planned technologies, including Playwright, Selenium WebDriver 4.51.0, Docker execution, runtime configuration, cross-browser execution, lightweight diagnostics, reporting, and parallel/sequential execution boundaries.

### Engineering Workflow

* [Git Branching Strategy](docs/git-branching-strategy.md)
  Branching model, merge strategy, and repository workflow standards.

* [Workflow](docs/workflow.md)
  Day-to-day workflow for branches, commits, Pull Requests, local validation, Playwright parallel execution, Selenium sequential execution, runtime overrides, cross-browser Smoke validation, diagnostics, reporting, marker execution, and CI responsibilities.

* [CI/CD Pipeline](docs/ci-cd-pipeline.md)
  Current eight-execution GitHub Actions topology: quality, Playwright Chromium Smoke/Regression/full-suite, Firefox/WebKit representative Smoke, Docker/Chromium visual regression, and native Selenium/Chrome E2E; plus runtime defaults, pytest-xdist boundaries, reporting, artifacts, triggers, and CI maturity boundaries.

* [Quality Tooling](docs/quality-tooling.md)
  Ruff, Black, isort, pre-commit, Pytest, pytest-xdist, Playwright runtime configuration, Selenium execution boundaries, project diagnostics, reporting integrations, and local/CI quality gates.

### Testing And Planning

* [Testing Strategy](docs/testing-strategy.md)
  Detailed test design, marker semantics, Playwright primary regression strategy, representative Firefox/WebKit Smoke compatibility validation, Selenium E2E strategy, sequential and parallel execution boundaries, runtime configuration behavior, diagnostics, reporting, fixture responsibility, parametrization, and validation approach.

* [Features Overview](docs/features.md)
  Implemented and planned framework capabilities, including the Phase 5D Selenium WebDriver E2E showcase, Phase 5C visual regression, Phase 5B Docker-based Playwright execution, Phase 5A cross-browser Smoke validation, Phase 4F diagnostics, and fixture organization.

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
* **Phase 4:** Framework Maturity — completed
* **Phase 4A:** Marker Strategy And Test Suite Organization — implemented
* **Phase 4B:** CI Execution Strategy — implemented
* **Phase 4C:** Parallel Execution — implemented
* **Phase 4D:** Reporting Upgrade — implemented
* **Phase 4E:** Runtime Configuration — completed
* **Phase 4F:** Diagnostics And Fixture Cleanup — completed
* **Phase 5:** Advanced Browser Automation And Execution — in progress
* **Phase 5A:** Playwright Cross-Browser Validation — completed
* **Phase 5B:** Containerized Playwright Execution — completed through AQA-0117
* **Phase 5C:** Visual Regression Testing — completed through AQA-0122
* **Phase 5D:** Selenium WebDriver E2E Showcase — implemented and CI-validated through AQA-0125; formal `docs/roadmap.md` closure remains AQA-0127

Phase 4 focused on framework maturity rather than expanding page-level functional coverage.

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

Phase 4F completed the Diagnostics And Fixture Cleanup workstream required before the final Phase 4 checkpoint.

The final Phase 4 checkpoint was completed through AQA-0111 after cross-workstream review of Phase 4A–4F. The validated AQA-0110 functional baseline remained unchanged, so its existing local and CI validation evidence was reused without unnecessary duplicate full-suite execution.

Phase 5 extends the mature Playwright framework with additional browser automation and execution capabilities.

The implemented Phase 5A cross-browser strategy introduces:

* Chromium as the primary complete regression browser
* representative Firefox Smoke compatibility validation
* representative WebKit Smoke compatibility validation
* reuse of the existing Smoke suite without browser-specific duplication
* a dedicated Firefox/WebKit GitHub Actions matrix
* pytest-xdist worker-level execution in cross-browser Smoke CI
* browser-specific pytest-html reports
* independent Firefox and WebKit CI artifacts
* preservation of Chromium Regression and complete full-suite execution

The Phase 5A strategy intentionally does not provide complete three-browser Regression or full-suite execution.

Phase 5B introduced the Docker execution functionality and was formally closed through AQA-0117. Its pinned image and locked Python dependencies remain an additional reproducible path alongside WSL/Linux and native functional CI.

Phase 5C implements controlled Pillow-based visual regression through AQA-0118–AQA-0120: two selected `standard_user` checkpoints, approved Chromium PNG baselines, an isolated visual suite, explicit reviewed refresh, controlled `visual_user` mismatch evidence and one dedicated passing Docker/Chromium CI job. Phase 5C was formally completed through AQA-0122.

Phase 5D implements the Selenium WebDriver E2E showcase through AQA-0123–AQA-0125: Selenium 4.51.0, built-in Selenium Manager, Chrome-only execution, a dedicated `selenium_pages/` Page Object layer, isolated `selenium_tests/`, a WebDriver lifecycle check, eight independent E2E tests representing one complete purchase journey, shared engine-independent test data, explicit waits, deterministic `driver.quit()` cleanup, a dedicated `selenium` marker, and one native Selenium/Chrome CI execution with its own pytest-html artifact. Playwright remains the primary regression and cross-browser framework. Formal Phase 5D completion in `docs/roadmap.md` remains reserved for AQA-0127.

Phase 4 is complete. Phase 5 implementation remains in progress, with Phase 5A, 5B, 5C, and the Phase 5D implementation capabilities already present in the framework.

Future extension areas include:

* API-level testing
* hybrid UI and API scenarios
* Jenkins integration
* advanced test analytics

The detailed and authoritative roadmap is maintained in [docs/roadmap.md](docs/roadmap.md).

## Navigation Notes

* Clickable links point directly to Markdown files in the repository.
* GitHub automatically renders `.md` files.
* Extended documentation is version-controlled alongside the framework.
* Detailed test strategy, runtime configuration behavior, Docker execution strategy, cross-browser execution strategy, Selenium E2E strategy, diagnostic behavior, fixture ownership, reporting behavior, and execution boundaries remain in `docs/testing-strategy.md`.
* Detailed CI runtime defaults, native cross-browser Smoke execution, dedicated Docker/Chromium visual regression, native Selenium/Chrome E2E execution, diagnostic visibility, reporting and artifact behavior remain in `docs/ci-cd-pipeline.md`.
* Detailed manual test cases remain under `test_cases/`.
* Runtime reports, Allure outputs, screenshots, traces, videos, Selenium pytest-html output, and other generated evidence are ignored by Git and handled as local outputs or CI artifacts.
* The project diagnostic layer does not create persistent project log files.
