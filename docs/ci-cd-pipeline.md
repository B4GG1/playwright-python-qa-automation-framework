# CI/CD Pipeline (GitHub Actions)

## Overview

This project uses GitHub Actions as the main Continuous Integration (CI) pipeline.

The pipeline automatically validates code quality, installs project dependencies, prepares the Playwright browser environment, runs automated tests, generates test reports, and publishes test artifacts after each workflow execution.

At the current stage, the project focuses on CI. Continuous Delivery / Deployment (CD) is not implemented yet and may be added later if the project requires deployment, package publishing, or environment-based execution.

## Current CI Scope

The current CI pipeline supports:

* Python 3.12 setup
* dependency installation
* Playwright Chromium browser installation
* Ruff linting
* Black formatting validation
* isort import validation
* Pytest test execution
* pytest HTML report generation
* screenshot artifact upload on failure
* reports directory upload as CI artifact
* validation for both `main` and `develop` workflows

The pipeline is designed to act as a quality gate before changes are merged into stable branches.

## CI Trigger Strategy

The pipeline is executed automatically on:

* `push` to the `main` branch
* `push` to the `develop` branch
* `pull_request` targeting the `main` branch
* `pull_request` targeting the `develop` branch
* manual execution via `workflow_dispatch`

This ensures that:

* stable branches are continuously validated
* pull requests are checked before merge
* login, inventory, and future feature workstreams are validated before integration
* manual debugging runs are possible when needed
* both `develop` and `main` can be protected by automated checks

## Execution Environment

Each pipeline run is executed on a fresh GitHub-hosted runner.

Current execution environment:

* Ubuntu latest
* Python 3.12
* isolated runtime environment
* Playwright Chromium browser installed during pipeline execution

The runner is temporary and is destroyed after the workflow finishes. This helps ensure that test results are reproducible and not dependent on local machine state.

## Pipeline Stages

The CI pipeline consists of the following stages.

### 1. Repository Checkout

The repository source code is downloaded into the GitHub Actions runner using:

* `actions/checkout`

This gives the runner access to the project files, tests, configuration, and documentation.

### 2. Python Setup

Python runtime is installed using:

* `actions/setup-python`

Current Python version:

* Python 3.12

This keeps CI aligned with the local development environment.

### 3. Dependency Installation

Project dependencies are installed from the locked dependency file:

* `requirements-lock.txt`

The pipeline also upgrades `pip` before installing project dependencies.

Using a locked dependency file improves repeatability because CI installs exact dependency versions instead of resolving the latest compatible versions on every run.

### 4. Playwright Browser Installation

Playwright browser dependencies are installed during the CI run.

Currently installed browser:

* Chromium

This ensures that UI tests can run in a clean Linux-based CI environment.

Future framework expansion may include Firefox and WebKit execution.

### 5. Code Quality Checks

The pipeline validates code quality using:

* Ruff for linting
* Black for formatting validation
* isort for import sorting validation

Current quality commands:

```bash
ruff check .
black --check .
isort . --check-only
```

These checks ensure that code formatting, linting rules, and import organization remain consistent across the project.

### 6. Test Execution

Automated tests are executed using Pytest.

Current test command generates:

* console output
* HTML test report
* screenshots on failure, if configured
* files inside the `reports/` directory

Current report location:

```text
reports/report.html
```

The test suite currently includes:

* smoke validation
* positive login scenarios
* negative login scenarios
* login UI behavior checks
* protected route access validation
* inventory page validation
* product list and product card validation
* product details navigation validation
* product sorting validation

### 7. Artifact Upload

The pipeline uploads test execution outputs as GitHub Actions artifacts.

Current artifacts include:

* pytest HTML report
* contents of the `reports/` directory
* screenshots from failed tests, if generated

Artifact upload steps should use:

```yaml
if: always()
```

This ensures that reports and screenshots are still uploaded even when tests fail.

## Test Reports And Artifacts

Generated reports and screenshots should not be committed to Git.

They are runtime outputs and should be handled through:

* local `reports/` directory
* GitHub Actions artifacts
* future reporting integrations such as Allure

Current artifact examples:

* `pytest-html-report`
* `test-artifacts`

Artifacts are available for download from the workflow run page in GitHub Actions.

## Artifact Retention

Artifacts are stored temporarily by GitHub Actions.

They are used for:

* debugging failed tests
* reviewing test execution evidence
* validating CI output
* sharing reports without committing generated files to the repository

The project may configure artifact retention explicitly, for example:

```yaml
retention-days: 7
```

This keeps artifacts available long enough for debugging while avoiding unnecessary long-term storage.

## Quality Gate Expectation

The CI pipeline acts as a quality gate.

Expected behavior:

* linting failure should fail the pipeline
* formatting failure should fail the pipeline
* import sorting failure should fail the pipeline
* test failure should fail the pipeline
* artifacts should still be uploaded for debugging when failures occur

Test execution should not use:

```yaml
continue-on-error: true
```

for the main test suite, because failing tests should block the pipeline.

## Marker-Based Test Execution

The framework supports pytest markers for selective test execution.

Current marker categories include:

* `smoke`
* `regression`
* `ui`
* `api`
* `e2e`
* `positive`
* `negative`
* `sorting`

Useful local validation commands:

```bash
pytest -m smoke -v
pytest -m regression -v
pytest -m positive -v
pytest -m negative -v
pytest -m sorting -v
pytest -m "ui and smoke" -v
pytest -m "ui and regression" -v
pytest -m "ui and sorting" -v
```

The main CI pipeline currently executes the full test suite.

Future CI improvements may include separate jobs for smoke, regression, API, sorting, and cross-browser test execution.

## Branch Protection Strategy

The CI pipeline supports the repository branching strategy.

Recommended branch protection rules:

### `main`

* require pull request before merge
* require CI pipeline to pass
* disallow direct pushes
* disallow force pushes
* keep as stable portfolio/release branch

### `develop`

* require pull request before merge
* require CI pipeline to pass
* disallow direct pushes where practical
* use as the main integration branch for completed workstreams

For a solo portfolio project, full enforcement can be introduced gradually. However, the preferred workflow is:

```text
feature branch → Pull Request → CI validation → Squash merge → develop
```

## Workflow Security Notes

GitHub Actions workflow files should be treated as sensitive project configuration.

Recommended practices:

* review all changes to `.github/workflows/*.yml`
* avoid unknown shell scripts in workflow steps
* avoid suspicious commands such as `curl | bash`, `wget | bash`, `eval`, or encoded shell payloads
* do not add secrets unless required
* avoid unnecessary workflow permissions
* use minimal `GITHUB_TOKEN` permissions where possible

Recommended minimal workflow permission for the current CI scope:

```yaml
permissions:
  contents: read
```

The project currently does not require deployment credentials, cloud credentials, or publish tokens.

## Benefits Of Current CI Setup

The current CI setup provides:

* automated validation on repository changes
* consistent execution environment
* early detection of linting and formatting issues
* automated UI test execution
* confidence before merging feature workstreams
* downloadable reports and artifacts
* support for professional Pull Request workflow
* foundation for future CI/CD improvements

## Current CI Status

The CI pipeline is operational and supports the completed Login Page Automation Workstream and the Inventory And Products Automation Workstream.

The pipeline validates:

* project setup
* code quality
* test execution
* generated reports
* CI artifacts

It is ready to support future framework expansion into cart, checkout, API testing, and reporting improvements.

## Future Improvements

Planned CI improvements include:

* dependency caching for faster pipeline execution
* Playwright browser caching
* JUnit XML test result publishing
* Allure reporting integration
* separate smoke and regression jobs
* parallel test execution
* multi-browser execution
* Docker-based execution environment
* scheduled regression runs
* advanced test analytics and history tracking
* optional deployment or publishing pipeline if the project scope requires it
