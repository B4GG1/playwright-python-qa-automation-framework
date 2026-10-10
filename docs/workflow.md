# Development Workflow

This document describes the day-to-day development workflow used in this project.

For detailed branching rules, see: [Git Branching Strategy](git-branching-strategy.md).

For detailed test categorization, pytest marker semantics, sequential/parallel execution strategy, runtime configuration, diagnostics, fixture responsibility, reporting behavior, and cross-browser execution strategy, see: [Testing Strategy](testing-strategy.md).

For detailed GitHub Actions execution, job dependencies, parallel browser-test execution, cross-browser Smoke validation, runtime defaults, reports, and artifacts, see: [CI/CD Pipeline](ci-cd-pipeline.md).

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

Workstream workflow:

```text
develop
  ↓
shared workstream branch
  ↓
multiple related task commits
  ↓
task-level validation
  ↓
workstream documentation sync
  ↓
final workstream checkpoint
  ↓
Pull Request to develop
  ↓
CI validation
  ↓
Squash merge
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
refactor/diagnostics-fixture-cleanup
feature/playwright-cross-browser-validation
```

In this workflow:

1. Create one branch for the whole workstream.
2. Implement multiple related tasks on the same branch.
3. Create separate commits for individual tasks.
4. Push regularly as backup.
5. Run local validation after meaningful changes.
6. Review scope, tests, documentation, diagnostics, reporting behavior, runtime configuration, fixture responsibility, browser execution, and cleanup during the workstream.
7. Complete the final workstream checkpoint.
8. Open or finalize the workstream Pull Request only when the complete approved workstream scope is ready.
9. Validate CI.
10. Squash merge the complete workstream into `develop`.

This approach is used for complete functional automation, refactor, documentation sync, reporting, runtime configuration, diagnostics, fixture cleanup, cross-browser validation, and stabilization workstreams.

It is useful when tasks are connected and reviewing them together makes more sense than creating many small Pull Requests.

A task-level commit and push on a shared workstream branch does not imply that the workstream should be merged immediately.

A temporary Pull Request may be used for CI validation during a workstream when useful, but the workstream branch can remain unmerged until the approved closing checkpoint is complete.

The final merge belongs to the complete workstream rather than an individual intermediate task when the active roadmap defines a shared workstream branch.

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
git checkout -b feature/playwright-cross-browser-validation
git checkout -b refactor/runtime-configuration
git checkout -b refactor/diagnostics-fixture-cleanup
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

Phase 4F diagnostics operate automatically through the normal Pytest execution path.

Phase 5A additionally supports representative Firefox and WebKit Smoke validation through the same functional suite.

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
* controlled failure validation
* situations where parallel execution is not required
* controlled runtime configuration validation
* diagnostic hook validation

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

Approved primary Chromium parallel validation commands:

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
* compatible with Phase 4F diagnostics
* browser-neutral unless a genuine compatibility limitation is demonstrated

Phase 4F preserves the existing worker-safe execution model.

The runtime summary is not duplicated by individual xdist workers.

Application scenario fixtures remain independent and function-scoped.

No sequential-only test exception is required for the current implementation.

### Cross-Browser Smoke Validation

Phase 5A extends local validation with representative Smoke execution on Firefox and WebKit.

Approved commands:

```bash
QA_BROWSER=firefox pytest -m smoke -n auto -v
QA_BROWSER=webkit pytest -m smoke -n auto -v
```

The selected Playwright browser must be installed locally.

For example:

```bash
playwright install --with-deps firefox webkit
```

Current browser responsibilities are:

```text
Chromium
├── Smoke
├── Regression
└── complete full suite

Firefox
└── representative Smoke

WebKit
└── representative Smoke
```

Cross-browser validation reuses:

* the existing `smoke` marker
* the existing functional test modules
* the existing Page Objects
* the existing application fixtures
* the existing reusable assertions
* centralized runtime configuration
* Phase 4F diagnostics
* pytest-xdist execution

It does not require:

* a new cross-browser marker
* browser-specific duplicate test modules
* browser-specific duplicate fixtures
* browser-specific duplicate Page Objects

Complete Firefox or WebKit Regression/full-suite execution is not part of the current workflow.

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

Phase 4F does not introduce additional runtime environment variables.

Phase 5A reuses `QA_BROWSER` rather than adding another browser-selection mechanism.

### Base URL Override

Example:

```bash
QA_BASE_URL="http://localhost:8000" pytest -m smoke -v
```

Page Objects continue to use their normal relative routes.

The configured application origin is composed through `BasePage`.

The effective application origin is also visible in the Phase 4F runtime summary.

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

Current execution responsibilities are:

* Chromium — Smoke, Regression, and complete full suite
* Firefox — representative Smoke
* WebKit — representative Smoke

Explicit native pytest-playwright browser options remain usable.

For example:

```bash
QA_BROWSER=firefox pytest -m smoke -v --browser chromium
```

uses the explicitly supplied native browser option.

The effective browser selection is shown by the runtime diagnostic header.

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

The effective mode is shown as `headed` or `headless` in the runtime diagnostic header.

Current CI execution remains headless across Chromium, Firefox, and WebKit.

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

The effective timeout values are shown in the Phase 4F runtime summary.

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

The effective execution configuration is visible through the runtime header.

### Focused Runtime Configuration Validation

Focused configuration validation uses:

```bash
pytest tests/test_runtime_config.py
```

This verifies:

* defaults
* accepted values
* browser normalization
* Chromium, Firefox, and WebKit browser values
* boolean parsing
* timeout parsing
* artifact policy parsing
* invalid configuration behavior

Invalid explicit configuration should fail early rather than silently falling back to a default.

## Phase 4F Diagnostics Workflow

Phase 4F provides lightweight runtime and failed-test diagnostics through:

```text
framework/diagnostics.py
```

and framework-level Pytest integration in:

```text
conftest.py
```

Diagnostics operate automatically during normal Pytest execution.

They do not require a separate command.

The same diagnostic model applies to Chromium, Firefox, and WebKit execution.

### Runtime Diagnostic Header

The runtime summary is emitted through:

```text
pytest_report_header
```

It shows:

```text
base_url
browser
mode
action/navigation timeout
assertion timeout
screenshot policy
trace policy
video policy
```

Representative output:

```text
[runtime] base_url=... | browser=... | mode=... | action_navigation_timeout_ms=... | assertion_timeout_ms=... | screenshot=... | trace=... | video=...
```

During pytest-xdist execution, workers do not emit duplicate runtime summaries.

The controlling Pytest process provides the execution-level runtime context.

### Failed-Test Diagnostics

Failed Pytest reports receive diagnostic context for:

```text
setup
call
teardown
```

Each failed-test summary includes:

* Pytest node ID
* failure phase

When a Playwright page is available, diagnostics also attempt to include:

* current page URL

When the custom project screenshot is successfully created, diagnostics also include:

* screenshot path

Representative output:

```text
[failure] test=<node-id> | phase=<phase> | url=<current-url> | screenshot=<path>
```

URL and screenshot fields are included only when available.

### Diagnostic Errors

Errors that occur while collecting diagnostic evidence are surfaced instead of being silently ignored.

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

Diagnostic errors are emitted through the project diagnostics logger and added to the failed Pytest report diagnostic sections.

Phase 4F does not create persistent project log files.

### Controlled Diagnostic Validation

When diagnostics behavior changes, use a controlled failing scenario to validate the affected behavior.

Relevant validation may include:

* runtime summary visibility
* effective runtime values
* effective browser value
* xdist runtime-header de-duplication
* Pytest node ID
* failure phase
* current URL
* screenshot path
* diagnostic-error output

A failed `call` phase should be used when validating the custom screenshot path.

Intentionally failing tests created only for diagnostics validation must remain temporary and must not be committed.

## Fixture Responsibility Workflow

Phase 4F separates framework-level Pytest integration from application scenario fixtures.

Framework-level Pytest responsibilities remain in:

```text
conftest.py
```

They include:

* runtime configuration integration
* browser integration
* runtime diagnostic header
* BrowserContext timeout configuration
* failed-test diagnostics
* custom failure screenshot handling
* Allure failure screenshot integration

Application scenario fixtures are located in:

```text
tests/conftest.py
```

Current scenario fixtures are:

```text
opened_login_page
standard_user
logged_in_inventory_page
inventory_page_with_one_product_in_cart
cart_page_with_one_product
checkout_step_one_page_with_one_product
checkout_step_two_page_with_one_product
checkout_last_step_page_with_one_product
```

When adding or changing fixtures:

* keep application scenario setup in `tests/conftest.py`
* keep framework-level hooks and runtime integration in the root `conftest.py`
* preserve independent scenario state
* avoid introducing shared mutable browser state
* preserve compatibility with sequential and pytest-xdist execution
* preserve compatibility with the supported browser engines
* prefer explicit scenario-oriented names
* add fixtures only when repeated setup justifies them

The current fixture strategy does not use:

* generic fixture factories
* dependency-injection layers
* autouse redesign
* multi-layer fixture packages
* fixture scope redesign
* browser-specific fixture packages

Firefox and WebKit reuse the same scenario fixtures as Chromium.

## Reporting Validation

Phase 4D introduced Allure reporting while preserving pytest-html and the existing failure screenshot mechanism.

Phase 4E adds configurable screenshot, trace, and video policies without replacing the existing reporting architecture.

Phase 4F adds runtime and failed-test diagnostic context without creating another reporting pipeline.

Phase 5A adds browser-specific pytest-html output for Firefox and WebKit Smoke while preserving Chromium full-suite Allure responsibility.

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

For combined pytest-html and Allure Chromium full-suite validation:

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

Allure reporting complements pytest-html and Phase 4F diagnostics rather than replacing them.

Firefox and WebKit Smoke currently remain pytest-html-focused and do not generate dedicated Allure reports in CI.

## Failure Evidence And Runtime Artifacts

### Failure Screenshots

The default screenshot policy is:

```text
QA_SCREENSHOT_POLICY=only-on-failure
```

Failed browser tests during the Pytest `call` phase use the existing custom screenshot mechanism when a Playwright page is available.

Failure screenshots are stored under:

```text
reports/screenshots/
```

When screenshot capture succeeds:

* the screenshot remains available under `reports/screenshots/`
* its path is included in the Phase 4F failed-test diagnostic summary
* when Allure result collection is active, the same PNG is attached as `Failure screenshot`

The Allure integration does not introduce a second screenshot capture mechanism.

The existing screenshot file is reused.

To disable the custom failure screenshot:

```bash
QA_SCREENSHOT_POLICY=off pytest -m smoke -v
```

When screenshot policy is disabled:

* no custom failure PNG is written
* no corresponding Allure `Failure screenshot` attachment is created
* failed-test diagnostics still identify the test and failure phase

The screenshot hook applies only to failures during the Pytest `call` phase.

Setup and teardown failures receive Phase 4F failure diagnostics but do not use the custom screenshot path.

If screenshot capture fails:

* the error is reported through the Phase 4F diagnostic mechanism
* no screenshot path is included
* no Allure screenshot attachment is attempted

If Allure attachment fails after successful screenshot creation:

* the screenshot remains available
* the screenshot path remains in failure diagnostics
* the attachment error is reported through the Phase 4F diagnostic mechanism

The same screenshot mechanism applies to Firefox and WebKit Smoke execution.

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

Phase 4F and Phase 5A do not change trace lifecycle ownership.

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

Phase 4F and Phase 5A do not change video lifecycle ownership.

### Runtime Artifact Cleanup

Generated reports and persistent browser diagnostic files are runtime outputs.

They should not be committed.

Relevant generated locations include:

```text
reports/
test-results/
allure-results/
allure-report/
playwright-report/
```

Phase 4F runtime summaries and failed-test summaries do not add a persistent diagnostic directory.

Persistent project log files are not implemented.

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

Smoke and Regression additionally have approved Chromium parallel forms:

```bash
pytest -m smoke -n auto -v
pytest -m regression -n auto -v
```

The Smoke suite additionally has representative Firefox and WebKit forms:

```bash
QA_BROWSER=firefox pytest -m smoke -n auto -v
QA_BROWSER=webkit pytest -m smoke -n auto -v
```

The existing CI pipeline executes dedicated Chromium Smoke and Regression jobs.

The Phase 5A matrix additionally executes the same Smoke suite on:

* Firefox
* WebKit

The following markers do not currently have dedicated CI jobs:

* `ui`
* `security`
* `sorting`
* `navigation`
* `e2e`

Tests carrying these markers are still included in the complete unfiltered Chromium full-suite CI execution.

Tests that also carry `smoke` additionally participate in representative Firefox and WebKit compatibility validation.

Because the Chromium full-suite CI job uses pytest-xdist, tests may execute on different workers as part of the complete collected suite.

Because the Chromium full-suite also collects Allure result data, those tests are represented in the advanced full-suite report as part of the complete execution.

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

Smoke-tagged E2E checkpoints may additionally execute in Firefox and WebKit Smoke validation.

Runtime overrides and Phase 4F diagnostics apply to marker-based execution without changing marker semantics.

Phase 5A does not introduce a cross-browser marker.

Browser selection remains an execution concern rather than a marker dimension.

Detailed marker meanings, test-independence expectations, execution rules, runtime behavior, diagnostic behavior, reporting behavior, and browser responsibilities are documented in [Testing Strategy](testing-strategy.md).

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

When execution behavior, fixture responsibility, fixture isolation, worker safety, or xdist-compatible diagnostics are part of the changed scope, parallel validation should additionally be used:

```bash
pytest -m smoke -n auto -v
pytest -m regression -n auto -v
pytest -n auto -v
```

When representative browser compatibility behavior is part of the changed scope, validate:

```bash
QA_BROWSER=firefox pytest -m smoke -n auto -v
QA_BROWSER=webkit pytest -m smoke -n auto -v
```

When runtime configuration behavior changes, validate:

```bash
pytest tests/test_runtime_config.py
```

and representative runtime overrides as required by the task.

When diagnostics behavior changes, run controlled failure validation appropriate to the changed diagnostic path.

When reporting behavior is part of the changed scope, validate the relevant report generation and runtime outputs in addition to the underlying tests.

When screenshot, trace, or video policy behavior changes, controlled artifact validation may be used.

Intentionally failing tests used only for runtime or diagnostic validation should remain temporary and should not be committed.

The full Chromium test suite should still pass before a workstream is considered ready for merge unless a scoped validation exception is explicitly accepted.

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
git commit -m "docs(AQA-0098): document reporting upgrade"
git commit -m "refactor(AQA-0100): centralize runtime configuration"
git commit -m "docs(AQA-0104): document phase 4e runtime configuration"
git commit -m "chore(AQA-0105): finalize runtime configuration workstream"
git commit -m "refactor(AQA-0106): add runtime diagnostics"
git commit -m "refactor(AQA-0107): add failed-test diagnostics"
git commit -m "refactor(AQA-0108): separate scenario fixtures from framework hooks"
git commit -m "docs(AQA-0109): document phase 4f diagnostics and fixture strategy"
git commit -m "ci(AQA-0112): add playwright cross-browser smoke validation"
git commit -m "docs(AQA-0113): document phase 5a cross-browser strategy"
```

Use the Conventional Commit type that best describes the actual change.

Common types include:

```text
feat
fix
test
refactor
docs
ci
chore
```

## Task Completion Workflow

Before considering an implementation task complete, verify:

* approved scope is implemented
* relevant tests pass
* required quality tools pass
* affected documentation is updated
* test case metadata is updated when functional test coverage changed
* generated runtime outputs are not unintentionally tracked
* changes are committed
* changes are pushed when required by the task workflow
* working tree status is verified

A task should not be marked complete only because the implementation appears to work locally.

The validation expected for the task must also be satisfied.

For framework infrastructure such as Phase 4F diagnostics, controlled negative-path validation may be required in addition to passing positive suites.

For execution-only work such as Phase 5A browser expansion, existing test case automation metadata does not need to change when no new functional coverage is introduced.

## Workstream Checkpoint Validation

A workstream checkpoint should verify the complete workstream rather than only the last implementation task.

Typical validation includes:

```bash
ruff check .
black --check .
isort . --check-only
pytest -v
```

When parallel behavior is part of the workstream:

```bash
pytest -m smoke -n auto -v
pytest -m regression -n auto -v
pytest -n auto -v
```

When cross-browser compatibility is part of the workstream:

```bash
QA_BROWSER=firefox pytest -m smoke -n auto -v
QA_BROWSER=webkit pytest -m smoke -n auto -v
```

When reporting behavior is part of the workstream:

```bash
pytest -n auto -v \
  --html=reports/report.html \
  --self-contained-html \
  --alluredir=reports/allure-results \
  --clean-alluredir
```

Then:

```bash
allure generate reports/allure-results \
  --clean \
  -o reports/allure-report
```

When diagnostics behavior is part of the workstream, controlled failures should additionally confirm the required diagnostic context.

For a workstream checkpoint, also run the relevant scoped test module and marker suites where useful.

Examples:

```bash
pytest -v tests/test_cart_page.py
pytest -v

pytest -v tests/test_checkout_page.py
pytest -m e2e -v
pytest -v
```

A closing checkpoint should also verify:

* the final branch state
* CI results
* expected browser-specific reports and artifacts when applicable
* documentation consistency
* working tree cleanliness
* readiness to merge the shared workstream

## Portfolio Promotion Workflow

Portfolio promotion is used when a completed and validated project state should become the stable public version on `main`.

Recommended portfolio promotion workflow:

1. Ensure `develop` contains the completed and validated project state.
2. Complete required documentation cleanup on `develop` or a dedicated documentation branch.
3. Verify that README and technical documentation describe the implemented state accurately.
4. Verify that planned future work is not described as already implemented.
5. Verify runtime configuration, diagnostics, fixture responsibility, reporting, CI, cross-browser execution, and execution documentation against current implementation.
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

A temporary Pull Request may also be used to obtain pull-request CI validation without requiring an immediate merge of the workstream.

### Current CI Structure

The current GitHub Actions workflow extends the Phase 4B Chromium topology with the Phase 5A Firefox/WebKit Smoke matrix:

```text
quality
├── smoke [Chromium]
├── regression [Chromium]
├── full-suite [Chromium]
└── cross-browser-smoke
    ├── Firefox
    └── WebKit
```

The `quality` job executes first.

After it succeeds, the following browser-test executions become independently executable:

* Chromium `smoke`
* Chromium `regression`
* Chromium `full-suite`
* `cross-browser-smoke (firefox)`
* `cross-browser-smoke (webkit)`

All current browser-test jobs use:

```yaml
needs: quality
```

The Chromium Smoke, Regression, and full-suite jobs do not depend on each other.

The Firefox and WebKit executions are expanded from one matrix job.

The matrix uses:

```yaml
fail-fast: false
```

so one additional-browser failure does not automatically cancel the other matrix entry.

GitHub Actions may therefore schedule the browser-test executions concurrently when runners are available.

Phase 4C provides pytest-xdist worker-level parallelism inside browser-test executions.

Phase 4D provides Allure reporting inside the Chromium `full-suite` job.

Phase 4E provides explicit runtime defaults.

Phase 4F provides runtime and failed-test diagnostics through the existing Pytest execution path.

Phase 5A provides representative Firefox and WebKit Smoke compatibility validation without replacing the existing Chromium topology.

### CI Runtime Defaults

The Chromium Smoke, Regression, and full-suite jobs use:

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

The Firefox/WebKit matrix uses the same runtime strategy except:

```text
QA_BROWSER=${{ matrix.browser }}
```

which resolves to:

```text
firefox
```

or:

```text
webkit
```

The quality job does not require browser runtime configuration.

The browser-test CI strategy therefore is:

* Chromium as the primary complete regression browser
* Firefox as a representative Smoke compatibility browser
* WebKit as a representative Smoke compatibility browser
* headless
* pytest-xdist parallel
* screenshot-on-failure enabled
* tracing disabled by default
* video disabled by default
* Phase 4F diagnostics active through normal Pytest execution

The current CI does not introduce:

* complete Firefox Regression
* complete WebKit Regression
* complete Firefox full-suite execution
* complete WebKit full-suite execution
* retries
* `continue-on-error`
* default trace retention
* default video retention
* secrets for non-secret runtime values
* diagnostic-specific environment variables
* persistent diagnostic artifacts

### GitHub Actions Concurrency, Matrix Expansion, And Pytest Parallelism

Three separate execution concepts are used.

GitHub Actions job-level scheduling:

```text
quality
├── smoke [Chromium]
├── regression [Chromium]
├── full-suite [Chromium]
└── cross-browser-smoke
```

GitHub Actions matrix expansion:

```text
cross-browser-smoke
├── Firefox
└── WebKit
```

Pytest worker-level execution:

```text
browser-test execution
└── pytest-xdist workers
```

Combined:

```text
quality
├── smoke [Chromium]
│   └── xdist workers
├── regression [Chromium]
│   └── xdist workers
├── full-suite [Chromium]
│   └── xdist workers
└── cross-browser-smoke
    ├── Firefox
    │   └── xdist workers
    └── WebKit
        └── xdist workers
```

GitHub Actions job concurrency, GitHub Actions matrix expansion, and pytest-xdist worker parallelism are separate mechanisms and should not be treated as interchangeable.

Reporting, runtime configuration, and diagnostics do not change these execution layers.

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

The quality job does not install Playwright browsers.

It does not execute browser tests and does not use pytest-xdist.

It does not generate browser-test reports.

It does not require the Phase 4E browser runtime environment variables.

A failure in the quality job prevents all current browser-test jobs from starting.

### Smoke Job

The dedicated `smoke` job is the Chromium Smoke execution path.

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

The Chromium Smoke job:

* installs Chromium
* uses the explicit Phase 4E CI runtime defaults
* runs Phase 4F runtime diagnostics through normal Pytest execution
* generates pytest-html reporting
* uploads Chromium Smoke-specific artifacts

It does not generate Allure results or an Allure HTML report.

Trace and video remain disabled by default.

### Regression Job

The dedicated `regression` job is the Chromium Regression execution path.

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

The Chromium Regression job:

* installs Chromium
* uses the explicit Phase 4E CI runtime defaults
* runs Phase 4F runtime diagnostics through normal Pytest execution
* generates pytest-html reporting
* uploads Chromium Regression-specific artifacts

It does not generate Allure results or an Allure HTML report.

Trace and video remain disabled by default.

### Full-Suite Job

The `full-suite` job remains the complete Chromium CI regression gate and the primary CI source for advanced Allure reporting.

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

The Chromium full-suite job uses the same explicit Phase 4E runtime defaults as Chromium Smoke and Regression.

Phase 4F diagnostics operate through the same Pytest execution path.

The dedicated Chromium Smoke and Regression jobs supplement the complete Chromium full-suite gate rather than replacing it.

Firefox and WebKit Smoke provide compatibility feedback but do not replace or expand complete Chromium regression responsibility.

### Cross-Browser Smoke Job

The `cross-browser-smoke` job provides representative Firefox and WebKit validation through one GitHub Actions matrix.

It uses:

```yaml
needs: quality

strategy:
  fail-fast: false
  matrix:
    browser:
      - firefox
      - webkit
```

Each matrix execution:

* checks out the repository
* configures Python 3.12
* installs project dependencies
* receives the browser-test runtime defaults
* sets `QA_BROWSER` from `${{ matrix.browser }}`
* installs only the selected Playwright browser engine
* runs the existing Smoke suite
* uses pytest-xdist through `-n auto`
* runs headless
* emits Phase 4F runtime diagnostics
* generates a browser-specific self-contained pytest-html report
* uploads browser-specific artifacts

Browser installation:

```bash
playwright install --with-deps ${{ matrix.browser }}
```

Core command:

```bash
pytest -m smoke -n auto -v
```

Report path:

```text
reports/${{ matrix.browser }}-smoke-report.html
```

Resolved reports:

```text
reports/firefox-smoke-report.html
reports/webkit-smoke-report.html
```

Chromium is intentionally excluded from this matrix because it already has dedicated Smoke, Regression, and complete full-suite execution.

Firefox and WebKit do not generate dedicated Allure reports.

### Allure CLI Setup In CI

The Chromium `full-suite` job configures Java 17 through:

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

This setup is limited to the Chromium full-suite job because Chromium Smoke, Chromium Regression, Firefox Smoke, and WebKit Smoke do not generate Allure HTML reports.

Phase 4F diagnostics do not require Java or the Allure CLI.

### Browser Setup

Current Playwright browser installation responsibilities are:

Chromium Smoke:

```bash
playwright install --with-deps chromium
```

Chromium Regression:

```bash
playwright install --with-deps chromium
```

Chromium full suite:

```bash
playwright install --with-deps chromium
```

Firefox matrix entry:

```bash
playwright install --with-deps firefox
```

WebKit matrix entry:

```bash
playwright install --with-deps webkit
```

The `quality` job does not require browser installation.

The runtime configuration layer recognizes:

```text
chromium
firefox
webkit
```

and all three browser engines are now used by the implemented execution strategy.

Current responsibilities remain:

* Chromium — complete regression responsibility
* Firefox — representative Smoke compatibility
* WebKit — representative Smoke compatibility

The workflow does not install all three engines in every browser-test job.

The matrix installs only its selected engine.

### CI Marker Responsibility

Dedicated Chromium marker-filtered CI jobs currently exist for:

* Smoke
* Regression

The existing Smoke marker is additionally used by:

* Firefox
* WebKit

through the Phase 5A cross-browser matrix.

Dedicated CI jobs do not currently exist for:

* UI
* Security
* Sorting
* Navigation
* E2E

These marker suites remain available for selective local execution.

Their tests still participate in Chromium full-suite CI execution as part of the normal collected test suite.

Tests that also carry `smoke` additionally participate in Firefox and WebKit representative compatibility validation.

Because the Chromium full-suite job uses pytest-xdist, tests may be distributed across workers during complete CI execution.

Because the Chromium full-suite collects Allure results, those tests are also included in the advanced full-suite reporting data.

Phase 5A does not introduce a dedicated cross-browser marker.

### Reports And Artifacts

Current reporting and diagnostic mechanisms are:

* Phase 4F runtime diagnostics
* Phase 4F failed-test diagnostics
* pytest-html
* browser-specific pytest-html
* Allure
* configurable failure screenshots
* optional Playwright trace
* optional Playwright video
* GitHub Actions artifacts

Chromium Smoke artifacts:

```text
smoke-pytest-html-report
smoke-test-artifacts
```

Chromium Regression artifacts:

```text
regression-pytest-html-report
regression-test-artifacts
```

Chromium full-suite artifacts:

```text
pytest-html-report
full-suite-allure-report
test-artifacts
```

Firefox Smoke artifacts:

```text
firefox-smoke-pytest-html-report
firefox-smoke-test-artifacts
```

WebKit Smoke artifacts:

```text
webkit-smoke-pytest-html-report
webkit-smoke-test-artifacts
```

The dedicated Chromium full-suite Allure artifact uses:

```text
reports/allure-report/
```

The broader Chromium full-suite artifact continues to upload:

```text
reports/
```

The Firefox and WebKit broader runtime artifacts independently upload:

```text
reports/
```

from their own matrix execution environments.

Browser-specific artifact names prevent Firefox and WebKit outputs from colliding.

Artifact upload steps use `if: always()` so available reports and runtime outputs can still be uploaded when a browser-test command fails.

The Chromium Allure report-generation step also uses failure-tolerant workflow execution and checks for usable result data before generating the report.

Current artifact retention remains seven days.

Trace and video are disabled in CI by default and are therefore not introduced as default retained artifacts.

Phase 4F does not introduce persistent log files or a dedicated diagnostics artifact.

Detailed artifact paths, retention, runtime defaults, and job behavior are documented in [CI/CD Pipeline](ci-cd-pipeline.md).

### CI Failure Behavior

A Pull Request should not be merged if required CI validation fails.

Current quality-gate behavior includes:

* Ruff failure fails CI
* Black failure fails CI
* isort failure fails CI
* failed `quality` prevents all browser-test jobs from starting
* Chromium Smoke failure fails the Smoke job
* Chromium Regression failure fails the Regression job
* Chromium full-suite failure fails the full-suite job
* Firefox Smoke failure fails the Firefox matrix execution
* WebKit Smoke failure fails the WebKit matrix execution
* `fail-fast: false` allows the other cross-browser matrix execution to continue when one matrix entry fails
* invalid Phase 4E runtime configuration fails before normal browser execution proceeds

The workflow does not convert required test or quality failures into successful results.

pytest-xdist does not change the failure policy.

Allure reporting does not change the failure policy.

Runtime configuration does not change the failure policy.

Phase 4F diagnostics do not change the failure policy.

Matrix execution does not change the failure policy.

A failing test executed by an xdist worker causes the corresponding Pytest command and browser-test job to fail.

Available reports, screenshots, diagnostics, and artifacts may still be produced for failure analysis according to their configured policies.

## Current Execution Scope

The current implementation combines:

* Phase 4B CI Execution Strategy
* Phase 4C Parallel Execution Strategy
* Phase 4D Reporting Strategy
* Phase 4E Runtime Configuration Strategy
* Phase 4F Diagnostics And Fixture Cleanup
* Phase 5A Playwright Cross-Browser Smoke Validation

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
* xdist integration into the existing Chromium browser-test CI jobs
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
* Chromium-only CI execution for the Phase 4E workstream
* preservation of Phase 4B–4D topology and reporting behavior

Phase 4F added:

* shared runtime and failure diagnostic formatting through `framework/diagnostics.py`
* effective runtime summary through `pytest_report_header`
* runtime base URL visibility
* effective browser visibility
* headed/headless mode visibility
* action/navigation timeout visibility
* assertion timeout visibility
* screenshot policy visibility
* trace policy visibility
* video policy visibility
* suppression of duplicate runtime summaries on xdist workers
* failed-test Pytest node ID reporting
* `setup`, `call`, and `teardown` failure-phase reporting
* current URL reporting when a Playwright page is available
* screenshot path reporting after successful custom screenshot capture
* diagnostic error reporting for page URL retrieval
* diagnostic error reporting for screenshot creation
* diagnostic error reporting for Allure attachment
* framework-level Pytest responsibilities retained in root `conftest.py`
* application scenario fixtures moved to `tests/conftest.py`
* preserved explicit scenario fixture names
* preserved fixture scopes
* preserved pytest-playwright browser lifecycle
* preserved pytest-playwright trace and video ownership
* preserved custom screenshot behavior
* preserved Allure screenshot reuse
* preservation of the Phase 4 CI topology

Phase 5A adds:

* Chromium retained as the primary complete regression browser
* existing Chromium Smoke execution preserved
* existing Chromium Regression execution preserved
* existing Chromium complete full-suite execution preserved
* local Firefox Smoke validation
* local WebKit Smoke validation
* dedicated Firefox/WebKit `cross-browser-smoke` matrix
* matrix limited to Firefox and WebKit
* `needs: quality`
* `fail-fast: false`
* selected-engine-only browser installation
* `QA_BROWSER` supplied from the matrix browser value
* reuse of the existing `smoke` marker
* reuse of existing functional tests
* reuse of existing Page Objects
* reuse of existing fixtures
* reuse of existing assertions
* pytest-xdist execution through `-n auto`
* Firefox-specific pytest-html report
* WebKit-specific pytest-html report
* independent Firefox artifacts
* independent WebKit artifacts
* preservation of Chromium full-suite Allure responsibility
* preservation of Phase 4F diagnostics
* preservation of existing failure screenshot policy

The current implementation does not include:

* report hosting
* GitHub Pages reporting
* Allure history persistence
* trend-history storage
* retries
* named environment profiles
* automatic `.env` loading
* device emulation
* complete Firefox Regression
* complete WebKit Regression
* complete Firefox full-suite execution
* complete WebKit full-suite execution
* complete three-browser regression parity
* persistent project log files
* browser console capture
* network capture
* HTML or page-source dumps
* automatic trace enablement
* automatic video enablement
* generic fixture factories
* dependency-injection layers
* autouse redesign
* multi-layer fixture packages
* fixture scope redesign
* Selenium execution

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

Phase 4F diagnostic summaries are transient execution output and do not introduce persistent project log files or another output directory.

Phase 5A adds browser-specific pytest-html output under `reports/` but does not change the repository-output boundary.

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
docs(AQA-0109): document phase 4f diagnostics and fixture strategy
docs(AQA-0113): document phase 5a cross-browser strategy
```

For a shared workstream branch, intermediate task commits remain on the workstream branch until the closing checkpoint authorizes the workstream merge.

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
* diagnostic behavior where applicable
* fixture responsibility and isolation where applicable
* parallel validation where required by the active workstream
* cross-browser validation where required by the active workstream
* reporting validation where required by the active workstream
* full test suite execution or accepted scoped validation
* CI status
* expected reports and artifacts
* browser-specific artifacts where applicable
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
AQA-0114 — Phase 5A Cross-Browser Validation Checkpoint
```

No new major workstream should start before the relevant checkpoint is completed when the roadmap requires that checkpoint.

For a shared workstream branch, the final checkpoint can also own the decision to merge the accumulated task commits into `develop`.

For portfolio promotion, the checkpoint should additionally verify that the project is suitable for public presentation through `main`.

## Documentation Updates

Documentation should be updated when changes affect:

* framework architecture
* project structure
* testing strategy
* marker strategy
* test execution strategy
* browser execution strategy
* runtime configuration strategy
* diagnostic strategy
* fixture responsibility
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

Execution-only browser expansion does not require test case automation metadata changes when no new product-facing functional coverage is introduced.

General documentation synchronization may be deferred to an approved review, stabilization, or checkpoint task when that is the defined workstream workflow.

For workstream final validation tasks, documentation should be checked for stale future-facing wording describing already implemented capabilities as planned.

### Marker Documentation Changes

When pytest marker behavior changes, verify that:

* `pytest.ini` reflects the intended executable markers
* automated test usage matches the registered marker definitions
* test case metadata matches automated marker usage
* `docs/testing-strategy.md` describes the current marker semantics
* workflow and README commands do not reference removed markers

Phase 5A does not introduce a cross-browser marker.

Browser execution should not be documented as a new marker dimension unless implementation explicitly changes.

### Parallel Execution Documentation Changes

When parallel execution behavior changes, verify that:

* `pytest-xdist` dependency status is described accurately
* sequential execution remains documented where supported
* approved parallel commands match actual execution
* fixture and test independence assumptions remain accurate
* parametrized and E2E tests do not rely on execution order
* reporting and screenshot behavior remains compatible with worker-level execution
* runtime configuration remains compatible with supported parallel execution
* Phase 4F runtime diagnostics remain compatible with xdist
* runtime summary output is not incorrectly documented as worker-duplicated
* browser-specific Smoke execution remains compatible with xdist where implemented
* no unvalidated sequential-only exception is documented as fact

### Runtime Configuration Documentation Changes

When runtime configuration behavior changes, verify that:

* `config/settings.py` remains the source of truth for supported project environment variables and defaults
* root `conftest.py` integration is documented accurately
* `BasePage` URL composition matches actual implementation
* accepted browser values are documented accurately
* headed boolean values are documented accurately
* timeout defaults and units are documented accurately
* screenshot policy values match implementation
* trace and video policy values match implementation
* invalid explicit configuration is documented as fail-fast behavior
* native pytest-playwright option precedence is documented where implemented
* local configuration behavior is separated from CI browser responsibility
* Chromium is documented as the primary complete regression browser
* Firefox and WebKit are documented as representative Smoke browsers
* `.env` loading is not documented unless implemented
* named environment profiles are not documented unless implemented
* complete Firefox/WebKit Regression or full-suite execution is not documented unless implemented
* Phase 4F diagnostics and fixture cleanup are documented as separate implemented responsibilities rather than Phase 4E configuration features

### Cross-Browser Documentation Changes

When browser execution coverage changes, verify that:

* Chromium complete regression responsibility is documented accurately
* Firefox coverage is documented accurately
* WebKit coverage is documented accurately
* the existing `smoke` marker remains the representative cross-browser suite unless implementation changes
* browser selection is separated from marker semantics
* local Firefox and WebKit commands match current runtime configuration
* CI matrix values match `.github/workflows/ci.yml`
* each matrix entry installs only its selected browser engine
* `pytest-xdist` remains documented where used
* browser-specific pytest-html paths match implementation
* browser-specific artifact names match implementation
* Chromium is not documented as part of the cross-browser matrix when it has separate dedicated jobs
* complete three-browser Regression or full-suite coverage is not claimed unless implemented
* browser-specific duplicate test modules are not described unless they actually exist
* Selenium is not described as implemented unless its dedicated scope is completed

### Diagnostic Documentation Changes

When Phase 4F diagnostic behavior changes, verify that:

* `framework/diagnostics.py` responsibilities are documented accurately
* runtime summary fields match implementation
* `pytest_report_header` ownership is documented accurately
* xdist worker-header suppression is documented accurately
* failed-test diagnostics include node ID and failure phase
* current URL is documented as conditional on an available Playwright page
* screenshot path is documented only after successful screenshot creation
* diagnostic errors for page URL retrieval, screenshot creation, and Allure attachment are documented accurately
* persistent project log files are not claimed unless explicitly implemented
* browser console capture is not claimed unless explicitly implemented
* network capture is not claimed unless explicitly implemented
* trace and video remain documented as pytest-playwright-owned behavior
* browser-engine selection does not imply a separate diagnostics implementation

### Fixture Documentation Changes

When fixture organization changes, verify that:

* root `conftest.py` framework responsibilities are documented accurately
* `tests/conftest.py` application scenario fixture ownership is documented accurately
* fixture names match implementation
* fixture scopes are not described as changed unless they actually changed
* fixture independence remains compatible with pytest-xdist
* supported browser engines reuse the same scenario fixture architecture unless implementation changes
* generic fixture factories are not claimed unless implemented
* dependency-injection layers are not claimed unless implemented
* autouse redesign is not claimed unless implemented
* multi-layer fixture packages are not claimed unless implemented

### Reporting Documentation Changes

When reporting behavior changes, verify that:

* pytest-html responsibilities remain accurate
* Chromium report paths match implementation
* Firefox/WebKit browser-specific report paths match implementation
* Allure result and HTML output locations match implementation
* local Allure commands match current behavior
* Allure CLI is described as a separate HTML-generation prerequisite
* failure screenshot behavior matches root `conftest.py`
* screenshot attachments reuse the existing captured file
* screenshot policy behavior is documented accurately
* failed-test screenshot path diagnostics are documented accurately
* trace and video runtime output is distinguished from project screenshot and report output
* sequential and parallel reporting compatibility is described accurately
* Firefox/WebKit Smoke is not documented as having dedicated Allure CI reporting
* generated outputs are clearly distinguished from repository content
* unsupported capabilities such as Allure history, hosting, GitHub Pages, retries, and complete three-browser reporting are not described as implemented

### CI Documentation Changes

When CI execution behavior changes, verify that:

* `.github/workflows/ci.yml` remains the implementation source of truth
* `docs/ci-cd-pipeline.md` reflects current jobs, dependencies, matrix behavior, reports, artifacts, triggers, runtime defaults, and parallel commands
* `docs/workflow.md` reflects current local and CI responsibilities
* README remains a useful high-level entry point
* marker suites executed in dedicated CI jobs are distinguished from locally selective marker suites
* Chromium complete regression responsibility is distinguished from representative Firefox/WebKit Smoke responsibility
* GitHub Actions job concurrency is distinguished from matrix expansion
* GitHub Actions matrix expansion is distinguished from pytest-xdist worker parallelism
* Chromium Smoke and Regression remain pytest-html-focused unless implementation explicitly changes
* Firefox and WebKit Smoke remain pytest-html-focused unless implementation explicitly changes
* Chromium full-suite Allure artifact naming and output locations match the workflow
* browser-specific Firefox/WebKit artifact names match the workflow
* browser-test jobs document their explicit runtime defaults
* Phase 4F diagnostics are described as part of the existing Pytest execution path
* browser installations match the actual job responsibilities
* future capabilities are not described as already implemented

### Portfolio Promotion Documentation Review

For portfolio promotion, documentation should also be checked for:

* stale workstream-finalization wording
* stale PR-readiness wording
* statements that suggest completed work exists only on an obsolete branch
* implemented features mixed with planned future extensions
* missing distinction between `main` as the stable portfolio branch and `develop` as the integration branch
* stale statements describing implemented runtime configuration as future work
* stale statements describing Phase 4F diagnostics or fixture cleanup as future work
* stale statements describing Phase 5A cross-browser Smoke as future work
* incorrect claims that the complete project is Chromium-only
* incorrect claims of complete three-browser Regression coverage

## Current Workflow Status

The current workflow supports completed Phase 3 page-level automation coverage for Login, Inventory, Product Details, Cart, and Checkout areas.

Phase 3 page-level automation coverage has been completed, reviewed, validated, squash-merged into `develop`, and promoted to `main` as the stable Phase 3 portfolio snapshot.

Phase 4 Framework Maturity is implemented.

Phase 4A established the current executable Pytest marker strategy.

Phase 4B CI Execution Strategy is implemented with:

* a dedicated `quality` job
* dedicated Chromium Smoke CI execution
* dedicated Chromium Regression CI execution
* a complete unfiltered Chromium `full-suite` job
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
* pytest-xdist execution inside the Chromium Smoke, Regression, and full-suite CI jobs
* preserved Phase 4B job structure
* preserved pytest-html reports and artifact behavior

No sequential-only test exceptions are required for the current execution model.

Phase 4D Reporting Strategy is implemented with:

* local Allure result collection
* local Allure HTML report generation
* Allure CLI report-generation workflow
* failure screenshot attachments in Allure
* reuse of the existing failure screenshot mechanism
* compatibility with sequential execution
* compatibility with pytest-xdist parallel execution
* Chromium full-suite Allure result collection in GitHub Actions
* Chromium full-suite Allure HTML generation in GitHub Actions
* dedicated `full-suite-allure-report` artifact
* preserved Chromium Smoke and Regression pytest-html reporting
* preserved existing browser-test artifact behavior

Phase 4E Runtime Configuration is implemented with:

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
* runtime integration through `BasePage` and root `conftest.py`
* preservation of pytest-playwright native runtime behavior
* explicit runtime defaults in browser-test CI jobs
* Chromium as the default browser

Phase 4F Diagnostics And Fixture Cleanup is implemented with:

* lightweight runtime diagnostics
* `framework/diagnostics.py`
* runtime summary formatting
* failed-test summary formatting
* diagnostic error formatting
* project diagnostics logger without persistent log files
* effective runtime header through `pytest_report_header`
* base URL visibility
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
* framework-level Pytest responsibilities in root `conftest.py`
* application scenario fixtures in `tests/conftest.py`
* preserved explicit scenario fixture names
* preserved fixture scopes
* preserved pytest-playwright browser lifecycle
* preserved pytest-playwright trace and video lifecycle
* preserved custom screenshot behavior
* preserved Allure screenshot reuse
* validated sequential execution compatibility
* validated pytest-xdist execution compatibility

Phase 4F validation confirmed:

```text
Smoke: 31 passed
Regression: 109 passed
Full sequential: 236 passed
Full pytest-xdist: 236 passed
Ruff: passed
Black check: passed
isort: passed
```

Controlled failure validation after fixture separation confirmed:

* runtime header
* failure phase
* Pytest node ID
* current page URL
* screenshot diagnostic path

Phase 5A Playwright Cross-Browser Strategy is implemented with:

* Chromium retained as the primary complete regression browser
* existing Chromium Smoke execution preserved
* existing Chromium Regression execution preserved
* existing Chromium complete full-suite execution preserved
* local Firefox Smoke validation
* local WebKit Smoke validation
* dedicated Firefox/WebKit `cross-browser-smoke` GitHub Actions matrix
* matrix limited to Firefox and WebKit
* `needs: quality`
* `fail-fast: false`
* browser selection through existing `QA_BROWSER`
* selected-engine-only Playwright installation
* reuse of the existing `smoke` marker
* reuse of existing functional tests
* reuse of existing Page Objects, fixtures, and assertions
* pytest-xdist execution through `-n auto`
* Firefox-specific pytest-html reporting
* WebKit-specific pytest-html reporting
* independent Firefox GitHub Actions artifacts
* independent WebKit GitHub Actions artifacts
* preserved Chromium full-suite Allure responsibility
* preserved Phase 4F diagnostics and failure screenshot behavior

Phase 5A validation confirmed:

```text
Firefox Smoke: 31 passed
WebKit Smoke: 31 passed
Chromium full-suite: 236 passed
Ruff: passed
Black check: passed
isort: passed
```

GitHub Actions validation additionally confirmed successful execution of:

* `quality`
* Chromium `smoke`
* Chromium `regression`
* Chromium `full-suite`
* `cross-browser-smoke (firefox)`
* `cross-browser-smoke (webkit)`

No Firefox- or WebKit-specific test duplication, fixture branching, Page Object branching, skip logic, or compatibility workaround was required.

Formal Phase 5A workstream closure and merge remain owned by the dedicated Phase 5A closing checkpoint.

The `main` branch represents the polished portfolio version of the project.

The `develop` branch remains the integration branch and may contain newer work after this document is read from `main`.

Future work should continue from `develop` or the approved active workstream branch unless a specific portfolio promotion or release task targets `main`.

The current framework does not implement:

* named environment profiles
* automatic `.env` loading
* complete Firefox Regression
* complete WebKit Regression
* complete Firefox full-suite execution
* complete WebKit full-suite execution
* complete three-browser regression parity
* device emulation
* retries
* persistent project log files
* browser console capture
* network capture
* HTML or page-source dumps
* automatic trace enablement
* automatic video enablement
* generic fixture factories
* dependency-injection infrastructure
* autouse fixture redesign
* multi-layer fixture packages
* fixture scope redesign
* Allure history persistence
* hosted reporting
* GitHub Pages reporting
* Selenium execution
* Docker-based execution