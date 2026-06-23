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

The framework currently focuses on Playwright-based UI automation and is being developed with a strong emphasis on:

* maintainable framework architecture
* readable test organization
* Page Object Model
* centralized test data
* pytest fixtures
* pytest parametrization
* marker-based test execution
* automated quality validation
* reproducible development environment
* CI-backed Pull Request workflow
* debugging and reporting capabilities

The long-term goal of the project is to evolve into a production-style automation framework demonstrating both practical QA automation skills and software engineering best practices.

## Current Status

Current project phase:

```text
Phase 3B in final review — Cart Automation Workstream
```

The project currently includes completed or implemented automation coverage for:

* login page and authentication behavior
* protected route access validation
* inventory page visibility and product listing behavior
* product card content validation
* product details navigation
* product sorting scenarios
* cart page navigation
* add-to-cart behavior
* cart badge behavior
* cart product content validation
* remove-from-cart behavior
* continue shopping navigation
* cart state persistence after logout and re-login

Completed login automation workstream includes:

* manual login test cases
* LoginPage Page Object Model
* reusable login page fixture
* centralized login test data
* positive login scenarios
* negative login scenarios
* UI validation scenarios
* protected inventory route access validation
* protected cart route access validation
* protected item details route access validation
* pytest parametrization
* pytest markers
* GitHub Actions CI validation
* HTML reporting and CI artifacts

Completed inventory/products automation workstream includes:

* manual inventory/products test cases
* InventoryPage Page Object Model extensions
* ProductDetailsPage Page Object Model
* centralized inventory/product test data
* inventory page visibility validation
* product list validation
* product card content validation
* product details navigation validation
* product sorting validation
* page-level UI assertions
* regression and smoke coverage for product-related behavior

Implemented cart automation workstream includes:

* manual cart test cases
* CartPage Page Object Model
* cart page availability validation
* empty cart state validation
* add-to-cart validation
* cart badge validation
* cart product visibility validation
* cart product content validation
* remove-from-cart validation
* continue shopping navigation validation
* cart state persistence validation after logout and re-login
* product-details-side Add to cart and Remove button state validation

The next planned workstream will expand automation coverage into:

* checkout information form validation
* checkout error handling
* checkout overview validation
* complete order flow
* order confirmation validation

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

Current automated coverage includes login, authentication, inventory, product, and cart-related behavior.

Detailed test case definitions are stored in dedicated files under the `test_cases/` directory. The README provides only a high-level coverage overview to keep the project entry point readable and maintainable.

| Workstream                        | Status          | Covered Areas                                                                                                                                            | Test Case Documentation                                               |
|-----------------------------------|-----------------|----------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------|
| Login Page Automation             | Completed       | positive login, negative login, UI validation, protected route access                                                                                    | [Login Page Test Cases](test_cases/login-page.md)                     |
| Inventory And Products Automation | Completed       | inventory page visibility, product list validation, product card content, product details navigation, product sorting                                    | [Inventory And Products Test Cases](test_cases/inventory-products.md) |
| Cart Automation                   | In Final Review | cart navigation, empty cart state, add to cart, cart badge validation, cart product content, remove from cart, continue shopping, cart state persistence | [Cart Test Cases](test_cases/cart.md)                                 |
| Checkout Flow Automation          | Planned         | checkout information, checkout overview, order completion, validation scenarios                                                                          | Planned                                                               |

Current automated test areas:

* login and authentication tests
* protected route access tests
* inventory page tests
* product details tests
* product sorting tests
* cart page tests
* cart badge tests
* cart item content tests
* cart persistence tests

Future automated test areas:

* checkout flow tests
* complete purchase flow tests
* broader multipage user journey tests
* API-level tests

## Technology Stack

Core technologies:

* Python 3.12
* Pytest
* Playwright
* pytest-playwright
* Git
* GitHub
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

## Getting Started

### Prerequisites

Before setting up the framework, ensure the following tools are installed:

* Python 3.12+
* Git
* WSL2 with Ubuntu Linux
* PyCharm Community or Professional
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

Alternative installation from main dependency list:

```bash
pip install -r requirements.txt
```

### 4. Install Playwright Browser

For local Linux or WSL2 setup:

```bash
playwright install --with-deps chromium
```

If system dependencies are already installed, Chromium-only installation is also sufficient:

```bash
playwright install chromium
```

## Running Tests

Run all tests:

```bash
pytest -v
```

Run smoke tests:

```bash
pytest -m smoke -v
```

Run regression tests:

```bash
pytest -m regression -v
```

Run positive tests:

```bash
pytest -m positive -v
```

Run negative tests:

```bash
pytest -m negative -v
```

Run sorting tests:

```bash
pytest -m sorting -v
```

Run navigation tests:

```bash
pytest -m navigation -v
```

Run UI smoke tests:

```bash
pytest -m "ui and smoke" -v
```

Run UI regression tests:

```bash
pytest -m "ui and regression" -v
```

Run UI sorting tests:

```bash
pytest -m "ui and sorting" -v
```

Run UI navigation tests:

```bash
pytest -m "ui and navigation" -v
```

Run selected login test files:

```bash
pytest tests/test_smoke_login.py -v
pytest tests/test_login_positive.py -v
pytest tests/test_login_negative.py -v
pytest tests/test_login_ui.py -v
pytest tests/test_login_access_control.py -v
```

Run inventory and product tests:

```bash
pytest tests/test_inventory_page.py -v
```

Run cart tests:

```bash
pytest tests/test_cart_page.py -v
```

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

## Reports And Artifacts

The framework generates runtime test outputs such as:

* pytest console output
* pytest HTML report
* screenshots on test failure
* GitHub Actions artifacts

Local report output is stored under:

```text
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

* [Inventory And Products Test Cases](test_cases/inventory-products.md)
  Manual inventory and product test cases mapped to automated test coverage.

* [Cart Test Cases](test_cases/cart.md)
  Manual cart test cases mapped to automated test coverage.

## Roadmap

Current roadmap direction:

* **Phase 1:** Foundation — completed
* **Phase 2:** Login Page Automation Workstream — completed
* **Phase 2 Checkpoint:** Documentation review and Phase 3 preparation — completed
* **Phase 3A:** Inventory And Products Automation Workstream — completed
* **Phase 3B:** Cart Automation Workstream — in final review
* **Phase 3C:** Checkout Flow Automation Workstream — planned
* **Phase 4:** Framework Maturity — planned
* **Phase 5:** Advanced Extensions — future

Future planned areas include:

* checkout flow automation
* complete purchase flow tests
* broader multipage user journey tests
* API testing layer
* Allure reporting
* cross-browser execution
* Docker-based execution environment
* Selenium comparison module
* Jenkins pipeline integration

## Navigation Notes

* Clickable links point directly to Markdown files in the repository.
* GitHub automatically renders `.md` files with preview.
* Extended documentation is version-controlled alongside the framework.
* Detailed manual test cases are stored outside the README to keep the main project overview concise.
* Runtime outputs such as reports and screenshots are ignored by Git and handled through local output or CI artifacts.
