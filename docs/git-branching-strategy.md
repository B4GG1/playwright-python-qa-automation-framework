# Git Branching And Merge Strategy

This document defines the branching strategy, merge workflow, and repository standards used in this project.

The goal is to keep the repository history clean, support isolated development, and ensure that changes are validated before being merged into stable branches.

## Branching Model

This repository follows a lightweight Git workflow inspired by a simplified Git Flow model.

The main goals are:

* clean and traceable history
* isolated feature or workstream development
* safe integration into stable branches
* CI validation before merging changes
* readable Pull Requests
* professional portfolio-friendly Git history

## Branch Structure

### `main`

The `main` branch represents the stable portfolio/release state of the repository.

Rules:

* should always remain stable
* should contain validated and reviewed changes only
* should be updated through Pull Requests
* should not receive direct pushes
* should be used as the most polished public version of the project

### `develop`

The `develop` branch is the main integration branch for ongoing development.

Rules:

* used as the base branch for feature work
* receives completed work through Pull Requests
* should remain reasonably stable
* acts as the staging area before changes are promoted to `main`
* should contain completed and validated workstreams

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
feature/checkout-flow
feature/api-client
```

A feature branch may represent:

* one small task,
* one larger feature,
* one complete workstream,
* one structure cleanup or stabilization workstream.

For small independent tasks, one branch per task is preferred.

For tightly connected workstreams, one larger branch is acceptable if commits remain organized and traceable by task ID.

Examples from the project:

```text
feature/login-page
feature/inventory-products
feature/cart-page
feature/structure-cleanup
```

These branches can be used for complete functional automation, structure cleanup, documentation synchronization, or stabilization workstreams when the tasks are tightly related and easier to validate together.

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
```

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
refactor(AQA-0032): parametrize negative login scenarios
test(AQA-0038): add protected inventory route access test
test(AQA-0057): add product to cart test
chore(AQA-0064): review and stabilize cart workstream
chore(AQA-0073): finalize phase 3c structure cleanup
```

Common commit types:

* `feat` — new framework functionality
* `test` — automated tests or test-related changes
* `docs` — documentation changes
* `refactor` — structural changes without behavior change
* `fix` — bug fixes
* `chore` — maintenance/configuration/review tasks

## Workstream Branch Strategy

For larger functional areas or tightly connected cleanup phases, the project may use one workstream branch.

Examples:

```text
feature/login-page
feature/inventory-products
feature/cart-page
feature/structure-cleanup
```

In this approach:

* all related tasks are committed on the same branch,
* each task still gets its own meaningful commit,
* commits should include the task ID when applicable,
* the branch is pushed regularly as backup,
* local validation is performed during and after the workstream,
* Pull Request is created only when the whole workstream is ready,
* final merge into `develop` is performed using Squash and merge.

This approach is acceptable when tasks are tightly connected and reviewing them together makes sense.

The `feature/structure-cleanup` branch is an example of a workstream branch used for structural cleanup, coverage synchronization, final validation, and documentation sync after page-level Login, Inventory, Product Details, and Cart automation coverage.

## Merge Strategy

The recommended merge strategy is:

> Squash and merge

Squash merge combines all commits from a feature branch into a single commit on the target branch.

Benefits:

* keeps commit history clean
* one workstream becomes one logical commit on `develop`
* simplifies rollback
* improves readability for reviewers and recruiters
* reduces noisy commit history
* keeps local development commits flexible

Example final squash commit:

```text
test(AQA-0064): complete cart automation workstream
```

For documentation-only, cleanup, or checkpoint-only changes, the squash commit may use `docs` or `chore` instead:

```text
chore(AQA-0064): review and stabilize cart workstream
docs(AQA-0064): update project documentation after cart workstream
chore(AQA-0073): finalize phase 3c structure cleanup
```

## Direct Push Policy

Direct pushes should be avoided for:

* `main`
* `develop`

Recommended workflow:

```text
feature branch -> Pull Request -> CI validation -> Review -> Squash merge
```

For this project, even when working solo, Pull Requests are used to practice professional workflow and validate changes through CI.

Direct pushes to a feature branch are acceptable during active implementation, review, documentation sync, and checkpoint work.

## Branch Protection Rules

Recommended GitHub branch protection settings are listed below.

### `main`

Recommended rules:

* require Pull Request before merging
* require CI status checks to pass
* disallow force pushes
* disallow direct commits
* require linear history if appropriate

### `develop`

Recommended rules:

* require Pull Request before merging
* require CI status checks to pass
* disallow force pushes where practical
* use as the primary integration branch for completed workstreams

For a solo portfolio project, these rules can be introduced gradually as the workflow matures.

## Pull Request Workflow

Standard Pull Request workflow:

1. Start from the latest `develop` branch.
2. Create a dedicated feature, fix, refactor, or documentation branch.
3. Implement changes locally.
4. Commit logical pieces of work.
5. Push the branch to GitHub regularly.
6. Run local validation.
7. Open a Pull Request into `develop`.
8. Wait for CI pipeline validation.
9. Review changed files manually.
10. Squash merge after validation.
11. Update local `develop`.
12. Delete the completed feature branch if no longer needed.

Pull Request direction for regular development:

```text
feature branch -> develop
```

Promotion to `main` should happen only after `develop` contains stable and validated changes that are ready to be presented as a polished portfolio version.

## Local Validation Before Pull Request

Recommended local checks before opening a Pull Request:

```bash
ruff check .
black --check .
isort . --check-only
pytest -v
```

Additional marker-based checks may be used when relevant:

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

For workstream-specific stabilization tasks, scoped validation may also be used before the full suite.

Examples:

```bash
pytest -v tests/test_login_page.py
pytest -v tests/test_inventory_page.py
pytest -v tests/test_product_details_page.py
pytest -v tests/test_cart_page.py
pytest -v
```

For a single-page task, running the relevant module before the full suite is usually enough.

Example:

```bash
pytest -v tests/test_cart_page.py
pytest -v
```

The full test suite should still pass before a workstream is considered ready for merge unless a scoped validation exception is explicitly accepted.

## Pull Request Review Checklist

Before merging a Pull Request, verify:

* CI pipeline passed
* no unrelated files are included
* no generated reports, screenshots, cache files, or virtual environment files are tracked
* changed files match the intended task or workstream scope
* documentation is updated when needed
* test cases and automated tests are aligned
* Page Object responsibilities remain logically separated
* shared authenticated-page behavior remains owned by the correct abstraction
* reusable assertion helpers remain focused on shared validation logic
* test data remains centralized where practical
* checkout behavior is not mixed into inventory, product details, or cart scope
* commit message for squash merge is clear
* target branch is correct

For regular feature work, the target branch should usually be:

```text
develop
```

## Post-Merge Local Cleanup

After a Pull Request is squash merged into `develop`, update the local repository:

```bash
git checkout develop
git pull origin develop
```

Then optionally delete the completed local feature branch:

```bash
git branch -d feature/<short-description>
```

If the remote branch was deleted on GitHub, clean stale remote references:

```bash
git fetch --prune
```

## Phase And Workstream Checkpoint Strategy

Before moving to the next major project phase or before merging a completed workstream, a checkpoint task should be completed.

A checkpoint task should verify:

* completed scope
* test coverage
* local test execution
* full suite execution or accepted scoped validation
* CI status
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
```

## Summary

This strategy ensures:

* predictable development process
* clean Git history
* controlled integration workflow
* CI/CD integration safety
* professional repository standards
* scalable workflow for future collaboration
* clear separation between active work, integration, and stable portfolio state
