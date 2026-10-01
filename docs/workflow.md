# Development Workflow

This document describes the day-to-day development workflow used in this project.

For detailed branching rules, see: [Git Branching Strategy](git-branching-strategy.md).

For detailed test categorization, pytest marker semantics, sequential/parallel execution strategy, runtime configuration, and reporting behavior, see: [Testing Strategy](testing-strategy.md).

For detailed GitHub Actions execution, job dependencies, parallel browser-test execution, runtime defaults, reports, and artifacts, see: [CI/CD Pipeline](ci-cd-pipeline.md).

The workflow described below supports two branch roles:

* `develop` is the main integration branch for completed and validated work.
* `main` is the stable portfolio branch used for polished portfolio snapshots.

When this document is read from `main`, the `develop` branch may already contain newer integration work that has not yet been promoted to the stable portfolio version.

## Workflow Overview

The project follows a professional Git-based development workflow.

Regular development workflow:

```text
develop
  ↓
feature / fix / docs / refactor branch
  ↓
local implementation
  ↓
local validation
  ↓
commit and push
  ↓
Pull Request to develop
  ↓
CI validation
  ↓
Squash merge
  ↓
phase or workstream checkpoint when needed
```

Portfolio promotion workflow:

```text
develop
  ↓
final documentation and validation review
  ↓
Pull Request to main
  ↓
CI validation
  ↓
Squash merge
  ↓
stable portfolio snapshot on main
```

The goal is to keep development organized, validated, easy to review, and suitable for a public QA automation portfolio.

## Standard Task Workflow

For small independent tasks, the recommended workflow is:

1. Start from the latest `develop` branch.
2. Create a dedicated feature, fix, refactor, or documentation branch.
3. Implement changes locally.
4. Run local checks appropriate to the changed scope.
5. Commit changes with a meaningful Conventional Commit message.
6. Push the branch to GitHub.
7. Open a Pull Request into `develop`.
8. Wait for CI validation.
9. Review changed files manually.
10. Merge using Squash and merge after validation.
11. Update local `develop`.

The standard task workflow should not target `main` directly.

Regular implementation work should flow through `develop` first.

## Workstream Workflow

For larger tightly connected areas, the project may use one workstream branch.

Examples:

```text
feature/login-page
feature/inventory-products
feature/cart-page
feature/structure-cleanup
feature/checkout
feature/allure-reporting
refactor/runtime-configuration
```

In this workflow:

1. Create one branch for the whole workstream.
2. Implement multiple related tasks on the same branch.
3. Create separate commits for individual tasks.
4. Push regularly as backup.
5. Run local validation after meaningful changes.
6. Review scope, tests, documentation, reporting behavior, runtime configuration, and cleanup during the workstream.
7. Complete the final workstream checkpoint.
8. Open one Pull Request only when the whole workstream is ready.
9. Validate CI.
10. Squash merge the complete workstream into `develop`.

This approach is used for complete functional automation, refactor, documentation sync, reporting, runtime configuration, and stabilization workstreams.

It is useful when tasks are connected and reviewing them together makes more sense than creating many small Pull Requests.

A task-level commit and push on a shared workstream branch does not imply that a Pull Request should be opened immediately.

The Pull Request is created only when the complete approved workstream scope and its required checkpoint are ready.

## Branch Creation

Start from updated `develop`:

```bash
git checkout develop
git pull origin develop
```

Create a new branch:

```bash
git checkout -b feature/cart-page
```

Other examples:

```bash
git checkout -b feature/inventory-products
git checkout -b feature/checkout
git checkout -b feature/structure-cleanup
git checkout -b feature/allure-reporting
git checkout -b refactor/runtime-configuration
git checkout -b fix/screenshot-hook
git checkout -b docs/update-testing-strategy
git checkout -b docs/portfolio-docs-cleanup
git checkout -b refactor/login-fixtures
```

For documentation cleanup before portfolio promotion, a documentation branch may be used:

```bash
git checkout -b docs/phase-3-portfolio-cleanup
```

## Daily Local Workflow

Before starting work:

```bash
git status
git checkout <working-branch>
git pull origin <working-branch>
```

During work:

```bash
git status
git add <changed-files>
git commit -m "<type>(<task-id>): <short description>"
git push origin <working-branch>
```

For workstream branches, pushing after each task is recommended as a backup and to keep GitHub updated.

For documentation-only or portfolio-promotion cleanup that is not tied to a single task ID, a commit message may omit the task ID if no approved task ID exists.

Examples:

```bash
git commit -m "docs: clean documentation before main promotion"
git commit -m "chore: promote phase 3 portfolio state to main"
```

## Local Validation

The project supports both sequential and pytest-xdist parallel test execution.

Runtime configuration can be supplied through supported environment variables without editing functional tests or Page Objects.

Standard sequential validation remains supported:

```bash
ruff check .
black --check .
isort . --check-only
pytest -v
```

Sequential execution remains useful for:

* normal implementation feedback
* focused debugging
* reproducing failures
* situations where parallel execution is not required
* controlled runtime configuration validation

If formatting changes are needed:

```bash
black .
isort .
```

Then validate again:

```bash
ruff check .
black --check .
isort . --check-only
pytest -v
```

### Parallel Validation

Phase 4C introduced validated worker-level parallel execution through `pytest-xdist`.

Approved parallel validation commands:

```bash
pytest -m smoke -n auto -v
pytest -m regression -n auto -v
pytest -n auto -v
```

`-n auto` delegates worker-count selection to pytest-xdist according to the available execution environment.

Parallel execution is an additional supported execution mode.

It does not replace sequential execution.

Tests executed in parallel must remain:

* order-independent
* isolated from state produced by other tests
* independently executable
* compatible with the existing Playwright fixture model
* compatible with process-level runtime configuration

The current suite was validated under parallel execution without identified sequential-only test exceptions.

## Runtime Configuration Workflow

Phase 4E provides centralized environment-based runtime configuration through:

```text
config/settings.py
```

Supported environment variables are:

```text
QA_BASE_URL
QA_BROWSER
QA_HEADED
QA_TIMEOUT_MS
QA_EXPECT_TIMEOUT_MS
QA_SCREENSHOT_POLICY
QA_TRACE_POLICY
QA_VIDEO_POLICY
```

Default values are:

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

Normal local execution does not require these variables to be exported explicitly because the same defaults are provided by `config/settings.py`.

Use environment overrides only when the execution requires different runtime behavior.

### Base URL Override

Example:

```bash
QA_BASE_URL="http://localhost:8000" pytest -m smoke -v
```

Page Objects continue to use their normal relative routes.

The configured application origin is composed through `BasePage`.

### Browser Override

Example:

```bash
QA_BROWSER=chromium pytest -m smoke -v
```

Supported configured browser values are:

```text
chromium
firefox
webkit
```

The configured browser must also be installed in the execution environment.

Current CI installs and validates Chromium only.

Explicit native pytest-playwright browser options remain usable.

For example:

```bash
QA_BROWSER=firefox pytest -m smoke -v --browser chromium
```

uses the explicitly supplied native browser option.

### Headed Execution

Default execution is headless:

```text
QA_HEADED=false
```

Headed local execution:

```bash
QA_HEADED=true pytest -m smoke -v
```

Supported true values include:

```text
true
1
yes
on
```

Supported false values include:

```text
false
0
no
off
```

The native pytest-playwright `--headed` option remains usable.

### Timeout Overrides

Action and navigation timeout:

```bash
QA_TIMEOUT_MS=45000 pytest -m regression -v
```

Assertion timeout:

```bash
QA_EXPECT_TIMEOUT_MS=7000 pytest -m smoke -v
```

Both values are expressed in milliseconds.

They must be non-negative integers.

A value of `0` is accepted and follows Playwright timeout semantics.

### Combined Runtime Override

Several values can be supplied for one execution:

```bash
QA_BASE_URL="https://www.saucedemo.com" \
QA_BROWSER="chromium" \
QA_HEADED="false" \
QA_TIMEOUT_MS="45000" \
QA_EXPECT_TIMEOUT_MS="7000" \
QA_SCREENSHOT_POLICY="only-on-failure" \
QA_TRACE_POLICY="retain-on-failure" \
QA_VIDEO_POLICY="off" \
pytest -m smoke -n auto -v
```

The override applies to that process.

No functional test or Page Object edit is required.

### Focused Runtime Configuration Validation

Focused configuration validation uses:

```bash
pytest tests/test_runtime_config.py
```

This verifies:

* defaults
* accepted values
* normalization
* boolean parsing
* timeout parsing
* artifact policy parsing
* invalid configuration behavior

Invalid explicit configuration should fail early rather than silently falling back to a default.

## Reporting Validation

Phase 4D introduced Allure reporting while preserving pytest-html and the existing failure screenshot mechanism.

Phase 4E adds configurable screenshot, trace, and video policies without replacing the existing reporting architecture.

Allure result collection supports sequential execution:

```bash
pytest -v \
  --alluredir=reports/allure-results \
  --clean-alluredir
```

It also supports pytest-xdist parallel execution:

```bash
pytest -n auto -v \
  --alluredir=reports/allure-results \
  --clean-alluredir
```

For combined pytest-html and Allure full-suite validation:

```bash
pytest -n auto -v \
  --html=reports/report.html \
  --self-contained-html \
  --alluredir=reports/allure-results \
  --clean-alluredir
```

Generated Allure result data is stored under:

```text
reports/allure-results/
```

Generate the local Allure HTML report with:

```bash
allure generate reports/allure-results \
  --clean \
  -o reports/allure-report
```

Generated Allure HTML output is stored under:

```text
reports/allure-report/
```

The Allure CLI must be installed locally and available on `PATH` for HTML generation.

The Python `allure-pytest` dependency handles result collection.

The standalone Allure CLI handles conversion of those results into the HTML report.

Allure reporting complements pytest-html rather than replacing it.

## Failure Evidence And Runtime Artifacts

### Failure Screenshots

The default screenshot policy is:

```text
QA_SCREENSHOT_POLICY=only-on-failure
```

Failed browser tests during the Pytest call phase use the existing custom screenshot mechanism.

Failure screenshots are stored under:

```text
reports/screenshots/
```

When screenshot capture succeeds and Allure result collection is active, the same PNG is attached to the Allure result as:

```text
Failure screenshot
```

The Allure integration does not introduce a second screenshot capture mechanism.

The existing screenshot file is reused.

To disable the custom failure screenshot:

```bash
QA_SCREENSHOT_POLICY=off pytest -m smoke -v
```

When screenshot policy is disabled:

* no custom failure PNG is written
* no corresponding Allure `Failure screenshot` attachment is created

The screenshot hook applies to failures during the Pytest call phase.

Setup and teardown failures do not use this custom screenshot path.

### Trace

Trace policy is controlled through:

```text
QA_TRACE_POLICY
```

Supported values are:

```text
off
retain-on-failure
on
```

Default:

```text
off
```

Example:

```bash
QA_TRACE_POLICY=retain-on-failure pytest -m regression -v
```

Trace generation uses pytest-playwright / Playwright runtime capabilities rather than custom project recording logic.

Generated trace output is stored under the pytest-playwright runtime artifact structure rooted under:

```text
test-results/
```

Representative trace output:

```text
trace.zip
```

Explicit native pytest-playwright tracing options remain usable and take precedence when supplied directly.

### Video

Video policy is controlled through:

```text
QA_VIDEO_POLICY
```

Supported values are:

```text
off
retain-on-failure
on
```

Default:

```text
off
```

Example:

```bash
QA_VIDEO_POLICY=on pytest tests/test_login_page.py -v
```

Video generation uses pytest-playwright / Playwright runtime capabilities rather than a custom project recording implementation.

Generated video output is stored under the pytest-playwright runtime artifact structure rooted under:

```text
test-results/
```

Representative output:

```text
video.webm
```

Explicit native pytest-playwright video options remain usable and take precedence when supplied directly.

### Runtime Artifact Cleanup

Generated reports and diagnostic files are runtime outputs.

They should not be committed.

Relevant generated locations include:

```text
reports/
test-results/
allure-results/
allure-report/
playwright-report/
```

Before finalizing work that intentionally produced runtime artifacts, clean generated output when required and verify Git status.

## Marker-Based Validation

Pytest markers support selective validation.

Current executable marker suites are:

```bash
pytest -m smoke -v
pytest -m regression -v
pytest -m ui -v
pytest -m security -v
pytest -m sorting -v
pytest -m navigation -v
pytest -m e2e -v
```

All marker suites remain available for sequential local execution.

Smoke and Regression additionally have approved parallel forms:

```bash
pytest -m smoke -n auto -v
pytest -m regression -n auto -v
```

The existing CI pipeline executes dedicated Smoke and Regression jobs.

The following markers do not currently have dedicated CI jobs and remain selectively executable locally when useful:

* `ui`
* `security`
* `sorting`
* `navigation`
* `e2e`

Tests carrying these markers are still included in the complete unfiltered full-suite CI execution.

Because the full-suite CI job uses pytest-xdist, those tests may execute on different workers as part of the complete collected suite.

Because full-suite also collects Allure result data, those tests are represented in the advanced full-suite report as part of the complete execution.

Markers describe different dimensions of test intent and may be combined where useful.

Common examples:

```bash
pytest -m "smoke and ui" -v
pytest -m "regression and ui" -v
pytest -m "smoke and navigation" -v
pytest -m "regression and navigation" -v
```

Marker expressions can also be scoped to a specific test module.

Example:

```bash
pytest tests/test_checkout_page.py -m e2e -v
```

The `e2e` suite represents independent checkpoint tests that collectively form the primary purchase journey.

Tests do not depend on shared state or execution order.

This independence also allows E2E tests to participate safely in parallel full-suite execution.

Runtime overrides apply to marker-based execution without changing marker semantics.

Detailed marker meanings, test-independence expectations, execution rules, runtime behavior, and reporting behavior are documented in [Testing Strategy](testing-strategy.md).

## Workstream-Specific Validation

Run the relevant test module before the full suite when useful.

Examples:

```bash
pytest -v tests/test_login_page.py
pytest -v tests/test_inventory_page.py
pytest -v tests/test_product_details_page.py
pytest -v tests/test_cart_page.py
pytest -v tests/test_checkout_page.py
```

Additional marker-based validation should be selected according to the changed behavior.

Examples:

```bash
pytest -m smoke -v
pytest -m regression -v
pytest -m security -v
pytest -m sorting -v
pytest -m navigation -v
pytest -m e2e -v
```

When execution behavior, fixture isolation, or worker safety is part of the changed scope, parallel validation should additionally be used:

```bash
pytest -m smoke -n auto -v
pytest -m regression -n auto -v
pytest -n auto -v
```

When runtime configuration behavior changes, validate:

```bash
pytest tests/test_runtime_config.py
```

and representative runtime overrides as required by the task.

When reporting behavior is part of the changed scope, validate the relevant report generation and runtime outputs in addition to the underlying tests.

When screenshot, trace, or video policy behavior changes, controlled artifact validation may be used.

Intentionally failing tests used only for runtime validation should remain temporary and should not be committed.

The full test suite should still pass before a workstream is considered ready for merge unless a scoped validation exception is explicitly accepted.

For documentation-only changes, code behavior has not changed, but required documentation and quality validation should still be completed according to the active task.

## Commit Convention

Commit messages should include the task ID when applicable.

Recommended format:

```text
<type>(<task-id>): <short description>
```

Examples:

```bash
git commit -m "docs(AQA-0026): create login page test cases"
git commit -m "feat(AQA-0027): implement login page object model"
git commit -m "refactor(AQA-0032): parametrize login validation scenarios"
git commit -m "test(AQA-0038): add protected inventory route access test"
git commit -m "test(AQA-0057): add product to cart test"
git commit -m "chore(AQA-0064): review and stabilize cart workstream"
git commit -m "chore(AQA-0073): finalize phase 3c structure cleanup"
git commit -m "test(AQA-0078): add checkout information page tests"
git commit -m "test(AQA-0079): add checkout overview tests"
git commit -m "test(AQA-0080): add checkout completion tests"
git commit -m "chore(AQA-0082): finalize checkout automation workstream"
git commit -m "feat(AQA-0096): integrate local allure reporting"
git commit -m "chore(AQA-0097): integrate allure reporting into ci"
git commit -m "docs(AQA-0098): document phase 4d reporting strategy"
git commit -m "refactor(AQA-0100): add runtime base url configuration"
git commit -m "feat(AQA-0101): add browser and timeout runtime options"
git commit -m "feat(AQA-0102): add runtime artifact policies"
git commit -m "chore(AQA-0103): integrate runtime configuration into ci"
git commit -m "docs(AQA-0104): document phase 4e runtime configuration"
```

For documentation cleanup, checkpoint, or portfolio promotion work without a dedicated task ID, these examples are acceptable:

```bash
git commit -m "docs: clean documentation before main promotion"
git commit -m "chore: promote phase 3 portfolio state to main"
```

Common commit types:

* `feat` — new framework functionality
* `test` — automated tests or test-related changes
* `docs` — documentation changes
* `refactor` — structural improvements without intended behavior change
* `fix` — bug fixes
* `chore` — maintenance, configuration, review, CI, or promotion changes

## Pull Request Flow

Pull Requests for regular development should usually follow this direction:

```text
feature/* -> develop
fix/* -> develop
docs/* -> develop
refactor/* -> develop
chore/* -> develop
```

Portfolio promotion flow:

```text
develop -> main
```

The `main` branch should only receive stable and validated changes.

The `develop` branch should remain the normal base branch for future implementation, documentation, refactor, and framework maturity work.

For a shared workstream branch, one Pull Request is opened only after all approved tasks for that workstream and its final checkpoint are complete.

Individual task commits on the workstream branch are pushed without creating separate Pull Requests unless the approved workflow explicitly requires otherwise.

## Pull Request Checklist

Before opening a Pull Request, verify:

* the complete intended workstream scope is finished
* required checkpoint work is complete
* local working tree is clean
* relevant commits are pushed
* local quality checks passed
* relevant scoped test module passed when applicable
* relevant marker suites passed when applicable
* focused runtime configuration tests passed when runtime configuration changed
* representative runtime overrides were validated when required
* full test suite passed or an explicitly accepted scoped validation applies
* parallel execution passed when the task or workstream affects parallel-safety assumptions
* reporting validation passed when reporting behavior changed
* screenshot, trace, or video policy behavior was validated when affected
* documentation is updated if needed
* test case documentation is aligned with automated coverage
* marker documentation is aligned with current marker behavior when marker usage changes
* execution documentation reflects current sequential and parallel behavior when execution strategy changes
* runtime configuration documentation reflects `config/settings.py`, `conftest.py`, Page Objects, and CI when runtime behavior changes
* reporting documentation reflects current pytest-html, Allure, screenshot, trace, video, and artifact behavior when reporting or diagnostics change
* no generated reports, Allure outputs, screenshots, traces, or videos are tracked
* no cache files or virtual environment files are tracked
* branch target is correct
* implemented features are not mixed with planned future features
* Chromium-only CI boundaries are stated accurately
* future environment profiles or `.env` loading are not described as implemented
* cart-owned checkout entry behavior remains separated from detailed checkout behavior
* Checkout Information, Checkout Overview, and Checkout Complete behavior remain owned by Checkout tests

Recommended standard pre-PR commands:

```bash
git status
ruff check .
black --check .
isort . --check-only
pytest -v
```

For work affecting parallel execution or test isolation, additionally run:

```bash
pytest -m smoke -n auto -v
pytest -m regression -n auto -v
pytest -n auto -v
```

For work affecting runtime configuration, use focused validation:

```bash
pytest tests/test_runtime_config.py
```

and representative environment-driven execution where required.

For work affecting Allure reporting, validate result generation and HTML generation where applicable:

```bash
pytest -n auto -v \
  --html=reports/report.html \
  --self-contained-html \
  --alluredir=reports/allure-results \
  --clean-alluredir

allure generate reports/allure-results \
  --clean \
  -o reports/allure-report
```

For a workstream checkpoint, also run the relevant scoped test module and marker suites where useful.

Examples:

```bash
pytest -v tests/test_cart_page.py
pytest -v

pytest -v tests/test_checkout_page.py
pytest -m e2e -v
pytest -v
```

## Portfolio Promotion Workflow

Portfolio promotion is used when a completed and validated project state should become the stable public version on `main`.

Recommended portfolio promotion workflow:

1. Ensure `develop` contains the completed and validated project state.
2. Complete required documentation cleanup on `develop` or a dedicated documentation branch.
3. Verify that README and technical documentation describe the implemented state accurately.
4. Verify that planned future work is not described as already implemented.
5. Verify runtime configuration, reporting, CI, and execution documentation against current implementation.
6. Run local validation when possible.
7. Open a Pull Request from `develop` to `main`.
8. Wait for CI validation.
9. Review the diff from a recruiter or technical reviewer perspective.
10. Squash merge into `main` after validation.
11. Update local `main` and `develop`.
12. Continue future work from `develop`.

Portfolio promotion should not introduce unrelated new implementation scope.

It should promote a stable, already validated snapshot.

The exact promotion title and description should reflect the phase or portfolio state being promoted rather than reusing an old phase-specific template automatically.

## CI Integration

GitHub Actions validates changes on:

* push to `main`
* push to `develop`
* Pull Requests targeting `main`
* Pull Requests targeting `develop`
* manual workflow execution through `workflow_dispatch`

Regular pushes to feature, refactor, fix, or documentation branches do not automatically start the workflow unless a Pull Request targets `main` or `develop`, or the workflow is started manually.

A manual `workflow_dispatch` execution may be used to validate a workstream branch before its final Pull Request when required by the active task or workstream.

### Current CI Structure

The current GitHub Actions workflow preserves the four-job structure introduced in Phase 4B:

```text
quality
├── smoke
├── regression
└── full-suite
```

The `quality` job executes first.

After it succeeds, the following browser-test jobs become independently executable:

* `smoke`
* `regression`
* `full-suite`

These three jobs do not depend on each other.

GitHub Actions may therefore schedule them concurrently when runners are available.

Phase 4C adds pytest-xdist worker-level parallelism inside the existing browser-test jobs.

Phase 4D adds Allure reporting inside the existing `full-suite` job without adding a new browser job.

Phase 4E adds explicit runtime defaults to the three existing browser-test jobs without changing the workflow topology.

### CI Runtime Defaults

Smoke, Regression, and full-suite use:

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

These values intentionally match the approved local defaults.

The quality job does not require browser runtime configuration.

The browser-test CI strategy therefore remains:

* Chromium-only
* headless
* pytest-xdist parallel
* screenshot-on-failure enabled
* tracing disabled by default
* video disabled by default

Phase 4E does not introduce:

* browser matrices
* Firefox installation
* WebKit installation
* retries
* `continue-on-error`
* default trace retention
* default video retention
* secrets for non-secret runtime values

### GitHub Actions Concurrency And Pytest Parallelism

Two separate concurrency layers are currently used.

GitHub Actions job-level scheduling:

```text
quality
├── smoke
├── regression
└── full-suite
```

After `quality`, the three browser-test jobs may run at the same time.

Inside each browser-test job, pytest-xdist distributes tests across worker processes.

Conceptually:

```text
quality
├── smoke
│   └── xdist workers
├── regression
│   └── xdist workers
└── full-suite
    └── xdist workers
```

GitHub Actions job concurrency and pytest-xdist worker parallelism are separate mechanisms and should not be treated as interchangeable.

Reporting and runtime configuration do not change either concurrency layer.

### Quality Job

The `quality` job validates:

* dependency installation
* Ruff linting
* Black formatting
* isort import sorting

Current commands:

```bash
ruff check .
black --check .
isort . --check-only
```

The quality job does not install Playwright Chromium.

It does not execute browser tests and does not use pytest-xdist.

It does not generate browser-test reports.

It does not require the Phase 4E browser runtime environment variables.

A failure in the quality job prevents Smoke, Regression, and full-suite browser execution.

### Smoke Job

The dedicated Smoke CI job executes the approved Smoke marker suite through pytest-xdist.

Core command:

```bash
pytest -m smoke -n auto -v
```

The actual CI command is:

```bash
pytest -m smoke -n auto -v \
  --html=reports/smoke-report.html \
  --self-contained-html
```

The Smoke job:

* installs Chromium
* uses the explicit Phase 4E CI runtime defaults
* generates pytest-html reporting
* uploads Smoke-specific artifacts

It does not generate Allure results or an Allure HTML report.

Trace and video remain disabled by default.

### Regression Job

The dedicated Regression CI job executes the approved Regression marker suite through pytest-xdist.

Core command:

```bash
pytest -m regression -n auto -v
```

The actual CI command is:

```bash
pytest -m regression -n auto -v \
  --html=reports/regression-report.html \
  --self-contained-html
```

The Regression job:

* installs Chromium
* uses the explicit Phase 4E CI runtime defaults
* generates pytest-html reporting
* uploads Regression-specific artifacts

It does not generate Allure results or an Allure HTML report.

Trace and video remain disabled by default.

### Full-Suite Job

The full-suite job remains the complete CI regression gate and the primary CI source for advanced Allure reporting.

Its test execution is intentionally not filtered by markers.

The actual CI command is:

```bash
pytest -n auto -v \
  --html=reports/report.html \
  --self-contained-html \
  --alluredir=reports/allure-results \
  --clean-alluredir
```

This execution generates:

```text
reports/report.html
reports/allure-results/
```

The workflow then attempts to generate:

```text
reports/allure-report/
```

with:

```bash
allure generate reports/allure-results \
  --clean \
  -o reports/allure-report
```

Allure HTML generation is attempted after the test step when usable Allure result data exists.

The full-suite job uses the same explicit Phase 4E runtime defaults as Smoke and Regression.

The dedicated Smoke and Regression jobs supplement the complete full-suite gate rather than replacing it.

### Allure CLI Setup In CI

The `full-suite` job configures Java 17 through:

```yaml
actions/setup-java@v4
```

with:

```yaml
distribution: temurin
java-version: "17"
```

It then installs the Allure command-line tool:

```bash
npm install -g allure-commandline
allure --version
```

This setup is limited to the full-suite job because Smoke and Regression do not generate Allure HTML reports.

### Browser Setup

Playwright Chromium is installed only in:

* `smoke`
* `regression`
* `full-suite`

Current browser installation command:

```bash
playwright install --with-deps chromium
```

The `quality` job does not require browser installation.

The runtime configuration layer recognizes:

```text
chromium
firefox
webkit
```

but current CI installation and validation remain Chromium-only.

The current execution, reporting, and runtime strategy does not introduce:

* Firefox CI execution
* WebKit CI execution
* cross-browser matrices
* cross-browser parallel execution

### CI Marker Responsibility

Dedicated CI jobs currently exist for:

* Smoke
* Regression

Dedicated CI jobs do not currently exist for:

* UI
* Security
* Sorting
* Navigation
* E2E

These marker suites remain available for selective local execution.

Their tests still participate in full-suite CI execution as part of the normal collected test suite.

Because the full-suite job uses pytest-xdist, those tests may be distributed across workers during complete CI execution.

Because full-suite collects Allure results, they are also included in the advanced full-suite reporting data.

### Reports And Artifacts

Current reporting and diagnostic mechanisms are:

* pytest-html
* Allure
* configurable failure screenshots
* optional Playwright trace
* optional Playwright video
* GitHub Actions artifacts

Smoke artifacts:

```text
smoke-pytest-html-report
smoke-test-artifacts
```

Regression artifacts:

```text
regression-pytest-html-report
regression-test-artifacts
```

Full-suite artifacts:

```text
pytest-html-report
full-suite-allure-report
test-artifacts
```

The dedicated full-suite Allure artifact uses:

```text
reports/allure-report/
```

The broader existing full-suite artifact continues to upload:

```text
reports/
```

Artifact upload steps use `if: always()` so available reports and runtime outputs can still be uploaded when a browser-test command fails.

The Allure report-generation step also uses failure-tolerant workflow execution and checks for usable result data before generating the report.

Current artifact retention remains seven days.

Trace and video are disabled in CI by default and are therefore not introduced as default retained artifacts.

Detailed artifact paths, retention, runtime defaults, and job behavior are documented in [CI/CD Pipeline](ci-cd-pipeline.md).

### CI Failure Behavior

A Pull Request should not be merged if required CI validation fails.

Current quality-gate behavior includes:

* Ruff failure fails CI
* Black failure fails CI
* isort failure fails CI
* failed `quality` prevents browser jobs from starting
* Smoke failure fails the Smoke job
* Regression failure fails the Regression job
* full-suite failure fails the full-suite job
* invalid Phase 4E runtime configuration fails before normal browser execution proceeds

The workflow does not convert required test or quality failures into successful results.

pytest-xdist does not change the failure policy.

Allure reporting does not change the failure policy.

Runtime configuration does not change the failure policy.

A failing test executed by an xdist worker causes the corresponding Pytest command and browser job to fail.

Available reports, screenshots, and artifacts may still be produced for failure analysis according to their configured policies.

## Current Execution Scope

The current implementation combines:

* Phase 4B CI Execution Strategy
* Phase 4C Parallel Execution Strategy
* Phase 4D Reporting Strategy
* Phase 4E Runtime Configuration Strategy

Phase 4B established:

* the `quality` prerequisite
* dedicated Smoke execution
* dedicated Regression execution
* complete full-suite execution
* job-level concurrency after successful quality validation
* job-specific reports and artifacts

Phase 4C added:

* validated local pytest-xdist execution
* parallel Smoke execution
* parallel Regression execution
* parallel full-suite execution
* xdist integration into the existing three browser-test CI jobs
* continued support for sequential local execution
* validation of test and fixture independence
* preservation of existing pytest-html and artifact behavior

Phase 4D added:

* local Allure result collection
* local Allure HTML report generation
* failure screenshot attachments in Allure
* sequential and parallel reporting compatibility
* full-suite Allure result collection in CI
* full-suite Allure HTML generation in CI
* dedicated `full-suite-allure-report` artifact
* preservation of existing pytest-html reports and artifacts

Phase 4E added:

* centralized runtime configuration
* configurable application base URL
* browser selection
* headed/headless execution configuration
* configurable Playwright action and navigation timeout
* configurable Playwright assertion timeout
* configurable screenshot policy
* configurable trace policy
* configurable video policy
* validation and normalization of environment-variable values
* fail-fast invalid configuration handling
* integration with the existing pytest-playwright fixture model
* explicit browser-test CI runtime defaults
* preserved Chromium-only CI execution
* preserved Phase 4B–4D topology and reporting behavior

The current implementation does not include:

* report hosting
* GitHub Pages reporting
* Allure history persistence
* trend-history storage
* retries
* named environment profiles
* automatic `.env` loading
* device emulation
* browser matrices
* cross-browser CI execution
* Phase 4F logging redesign
* Phase 4F fixture cleanup

## Generated Runtime Output Policy

Generated reports and execution evidence are runtime outputs.

Current generated paths include:

```text
reports/
reports/screenshots/
reports/allure-results/
reports/allure-report/
test-results/
playwright-report/
```

These files are used for:

* local debugging
* failure analysis
* execution evidence
* CI artifact publishing where configured

They should not be committed to Git.

The current ignore policy covers generated reporting and pytest-playwright artifact locations.

Repository content should contain implementation, configuration, test assets, and documentation.

Generated execution output should remain outside version-controlled project content.

## Merge Strategy

The project uses:

```text
Squash and merge
```

Squash merge combines all commits from a branch into one clean commit on the target branch.

This keeps `develop` and `main` history readable.

Example final squash commit:

```text
test(AQA-0064): complete cart automation workstream
```

For checkpoint-only or documentation-heavy stabilization tasks, a `chore` or `docs` squash commit may also be appropriate:

```text
chore(AQA-0064): review and stabilize cart workstream
docs(AQA-0064): update project documentation after cart workstream
chore(AQA-0073): finalize phase 3c structure cleanup
chore(AQA-0082): finalize checkout automation workstream
docs(AQA-0104): document phase 4e runtime configuration
```

For portfolio promotion into `main`, a `chore` squash commit may be appropriate.

The exact message should describe the phase or snapshot being promoted.

## Post-Merge Workflow

### After Merge Into `develop`

After a Pull Request is merged into `develop`, update local `develop`:

```bash
git checkout develop
git pull origin develop
```

Check recent commits:

```bash
git log --oneline --decorate -5
```

Optionally delete the completed local source branch:

```bash
git branch -d <source-branch>
```

Clean deleted remote branch references:

```bash
git fetch --prune
```

Run final validation if needed:

```bash
pytest -v
```

### After Promotion Into `main`

After a Pull Request is merged into `main`, update local branches:

```bash
git checkout main
git pull origin main
git checkout develop
git pull origin develop
git fetch --prune
```

Check recent commits on `main`:

```bash
git checkout main
git log --oneline --decorate -5
```

Future implementation, documentation, refactor, and framework maturity work should continue from `develop`.

## Phase And Workstream Checkpoint Workflow

Before moving to the next major project phase or before merging a completed workstream when required by the roadmap, a checkpoint task must be completed.

A checkpoint verifies:

* completed scope
* test coverage
* local validation
* relevant scoped test execution
* relevant marker suite execution where applicable
* runtime configuration status where applicable
* parallel validation where required by the active workstream
* reporting validation where required by the active workstream
* full test suite execution or accepted scoped validation
* CI status
* expected reports and artifacts
* documentation status
* Git status
* cleanup needs
* generated files and ignored artifacts
* readiness for the next phase or merge

Example checkpoints:

```text
AQA-0041 — Review Phase 2 And Prepare Phase 3 Scope
AQA-0064 — Review And Stabilize Cart Workstream
AQA-0073 — Phase 3C Final Validation And Documentation Sync
AQA-0082 — Checkout Workstream Final Validation And Documentation Sync
```

No new major workstream should start before the relevant checkpoint is completed when the roadmap requires that checkpoint.

For portfolio promotion, the checkpoint should also verify that the project is suitable for public presentation through `main`.

## Documentation Updates

Documentation should be updated when changes affect:

* framework architecture
* project structure
* testing strategy
* marker strategy
* test execution strategy
* runtime configuration strategy
* reporting strategy
* CI/CD workflow
* quality tooling
* roadmap
* feature list
* technology stack
* test case coverage
* README instructions

Documentation changes may be committed as part of the relevant task or as a separate documentation cleanup or stabilization task.

For automation work that implements a documented manual test case, update the related test case metadata in the same task when required.

General documentation synchronization may be deferred to an approved review, stabilization, or checkpoint task when that is the defined workstream workflow.

For workstream final validation tasks, documentation should be checked for stale future-facing wording describing already implemented capabilities as planned.

### Marker Documentation Changes

When pytest marker behavior changes, verify that:

* `pytest.ini` reflects the intended executable markers
* automated test usage matches the registered marker definitions
* test case metadata matches automated marker usage
* `docs/testing-strategy.md` describes the current marker semantics
* workflow and README commands do not reference removed markers

### Parallel Execution Documentation Changes

When parallel execution behavior changes, verify that:

* `pytest-xdist` dependency status is described accurately
* sequential execution remains documented where supported
* approved parallel commands match actual execution
* fixture and test independence assumptions remain accurate
* parametrized and E2E tests do not rely on execution order
* reporting and screenshot behavior remains compatible with worker-level execution
* runtime configuration remains compatible with supported parallel execution
* no unvalidated sequential-only exception is documented as fact

### Runtime Configuration Documentation Changes

When runtime configuration behavior changes, verify that:

* `config/settings.py` remains the source of truth for supported project environment variables and defaults
* `conftest.py` integration is documented accurately
* `BasePage` URL composition matches actual implementation
* accepted browser values are documented accurately
* headed boolean values are documented accurately
* timeout defaults and units are documented accurately
* screenshot policy values match implementation
* trace and video policy values match implementation
* invalid explicit configuration is documented as fail-fast behavior
* native pytest-playwright option precedence is documented where implemented
* local configuration behavior is separated from CI browser installation scope
* Chromium-only CI is stated clearly
* `.env` loading is not documented unless implemented
* named environment profiles are not documented unless implemented
* browser matrices are not documented unless implemented
* Phase 4F diagnostics and fixture cleanup are not described as Phase 4E functionality

### Reporting Documentation Changes

When reporting behavior changes, verify that:

* pytest-html responsibilities remain accurate
* Allure result and HTML output locations match implementation
* local Allure commands match current behavior
* Allure CLI is described as a separate HTML-generation prerequisite
* failure screenshot behavior matches `conftest.py`
* screenshot attachments reuse the existing captured file
* screenshot policy behavior is documented accurately
* trace and video runtime output is distinguished from project screenshot and report output
* sequential and parallel reporting compatibility is described accurately
* generated outputs are clearly distinguished from repository content
* unsupported capabilities such as Allure history, hosting, GitHub Pages, retries, and cross-browser reporting are not described as implemented

### CI Documentation Changes

When CI execution behavior changes, verify that:

* `.github/workflows/ci.yml` remains the implementation source of truth
* `docs/ci-cd-pipeline.md` reflects current jobs, dependencies, reports, artifacts, triggers, runtime defaults, and parallel commands
* `docs/workflow.md` reflects current local and CI responsibilities
* README remains a useful high-level entry point
* marker suites executed in dedicated CI jobs are distinguished from locally selective marker suites
* GitHub Actions job concurrency is distinguished from pytest-xdist worker parallelism
* Smoke and Regression remain pytest-html-focused unless implementation explicitly changes
* full-suite Allure artifact naming and output locations match the workflow
* browser-test jobs document their explicit Phase 4E defaults
* Chromium-only installation remains clear
* future capabilities are not described as already implemented

### Portfolio Promotion Documentation Review

For portfolio promotion, documentation should also be checked for:

* stale workstream-finalization wording
* stale PR-readiness wording
* statements that suggest completed work exists only on an obsolete branch
* implemented features mixed with planned future extensions
* missing distinction between `main` as the stable portfolio branch and `develop` as the integration branch
* stale statements describing implemented runtime configuration as future work

## Current Workflow Status

The current workflow supports completed Phase 3 page-level automation coverage for Login, Inventory, Product Details, Cart, and Checkout areas.

Phase 3 page-level automation coverage has been completed, reviewed, validated, squash-merged into `develop`, and promoted to `main` as the stable Phase 3 portfolio snapshot.

Phase 4A established the current executable Pytest marker strategy.

Phase 4B CI Execution Strategy is implemented with:

* a dedicated `quality` job
* dedicated Smoke CI execution
* dedicated Regression CI execution
* a complete unfiltered `full-suite` job
* quality-gate dependencies before browser execution
* separate pytest-html reports and artifacts for browser-test jobs

Phase 4C Parallel Execution Strategy is implemented with:

* validated local pytest-xdist execution
* supported sequential execution
* parallel Smoke execution
* parallel Regression execution
* parallel complete full-suite execution
* worker-level test distribution through `-n auto`
* validated fixture and test independence
* pytest-xdist execution inside the existing Smoke, Regression, and full-suite CI jobs
* preserved Phase 4B job structure
* preserved pytest-html reports and artifact behavior
* current Chromium-only CI browser scope

No sequential-only test exceptions were identified during Phase 4C validation.

Phase 4D Reporting Strategy is implemented with:

* local Allure result collection
* local Allure HTML report generation
* Allure CLI report-generation workflow
* failure screenshot attachments in Allure
* reuse of the existing failure screenshot mechanism
* compatibility with sequential execution
* compatibility with pytest-xdist parallel execution
* full-suite Allure result collection in GitHub Actions
* full-suite Allure HTML generation in GitHub Actions
* dedicated `full-suite-allure-report` artifact
* preserved Smoke and Regression pytest-html reporting
* preserved existing browser-test artifact behavior

Phase 4E Runtime Configuration was completed through AQA-0100–AQA-0105 and includes:

* centralized runtime settings in `config/settings.py`
* configurable application base URL
* configurable browser selection
* configurable headed/headless execution
* configurable action and navigation timeout
* configurable assertion timeout
* configurable failure screenshot policy
* configurable trace policy
* configurable video policy
* environment-variable normalization and validation
* fail-fast invalid explicit configuration
* runtime integration through `BasePage` and `conftest.py`
* preservation of pytest-playwright native runtime behavior
* explicit runtime defaults in Smoke, Regression, and full-suite CI jobs
* Chromium-only CI execution
* preservation of the existing Phase 4B–4D execution, parallelization, reporting, and artifact architecture
* final runtime-configuration validation
* sequential and pytest-xdist parallel suite validation
* controlled screenshot, trace, and video policy validation
* pytest-html and Allure reporting validation
* successful GitHub Actions validation
* Phase 4E documentation and roadmap synchronization

Phase 4E is completed. Phase 4F Diagnostics And Fixture Cleanup remains planned.

The `main` branch represents the polished portfolio version of the project.

The `develop` branch remains the integration branch and may contain newer work after this document is read from `main`.

Future framework maturity work should continue from `develop` unless a specific portfolio promotion or release task targets `main`.

The current framework does not yet implement:

* named environment profiles
* automatic `.env` loading
* browser matrices
* cross-browser CI
* device emulation
* retries
* Phase 4F logging improvements
* Phase 4F fixture cleanup
* Allure history persistence
* hosted reporting
* GitHub Pages reporting