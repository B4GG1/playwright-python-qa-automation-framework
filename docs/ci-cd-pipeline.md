# CI/CD Pipeline (GitHub Actions)

## Overview

This project uses GitHub Actions as the main Continuous Integration (CI) pipeline.

The current pipeline combines:

* the Phase 4B CI job structure
* the Phase 4C pytest-xdist parallel execution strategy
* the Phase 4D reporting strategy
* the Phase 4E runtime configuration strategy
* the Phase 4F diagnostics strategy
* the Phase 5A representative Playwright cross-browser Smoke validation strategy

The workflow provides:

* dedicated code-quality validation
* dedicated Chromium Smoke execution
* dedicated Chromium Regression execution
* complete Chromium full-suite execution
* representative Firefox Smoke execution
* representative WebKit Smoke execution

The reporting and diagnostic strategy intentionally uses complementary mechanisms:

* pytest-html provides lightweight self-contained HTML reports
* Allure provides advanced reporting for the complete Chromium full-suite CI execution
* configurable failure screenshots provide browser evidence for failed test calls
* Phase 4F runtime diagnostics expose effective execution configuration
* Phase 4F failed-test diagnostics expose failure identity and available browser context
* Playwright trace and video capabilities remain available through runtime configuration
* browser-specific GitHub Actions artifacts preserve generated reporting and debugging outputs temporarily

Chromium Smoke and Regression remain focused on pytest-html reporting.

The complete Chromium `full-suite` job additionally collects Allure result data, generates an Allure HTML report, and publishes it as a dedicated GitHub Actions artifact.

The Phase 5A `cross-browser-smoke` matrix reuses the existing Smoke suite on Firefox and WebKit. Each matrix entry installs only its selected browser engine, executes through pytest-xdist, generates a browser-specific pytest-html report, and uploads browser-specific artifacts.

Chromium remains the primary complete regression browser. Firefox and WebKit provide representative browser-engine compatibility validation and do not execute the complete Regression suite or complete full suite.

Phase 4F diagnostics operate through the existing Pytest execution path and do not introduce a separate diagnostics job or persistent diagnostic artifact.

At the current stage, the project focuses on CI.

Continuous Delivery / Deployment is not implemented and should not be treated as part of the current project capabilities.

## Current CI Scope

The current CI pipeline supports:

* Python 3.12 setup
* dependency installation from `requirements-lock.txt`
* dedicated Ruff, Black, and isort quality validation
* dedicated Chromium Smoke browser-test execution
* dedicated Chromium Regression browser-test execution
* complete unfiltered Chromium Pytest full-suite execution
* representative Firefox Smoke browser-test execution
* representative WebKit Smoke browser-test execution
* a dedicated Firefox/WebKit `cross-browser-smoke` matrix
* `pytest-xdist` worker-level parallel execution in every browser-test job
* automatic xdist worker selection through `-n auto`
* Playwright Chromium installation with Linux dependencies in Chromium browser-test jobs
* installation of only the selected Firefox or WebKit engine in the corresponding cross-browser matrix entry
* centralized Phase 4E runtime configuration
* explicit browser-test CI runtime defaults
* configurable application base URL
* Chromium as the primary complete regression browser
* Firefox and WebKit as representative Smoke compatibility browsers
* explicit headless execution
* explicit Playwright timeout defaults
* configurable failure screenshot policy
* configurable trace policy
* configurable video policy
* Phase 4F runtime summary diagnostics
* Phase 4F failed-test diagnostics
* xdist runtime-header de-duplication
* failed-test node ID reporting
* failed-test phase reporting
* current page URL reporting when available
* custom screenshot path reporting when available
* diagnostic error reporting
* pytest-html report generation
* browser-specific Firefox and WebKit pytest-html reports
* Allure result collection in the Chromium `full-suite` job
* Allure HTML report generation in the Chromium `full-suite` job
* failure screenshot collection
* Allure failure screenshot attachments
* job-specific GitHub Actions artifacts
* independent Firefox and WebKit cross-browser artifacts
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

The current workflow does not provide workflow-dispatch runtime configuration forms.

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
* expose execution diagnostics
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

Phase 4F diagnostics also do not require secrets or additional GitHub permissions.

## Execution Environment

Each CI job executes on a fresh GitHub-hosted runner.

Current execution environment:

* `ubuntu-latest`
* Python 3.12
* isolated runtime environment
* dependencies installed from `requirements-lock.txt`

The Chromium browser-test jobs install Chromium and its required Linux dependencies through Playwright.

The `cross-browser-smoke` matrix installs only the selected matrix engine:

* Firefox in the Firefox matrix entry
* WebKit in the WebKit matrix entry

The `quality` job does not install Playwright browsers because it performs static code-quality validation only.

The `quality` job also does not use pytest-xdist.

The Chromium `full-suite` job additionally prepares the tooling required for Allure HTML report generation:

* Java 17 through `actions/setup-java@v4`
* Allure CLI through the `allure-commandline` npm package

Firefox and WebKit Smoke matrix entries do not install Java or the Allure CLI because their reporting responsibility is limited to pytest-html and runtime artifacts.

Phase 4F diagnostics use the existing Python runtime and Python standard-library logging support.

They do not require an additional CI package, logging service, or persistent filesystem location.

GitHub-hosted runners are temporary and are destroyed after execution.

Generated reports and browser evidence therefore need to be published as workflow artifacts when they should remain available after the job completes.

## Current Job Structure

The current job structure extends the Phase 4B topology with the Phase 5A representative cross-browser Smoke matrix:

```text
quality
├── smoke [Chromium]
├── regression [Chromium]
├── full-suite [Chromium]
└── cross-browser-smoke
    ├── Firefox
    └── WebKit
```

The dependency model is intentional.

The `quality` job executes first.

After `quality` succeeds:

* `smoke`
* `regression`
* `full-suite`
* `cross-browser-smoke (firefox)`
* `cross-browser-smoke (webkit)`

become independently executable browser-test jobs.

All browser-test jobs depend on:

```yaml
needs: quality
```

The browser-test jobs do not depend on each other.

A failure in one browser-test job does not prevent the other already-released browser-test jobs from executing.

The cross-browser matrix uses:

```yaml
fail-fast: false
```

so a failure in one additional browser does not cancel the other matrix entry.

GitHub Actions may schedule independent browser-test jobs concurrently when runners are available.

Phase 4C provides worker-level parallel test execution inside each browser-test job.

Phase 5A reuses the same pytest-xdist execution model in both Firefox and WebKit Smoke matrix entries.

These are separate execution mechanisms:

* **GitHub Actions job-level concurrency** — independent browser-test jobs may execute at the same time after `quality`
* **GitHub Actions matrix expansion** — `cross-browser-smoke` expands into Firefox and WebKit executions
* **Pytest worker-level parallelism** — pytest-xdist distributes collected tests between workers inside each browser-test job

The resulting execution model is:

```text
quality
├── smoke [Chromium]
│   └── pytest-xdist workers
├── regression [Chromium]
│   └── pytest-xdist workers
├── full-suite [Chromium]
│   └── pytest-xdist workers
└── cross-browser-smoke
    ├── Firefox
    │   └── pytest-xdist workers
    └── WebKit
        └── pytest-xdist workers
```

Phase 4D advanced reporting remains inside the Chromium `full-suite` job.

Conceptually:

```text
quality
├── smoke [Chromium]
│   └── pytest-xdist
│       └── pytest-html
├── regression [Chromium]
│   └── pytest-xdist
│       └── pytest-html
├── full-suite [Chromium]
│   └── pytest-xdist
│       ├── pytest-html
│       ├── Allure results
│       ├── failure screenshots
│       └── Allure HTML report
└── cross-browser-smoke
    ├── Firefox
    │   └── pytest-xdist
    │       └── browser-specific pytest-html
    └── WebKit
        └── pytest-xdist
            └── browser-specific pytest-html
```

Phase 4E provides explicit runtime configuration to browser-test jobs.

Phase 4F provides diagnostics through the same Pytest execution path.

Phase 5A changes browser execution coverage without changing marker ownership or introducing duplicate browser-specific functional test modules.

The `quality` job remains outside the browser, xdist, browser-runtime, diagnostic-hook, and test-reporting execution layers.

## Phase 4E Runtime Defaults

The approved default browser-test runtime values remain:

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

The Chromium Smoke, Regression, and full-suite jobs use those values directly.

The Phase 5A Firefox/WebKit matrix uses the same runtime settings except that:

```text
QA_BROWSER
```

is supplied from:

```text
matrix.browser
```

and therefore resolves to either:

```text
firefox
```

or:

```text
webkit
```

The CI runtime strategy therefore preserves:

* Sauce Demo as the default application origin
* Chromium as the default and primary complete regression browser
* representative Firefox and WebKit Smoke compatibility validation
* headless execution
* 30-second Playwright action and navigation timeout
* 5-second Playwright assertion timeout
* existing failure screenshot behavior
* trace disabled by default
* video disabled by default

The `quality` job does not require browser runtime values because it does not start browser-test execution.

Phase 4F does not add additional `QA_*` environment variables.

## Runtime Configuration Ownership

The CI workflow provides explicit environment values.

Runtime parsing and validation remain owned by:

```text
config/settings.py
```

Integration with pytest-playwright and framework-level Pytest hooks remains owned by:

```text
conftest.py
```

Application URL composition remains owned by:

```text
pages/base_page.py
```

Diagnostic formatting remains owned by:

```text
framework/diagnostics.py
```

CI therefore does not duplicate:

* runtime configuration parsing
* validation
* browser lifecycle ownership
* diagnostics formatting
* screenshot implementation

Its responsibility is to provide predictable runtime values to the already implemented framework layers.

The resulting flow is:

```text
.github/workflows/ci.yml
        ↓
QA_* environment variables
        ↓
config/settings.py
        ↓
root conftest.py
        ├── pytest-playwright integration
        ├── runtime diagnostic header
        ├── BrowserContext timeout configuration
        └── failed-test diagnostic hook
        ↓
framework/diagnostics.py
        ↓
pytest-playwright / Playwright
        ↓
test execution
```

Page Object URL composition separately consumes:

```text
settings.base_url
        ↓
BasePage
        ↓
application routes
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

The effective base URL is also exposed through the Phase 4F runtime summary.

The workflow does not currently use:

* environment profiles
* `.env` loading
* secrets for the base URL
* workflow-dispatch base URL form inputs

## Browser Configuration In CI

The runtime configuration layer recognizes:

```text
chromium
firefox
webkit
```

The implemented CI browser strategy is intentionally asymmetric.

### Chromium

Chromium remains the primary complete regression browser.

The dedicated Chromium jobs use:

```text
QA_BROWSER=chromium
```

and install:

```bash
playwright install --with-deps chromium
```

Chromium executes:

* Smoke
* Regression
* the complete unfiltered full suite

### Firefox And WebKit

The Phase 5A `cross-browser-smoke` matrix is limited to:

```text
firefox
webkit
```

Each matrix entry receives:

```text
QA_BROWSER=${{ matrix.browser }}
```

and installs only the selected browser engine:

```bash
playwright install --with-deps ${{ matrix.browser }}
```

Firefox executes representative Smoke coverage only.

WebKit executes representative Smoke coverage only.

Chromium is intentionally not duplicated in the matrix because it already has dedicated Smoke, Regression, and full-suite jobs.

The effective browser value is exposed in the Phase 4F runtime summary.

The current implementation does not introduce:

* complete Firefox Regression execution
* complete WebKit Regression execution
* complete Firefox full-suite execution
* complete WebKit full-suite execution
* browser-specific functional test modules
* a dedicated cross-browser pytest marker
* browser-specific skip logic without a demonstrated compatibility limitation

Cross-browser CI therefore represents representative compatibility validation rather than complete three-browser regression coverage.

## Headed And Headless Execution In CI

The browser-test jobs explicitly use:

```text
QA_HEADED=false
```

CI therefore remains headless.

The runtime configuration layer also supports headed local execution, but that capability does not change the CI execution model.

The current workflow does not provide a headed CI mode or workflow-dispatch toggle.

The effective execution mode is shown as:

```text
mode=headless
```

in the Phase 4F runtime summary.

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

The effective values are exposed in the runtime summary as:

```text
action_navigation_timeout_ms
assertion_timeout_ms
```

## Screenshot Policy In CI

Current screenshot policy:

```text
QA_SCREENSHOT_POLICY=only-on-failure
```

This preserves the existing project-owned screenshot mechanism.

When a browser test fails during the Pytest `call` phase and exposes the Playwright `page` fixture:

* the project screenshot hook captures one PNG
* the screenshot is written under `reports/screenshots/`
* the successful screenshot path is added to the Phase 4F failed-test diagnostic summary
* the same successfully captured PNG can be attached to Allure as `Failure screenshot`

The workflow does not enable pytest-playwright's screenshot option as a second project-level screenshot mechanism.

This avoids duplicate screenshot generation.

The runtime configuration also supports:

```text
QA_SCREENSHOT_POLICY=off
```

but CI intentionally retains the approved default:

```text
only-on-failure
```

Setup and teardown failures receive Phase 4F failed-test diagnostics but do not trigger custom screenshot capture.

If screenshot capture fails, the diagnostic mechanism reports the screenshot operation error.

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

Phase 4F does not automatically enable tracing and does not change trace lifecycle ownership.

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

Phase 4F does not automatically enable video capture and does not change video lifecycle ownership.

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

CI currently does not pass explicit native browser, trace, or video options because the approved runtime values are supplied through the `QA_*` environment variables.

For the Phase 5A matrix, browser selection is supplied through `QA_BROWSER=${{ matrix.browser }}`.

The Phase 4F runtime summary reports the effective values exposed through the resulting Pytest configuration.

## Phase 4F Runtime Diagnostics In CI

Phase 4F diagnostics operate automatically during browser-test Pytest execution.

The shared diagnostics implementation is:

```text
framework/diagnostics.py
```

The runtime integration is provided by:

```text
conftest.py
```

No CI command-line flag is required to enable the runtime summary or failed-test diagnostics.

### Runtime Summary

The runtime summary is emitted through:

```text
pytest_report_header
```

Current fields are:

* base URL
* browser
* headed/headless mode
* action/navigation timeout
* assertion timeout
* screenshot policy
* trace policy
* video policy

Representative output:

```text
[runtime] base_url=... | browser=... | mode=... | action_navigation_timeout_ms=... | assertion_timeout_ms=... | screenshot=... | trace=... | video=...
```

This gives CI logs immediate visibility into the effective browser-test configuration.

The same diagnostic mechanism applies to Chromium, Firefox, and WebKit executions.

### pytest-xdist Header Behavior

Browser-test jobs use pytest-xdist.

The Phase 4F runtime hook detects worker execution and does not return the runtime header from xdist workers.

This prevents each worker from printing the same runtime summary.

The controlling Pytest process therefore provides one execution-level runtime summary.

### Failed-Test Diagnostics

When a Pytest report fails, Phase 4F adds diagnostic context for:

```text
setup
call
teardown
```

Every failed-test summary identifies:

* Pytest node ID
* failure phase

When a Playwright page is available, diagnostics additionally attempt to include:

* current page URL

When the project screenshot is successfully created, diagnostics additionally include:

* screenshot path

Representative output:

```text
[failure] test=<node-id> | phase=<phase> | url=<current-url> | screenshot=<path>
```

URL and screenshot fields are included only when the corresponding values are available.

### Diagnostic Errors

Errors occurring during diagnostic evidence collection are also surfaced.

Current operations include:

```text
page-url
screenshot
allure-attachment
```

Representative output:

```text
[diagnostic-error] operation=<operation> | test=<node-id> | phase=<phase> | error=<error>
```

Diagnostic errors are:

* emitted through the project diagnostics logger
* appended to failed Pytest report diagnostic sections

The diagnostics logger does not use a project FileHandler.

Phase 4F therefore does not create persistent project log files in CI.

## Diagnostic CI Boundaries

Phase 4F does not introduce:

* a diagnostics GitHub Actions job
* diagnostic-specific environment variables
* persistent log files
* log-file artifacts
* browser console capture
* network capture
* custom network tracing
* HTML or page-source dumps
* automatic trace enablement
* automatic video enablement
* retries
* hosted diagnostics
* new workflow topology

Diagnostics remain part of normal browser-test execution.

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
* Playwright
* pytest-playwright
* pytest-xdist
* pytest-html
* allure-pytest
* Ruff
* Black
* isort
* the remaining project dependencies

The Allure CLI itself is not provided by the Python requirements file.

It is prepared separately inside the `full-suite` CI job.

Phase 4F diagnostics do not add another external Python dependency.

They use Python's standard `logging` module.

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

* install Playwright browsers
* execute browser tests
* execute Pytest through xdist
* use browser runtime settings
* emit browser runtime diagnostics
* generate pytest-html reports
* generate Allure results
* generate Allure HTML reports
* upload browser-test artifacts

A failure in Ruff, Black, isort, dependency installation, or another required quality-job step fails the job.

Because all browser-test jobs declare:

```yaml
needs: quality
```

a failed quality job prevents Chromium Smoke, Chromium Regression, Chromium full-suite, Firefox Smoke, and WebKit Smoke execution.

This avoids unnecessary browser setup and test execution when the repository does not pass the initial code-quality gate.

## Smoke Job

The `smoke` job provides dedicated Chromium CI execution of the approved Smoke marker suite.

It depends on:

```yaml
needs: quality
```

After the quality job succeeds, the Smoke job:

1. checks out the repository
2. configures Python 3.12
3. installs project dependencies
4. receives the explicit Phase 4E runtime defaults
5. installs Playwright Chromium
6. executes the Smoke suite through pytest-xdist
7. emits the Phase 4F runtime summary
8. provides Phase 4F failed-test diagnostics when failures occur
9. generates a self-contained pytest-html report
10. uploads Smoke-specific artifacts

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

Smoke does not collect or generate a dedicated Allure report.

This is intentional.

The dedicated Smoke job remains the lightweight, targeted pytest-html feedback path for Chromium.

Current Chromium Smoke runtime defaults remain:

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

Available screenshots created during failed call phases are stored under:

```text
reports/screenshots/
```

and can be included in:

```text
smoke-test-artifacts
```

because that artifact uploads the broader:

```text
reports/
```

directory.

## Regression Job

The `regression` job provides dedicated Chromium CI execution of the approved Regression marker suite.

It depends on:

```yaml
needs: quality
```

After the quality job succeeds, the Regression job:

1. checks out the repository
2. configures Python 3.12
3. installs project dependencies
4. receives the explicit Phase 4E runtime defaults
5. installs Playwright Chromium
6. executes the Regression suite through pytest-xdist
7. emits the Phase 4F runtime summary
8. provides Phase 4F failed-test diagnostics when failures occur
9. generates a self-contained pytest-html report
10. uploads Regression-specific artifacts

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

A failing Regression test fails the `regression` job.

The job does not use:

```yaml
continue-on-error: true
```

Regression does not collect or generate a dedicated Allure report.

This is intentional.

Current Chromium Regression runtime defaults are identical to the Chromium Smoke and full-suite defaults.

Available screenshots created during failed call phases can be included in:

```text
regression-test-artifacts
```

through the uploaded:

```text
reports/
```

directory.

## Full-Suite Job

The Chromium `full-suite` job remains the complete unfiltered CI regression gate.

It depends on:

```yaml
needs: quality
```

After the quality job succeeds, the full-suite job:

1. checks out the repository
2. configures Python 3.12
3. installs project dependencies
4. receives the explicit Phase 4E runtime defaults
5. configures Java 17
6. installs the Allure CLI
7. installs Playwright Chromium
8. executes the complete unfiltered suite through pytest-xdist
9. emits the Phase 4F runtime summary
10. provides Phase 4F failed-test diagnostics when failures occur
11. generates pytest-html
12. collects Allure result data
13. generates the Allure HTML report when usable result data exists
14. uploads full-suite reports and artifacts

The actual test command is:

```bash
mkdir -p reports
pytest -n auto -v \
  --html=reports/report.html \
  --self-contained-html \
  --alluredir=reports/allure-results \
  --clean-alluredir
```

The execution produces:

```text
reports/report.html
reports/allure-results/
```

When failures occur during applicable test calls, it may additionally produce:

```text
reports/screenshots/
```

Phase 4F diagnostics themselves do not create another persistent output directory.

## Cross-Browser Smoke Job

The `cross-browser-smoke` job provides representative Firefox and WebKit compatibility validation through one GitHub Actions matrix.

It depends on:

```yaml
needs: quality
```

Current matrix:

```yaml
strategy:
  fail-fast: false
  matrix:
    browser:
      - firefox
      - webkit
```

Each matrix entry:

1. checks out the repository
2. configures Python 3.12
3. installs project dependencies
4. receives the normal browser-test runtime configuration
5. sets `QA_BROWSER` from `${{ matrix.browser }}`
6. installs only its selected Playwright browser engine
7. executes the existing Smoke suite through pytest-xdist
8. emits the Phase 4F runtime summary
9. provides Phase 4F failed-test diagnostics when failures occur
10. generates a browser-specific self-contained pytest-html report
11. uploads browser-specific report and runtime artifacts

Browser installation:

```bash
playwright install --with-deps ${{ matrix.browser }}
```

Core test command:

```bash
pytest -m smoke -n auto -v
```

Actual report output:

```text
reports/${{ matrix.browser }}-smoke-report.html
```

The resulting report files are:

```text
reports/firefox-smoke-report.html
reports/webkit-smoke-report.html
```

The matrix intentionally excludes Chromium because Chromium already has a dedicated Smoke job plus Regression and complete full-suite execution.

Firefox and WebKit do not collect or generate dedicated Allure reports.

Current browser-specific artifact names are:

```text
firefox-smoke-pytest-html-report
firefox-smoke-test-artifacts
webkit-smoke-pytest-html-report
webkit-smoke-test-artifacts
```

The broader browser-specific runtime artifacts upload:

```text
reports/
```

Available screenshots created during failed call phases can therefore be preserved within the corresponding browser-specific runtime artifact.

The matrix does not use `continue-on-error`, so a failed Firefox or WebKit Smoke execution fails its corresponding matrix job.

`fail-fast: false` ensures that one matrix failure does not prevent the other browser from producing its result.

## Allure CLI Setup In CI

The full-suite job configures Java 17 through:

```yaml
actions/setup-java@v4
```

Current configuration:

```yaml
distribution: temurin
java-version: "17"
```

The workflow installs Allure CLI with:

```bash
npm install -g allure-commandline
allure --version
```

The standalone Allure CLI is required for converting Allure result data into the browsable HTML report.

It is separate from:

```text
allure-pytest
```

which is installed through the Python dependency lock and handles Pytest-side result generation.

Chromium Smoke, Chromium Regression, Firefox Smoke, and WebKit Smoke do not configure Java or Allure CLI because they do not generate Allure HTML reports.

Phase 4F diagnostics also do not require Java or Allure CLI.

## Full-Suite Allure HTML Generation

After Pytest execution, the workflow attempts to generate:

```text
reports/allure-report/
```

using:

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

Every current browser-test CI execution uses:

```text
-n auto
```

to enable worker-level parallel execution.

Current core Chromium CI commands are:

```bash
pytest -m smoke -n auto -v
pytest -m regression -n auto -v
pytest -n auto -v
```

The actual Chromium full-suite command additionally enables pytest-html and Allure result collection.

The Phase 5A Firefox/WebKit matrix executes:

```bash
pytest -m smoke -n auto -v
```

with `QA_BROWSER` supplied from the matrix browser value.

Sequential local execution remains supported.

Examples:

```bash
pytest -m smoke -v
pytest -m regression -v
pytest -v
```

Representative local cross-browser Smoke validation uses:

```bash
QA_BROWSER=firefox pytest -m smoke -n auto -v
QA_BROWSER=webkit pytest -m smoke -n auto -v
```

Parallel execution extends the supported execution strategy rather than replacing sequential Pytest execution.

Runtime configuration and diagnostics apply consistently across Chromium, Firefox, and WebKit execution.

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
* Phase 4F diagnostics do not depend on shared cross-worker state
* representative Smoke scenarios remain browser-engine-neutral unless a genuine compatibility limitation is demonstrated

Application scenario fixtures are located in:

```text
tests/conftest.py
```

Framework-level Pytest integration remains in:

```text
conftest.py
```

This responsibility split does not change the test isolation model.

No sequential-only test exception is required for the current suite.

### Reporting And Diagnostic Compatibility

The current implementation is compatible with the existing xdist model.

Supported behavior includes:

* pytest-html under parallel Chromium CI execution
* browser-specific pytest-html under parallel Firefox/WebKit Smoke execution
* Allure result collection through the parallel Chromium full suite
* failure screenshot capture during parallel execution
* Allure attachment of failure screenshots when result collection is active
* Phase 4F failed-test diagnostics
* one execution-level runtime summary without worker duplication

Sequential execution remains supported as well.

No sequential-only reporting or diagnostics requirement is introduced.

## GitHub Actions Concurrency Versus Pytest Parallelism

GitHub Actions job-level concurrency, GitHub Actions matrix expansion, and pytest-xdist worker-level parallelism operate at different levels.

### GitHub Actions Job-Level Concurrency

After `quality` succeeds, GitHub Actions may independently schedule:

```text
smoke [Chromium]
regression [Chromium]
full-suite [Chromium]
cross-browser-smoke (firefox)
cross-browser-smoke (webkit)
```

Each is an independent browser-test execution in its own runner environment.

The Firefox and WebKit executions originate from the same `cross-browser-smoke` matrix job definition.

### Pytest Worker-Level Parallelism

Inside each browser-test execution, pytest-xdist distributes collected tests between worker processes.

For example:

```text
cross-browser-smoke (firefox)
└── pytest -m smoke -n auto -v
    ├── worker
    ├── worker
    └── ...
```

The number of workers selected by `-n auto` depends on the execution environment and should not be treated as a fixed CI configuration value.

Phase 4C introduced worker-level parallel execution inside the existing Chromium jobs.

Phase 5A reuses that same xdist model for representative Firefox and WebKit Smoke execution.

Phase 4D reporting does not change the concurrency model.

Phase 4E runtime configuration does not change the concurrency model.

Phase 4F diagnostics do not change the concurrency model.

## Playwright Browser Installation

Playwright browsers are installed only in jobs that execute browser tests.

The Chromium jobs are:

* `smoke`
* `regression`
* `full-suite`

and use:

```bash
playwright install --with-deps chromium
```

The Phase 5A `cross-browser-smoke` matrix contains:

* Firefox
* WebKit

Each matrix entry installs only its selected engine:

```bash
playwright install --with-deps ${{ matrix.browser }}
```

The `quality` job intentionally does not install any Playwright browser.

Current browser responsibilities are:

* Chromium — Smoke, Regression, complete full suite
* Firefox — representative Smoke only
* WebKit — representative Smoke only

Installing Firefox and WebKit for representative Smoke validation does not imply complete three-browser Regression or full-suite execution.

The current execution strategy does not introduce:

* browser-specific functional test modules
* browser-specific application coverage
* a Chromium matrix entry added only for symmetry
* Selenium execution
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

Phase 5A does not add a cross-browser marker.

The existing `smoke` marker remains the representative suite used by Chromium, Firefox, and WebKit Smoke execution.

### Marker Suites Executed As Dedicated CI Jobs

The existing CI structure provides dedicated Chromium marker-filtered jobs for:

* `smoke`
* `regression`

Current Chromium commands:

```bash
pytest -m smoke -n auto -v
pytest -m regression -n auto -v
```

The Phase 5A Firefox/WebKit matrix additionally executes:

```bash
pytest -m smoke -n auto -v
```

with the browser selected through `QA_BROWSER`.

Chromium Smoke and Regression retain their existing pytest-html reporting.

Firefox and WebKit Smoke use browser-specific pytest-html reporting.

None of these marker-filtered jobs generate dedicated Allure reports.

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

These tests are still included in the complete Chromium full-suite CI execution when they form part of the normal collected test suite.

Tests that also carry `smoke` additionally participate in representative Firefox and WebKit Smoke validation.

Because the Chromium full-suite CI job uses pytest-xdist, tests may execute on xdist workers as part of the complete collection.

Because the Chromium full-suite also collects Allure results, those tests can additionally appear in the advanced full-suite Allure report.

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

Approved Chromium parallel commands:

```bash
pytest -m smoke -n auto -v
pytest -m regression -n auto -v
pytest -n auto -v
```

Representative cross-browser Smoke commands:

```bash
QA_BROWSER=firefox pytest -m smoke -n auto -v
QA_BROWSER=webkit pytest -m smoke -n auto -v
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

This independence allows E2E tests to participate safely in parallel full-suite execution and allows Smoke-tagged E2E checkpoints to execute safely in representative Firefox/WebKit validation.

Runtime configuration and diagnostics do not alter marker semantics.

## Local And CI Execution Responsibilities

Local execution and CI execution serve related but different purposes.

### Local Execution

Local execution supports sequential and parallel Pytest modes.

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
* validating diagnostics through controlled failures
* generating local Allure reporting
* enabling trace or video during focused diagnostics
* validating representative Firefox and WebKit compatibility

Sequential execution remains useful for normal development and focused debugging.

Primary Chromium parallel validation commands are:

```bash
pytest -m smoke -n auto -v
pytest -m regression -n auto -v
pytest -n auto -v
```

Representative cross-browser Smoke validation uses:

```bash
QA_BROWSER=firefox pytest -m smoke -n auto -v
QA_BROWSER=webkit pytest -m smoke -n auto -v
```

Local Allure results can be collected through either sequential or parallel complete-suite execution.

Example:

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
* dedicated parallel Chromium Smoke execution
* dedicated parallel Chromium Regression execution
* parallel complete unfiltered Chromium full-suite execution
* representative parallel Firefox Smoke execution
* representative parallel WebKit Smoke execution
* explicit runtime defaults
* Phase 4F runtime diagnostics
* Phase 4F failed-test diagnostics
* clean-environment browser execution
* pytest-html reporting
* browser-specific Firefox/WebKit pytest-html reporting
* Chromium full-suite Allure reporting
* configurable failure screenshots
* browser-specific downloadable runtime artifacts
* merge-gate feedback

The Chromium full-suite job remains the complete automated regression gate.

Chromium Smoke and Regression provide additional targeted feedback.

Firefox and WebKit Smoke provide representative browser-engine compatibility feedback without replacing or expanding complete Chromium regression responsibility.

## Reporting And Diagnostic Responsibilities

The current model intentionally separates responsibilities.

### Runtime Diagnostics

Phase 4F runtime diagnostics expose effective browser-test configuration through Pytest output.

They provide execution context rather than a persistent report.

No diagnostic file is created.

### Failed-Test Diagnostics

Phase 4F failed-test diagnostics provide:

* node ID
* failure phase
* current URL when available
* custom screenshot path when available
* diagnostic-operation errors when evidence collection fails

They supplement normal Pytest failure output.

### pytest-html

pytest-html provides the lightweight HTML reporting layer.

It is used by:

* Chromium Smoke CI
* Chromium Regression CI
* Chromium full-suite CI
* Firefox Smoke CI
* WebKit Smoke CI

Current Chromium report files:

```text
reports/smoke-report.html
reports/regression-report.html
reports/report.html
```

Current cross-browser Smoke report files:

```text
reports/firefox-smoke-report.html
reports/webkit-smoke-report.html
```

pytest-html remains available after Allure, diagnostics, and Phase 5A cross-browser integration.

Neither Allure nor diagnostics replace it.

### Allure

Allure provides the richer advanced reporting layer.

Current responsibilities include:

* structured result collection through `allure-pytest`
* local complete-suite reporting
* parallel reporting compatibility
* generated local HTML reports
* complete Chromium full-suite CI reporting
* failure screenshot attachments

Current output locations:

```text
reports/allure-results/
reports/allure-report/
```

Allure is not currently generated independently in Chromium Smoke, Chromium Regression, Firefox Smoke, or WebKit Smoke jobs.

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

and the failure occurs during:

```text
call
```

with a Playwright page available.

When screenshot capture succeeds:

* the screenshot remains available under `reports/screenshots/`
* the path is included in the failed-test diagnostic summary
* when Allure result collection is active, the same PNG is attached as `Failure screenshot`

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

Phase 4F does not change this ownership.

### GitHub Actions Artifacts

GitHub Actions artifacts preserve generated reports and runtime evidence after the temporary runner is destroyed.

Artifacts are temporary execution outputs.

They are not repository source content.

## Test Reports And Artifacts

### Chromium Smoke Artifacts

Smoke HTML report:

```text
reports/smoke-report.html
```

GitHub Actions artifact names:

```text
smoke-pytest-html-report
smoke-test-artifacts
```

The dedicated pytest-html artifact contains the Chromium Smoke report.

The broader Smoke runtime artifact uploads:

```text
reports/
```

Available failure screenshots are therefore included when generated.

### Chromium Regression Artifacts

Regression HTML report:

```text
reports/regression-report.html
```

GitHub Actions artifact names:

```text
regression-pytest-html-report
regression-test-artifacts
```

The dedicated pytest-html artifact contains the Chromium Regression report.

The broader Regression runtime artifact uploads:

```text
reports/
```

Available failure screenshots are therefore included when generated.

### Cross-Browser Smoke Artifacts

Firefox HTML report:

```text
reports/firefox-smoke-report.html
```

Firefox GitHub Actions artifact names:

```text
firefox-smoke-pytest-html-report
firefox-smoke-test-artifacts
```

WebKit HTML report:

```text
reports/webkit-smoke-report.html
```

WebKit GitHub Actions artifact names:

```text
webkit-smoke-pytest-html-report
webkit-smoke-test-artifacts
```

Each dedicated pytest-html artifact contains the corresponding browser-specific report.

Each broader browser runtime artifact uploads:

```text
reports/
```

so available failure screenshots and other report outputs for that matrix execution are preserved independently.

Browser-specific artifact names prevent Firefox and WebKit matrix entries from colliding.

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

* `pytest-html-report` — dedicated full-suite pytest-html report
* `full-suite-allure-report` — generated Allure HTML report
* `test-artifacts` — broader `reports/` runtime output

The Allure artifact uses:

```yaml
name: full-suite-allure-report
path: reports/allure-report/
```

The existing `test-artifacts` artifact uploads:

```text
reports/
```

Because Allure output is located inside `reports/`, the broader `test-artifacts` artifact may also contain Allure runtime output in addition to the dedicated Allure report artifact.

The dedicated `full-suite-allure-report` artifact remains the clearly named source for the generated advanced report.

### Phase 4F Diagnostics Artifact Boundary

Runtime summaries and failed-test diagnostic sections are part of Pytest execution output.

Phase 4F does not create:

* `diagnostics.log`
* another log directory
* a dedicated diagnostics artifact
* a persistent diagnostic report file

Failure screenshots remain separate generated evidence under:

```text
reports/screenshots/
```

and are handled through the existing `reports/` artifact strategy.

### Trace And Video Artifact Boundary

Current CI defaults do not generate trace or video output:

```text
QA_TRACE_POLICY=off
QA_VIDEO_POLICY=off
```

Therefore, the current CI does not add:

* a trace artifact upload step
* a video artifact upload step
* new trace/video artifact names
* trace/video retention by default

If a future approved CI strategy enables these outputs, artifact publication should be defined explicitly rather than assumed from the current workflow.

## Artifact Upload After Test Failure

Browser-job artifact upload steps use:

```yaml
if: always()
```

This allows available reports and runtime outputs to be uploaded even when a test command fails within an executing browser job.

The Chromium full-suite Allure report-generation step also uses:

```yaml
if: always()
```

and separately checks whether usable Allure result data exists.

Therefore:

* a failed test suite still fails its job
* available pytest-html output can still be uploaded
* available failure screenshots can still be uploaded
* failed-test diagnostics remain visible in Pytest output
* Chromium full-suite Allure report generation can still be attempted
* a generated Allure report can still be published as an artifact

If the `quality` job fails, the browser jobs do not start, so they do not produce browser-test artifacts for that workflow execution.

Trace and video remain disabled under the default CI runtime configuration.

## Failure Screenshots And Parallel Execution

Failure screenshots are generated through the framework-level Pytest failure hook when screenshot policy is enabled.

Screenshot output is stored under:

```text
reports/screenshots/
```

Screenshot filenames include:

* the test name
* a UTC timestamp

The screenshot mechanism remains compatible with pytest-xdist worker-level execution.

The current implementation does not require a sequential-only screenshot mechanism.

Phase 4D reuses the same successfully captured PNG as the Allure screenshot attachment.

Phase 4E controls the feature through:

```text
QA_SCREENSHOT_POLICY
```

Phase 4F additionally exposes the screenshot path in the failed-test diagnostic summary after successful capture.

Phase 5A reuses the same screenshot and diagnostic behavior during Firefox and WebKit Smoke execution.

The original runtime screenshot continues to exist under:

```text
reports/screenshots/
```

when the policy is `only-on-failure` and capture succeeds.

This keeps screenshot evidence useful independently of Allure while also exposing its location through failure diagnostics.

## Generated Runtime Output Policy

Generated reports and persistent evidence are runtime outputs.

Current generated paths include:

```text
reports/
reports/screenshots/
reports/allure-results/
reports/allure-report/
test-results/
playwright-report/
```

Generated reporting and diagnostic artifacts should not be committed to Git.

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

Phase 4F runtime and failure summaries are transient console/report-section diagnostics and do not add another generated-output directory.

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
* persistent diagnostic log files
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

Phase 4F does not change the existing seven-day retention strategy.

Phase 5A uses the same seven-day retention for Firefox and WebKit browser-specific artifacts.

Trace and video are disabled by default and therefore are not part of the default retained CI artifact set.

## Quality Gate Behavior

The CI pipeline acts as a merge quality gate.

Current expected failure behavior:

* Ruff failure fails `quality`
* Black validation failure fails `quality`
* isort validation failure fails `quality`
* failed `quality` prevents all browser-test jobs from starting
* invalid runtime configuration prevents normal browser-test execution
* Chromium Smoke test failure fails `smoke`
* Chromium Regression test failure fails `regression`
* Chromium full-suite test failure fails `full-suite`
* Firefox Smoke failure fails the Firefox `cross-browser-smoke` matrix entry
* WebKit Smoke failure fails the WebKit `cross-browser-smoke` matrix entry
* `fail-fast: false` allows the other cross-browser matrix entry to continue when one matrix entry fails
* browser-test failures are not converted into successful results
* available browser-job reports and artifacts are uploaded through `if: always()`
* Allure report generation may still be attempted after Chromium full-suite test failure
* Phase 4F diagnostics provide failure context without changing test outcomes

The workflow does not use:

```yaml
continue-on-error: true
```

for required quality or browser-test execution commands.

A failed required validation should therefore prevent the workflow from being treated as successful.

pytest-xdist does not change this failure policy.

Matrix execution does not change this failure policy.

Allure reporting does not change this failure policy.

Runtime configuration does not change this failure policy.

Phase 4F diagnostics do not change this failure policy.

Reporting and diagnostics provide evidence about execution.

They do not mask test or configuration failures.

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

Current runtime values, Phase 4F diagnostics, and Phase 5A browser selection do not require secrets.

## Phase 4B–Phase 5A CI Strategy

The current CI combines the framework maturity layers introduced during Phase 4 with the Phase 5A cross-browser execution extension.

### Phase 4B — CI Execution Structure

Phase 4B established:

* separation of code-quality validation from browser execution
* dedicated Smoke CI execution
* dedicated Regression CI execution
* preserved complete full-suite execution
* explicit job dependencies through the quality gate
* suite-specific reports and artifacts

The Phase 4B structure at the time of implementation was:

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
* preservation of Chromium-only browser execution for the Phase 4C workstream

Phase 4C did not introduce new GitHub Actions jobs.

The core browser commands are:

```bash
pytest -m smoke -n auto -v
pytest -m regression -n auto -v
pytest -n auto -v
```

The independent Smoke, Regression, and full-suite GitHub Actions jobs could execute concurrently after `quality`.

That remains GitHub Actions job-level concurrency.

pytest-xdist worker execution happens independently inside each browser-test job.

Phase 5A later reuses the same xdist strategy for Firefox and WebKit Smoke validation.

### Phase 4D — Reporting Upgrade

Phase 4D added reporting capabilities without changing the established CI job architecture at that time.

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
* continued Chromium-only browser scope for the Phase 4D workstream

The complementary reporting model introduced by Phase 4D is:

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

Phase 4D did not introduce:

* Allure history persistence
* trend-history storage
* report hosting
* GitHub Pages publishing
* additional browser jobs
* CI matrices
* retries
* cross-browser reporting

Phase 5A later adds browser-specific pytest-html reporting for Firefox and WebKit Smoke while preserving the Chromium full-suite Allure responsibility.

Trace/video policy and runtime environment configuration were added separately in Phase 4E.

### Phase 4E — Runtime Configuration

Phase 4E added centralized execution configuration while preserving the established Phase 4B–4D CI architecture.

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
* preservation of Chromium-only browser installation for the Phase 4E workstream

Phase 4E did not introduce:

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

Those statements describe the Phase 4E workstream boundary.

Phase 5A later consumes the browser-selection capability already provided by Phase 4E.

### Phase 4F — Diagnostics And Fixture Cleanup

Phase 4F improved runtime visibility and framework responsibility boundaries while preserving the established Phase 4 CI structure at the time of implementation.

Implemented CI-relevant behavior includes:

* runtime summary formatting through `framework/diagnostics.py`
* failed-test summary formatting
* diagnostic error formatting
* project diagnostics logger
* runtime summary through `pytest_report_header`
* effective base URL visibility
* effective browser visibility
* headed/headless mode visibility
* action/navigation timeout visibility
* assertion timeout visibility
* screenshot policy visibility
* trace policy visibility
* video policy visibility
* xdist worker runtime-header suppression
* failed-test node ID reporting
* `setup`, `call`, and `teardown` failure-phase reporting
* current URL reporting when a Playwright page is available
* screenshot path reporting after successful custom screenshot capture
* diagnostic error reporting for page URL retrieval
* diagnostic error reporting for screenshot creation
* diagnostic error reporting for Allure attachment
* framework-level runtime and diagnostics hooks retained in root `conftest.py`
* application scenario fixtures separated into `tests/conftest.py`
* preserved fixture scopes
* preserved test independence
* preserved pytest-xdist compatibility
* preserved custom screenshot ownership
* preserved pytest-playwright trace ownership
* preserved pytest-playwright video ownership
* preserved pytest-html reporting
* preserved Allure reporting
* preserved Phase 4 GitHub Actions topology
* preserved artifact names
* preserved seven-day artifact retention

Phase 4F did not introduce:

* a new GitHub Actions job
* a diagnostics workflow
* persistent project log files
* a log-file artifact
* browser console capture
* network capture
* HTML or page-source dumps
* automatic trace enablement
* automatic video enablement
* retries
* another browser installation
* another reporting service
* another CI topology

Those statements describe the Phase 4F workstream boundary.

Phase 5A later adds the cross-browser Smoke matrix while preserving Phase 4F diagnostic and fixture behavior.

### Phase 5A — Playwright Cross-Browser Smoke Validation

Phase 5A extends the existing Chromium execution strategy with representative Firefox and WebKit compatibility validation.

Implemented CI behavior includes:

* Chromium remaining the primary complete regression browser
* preservation of dedicated Chromium Smoke execution
* preservation of dedicated Chromium Regression execution
* preservation of complete Chromium full-suite execution
* a dedicated `cross-browser-smoke` matrix
* Firefox as a representative Smoke compatibility browser
* WebKit as a representative Smoke compatibility browser
* `needs: quality` on the cross-browser matrix
* `fail-fast: false` for independent Firefox and WebKit results
* installation of only the selected matrix browser engine
* reuse of the existing `smoke` marker
* pytest-xdist execution through `-n auto`
* centralized runtime configuration through `QA_BROWSER`
* browser-specific self-contained pytest-html reports
* independent Firefox and WebKit report artifact names
* independent Firefox and WebKit broader runtime artifact names
* preservation of the existing Chromium Allure reporting responsibility
* preservation of Phase 4F diagnostics and screenshot behavior

The matrix is intentionally limited to:

```text
firefox
webkit
```

Chromium is not added to the matrix because it already has dedicated Smoke, Regression, and full-suite jobs.

Phase 5A does not introduce:

* complete Firefox Regression execution
* complete WebKit Regression execution
* complete Firefox full-suite execution
* complete WebKit full-suite execution
* a new cross-browser pytest marker
* duplicate browser-specific test modules
* browser-specific application coverage
* Selenium
* browser-specific conditional logic without a demonstrated engine limitation

## Phase 4F Validation Status

Final Phase 4F validation confirmed:

```text
Smoke: 31 passed
Regression: 109 passed
Full sequential: 236 passed
Full pytest-xdist: 236 passed
Ruff: passed
Black check: passed
isort: passed
```

Controlled failure validation after fixture responsibility separation confirmed:

* runtime header
* failure phase
* Pytest node ID
* current page URL
* screenshot diagnostic path

This confirms that Phase 4F diagnostics and fixture responsibility cleanup remain compatible with the existing sequential and pytest-xdist execution model.

## Phase 5A Cross-Browser Validation Status

Phase 5A validation confirmed that the existing representative Smoke suite executes successfully on Firefox and WebKit without browser-specific test modules or compatibility workarounds.

Local validation confirmed:

```text
Firefox Smoke: 31 passed
WebKit Smoke: 31 passed
Chromium full-suite: 236 passed
Ruff: passed
Black check: passed
isort: passed
```

GitHub Actions validation confirmed successful execution of:

* `quality`
* Chromium `smoke`
* Chromium `regression`
* Chromium `full-suite`
* `cross-browser-smoke (firefox)`
* `cross-browser-smoke (webkit)`

The validated CI execution also produced independent Firefox and WebKit pytest-html reports and browser-specific artifact names.

No Firefox- or WebKit-specific conditional, skip, or duplicated test implementation was required.

The validation confirms the intended responsibility split:

* Chromium — primary complete regression browser
* Firefox — representative Smoke compatibility browser
* WebKit — representative Smoke compatibility browser

## Current CI Status

The current CI pipeline implements:

* Phase 4B CI execution structure
* Phase 4C parallel execution
* Phase 4D reporting
* Phase 4E runtime configuration
* Phase 4F runtime and failed-test diagnostics
* Phase 5A representative Playwright cross-browser Smoke validation

It currently validates or provides:

* project dependency setup
* Ruff
* Black
* isort
* dedicated parallel Chromium Smoke execution
* dedicated parallel Chromium Regression execution
* parallel complete Chromium Pytest execution
* representative parallel Firefox Smoke execution
* representative parallel WebKit Smoke execution
* a dedicated Firefox/WebKit `cross-browser-smoke` matrix
* explicit runtime defaults
* configurable application origin
* Chromium as the primary complete regression browser
* Firefox/WebKit runtime selection through the matrix
* explicit headless CI execution
* approved timeout defaults
* default failure screenshot policy
* trace disabled by default
* video disabled by default
* Phase 4F runtime summary
* xdist runtime-header de-duplication
* failed-test node ID diagnostics
* failed-test phase diagnostics
* current page URL diagnostics when available
* custom screenshot path diagnostics when available
* diagnostic error reporting
* Playwright Chromium setup for Chromium browser jobs
* Playwright Firefox setup for the Firefox Smoke matrix entry
* Playwright WebKit setup for the WebKit Smoke matrix entry
* pytest-html report generation
* browser-specific Firefox/WebKit pytest-html reports
* Chromium full-suite Allure result generation
* Chromium full-suite Allure HTML report generation
* failure screenshot evidence
* job-specific test artifacts
* browser-specific Firefox/WebKit artifacts
* dedicated full-suite Allure report artifact
* Pull Requests targeting `develop`
* Pull Requests targeting `main`
* pushes to `develop`
* pushes to `main`
* manual workflow executions

Current execution structure:

```text
runtime defaults
        ↓
Phase 4F runtime diagnostics
        ↓
quality
├── smoke [Chromium]
│   └── pytest-xdist
│       └── pytest-html
├── regression [Chromium]
│   └── pytest-xdist
│       └── pytest-html
├── full-suite [Chromium]
│   └── pytest-xdist
│       ├── pytest-html
│       ├── Allure results
│       ├── failure screenshots
│       └── Allure HTML report
└── cross-browser-smoke
    ├── Firefox
    │   └── pytest-xdist
    │       └── browser-specific pytest-html
    └── WebKit
        └── pytest-xdist
            └── browser-specific pytest-html
```

The quality job is the prerequisite gate.

All browser-test executions are independent after successful quality validation.

The Chromium full-suite job remains the complete unfiltered CI regression gate.

Firefox and WebKit provide representative Smoke compatibility validation only.

Dedicated CI jobs are not currently implemented for:

* UI
* Security
* Sorting
* Navigation
* E2E

The current CI scope does not implement:

* complete Firefox Regression
* complete WebKit Regression
* complete Firefox full-suite execution
* complete WebKit full-suite execution
* Docker execution
* environment profiles
* `.env` loading
* workflow-dispatch configuration forms
* device emulation
* additional marker-specific jobs
* Allure history persistence
* hosted Allure reporting
* GitHub Pages reporting
* retries
* persistent project log files
* browser console capture
* network capture
* HTML or page-source dumps
* automatic trace enablement
* automatic video enablement
* diagnostic-specific CI jobs
* Selenium execution

Formal Phase 5A roadmap completion remains outside this documentation file and belongs to the dedicated Phase 5A closing task.

## Future Improvements

Future CI and framework maturity work may include capabilities approved in later project phases, such as:

* dependency or browser caching where justified
* JUnit XML publishing where useful
* Allure history and trend persistence
* hosted reporting where justified
* complete Firefox or WebKit Regression/full-suite execution if future scope justifies it
* environment profiles
* `.env` loading if explicitly approved
* Docker-based execution
* scheduled execution
* improved test analytics
* persistent structured logging if explicitly justified
* browser console capture if explicitly approved
* additional diagnostic evidence if justified by future scope

The following are already implemented and should not be described as future-only functionality:

* dedicated Chromium Smoke CI
* dedicated Chromium Regression CI
* complete Chromium full-suite CI
* representative Firefox Smoke CI
* representative WebKit Smoke CI
* Firefox/WebKit `cross-browser-smoke` matrix
* pytest-xdist parallel execution
* pytest-html reporting
* browser-specific Firefox/WebKit pytest-html reports
* browser-specific Firefox/WebKit artifacts
* failure screenshots
* local Allure reporting
* Chromium full-suite CI Allure reporting
* dedicated Allure report artifact publishing
* centralized runtime environment configuration
* runtime Chromium/Firefox/WebKit browser selection
* headed/headless configuration
* Playwright timeout configuration
* screenshot policy
* trace policy
* video policy
* explicit CI runtime defaults
* Phase 4F runtime diagnostics
* Phase 4F failed-test diagnostics
* xdist runtime-header de-duplication
* diagnostic error reporting
* framework-hook and application-fixture responsibility separation

Future capabilities should not be described as implemented until their corresponding project scope is completed and validated.