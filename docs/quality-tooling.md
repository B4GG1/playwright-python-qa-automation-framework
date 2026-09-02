# Quality Tooling

This document describes the code quality and validation tooling used in the QA automation framework.

The goal of quality tooling is to keep the codebase readable, consistent, maintainable, and safe to extend as the framework grows.

The tooling described here supports local development, selective test execution, Pull Request validation, CI quality gates, and stable portfolio promotion.

## Tooling Overview

The project currently uses:

* Ruff for linting and static checks
* Black for Python code formatting
* isort for import sorting
* pre-commit for local quality validation
* Pytest as the main automated test runner
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
* integrating with Playwright
* producing results used by local validation and CI

Run the complete test suite:

```bash
pytest -v
```

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

Run Smoke:

```bash
pytest -m smoke -v
```

Run Regression:

```bash
pytest -m regression -v
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

### Smoke And Regression

Smoke tests provide fast representative validation of critical behavior.

Regression tests provide broader or deeper validation across expanded applicable cases.

Smoke and Regression are not automatically assigned together.

Representative coverage should normally use Smoke, while expanded or all-cases coverage should normally use Regression.

### UI

The `ui` marker is used when visibility, presentation, state, or direct UI behavior is materially validated.

A Playwright test does not automatically require the `ui` marker.

### Security

The `security` marker covers authentication access control and protected-route validation.

Current Security coverage includes unauthenticated access attempts to protected areas such as:

* Inventory
* Cart
* Product Details
* Checkout Information
* Checkout Overview
* Checkout Complete

### Sorting

The `sorting` marker identifies product sorting behavior.

Current sorting coverage includes:

* product name A to Z
* product name Z to A
* product price low to high
* product price high to low

### Navigation

The `navigation` marker identifies meaningful page transitions.

The authentication Login → Inventory transition is intentionally excluded from the Navigation suite.

Navigation may be combined with Smoke or Regression depending on whether the scenario is representative or expanded.

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

Before pushing changes or opening a Pull Request, the standard full local validation is:

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

## CI Quality Checks

GitHub Actions validates the project automatically for the configured workflow triggers.

Current CI checks include:

* Ruff linting
* Black formatting validation
* isort import validation
* full Pytest execution
* pytest HTML report generation
* artifact upload for reports and screenshots

Current CI quality and test commands include:

```bash
ruff check .
black --check .
isort . --check-only
pytest -v --html=reports/report.html --self-contained-html
```

The current CI pipeline runs the complete automated test suite.

It does not currently split execution into separate marker-based jobs.

Marker-based execution is primarily used for selective local validation.

Separate Smoke, Regression, E2E, Security, Navigation, or other marker-based CI jobs should only be described as implemented after the corresponding workflow changes are introduced and validated.

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
* tests must pass
* configured quality checks must pass
* generated execution artifacts should be available when needed for debugging

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
* Smoke suite execution
* Regression suite execution
* UI suite execution
* Security suite execution
* Sorting suite execution
* Navigation suite execution
* independent E2E checkpoint suite execution
* screenshot capture on failure
* local quality validation
* full-suite CI validation
* HTML report generation
* CI artifact upload

The current CI strategy remains full-suite execution.

Marker-based suite separation in CI is not implemented yet.

## Quality Goals

The project quality tooling supports:

* consistent formatting
* readable and maintainable code
* automated local validation
* reduced formatting conflicts
* consistent import organization
* reliable Pytest execution
* selective marker-based local validation
* reliable CI validation
* stable workstream integration
* professional Pull Request workflow
* traceability between test cases and automated coverage
* safe checkpoint validation
* stable portfolio promotion

## Future Improvements

Possible future quality tooling improvements include:

* stricter Ruff rules where justified
* type checking with mypy
* test coverage reporting
* JUnit XML output
* refined pre-commit configuration
* stronger failure diagnostics
* separate marker-based CI jobs
* parallel test execution
* Allure reporting integration

Future improvements should not be described as implemented until the corresponding project work is completed and validated.
