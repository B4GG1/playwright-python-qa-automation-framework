# CI/CD Pipeline (GitHub Actions)

## Overview

This project uses GitHub Actions as the main Continuous Integration (CI) pipeline.

The current pipeline combines:

* the Phase 4B CI job structure
* the Phase 4C pytest-xdist parallel execution strategy
* the Phase 4D reporting strategy

The workflow provides dedicated CI jobs for:

* code-quality validation
* parallel Smoke suite execution
* parallel Regression suite execution
* parallel complete full-suite execution

The reporting strategy intentionally uses complementary reporting mechanisms:

* pytest-html provides lightweight self-contained HTML reports
* Allure provides advanced reporting for the complete full-suite CI execution
* failure screenshots provide browser evidence for failed test calls
* GitHub Actions artifacts preserve generated reporting and debugging outputs temporarily

Smoke and Regression remain focused on pytest-html reporting.

The complete `full-suite` job additionally collects Allure result data, generates an Allure HTML report, and publishes it as a dedicated GitHub Actions artifact.

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
* pytest-html report generation
* Allure result collection in the `full-suite` job
* Allure HTML report generation in the `full-suite` job
* failure screenshot collection
* Allure failure screenshot attachments
* job-specific GitHub Actions artifacts
* dedicated Allure report artifact publishing
* explicit seven-day artifact retention
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
* generate runtime reports
* upload artifacts

The project currently does not require:

* deployment credentials
* cloud credentials
* package publishing tokens
* report-hosting credentials
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

The `full-suite` job additionally prepares the tooling required for Allure HTML report generation:

* Java 17 through `actions/setup-java@v4`
* Allure CLI through the `allure-commandline` npm package

GitHub-hosted runners are temporary and are destroyed after execution.

Generated reports and browser evidence therefore need to be published as workflow artifacts when they should remain available after the job completes.

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

Phase 4C enables worker-level parallel test execution inside each browser-test job.

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

Phase 4D adds advanced reporting inside the existing `full-suite` job.

It does not introduce another browser job.

Conceptually:

```text
quality
├── smoke
│   └── pytest-xdist
│       └── pytest-html
├── regression
│   └── pytest-xdist
│       └── pytest-html
└── full-suite
    └── pytest-xdist
        ├── pytest-html
        ├── Allure results
        └── Allure HTML report
```

The `quality` job remains outside the browser, xdist, and test-reporting execution layer.

## Quality Job

The `quality` job is the first CI gate.

Its responsibility is to validate repository code quality before browser resources are prepared.

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

Current commands:

```bash
python -m pip install --upgrade pip
pip install -r requirements-lock.txt
```

The locked dependencies include:

* pytest
* pytest-playwright
* pytest-xdist
* pytest-html
* allure-pytest
* the remaining project dependencies

The Allure CLI itself is not provided by the Python requirements file.

It is prepared separately inside the `full-suite` CI job.

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
* generate pytest-html reports
* generate Allure results
* generate Allure HTML reports
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
3. installs project dependencies
4. installs Playwright Chromium
5. executes the Smoke suite through pytest-xdist
6. generates a self-contained pytest-html report
7. uploads Smoke-specific artifacts

The core parallel marker command is:

```bash
pytest -m smoke -n auto -v
```

The actual CI command is:

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

The job does not use:

```yaml
continue-on-error: true
```

Smoke does not collect or generate Allure reporting.

This is intentional.

The dedicated Smoke job remains the lightweight, targeted pytest-html feedback path.

## Regression Job

The `regression` job provides dedicated CI execution of the approved Regression marker suite.

It depends on:

```yaml
needs: quality
```

After the quality job succeeds, the Regression job:

1. checks out the repository
2. configures Python 3.12
3. installs project dependencies
4. installs Playwright Chromium
5. executes the Regression suite through pytest-xdist
6. generates a self-contained pytest-html report
7. uploads Regression-specific artifacts

The core parallel marker command is:

```bash
pytest -m regression -n auto -v
```

The actual CI command is:

```bash
mkdir -p reports
pytest -m regression -n auto -v --html=reports/regression-report.html --self-contained-html
```

Current Regression HTML report:

```text
reports/regression-report.html
```

A failing Regression test fails the `regression` job and therefore contributes to an unsuccessful CI workflow result.

The job does not use:

```yaml
continue-on-error: true
```

Regression does not collect or generate Allure reporting.

This is intentional.

The dedicated Regression job remains focused on broader marker-specific pytest-html feedback.

## Full-Suite Job

The `full-suite` job remains the complete CI regression gate and is the primary CI source for advanced Allure reporting.

It depends on:

```yaml
needs: quality
```

After the quality job succeeds, the full-suite job:

1. checks out the repository
2. configures Python 3.12
3. installs project dependencies
4. configures Java 17 for Allure CLI
5. installs Allure CLI
6. installs Playwright Chromium
7. executes the complete Pytest suite through pytest-xdist
8. generates the existing self-contained pytest-html report
9. collects Allure result data
10. generates the Allure HTML report when usable result data exists
11. uploads the existing pytest-html artifact
12. uploads the dedicated Allure report artifact
13. uploads the broader `reports/` runtime artifact

The full-suite execution is intentionally not filtered by Pytest markers.

### Java Setup

The workflow configures Java through:

```yaml
uses: actions/setup-java@v4
with:
  distribution: temurin
  java-version: "17"
```

Java is required by the Allure command-line report generator.

This setup is limited to the `full-suite` job.

### Allure CLI Installation

The workflow installs the Allure command-line tool with:

```bash
npm install -g allure-commandline
allure --version
```

The CLI is separate from `allure-pytest`.

Their responsibilities are different:

* `allure-pytest` integrates Allure result collection with Pytest
* Allure CLI converts the generated result data into a browsable HTML report

### Full-Suite Test Execution

The current command is:

```bash
mkdir -p reports
pytest -n auto -v \
  --html=reports/report.html \
  --self-contained-html \
  --alluredir=reports/allure-results \
  --clean-alluredir
```

This command performs two report-producing responsibilities during the same Pytest execution:

* pytest-html generates the lightweight HTML report
* allure-pytest writes Allure result data

Current pytest-html output:

```text
reports/report.html
```

Current Allure result location:

```text
reports/allure-results/
```

The `--clean-alluredir` option removes stale result data before the current test execution populates the directory.

### Allure HTML Generation

After Pytest execution, the workflow contains a separate Allure report-generation step.

The generated report location is:

```text
reports/allure-report/
```

The core generation command is:

```bash
allure generate reports/allure-results \
  --clean \
  -o reports/allure-report
```

The generation step uses:

```yaml
if: always()
```

so it can still execute after a failed Pytest step.

The shell logic additionally checks that:

* `reports/allure-results/` exists
* the directory contains usable result files

before running `allure generate`.

Conceptually:

```bash
if Allure result data exists:
    generate reports/allure-report/
else:
    skip generation
```

This avoids treating absence of result data as a report-generation failure.

It also means a failed full-suite test execution can still produce a useful Allure HTML report when Pytest generated usable Allure result data before failing.

A failed test command still fails the `full-suite` job.

Report generation does not convert a failed test suite into a successful test result.

## Pytest-xdist Execution

`pytest-xdist` is an implemented project capability.

The current CI browser jobs use:

```text
-n auto
```

to enable worker-level parallel execution.

Current core CI commands are:

```bash
pytest -m smoke -n auto -v
pytest -m regression -n auto -v
pytest -n auto -v
```

The actual full-suite command additionally enables pytest-html and Allure result collection.

Sequential local execution remains supported.

Examples:

```bash
pytest -m smoke -v
pytest -m regression -v
pytest -v
```

Parallel execution extends the supported execution strategy rather than replacing sequential Pytest execution.

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

### Reporting Compatibility

The reporting implementation is compatible with the existing xdist model.

Supported behavior includes:

* pytest-html under parallel CI execution
* Allure result collection through the parallel full suite
* failure screenshot capture during parallel execution
* Allure attachment of failure screenshots when result collection is active

Sequential execution remains supported as well.

Phase 4D therefore does not introduce a sequential-only reporting requirement.

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

Phase 4C does not replace GitHub Actions job concurrency.

It adds a second execution layer inside the existing browser-test jobs.

Phase 4D does not change either concurrency model.

It adds reporting capabilities to the existing execution structure.

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

The current execution and reporting strategy does not introduce:

* Firefox CI execution
* WebKit CI execution
* cross-browser matrices
* browser-specific parallel jobs

The current CI browser scope remains Chromium-only.

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

Current commands:

```bash
pytest -m smoke -n auto -v
pytest -m regression -n auto -v
```

These jobs retain their existing pytest-html reporting.

They do not generate Allure reports.

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

Because full-suite also collects Allure results, these tests can additionally appear in the advanced full-suite Allure report.

Not having a dedicated marker job does not mean that the tests are excluded from CI.

It means only that CI does not execute them as separate marker-filtered jobs.

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

Approved parallel commands:

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
* generating local Allure reporting when richer execution analysis is useful

Sequential execution remains useful for normal development and focused debugging.

Parallel execution is useful for validating worker-safe behavior and reducing suite execution time where appropriate.

Approved parallel validation commands:

```bash
pytest -m smoke -n auto -v
pytest -m regression -n auto -v
pytest -n auto -v
```

Local Allure results can be collected through either sequential or parallel execution.

Example parallel execution:

```bash
pytest -n auto -v \
  --alluredir=reports/allure-results \
  --clean-alluredir
```

Generate the corresponding local Allure HTML report with:

```bash
allure generate reports/allure-results \
  --clean \
  -o reports/allure-report
```

The Allure CLI must be installed locally and available on `PATH` for HTML generation.

### CI Execution

Current CI provides:

* mandatory code-quality validation
* dedicated parallel Smoke execution
* dedicated parallel Regression execution
* parallel complete unfiltered full-suite execution
* clean-environment browser execution
* pytest-html reporting
* full-suite Allure reporting
* failure screenshots
* downloadable runtime artifacts
* merge-gate feedback

The full-suite job remains the complete automated regression gate.

Smoke and Regression provide additional targeted feedback without replacing complete suite execution.

## Reporting Responsibilities

The current reporting model intentionally separates responsibilities.

### pytest-html

pytest-html provides the lightweight HTML reporting layer.

It is used by:

* Smoke CI
* Regression CI
* full-suite CI

Current report files:

```text
reports/smoke-report.html
reports/regression-report.html
reports/report.html
```

pytest-html remains available even after Allure integration.

Allure does not replace it.

### Allure

Allure provides the richer advanced reporting layer.

Current responsibilities include:

* structured result collection through `allure-pytest`
* local complete-suite reporting
* parallel reporting compatibility
* generated local HTML reports
* complete full-suite CI reporting
* failure screenshot attachments

Current output locations:

```text
reports/allure-results/
reports/allure-report/
```

Allure is not currently generated independently in the dedicated Smoke and Regression jobs.

### Failure Screenshots

Failure screenshots provide browser evidence for failed test calls.

Current output location:

```text
reports/screenshots/
```

The screenshot is captured through the existing Pytest failure hook.

When screenshot capture succeeds and Allure result collection is active, the same PNG file is attached to the Allure result as:

```text
Failure screenshot
```

The Allure integration does not capture a second screenshot.

The existing screenshot file is reused.

### GitHub Actions Artifacts

GitHub Actions artifacts preserve generated reports and runtime evidence after the temporary runner is destroyed.

Artifacts are temporary execution outputs.

They are not repository source content.

## Test Reports And Artifacts

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

The dedicated pytest-html artifact contains the Smoke report.

The broader Smoke runtime artifact uploads:

```text
reports/
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

The dedicated pytest-html artifact contains the Regression report.

The broader Regression runtime artifact uploads:

```text
reports/
```

### Full-Suite Artifacts

Full-suite pytest-html report:

```text
reports/report.html
```

Full-suite Allure results:

```text
reports/allure-results/
```

Generated full-suite Allure HTML report:

```text
reports/allure-report/
```

GitHub Actions artifact names:

```text
pytest-html-report
full-suite-allure-report
test-artifacts
```

Responsibilities:

* `pytest-html-report` — dedicated existing full-suite pytest-html report
* `full-suite-allure-report` — generated Allure HTML report
* `test-artifacts` — broader existing `reports/` runtime output

The Allure artifact uses:

```yaml
name: full-suite-allure-report
path: reports/allure-report/
```

The existing `test-artifacts` artifact continues to upload:

```text
reports/
```

This preserves the existing runtime artifact behavior.

Because Allure output is located inside `reports/`, the broader `test-artifacts` artifact may also contain Allure runtime output in addition to the dedicated Allure report artifact.

The dedicated `full-suite-allure-report` artifact remains the clearly named source for the generated advanced report.

## Artifact Upload After Test Failure

Browser-job artifact upload steps use:

```yaml
if: always()
```

This allows available reports and runtime outputs to be uploaded even when a test command fails within an executing browser job.

The full-suite Allure report-generation step also uses:

```yaml
if: always()
```

and separately checks whether usable Allure result data exists.

Therefore:

* a failed test suite still fails the job
* available pytest-html output can still be uploaded
* available failure screenshots can still be uploaded
* Allure report generation can still be attempted
* a generated Allure report can still be published as an artifact

If the `quality` job fails, the browser jobs do not start, so they do not produce browser-test artifacts for that workflow execution.

## Failure Screenshots And Parallel Execution

Failure screenshots are generated through the existing Pytest failure hook.

Screenshot output is stored under:

```text
reports/screenshots/
```

Screenshot filenames include:

* the test name
* a UTC timestamp

The screenshot mechanism was validated with pytest-xdist worker-level execution.

The current implementation does not require a sequential-only screenshot mechanism.

Phase 4D extends the existing screenshot behavior by attaching the same successfully captured PNG to Allure result data.

The original runtime screenshot continues to exist under:

```text
reports/screenshots/
```

This keeps screenshot evidence useful independently of Allure while also exposing it inside the advanced report.

## Generated Runtime Output Policy

Generated reports and evidence are runtime outputs.

Current generated paths include:

```text
reports/
reports/screenshots/
reports/allure-results/
reports/allure-report/
```

Generated reporting output should not be committed to Git.

The repository ignore policy includes:

```text
reports/*
!reports/.gitkeep

allure-results/
allure-report/
```

Because the implemented Allure output paths are currently nested under `reports/`, they are already covered by the `reports/*` ignore rule.

The additional root-level Allure ignore entries protect against accidental generated output if Allure is run with default or alternate root-level paths.

Repository content should include:

* test code
* framework code
* configuration
* documentation

Repository content should not include generated:

* pytest-html reports
* Allure result files
* Allure HTML reports
* failure screenshots
* other execution artifacts

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
* Allure report inspection

Phase 4D does not change the existing seven-day retention strategy.

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
* Allure report generation may still be attempted after full-suite test failure

The workflow does not use:

```yaml
continue-on-error: true
```

for the required quality or browser-test execution commands.

A failed required validation should therefore prevent the workflow from being treated as successful.

pytest-xdist does not change this failure policy.

Allure reporting also does not change this failure policy.

Reporting provides evidence about execution.

It does not mask test failures.

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

For a larger shared workstream branch, multiple approved tasks may be completed and pushed on the same branch before one final workstream Pull Request is created.

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

## Phase 4B, Phase 4C, And Phase 4D Strategy

The current CI combines three framework maturity layers.

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
* preservation of existing pytest-html reports
* preservation of existing artifact names
* preservation of seven-day artifact retention
* preservation of Chromium-only browser execution

Phase 4C does not introduce new GitHub Actions jobs.

The core browser commands are:

```bash
pytest -m smoke -n auto -v
pytest -m regression -n auto -v
pytest -n auto -v
```

The independent Smoke, Regression, and full-suite GitHub Actions jobs may still execute concurrently after `quality`.

That remains GitHub Actions job-level concurrency.

pytest-xdist worker execution happens independently inside each browser-test job.

### Phase 4D — Reporting Upgrade

Phase 4D adds reporting capabilities without changing the established CI job architecture.

Implemented Phase 4D behavior includes:

* Allure Pytest integration
* full-suite Allure result collection
* full-suite Allure HTML generation
* explicit Allure CLI setup in CI
* Java setup required by Allure CLI
* dedicated `full-suite-allure-report` artifact
* preservation of existing pytest-html reports
* preservation of existing artifact names
* preservation of seven-day artifact retention
* reuse of existing failure screenshots as Allure attachments
* reporting compatibility with pytest-xdist
* reporting compatibility with sequential local execution
* continued Chromium-only browser scope

The current complementary reporting model is:

```text
pytest-html
    → lightweight HTML reports

Allure
    → advanced full-suite reporting

failure screenshots
    → direct browser failure evidence
    → attached to Allure when result collection is active

GitHub Actions artifacts
    → temporary distribution of generated CI outputs
```

Allure does not replace pytest-html.

Phase 4D does not introduce:

* Allure history persistence
* trend-history storage
* report hosting
* GitHub Pages publishing
* additional browser jobs
* CI matrices
* retries
* cross-browser reporting
* trace/video policy
* runtime environment configuration

## Current CI Status

The current CI pipeline implements the Phase 4B structure, Phase 4C parallel execution strategy, and Phase 4D reporting strategy.

It currently validates or provides:

* project dependency setup
* Ruff
* Black
* isort
* dedicated parallel Smoke execution
* dedicated parallel Regression execution
* parallel complete automated Pytest execution
* Playwright Chromium setup for browser jobs
* pytest-html report generation
* full-suite Allure result generation
* full-suite Allure HTML report generation
* failure screenshot evidence
* job-specific test artifacts
* dedicated full-suite Allure report artifact
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
│       └── pytest-html
├── regression
│   └── pytest-xdist
│       └── pytest-html
└── full-suite
    └── pytest-xdist
        ├── pytest-html
        ├── Allure results
        └── Allure HTML report
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

The current CI scope does not implement:

* runtime environment configuration
* multi-browser execution
* Docker execution
* CI matrices
* additional marker-specific jobs
* Allure history persistence
* hosted Allure reporting
* GitHub Pages reporting
* retries

These remain outside the current implemented CI scope.

## Future Improvements

Future CI and framework maturity work may include capabilities approved in later project phases, such as:

* improved diagnostics and logs
* runtime environment configuration
* dependency or browser caching where justified
* JUnit XML publishing where useful
* Allure history and trend persistence
* hosted reporting where justified
* multi-browser execution
* Docker-based execution
* scheduled execution
* improved test analytics

The following are already implemented and should not be described as future-only functionality:

* dedicated Smoke and Regression CI jobs
* pytest-xdist parallel execution
* pytest-html reporting
* failure screenshots
* local Allure reporting
* full-suite CI Allure reporting
* dedicated Allure report artifact publishing

Future capabilities should not be described as implemented until their corresponding project scope is completed and validated.