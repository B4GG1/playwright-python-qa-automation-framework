# Quality Tooling

This document describes the code quality tooling used in the QA automation framework.

The goal of quality tooling is to keep the codebase readable, consistent, maintainable, and safe to extend as the framework grows.

## Tooling Overview

The project currently uses:

* Ruff for linting and static checks
* Black for Python code formatting
* isort for import sorting
* pre-commit for local quality validation before commits
* Pytest as the main automated test runner
* Playwright assertions for stable UI validation

These tools are used locally and in the CI pipeline to validate changes before they are merged into stable branches.

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

It enforces a consistent formatting style across the project.

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

The purpose of pre-commit is to catch common formatting, import sorting, and linting issues before code is committed.

Current pre-commit hook sources:

* `astral-sh/ruff-pre-commit`
* `psf/black`
* `pycqa/isort`

## Pytest

Pytest is used as the main test runner.

Current responsibilities:

* executing automated UI tests
* supporting test fixtures
* supporting parametrized test cases
* supporting marker-based test categorization
* integrating with Playwright
* generating test results used by local workflow and CI

Run the full test suite:

```bash
pytest -v
```

Run selected marker groups:

```bash
pytest -m smoke -v
pytest -m regression -v
pytest -m positive -v
pytest -m negative -v
pytest -m sorting -v
pytest -m navigation -v
pytest -m "ui and smoke" -v
pytest -m "ui and regression" -v
pytest -m "ui and sorting" -v
pytest -m "ui and navigation" -v
```

Marker definitions are stored in:

```text
pytest.ini
```

Current marker categories include:

* `smoke`
* `regression`
* `ui`
* `api`
* `e2e`
* `positive`
* `negative`
* `sorting`
* `navigation`

The project uses strict marker validation, so markers used in tests should be registered in `pytest.ini`.

## Playwright Assertions

Playwright assertions are used for UI validation.

Examples of current assertion usage include:

* checking page title
* checking URL after login
* checking URL after navigation
* checking element visibility
* checking element hidden state
* checking form field attributes
* checking protected route redirection
* checking inventory page visibility
* checking product card content
* checking product details content
* checking product image attributes
* checking cart page visibility
* checking cart badge visibility and text
* checking cart item visibility
* checking cart item content
* checking Add to cart and Remove button states
* checking cart state after logout and re-login

Playwright assertions should be preferred for browser and UI state validation because they include built-in waiting behavior.

Plain Python assertions are used when comparing extracted values such as product names, product prices, sorted lists, expected error message strings, or other already-read data.

## Local Quality Workflow

Before pushing changes, the recommended local validation workflow is:

```bash
ruff check .
black --check .
isort . --check-only
pytest -v
```

If formatting changes are needed, run:

```bash
black .
isort .
```

Then run validation again:

```bash
ruff check .
black --check .
isort . --check-only
pytest -v
```

For login-related changes, marker-based checks may also be useful:

```bash
pytest -m smoke -v
pytest -m regression -v
pytest -m positive -v
pytest -m negative -v
pytest -m "ui and smoke" -v
pytest -v tests/test_login_positive.py
pytest -v tests/test_login_negative.py
pytest -v tests/test_login_ui.py
pytest -v tests/test_login_access_control.py
```

For inventory and product-related changes, these commands may also be useful:

```bash
pytest -v tests/test_inventory_page.py
pytest -m sorting -v
pytest -m "ui and sorting" -v
```

For cart-related changes, these commands may also be useful:

```bash
pytest -v tests/test_cart_page.py
pytest -m navigation -v
pytest -m "ui and navigation" -v
pytest -m "ui and regression" -v
```

For checkpoint or stabilization tasks, run both scoped and full validation when possible:

```bash
pytest -v tests/test_cart_page.py
pytest -v
```

## CI Quality Checks

The GitHub Actions pipeline validates code quality automatically.

Current CI checks include:

* Ruff linting
* Black formatting validation
* isort import validation
* Pytest test execution
* pytest HTML report generation
* artifact upload for reports and screenshots

Current CI quality commands include:

```bash
ruff check .
black --check .
isort . --check-only
pytest -v --html=reports/report.html --self-contained-html
```

These checks help ensure that only validated changes are integrated into stable branches.

The CI pipeline should fail when:

* linting fails
* formatting validation fails
* import sorting validation fails
* automated tests fail

Generated reports and screenshots should be uploaded as artifacts instead of being committed to Git.

## Quality Gates

The project uses quality gates at multiple levels.

### Local quality gate

Before commit or push:

```bash
ruff check .
black --check .
isort . --check-only
pytest -v
```

### Pre-commit quality gate

Before creating commits, or manually before final validation:

```bash
pre-commit run --all-files
```

### Scoped workstream quality gate

For workstream-specific review or stabilization tasks:

```bash
pytest -v tests/test_cart_page.py
```

The scoped command should be followed by full-suite validation before the workstream is considered ready for merge unless a scoped validation exception is explicitly accepted.

### CI quality gate

Before merging Pull Requests:

* GitHub Actions workflow must pass
* tests must pass
* quality checks must pass
* generated artifacts should be available for review when needed

## Current Quality Status

The current quality tooling supports the completed Login Page Automation Workstream, Inventory And Products Automation Workstream, and Cart Automation Workstream.

The project currently includes:

* Page Object Model implementation for login page
* Page Object Model implementation for inventory page
* Page Object Model implementation for product details page
* Page Object Model implementation for cart page
* reusable pytest fixture for opened login page
* reusable pytest fixture for logged-in inventory page
* centralized login test data
* centralized inventory product test data
* parametrized login tests
* parametrized protected route access tests
* parametrized inventory product tests
* parametrized cart tests
* marker-based test categorization
* screenshot capture on test failure
* local and CI validation workflow
* HTML report generation
* CI artifact upload
* full-suite CI validation

## Quality Goals

The project quality tooling supports:

* consistent code formatting
* readable and maintainable codebase
* automated local validation
* reduced formatting conflicts
* consistent import ordering
* reliable CI validation
* stable automated test execution
* scalable development workflow
* professional Pull Request workflow
* traceability between test cases and automated coverage
* safe checkpoint validation before workstream merge preparation

## Future Improvements

Planned quality tooling improvements may include:

* stricter Ruff rule selection
* type checking with mypy
* test coverage reporting
* JUnit XML output for CI test results
* refined pre-commit hook configuration
* improved custom assertion helpers
* stronger test diagnostics
* separate CI jobs for smoke and regression suites
* separate marker-based CI jobs for selected test categories
* Allure reporting integration
