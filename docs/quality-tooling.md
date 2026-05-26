# Quality Tooling

The framework includes automated quality tooling to maintain consistent code standards, improve readability, and support scalable development workflows.

## Static Analysis

### Ruff

Used for fast Python linting and static code analysis.

```bash
ruff check .
```

---

## Code Formatting

### Black

Used to enforce consistent Python code formatting.

```bash
black .
```

### isort

Used to standardize and organize Python imports.

```bash
isort .
```

---

## Automated Quality Gates

### pre-commit

Pre-commit hooks automatically validate code quality before commits are created.

Configured hooks currently include:

* Ruff
* Black
* isort

Run all hooks manually:

```bash
pre-commit run --all-files
```

Install hooks locally:

```bash
pre-commit install
```

---

## Code Quality & Development Tooling

The framework uses automated quality tooling to enforce consistent code standards, improve maintainability, and support scalable development workflows.

* Ruff (linting)
* Black (code formatting)
* isort (import standardization)
* pre-commit hooks (automated local validation)
* 
## Quality Goals

* Consistent code formatting
* Readable and maintainable codebase
* Automated local validation
* Reduced formatting conflicts
* Standardized development workflow
