# Git Branching And Merge Strategy

This document defines the branching strategy, merge workflow, and repository standards used in this project.

The goal is to keep the repository history clean, support isolated development, and ensure that changes are validated before being merged into stable branches.

The branching strategy supports two stable branch roles:

* `main` represents the polished portfolio/release version of the project.
* `develop` represents the integration branch for completed and validated work before it is promoted to `main`.

When this document is read from `main`, the `develop` branch may already contain newer integration work that has not yet been promoted to the stable portfolio branch.

For detailed pytest marker semantics and suite execution strategy, see [Testing Strategy](testing-strategy.md).

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
```

In this approach:

* all related tasks are committed on the same branch
* each task still gets its own meaningful commit
* commits should include the task ID when applicable
* the branch is pushed regularly as backup
* local validation is performed during and after the workstream
* a Pull Request is created only when the whole workstream is ready
* final merge into `develop` is performed using Squash and merge

This approach is acceptable when tasks are tightly connected and reviewing them together makes sense.

The `feature/structure-cleanup` branch is an example of a workstream branch used for structural cleanup, coverage synchronization, final validation, and documentation sync after page-level Login, Inventory, Product Details, and Cart automation coverage.

The `feature/checkout` branch is an example of a functional workstream branch used for checkout automation, related coverage completion, final validation, and documentation synchronization before integration into `develop`.

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
8. Open a Pull Request into `develop`.
9. Wait for CI pipeline validation.
10. Review changed files manually.
11. Squash merge after validation.
12. Update local `develop`.
13. Delete the completed source branch if no longer needed.

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

Recommended full local checks before opening a Pull Request:

```bash
ruff check .
black --check .
isort . --check-only
pytest -v
```

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

Marker-based execution is primarily used for selective local validation.

Detailed marker semantics and assignment rules are documented in [Testing Strategy](testing-strategy.md).

The current GitHub Actions pipeline executes the complete automated test suite rather than separate marker-based jobs.

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

For a single-page task, running the relevant module before the full suite is usually appropriate.

Example:

```bash
pytest -v tests/test_checkout_page.py
pytest -v
```

The full test suite should still pass before a workstream is considered ready for merge unless a scoped validation exception is explicitly accepted.

For portfolio promotion into `main`, the full test suite and quality checks should pass before merge unless a specific scoped validation exception is explicitly accepted.

## Pull Request Review Checklist

Before merging a Pull Request, verify:

* CI pipeline passed
* no unrelated files are included
* no generated reports, screenshots, cache files, or virtual environment files are tracked
* changed files match the intended task, workstream, cleanup, or promotion scope
* documentation is updated when needed
* test cases and automated tests are aligned
* marker documentation reflects current executable marker behavior when marker usage changes
* Page Object responsibilities remain logically separated
* shared authenticated-page behavior remains owned by the correct abstraction
* reusable assertion helpers remain focused on shared validation logic
* test data remains centralized where practical
* cart-owned checkout entry behavior remains separated from detailed checkout behavior
* Checkout Information, Checkout Overview, and Checkout Complete behavior remain owned by checkout tests
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
* documentation clearly separates implemented scope from planned future scope
* test case documentation is aligned with automated coverage
* generated reports, screenshots, cache files, and virtual environment files are not tracked
* the promoted state is suitable for recruiters or technical reviewers
* future work remains directed through `develop`

## Post-Merge Local Cleanup

### After Merge Into `develop`

After a Pull Request is squash merged into `develop`, update the local repository:

```bash
git checkout develop
git pull origin develop
```

Then optionally delete the completed local source branch:

```bash
git branch -d feature/<short-description>
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
AQA-0082 — Checkout Workstream Final Validation And Documentation Sync
```

A separate portfolio promotion review may also be used when a completed phase is promoted from `develop` to `main`.

## Summary

This strategy ensures:

* predictable development process
* clean Git history
* controlled integration workflow
* controlled portfolio promotion workflow
* reliable CI integration
* consistent local validation
* normalized marker-based selective execution
* professional repository standards
* scalable workflow for future collaboration
* clear separation between active work, integration, and stable portfolio state
