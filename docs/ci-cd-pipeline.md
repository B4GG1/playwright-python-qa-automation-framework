# CI/CD Pipeline (GitHub Actions)

## Overview

This project uses GitHub Actions as the main Continuous Integration (CI) pipeline.

The current pipeline preserves the Phase 4B job structure separating code-quality validation from browser-test execution and extends the browser-test jobs with the Phase 4C Pytest parallel execution strategy.

The workflow provides dedicated CI jobs for:

* code-quality validation
* parallel Smoke suite execution
* parallel Regression suite execution
* parallel complete full-suite execution

The workflow installs project dependencies, validates code quality, prepares Playwright Chromium where browser execution is required, runs the appropriate Pytest suites through `pytest-xdist`, generates HTML reports, and publishes test artifacts.

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
* `pytest-xdist` worker-level parallel execution in browser-test jobs
* automatic xdist worker selection through `-n auto`
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

The workflow can also be executed manually through:

* `workflow_dispatch`

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

The `quality` job also does not use pytest-xdist.

GitHub-hosted runners are temporary and are destroyed after execution.

This helps ensure that CI results do not depend on local developer machine state.

## Current Job Structure

The job structure introduced in Phase 4B is preserved:

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

GitHub Actions may schedule these independent browser jobs concurrently when runners are available.

Phase 4C additionally enables worker-level parallel test execution inside each browser-test job.

These are two separate concurrency mechanisms:

* **GitHub Actions job-level concurrency** — Smoke, Regression, and full-suite may execute as separate jobs at the same time
* **Pytest worker-level parallelism** — pytest-xdist distributes collected tests between workers inside an individual browser-test job

The resulting execution model is:

```text
quality
├── smoke
│   └── pytest-xdist workers
├── regression
│   └── pytest-xdist workers
└── full-suite
    └── pytest-xdist workers
```

The `quality` job remains outside the browser and xdist execution layer.

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

The locked dependencies include `pytest-xdist`, which is used later by the browser-test jobs.

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
* execute Pytest through xdist
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
5. executes the Smoke suite through pytest-xdist
6. generates a self-contained HTML report
7. uploads Smoke-specific artifacts

The parallel marker selection command is:

```bash
pytest -m smoke -n auto -v
```

The current CI command also generates the HTML report:

```bash
mkdir -p reports
pytest -m smoke -n auto -v --html=reports/smoke-report.html --self-contained-html
```

Current Smoke HTML report:

```text
reports/smoke-report.html
```

`-n auto` lets pytest-xdist select the worker count based on the available runner environment.

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
5. executes the Regression suite through pytest-xdist
6. generates a self-contained HTML report
7. uploads Regression-specific artifacts

The parallel marker selection command is:

```bash
pytest -m regression -n auto -v
```

The current CI command also generates the HTML report:

```bash
mkdir -p reports
pytest -m regression -n auto -v --html=reports/regression-report.html --self-contained-html
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
5. executes the complete Pytest suite through pytest-xdist
6. generates a self-contained HTML report
7. uploads full-suite artifacts

The full-suite execution is intentionally not filtered by Pytest markers.

The parallel core command is:

```bash
pytest -n auto -v
```

The current CI command is:

```bash
mkdir -p reports
pytest -n auto -v --html=reports/report.html --self-contained-html
```

Current full-suite HTML report:

```text
reports/report.html
```

The full-suite job validates the complete automated test collection regardless of Smoke, Regression, or other marker assignment.

Dedicated Smoke and Regression jobs provide additional suite-specific CI feedback, but they do not replace the full-suite gate.

A failed full-suite test fails the `full-suite` job and the overall CI workflow.

## Pytest-xdist Execution

`pytest-xdist` is an implemented project capability.

The current CI browser jobs use:

```text
-n auto
```

to enable worker-level parallel execution.

Current CI parallel commands:

```bash
pytest -m smoke -n auto -v
pytest -m regression -n auto -v
pytest -n auto -v
```

The same execution model was validated locally before CI integration.

Sequential local execution remains supported and is not removed by the Phase 4C implementation.

Examples:

```bash
pytest -m smoke -v
pytest -m regression -v
pytest -v
```

Parallel execution therefore extends the supported execution strategy rather than replacing sequential Pytest execution.

### Test Isolation Expectations

Worker-level parallel execution requires tests to remain independent.

The validated suite follows these expectations:

* tests do not depend on execution order
* tests do not depend on application state created by another test
* Playwright browser state is isolated through the existing fixture model
* Cart and Checkout scenarios prepare their own required state
* parametrized scenarios remain independently executable
* E2E checkpoints remain independently executable
* no shared stateful purchase journey is distributed across test functions

No sequential-only test exceptions were identified during Phase 4C parallel-safety validation.

## GitHub Actions Concurrency Versus Pytest Parallelism

GitHub Actions concurrency and pytest-xdist parallelism operate at different levels.

### GitHub Actions Job-Level Concurrency

After `quality` succeeds, GitHub Actions may independently schedule:

```text
smoke
regression
full-suite
```

Each is a separate GitHub Actions job running in its own runner environment.

This behavior was established as part of the Phase 4B CI architecture.

### Pytest Worker-Level Parallelism

Inside each browser-test job, pytest-xdist distributes collected tests between worker processes.

For example:

```text
smoke job
└── pytest -m smoke -n auto -v
    ├── worker
    ├── worker
    └── ...
```

The number of workers selected by `-n auto` depends on the execution environment and should not be treated as a fixed CI configuration value.

Phase 4C therefore does not replace GitHub Actions job concurrency.

It adds a second execution layer inside the existing browser-test jobs.

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

Parallel execution does not introduce:

* Firefox CI execution
* WebKit CI execution
* cross-browser matrices
* browser-specific parallel jobs

The current parallel CI scope remains Chromium-only.

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

The existing CI structure provides dedicated browser jobs for:

* `smoke`
* `regression`

Phase 4C preserves those jobs and enables xdist inside them.

Current commands:

```bash
pytest -m smoke -n auto -v
pytest -m regression -n auto -v
```

### Markers Without Dedicated CI Jobs

The following executable markers do not currently have dedicated GitHub Actions jobs:

* `ui`
* `security`
* `sorting`
* `navigation`
* `e2e`

They remain available for selective local execution and for scoped validation during implementation or investigation.

Example sequential commands:

```bash
pytest -m ui -v
pytest -m security -v
pytest -m sorting -v
pytest -m navigation -v
pytest -m e2e -v
```

These tests are still included in the complete full-suite CI execution when they form part of the normal collected test suite.

Because the full-suite CI job uses pytest-xdist, those tests may execute on xdist workers as part of the complete collection.

Not having a dedicated marker job does not mean that the tests are excluded from CI.

It means only that CI does not currently execute them as separate marker-filtered jobs.

### Local Marker Execution

All approved executable markers remain available locally.

Sequential execution:

```bash
pytest -m smoke -v
pytest -m regression -v
pytest -m ui -v
pytest -m security -v
pytest -m sorting -v
pytest -m navigation -v
pytest -m e2e -v
```

Approved Phase 4C parallel commands:

```bash
pytest -m smoke -n auto -v
pytest -m regression -n auto -v
pytest -n auto -v
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

This independence allows E2E tests to participate safely in parallel full-suite execution.

## Local And CI Execution Responsibilities

Local execution and CI execution serve related but different purposes.

### Local Execution

Local execution supports both sequential and parallel Pytest modes.

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

Sequential execution remains useful for normal development and focused debugging.

Parallel execution is useful for validating worker-safe behavior and reducing suite execution time, where appropriate.

Approved parallel validation commands:

```bash
pytest -m smoke -n auto -v
pytest -m regression -n auto -v
pytest -n auto -v
```

### CI Execution

Current CI provides:

* mandatory code-quality validation
* dedicated parallel Smoke execution
* dedicated parallel Regression execution
* parallel complete unfiltered full-suite execution
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

The existing reporting and artifact structure was preserved when pytest-xdist was enabled.

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

The Phase 4C CI validation confirmed that the expected report and artifact outputs remain available with pytest-xdist enabled.

## Failure Screenshots And Parallel Execution

Failure screenshots are generated through the existing Pytest failure hook.

Screenshot output is stored under:

```text
reports/screenshots/
```

Screenshot filenames include:

* the test name
* a UTC timestamp

The screenshot mechanism and shared report directory were reviewed during Phase 4C parallel-safety validation.

The parallel validation did not identify a filename collision or another worker-safety issue requiring a framework change.

The current implementation therefore keeps the existing screenshot and report structure unchanged.

No new reporting architecture was introduced as part of Phase 4C.

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

Parallel execution does not change the existing retention strategy.

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

pytest-xdist does not change this failure policy.

A failing worker-level test still causes the corresponding Pytest command and browser-test job to fail.

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

## Phase 4B And Phase 4C Execution Strategy

The current CI combines two completed framework maturity layers.

### Phase 4B — CI Execution Structure

Phase 4B established:

* separation of code-quality validation from browser execution
* dedicated Smoke CI execution
* dedicated Regression CI execution
* preserved complete full-suite execution
* explicit job dependencies through the quality gate
* suite-specific reports and artifacts

The Phase 4B structure remains:

```text
quality
├── smoke
├── regression
└── full-suite
```

### Phase 4C — Parallel Execution

Phase 4C introduced and validated Pytest worker-level parallel execution using `pytest-xdist`.

Implemented Phase 4C CI behavior includes:

* parallel Smoke execution
* parallel Regression execution
* parallel complete full-suite execution
* `-n auto` worker selection
* xdist integration into the existing browser-test jobs
* preservation of the `quality` prerequisite
* preservation of existing HTML reports
* preservation of existing artifact names
* preservation of seven-day artifact retention
* preservation of Chromium-only browser execution

Phase 4C does not introduce new GitHub Actions jobs.

The current browser commands are:

```bash
pytest -m smoke -n auto -v
pytest -m regression -n auto -v
pytest -n auto -v
```

The independent Smoke, Regression, and full-suite GitHub Actions jobs may still execute concurrently after `quality`.

That remains GitHub Actions job-level concurrency.

pytest-xdist worker execution happens independently inside each browser-test job.

### Phase 4D — Reporting Upgrade

Advanced Allure reporting is not currently implemented.

Allure belongs to the planned Phase 4D reporting upgrade.

The current reporting implementation uses:

* `pytest-html`
* failure screenshots where generated
* GitHub Actions artifacts

The presence of `allure-pytest` in project dependencies must not be treated as evidence that Allure reporting is currently part of the active local or CI workflow.

## Current CI Status

The current CI pipeline is operational with the Phase 4B structure and Phase 4C parallel execution strategy.

It currently validates:

* project dependency setup
* Ruff
* Black
* isort
* dedicated parallel Smoke execution
* dedicated parallel Regression execution
* parallel complete automated Pytest execution
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
│   └── pytest-xdist
├── regression
│   └── pytest-xdist
└── full-suite
    └── pytest-xdist
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

Phase 4C does not implement:

* advanced Allure reporting
* runtime environment configuration
* multi-browser execution
* Docker execution
* CI matrices
* additional marker-specific jobs

These remain outside the current implemented CI scope.

## Future Improvements

Future CI and framework maturity work may include capabilities approved in later project phases, such as:

* Phase 4D Allure reporting
* improved reporting and diagnostics
* runtime environment configuration
* dependency or browser caching where justified
* JUnit XML publishing where useful
* multi-browser execution
* Docker-based execution
* scheduled execution
* improved test analytics and history tracking

Pytest-xdist parallel execution is already implemented and should not be described as future functionality.

Future capabilities should not be described as implemented until their corresponding project scope is completed and validated.
