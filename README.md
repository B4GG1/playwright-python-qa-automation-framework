# Playwright Python QA Automation Framework

## Table of Contents

- [Project Overview](#project-overview)
- [Technology Stack](#technology-stack)
- [Framework and Project Structure](#framework-and-project-structure)
- [Features](#features)
- [Getting Started](#getting-started)
- [Quality Tooling](#quality-tooling)
- [Roadmap](#roadmap)


## Project Overview
This repository contains a scalable QA Automation Framework built primarily with Playwright, Pytest, and Python.
The project serves as both a practical automation engineering playground and a portfolio-oriented framework designed to showcase modern test automation practices, framework architecture, tooling integration, and quality engineering workflows.
The framework focuses mainly on Playwright-based UI automation while also planning to include Selenium-based comparison modules to evaluate different automation approaches, execution models, and framework design patterns.
The repository is being developed with a strong emphasis on:

- maintainable framework architecture, 
- scalable test organization, 
- modern Python tooling, 
- automated quality validation, 
- reproducible development environments, 
- CI/CD readiness, 
- debugging and reporting capabilities.

The long-term goal of the project is to evolve into a production-style automation framework demonstrating both practical QA automation skills and software engineering best practices.

### System Under Test (SUT)

The framework is built and validated against the following application:

- **Application:** Sauce Demo  
- **URL:** https://www.saucedemo.com/  

### Rationale

Sauce Demo is used as the primary System Under Test (SUT) because it is a stable, publicly available web application designed specifically for UI automation practice and testing education purposes.
It provides a realistic e-commerce user flow, including authentication and basic shopping cart functionality, which makes it suitable for demonstrating end-to-end test automation scenarios.
Key reasons for choosing this SUT:

- Stable and reliable test environment with minimal UI changes  
- Covers essential e-commerce workflows (login, product browsing, cart operations)  
- Ideal for UI automation practice with Playwright and Selenium  
- Does not require external setup, accounts, or backend configuration  
- Enables repeatable and deterministic test execution  
- Suitable for both beginner and advanced automation scenarios  

This SUT serves as the foundational application for validating framework stability, test design patterns, and future scalability of the automation architecture.

## Technology Stack

### Core Technologies

* Python 3.12
* Pytest
* Playwright
* Requests
* pytest-playwright
* WSL2 (Ubuntu Linux)
* Git
* GitHub

### Code Quality & Development Tooling

* Ruff (linting)
* Black (formatting)
* isort (imports)
* pre-commit hooks

### Reporting & Debugging

* pytest-html
* allure-pytest
* Automatic screenshot capture on test failure

### Planned Integrations & Future Extensions

* Selenium WebDriver comparison module
* Page Object Model (POM) architecture
* API testing layer expansion
* Advanced Allure reporting
* GitHub Actions CI/CD pipelines
* Docker-based execution environments
* Parallel test execution improvements
* Environment configuration management
* Test data management utilities
* Cross-browser execution support
* Jenkins CI integration

## Framework and Project Structure

The framework is structured to support scalable UI automation, API testing, reporting, and future CI/CD integration while maintaining readability and modularity.

```text
playwright-python-qa-automation-framework/
│
├── config/                 # Framework and environment configuration
├── docs/                   # Project documentation
├── framework/              # Shared framework utilities and core infrastructure
├── pages/                  # Page Object Model components
├── reports/                # Test reports, screenshots, and execution artifacts
├── resources/              # Static resources and supporting files
├── test_data/              # Externalized test datasets and test inputs
├── tests/                  # Automated test suites
│
├── conftest.py             # Shared pytest fixtures and hooks
├── pytest.ini              # Centralized pytest configuration
├── pyproject.toml          # Ruff, Black, and isort configuration
├── requirements.txt        # Project dependencies
├── requirements-lock.txt   # Locked dependency versions
├── .pre-commit-config.yaml # Automated quality hooks configuration
└── README.md               # Project documentation and portfolio overview
```
### Architecture Goals

- Maintainable and scalable project structure
- Clear separation of framework layers
- Reusable automation components
- Centralized test configuration
- CI/CD-ready development workflow
- Readable and consistent test organization

## Features

### Currently Implemented

- UI test automation using Playwright
- Pytest-based test execution
- Smoke test execution support
- Centralized pytest configuration
- Automatic screenshot capture on test failure
- Virtual environment isolation using venv
- Static code analysis with Ruff
- Automated code formatting using Black
- Import standardization with isort
- Automated quality gates using pre-commit hooks
- Linux-based development workflow using WSL2
- GitHub-based portfolio repository structure

### Planned Features

- Selenium-based comparison module
- Page Object Model (POM) architecture
- API automation testing layer
- Allure reporting integration
- HTML reporting improvements
- Parallel test execution optimization
- Environment-based configuration management
- Test data management utilities
- CI/CD pipelines with GitHub Actions
- Dockerized test execution
- Cross-browser execution support
- Jenkins pipeline integration
- Advanced logging and debugging utilities

## Getting Started

### Dependency Management
Project dependencies are managed using requirements.txt and isolated Python virtual environments (.venv).
All packages should be installed inside the project virtual environment.

### Prerequisites

Before setting up the framework, ensure the following tools are installed:

* Python 3.12+
* Git
* WSL2 with Ubuntu Linux
* PyCharm Professional / Community Edition
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

```bash
pip install -r requirements.txt
```

### 4. Install Playwright Browsers

```bash
playwright install chromium
```

### 5. Run Tests

Execute all tests:

```bash
pytest -v
```

Run smoke tests only:

```bash
pytest -k smoke -v
```

### 6. Run Quality Checks

```bash
ruff check .
black --check .
isort .
pre-commit run --all-files
```

## Quality Tooling

The framework includes automated quality tooling to maintain consistent code standards, improve readability, and support scalable development workflows.

### Static Analysis

#### Ruff

Used for fast Python linting and static code analysis.

```bash
ruff check .
```

---

### Code Formatting

#### Black

Used to enforce consistent Python code formatting.

```bash
black .
```

#### isort

Used to standardize and organize Python imports.

```bash
isort .
```

---

### Automated Quality Gates

#### pre-commit

Pre-commit hooks automatically validate code quality before commits are created.

Configured hooks currently include:

* Ruff
* Black
* isort

Run all hooks manually:

```bash
pre-commit run --all-files
```

Install hooks locally:

```bash
pre-commit install
```

---

### Quality Goals

* Consistent code formatting
* Readable and maintainable codebase
* Automated local validation
* Reduced formatting conflicts
* Standardized development workflow


## Roadmap

This section outlines the planned evolution of the QA Automation Framework. The goal is to continuously transform this repository into a production-grade automation solution demonstrating modern QA engineering practices.

### Short-Term Goals

- Implement Page Object Model (POM) architecture
- Expand UI test coverage for critical user flows
- Add structured API testing layer
- Improve test data management strategy
- Enhance logging and debugging capabilities

---

### Mid-Term Goals

- Integrate Allure reporting with rich test reporting dashboards
- Introduce parallel test execution optimization (pytest-xdist tuning)
- Implement environment-based configuration management
- Add Dockerized execution environment for reproducibility
- Extend Selenium-based comparison module alongside Playwright

---

### Long-Term Goals

- CI/CD integration with GitHub Actions
- Jenkins pipeline support for enterprise workflows
- Cross-browser execution strategy (Chrome, Firefox, WebKit)
- Advanced test analytics and reporting layer
- Test execution visualization dashboard
- Framework packaging as reusable automation template

---

### Strategic Vision

The long-term objective is to evolve this repository into a scalable, production-ready QA automation framework that demonstrates:

- strong software engineering principles,
- maintainable test architecture,
- modern tooling and CI/CD practices,
- cross-tool automation expertise (Playwright + Selenium),
- readiness for enterprise-level QA environments.