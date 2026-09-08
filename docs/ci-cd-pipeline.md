# CI/CD Pipeline (GitHub Actions)

## Overview

This project uses GitHub Actions as the main Continuous Integration (CI) pipeline.

The current Phase 4B pipeline separates code-quality validation from browser-test execution and provides dedicated CI jobs for:

* code-quality validation
* Smoke suite execution
* Regression suite execution
* complete full-suite execution

The workflow installs project dependencies, validates code quality, prepares Playwright Chromium where browser execution is required, runs the appropriate Pytest suites, generates HTML reports, and publishes test artifacts.

At the current stage, the project focuses on CI.

Continuous Delivery / Deployment is not implemented and should not be treated as part of the current project capabilities.

## Current CI Scope

The current CI pipeline supports:

* Python 3.12 setup
* dependency installation from `requirements-lock.txt`
* dedicated Ruff, Black, and isort quality validation
* dedicated Smoke browser-test execution
* dedicated Regression browser-test execution
* complete unfiltered Pytest full-suite execution
* Playwright Chromium installation with Linux dependencies for browser-test jobs
* pytest HTML report generation
* screenshot artifact collection through the `reports/` directory
* job-specific GitHub Actions artifacts
* explicit artifact retention configuration
* validation for `main` and `develop`
* validation for Pull Requests targeting `main` and `develop`
* manual workflow execution through GitHub Actions

The pipeline acts as a quality gate before changes are merged into stable branches.

The `main` branch represents the stable portfolio version of the project.

The `develop` branch remains the integration branch and may contain newer validated work before it is promoted to `main`.

## CI Trigger Strategy

The pipeline is executed automatically on:

* `push` to `main`
* `push` to `develop`
* `pull_request` targeting `main`
* `pull_request` targeting `develop`
* manual execution through `workflow_dispatch`

Regular pushes to feature, refactor, fix, or documentation branches do not automatically execute CI unless:

* a Pull Request targeting `main` or `develop` is opened
* the workflow is started manually through `workflow_dispatch`

This trigger strategy ensures that:

* integration and stable branches are continuously validated
* Pull Requests are checked before merge
* completed workstreams can be validated before integration
* portfolio promotion from `develop` to `main` is validated
* manual validation and debugging runs remain available

## Workflow Permissions

The current workflow uses minimal GitHub token permissions:

```yaml
permissions:
  contents: read
```

This is sufficient because the workflow only needs to:

* read repository contents
* install dependencies
* execute quality checks
* run automated tests
* upload artifacts

The project currently does not require:

* deployment credentials
* cloud credentials
* package publishing tokens
* elevated repository permissions

## Execution Environment

Each CI job executes on a fresh GitHub-hosted runner.

Current execution environment:

* `ubuntu-latest`
* Python 3.12
* isolated runtime environment
* dependencies installed from `requirements-lock.txt`

Browser-test jobs additionally install Chromium and its required Linux dependencies through Playwright.

The `quality` job does not install Chromium because it performs static code-quality validation only.

GitHub-hosted runners are temporary and are destroyed after execution.

This helps ensure that CI results do not depend on local developer machine state.

## Current Job Structure

The Phase 4B pipeline contains four jobs:

```text
quality
├── smoke
├── regression
└── full-suite
```

The dependency model is intentional.

The `quality` job executes first.

After `quality` succeeds:

* `smoke`
* `regression`
* `full-suite`

become independently executable jobs.

The browser jobs do not depend on each other.

A Smoke failure does not prevent Regression or full-suite from executing after they have been released by the successful quality gate.

Similarly, Regression and full-suite do not define execution dependencies between each other.

GitHub Actions may schedule these independent jobs concurrently when runners are available.

This job-level concurrency is not the same as parallel Pytest execution.

Parallel test execution with `pytest-xdist` belongs to Phase 4C and is not part of the current Phase 4B implementation.

## Quality Job

The `quality` job is the first CI gate.

Its responsibility is to validate repository code quality before browser resources are prepared.

The job performs:

### Repository Checkout

```yaml
actions/checkout@v4
```

### Python Setup

```yaml
actions/setup-python@v5
```

Current Python version:

```text
3.12
```

### Dependency Installation

The workflow upgrades `pip` and installs project dependencies from:

```text
requirements-lock.txt
```

Current installation commands:

```bash
python -m pip install --upgrade pip
pip install -r requirements-lock.txt
```

### Ruff Validation

```bash
ruff check .
```

### Black Validation

```bash
black --check .
```

### isort Validation

```bash
isort . --check-only
```

The quality job does not:

* install Playwright Chromium
* execute browser tests
* generate browser-test HTML reports
* upload browser-test artifacts

A failure in Ruff, Black, isort, dependency installation, or another required quality-job step fails the job.

Because all browser jobs declare:

```yaml
needs: quality
```

a failed quality job prevents Smoke, Regression, and full-suite execution.

This avoids unnecessary browser setup and test execution when the repository does not pass the initial code-quality gate.

## Smoke Job

The `smoke` job provides dedicated CI execution of the approved Smoke marker suite.

It depends on:

```yaml
needs: quality
```

After the quality job succeeds, the Smoke job:

1. checks out the repository
2. configures Python 3.12
3. installs dependencies
4. installs Playwright Chromium
5. executes the Smoke suite
6. generates a self-contained HTML report
7. uploads Smoke-specific artifacts

The marker selection command is:

```bash
pytest -m smoke -v
```

The current CI command also generates the HTML report:

```bash
mkdir -p reports
pytest -m smoke -v --html=reports/smoke-report.html --self-contained-html
```

Current Smoke HTML report:

```text
reports/smoke-report.html
```

A failing Smoke test fails the `smoke` job and therefore contributes to an unsuccessful CI workflow result.

The job does not use `continue-on-error: true`.

## Regression Job

The `regression` job provides dedicated CI execution of the approved Regression marker suite.

It depends on:

```yaml
needs: quality
```

After the quality job succeeds, the Regression job:

1. checks out the repository
2. configures Python 3.12
3. installs dependencies
4. installs Playwright Chromium
5. executes the Regression suite
6. generates a self-contained HTML report
7. uploads Regression-specific artifacts

The marker selection command is:

```bash
pytest -m regression -v
```

The current CI command also generates the HTML report:

```bash
mkdir -p reports
pytest -m regression -v --html=reports/regression-report.html --self-contained-html
```

Current Regression HTML report:

```text
reports/regression-report.html
```

A failing Regression test fails the `regression` job and therefore contributes to an unsuccessful CI workflow result.

The job does not use `continue-on-error: true`.

## Full-Suite Job

The `full-suite` job remains the complete CI regression gate.

It depends on:

```yaml
needs: quality
```

After the quality job succeeds, the full-suite job:

1. checks out the repository
2. configures Python 3.12
3. installs dependencies
4. installs Playwright Chromium
5. executes the complete Pytest suite
6. generates a self-contained HTML report
7. uploads full-suite artifacts

The full-suite execution is intentionally not filtered by Pytest markers.

The core command is:

```bash
pytest -v
```

The current CI command is:

```bash
mkdir -p reports
pytest -v --html=reports/report.html --self-contained-html
```

Current full-suite HTML report:

```text
reports/report.html
```

The full-suite job validates the complete automated test collection regardless of Smoke, Regression, or other marker assignment.

Dedicated Smoke and Regression jobs provide additional suite-specific CI feedback, but they do not replace the full-suite gate.

A failed full-suite test fails the `full-suite` job and the overall CI workflow.

## Playwright Browser Installation

Chromium is installed only in jobs that execute browser tests:

* `smoke`
* `regression`
* `full-suite`

The installation command is:

```bash
playwright install --with-deps chromium
```

The `quality` job intentionally does not install Chromium.

Current CI browser:

* Chromium

Cross-browser CI execution is not currently implemented.

## Pytest Marker Strategy And CI

The framework uses explicit Pytest markers to provide selectively executable test suites.

Current executable markers are:

* `smoke`
* `regression`
* `ui`
* `security`
* `sorting`
* `navigation`
* `e2e`

Detailed marker semantics and assignment rules are documented in [Testing Strategy](testing-strategy.md).

### Marker Suites Executed As Dedicated CI Jobs

Phase 4B currently provides dedicated CI jobs for:

* `smoke`
* `regression`

These suites are executed automatically whenever their CI jobs are released after successful quality validation.

### Markers Without Dedicated CI Jobs

The following executable markers do not currently have dedicated GitHub Actions jobs:

* `ui`
* `security`
* `sorting`
* `navigation`
* `e2e`

They remain available for selective local execution and for scoped validation during implementation or investigation.

Example commands:

```bash
pytest -m ui -v
pytest -m security -v
pytest -m sorting -v
pytest -m navigation -v
pytest -m e2e -v
```

These tests are still included in the complete full-suite CI execution when they form part of the normal collected test suite.

Not having a dedicated marker job does not mean that the tests are excluded from CI.

It means only that CI does not currently execute them as separate marker-filtered jobs.

### Local Marker Execution

All approved executable markers remain available locally:

```bash
pytest -m smoke -v
pytest -m regression -v
pytest -m ui -v
pytest -m security -v
pytest -m sorting -v
pytest -m navigation -v
pytest -m e2e -v
```

Markers may also be combined.

Examples:

```bash
pytest -m "smoke and ui" -v
pytest -m "regression and ui" -v
pytest -m "smoke and navigation" -v
pytest -m "regression and navigation" -v
```

Marker execution may also be scoped to a specific test module.

Example:

```bash
pytest tests/test_checkout_page.py -m e2e -v
```

The `e2e` suite consists of independent checkpoints that collectively represent the primary purchase journey.

Individual E2E tests remain:

* independently executable
* fixture-driven
* order-independent
* isolated from state produced by other tests

## Local And CI Execution Responsibilities

Local execution and CI execution serve related but different purposes.

### Local Execution

Selective local execution is useful for:

* fast feedback during implementation
* validating a changed behavior category
* running the representative Smoke suite
* running broader Regression coverage
* validating UI behavior
* checking Security or Sorting behavior
* validating Navigation-related changes
* validating the logical E2E checkpoint suite
* running focused module-level validation before the full suite

### CI Execution

Current Phase 4B CI provides:

* mandatory code-quality validation
* dedicated Smoke execution
* dedicated Regression execution
* complete unfiltered full-suite execution
* clean-environment browser execution
* generated HTML reports
* downloadable runtime artifacts
* merge-gate feedback

The full-suite job remains the complete automated regression gate.

Smoke and Regression provide additional targeted feedback without replacing complete suite execution.

## Test Reports And Artifacts

Generated reports and screenshots are runtime outputs and should not be committed to Git.

They are handled through:

* the local `reports/` directory
* GitHub Actions artifacts

Each browser job uses report and artifact names that do not conflict with the other jobs.

### Smoke Artifacts

Smoke HTML report:

```text
reports/smoke-report.html
```

GitHub Actions artifact names:

```text
smoke-pytest-html-report
smoke-test-artifacts
```

### Regression Artifacts

Regression HTML report:

```text
reports/regression-report.html
```

GitHub Actions artifact names:

```text
regression-pytest-html-report
regression-test-artifacts
```

### Full-Suite Artifacts

Full-suite HTML report:

```text
reports/report.html
```

GitHub Actions artifact names:

```text
pytest-html-report
test-artifacts
```

Browser-job artifact upload steps use:

```yaml
if: always()
```

This allows available reports and runtime outputs to be uploaded even when a test command fails within an executing browser job.

If the `quality` job fails, the browser jobs do not start, so they do not produce browser-test artifacts for that workflow execution.

## Artifact Retention

Current GitHub Actions artifacts are retained for:

```yaml
retention-days: 7
```

Temporary retention keeps execution and debugging evidence available without treating generated runtime output as permanent repository content.

Artifacts can be used for:

* failure investigation
* execution evidence
* debugging
* Pull Request review

## Quality Gate Behavior

The CI pipeline acts as a merge quality gate.

Current expected failure behavior:

* Ruff failure fails `quality`
* Black validation failure fails `quality`
* isort validation failure fails `quality`
* failed `quality` prevents all browser jobs from starting
* Smoke test failure fails `smoke`
* Regression test failure fails `regression`
* full-suite test failure fails `full-suite`
* browser-test failures are not converted into successful results
* available browser-job reports and artifacts are uploaded through `if: always()`

The workflow does not use:

```yaml
continue-on-error: true
```

for the required quality or browser-test execution commands.

A failed required validation should therefore prevent the workflow from being treated as successful.

## Branch Protection Strategy

The CI pipeline supports the repository branching strategy.

Recommended protection for `main`:

* require Pull Request before merge
* require CI to pass
* disallow direct pushes
* disallow force pushes
* preserve `main` as the stable portfolio branch

Recommended protection for `develop`:

* require Pull Request before merge
* require CI to pass
* disallow direct pushes where practical
* preserve `develop` as the normal integration branch

Preferred integration flow:

```text
feature / fix / docs / refactor branch
        ↓
Pull Request
        ↓
CI validation
        ↓
Squash merge
        ↓
develop
```

Portfolio promotion flow:

```text
develop
  ↓
Pull Request
  ↓
CI validation
  ↓
Squash merge
  ↓
main
```

## Workflow Security Notes

GitHub Actions workflow files should be treated as sensitive project configuration.

Recommended practices:

* review every change to `.github/workflows/*.yml`
* avoid unknown shell scripts
* avoid suspicious commands such as `curl | bash`, `wget | bash`, `eval`, or encoded payload execution
* do not add secrets unless required
* avoid unnecessary workflow permissions
* use minimal `GITHUB_TOKEN` permissions

Current permission configuration:

```yaml
permissions:
  contents: read
```

No elevated GitHub token permission is currently required.

## Phase 4B And Future CI Maturity

The current documented implementation represents Phase 4B CI Execution Strategy.

Phase 4B includes:

* separation of code-quality validation from browser execution
* dedicated Smoke CI execution
* dedicated Regression CI execution
* preserved complete full-suite execution
* explicit job dependencies through the quality gate
* suite-specific reports and artifacts

### Phase 4C — Parallel Execution

Parallel Pytest execution is not currently implemented.

Phase 4C is intended to introduce and validate parallel execution using `pytest-xdist`.

The current Phase 4B workflow must therefore not be described as using:

* `pytest-xdist`
* `pytest -n`
* parallel test workers

The independent Smoke, Regression, and full-suite GitHub Actions jobs may execute concurrently after `quality`, but this is CI job scheduling rather than Pytest-level parallelization.

### Phase 4D — Reporting Upgrade

Advanced Allure reporting is not currently implemented.

Allure belongs to the planned Phase 4D reporting upgrade.

The current reporting implementation uses:

* `pytest-html`
* failure screenshots where generated
* GitHub Actions artifacts

The presence of `allure-pytest` in project dependencies must not be treated as evidence that Allure reporting is currently part of the active local or CI workflow.

## Current CI Status

The Phase 4B CI pipeline is operational.

It currently validates:

* project dependency setup
* Ruff
* Black
* isort
* dedicated Smoke execution
* dedicated Regression execution
* complete automated Pytest execution
* Playwright Chromium setup for browser jobs
* HTML report generation
* job-specific test artifacts
* Pull Requests targeting `develop`
* Pull Requests targeting `main`
* pushes to `develop`
* pushes to `main`
* manual workflow executions

Current execution structure:

```text
quality
├── smoke
├── regression
└── full-suite
```

The quality job is the prerequisite gate.

Smoke, Regression, and full-suite are independent browser-test jobs after successful quality validation.

The full-suite job remains the complete unfiltered CI regression gate.

Dedicated CI jobs are not currently implemented for:

* UI
* Security
* Sorting
* Navigation
* E2E

Parallel Pytest execution, advanced Allure reporting, runtime environment configuration, multi-browser execution, and other later framework maturity capabilities are not part of the current Phase 4B implementation.

## Future Improvements

Future CI and framework maturity work may include capabilities approved in later project phases, such as:

* Phase 4C parallel Pytest execution
* Phase 4D Allure reporting
* improved reporting and diagnostics
* runtime environment configuration
* dependency or browser caching where justified
* JUnit XML publishing where useful
* multi-browser execution
* Docker-based execution
* scheduled execution
* improved test analytics and history tracking

These capabilities should not be described as implemented until their corresponding project scope is completed and validated.
