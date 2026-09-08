# Technology Stack

This document describes the technologies, tools, and planned integrations used in the QA automation framework.

The stack is divided into implemented technologies, installed but not fully integrated tools, and planned future extensions.

The `main` branch represents the stable portfolio version of the project, while `develop` and active workstream branches may contain newer validated changes before promotion.

## Core Technologies

The project is currently built with:

* Python 3.12
* Pytest
* Playwright
* pytest-playwright
* Git
* GitHub
* GitHub Actions
* WSL2 with Ubuntu Linux

These technologies form the current implemented UI automation foundation.

## Test Automation

Current implemented test automation stack:

* Playwright for browser automation
* Pytest as the test runner
* pytest-playwright for Playwright and Pytest integration
* Page Object Model for page interaction abstraction
* shared authenticated-page behavior through `AppPage`
* reusable assertion helpers for repeated product and checkout validation
* pytest fixtures for reusable setup
* pytest parametrization for data-driven scenarios
* explicit pytest markers for test categorization
* strict pytest marker validation
* selective local marker-based execution
* dedicated Smoke CI execution
* dedicated Regression CI execution
* complete full-suite CI execution
* independent E2E purchase-journey checkpoints

### Current Pytest Markers

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

Examples include:

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

### Current Browser Execution

Current implemented browser execution:

* Chromium

Chromium is used for both local Playwright execution and current CI browser-test jobs.

Planned browser execution may include:

* Firefox
* WebKit
* cross-browser execution strategy

Firefox, WebKit, and cross-browser execution are future extensions.

### Current Automated UI Coverage

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

### Current Page Object Responsibilities

Current Page Object responsibilities include:

* shared page initialization and opening through `BasePage`
* shared authenticated-page behavior through `AppPage`
* Login page navigation
* username input interaction
* password input interaction
* Login submission
* authentication error handling
* Login UI locator access
* Inventory visibility and product access
* Inventory product sorting
* Product Details navigation from product names
* Product Details navigation from product images
* Product Details content access
* Inventory Cart actions
* Product Details Cart actions
* authenticated Cart link access
* cart badge access
* application menu interactions
* logout support
* reset app state support
* All Items navigation
* About link access
* Cart page access
* Cart item lookup
* Cart item content access
* Cart item removal
* Product Details navigation from Cart
* Continue Shopping
* Checkout entry from Cart
* Checkout Information field access
* Checkout Information submission
* Checkout validation error access
* Checkout input error icon access
* Checkout error close interaction
* Checkout Information cancellation
* Checkout Overview product access
* Checkout Overview price summary access
* Checkout Overview cancellation
* Product Details navigation from Checkout Overview
* Finish action
* Checkout Complete confirmation access
* Back Home navigation

Planned Page Object expansion:

* additional Page Objects only when future application areas require dedicated page-level ownership

## Reusable Assertions

Currently implemented:

```text
framework/assertions/product_assertions.py
```

Current reusable assertion responsibilities include:

* Inventory product card content validation
* Product Details content validation
* Cart item content validation
* Checkout Overview product content validation
* Checkout Overview price summary validation
* Inventory product state validation after navigation
* product price conversion for numeric sorting and checkout calculations

Reusable assertion helpers remain focused on shared validation logic.

They should not own:

* navigation
* browser setup
* fixture setup
* Page Object responsibilities

## Test Data Management

Currently implemented:

* centralized login test data
* centralized product test data
* centralized checkout test data
* valid user credentials
* invalid credential cases
* empty credential cases
* locked out user case
* expected authentication validation messages
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
* Checkout Complete header and message expectations
* deterministic product data shared across Inventory, Product Details, Cart, and Checkout tests
* manual test case IDs used in parametrized output where practical

Current test data files:

```text
test_data/login_test_data.py
test_data/product_test_data.py
test_data/checkout_test_data.py
```

Planned test data expansion may include:

* API test data
* environment-specific test data
* additional UI datasets when future approved scope requires them

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

The same Ruff, Black, and isort checks are executed in the dedicated CI `quality` job.

## Test Execution Strategy

### Full Test Suite

Run the complete automated suite:

```bash
pytest -v
```

The complete unfiltered test suite is also executed in the GitHub Actions `full-suite` job.

### Marker-Based Local Execution

Current marker suites can be executed locally with:

```bash
pytest -m smoke -v
pytest -m regression -v
pytest -m ui -v
pytest -m security -v
pytest -m sorting -v
pytest -m navigation -v
pytest -m e2e -v
```

Useful combined selections include:

```bash
pytest -m "smoke and ui" -v
pytest -m "regression and ui" -v
pytest -m "smoke and navigation" -v
pytest -m "regression and navigation" -v
```

Marker expressions may also be scoped to a test module.

Example:

```bash
pytest tests/test_checkout_page.py -m e2e -v
```

All registered markers remain available for selective local validation.

Dedicated CI jobs currently exist only for:

* `smoke`
* `regression`

The following markers do not currently have dedicated CI jobs:

* `ui`
* `security`
* `sorting`
* `navigation`
* `e2e`

Tests carrying those markers still participate in the complete unfiltered `full-suite` CI execution.

## E2E Execution Model

The current `e2e` suite represents independent checkpoints that collectively form the primary purchase journey.

The logical journey includes:

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

Run the logical E2E suite with:

```bash
pytest -m e2e -v
```

E2E currently remains a selectively executable marker suite without a dedicated GitHub Actions job.

Its tests remain included in complete full-suite CI execution.

## CI/CD And Automation

Current CI technology:

* GitHub Actions

The current Phase 4B CI strategy separates code-quality validation from browser-test execution.

Current job structure:

```text
quality
├── smoke
├── regression
└── full-suite
```

### Quality Job

The `quality` job is the prerequisite CI quality gate.

Current responsibilities:

* repository checkout
* Python 3.12 setup
* dependency installation from `requirements-lock.txt`
* Ruff validation
* Black validation
* isort validation

Current quality commands:

```bash
ruff check .
black --check .
isort . --check-only
```

The quality job does not install Playwright Chromium.

If `quality` fails, Smoke, Regression, and full-suite do not execute.

### Smoke Job

The dedicated Smoke job:

* depends on `quality`
* installs project dependencies
* installs Playwright Chromium
* executes the Smoke marker suite
* generates a self-contained pytest HTML report
* uploads Smoke-specific artifacts

Core marker command:

```bash
pytest -m smoke -v
```

Current report path:

```text
reports/smoke-report.html
```

### Regression Job

The dedicated Regression job:

* depends on `quality`
* installs project dependencies
* installs Playwright Chromium
* executes the Regression marker suite
* generates a self-contained pytest HTML report
* uploads Regression-specific artifacts

Core marker command:

```bash
pytest -m regression -v
```

Current report path:

```text
reports/regression-report.html
```

### Full-Suite Job

The `full-suite` job:

* depends on `quality`
* installs project dependencies
* installs Playwright Chromium
* executes the complete unfiltered automated test suite
* generates a self-contained pytest HTML report
* uploads full-suite artifacts

Core command:

```bash
pytest -v
```

Current report path:

```text
reports/report.html
```

The full-suite job remains the complete CI regression gate.

Dedicated Smoke and Regression jobs provide targeted suite feedback but do not replace complete full-suite validation.

### CI Dependencies

All three browser jobs use:

```yaml
needs: quality
```

Smoke, Regression, and full-suite do not depend on each other.

GitHub Actions may therefore schedule these jobs concurrently after successful quality validation.

This is CI job-level scheduling.

It is not Pytest-level parallel execution with `pytest-xdist`.

### Current CI Targets

The workflow executes automatically for:

* pushes to `main`
* pushes to `develop`
* Pull Requests targeting `main`
* Pull Requests targeting `develop`

The workflow can also be started manually through:

* `workflow_dispatch`

Regular pushes to feature, refactor, fix, or documentation branches do not automatically trigger CI unless the branch participates in a Pull Request targeting `main` or `develop`, or the workflow is started manually.

### Workflow Permissions

Current GitHub Actions permissions:

```yaml
permissions:
  contents: read
```

No elevated repository permissions are required for the current workflow.

## Reporting And Debugging

Currently implemented:

* pytest-html
* HTML report generation
* automatic screenshot capture on test failure
* `reports/` runtime output directory
* GitHub Actions artifact upload
* downloadable CI artifacts
* separate reports and artifacts for Smoke, Regression, and full-suite jobs

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
test-artifacts
```

Artifact upload steps use:

```yaml
if: always()
```

This allows available browser-test reports and runtime outputs to be published even when an executing test command fails.

Current artifact retention:

```text
7 days
```

Installed but not currently integrated into the active reporting workflow:

* allure-pytest

Current reporting status:

* pytest-html is the implemented reporting solution
* screenshots on failure are implemented
* GitHub Actions artifacts are implemented
* Allure reporting is not currently implemented

Advanced Allure reporting belongs to Phase 4D.

## API Testing

Currently installed:

* `requests`

Current status:

* API testing is not implemented
* API tests are not part of the current test suite
* `api` is not a current executable pytest marker

Planned API usage may include:

* API smoke validation
* backend validation
* hybrid UI and API scenarios
* API-based test data setup
* API-based test data cleanup

The presence of `requests` prepares the framework for future API work but does not mean that an API testing layer currently exists.

## Test Execution Optimization

Currently installed:

* pytest-xdist

Current status:

* Pytest-level parallel execution is not part of the default local workflow
* Pytest-level parallel execution is not part of the current CI workflow

The independent Smoke, Regression, and full-suite GitHub Actions jobs may execute concurrently after `quality`, but this does not use `pytest-xdist`.

Parallel Pytest execution belongs to Phase 4C.

Potential future usage may include:

* faster Regression execution
* parallel UI test execution
* CI runtime optimization

Parallel execution should be introduced only after the corresponding Phase 4C implementation and stability validation.

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
* `pytest-html`
* `ruff`
* `black`
* `isort`
* `pre-commit`

Installed for future expansion:

* `requests`
* `allure-pytest`
* `pytest-xdist`

Installed dependencies should not be treated as implemented framework capabilities unless they are actively integrated into the current workflow.

Specifically:

* `pytest-xdist` does not mean parallel execution is implemented
* `allure-pytest` does not mean Allure reporting is implemented
* `requests` does not mean API automation is implemented

Planned dependency-management improvements may include:

* dependency update workflow
* optional dependency grouping if the project grows

## Development Environment

Current local development environment:

* Windows host
* WSL2 with Ubuntu Linux
* Python virtual environment
* PyCharm Community
* Git
* GitHub
* Playwright browser automation

This setup supports Linux-based local execution while remaining aligned with GitHub Actions.

## Current Phase Boundaries

### Phase 4B — CI Execution Strategy

Currently implemented:

* separate CI quality validation
* dedicated Smoke CI execution
* dedicated Regression CI execution
* complete full-suite CI execution
* explicit quality-gate dependencies
* job-specific HTML reports
* job-specific GitHub Actions artifacts

### Phase 4C — Parallel Execution

Not currently implemented.

Planned scope includes Pytest-level parallel execution using `pytest-xdist`.

Current independent GitHub Actions browser jobs should not be described as Phase 4C parallel test execution.

### Phase 4D — Reporting Upgrade

Not currently implemented.

Planned scope includes advanced Allure reporting.

The current reporting solution remains based on:

* pytest-html
* screenshots on failure
* GitHub Actions artifacts

## Planned Integrations

Potential future integrations include:

* Selenium WebDriver comparison
* Docker-based execution
* environment configuration management
* expanded test data utilities
* Jenkins CI integration
* cross-browser execution
* Phase 4D Allure reporting
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
* Chromium execution
* Pytest test execution
* Page Object Model
* shared authenticated-page behavior through `AppPage`
* reusable product and checkout assertions
* reusable fixtures
* centralized test data
* parametrization
* normalized marker-based organization
* Smoke suite execution
* Regression suite execution
* UI suite execution
* Security suite execution
* Sorting suite execution
* Navigation suite execution
* independent E2E checkpoint execution
* selective local marker execution
* local quality checks
* GitHub Actions CI
* dedicated CI quality validation
* dedicated Smoke CI execution
* dedicated Regression CI execution
* complete full-suite CI validation
* pytest-html reporting
* screenshot capture on failure
* job-specific CI artifacts
* technical documentation

Current Phase 4B CI structure:

```text
quality
├── smoke
├── regression
└── full-suite
```

UI, Security, Sorting, Navigation, and E2E remain selectively executable without dedicated CI jobs.

Parallel Pytest execution with `pytest-xdist`, advanced Allure reporting, runtime environment configuration, API testing, and cross-browser execution are not currently implemented.

The `main` branch remains the stable portfolio version of the project.

The `develop` branch and active workstream branches may contain newer validated changes before promotion.

Future stack expansion should remain clearly separated from currently implemented capabilities.
