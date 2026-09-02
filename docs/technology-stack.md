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

```
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

```
docs/testing-strategy.md
```

### Current Browser Execution

Current implemented browser execution:

* Chromium

Planned browser execution:

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

```
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

```
test_data/login_test_data.py
test_data/product_test_data.py
test_data/checkout_test_data.py
```

Planned test data expansion:

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

Tool configuration is stored in:

```
pyproject.toml
.pre-commit-config.yaml
pytest.ini
```

Standard local quality validation:

```
ruff check .
black --check .
isort . --check-only
pytest -v
```

## Test Execution Strategy

### Full Test Suite

Run the complete automated suite:

```
pytest -v
```

### Marker-Based Local Execution

Current marker suites can be executed locally with:

```
pytest -m smoke -v
pytest -m regression -v
pytest -m ui -v
pytest -m security -v
pytest -m sorting -v
pytest -m navigation -v
pytest -m e2e -v
```

Useful combined selections include:

```
pytest -m "smoke and ui" -v
pytest -m "regression and ui" -v
pytest -m "smoke and navigation" -v
pytest -m "regression and navigation" -v
```

Marker expressions may also be scoped to a test module.

Example:

```
pytest tests/test_checkout_page.py -m e2e -v
```

Marker-based execution is primarily used for selective local validation.

## E2E Execution Model

The current `e2e` suite represents independent checkpoints that collectively form the primary purchase journey.

The logical journey includes:

```
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

```
pytest -m e2e -v
```

## CI/CD And Automation

Current CI technology:

* GitHub Actions

Current CI responsibilities:

* repository checkout
* Python 3.12 setup
* dependency installation
* Playwright Chromium installation
* Ruff validation
* Black validation
* isort validation
* full Pytest execution
* HTML report generation
* artifact upload

Current CI targets:

* pushes to `main`
* pushes to `develop`
* Pull Requests targeting `main`
* Pull Requests targeting `develop`
* manual execution through `workflow_dispatch`

The current GitHub Actions pipeline executes the complete automated suite.

It does not currently execute separate marker-based jobs.

Marker-based commands are primarily part of local selective validation.

Planned CI/CD improvements may include:

* dependency caching
* Playwright browser caching
* JUnit XML reporting
* separate Smoke execution
* separate Regression execution
* selected marker-based jobs
* parallel execution
* multi-browser execution
* Docker-based execution
* improved reporting publication

These improvements should not be described as implemented until the corresponding workflow changes are completed and validated.

## Reporting And Debugging

Currently implemented:

* pytest-html
* HTML report generation
* automatic screenshot capture on test failure
* `reports/` runtime output directory
* GitHub Actions artifact upload
* downloadable CI artifacts

Installed but not fully integrated:

* allure-pytest

Current reporting status:

* pytest-html is the implemented reporting solution
* screenshots on failure are implemented
* GitHub Actions artifacts are implemented
* Allure reporting remains a future extension

Planned reporting improvements may include:

* advanced Allure reporting
* improved screenshot organization
* structured logs
* JUnit XML output
* execution history
* test analytics
* richer failure diagnostics

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

* parallel test execution is not part of the default local workflow
* parallel test execution is not part of the current CI workflow

Planned usage may include:

* faster Regression execution
* parallel UI test execution
* CI runtime optimization

Parallel execution should be introduced only after corresponding implementation and stability validation.

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

## Planned Integrations

Potential future integrations include:

* Selenium WebDriver comparison
* Docker-based execution
* environment configuration management
* expanded test data utilities
* Jenkins CI integration
* cross-browser execution
* Allure reporting
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
* local quality checks
* GitHub Actions CI
* full-suite CI validation
* HTML reporting
* screenshot capture on failure
* CI artifacts
* technical documentation

The `main` branch remains the stable portfolio version of the project.

The `develop` branch and active workstream branches may contain newer validated changes before promotion.

Future stack expansion should remain clearly separated from currently implemented capabilities.
