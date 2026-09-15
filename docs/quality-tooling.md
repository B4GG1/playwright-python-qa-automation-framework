# Quality Tooling

This document describes the code quality, validation, execution, and reporting tooling used in the QA automation framework.

The goal of quality tooling is to keep the codebase readable, consistent, maintainable, observable, and safe to extend as the framework grows.

The tooling described here supports local development, selective test execution, sequential and parallel Pytest execution, reporting, failure diagnostics, Pull Request validation, CI quality gates, and stable portfolio promotion.

## Tooling Overview

The project currently uses:

* Ruff for linting and static checks
* Black for Python code formatting
* isort for import sorting
* pre-commit for local quality validation
* Pytest as the main automated test runner
* pytest-xdist for worker-level parallel Pytest execution
* pytest-html for lightweight HTML reporting
* allure-pytest for Allure result collection
* Allure CLI for Allure HTML report generation
* Playwright assertions for browser and UI validation
* failure screenshots for browser-test evidence
* GitHub Actions artifacts for CI report and runtime-output retention

These tools support local development and CI validation.

## Ruff

Ruff is used for fast Python linting and static code analysis.

Current responsibilities:

* detecting common Python issues
* enforcing selected linting rules
* validating import-related rules
* supporting consistent code quality across the project

Run Ruff locally:

```bash
ruff check .
```

Ruff configuration is stored in:

```text
pyproject.toml
```

Current Ruff configuration:

```toml
[tool.ruff]
line-length = 200
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "I"]

[tool.ruff.lint.isort]
known-first-party = ["config", "framework", "pages", "test_data", "tests"]
```

## Black

Black is used as the main Python code formatter.

It enforces consistent Python formatting across the project.

Check formatting without modifying files:

```bash
black --check .
```

Format files locally:

```bash
black .
```

Black configuration is stored in:

```text
pyproject.toml
```

Current Black configuration:

```toml
[tool.black]
line-length = 100
target-version = ['py312']
```

## isort

isort is used to organize Python imports.

The project uses Black-compatible isort configuration.

Check import sorting without modifying files:

```bash
isort . --check-only
```

Sort imports locally:

```bash
isort .
```

isort configuration is stored in:

```text
pyproject.toml
```

Current isort configuration:

```toml
[tool.isort]
profile = "black"
line_length = 100
```

## pre-commit

pre-commit runs configured quality checks before a commit is created.

Current pre-commit hooks include:

* Ruff
* Black
* isort

Install hooks locally:

```bash
pre-commit install
```

Run all hooks manually:

```bash
pre-commit run --all-files
```

Current pre-commit hook sources include:

* `astral-sh/ruff-pre-commit`
* `psf/black`
* `pycqa/isort`

The purpose of pre-commit is to catch formatting, import sorting, and linting issues before changes are committed.

## Pytest

Pytest is the main automated test runner.

Current responsibilities include:

* executing Playwright UI tests
* supporting fixtures
* supporting parametrized tests
* supporting marker-based test categorization
* supporting selective suite execution
* supporting sequential test execution
* supporting pytest-xdist worker-level parallel execution
* integrating with Playwright
* integrating with pytest-html
* integrating with allure-pytest
* producing results used by local validation and CI

Run the complete test suite sequentially:

```bash
pytest -v
```

Run the complete suite in parallel:

```bash
pytest -n auto -v
```

Sequential execution remains supported.

Parallel execution is an additional validated execution mode and does not replace the sequential baseline.

## pytest-xdist

pytest-xdist provides worker-level parallel execution for the current Pytest suite.

Current implemented usage includes:

* parallel Smoke execution
* parallel Regression execution
* parallel full-suite execution
* local parallel validation
* parallel execution inside existing GitHub Actions browser-test jobs
* compatibility with pytest-html
* compatibility with Allure result collection
* compatibility with failure screenshot handling

Approved commands:

```bash
pytest -m smoke -n auto -v
pytest -m regression -n auto -v
pytest -n auto -v
```

`-n auto` allows pytest-xdist to determine the worker count according to the available execution environment.

The current test suite was validated for worker-safe execution during Phase 4C.

Validated areas included:

* Playwright fixture isolation
* browser-state independence
* Cart setup
* Checkout setup
* logout and re-login persistence
* E2E checkpoint independence
* parametrized scenario independence
* failure screenshot behavior
* report output behavior

No sequential-only test exceptions were identified.

Phase 4D reporting remains compatible with the same worker-level execution model.

### Current Executable Markers

Current registered pytest markers are:

* `smoke`
* `regression`
* `ui`
* `security`
* `sorting`
* `navigation`
* `e2e`

Marker definitions are stored in:

```text
pytest.ini
```

The project uses strict marker validation through `--strict-markers`, so every executable marker used by tests must be registered in `pytest.ini`.

Detailed marker semantics and assignment rules are documented in:

```text
docs/testing-strategy.md
```

### Marker-Based Test Execution

Run Smoke sequentially:

```bash
pytest -m smoke -v
```

Run Smoke in parallel:

```bash
pytest -m smoke -n auto -v
```

Run Regression sequentially:

```bash
pytest -m regression -v
```

Run Regression in parallel:

```bash
pytest -m regression -n auto -v
```

Run UI:

```bash
pytest -m ui -v
```

Run Security:

```bash
pytest -m security -v
```

Run Sorting:

```bash
pytest -m sorting -v
```

Run Navigation:

```bash
pytest -m navigation -v
```

Run the primary E2E checkpoint suite:

```bash
pytest -m e2e -v
```

Markers describe different dimensions of test intent and may be combined.

Examples:

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

Parallel execution changes how collected tests are distributed between workers.

It does not change marker semantics.

Reporting also does not change marker semantics.

### Smoke And Regression

Smoke tests provide fast representative validation of critical behavior.

Regression tests provide broader or deeper validation across expanded applicable cases.

Smoke and Regression are not automatically assigned together.

Representative coverage should normally use Smoke, while expanded or all-cases coverage should normally use Regression.

Both Smoke and Regression are executed as dedicated GitHub Actions CI jobs.

Both dedicated jobs use pytest-xdist worker-level parallel execution.

Both dedicated jobs remain focused on pytest-html reporting.

### UI

The `ui` marker is used when visibility, presentation, state, or direct UI behavior is materially validated.

A Playwright test does not automatically require the `ui` marker.

The UI marker does not currently have a dedicated CI job.

### Security

The `security` marker covers authentication access control and protected-route validation.

Current Security coverage includes unauthenticated access attempts to protected areas such as:

* Inventory
* Cart
* Product Details
* Checkout Information
* Checkout Overview
* Checkout Complete

The Security marker does not currently have a dedicated CI job.

### Sorting

The `sorting` marker identifies product sorting behavior.

Current sorting coverage includes:

* product name A to Z
* product name Z to A
* product price low to high
* product price high to low

The Sorting marker does not currently have a dedicated CI job.

### Navigation

The `navigation` marker identifies meaningful page transitions.

The authentication Login → Inventory transition is intentionally excluded from the Navigation suite.

Navigation may be combined with Smoke or Regression depending on whether the scenario is representative or expanded.

The Navigation marker does not currently have a dedicated CI job.

### End-to-End

The `e2e` marker identifies independent checkpoints that collectively form the primary purchase journey.

The E2E suite does not rely on:

* shared test state
* execution order
* one monolithic browser journey

Each E2E checkpoint prepares its own state through fixtures or test setup and can execute independently.

Run the complete logical E2E checkpoint suite with:

```bash
pytest -m e2e -v
```

The E2E marker does not currently have a dedicated CI job.

Tests carrying UI, Security, Sorting, Navigation, or E2E markers still participate in the complete unfiltered full-suite CI execution.

Because full-suite CI uses pytest-xdist, those tests may execute on different workers.

Because full-suite CI also collects Allure results, those tests are included in the advanced full-suite report.

## Playwright Assertions

Playwright assertions are used for browser and UI state validation.

Current assertion patterns include:

* checking URLs after navigation
* checking element visibility
* checking hidden state
* checking form field attributes
* checking authentication redirects
* checking Inventory visibility
* checking product card content
* checking Product Details content
* checking Cart state
* checking cart badge state
* checking Add to cart and Remove button states
* checking checkout validation errors
* checking Checkout Overview content
* checking Checkout Complete content

Playwright assertions should be preferred for browser and UI state because they include built-in waiting behavior.

Plain Python assertions are appropriate for comparisons involving already extracted or calculated values such as:

* product names
* product prices
* sorted lists
* expected strings
* calculated checkout totals

## pytest-html

pytest-html provides the lightweight HTML reporting layer.

It remains implemented for:

* local reporting where requested
* Smoke CI
* Regression CI
* full-suite CI

Current CI report paths are:

```text
reports/smoke-report.html
reports/regression-report.html
reports/report.html
```

Smoke and Regression intentionally remain pytest-html-focused.

The full-suite job retains pytest-html while additionally collecting Allure result data.

Allure does not replace pytest-html.

## Allure Pytest Integration

`allure-pytest` provides the Python-side integration between Pytest and Allure.

Its responsibility is to generate structured Allure result data during test execution.

Current output location:

```text
reports/allure-results/
```

Collect Allure results sequentially:

```bash
pytest -v \
  --alluredir=reports/allure-results \
  --clean-alluredir
```

Collect Allure results through pytest-xdist:

```bash
pytest -n auto -v \
  --alluredir=reports/allure-results \
  --clean-alluredir
```

Allure result collection is compatible with both supported execution modes:

* sequential Pytest execution
* pytest-xdist worker-level parallel execution

`--clean-alluredir` prevents stale result data from previous runs from being mixed into the current execution.

## Allure CLI

The standalone Allure CLI converts generated result data into a browsable HTML report.

It is separate from the Python `allure-pytest` dependency.

Installing `allure-pytest` does not itself provide the standalone HTML report generator.

Verify local CLI availability:

```bash
allure --version
```

Generate the Allure HTML report:

```bash
allure generate reports/allure-results \
  --clean \
  -o reports/allure-report
```

Current generated report location:

```text
reports/allure-report/
```

The CLI is therefore a prerequisite when local Allure HTML report generation is required.

In CI, the full-suite job prepares the required report-generation environment before generating the Allure HTML report.

## Failure Screenshots

Browser-test failures use the existing screenshot mechanism in `conftest.py`.

The hook operates on failed Pytest test calls.

Current screenshot location:

```text
reports/screenshots/
```

Screenshot filenames contain:

* the test name
* a UTC timestamp

The screenshot is captured once.

After successful screenshot capture, the same PNG file is attached to the Allure result as:

```text
Failure screenshot
```

when Allure result collection is active.

The Allure integration does not create a second screenshot.

This preserves a single failure-evidence capture path.

If screenshot capture fails, no Allure screenshot attachment is attempted because no screenshot file exists.

If the Allure attachment fails after a successful screenshot capture, the original screenshot remains available under:

```text
reports/screenshots/
```

This keeps browser failure evidence useful independently from the Allure report.

## Reporting Compatibility

Current reporting behavior supports:

* sequential Pytest execution
* pytest-xdist worker-level parallel execution
* pytest-html generation
* Allure result collection
* failure screenshot capture
* failure screenshot attachment to Allure
* generated Allure HTML reports

No sequential-only reporting exception is required for the current framework.

The reporting layer does not change test isolation requirements.

Tests must remain independent regardless of whether reporting is enabled.

## Generated Runtime Output

Reporting output is generated runtime data rather than repository source content.

Current generated paths include:

```text
reports/
reports/screenshots/
reports/allure-results/
reports/allure-report/
```

These outputs are used for:

* local debugging
* failure analysis
* execution evidence
* report inspection
* CI artifact publishing

They should not be committed to Git.

The repository ignore policy includes:

```text
reports/*
!reports/.gitkeep

allure-results/
allure-report/
```

The implemented Allure paths are nested under:

```text
reports/
```

and are therefore already covered by the `reports/*` ignore rule.

The additional root-level Allure ignore entries protect against accidental output generated with alternate paths.

## Local Quality Workflow

Before pushing changes or opening a Pull Request where full validation is required, the standard sequential local validation is:

```bash
ruff check .
black --check .
isort . --check-only
pytest -v
```

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

Sequential execution remains a supported baseline for normal local validation.

### Parallel Validation

When parallel execution, worker safety, fixture isolation, or execution behavior is part of the validation scope, use:

```bash
pytest -m smoke -n auto -v
pytest -m regression -n auto -v
pytest -n auto -v
```

The current suite passed these validations during Phase 4C stabilization.

Parallel validation is not required for every unrelated implementation task unless the active scope affects parallel-safety assumptions.

### Reporting Validation

When reporting behavior is part of the active scope, validate both result collection and report generation.

Example complete parallel reporting validation:

```bash
pytest -n auto -v \
  --html=reports/report.html \
  --self-contained-html \
  --alluredir=reports/allure-results \
  --clean-alluredir
```

Then generate the advanced report:

```bash
allure generate reports/allure-results \
  --clean \
  -o reports/allure-report
```

The expected outputs are:

```text
reports/report.html
reports/allure-results/
reports/allure-report/
```

Failure screenshot behavior should additionally be validated when changes affect:

* `conftest.py`
* screenshot handling
* Allure attachment behavior

## Scoped Local Validation

During implementation, relevant scoped validation may be run before the full suite.

### Login Changes

```bash
pytest -v tests/test_login_page.py
pytest -m security -v
pytest -m "smoke and ui" -v
pytest -m "regression and ui" -v
```

### Inventory Changes

```bash
pytest -v tests/test_inventory_page.py
pytest -m sorting -v
pytest tests/test_inventory_page.py -m navigation -v
```

### Product Details Changes

```bash
pytest -v tests/test_product_details_page.py
pytest tests/test_product_details_page.py -m navigation -v
pytest tests/test_product_details_page.py -m regression -v
```

### Cart Changes

```bash
pytest -v tests/test_cart_page.py
pytest tests/test_cart_page.py -m navigation -v
pytest tests/test_cart_page.py -m regression -v
```

### Checkout Changes

```bash
pytest -v tests/test_checkout_page.py
pytest tests/test_checkout_page.py -m navigation -v
pytest tests/test_checkout_page.py -m regression -v
pytest tests/test_checkout_page.py -m e2e -v
```

### Primary Purchase Journey Changes

When changes affect the main purchase journey, run:

```bash
pytest -m e2e -v
```

Scoped validation should normally be followed by the complete test suite before a workstream is considered ready for merge unless a scoped validation exception is explicitly accepted.

## Full Workstream Validation

For checkpoint, stabilization, or portfolio promotion work, the following page-level validation may be useful:

```bash
pytest -v tests/test_login_page.py
pytest -v tests/test_inventory_page.py
pytest -v tests/test_product_details_page.py
pytest -v tests/test_cart_page.py
pytest -v tests/test_checkout_page.py
pytest -v
```

Quality checks should also be run:

```bash
ruff check .
black --check .
isort . --check-only
```

When parallel execution is relevant to the workstream, additionally run:

```bash
pytest -m smoke -n auto -v
pytest -m regression -n auto -v
pytest -n auto -v
```

When reporting is relevant to the workstream, additionally validate:

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

## CI Quality Checks

GitHub Actions validates the project automatically for the configured workflow triggers.

The current pipeline combines:

* Phase 4B CI job structure
* Phase 4C parallel execution
* Phase 4D reporting

Current job structure:

```text
quality
├── smoke
├── regression
└── full-suite
```

The `quality` job executes first.

After successful quality validation, Smoke, Regression, and full-suite become independently executable browser jobs.

GitHub Actions may schedule these jobs concurrently.

Inside each browser-test job, pytest-xdist distributes tests between workers.

These are separate concurrency layers.

Reporting operates on top of those execution layers.

### Quality Job

The quality job executes:

```bash
ruff check .
black --check .
isort . --check-only
```

It also performs:

* repository checkout
* Python 3.12 setup
* dependency installation

The quality job does not:

* install Playwright Chromium
* execute browser tests
* use pytest-xdist
* generate browser-test reports

A failure in the quality job prevents all three browser jobs from starting.

### Smoke CI Job

The Smoke CI job executes the approved Smoke marker suite through pytest-xdist.

Core command:

```bash
pytest -m smoke -n auto -v
```

The current workflow also generates:

```text
reports/smoke-report.html
```

and uploads Smoke-specific artifacts.

Smoke remains pytest-html-focused.

It does not generate a dedicated Allure report.

### Regression CI Job

The Regression CI job executes the approved Regression marker suite through pytest-xdist.

Core command:

```bash
pytest -m regression -n auto -v
```

The current workflow also generates:

```text
reports/regression-report.html
```

and uploads Regression-specific artifacts.

Regression remains pytest-html-focused.

It does not generate a dedicated Allure report.

### Full-Suite CI Job

The full-suite job executes the complete unfiltered test suite through pytest-xdist.

Current command:

```bash
pytest -n auto -v \
  --html=reports/report.html \
  --self-contained-html \
  --alluredir=reports/allure-results \
  --clean-alluredir
```

This execution produces:

```text
reports/report.html
reports/allure-results/
```

The full-suite job remains the primary full regression gate.

It is also the primary CI source for the advanced Allure report.

After Pytest execution, the workflow attempts to generate:

```text
reports/allure-report/
```

from:

```text
reports/allure-results/
```

when usable Allure result data exists.

Dedicated Smoke and Regression jobs provide additional suite-specific feedback but do not replace full-suite validation.

### Allure CI Tooling

The full-suite job prepares:

* Java 17
* Allure CLI

Java is configured through:

```text
actions/setup-java@v4
```

using Temurin 17.

The Allure CLI is installed with:

```bash
npm install -g allure-commandline
allure --version
```

These prerequisites are used for HTML generation.

They are not added to Smoke or Regression.

### Allure Generation After Test Failure

The Allure HTML generation step uses:

```yaml
if: always()
```

The step checks whether:

```text
reports/allure-results/
```

exists and contains result files before invoking the CLI.

This allows Allure HTML generation to be attempted after failed full-suite test execution when usable result data exists.

A failed test command still fails the `full-suite` job.

Reporting does not convert failed tests into successful CI validation.

### CI Marker Coverage

Dedicated CI jobs currently exist for:

* Smoke
* Regression

Dedicated CI jobs do not currently exist for:

* UI
* Security
* Sorting
* Navigation
* E2E

These markers remain available for selective local validation.

Tests assigned to them still run through the complete full-suite CI job.

## GitHub Actions Concurrency And pytest-xdist

The current execution model contains two distinct concurrency layers.

GitHub Actions job-level concurrency:

```text
quality
├── smoke
├── regression
└── full-suite
```

After `quality` succeeds, the browser jobs may run independently.

pytest-xdist worker-level parallelism:

```text
smoke / regression / full-suite job
        ↓
pytest -n auto
        ↓
xdist workers
```

GitHub Actions concurrency controls independent workflow jobs.

pytest-xdist controls test distribution inside each individual browser-test job.

These mechanisms should not be treated as equivalent.

Allure reporting does not add another concurrency layer.

## CI Reports And Artifacts

Current browser-test jobs generate self-contained pytest-html reports.

### Smoke Artifacts

```text
smoke-pytest-html-report
smoke-test-artifacts
```

### Regression Artifacts

```text
regression-pytest-html-report
regression-test-artifacts
```

### Full-Suite Artifacts

```text
pytest-html-report
full-suite-allure-report
test-artifacts
```

The dedicated Allure artifact publishes:

```text
reports/allure-report/
```

The broader full-suite runtime artifact continues to publish:

```text
reports/
```

Artifact upload steps use:

```yaml
if: always()
```

This allows available reports and runtime outputs to be uploaded when an executing browser-test command fails.

If the quality job fails, browser jobs are not started and therefore do not generate browser-test artifacts for that workflow run.

Current artifact retention is:

```text
7 days
```

The reporting and failure-evidence model supports the current pytest-xdist execution strategy.

No sequential-only reporting exception is required.

Detailed CI behavior is documented in:

```text
docs/ci-cd-pipeline.md
```

## Quality Gates

The project uses quality gates at multiple levels.

### Local Quality Gate

Before commit, push, or Pull Request where full validation is required:

```bash
ruff check .
black --check .
isort . --check-only
pytest -v
```

### Parallel Execution Gate

When the scope affects worker-level execution or test isolation:

```bash
pytest -m smoke -n auto -v
pytest -m regression -n auto -v
pytest -n auto -v
```

### Reporting Gate

When reporting behavior changes:

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

The validation should confirm:

* pytest-html output is generated
* Allure result data is generated
* Allure HTML generation succeeds
* failure screenshots remain available when applicable
* Allure attachments reuse the existing screenshot
* generated output remains outside tracked repository content

### Pre-commit Quality Gate

Run all configured hooks:

```bash
pre-commit run --all-files
```

### Scoped Workstream Quality Gate

Run the relevant test module and marker suites for the changed behavior.

Examples:

```bash
pytest -v tests/test_login_page.py
pytest -v tests/test_inventory_page.py
pytest -v tests/test_product_details_page.py
pytest -v tests/test_cart_page.py
pytest -v tests/test_checkout_page.py
```

The scoped validation should normally be followed by full-suite validation before merge unless an explicit scoped-validation exception is accepted.

### CI Quality Gate

Before merging a Pull Request:

* GitHub Actions must pass
* Ruff must pass
* Black validation must pass
* isort validation must pass
* required browser-test jobs must pass
* full-suite validation must pass
* expected pytest-html artifacts should be available
* expected full-suite Allure artifact should be available
* runtime artifacts should remain available for failure investigation when generated

The current dependency model means:

```text
quality
├── smoke
├── regression
└── full-suite
```

A failed quality job prevents browser execution.

Smoke, Regression, and full-suite do not depend on each other.

All three browser-test jobs currently execute Pytest through pytest-xdist.

### Portfolio Promotion Quality Gate

Before promoting `develop` to `main`:

* full local validation should pass when possible
* CI on the promotion Pull Request should pass
* documentation should match implemented framework behavior
* reporting documentation should match the actual runtime and CI implementation
* planned functionality should not be presented as implemented
* generated reports, screenshots, Allure outputs, caches, and virtual environment files should not be tracked
* the resulting `main` state should be suitable as a stable portfolio snapshot

## Reporting Scope Boundaries

The current implemented reporting stack includes:

* pytest-html
* allure-pytest
* Allure CLI HTML generation
* failure screenshots
* Allure failure screenshot attachments
* GitHub Actions artifacts

Current reporting does not implement:

* Allure history persistence
* trend-history storage
* report hosting
* GitHub Pages reporting
* trace policy
* video policy
* retries
* cross-browser reporting

Runtime environment configuration also remains outside Phase 4D reporting scope.

## Current Quality Status

The current quality tooling supports the implemented Playwright framework covering Login, Inventory, Product Details, Cart, and Checkout areas.

Current capabilities include:

* Page Object Model implementation
* shared authenticated-page behavior through `AppPage`
* reusable product and checkout assertion helpers
* reusable pytest fixtures
* centralized login, product, and checkout test data
* parametrized tests
* normalized marker-based test categorization
* selective local Smoke execution
* selective local Regression execution
* selective local UI execution
* selective local Security execution
* selective local Sorting execution
* selective local Navigation execution
* independent E2E checkpoint execution
* supported sequential Pytest execution
* pytest-xdist worker-level parallel execution
* parallel Smoke validation
* parallel Regression validation
* parallel full-suite validation
* local quality validation
* dedicated CI quality validation
* dedicated parallel Smoke CI execution
* dedicated parallel Regression CI execution
* parallel complete full-suite CI validation
* pytest-html report generation
* Allure result collection
* Allure HTML report generation
* failure screenshot capture
* failure screenshot attachment to Allure
* job-specific CI artifact upload
* dedicated full-suite Allure artifact
* generated runtime-output isolation

Current CI execution and reporting model:

```text
quality
├── smoke
│   └── pytest-xdist workers
│       └── pytest-html
├── regression
│   └── pytest-xdist workers
│       └── pytest-html
└── full-suite
    └── pytest-xdist workers
        ├── pytest-html
        ├── Allure results
        └── Allure HTML report
```

The quality job is the prerequisite gate for browser-test execution.

Smoke and Regression have dedicated CI jobs.

UI, Security, Sorting, Navigation, and E2E remain selectively executable without dedicated CI jobs.

The full-suite job remains the complete unfiltered regression gate and the primary source of the CI Allure report.

No sequential-only test or reporting exceptions are required for the current implemented execution model.

## Quality Goals

The project quality tooling supports:

* consistent formatting
* readable and maintainable code
* automated local validation
* reduced formatting conflicts
* consistent import organization
* reliable Pytest execution
* sequential and parallel test execution
* selective marker-based local validation
* worker-safe test independence
* lightweight pytest-html reporting
* advanced Allure reporting
* reusable failure evidence
* dedicated Smoke CI feedback
* dedicated Regression CI feedback
* complete full-suite CI regression protection
* reliable CI quality gates
* useful CI execution artifacts
* stable workstream integration
* professional Pull Request workflow
* traceability between test cases and automated coverage
* safe checkpoint validation
* stable portfolio promotion

## Current Phase Boundaries

### Phase 4B — CI Execution Strategy

Implemented capabilities include:

* separate code-quality validation
* dedicated Smoke CI execution
* dedicated Regression CI execution
* complete full-suite execution
* job-specific pytest-html reports and artifacts
* independent browser-test job scheduling after `quality`

### Phase 4C — Parallel Execution

Implemented capabilities include:

* pytest-xdist worker-level parallel execution
* local parallel Smoke execution
* local parallel Regression execution
* local parallel full-suite execution
* sequential execution as a supported fallback
* fixture and test independence validation
* parametrized and E2E independence validation
* parallel Smoke CI execution
* parallel Regression CI execution
* parallel full-suite CI execution
* preserved Phase 4B CI job structure
* preserved pytest-html report and artifact behavior
* Chromium-only execution scope

GitHub Actions job-level concurrency and pytest-xdist worker-level parallelism are separate execution mechanisms.

### Phase 4D — Reporting Upgrade

Implemented reporting capabilities include:

* allure-pytest integration
* local Allure result collection
* local Allure HTML report generation
* Allure CLI as the HTML-generation prerequisite
* existing failure screenshot reuse
* failure screenshot attachment to Allure
* sequential reporting compatibility
* pytest-xdist reporting compatibility
* full-suite CI Allure result collection
* full-suite CI Allure HTML generation
* dedicated `full-suite-allure-report` artifact
* preservation of existing pytest-html reports
* preservation of existing browser-test artifacts
* generated reporting output excluded from version-controlled repository content

The Phase 4D workstream should not be treated as fully completed until its remaining approved tasks and final checkpoint are completed.

Current Phase 4D does not implement:

* Allure history persistence
* trend history
* hosted reports
* GitHub Pages reporting
* trace/video policy
* retries
* cross-browser reporting
* runtime environment configuration

## Future Improvements

Possible future quality tooling improvements include:

* stricter Ruff rules where justified
* type checking with mypy
* test coverage reporting
* JUnit XML output
* refined pre-commit configuration
* stronger failure diagnostics
* Allure history and trend reporting when approved
* hosted reporting when approved
* additional CI execution improvements where justified

pytest-xdist parallel execution and current Allure reporting are already implemented and should not be listed as future-only functionality.

Future improvements should not be described as implemented until the corresponding project work is completed and validated.