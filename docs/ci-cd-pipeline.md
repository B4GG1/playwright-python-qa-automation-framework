# CI/CD Pipeline (GitHub Actions)

## Overview

This project uses GitHub Actions as the main Continuous Integration (CI) pipeline.

The current pipeline combines:

* the Phase 4B CI job structure
* the Phase 4C pytest-xdist parallel execution strategy
* the Phase 4D reporting strategy
* the Phase 4E runtime configuration strategy

The workflow provides dedicated CI jobs for:

* code-quality validation
* parallel Smoke suite execution
* parallel Regression suite execution
* parallel complete full-suite execution

The reporting strategy intentionally uses complementary mechanisms:

* pytest-html provides lightweight self-contained HTML reports
* Allure provides advanced reporting for the complete full-suite CI execution
* configurable failure screenshots provide browser evidence for failed test calls
* Playwright trace and video capabilities are available through runtime configuration
* GitHub Actions artifacts preserve generated reporting and debugging outputs temporarily

Smoke and Regression remain focused on pytest-html reporting.

The complete `full-suite` job additionally collects Allure result data, generates an Allure HTML report, and publishes it as a dedicated GitHub Actions artifact.

The three browser-test jobs use explicit Phase 4E runtime defaults while preserving the existing CI architecture.

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
* centralized Phase 4E runtime configuration
* explicit browser-test CI runtime defaults
* configurable application base URL
* explicit Chromium browser selection
* explicit headless execution
* explicit Playwright timeout defaults
* configurable failure screenshot policy
* configurable trace policy
* configurable video policy
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

Phase 4E does not introduce workflow-dispatch configuration forms.

Manual workflow execution therefore uses the same workflow-defined runtime defaults unless the workflow itself is changed in a future approved task.

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
* secrets for non-secret runtime configuration values

Phase 4E runtime defaults are normal workflow environment values.

They are not stored as secrets because they do not contain sensitive information.

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

Phase 4E adds explicit runtime configuration to the existing browser-test jobs.

It does not modify the job topology.

Conceptually:

```text
Phase 4E browser runtime defaults
        ↓
quality
├── smoke
│   └── pytest-xdist
├── regression
│   └── pytest-xdist
└── full-suite
    └── pytest-xdist
```

The `quality` job remains outside the browser, xdist, browser-runtime, and test-reporting execution layers.

## Phase 4E Runtime Defaults

Smoke, Regression, and full-suite use explicit runtime values:

```text
QA_BASE_URL=https://www.saucedemo.com
QA_BROWSER=chromium
QA_HEADED=false
QA_TIMEOUT_MS=30000
QA_EXPECT_TIMEOUT_MS=5000
QA_SCREENSHOT_POLICY=only-on-failure
QA_TRACE_POLICY=off
QA_VIDEO_POLICY=off
```

These values intentionally match the approved local defaults defined by:

```text
config/settings.py
```

The CI runtime defaults therefore preserve:

* Sauce Demo as the default application origin
* Chromium execution
* headless execution
* 30-second Playwright action and navigation timeout
* 5-second Playwright assertion timeout
* existing failure screenshot behavior
* trace disabled by default
* video disabled by default

The environment values are configured directly in each browser-test job.

The `quality` job does not require them because it does not start browser-test execution.

## Runtime Configuration Ownership

The CI workflow provides explicit environment values.

Runtime parsing and validation remain owned by:

```text
config/settings.py
```

Integration with pytest-playwright remains owned by:

```text
conftest.py
```

Application URL composition remains owned by:

```text
pages/base_page.py
```

CI therefore does not duplicate configuration parsing logic.

Its responsibility is to provide predictable values to the already implemented framework configuration layer.

The resulting flow is:

```text
.github/workflows/ci.yml
        ↓
QA_* environment variables
        ↓
config/settings.py
        ↓
conftest.py / BasePage
        ↓
pytest-playwright / Playwright
        ↓
test execution
```

## Base URL Configuration In CI

The current CI application origin is:

```text
QA_BASE_URL=https://www.saucedemo.com
```

The configured origin is consumed through the framework runtime configuration.

Page Objects continue to use their application-relative `ROUTE` values.

The CI workflow does not require test or Page Object modifications to define the application origin.

The configured base URL must satisfy the validation implemented in `config/settings.py`.

Invalid explicit configuration fails before normal test execution proceeds.

The workflow does not currently use:

* environment profiles
* `.env` loading
* secrets for the base URL
* workflow-dispatch base URL form inputs

## Browser Configuration In CI

The browser-test jobs explicitly use:

```text
QA_BROWSER=chromium
```

The framework configuration layer recognizes:

```text
chromium
firefox
webkit
```

but CI installs only:

```text
chromium
```

Current installation command:

```bash
playwright install --with-deps chromium
```

The CI pipeline therefore remains intentionally Chromium-only.

Recognizing Firefox and WebKit in project runtime configuration does not mean that CI provides those browsers.

Phase 4E does not introduce:

* a browser matrix
* Firefox installation
* WebKit installation
* browser-specific workflow jobs
* cross-browser compatibility claims

## Headed And Headless Execution In CI

The browser-test jobs explicitly use:

```text
QA_HEADED=false
```

CI therefore remains headless.

The runtime configuration layer also supports headed local execution, but that capability does not change the CI execution model.

The current workflow does not provide a headed CI mode or workflow-dispatch toggle.

## Timeout Configuration In CI

The browser-test jobs explicitly use:

```text
QA_TIMEOUT_MS=30000
QA_EXPECT_TIMEOUT_MS=5000
```

`QA_TIMEOUT_MS` is applied through the framework as:

* Playwright default action timeout
* Playwright default navigation timeout

`QA_EXPECT_TIMEOUT_MS` configures:

* Playwright assertion timeout

The CI values intentionally match the approved local defaults.

Timeout values are interpreted as integer milliseconds by the runtime configuration layer.

## Screenshot Policy In CI

Current screenshot policy:

```text
QA_SCREENSHOT_POLICY=only-on-failure
```

This preserves the project screenshot mechanism implemented before Phase 4E.

When a browser test fails during the Pytest call phase and exposes the Playwright `page` fixture:

* the project screenshot hook captures a PNG
* the screenshot is written under `reports/screenshots/`
* the same successfully captured PNG can be attached to Allure as `Failure screenshot`

The workflow does not enable pytest-playwright's screenshot option as a second project-level screenshot mechanism.

This avoids duplicate screenshot generation.

The runtime configuration also supports:

```text
QA_SCREENSHOT_POLICY=off
```

but CI intentionally retains the approved default `only-on-failure`.

## Trace Policy In CI

Current trace policy:

```text
QA_TRACE_POLICY=off
```

Supported project values are:

```text
off
retain-on-failure
on
```

Trace behavior uses pytest-playwright / Playwright-supported mechanisms.

The project does not implement custom trace recording logic.

When enabled locally or in another explicitly configured execution, pytest-playwright trace output is generated under its runtime artifact structure rooted at:

```text
test-results/
```

Representative trace output includes:

```text
trace.zip
```

CI does not enable or retain traces by default.

Phase 4E therefore adds trace configurability without adding default CI trace artifacts.

## Video Policy In CI

Current video policy:

```text
QA_VIDEO_POLICY=off
```

Supported project values are:

```text
off
retain-on-failure
on
```

Video behavior uses pytest-playwright / Playwright-supported mechanisms.

The project does not implement custom video recording logic.

When enabled locally or in another explicitly configured execution, generated video output is written under the pytest-playwright runtime artifact structure rooted at:

```text
test-results/
```

Representative video output includes:

```text
video.webm
```

CI does not enable or retain videos by default.

Phase 4E therefore adds video configurability without adding default CI video artifacts.

## Native pytest-playwright Runtime Options

Project runtime configuration is integrated with the existing pytest-playwright model rather than replacing it.

Explicit native pytest-playwright runtime options remain usable where supported by the implementation.

For browser selection, an explicitly supplied native:

```text
--browser
```

option is not silently replaced by `QA_BROWSER`.

For trace and video, explicitly supplied native pytest-playwright options take precedence over the corresponding project environment-derived policy.

This preserves normal pytest-playwright command-line behavior for explicit execution overrides.

CI currently does not pass explicit native browser, trace, or video options because the approved Phase 4E defaults are supplied through the `QA_*` environment variables.

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
* use Phase 4E browser runtime settings
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
4. resolves the explicit Phase 4E runtime defaults
5. installs Playwright Chromium
6. executes the Smoke suite through pytest-xdist
7. generates a self-contained pytest-html report
8. uploads Smoke-specific artifacts

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

Current Smoke runtime defaults remain:

```text
QA_BASE_URL=https://www.saucedemo.com
QA_BROWSER=chromium
QA_HEADED=false
QA_TIMEOUT_MS=30000
QA_EXPECT_TIMEOUT_MS=5000
QA_SCREENSHOT_POLICY=only-on-failure
QA_TRACE_POLICY=off
QA_VIDEO_POLICY=off
```

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
4. resolves the explicit Phase 4E runtime defaults
5. installs Playwright Chromium
6. executes the Regression suite through pytest-xdist
7. generates a self-contained pytest-html report
8. uploads Regression-specific artifacts

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

Current Regression runtime defaults remain:

```text
QA_BASE_URL=https://www.saucedemo.com
QA_BROWSER=chromium
QA_HEADED=false
QA_TIMEOUT_MS=30000
QA_EXPECT_TIMEOUT_MS=5000
QA_SCREENSHOT_POLICY=only-on-failure
QA_TRACE_POLICY=off
QA_VIDEO_POLICY=off
```

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
4. resolves the explicit Phase 4E runtime defaults
5. configures Java 17 for Allure CLI
6. installs Allure CLI
7. installs Playwright Chromium
8. executes the complete Pytest suite through pytest-xdist
9. generates the existing self-contained pytest-html report
10. collects Allure result data
11. generates the Allure HTML report when usable result data exists
12. uploads the existing pytest-html artifact
13. uploads the dedicated Allure report artifact
14. uploads the broader `reports/` runtime artifact

The full-suite execution is intentionally not filtered by Pytest markers.

Current full-suite runtime defaults remain:

```text
QA_BASE_URL=https://www.saucedemo.com
QA_BROWSER=chromium
QA_HEADED=false
QA_TIMEOUT_MS=30000
QA_EXPECT_TIMEOUT_MS=5000
QA_SCREENSHOT_POLICY=only-on-failure
QA_TRACE_POLICY=off
QA_VIDEO_POLICY=off
```

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

```text
if usable Allure result data exists
    generate reports/allure-report/
else
    skip Allure HTML generation
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

Runtime configuration applies consistently to both execution modes.

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
* runtime configuration is process-level execution configuration rather than shared test state

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

Phase 4E does not introduce a separate parallel runtime configuration model.

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

Phase 4E also does not change either concurrency model.

Reporting and runtime configuration are separate concerns layered onto the established execution structure.

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

The runtime configuration recognizes Playwright browser engines, but CI remains Chromium-only.

The current execution, reporting, and runtime configuration strategy does not introduce:

* Firefox CI execution
* WebKit CI execution
* cross-browser matrices
* browser-specific parallel jobs
* device-specific browser jobs

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

They remain available for selective local execution and scoped validation during implementation or investigation.

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

Runtime configuration does not alter marker semantics.

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
* validating runtime configuration overrides
* generating local Allure reporting
* enabling trace or video during focused diagnostics

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

Runtime overrides may be supplied for a single local process.

Example:

```bash
QA_BROWSER=chromium \
QA_HEADED=false \
QA_TIMEOUT_MS=45000 \
QA_EXPECT_TIMEOUT_MS=7000 \
QA_TRACE_POLICY=retain-on-failure \
pytest -m smoke -n auto -v
```

The Allure CLI must be installed locally and available on `PATH` for HTML generation.

### CI Execution

Current CI provides:

* mandatory code-quality validation
* dedicated parallel Smoke execution
* dedicated parallel Regression execution
* parallel complete unfiltered full-suite execution
* explicit Phase 4E runtime defaults
* clean-environment browser execution
* pytest-html reporting
* full-suite Allure reporting
* configurable failure screenshots
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

pytest-html remains available after Allure integration.

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

The screenshot is captured through the existing Pytest failure hook when:

```text
QA_SCREENSHOT_POLICY=only-on-failure
```

When screenshot capture succeeds and Allure result collection is active, the same PNG file is attached to the Allure result as:

```text
Failure screenshot
```

The Allure integration does not capture a second screenshot.

The existing screenshot file is reused.

When:

```text
QA_SCREENSHOT_POLICY=off
```

the project failure screenshot and corresponding Allure screenshot attachment are disabled.

Current CI retains:

```text
QA_SCREENSHOT_POLICY=only-on-failure
```

### Trace And Video

Trace and video are Playwright diagnostic outputs controlled through runtime configuration.

Current project policies:

```text
QA_TRACE_POLICY
QA_VIDEO_POLICY
```

Supported values:

```text
off
retain-on-failure
on
```

Both CI defaults are:

```text
off
```

When enabled, generated output uses pytest-playwright runtime artifact paths rooted under:

```text
test-results/
```

Representative files include:

```text
trace.zip
video.webm
```

These are runtime diagnostics rather than repository source content.

They are not enabled or retained by CI by default.

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

### Trace And Video Artifact Boundary

Current CI defaults do not generate trace or video output:

```text
QA_TRACE_POLICY=off
QA_VIDEO_POLICY=off
```

Therefore, Phase 4E does not add:

* a trace artifact upload step
* a video artifact upload step
* new trace/video artifact names
* trace/video retention in CI by default

If a future approved CI strategy enables these outputs, artifact publication should be defined explicitly rather than assumed from the current workflow.

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

Trace and video remain disabled under the default CI runtime configuration.

## Failure Screenshots And Parallel Execution

Failure screenshots are generated through the existing Pytest failure hook when screenshot policy is enabled.

Screenshot output is stored under:

```text
reports/screenshots/
```

Screenshot filenames include:

* the test name
* a UTC timestamp

The screenshot mechanism remains compatible with pytest-xdist worker-level execution.

The current implementation does not require a sequential-only screenshot mechanism.

Phase 4D attaches the same successfully captured PNG to Allure result data.

Phase 4E adds the ability to disable the screenshot mechanism through:

```text
QA_SCREENSHOT_POLICY=off
```

The original runtime screenshot continues to exist under:

```text
reports/screenshots/
```

when the policy is `only-on-failure` and capture succeeds.

This keeps screenshot evidence useful independently of Allure while also exposing it inside the advanced report.

## Generated Runtime Output Policy

Generated reports and evidence are runtime outputs.

Current generated paths include:

```text
reports/
reports/screenshots/
reports/allure-results/
reports/allure-report/
test-results/
playwright-report/
```

Generated reporting and diagnostic output should not be committed to Git.

The repository ignore policy includes generated-output protection for:

```text
reports/*
!reports/.gitkeep

allure-results/
allure-report/
test-results/
playwright-report/
```

Because the implemented Allure output paths are currently nested under `reports/`, they are already covered by the `reports/*` ignore rule.

The additional root-level Allure ignore entries protect against accidental generated output if Allure is run with default or alternate root-level paths.

`test-results/` protects pytest-playwright runtime output such as traces and videos.

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
* trace ZIP files
* video files
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

Phase 4E does not change the existing seven-day retention strategy.

Trace and video are disabled by default and therefore are not part of the default retained CI artifact set.

## Quality Gate Behavior

The CI pipeline acts as a merge quality gate.

Current expected failure behavior:

* Ruff failure fails `quality`
* Black validation failure fails `quality`
* isort validation failure fails `quality`
* failed `quality` prevents all browser jobs from starting
* invalid runtime configuration prevents normal browser-test execution
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

Allure reporting does not change this failure policy.

Runtime configuration does not change this failure policy.

Reporting provides evidence about execution.

It does not mask test or configuration failures.

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
* do not store non-secret runtime defaults as secrets
* avoid unnecessary workflow permissions
* use minimal `GITHUB_TOKEN` permissions

Current permission configuration:

```yaml
permissions:
  contents: read
```

No elevated GitHub token permission is currently required.

Current Phase 4E runtime values do not require secrets.

## Phase 4B, Phase 4C, Phase 4D, And Phase 4E Strategy

The current CI combines four framework maturity layers.

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

Trace/video policy and runtime environment configuration were added separately in Phase 4E.

### Phase 4E — Runtime Configuration

Phase 4E adds centralized execution configuration while preserving the established Phase 4B–4D CI architecture.

Implemented CI-related behavior includes:

* explicit `QA_BASE_URL`
* explicit `QA_BROWSER`
* explicit `QA_HEADED`
* explicit `QA_TIMEOUT_MS`
* explicit `QA_EXPECT_TIMEOUT_MS`
* explicit `QA_SCREENSHOT_POLICY`
* explicit `QA_TRACE_POLICY`
* explicit `QA_VIDEO_POLICY`
* approved defaults aligned with local execution
* browser-test job integration
* preservation of the existing quality gate
* preservation of pytest-xdist execution
* preservation of existing Smoke and Regression commands
* preservation of complete full-suite execution
* preservation of pytest-html
* preservation of full-suite Allure reporting
* preservation of existing artifact names
* preservation of seven-day retention
* preservation of `contents: read`
* preservation of workflow triggers
* preservation of Chromium-only browser installation

Phase 4E does not introduce:

* workflow matrices
* browser matrices
* Firefox installation
* WebKit installation
* cross-browser CI execution
* workflow-dispatch runtime configuration forms
* secrets for non-secret runtime values
* retries
* `continue-on-error`
* default trace retention
* default video retention
* device emulation
* Phase 4F diagnostics changes

The Phase 4E implementation uses the existing runtime configuration and pytest-playwright integration rather than creating CI-specific browser management logic.

## Current CI Status

The current CI pipeline implements the Phase 4B structure, Phase 4C parallel execution strategy, Phase 4D reporting strategy, and Phase 4E runtime configuration strategy.

It currently validates or provides:

* project dependency setup
* Ruff
* Black
* isort
* dedicated parallel Smoke execution
* dedicated parallel Regression execution
* parallel complete automated Pytest execution
* explicit Phase 4E runtime defaults
* configurable application origin
* explicit Chromium selection
* explicit headless CI execution
* approved timeout defaults
* default failure screenshot policy
* trace disabled by default
* video disabled by default
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
Phase 4E runtime defaults
        ↓
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

* multi-browser CI execution
* Docker execution
* CI browser matrices
* environment profiles
* `.env` loading
* workflow-dispatch configuration forms
* device emulation
* additional marker-specific jobs
* Allure history persistence
* hosted Allure reporting
* GitHub Pages reporting
* retries
* Phase 4F logging or fixture cleanup

Phase 4E was completed through AQA-0105 after final local runtime-configuration validation, sequential and pytest-xdist parallel validation, controlled artifact-policy validation, pytest-html and Allure reporting validation, successful GitHub Actions validation, and roadmap synchronization.

## Future Improvements

Future CI and framework maturity work may include capabilities approved in later project phases, such as:

* improved diagnostics and logs
* fixture organization review
* dependency or browser caching where justified
* JUnit XML publishing where useful
* Allure history and trend persistence
* hosted reporting where justified
* multi-browser execution
* browser matrices
* environment profiles
* `.env` loading if explicitly approved
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
* centralized runtime environment configuration
* runtime browser selection
* headed/headless configuration
* Playwright timeout configuration
* screenshot policy
* trace policy
* video policy
* explicit Phase 4E CI runtime defaults

Future capabilities should not be described as implemented until their corresponding project scope is completed and validated.