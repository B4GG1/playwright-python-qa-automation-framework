# Playwright Python QA Automation Framework

## Table of Contents

- [Project Overview](#project-overview)
- [Getting Started](#getting-started)
- [Documentation](#documentation)

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
isort . --check-only
pre-commit run --all-files
```

## Documentation

All extended project documentation is stored in the `docs/` directory to keep the README lightweight and focused on high-level information.

### Core Documentation

- [Architecture](docs/architecture.md)  
  Overview of the framework architecture, layers, and design direction.

- [Framework and Project Structure](docs/framework-and-project-structure.md)  
  Explanation of folder structure, responsibilities, and repository organization.

- [Technology Stack](docs/technology-stack.md)  
  Overview of implemented and planned technologies.

### Engineering Workflow

- [Git Branching Strategy](docs/git-branching-strategy.md)  
  Branching model, merge strategy, and repository workflow standards.

- [Workflow](docs/workflow.md)  
  Day-to-day development workflow for working with branches, commits, pull requests, and CI.

- [CI/CD Pipeline](docs/ci-cd-pipeline.md)  
  GitHub Actions workflow, pipeline stages, reports, and artifacts.

- [Quality Tooling](docs/quality-tooling.md)  
  Ruff, Black, isort, and pre-commit configuration.

### Testing & Planning

- [Testing Strategy](docs/testing-strategy.md)  
  Test types, test design principles, and automation approach.

- [Features Overview](docs/features.md)  
  Implemented and planned framework capabilities.

- [Roadmap](docs/roadmap.md)  
  Development phases and long-term project direction.

---

### 📌 Navigation Notes

- Clickable links point directly to Markdown files in the repository
- GitHub automatically renders `.md` files with preview
- This structure simulates "documentation tabs" using repository navigation
- All documentation is version-controlled alongside the framework