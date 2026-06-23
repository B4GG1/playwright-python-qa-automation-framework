# Development Workflow

This document describes the day-to-day development workflow used in this project.

For detailed branching rules, see: [Git Branching Strategy](git-branching-strategy.md).

## Workflow Overview

The project follows a professional Git-based development workflow:

```text
develop
  ↓
feature / fix / docs branch
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

The goal is to keep development organized, validated, and easy to review.

## Standard Task Workflow

For small independent tasks, the recommended workflow is:

1. Start from the latest `develop` branch.
2. Create a dedicated feature, fix, refactor, or documentation branch.
3. Implement changes locally.
4. Run local checks.
5. Commit changes with a meaningful message.
6. Push the branch to GitHub.
7. Open a Pull Request into `develop`.
8. Wait for CI validation.
9. Review changed files manually.
10. Merge using Squash and merge after validation.
11. Update local `develop`.

## Workstream Workflow

For larger tightly connected areas, the project may use one workstream branch.

Examples:

```text
feature/login-page
feature/inventory-products
feature/cart-page
```

In this workflow:

1. Create one branch for the whole workstream.
2. Implement multiple related tasks on the same branch.
3. Create separate commits for individual tasks.
4. Push regularly as backup.
5. Run local validation after meaningful changes.
6. Review scope, tests, documentation, and cleanup during a checkpoint task when the workstream is complete.
7. Open one Pull Request only when the whole workstream is ready.
8. Validate CI.
9. Squash merge the complete workstream into `develop`.

This approach was used for complete functional automation workstreams such as Login Page Automation and Cart Automation.

It is useful when tasks are connected and reviewing them together makes more sense than creating many small Pull Requests.

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
git checkout -b feature/checkout-flow
git checkout -b fix/screenshot-hook
git checkout -b docs/update-testing-strategy
git checkout -b refactor/login-fixtures
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

## Local Validation

Before pushing or opening a Pull Request, run:

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

For marker-based validation, use:

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

For workstream-specific validation, run the relevant test module before the full suite when useful.

Examples:

```bash
pytest -v tests/test_inventory_page.py
pytest -v tests/test_cart_page.py
```

The full test suite should still pass before a workstream is considered ready for merge unless a scoped validation exception is explicitly accepted.

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
git commit -m "refactor(AQA-0032): parametrize negative login scenarios"
git commit -m "test(AQA-0038): add protected inventory route access test"
git commit -m "test(AQA-0057): add product to cart test"
git commit -m "chore(AQA-0064): review and stabilize cart workstream"
```

Common commit types:

* `feat` — new framework functionality
* `test` — automated tests or test-related changes
* `docs` — documentation changes
* `refactor` — structural improvements without behavior change
* `fix` — bug fixes
* `chore` — maintenance, configuration, or review changes

## Pull Request Flow

Pull Requests should usually follow this direction:

```text
feature/* -> develop
fix/* -> develop
docs/* -> develop
refactor/* -> develop
```

Promotion flow:

```text
develop -> main
```

The `main` branch should only receive stable and validated changes.

## Pull Request Checklist

Before opening a Pull Request, verify:

* local working tree is clean
* relevant commits are pushed
* local quality checks passed
* relevant scoped test module passed when applicable
* full test suite passed
* documentation is updated if needed
* no generated reports or screenshots are tracked
* no cache files or virtual environment files are tracked
* branch target is correct

Recommended pre-PR commands:

```bash
git status
ruff check .
black --check .
isort . --check-only
pytest -v
```

For a workstream checkpoint, also run the relevant scoped test module.

Example:

```bash
pytest -v tests/test_cart_page.py
pytest -v
```

## CI Integration

GitHub Actions validates changes on:

* push to `main`
* push to `develop`
* pull requests targeting `main`
* pull requests targeting `develop`
* manual workflow dispatch

The CI pipeline validates:

* dependency installation
* Playwright browser installation
* Ruff linting
* Black formatting validation
* isort import sorting validation
* Pytest test execution
* HTML report generation
* artifact upload

A Pull Request should not be merged if CI fails.

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
```

## Post-Merge Workflow

After a Pull Request is merged into `develop`, update local `develop`:

```bash
git checkout develop
git pull origin develop
```

Check recent commits:

```bash
git log --oneline --decorate -5
```

Optionally delete the completed local feature branch:

```bash
git branch -d feature/<short-description>
```

Clean deleted remote branch references:

```bash
git fetch --prune
```

Run final validation if needed:

```bash
pytest -v
```

## Phase And Workstream Checkpoint Workflow

Before moving to the next major project phase or before merging a completed workstream, a checkpoint task must be completed.

A checkpoint verifies:

* completed scope
* test coverage
* local validation
* relevant scoped test execution
* full test suite execution or accepted scoped validation
* CI status
* documentation status
* Git status
* cleanup needs
* generated files and ignored artifacts
* readiness for the next phase or merge

Example checkpoints:

```text
AQA-0041 — Review Phase 2 And Prepare Phase 3 Scope
AQA-0064 — Review And Stabilize Cart Workstream
```

No new functional work should start before the relevant checkpoint is completed.

## Documentation Updates

Documentation should be updated when changes affect:

* framework architecture
* project structure
* testing strategy
* CI/CD workflow
* quality tooling
* roadmap
* feature list
* technology stack
* test case coverage
* README instructions

Documentation changes may be committed as part of the relevant task or as a separate documentation cleanup or stabilization task.

For automation work that implements a documented manual test case, update the related test case metadata in the same task when required.

## Summary

This workflow ensures that every change is developed, validated, reviewed, and integrated in a controlled way.

It supports:

* clean Git history
* professional Pull Request workflow
* reliable CI validation
* readable project evolution
* safe workstream integration
* phase-based project management
* portfolio-ready repository standards
