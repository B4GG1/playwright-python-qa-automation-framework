# Quality Tooling

This document describes the code quality tooling used in the QA automation framework.
The goal of quality tooling is to keep the codebase readable, consistent, maintainable, and safe to extend as the framework grows.

## Tooling Overview

The project currently uses:

- Ruff for linting and static checks
- Black for Python code formatting
- isort for import sorting
- pre-commit for local quality validation before commits

These tools are used both locally and in the CI pipeline.

## Ruff

Ruff is used for fast Python linting and static code analysis.

Current responsibilities:

- detecting common Python issues
- enforcing selected linting rules
- validating import-related rules

Run Ruff locally:

```bash
ruff check .
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

## pre-commit

pre-commit runs configured quality checks before a commit is created.

Current pre-commit hooks include:

- Ruff
- Ruff format
- Black
- isort

Install hooks locally:

```bash
pre-commit install
```

Run all hooks manually:

```bash
pre-commit run --all-files
```

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

## CI Quality Checks

The GitHub Actions pipeline validates code quality automatically.

Current CI checks include:

- Ruff linting
- Black formatting validation
- isort import validation
- Pytest test execution

These checks help ensure that only validated changes are integrated into stable branches.

## Quality Goals

The project quality tooling supports:

- consistent code formatting
- readable and maintainable codebase
- automated local validation
- reduced formatting conflicts
- consistent import ordering
- reliable CI validation
- scalable development workflow

## Future Improvements

Planned quality tooling improvements may include:

- stricter Ruff rule selection
- type checking with mypy
- test coverage reporting
- JUnit XML output for CI test results
- refined pre-commit hook configuration