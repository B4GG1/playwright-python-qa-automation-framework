# Git Branching And Merge Strategy

This document defines the branching strategy, merge workflow, and repository standards used in this project.

The goal is to keep the repository history clean, support isolated development, and ensure that changes are validated before being merged into stable branches.

The branching strategy supports two stable branch roles:

* `main` represents the polished portfolio/release version of the project.
* `develop` represents the integration branch for completed and validated work before it is promoted to `main`.

When this document is read from `main`, the `develop` branch may already contain newer integration work that has not yet been promoted to the stable portfolio branch.

For detailed pytest marker semantics, sequential/parallel suite execution strategy, runtime configuration, diagnostics, fixture responsibility behavior, cross-browser validation, containerized execution, and visual regression strategy, see [Testing Strategy](testing-strategy.md).

For detailed GitHub Actions execution, job dependencies, pytest-xdist execution, cross-browser Smoke matrix, runtime defaults, diagnostics, reports, artifacts, and the boundary between native functional CI and the dedicated Docker-based visual regression job, see [CI/CD Pipeline](ci-cd-pipeline.md).

The current Phase 5A browser validation strategy uses:

* Chromium as the primary complete regression browser.
* Firefox for representative Smoke compatibility validation.
* WebKit for representative Smoke compatibility validation.

Firefox and WebKit do not execute the complete Regression suite or complete full suite.

Phase 5B added Docker as an additional reproducible Playwright/Pytest execution path while preserving direct WSL/Linux execution and native functional GitHub Actions CI. Phase 5B was formally closed through AQA-0117.

The active Phase 5C workstream uses `feature/visual-regression-testing`.

Phase 5C reuses the Phase 5B Docker environment for one dedicated Chromium visual regression CI job while keeping the existing functional CI jobs native.

Formal Phase 5C roadmap closure remains owned by the AQA-0122 closing checkpoint.

## Branching Model

This repository follows a lightweight Git workflow inspired by a simplified Git Flow model.

The main goals are:

* clean and traceable history
* isolated feature or workstream development
* safe integration into stable branches
* CI validation before merging changes
* readable Pull Requests
* professional portfolio-friendly Git history
* controlled promotion from integration state to stable portfolio state

## Branch Structure

### `main`

The `main` branch represents the stable portfolio/release state of the repository.

Rules:

* should always remain stable
* should contain validated and reviewed changes only
* should be updated through Pull Requests
* should not receive direct pushes
* should be used as the most polished public version of the project
* should represent a stable portfolio snapshot suitable for recruiters or reviewers

The current stable portfolio baseline is promoted to `main` only after the corresponding work has been completed, validated, reviewed, and integrated through `develop`.

### `develop`

The `develop` branch is the main integration branch for ongoing development.

Rules:

* used as the base branch for feature work
* receives completed work through Pull Requests
* should remain reasonably stable
* acts as the staging area before changes are promoted to `main`
* should contain completed and validated workstreams
* may contain newer work than `main` after the latest stable portfolio snapshot has been promoted

The `develop` branch is the source branch for portfolio promotion Pull Requests into `main`.

### Feature Branches

Feature branches are used for new functionality, framework improvements, refactors, or larger functional workstreams.

Naming convention:

```text
feature/<short-description>
```

Examples:

```text
feature/login-page
feature/inventory-products
feature/cart-page
feature/structure-cleanup
feature/checkout
feature/allure-reporting
feature/playwright-cross-browser-validation
feature/containerized-playwright-execution
feature/visual-regression-testing
feature/api-client
```

A feature branch may represent:

* one small task
* one larger feature
* one complete workstream
* one structure cleanup or stabilization workstream

For small independent tasks, one branch per task is preferred.

For tightly connected workstreams, one larger branch is acceptable if commits remain organized and traceable by task ID.

Examples from the project:

```text
feature/login-page
feature/inventory-products
feature/cart-page
feature/structure-cleanup
feature/checkout
feature/allure-reporting
feature/playwright-cross-browser-validation
feature/containerized-playwright-execution
feature/visual-regression-testing
```

These branches can be used for complete functional automation, structure cleanup, documentation synchronization, reporting upgrades, cross-browser validation, containerized execution, visual regression workstreams, or stabilization workstreams when the tasks are tightly related and easier to validate together.

### Fix Branches

Fix branches are used for bug fixes or corrections.

Naming convention:

```text
fix/<short-description>
```

Examples:

```text
fix/login-timeout
fix/ci-artifact-upload
fix/screenshot-hook
```

### Documentation Branches

Documentation branches may be used for documentation-only changes.

Naming convention:

```text
docs/<short-description>
```

Examples:

```text
docs/update-readme
docs/testing-strategy
docs/git-workflow
docs/phase-review
docs/portfolio-promotion
```

### Refactor Branches

Refactor branches may be used when changes improve structure without adding new behavior.

Naming convention:

```text
refactor/<short-description>
```

Examples:

```text
refactor/login-fixtures
refactor/page-object-cleanup
refactor/test-data-structure
refactor/runtime-configuration
refactor/diagnostics-fixture-cleanup
```

### Promotion Branches

Promotion branches may be used for final documentation cleanup, stabilization, or portfolio release preparation before promoting `develop` to `main`.

Naming convention:

```text
chore/<short-description>
```

Examples:

```text
chore/phase-3-portfolio-promotion
chore/main-portfolio-promotion
chore/docs-cleanup-before-main
```

Promotion branches should not introduce unrelated new feature work.

Their purpose is to prepare an already validated integration state for the stable portfolio branch.

## Commit Strategy

Commits should be small enough to be understandable, but large enough to represent a logical step.

Recommended commit format:

```text
<type>(<task-id>): <short description>
```

Examples:

```text
docs(AQA-0026): create login page test cases
feat(AQA-0027): implement login page object model
refactor(AQA-0032): parametrize login validation scenarios
test(AQA-0038): add protected inventory route access test
test(AQA-0057): add product to cart test
chore(AQA-0064): review and stabilize cart workstream
chore(AQA-0073): finalize phase 3c structure cleanup
test(AQA-0078): add checkout information page tests
test(AQA-0079): add checkout overview tests
test(AQA-0080): add checkout completion tests
chore(AQA-0082): finalize checkout automation workstream
feat(AQA-0096): integrate local allure reporting
chore(AQA-0097): integrate allure reporting into ci
docs(AQA-0098): document phase 4d reporting strategy
refactor(AQA-0100): add runtime base url configuration
feat(AQA-0101): add browser and timeout runtime options
feat(AQA-0102): add runtime artifact policies
chore(AQA-0103): integrate runtime configuration into ci
docs(AQA-0104): document phase 4e runtime configuration
refactor(AQA-0106): add runtime diagnostics
refactor(AQA-0107): add failed-test diagnostics
refactor(AQA-0108): separate scenario fixtures from framework hooks
docs(AQA-0109): document phase 4f diagnostics and fixture strategy
ci(AQA-0112): add playwright cross-browser smoke validation
docs(AQA-0113): document phase 5a cross-browser strategy
build(AQA-0115): add containerized playwright execution
docs(AQA-0116): document containerized playwright execution
test(AQA-0118): add visual regression comparison infrastructure
test(AQA-0119): add controlled visual regression checkpoints
ci(AQA-0120): add visual regression validation job
docs(AQA-0121): document phase 5c visual regression strategy
```

For portfolio promotion work that is not tied to a single implementation task, the commit message may omit a task ID if no approved task ID exists.

Examples:

```text
chore: promote phase 3 portfolio state to main
docs: clean up documentation before main promotion
```

Common commit types:

* `feat` — new framework functionality
* `test` — automated tests or test-related changes
* `docs` — documentation changes
* `refactor` — structural changes without behavior change
* `fix` — bug fixes
* `ci` — CI workflow changes
* `build` — build, containerization, or execution-environment changes
* `chore` — maintenance, configuration, review, or promotion work

## Workstream Branch Strategy

For larger functional areas or tightly connected cleanup phases, the project may use one workstream branch.

Examples:

```text
feature/login-page
feature/inventory-products
feature/cart-page
feature/structure-cleanup
feature/checkout
feature/allure-reporting
feature/playwright-cross-browser-validation
feature/containerized-playwright-execution
feature/visual-regression-testing
refactor/runtime-configuration
refactor/diagnostics-fixture-cleanup
```

In this approach:

* all related tasks are committed on the same branch
* each task still gets its own meaningful commit
* commits should include the task ID when applicable
* the branch is pushed regularly as backup
* local validation is performed during and after the workstream
* the workstream Pull Request is merged only when the whole approved workstream is ready
* final merge into `develop` is performed using Squash and merge

This approach is acceptable when tasks are tightly connected and reviewing them together makes sense.

The `feature/structure-cleanup` branch is an example of a workstream branch used for structural cleanup, coverage synchronization, final validation, and documentation sync after page-level Login, Inventory, Product Details, and Cart automation coverage.

The `feature/checkout` branch is an example of a functional workstream branch used for checkout automation, related coverage completion, final validation, and documentation synchronization before integration into `develop`.

The `feature/allure-reporting` branch is an example of a framework-maturity workstream branch used for reporting implementation, CI integration, documentation synchronization, and final Phase 4D validation before integration into `develop`.

The `refactor/runtime-configuration` branch is an example of a framework-maturity workstream branch used for Phase 4E runtime configuration implementation and CI integration before integration into `develop`.

The `refactor/diagnostics-fixture-cleanup` branch is an example of a framework-maturity workstream branch used for Phase 4F runtime diagnostics, failed-test diagnostics, fixture responsibility cleanup, documentation synchronization, and final workstream validation before integration into `develop`.

The `feature/playwright-cross-browser-validation` branch is the Phase 5A workstream branch used for representative Playwright Firefox/WebKit Smoke CI integration, documentation synchronization, and final cross-browser validation checkpoint.

The `feature/containerized-playwright-execution` branch is the Phase 5B workstream branch used for Docker-based Playwright execution implementation, validation, documentation synchronization, and the final Phase 5B closing checkpoint. Phase 5B was completed through AQA-0117.

The `feature/visual-regression-testing` branch is the Phase 5C workstream branch used for visual comparison infrastructure, approved visual checkpoints, Docker-based visual CI integration, documentation synchronization, and the final Phase 5C closing checkpoint.

The workstream deliberately keeps the six existing functional CI executions native while adding one dedicated Docker-based Chromium `visual-regression` job.

A workstream branch may remain unmerged while related implementation, documentation, and final checkpoint tasks are completed.

A temporary Pull Request may be used for CI validation without requiring an immediate merge.

The final integration remains subject to the approved workstream checkpoint and merge workflow.

## Merge Strategy

The recommended merge strategy is:

> Squash and merge

Squash merge combines all commits from a source branch into a single commit on the target branch.

Benefits:

* keeps commit history clean
* one workstream becomes one logical commit on `develop`
* one portfolio promotion becomes one logical commit on `main`
* simplifies rollback
* improves readability for reviewers and recruiters
* reduces noisy commit history
* keeps local development commits flexible

Example final squash commit:

```text
test(AQA-0064): complete cart automation workstream
```

For documentation-only, cleanup, checkpoint-only, or portfolio-promotion changes, the squash commit may use `docs` or `chore` instead:

```text
chore(AQA-0064): review and stabilize cart workstream
docs(AQA-0064): update project documentation after cart workstream
chore(AQA-0073): finalize phase 3c structure cleanup
chore(AQA-0082): finalize checkout automation workstream
docs(AQA-0104): document phase 4e runtime configuration
docs(AQA-0109): document phase 4f diagnostics and fixture strategy
docs(AQA-0113): document phase 5a cross-browser strategy
docs(AQA-0116): document containerized playwright execution
chore(AQA-0117): close phase 5b containerized execution workstream
docs(AQA-0121): document phase 5c visual regression strategy
chore(AQA-0122): close phase 5c visual regression workstream
chore: promote phase 3 portfolio state to main
```

## Direct Push Policy

Direct pushes should be avoided for:

* `main`
* `develop`

Recommended workflow for regular development:

```text
feature / fix / docs / refactor branch
        ↓
Pull Request
        ↓
CI validation
        ↓
Review
        ↓
Squash merge
        ↓
develop
```

Recommended workflow for stable portfolio promotion:

```text
develop
  ↓
Pull Request
  ↓
CI validation
  ↓
Review
  ↓
Squash merge
  ↓
main
```

For this project, even when working solo, Pull Requests are used to practice professional workflow and validate changes through CI.

Direct pushes to feature, fix, documentation, refactor, or promotion branches are acceptable during active implementation, review, documentation sync, stabilization, and checkpoint work.

## Branch Protection Rules

Recommended GitHub branch protection settings are listed below.

### `main`

Recommended rules:

* require Pull Request before merging
* require CI status checks to pass
* disallow force pushes
* disallow direct commits
* require linear history if appropriate
* keep as the stable portfolio/release branch

### `develop`

Recommended rules:

* require Pull Request before merging
* require CI status checks to pass
* disallow force pushes where practical
* use as the primary integration branch for completed workstreams

For a solo portfolio project, these rules can be introduced gradually as the workflow matures.

## Pull Request Workflow

### Regular Development Pull Requests

Standard Pull Request workflow for feature, fix, documentation, refactor, and workstream branches:

1. Start from the latest `develop` branch.
2. Create a dedicated feature, fix, refactor, documentation, or workstream branch.
3. Implement changes locally.
4. Commit logical pieces of work.
5. Push the branch to GitHub regularly.
6. Run relevant local validation.
7. Run the complete suite before merge when required.
8. Complete the required workstream checkpoint when applicable.
9. Open a Pull Request into `develop`.
10. Wait for CI pipeline validation.
11. Review changed files manually.
12. Squash merge after validation.
13. Update local `develop`.
14. Delete the completed source branch if no longer needed.

Pull Request direction for regular development:

```text
feature/* -> develop
fix/* -> develop
docs/* -> develop
refactor/* -> develop
chore/* -> develop
```

### Portfolio Promotion Pull Requests

Promotion to `main` should happen only after `develop` contains stable and validated changes that are ready to be presented as a polished portfolio version.

Recommended portfolio promotion workflow:

1. Ensure `develop` contains the completed and validated project state.
2. Complete any required documentation cleanup on `develop` or a dedicated promotion branch.
3. Run local validation before promotion when possible.
4. Open a Pull Request from `develop` to `main`.
5. Wait for CI pipeline validation on the Pull Request.
6. Review changed files manually from a portfolio or technical-review perspective.
7. Confirm that the promoted state does not describe unfinished work as implemented.
8. Squash merge into `main` after validation.
9. Update local `main` and `develop`.
10. Continue future work from `develop`.

Pull Request direction for portfolio promotion:

```text
develop -> main
```

Promotion to `main` should not be used for incomplete feature work, experimental changes, or unvalidated workstreams.

## Local Validation Before Pull Request

Recommended full sequential local checks before opening a Pull Request:

```bash
ruff check .
black --check .
isort . --check-only
pytest -v
```

Sequential execution remains supported as the baseline local validation mode.

### Parallel Validation

Phase 4C adds validated pytest-xdist worker-level parallel execution.

Approved primary Chromium parallel commands are:

```bash
pytest -m smoke -n auto -v
pytest -m regression -n auto -v
pytest -n auto -v
```

Parallel validation should be used when the task or workstream affects:

* worker-level execution
* fixture isolation
* fixture responsibility or organization
* shared-state assumptions
* parametrized execution independence
* E2E checkpoint independence
* parallel reporting or failure-artifact behavior
* runtime diagnostics under pytest-xdist

Parallel execution is an additional supported mode and does not replace sequential validation.

The current suite was validated under pytest-xdist execution without identified sequential-only test exceptions.

### Cross-Browser Smoke Validation

Phase 5A adds representative Playwright browser-engine compatibility validation.

Chromium remains the primary complete regression browser.

Firefox and WebKit execute representative Smoke tests using the existing `smoke` marker.

Approved local commands:

```bash
QA_BROWSER=firefox pytest -m smoke -n auto -v
QA_BROWSER=webkit pytest -m smoke -n auto -v
```

The selected Playwright engines must be installed locally before execution.

The representative Smoke suite reuses:

* existing functional tests
* existing Page Objects
* existing application fixtures
* existing assertions
* centralized runtime configuration
* Phase 4F diagnostics
* pytest-xdist worker-level execution

No new cross-browser marker or duplicate browser-specific test modules are required.

Current browser responsibilities:

```text
Chromium
├── Smoke
├── Regression
├── complete functional full suite
└── dedicated visual regression

Firefox
└── representative Smoke

WebKit
└── representative Smoke
```

Complete Firefox or WebKit Regression/full-suite validation is not part of the current execution strategy.

### Containerized Playwright Validation

Phase 5B adds Docker as an additional reproducible execution path for the existing Playwright/Pytest framework.

Build the pinned project image from the repository root:

```bash
docker build -t playwright-qa-framework:local .
```

Validated sequential Chromium Smoke execution:

```bash
docker run --rm --init --ipc=host \
  playwright-qa-framework:local \
  -m smoke -v
```

Validated pytest-xdist execution includes explicit `-n 2` execution and a controlled `-n auto` run capped to two workers:

```bash
docker run --rm --init --ipc=host \
  -e PYTEST_XDIST_AUTO_NUM_WORKERS=2 \
  playwright-qa-framework:local \
  -m smoke -n auto -v
```

Validated Firefox Smoke execution:

```bash
docker run --rm --init --ipc=host \
  -e QA_BROWSER=firefox \
  playwright-qa-framework:local \
  -m smoke -v
```

The Docker execution path reuses the existing `QA_*` runtime configuration and existing functional tests, markers, fixtures, assertions, diagnostics, and reporting integrations.

Recommended runtime flags are:

```text
--rm
--init
--ipc=host
```

When bind-mounted output should belong to the invoking WSL/Linux user, execution can additionally use:

```bash
--user "$(id -u):$(id -g)"
```

with:

```bash
-o cache_dir=/tmp/pytest_cache
```

Validated host-persistent output includes pytest-html reports, raw Allure result data, failure screenshots, Playwright traces, and Playwright videos through bind mounts to the relevant `reports/`, `allure-results/`, and `test-results/` directories.

Phase 5B validation does not establish complete Docker full-suite execution, separately validated Docker WebKit execution, or headed Docker execution.

Existing functional GitHub Actions jobs remain native. Phase 5C adds one dedicated exception: `visual-regression` builds the existing Phase 5B Docker image and runs only the isolated visual suite inside it.

### Visual Regression Validation

Phase 5C adds controlled Chromium-only visual regression validation.

The permanent visual suite is intentionally isolated from normal functional test collection and runs under:

```text
visual_tests/
```

with the registered:

```text
visual
```

marker.

Focused direct execution:

```bash
python -m pytest visual_tests -m visual --browser chromium -v
```

Canonical validation uses the existing project Docker environment:

```bash
docker build -t playwright-qa-framework:visual .

mkdir -p reports/visual

docker run --rm --init --ipc=host \
  -v "$PWD/visual_baselines:/app/visual_baselines:ro" \
  -v "$PWD/reports/visual:/app/reports/visual" \
  -e QA_BASE_URL=https://www.saucedemo.com \
  -e QA_BROWSER=chromium \
  -e QA_HEADED=false \
  playwright-qa-framework:visual \
  visual_tests -m visual --browser chromium -v
```

The canonical visual strategy requires:

* Chromium only
* headless execution
* fixed rendering conditions
* sequential execution without pytest-xdist
* approved baselines under `visual_baselines/chromium/`
* generated actual/diff evidence under `reports/visual/`
* read-only baseline mounts during normal comparison
* explicit baseline refresh only through `--update-visual-baselines`
* no Firefox/WebKit visual matrix
* no permanently failing `visual_user` CI test

The controlled `visual_user` mismatch was used only as a one-off validation that the comparator detects a meaningful visual defect and creates diff evidence.

The dedicated GitHub Actions `visual-regression` job depends on `quality`, runs separately from the existing functional jobs, and uploads:

```text
visual-regression-artifacts
```

with `if: always()` and seven-day retention.

AQA-0120 validation completed successfully with all seven workflow job executions passing and the visual artifact upload verified.

### Runtime Configuration Validation

Phase 4E provides focused runtime configuration validation through:

```bash
pytest tests/test_runtime_config.py
```

Runtime configuration validation should be included when a task or workstream changes:

* supported environment variables
* runtime defaults
* base URL behavior
* browser selection
* headed/headless behavior
* action or navigation timeout behavior
* assertion timeout behavior
* screenshot policy
* trace policy
* video policy
* pytest-playwright runtime integration

Representative environment-driven execution should additionally be used when the changed behavior requires it.

Example:

```bash
QA_BROWSER=chromium \
QA_HEADED=false \
QA_TIMEOUT_MS=20000 \
QA_EXPECT_TIMEOUT_MS=4000 \
pytest -m smoke -v
```

Invalid explicit runtime configuration should fail early rather than silently fall back to default values.

### Diagnostics Validation

Phase 4F provides runtime and failed-test diagnostics through:

```text
framework/diagnostics.py
```

and the framework-level Pytest hooks in:

```text
conftest.py
```

When a task or workstream changes diagnostics behavior, controlled validation should verify the affected behavior.

Relevant checks may include:

* effective runtime header
* xdist worker runtime-header de-duplication
* Pytest node ID
* `setup`, `call`, or `teardown` failure phase
* current page URL when available
* custom screenshot path after successful screenshot capture
* diagnostic-error output

Intentionally failing tests used only for diagnostics validation should remain temporary and should not be committed.

Phase 4F diagnostics do not create persistent project log files.

The same diagnostic model applies to Chromium, Firefox, and WebKit execution.

### Reporting Validation

When the task or workstream changes reporting behavior, local validation should cover the implemented report generation path.

Current Chromium full-suite reporting validation can use:

```bash
pytest -n auto -v \
  --html=reports/report.html \
  --self-contained-html \
  --alluredir=reports/allure-results \
  --clean-alluredir
```

Generate the Allure HTML report with:

```bash
allure generate reports/allure-results \
  --clean \
  -o reports/allure-report
```

Current generated reporting paths include:

```text
reports/report.html
reports/allure-results/
reports/allure-report/
reports/screenshots/
reports/visual/actual/
reports/visual/diff/
```

The Phase 5A cross-browser Smoke matrix additionally generates:

```text
reports/firefox-smoke-report.html
reports/webkit-smoke-report.html
```

Firefox and WebKit Smoke remain pytest-html-focused and do not generate dedicated Allure reports in CI.

The standalone Allure CLI must be available when local Allure HTML generation is required.

Generated reports, failure screenshots, and visual actual/diff evidence remain runtime output and should not be committed to Git. Approved visual baselines under `visual_baselines/chromium/` are reviewed repository assets and are intentionally version-controlled.

### Trace And Video Runtime Artifacts

Phase 4E provides optional Playwright trace and video policies through:

```text
QA_TRACE_POLICY
QA_VIDEO_POLICY
```

Both default to:

```text
off
```

When enabled, pytest-playwright runtime output is generated under:

```text
test-results/
```

Representative files include:

```text
trace.zip
video.webm
```

Generated traces and videos are runtime outputs and should not be committed to Git.

Phase 4F does not change trace or video lifecycle ownership.

Phase 5A reuses the same runtime policies without implementing separate trace or video lifecycle management.

Phase 5B also reuses these policies. Trace and video persistence inside Docker was validated through bind-mounted `test-results/` output without changing pytest-playwright lifecycle ownership.

### Marker-Based Validation

Selective marker-based checks may be used during implementation and review when relevant.

Current executable marker suites are:

```bash
pytest -m smoke -v
pytest -m regression -v
pytest -m ui -v
pytest -m security -v
pytest -m sorting -v
pytest -m navigation -v
pytest -m e2e -v
python -m pytest visual_tests -m visual --browser chromium -v
```

Useful marker combinations include:

```bash
pytest -m "smoke and ui" -v
pytest -m "regression and ui" -v
pytest -m "smoke and navigation" -v
pytest -m "regression and navigation" -v
```

Marker execution may also be scoped to a specific module.

Example:

```bash
pytest tests/test_checkout_page.py -m e2e -v
```

All current marker suites remain available for selective local validation.

Detailed marker semantics, test-independence expectations, parallel execution behavior, runtime configuration behavior, diagnostics, fixture responsibility, reporting compatibility, and cross-browser scope are documented in [Testing Strategy](testing-strategy.md).

### Marker Execution In CI

The current GitHub Actions pipeline provides dedicated Chromium marker-filtered CI execution for:

* Smoke
* Regression

The existing Smoke suite additionally executes through the Phase 5A matrix on:

* Firefox
* WebKit

The following functional marker suites do not currently have dedicated CI jobs:

* UI
* Security
* Sorting
* Navigation
* E2E

The `visual` marker is intentionally excluded from this list because it owns the dedicated Docker-based `visual-regression` CI job.

Tests carrying these functional markers still participate in the complete unfiltered Chromium full-suite CI execution.

Tests that also carry `smoke` additionally participate in representative Firefox and WebKit validation.

Dedicated marker execution in CI does not change marker semantics or local execution availability.

All functional browser-test CI executions use pytest-xdist worker-level parallelism. The dedicated visual regression job runs sequentially.

Chromium Smoke and Regression remain pytest-html-focused.

Firefox and WebKit Smoke remain pytest-html-focused.

The complete Chromium full-suite job additionally provides the advanced Allure reporting path.

All browser-test jobs use explicit runtime defaults, with the Phase 5A matrix supplying the appropriate Firefox or WebKit browser value.

Phase 4F diagnostics operate through the normal Pytest execution path in all current browser-test jobs.

Phase 5A does not introduce a cross-browser pytest marker.

## CI Validation

GitHub Actions separates code-quality validation from browser-test execution.

The Phase 4B job structure established the Chromium execution foundation:

```text
quality
├── smoke
├── regression
└── full-suite
```

The `quality` job executes first and validates:

```bash
ruff check .
black --check .
isort . --check-only
```

The quality job does not install Playwright browsers and does not use pytest-xdist.

Smoke, Regression, and full-suite all depend on successful `quality` validation.

They do not depend on each other.

Phase 4C introduced worker-level parallelism inside those existing browser jobs:

```text
quality
├── smoke
│   └── pytest-xdist workers
├── regression
│   └── pytest-xdist workers
└── full-suite
    └── pytest-xdist workers
```

Phase 4D added reporting capabilities while preserving that job structure:

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

Phase 4E introduced explicit runtime configuration to the existing three Chromium browser-test jobs without changing the CI topology at that time.

Current Chromium CI runtime defaults are:

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

Phase 4F introduced runtime and failed-test diagnostics through the existing Pytest execution path without changing the CI topology at that time.

Phase 5A extends the established Chromium CI jobs with a Firefox/WebKit Smoke matrix.

Phase 5B did not containerize the functional CI architecture. Those existing jobs continue to run natively on GitHub-hosted Ubuntu runners. Phase 5C later reuses the same project Docker image only for the dedicated visual regression job.

Docker therefore remains a general reproducible execution path and also serves as the canonical environment for Phase 5C visual comparison.

Current CI structure:

```text
quality
├── smoke [Chromium, native]
│   └── pytest-xdist
│       └── pytest-html
├── regression [Chromium, native]
│   └── pytest-xdist
│       └── pytest-html
├── full-suite [Chromium, native]
│   └── pytest-xdist
│       ├── pytest-html
│       ├── Allure results
│       └── Allure HTML report
├── cross-browser-smoke [native]
│   ├── Firefox
│   │   └── pytest-xdist
│   │       └── browser-specific pytest-html
│   └── WebKit
│       └── pytest-xdist
│           └── browser-specific pytest-html
└── visual-regression [Chromium, Docker]
    └── sequential visual checkpoints
```

The current CI strategy is:

* Chromium — primary complete regression browser
* Firefox — representative Smoke compatibility browser
* WebKit — representative Smoke compatibility browser
* Chromium-only visual regression in Docker
* headless browser execution
* pytest-xdist parallel execution for functional browser jobs
* sequential visual regression execution
* screenshot-on-failure enabled
* trace disabled by default
* video disabled by default
* runtime diagnostics through normal Pytest execution
* failed-test diagnostics through normal Pytest execution

All functional browser-test jobs and the dedicated visual regression job depend on `quality` but do not depend on each other.

The Firefox/WebKit matrix uses `fail-fast: false` so one browser failure does not cancel the other matrix execution.

### Smoke CI

The dedicated `smoke` job executes the existing Smoke suite on Chromium:

```bash
pytest -m smoke -n auto -v
```

The actual CI command additionally generates:

```text
reports/smoke-report.html
```

The job uploads:

```text
smoke-pytest-html-report
smoke-test-artifacts
```

Smoke does not generate a dedicated Allure report.

### Regression CI

The dedicated `regression` job executes the existing Regression suite on Chromium:

```bash
pytest -m regression -n auto -v
```

The actual CI command additionally generates:

```text
reports/regression-report.html
```

The job uploads:

```text
regression-pytest-html-report
regression-test-artifacts
```

Regression does not generate a dedicated Allure report.

### Full-Suite CI

The `full-suite` job executes the complete unfiltered Chromium automated test suite:

```bash
pytest -n auto -v \
  --html=reports/report.html \
  --self-contained-html \
  --alluredir=reports/allure-results \
  --clean-alluredir
```

The Chromium full-suite job remains the complete CI regression gate.

It also serves as the primary CI source for advanced Allure reporting.

After test execution, the workflow attempts to generate:

```text
reports/allure-report/
```

from:

```text
reports/allure-results/
```

when usable Allure result data exists.

The generated Allure report is published as:

```text
full-suite-allure-report
```

The job additionally uploads:

```text
pytest-html-report
test-artifacts
```

Dedicated Chromium Smoke and Regression execution provides targeted feedback without replacing full-suite validation.

Firefox/WebKit representative Smoke execution also does not replace complete Chromium regression validation.

### Cross-Browser Smoke CI

The Phase 5A `cross-browser-smoke` job executes the existing Smoke suite on Firefox and WebKit through a GitHub Actions matrix.

Current matrix configuration:

```yaml
needs: quality

strategy:
  fail-fast: false
  matrix:
    browser:
      - firefox
      - webkit
```

Each matrix entry:

* selects its browser through `QA_BROWSER=${{ matrix.browser }}`
* installs only its selected Playwright engine
* runs headless
* uses the existing `smoke` marker
* executes through pytest-xdist with `-n auto`
* uses existing Page Objects and scenario fixtures
* reuses Phase 4F diagnostics
* generates a self-contained browser-specific pytest-html report
* uploads browser-specific artifacts

Browser installation:

```bash
playwright install --with-deps ${{ matrix.browser }}
```

The core test command is:

```bash
pytest -m smoke -n auto -v
```

Browser-specific reports:

```text
reports/firefox-smoke-report.html
reports/webkit-smoke-report.html
```

Firefox artifacts:

```text
firefox-smoke-pytest-html-report
firefox-smoke-test-artifacts
```

WebKit artifacts:

```text
webkit-smoke-pytest-html-report
webkit-smoke-test-artifacts
```

Artifact uploads use `if: always()` and retain available outputs for seven days.

Firefox and WebKit do not generate dedicated Allure reports in CI.

Chromium is not duplicated in the cross-browser matrix because it already has dedicated Smoke, Regression, and full-suite jobs.

The matrix does not implement complete Firefox or WebKit Regression/full-suite validation.

### Visual Regression CI

The Phase 5C `visual-regression` job executes only the isolated visual suite.

It:

* depends on `quality`
* runs on `ubuntu-24.04`
* builds the existing repository Dockerfile
* runs Chromium headless
* executes sequentially without pytest-xdist
* mounts approved baselines read-only
* preserves generated `reports/visual/` output
* uploads `visual-regression-artifacts` through `if: always()`
* does not refresh baselines
* does not include Firefox or WebKit

Permanent CI uses only the approved `standard_user` visual checkpoints.

The controlled `visual_user` mismatch validation remains outside permanent CI.

### CI Triggers

The current GitHub Actions workflow runs automatically for:

* pushes to `main`
* pushes to `develop`
* Pull Requests targeting `main`
* Pull Requests targeting `develop`

The workflow can also be started manually through:

* `workflow_dispatch`

Regular pushes to feature, fix, documentation, refactor, or promotion branches do not automatically start CI unless the branch participates in a Pull Request targeting `main` or `develop`, or the workflow is started manually.

A manual workflow run may therefore be used to validate an active workstream branch before its final Pull Request when required by the workstream Definition of Done.

### CI Execution Boundaries

The current execution model combines:

* Phase 4B CI job structure
* Phase 4C pytest-xdist worker-level parallelism
* Phase 4D reporting
* Phase 4E runtime configuration
* Phase 4F diagnostics and fixture responsibility cleanup
* Phase 5A representative Playwright cross-browser Smoke validation
* Phase 5B containerized Playwright execution as a general reproducible execution path
* Phase 5C dedicated Docker-based Chromium visual regression CI validation

GitHub Actions may schedule Chromium Smoke, Regression, full-suite, Firefox Smoke, WebKit Smoke, and visual regression independently after `quality`.

This is **GitHub Actions job-level concurrency**.

The `cross-browser-smoke` matrix expands one job definition into Firefox and WebKit browser executions.

This is **GitHub Actions matrix expansion**.

Inside every functional browser-test execution, pytest-xdist distributes collected tests between workers. The visual regression job intentionally runs sequentially.

This is **Pytest worker-level parallelism**.

These mechanisms are separate and should not be treated as interchangeable.

Docker container execution is another distinct execution environment. General Phase 5B Docker validation may use sequential Pytest or pytest-xdist internally. Phase 5C additionally uses Docker inside one dedicated visual CI job; this still remains separate from GitHub Actions matrix expansion and pytest-xdist worker parallelism.

Reporting is a separate concern layered on top of execution.

Runtime configuration is another separate concern layered on top of execution.

Diagnostics are also layered onto the existing Pytest execution path without introducing a separate diagnostics job.

The current execution model does not introduce:

* complete Firefox Regression
* complete WebKit Regression
* complete Firefox full-suite execution
* complete WebKit full-suite execution
* complete three-browser regression parity
* browser-specific duplicate functional test modules
* a cross-browser pytest marker
* Docker-based GitHub Actions jobs other than the dedicated Phase 5C visual regression job
* workflow-dispatch runtime forms
* secrets for non-secret runtime values
* retries
* `continue-on-error`
* default trace retention
* default video retention
* Allure history persistence
* report hosting
* GitHub Pages reporting
* persistent project log files
* browser console capture
* network capture
* diagnostic-specific CI jobs
* Selenium execution

Detailed CI behavior, runtime defaults, diagnostics, reports, artifacts, retention, and failure handling are documented in [CI/CD Pipeline](ci-cd-pipeline.md).

### Workstream-Specific Validation

For workstream-specific stabilization tasks, scoped validation may be used before the full suite.

Examples:

```bash
pytest -v tests/test_login_page.py
pytest -v tests/test_inventory_page.py
pytest -v tests/test_product_details_page.py
pytest -v tests/test_cart_page.py
pytest -v tests/test_checkout_page.py
```

For runtime-configuration work:

```bash
pytest tests/test_runtime_config.py
```

For a single-page task, running the relevant module before the full suite is usually appropriate.

Example:

```bash
pytest -v tests/test_checkout_page.py
pytest -v
```

When a workstream affects parallel-safety assumptions, fixture responsibility, or xdist-compatible diagnostics, additionally run:

```bash
pytest -m smoke -n auto -v
pytest -m regression -n auto -v
pytest -n auto -v
```

When a workstream affects representative cross-browser compatibility, validate:

```bash
QA_BROWSER=firefox pytest -m smoke -n auto -v
QA_BROWSER=webkit pytest -m smoke -n auto -v
```

When a workstream affects containerized execution, validate the applicable Docker path, for example:

```bash
docker build -t playwright-qa-framework:local .
docker run --rm --init --ipc=host playwright-qa-framework:local -m smoke -v
docker run --rm --init --ipc=host -e PYTEST_XDIST_AUTO_NUM_WORKERS=2 playwright-qa-framework:local -m smoke -n auto -v
docker run --rm --init --ipc=host -e QA_BROWSER=firefox playwright-qa-framework:local -m smoke -v
```

Use the relevant bind mount when the scope affects report or browser-artifact persistence.

When a workstream affects visual regression, validate the dedicated Chromium visual path in the canonical Docker environment and verify the expected baseline/actual/diff ownership.

When a workstream affects runtime configuration, validate the focused configuration tests and relevant environment-driven execution.

When a workstream affects diagnostics, validate the relevant runtime and failed-test diagnostic behavior through controlled failures.

When a workstream affects reporting behavior, validate the implemented reporting path and expected report outputs.

When a workstream affects screenshot, trace, or video policy behavior, validate the relevant runtime artifacts.

The full Chromium test suite should still pass before a workstream is considered ready for merge unless a scoped validation exception is explicitly accepted.

For portfolio promotion into `main`, the full test suite and quality checks should pass before merge unless a specific scoped validation exception is explicitly accepted.

## Pull Request Review Checklist

Before merging a Pull Request, verify:

* CI pipeline passed
* required quality validation passed
* required Chromium browser-test jobs passed
* required Firefox/WebKit representative Smoke matrix executions passed
* dedicated visual regression CI execution passed when applicable
* `visual-regression-artifacts` is available when visual validation is in scope
* complete Chromium full-suite CI validation passed
* expected reports and artifacts are available when required by the workstream
* browser-specific Firefox/WebKit reports and artifacts are available when applicable
* no unrelated files are included
* no generated reports, screenshots, traces, videos, Allure outputs, cache files, or virtual environment files are tracked
* changed files match the intended task, workstream, cleanup, or promotion scope
* documentation is updated when needed
* test cases and automated tests are aligned
* marker documentation reflects current executable marker behavior when marker usage changes
* execution documentation reflects current sequential, parallel, cross-browser, and containerized behavior when execution strategy changes
* Docker documentation reflects the implemented Phase 5B path while distinguishing native functional CI from the dedicated Phase 5C Docker-based visual job
* Docker validation claims remain limited to the execution modes, browsers, and artifacts that were actually validated
* runtime configuration documentation reflects current settings, defaults, and CI behavior when runtime configuration changes
* diagnostics documentation reflects current runtime summary, failed-test context, and diagnostic-error behavior when diagnostics change
* fixture documentation reflects the current framework-hook and application-scenario responsibility boundary when fixture organization changes
* reporting documentation reflects current pytest-html, Allure, failure screenshot, visual actual/diff, trace, video, diagnostics, and artifact behavior when reporting or diagnostic behavior changes
* CI documentation reflects current workflow behavior and runtime defaults when CI execution changes
* GitHub Actions job concurrency is not confused with GitHub Actions matrix expansion, pytest-xdist worker parallelism, or Docker container execution
* Chromium remains documented as the primary complete regression browser
* Firefox and WebKit are documented as representative Smoke compatibility browsers
* complete three-browser Regression/full-suite coverage is not claimed
* Firefox/WebKit visual regression or a visual browser matrix is not claimed
* approved visual baseline ownership is distinguished from generated actual/diff output
* controlled `visual_user` mismatch validation is not described as a permanent failing CI test
* Page Object responsibilities remain logically separated
* shared authenticated-page behavior remains owned by the correct abstraction
* reusable assertion helpers remain focused on shared validation logic
* test data remains centralized where practical
* Cart-owned checkout entry behavior remains separated from detailed checkout behavior
* Checkout Information, Checkout Overview, and Checkout Complete behavior remain owned by Checkout tests
* implemented features are not mixed with planned future features
* commit message for squash merge is clear
* target branch is correct

For regular feature work, the target branch should usually be:

```text
develop
```

For portfolio promotion, the target branch should be:

```text
main
```

## Portfolio Promotion Checklist

Before promoting `develop` to `main`, verify:

* `develop` contains a completed and validated project snapshot
* full local validation passed or a scoped validation exception is explicitly accepted
* CI on the promotion Pull Request passed
* README reflects the stable portfolio state
* documentation does not contain stale workstream-finalization wording
* documentation reflects current marker definitions and execution commands
* documentation reflects current sequential and parallel execution behavior
* documentation reflects the implemented cross-browser Smoke strategy
* documentation reflects the implemented Phase 5B containerized Playwright execution path
* documentation reflects the implemented Phase 5C visual regression strategy
* documentation reflects the dedicated Docker-based Chromium visual CI job and `visual-regression-artifacts`
* documentation distinguishes direct WSL/Linux execution, general Docker execution, native functional GitHub Actions CI, and the dedicated Docker-based visual regression CI job
* documentation distinguishes Chromium full regression from Firefox/WebKit representative Smoke
* documentation reflects current runtime configuration behavior
* documentation reflects current diagnostics behavior
* documentation reflects current fixture responsibility boundaries
* documentation reflects current reporting behavior
* documentation reflects current CI execution behavior and runtime defaults
* documentation clearly separates implemented scope from planned future scope
* test case documentation is aligned with automated coverage
* generated reports, screenshots, traces, videos, Allure outputs, cache files, and virtual environment files are not tracked
* the promoted state is suitable for recruiters or technical reviewers
* future work remains directed through `develop`

## Post-Merge Local Cleanup

### After Merge Into `develop`

After a Pull Request is squash merged into `develop`, update the local repository:

```bash
git checkout develop
git pull origin develop
```

Then optionally delete the completed local source branch if it is no longer required for related work:

```bash
git branch -d feature/<short-description>
```

For a refactor workstream branch:

```bash
git branch -d refactor/<short-description>
```

If the remote branch was deleted on GitHub, clean stale remote references:

```bash
git fetch --prune
```

### After Promotion Into `main`

After a Pull Request is squash merged into `main`, update the local repository:

```bash
git checkout main
git pull origin main
git checkout develop
git pull origin develop
git fetch --prune
```

Future feature, fix, documentation, refactor, and framework maturity work should continue from `develop`.

## Phase And Workstream Checkpoint Strategy

Before moving to the next major project phase or before merging a completed workstream, a checkpoint task should be completed.

A checkpoint task should verify:

* completed scope
* test coverage
* local validation
* relevant scoped test execution
* relevant marker suite execution where applicable
* runtime configuration validation where applicable
* diagnostics validation where applicable
* fixture responsibility and isolation where applicable
* parallel validation where required by the active scope
* cross-browser validation where required by the active scope
* containerized execution validation where required by the active scope
* Docker report and browser-artifact persistence where required by the active scope
* visual baseline/actual/diff validation where required by the active scope
* visual CI artifact validation where required by the active scope
* reporting validation where required by the active scope
* screenshot, trace, or video artifact validation where required by the active scope
* full suite execution or accepted scoped validation
* CI status
* expected reports and artifacts
* Firefox/WebKit browser-specific reports and artifacts where applicable
* documentation status
* Git status
* cleanup needs
* generated files and ignored artifacts
* readiness for the next phase or merge

This prevents new work from being built on top of unstable or outdated project state.

Example checkpoint tasks:

```text
AQA-0041 — Review Phase 2 And Prepare Phase 3 Scope
AQA-0064 — Review And Stabilize Cart Workstream
AQA-0073 — Phase 3C Final Validation And Documentation Sync
AQA-0082 — Checkout Workstream Final Validation And Documentation Sync
AQA-0114 — Phase 5A Cross-Browser Validation Checkpoint
AQA-0117 — Phase 5B Containerized Execution Closing Checkpoint
AQA-0122 — Phase 5C Visual Regression Closing Checkpoint
```

A separate portfolio promotion review may also be used when a completed phase is promoted from `develop` to `main`.

## Summary

This strategy ensures:

* predictable development process
* clean Git history
* controlled integration workflow
* controlled portfolio promotion workflow
* reliable CI quality gating
* dedicated parallel Chromium Smoke CI validation
* dedicated parallel Chromium Regression CI validation
* parallel complete Chromium full-suite CI regression validation
* representative Firefox Smoke CI validation
* representative WebKit Smoke CI validation
* reproducible Docker-based Playwright execution
* validated sequential and pytest-xdist Docker Smoke execution
* Docker reuse of existing `QA_*` runtime configuration
* bind-mounted Docker report and browser-artifact persistence
* controlled Chromium visual regression validation
* approved visual baseline ownership
* explicit visual baseline refresh workflow
* dedicated Docker-based `visual-regression` CI job
* independent `visual-regression-artifacts`
* consistent sequential local validation
* supported pytest-xdist parallel validation
* centralized runtime configuration validation
* explicit local and CI runtime defaults
* lightweight runtime and failed-test diagnostics
* clear framework-hook and application-fixture responsibility separation
* configurable screenshot, trace, and video policies
* complementary pytest-html and Allure reporting
* browser-specific Firefox/WebKit pytest-html reporting
* independent browser-specific CI artifacts
* normalized marker-based selective execution
* clear separation between GitHub Actions job concurrency, matrix expansion, Pytest worker parallelism, sequential visual execution, and Docker container execution
* clear separation between runtime configuration and functional test logic
* clear separation between browser selection and marker semantics
* clear separation between diagnostics and persistent logging
* clear separation between generated runtime outputs and repository content
* professional repository standards
* scalable workflow for future collaboration
* clear separation between active work, integration, and stable portfolio state

Chromium remains the primary complete regression browser.

Firefox and WebKit execute representative Smoke compatibility validation without complete Regression/full-suite parity.

Phase 5B Docker execution is implemented as an additional reproducible path alongside direct WSL/Linux execution and native functional GitHub Actions CI. Phase 5B was formally closed through AQA-0117.

Phase 5C Visual Regression Testing is implemented and CI-validated. It reuses the existing Docker environment for one dedicated Chromium visual job without moving the functional CI jobs into Docker.

Formal Phase 5C roadmap closure remains owned by AQA-0122.

The detailed CI, runtime configuration, diagnostics, reporting, containerized-execution, and visual-regression boundaries remain documented in [CI/CD Pipeline](ci-cd-pipeline.md).
