# Playwright Python QA Automation Framework

## Table of Contents

* [Project Overview](#project-overview)
* [Current Status](#current-status)
* [System Under Test](#system-under-test)
* [Implemented Coverage](#implemented-coverage)
* [Technology Stack](#technology-stack)
* [Getting Started](#getting-started)
* [Running Tests](#running-tests)
* [Quality Checks](#quality-checks)
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
* automated quality validation
* reproducible development environment
* CI-backed Pull Request workflow
* debugging and reporting capabilities
* traceability between manual test cases and automated tests

The long-term goal of the project is to evolve into a production-style automation framework demonstrating both practical QA automation skills and software engineering best practices.

## Current Status

Current project phase:

```
Phase 3 completed — Products, Cart, And Checkout Coverage
```

Latest completed integration:

```
AQA-0083 — Checkout Automation Workstream merged into develop in PR #6
```

Stable portfolio snapshot:

```
Completed Phase 3 state promoted to main as the current portfolio version
```

The `main` branch represents the polished portfolio version of the completed Phase 3 project state. The `develop` branch remains the integration branch and may contain newer work after this README is read from `main`.

The project currently includes completed automation coverage for:

* login page and authentication behavior
* protected route access validation
* protected checkout route access validation
* inventory page visibility and product listing behavior
* product card content validation
* inventory-side product details navigation
* product details page validation
* product sorting scenarios
* cart page navigation
* add-to-cart behavior from inventory and product details pages
* cart badge behavior
* cart product content validation
* remove-from-cart behavior from inventory, product details, and cart pages
* Continue Shopping navigation
* cart state persistence after logout and re-login
* cart-owned checkout step one navigation
* checkout information form validation
* checkout information required field validation
* checkout information error handling
* checkout overview validation
* checkout overview price summary validation
* product details navigation from checkout overview
* checkout finish action
* checkout complete page confirmation validation
* Back Home navigation after order completion

Completed login automation workstream includes:

* manual login test cases
* `LoginPage` Page Object Model
* reusable login page fixture
* centralized login test data
* positive login scenarios
* negative login scenarios
* UI validation scenarios
* protected inventory route access validation
* protected cart route access validation
* protected item details route access validation
* protected checkout information route access validation
* protected checkout overview route access validation
* protected checkout complete route access validation
* input error icon validation after failed login
* pytest parametrization
* pytest markers
* GitHub Actions CI validation
* HTML reporting and CI artifacts

Completed inventory automation workstream includes:

* manual inventory test cases
* `InventoryPage` Page Object Model
* centralized product test data
* inventory page visibility validation
* product list validation
* product card content validation
* product details navigation from inventory product names
* product details navigation from inventory product images
* product sorting validation
* inventory-side add-to-cart and remove-from-cart validation
* cart badge validation from inventory actions
* regression and smoke coverage for inventory behavior

Completed product details automation coverage includes:

* manual product details test cases
* `ProductDetailsPage` Page Object Model
* product details content validation
* return navigation to inventory page
* product-details-side add-to-cart validation
* product-details-side remove-from-cart validation
* cart badge validation from product details actions
* cart navigation from product details page
* all-products product details coverage using centralized product data

Completed cart automation workstream includes:

* manual cart test cases
* `CartPage` Page Object Model
* cart page availability validation
* empty cart state validation
* added product visibility validation
* cart product content validation
* remove-from-cart validation
* cart badge decrement and removal validation
* Continue Shopping navigation validation
* Continue Shopping cart state preservation
* product details navigation from cart item name
* checkout information page navigation from the cart page with product in cart
* cart state persistence validation after logout and re-login
* all-products cart visibility and remove-from-cart coverage

Completed checkout automation workstream includes:

* manual checkout test cases
* checkout Page Objects
* centralized checkout test data
* reusable checkout setup fixtures
* checkout information form visibility validation
* checkout required customer field validation
* checkout information error message validation
* checkout information input error icon validation
* checkout information error close behavior
* checkout information form submission with valid data
* checkout information cancel navigation back to cart
* checkout overview selected product validation
* checkout overview all-products validation
* checkout overview price summary validation
* checkout overview cancel navigation back to inventory
* product details navigation from checkout overview item name
* all-products product details navigation from checkout overview
* checkout finish action validation
* checkout complete page confirmation validation
* Back Home navigation after order completion

Completed Phase 3 finalization includes:

* one automated test module per covered page area
* one manual test case file per covered page area
* `BasePage` and `AppPage` structure alignment
* shared authenticated-page behavior ownership through `AppPage`
* reusable product and checkout assertion helpers
* fixture naming and reuse review
* navigation return type review
* test case metadata cleanup
* documentation synchronization
* final local quality validation
* final full pytest validation
* PR review, CI validation, and squash merge into `develop`
* stable Phase 3 portfolio promotion to `main`

The next project direction is Phase 4 Framework Maturity.

## System Under Test

The framework is built and validated against the following application:

* **Application:** Sauce Demo
* **URL:** `https://www.saucedemo.com/`

Sauce Demo is used as the primary System Under Test because it is a stable, publicly available web application designed for UI automation practice and testing education.

It provides realistic e-commerce-style flows, including:

* authentication
* product listing
* cart operations
* checkout process

This makes it suitable for demonstrating end-to-end test automation scenarios and scalable framework design.

## Implemented Coverage

Current automated coverage includes Login, Inventory, Product Details, Cart, and Checkout-related behavior.

Detailed test case definitions are stored in dedicated files under the `test_cases/` directory. The README provides only a high-level coverage overview to keep the project entry point readable and maintainable.

| Workstream                      | Status    | Covered Areas                                                                                                                                                 | Test Case Documentation                                               |
| ------------------------------- | --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| Login Page Automation           | Completed | positive login, negative login, UI validation, protected route access, protected checkout route access, input error icons                                     | [Login Page Test Cases](test_cases/login-page.md)                     |
| Inventory Page Automation       | Completed | inventory page visibility, product list validation, product card content, sorting, product details navigation, inventory-side cart actions                    | [Inventory Page Test Cases](test_cases/inventory-page.md)             |
| Product Details Page Automation | Completed | product details content, return navigation, product-details-side cart actions, cart badge behavior, cart navigation                                           | [Product Details Page Test Cases](test_cases/product-details-page.md) |
| Cart Page Automation            | Completed | empty cart, added product visibility, cart content, remove from cart, cart badge behavior, Continue Shopping, cart persistence, checkout entry navigation     | [Cart Page Test Cases](test_cases/cart-page.md)                       |
| Checkout Flow Automation        | Completed | checkout information form, required field validation, checkout overview, price summary validation, product details navigation from overview, order completion | [Checkout Page Test Cases](test_cases/checkout-page.md)               |

Current automated test areas:

* login and authentication tests
* protected route access tests
* protected checkout route access tests
* inventory page tests
* product details tests
* product sorting tests
* cart page tests
* cart badge tests
* cart item content tests
* cart persistence tests
* checkout information form tests
* checkout overview tests
* checkout price summary tests
* checkout completion tests
* shared page-level behavior validation through reusable Page Objects

Future automated test areas:

* broader multipage user journey tests
* API-level tests
* cross-browser UI tests
* additional approved edge-case or known-defect coverage

## Technology Stack

Core technologies:

* Python 3.12
* Pytest
* Playwright
* pytest-playwright
* Git
* GitHub
* GitHub Actions
* WSL2 with Ubuntu Linux

Code quality tools:

* Ruff
* Black
* isort
* pre-commit

Reporting and debugging:

* pytest-html
* screenshots on test failure
* GitHub Actions artifacts

CI/CD:

* GitHub Actions

Installed for future expansion:

* requests
* allure-pytest
* pytest-xdist

The currently implemented framework focuses on Playwright-based UI automation. API testing, advanced Allure reporting, parallel execution with pytest-xdist, Docker-based execution, Jenkins integration, Selenium comparison, and cross-browser execution are planned future extensions and are not part of the implemented framework scope yet.

## Getting Started

### Prerequisites

Before setting up the framework, ensure the following tools are installed:

* Python 3.12+
* Git
* WSL2 with Ubuntu Linux or another compatible Linux environment
* IDE or editor of choice
* Playwright-supported browser dependencies

### 1. Clone Repository

```
git clone git@github.com:B4GG1/playwright-python-qa-automation-framework.git
cd playwright-python-qa-automation-framework
```

### 2. Create Virtual Environment

```
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Project Dependencies

Recommended installation from locked dependency versions:

```
pip install -r requirements-lock.txt
```

Alternative installation from main dependency list:

```
pip install -r requirements.txt
```

### 4. Install Playwright Browser

For local Linux or WSL2 setup:

```
playwright install --with-deps chromium
```

If system dependencies are already installed, Chromium-only installation is also sufficient:

```
playwright install chromium
```

## Running Tests

Run all tests:

```
pytest -v
```

Run smoke tests:

```
pytest -m smoke -v
```

Run regression tests:

```
pytest -m regression -v
```

Run positive tests:

```
pytest -m positive -v
```

Run negative tests:

```
pytest -m negative -v
```

Run sorting tests:

```
pytest -m sorting -v
```

Run navigation tests:

```
pytest -m navigation -v
```

Run end-to-end tests:

```
pytest -m e2e -v
```

Run UI smoke tests:

```
pytest -m "ui and smoke" -v
```

Run UI regression tests:

```
pytest -m "ui and regression" -v
```

Run UI sorting tests:

```
pytest -m "ui and sorting" -v
```

Run UI navigation tests:

```
pytest -m "ui and navigation" -v
```

Run login tests:

```
pytest tests/test_login_page.py -v
```

Run inventory tests:

```
pytest tests/test_inventory_page.py -v
```

Run product details tests:

```
pytest tests/test_product_details_page.py -v
```

Run cart tests:

```
pytest tests/test_cart_page.py -v
```

Run checkout tests:

```
pytest tests/test_checkout_page.py -v
```

For Phase 3 completed coverage validation, run:

```
pytest -v tests/test_login_page.py
pytest -v tests/test_inventory_page.py
pytest -v tests/test_product_details_page.py
pytest -v tests/test_cart_page.py
pytest -v tests/test_checkout_page.py
pytest -v
```

## Quality Checks

Run Ruff linting:

```
ruff check .
```

Check formatting with Black:

```
black --check .
```

Check import sorting with isort:

```
isort . --check-only
```

Run all main local validation checks:

```
ruff check .
black --check .
isort . --check-only
pytest -v
```

If formatting changes are needed:

```
black .
isort .
```

Run pre-commit hooks manually:

```
pre-commit run --all-files
```

Install pre-commit hooks:

```
pre-commit install
```

## Reports And Artifacts

The framework generates runtime test outputs such as:

* pytest console output
* pytest HTML report
* screenshots on test failure
* GitHub Actions artifacts

Local report output is stored under:

```
reports/
```

Generated reports, screenshots, cache files, and runtime artifacts should not be committed to Git.

In CI, reports and screenshots are uploaded as GitHub Actions artifacts and can be downloaded from the workflow run page.

## Documentation

All extended project documentation is stored in the `docs/` directory to keep the README focused on high-level information.

### Core Documentation

* [Architecture](docs/architecture.md)
  Overview of the framework architecture, layers, and design direction.

* [Framework And Project Structure](docs/framework-and-project-structure.md)
  Explanation of folder structure, responsibilities, and repository organization.

* [Technology Stack](docs/technology-stack.md)
  Overview of implemented and planned technologies.

### Engineering Workflow

* [Git Branching Strategy](docs/git-branching-strategy.md)
  Branching model, merge strategy, and repository workflow standards.

* [Workflow](docs/workflow.md)
  Day-to-day development workflow for working with branches, commits, pull requests, and CI.

* [CI/CD Pipeline](docs/ci-cd-pipeline.md)
  GitHub Actions workflow, pipeline stages, reports, and artifacts.

* [Quality Tooling](docs/quality-tooling.md)
  Ruff, Black, isort, pre-commit, Pytest, and local/CI quality gates.

### Testing And Planning

* [Testing Strategy](docs/testing-strategy.md)
  Test types, test design principles, automation strategy, and validation workflow.

* [Features Overview](docs/features.md)
  Implemented and planned framework capabilities.

* [Roadmap](docs/roadmap.md)
  Development phases and long-term project direction.

### Test Case Documentation

* [Login Page Test Cases](test_cases/login-page.md)
  Manual login test cases mapped to automated test coverage.

* [Inventory Page Test Cases](test_cases/inventory-page.md)
  Manual inventory test cases mapped to automated test coverage.

* [Product Details Page Test Cases](test_cases/product-details-page.md)
  Manual product details test cases mapped to automated test coverage.

* [Cart Page Test Cases](test_cases/cart-page.md)
  Manual cart test cases mapped to automated test coverage.

* [Checkout Page Test Cases](test_cases/checkout-page.md)
  Manual checkout test cases mapped to automated test coverage.

## Roadmap

Current roadmap direction:

* **Phase 1:** Foundation — completed
* **Phase 2:** Login Page Automation Workstream — completed
* **Phase 2 Checkpoint:** Documentation review and Phase 3 preparation — completed
* **Phase 3A:** Inventory And Products Automation Workstream — completed
* **Phase 3B:** Cart Automation Workstream — completed
* **Phase 3C:** Structure Cleanup, Coverage Completion, And Documentation Sync — completed
* **Phase 3D:** Checkout Automation Workstream — completed and merged into `develop`
* **Phase 3 Completion Review:** covered by AQA-0082 and AQA-0083
* **Phase 3 Portfolio Promotion:** completed Phase 3 state promoted to `main`
* **Phase 4:** Framework Maturity — planned
* **Phase 5:** Advanced Extensions — future

Future planned areas include:

* broader multipage user journey tests
* API-level tests
* Allure reporting
* cross-browser execution
* Docker-based execution environment
* Selenium comparison module
* Jenkins pipeline integration
* CI optimization
* framework maturity improvements

## Navigation Notes

* Clickable links point directly to Markdown files in the repository.
* GitHub automatically renders `.md` files with preview.
* Extended documentation is version-controlled alongside the framework.
* Detailed manual test cases are stored outside the README to keep the main project overview concise.
* Runtime outputs such as reports and screenshots are ignored by Git and handled through local output or CI artifacts.
