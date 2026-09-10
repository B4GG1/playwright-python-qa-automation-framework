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
* pytest fixtures
* pytest parametrization
* marker-based test execution
* representative Smoke and broader Regression coverage
* independent end-to-end journey checkpoints
* pytest-xdist worker-level parallel execution
* automated quality validation
* dedicated Smoke and Regression CI execution
* complete full-suite CI validation
* parallel browser-test execution inside Pytest CI processes
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
* **URL:** `https://www.saucedemo.com/`

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
| ------------------------------- | --------- | --------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------- |
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

The automated suite has also been validated with `pytest-xdist` worker-level parallel execution.

Parallel execution preserves the same test-independence expectations:

* tests do not depend on execution order
* tests do not depend on state produced by another test
* Playwright browser state is isolated through the existing test fixture model
* parametrized scenarios remain independently executable
* E2E checkpoints remain independently executable
* Cart and Checkout scenarios prepare their own required state

No sequential-only test exceptions were identified during Phase 4C parallel-safety validation.

Sequential execution remains supported.

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

Detailed marker definitions, assignment rules, parallel execution behavior, and examples are documented in:

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

### Reporting And Debugging

* pytest-html
* screenshots on test failure
* GitHub Actions artifacts

### CI

* GitHub Actions
* dedicated quality validation
* parallel Smoke suite execution
* parallel Regression suite execution
* parallel complete full-suite execution

### Installed For Future Expansion

* requests
* allure-pytest

The currently implemented framework focuses on Playwright-based UI automation.

Pytest parallel execution with `pytest-xdist` is implemented locally and in the existing CI browser-test jobs.

API testing, advanced Allure reporting, Docker-based execution, Jenkins integration, Selenium comparison, and cross-browser execution remain future extensions and are not part of the current implemented framework scope.

## Getting Started

### Prerequisites

Before setting up the framework, ensure the following tools are installed:

* Python 3.12+
* Git
* WSL2 with Ubuntu Linux or another compatible Linux environment
* IDE or editor of choice
* Playwright-supported browser dependencies

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

## Running Tests

Run the complete automated test suite sequentially:

```bash
pytest -v
```

Sequential execution remains fully supported.

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

Parallel execution does not change marker semantics, test ownership, or test independence requirements.

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

The current GitHub Actions pipeline combines the Phase 4B CI job structure with the Phase 4C Pytest parallel execution strategy.

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

It does not install Playwright Chromium and does not use `pytest-xdist`.

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

The actual CI command also generates its existing self-contained HTML report:

```bash
pytest -m smoke -n auto -v --html=reports/smoke-report.html --self-contained-html
```

Regression executes:

```bash
pytest -m regression -n auto -v
```

The actual CI command also generates its existing self-contained HTML report:

```bash
pytest -m regression -n auto -v --html=reports/regression-report.html --self-contained-html
```

The full-suite job executes the complete unfiltered suite:

```bash
pytest -n auto -v
```

The actual CI command also generates its existing self-contained HTML report:

```bash
pytest -n auto -v --html=reports/report.html --self-contained-html
```

All three browser jobs install Playwright Chromium.

The current CI browser scope remains Chromium-only.

The workflow runs automatically for:

* pushes to `main`
* pushes to `develop`
* Pull Requests targeting `main`
* Pull Requests targeting `develop`

It can also be started manually through `workflow_dispatch`.

Parallel Pytest execution does not introduce additional CI jobs, matrices, browsers, marker suites, or runtime configuration.

Advanced Allure reporting is not part of the current CI workflow.

Detailed CI job behavior, dependencies, xdist execution, commands, artifacts, and failure handling are documented in:

* [CI/CD Pipeline](docs/ci-cd-pipeline.md)

## Reports And Artifacts

The framework generates runtime outputs such as:

* pytest console output
* pytest HTML reports
* screenshots on test failure
* GitHub Actions artifacts

Local report output is stored under:

```text
reports/
```

Failure screenshots are stored under:

```text
reports/screenshots/
```

Generated reports, screenshots, cache files, and runtime artifacts should not be committed to Git.

The current report and failure-artifact behavior was validated with worker-level parallel execution.

No sequential-only reporting exception was identified during Phase 4C validation.

The current CI browser jobs generate self-contained pytest HTML reports and upload available report outputs as GitHub Actions artifacts.

Current Smoke artifacts:

* `smoke-pytest-html-report`
* `smoke-test-artifacts`

Current Regression artifacts:

* `regression-pytest-html-report`
* `regression-test-artifacts`

Current full-suite artifacts:

* `pytest-html-report`
* `test-artifacts`

Artifact uploads use separate names between jobs to avoid conflicts.

Available browser-job reports and artifacts are uploaded with `if: always()` even when test execution fails.

The introduction of xdist does not change the existing report paths, artifact names, upload behavior, or seven-day retention policy.

Artifacts are retained temporarily for debugging and execution review.

Detailed artifact paths, retention, parallel execution behavior, and CI handling are documented in:

* [CI/CD Pipeline](docs/ci-cd-pipeline.md)

## Documentation

Extended project documentation is stored in the `docs/` directory so that the README can remain a high-level entry point.

### Core Documentation

* [Architecture](docs/architecture.md)
  Overview of framework architecture, layers, execution isolation, and design direction.

* [Framework And Project Structure](docs/framework-and-project-structure.md)
  Explanation of folder structure, responsibilities, repository organization, and parallel-execution considerations.

* [Technology Stack](docs/technology-stack.md)
  Overview of implemented and planned technologies.

### Engineering Workflow

* [Git Branching Strategy](docs/git-branching-strategy.md)
  Branching model, merge strategy, and repository workflow standards.

* [Workflow](docs/workflow.md)
  Day-to-day workflow for branches, commits, Pull Requests, local validation, sequential and parallel execution, marker execution, and CI responsibilities.

* [CI/CD Pipeline](docs/ci-cd-pipeline.md)
  Current GitHub Actions quality gate, parallel Smoke and Regression jobs, parallel complete full-suite execution, reports, artifacts, triggers, and CI maturity boundaries.

* [Quality Tooling](docs/quality-tooling.md)
  Ruff, Black, isort, pre-commit, Pytest, pytest-xdist, and local/CI quality gates.

### Testing And Planning

* [Testing Strategy](docs/testing-strategy.md)
  Detailed test design, marker semantics, sequential and parallel suite execution strategy, E2E checkpoint model, fixtures, parametrization, and validation approach.

* [Features Overview](docs/features.md)
  Implemented and planned framework capabilities.

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
* **Phase 4D:** Reporting Upgrade — planned
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

Planned later Phase 4 areas include:

* reporting improvements
* environment-based configuration
* logging and diagnostics
* fixture organization improvements

Advanced Allure reporting is not currently implemented.

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
* Detailed test strategy and parallel execution behavior remain in `docs/testing-strategy.md`.
* Detailed CI behavior remains in `docs/ci-cd-pipeline.md`.
* Detailed manual test cases remain under `test_cases/`.
* Runtime reports and screenshots are ignored by Git and handled as local outputs or CI artifacts.
