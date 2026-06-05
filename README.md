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
Phase 2 completed — Login Page Automation Workstream
```

The project currently includes a complete login page automation workstream covering:

* manual login test cases
* LoginPage Page Object Model
* reusable login page fixture
* centralized login test data
* positive login scenarios
* negative login scenarios
* UI validation scenarios
* protected route access validation
* pytest parametrization
* pytest markers
* GitHub Actions CI validation
* HTML reporting and CI artifacts

The next planned phase will expand automation coverage into:

* inventory / products page
* cart functionality
* checkout flow
* multi-page user journeys

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

Current automated coverage focuses on login page and authentication-related behavior.

Implemented test cases:

| Test Case ID | Scenario                                                 | Test Area        |
| ------------ | -------------------------------------------------------- | ---------------- |
| TC-LOGIN-001 | Successful login with valid credentials                  | Positive / Smoke |
| TC-LOGIN-002 | Login with invalid username                              | Negative         |
| TC-LOGIN-003 | Login with invalid password                              | Negative         |
| TC-LOGIN-004 | Login with empty username                                | Negative         |
| TC-LOGIN-005 | Login with empty password                                | Negative         |
| TC-LOGIN-006 | Login with empty credentials                             | Negative         |
| TC-LOGIN-007 | Locked out user login attempt                            | Negative         |
| TC-LOGIN-008 | Login with invalid username and invalid password         | Negative         |
| TC-LOGIN-009 | Error message can be closed after failed login           | UI               |
| TC-LOGIN-010 | Login page elements are visible                          | UI / Smoke       |
| TC-LOGIN-011 | Password field masks entered characters                  | UI / Regression  |
| TC-LOGIN-012 | Login form can be submitted with Enter key               | Positive / UI    |
| TC-LOGIN-013 | Direct access to inventory page without login is blocked | Access Control   |

Detailed manual test cases are documented in:

```text
test_cases/login-page.md
```

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

Run UI smoke tests:

```bash
pytest -m "ui and smoke" -v
```

Run UI regression tests:

```bash
pytest -m "ui and regression" -v
```

Run a selected test file:

```bash
pytest tests/test_login_positive.py -v
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

## Roadmap

Current roadmap direction:

* **Phase 1:** Foundation — completed
* **Phase 2:** Login Page Automation Workstream — completed
* **Phase 2 Checkpoint:** Documentation review and Phase 3 preparation — current
* **Phase 3:** Products, Cart, and Checkout Coverage — planned
* **Phase 4:** Framework Maturity — planned
* **Phase 5:** Advanced Extensions — future

Future planned areas include:

* inventory and product page validation
* cart functionality tests
* checkout flow automation
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
* Runtime outputs such as reports and screenshots are ignored by Git and handled through local output or CI artifacts.
