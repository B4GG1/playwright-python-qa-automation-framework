# Quality Tooling

This document describes the code quality and validation tooling used in the QA automation framework.

The goal of quality tooling is to keep the codebase readable, consistent, maintainable, and safe to extend as the framework grows.

The tooling described here supports local development, selective test execution, sequential and parallel Pytest execution, Pull Request validation, CI quality gates, and stable portfolio promotion.

## Tooling Overview

The project currently uses:

* Ruff for linting and static checks
* Black for Python code formatting
* isort for import sorting
* pre-commit for local quality validation
* Pytest as the main automated test runner
* pytest-xdist for worker-level parallel Pytest execution
* Playwright assertions for browser and UI validation

These tools support both local development and CI validation.

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

### Smoke And Regression

Smoke tests provide fast representative validation of critical behavior.

Regression tests provide broader or deeper validation across expanded applicable cases.

Smoke and Regression are not automatically assigned together.

Representative coverage should normally use Smoke, while expanded or all-cases coverage should normally use Regression.

Both Smoke and Regression are executed as dedicated GitHub Actions CI jobs.

Both dedicated jobs use pytest-xdist worker-level parallel execution.

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

## Local Quality Workflow

Before pushing changes or opening a Pull Request, the standard full sequential local validation is:

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

Sequential execution remains the supported baseline for normal local validation.

### Parallel Validation

When parallel execution, worker safety, fixture isolation, or execution behavior is part of the validation scope, use:

```bash
pytest -m smoke -n auto -v
pytest -m regression -n auto -v
pytest -n auto -v
```

The current suite passed these validations during Phase 4C stabilization.

Parallel validation is not required for every unrelated implementation task unless the active scope affects parallel-safety assumptions.

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

## CI Quality Checks

GitHub Actions validates the project automatically for the configured workflow triggers.

The current pipeline combines the Phase 4B job structure with the Phase 4C parallel execution strategy.

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

### Quality Job

The quality job executes:

```bash
ruff check .
black --check .
isort . --check-only
```

It also performs repository checkout, Python 3.12 setup, and dependency installation.

The quality job does not install Playwright Chromium.

The quality job does not execute browser tests and does not use pytest-xdist.

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

### Full-Suite CI Job

The full-suite job executes the complete unfiltered test suite through pytest-xdist.

Core command:

```bash
pytest -n auto -v
```

The workflow generates:

```text
reports/report.html
```

The complete full-suite job remains the primary full regression gate.

Dedicated Smoke and Regression jobs provide additional suite-specific feedback but do not replace full-suite validation.

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

## CI Reports And Artifacts

Current browser-test jobs generate self-contained pytest HTML reports.

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
test-artifacts
```

Artifact upload steps use:

```yaml
if: always()
```

This allows available reports and runtime outputs to be uploaded when an executing browser-test command fails.

If the quality job fails, browser jobs are not started and therefore do not generate browser-test artifacts for that workflow run.

Current artifact retention is seven days.

The existing report, artifact, and failure-screenshot behavior was validated under pytest-xdist execution during Phase 4C.

No sequential-only reporting exception was identified.

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
* generated execution artifacts should be available when needed for debugging

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
* planned functionality should not be presented as implemented
* generated reports, screenshots, caches, and virtual environment files should not be tracked
* the resulting `main` state should be suitable as a stable portfolio snapshot

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
* screenshot capture on failure
* local quality validation
* dedicated CI quality validation
* dedicated parallel Smoke CI execution
* dedicated parallel Regression CI execution
* parallel complete full-suite CI validation
* pytest HTML report generation
* CI artifact upload

Current CI execution model:

```text
quality
├── smoke
│   └── pytest-xdist workers
├── regression
│   └── pytest-xdist workers
└── full-suite
    └── pytest-xdist workers
```

The quality job is the prerequisite gate for browser-test execution.

Smoke and Regression have dedicated CI jobs.

UI, Security, Sorting, Navigation, and E2E remain selectively executable without dedicated CI jobs.

The full-suite job remains the complete unfiltered regression gate.

No sequential-only test exceptions were identified during Phase 4C validation.

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
* dedicated Smoke CI feedback
* dedicated Regression CI feedback
* complete full-suite CI regression protection
* reliable CI quality gates
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
* job-specific reports and artifacts
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
* preserved report and artifact behavior
* Chromium-only execution scope

GitHub Actions job-level concurrency and pytest-xdist worker-level parallelism are separate execution mechanisms.

### Phase 4D — Reporting Upgrade

Advanced Allure reporting is not currently implemented.

Allure reporting belongs to Phase 4D.

The presence of `allure-pytest` in project dependencies must not be treated as evidence that Allure reporting is active in the current validation workflow.

The current reporting solution remains:

* pytest-html
* screenshots on failure
* GitHub Actions artifacts

## Future Improvements

Possible future quality tooling improvements include:

* stricter Ruff rules where justified
* type checking with mypy
* test coverage reporting
* JUnit XML output
* refined pre-commit configuration
* stronger failure diagnostics
* Phase 4D Allure reporting integration
* additional CI execution improvements where justified

pytest-xdist parallel execution is already implemented and should not be listed as future functionality.

Future improvements should not be described as implemented until the corresponding project work is completed and validated.
