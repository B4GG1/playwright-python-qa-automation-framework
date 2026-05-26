# CI/CD Pipeline (GitHub Actions)
## Overview

The project uses GitHub Actions (CI/CD automation system) to automatically validate code quality and execute the full test suite on every change pushed to the repository.

CI/CD (Continuous Integration / Continuous Delivery) ensures that every change is automatically verified in a clean, isolated environment before being merged into the main branch.

## CI Trigger Strategy

The pipeline is executed automatically on:
- ``` push ``` to ``` main ``` branch
- ``` pull_request ``` targeting ``` main ``` branch
- manual execution via ``` workflow_dispatch ```

This ensures:
- all production-like changes are validated 
- pull requests are verified before merge 
- manual debugging runs are possible when needed

## Execution Environment

Each pipeline run is executed on a fresh virtual machine:
- Ubuntu latest 
- Clean environment (no cached dependencies unless explicitly configured)
- Isolated Python runtime

## Pipeline Stages

The CI pipeline consists of the following stages:

1. Repository Checkout
* Uses ``` actions/checkout ```
* Downloads repository source code into runner

2. Python Setup
* Uses ``` actions/setup-python ```
* Installs Python 3.12 runtime environment

3. Dependency Installation
* Installs project dependencies from ```requirements.txt```
* Upgrades ``` pip ``` before installation

4. Browser Installation (Playwright)
* Installs Chromium browser required for UI tests
* Ensures consistent test execution environment

5. Code Quality Checks
Automated static analysis tools:
* __Ruff (linting)__
* __Black (formatting)__
* __isort (import sorting)__
These steps ensure consistent coding standards across the project.

6. Test Execution (Pytest)
* Executes full test suite using ``` pytest ``` 
* Runs UI automation tests (Playwright)
* Uses verbose output for debugging (``` -v ```)

Optional configuration:
* HTML reports generation (``` pytest-html ```)
* Failure screenshots capture

## Test Artifacts (CI Outputs)

The pipeline can generate and store artifacts such as:
* test execution reports (HTML reports)
* screenshots from failed tests 
* logs from test execution

Artifacts are published using __GitHub Actions Artifacts system__ and are available for download directly from the workflow run page.

## Artifact Retention Strategy

* Artifacts are generated only during CI execution 
* Stored temporarily in GitHub Actions storage 
* Used for debugging and test failure analysis 
* Automatically removed after retention period (GitHub default unless configured otherwise)

## Branch Protection Strategy (CI Integration)

CI is designed to support protected branch workflow:
* ```main``` branch is the primary validated branch 
* Changes should enter via Pull Requests 
* CI must pass before merging (recommended future enforcement)

## Benefits of Current CI/CD Setup

* automatic regression validation 
* consistent execution environment 
* early detection of bugs and linting issues 
* reproducible test results 
* improved debugging via artifacts 
* foundation for future CD (deployment automation)

## Future Improvements

Planned CI/CD enhancements:
* Allure reporting integration 
* parallel test execution
* Docker-based test environment 
* test caching for faster builds 
* deployment pipeline (CD stage)
* multi-browser execution (Chromium, Firefox, WebKit)
* test history tracking & analytics