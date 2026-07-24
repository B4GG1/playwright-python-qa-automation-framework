# Quality Tooling

This document describes the code quality tooling used in the QA automation framework.

The goal of quality tooling is to keep the codebase readable, consistent, maintainable, and safe to extend as the framework grows.

The quality tooling described below supports the stable Phase 3 portfolio snapshot. The `main` branch should contain the polished portfolio version of this snapshot, while `develop` remains the integration branch and may contain newer work after this document is read from `main`.

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

```
ruff check .
```

Ruff configuration is stored in:

```
pyproject.toml
```

Current Ruff configuration:

```
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

```
black --check .
```

Format files locally:

```
black .
```

Black configuration is stored in:

```
pyproject.toml
```

Current Black configuration:

```
[tool.black]
line-length = 100
target-version = ['py312']
```

## isort

isort is used to organize Python imports.

The project uses Black-compatible isort configuration.

Check import sorting without modifying files:

```
isort . --check-only
```

Sort imports locally:

```
isort .
```

isort configuration is stored in:

```
pyproject.toml
```

Current isort configuration:

```
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

```
pre-commit install
```

Run all hooks manually:

```
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

```
pytest -v
```

Run selected marker groups:

```
pytest -m smoke -v
pytest -m regression -v
pytest -m positive -v
pytest -m negative -v
pytest -m sorting -v
pytest -m navigation -v
pytest -m e2e -v
pytest -m "ui and smoke" -v
pytest -m "ui and regression" -v
pytest -m "ui and sorting" -v
pytest -m "ui and navigation" -v
```

Marker definitions are stored in:

```
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

The current implemented automated test suite focuses on UI coverage. The `api` marker is registered for future API testing scope and does not mean that API tests are implemented yet.

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
* checking checkout information form visibility
* checking checkout required field error messages
* checking checkout input error icon visibility
* checking checkout overview visibility
* checking checkout overview product item content
* checking checkout overview price summary content
* checking checkout complete page visibility
* checking checkout completion header and message
* checking Back Home navigation after order completion

Playwright assertions should be preferred for browser and UI state validation because they include built-in waiting behavior.

Plain Python assertions are used when comparing extracted values such as product names, product prices, sorted lists, expected error message strings, checkout summary values, or other already-read data.

## Local Quality Workflow

Before pushing changes, the recommended local validation workflow is:

```
ruff check .
black --check .
isort . --check-only
pytest -v
```

If formatting changes are needed, run:

```
black .
isort .
```

Then run validation again:

```
ruff check .
black --check .
isort . --check-only
pytest -v
```

For login-related changes, these commands may also be useful:

```
pytest -v tests/test_login_page.py
pytest -m smoke -v
pytest -m regression -v
pytest -m positive -v
pytest -m negative -v
pytest -m "ui and smoke" -v
```

For inventory-related changes, these commands may also be useful:

```
pytest -v tests/test_inventory_page.py
pytest -m sorting -v
pytest -m "ui and sorting" -v
```

For product-details-related changes, these commands may also be useful:

```
pytest -v tests/test_product_details_page.py
pytest -m navigation -v
pytest -m "ui and navigation" -v
pytest -m "ui and regression" -v
```

For cart-related changes, these commands may also be useful:

```
pytest -v tests/test_cart_page.py
pytest -m navigation -v
pytest -m "ui and navigation" -v
pytest -m "ui and regression" -v
```

For checkout-related changes, these commands may also be useful:

```
pytest -v tests/test_checkout_page.py
pytest -m e2e -v
pytest -m navigation -v
pytest -m "ui and regression" -v
pytest -m "ui and navigation" -v
```

For checkpoint, stabilization, or portfolio promotion tasks, run relevant scoped modules and full validation when possible:

```
pytest -v tests/test_login_page.py
pytest -v tests/test_inventory_page.py
pytest -v tests/test_product_details_page.py
pytest -v tests/test_cart_page.py
pytest -v tests/test_checkout_page.py
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

```
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

### Local Quality Gate

Before commit or push:

```
ruff check .
black --check .
isort . --check-only
pytest -v
```

### Pre-commit Quality Gate

Before creating commits, or manually before final validation:

```
pre-commit run --all-files
```

### Scoped Workstream Quality Gate

For workstream-specific review or stabilization tasks:

```
pytest -v tests/test_login_page.py
pytest -v tests/test_inventory_page.py
pytest -v tests/test_product_details_page.py
pytest -v tests/test_cart_page.py
pytest -v tests/test_checkout_page.py
```

The scoped command should be followed by full-suite validation before the workstream is considered ready for merge unless a scoped validation exception is explicitly accepted.

### CI Quality Gate

Before merging Pull Requests:

* GitHub Actions workflow must pass
* tests must pass
* quality checks must pass
* generated artifacts should be available for review when needed

### Portfolio Promotion Quality Gate

Before promoting `develop` to `main`:

* full local validation should pass when possible
* CI on the promotion Pull Request should pass
* documentation should not describe unfinished future work as implemented
* generated reports, screenshots, cache files, and virtual environment files should not be tracked
* the promoted state should be suitable as a stable portfolio snapshot

## Current Quality Status

The current quality tooling supports completed page-level automation coverage for Login, Inventory, Product Details, Cart, and Checkout areas.

The project currently includes:

* Page Object Model implementation for login page
* Page Object Model implementation for inventory page
* Page Object Model implementation for product details page
* Page Object Model implementation for cart page
* Page Object Model implementation for checkout pages
* shared authenticated-page behavior through `AppPage`
* reusable product assertion helpers
* reusable checkout overview assertion helpers
* reusable pytest fixture for opened login page
* reusable pytest fixture for standard user credentials
* reusable pytest fixture for logged-in inventory page
* reusable pytest fixture for inventory page with one product in cart
* reusable pytest fixture for cart page with one product
* reusable pytest fixture for checkout step one page with one product
* reusable pytest fixture for checkout step two page with one product
* reusable pytest fixture for checkout complete page with one product
* centralized login test data
* centralized product test data
* centralized checkout test data
* parametrized login tests
* parametrized protected route access tests
* parametrized inventory product tests
* parametrized product details tests
* parametrized cart tests
* parametrized checkout tests where practical
* marker-based test categorization
* screenshot capture on test failure
* local and CI validation workflow
* HTML report generation
* CI artifact upload
* full-suite CI validation

Phase 3 page-level automation coverage has been completed, reviewed, validated, squash-merged into `develop`, and promoted to `main` as the stable Phase 3 portfolio snapshot.

The `main` branch represents the polished portfolio version of the project. The `develop` branch remains the integration branch and may contain newer work after this document is read from `main`.

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
* safe checkpoint validation before workstream merge or portfolio promotion

## Future Improvements

Planned quality tooling improvements may include:

* stricter Ruff rule selection
* type checking with mypy
* test coverage reporting
* JUnit XML output for CI test results
* refined pre-commit hook configuration
* stronger test diagnostics
* separate CI jobs for smoke and regression suites
* separate marker-based CI jobs for selected test categories
* Allure reporting integration
