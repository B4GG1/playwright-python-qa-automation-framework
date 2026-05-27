# CI/CD Pipeline (GitHub Actions)

## Overview

This project uses GitHub Actions as the main Continuous Integration (CI) pipeline.
The pipeline automatically validates code quality, installs project dependencies, runs automated tests, generates test reports, and publishes test artifacts after each workflow execution.
At the current stage, the project focuses on CI. Continuous Delivery / Deployment (CD) is not implemented yet and may be added later if the project requires deployment or publishing automation.

## CI Trigger Strategy

The pipeline is executed automatically on:

- `push` to the `main` branch
- `push` to the `develop` branch
- `pull_request` targeting the `main` branch
- `pull_request` targeting the `develop` branch
- manual execution via `workflow_dispatch`

This ensures that:

- stable branches are continuously validated
- pull requests are checked before merge
- manual debugging runs are possible when needed
- both `develop` and `main` remain protected by automated checks

## Execution Environment

Each pipeline run is executed on a fresh GitHub-hosted runner.

Current execution environment:

- Ubuntu latest
- Python 3.12
- isolated runtime environment
- Playwright Chromium browser installed during pipeline execution

The runner is temporary and is destroyed after the workflow finishes.

## Pipeline Stages

The CI pipeline consists of the following stages.

### 1. Repository Checkout

The repository source code is downloaded into the GitHub Actions runner using:

- `actions/checkout`

### 2. Python Setup

Python runtime is installed using:

- `actions/setup-python`

Current Python version:

- Python 3.12

### 3. Dependency Installation

Project dependencies are installed from:

- `requirements.txt`

The pipeline also upgrades `pip` before installing project dependencies.

### 4. Playwright Browser Installation

Playwright browser dependencies are installed during the CI run.

Currently installed browser:

- Chromium

This ensures that UI tests can run in a clean Linux-based CI environment.

### 5. Code Quality Checks

The pipeline validates code quality using:

- Ruff for linting
- Black for formatting validation
- isort for import sorting validation

These checks ensure that code formatting and import organization remain consistent across the project.

### 6. Test Execution

Automated tests are executed using Pytest.

The test command generates:

- console output
- HTML test report
- screenshots on failure, if configured
- files inside the `reports/` directory

Current report location:

- `reports/report.html`

## Test Reports And Artifacts

The pipeline uploads test execution outputs as GitHub Actions artifacts.

Current artifacts include:

- pytest HTML report
- contents of the `reports/` directory
- screenshots from failed tests, if generated

Artifacts are available for download from the workflow run page in GitHub Actions.

## Artifact Retention

Artifacts are stored temporarily by GitHub Actions.

They are used for:

- debugging failed tests
- reviewing test execution evidence
- validating CI output
- sharing reports without committing generated files to the repository

Generated reports and screenshots should not be committed to Git.

## Quality Gate Expectation

The CI pipeline should act as a quality gate.

Expected behavior:

- linting failure should fail the pipeline
- formatting failure should fail the pipeline
- import sorting failure should fail the pipeline
- test failure should fail the pipeline
- artifacts should still be uploaded for debugging when failures occur

Artifact upload steps should use `if: always()` so reports are preserved even when tests fail.

## Branch Protection Strategy

The CI pipeline supports the repository branching strategy.

Recommended branch protection rules:

### `main`

- require pull request before merge
- require CI pipeline to pass
- disallow direct pushes
- disallow force pushes

### `develop`

- require pull request before merge
- require CI pipeline to pass
- disallow direct pushes where practical

For a solo portfolio project, full enforcement can be introduced gradually.

## Benefits Of Current CI Setup

The current CI setup provides:

- automated validation on repository changes
- consistent execution environment
- early detection of linting and formatting issues
- automated test execution
- downloadable reports and artifacts
- foundation for future CI/CD improvements

## Future Improvements

Planned CI improvements include:

- installing dependencies from a locked requirements file
- dependency caching for faster pipeline execution
- Playwright browser caching
- JUnit XML test result publishing
- Allure reporting integration
- parallel test execution
- multi-browser execution
- Docker-based execution environment
- advanced test analytics and history tracking