# Development Workflow

This document describes the day-to-day development workflow used in this project.

For detailed branching rules, see: [Git Branching Strategy](git-branching-strategy.md).

For detailed test categorization and pytest marker semantics, see: [Testing Strategy](testing-strategy.md).

The workflow described below supports two branch roles:

* `develop` is the main integration branch for completed and validated work.
* `main` is the stable portfolio branch used for polished portfolio snapshots.

When this document is read from `main`, the `develop` branch may already contain newer integration work that has not yet been promoted to the stable portfolio version.

## Workflow Overview

The project follows a professional Git-based development workflow.

Regular development workflow:

```text
develop
  ↓
feature / fix / docs / refactor branch
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

Portfolio promotion workflow:

```text
develop
  ↓
final documentation and validation review
  ↓
Pull Request to main
  ↓
CI validation
  ↓
Squash merge
  ↓
stable portfolio snapshot on main
```

The goal is to keep development organized, validated, easy to review, and suitable for a public QA automation portfolio.

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

The standard task workflow should not target `main` directly. Regular implementation work should flow through `develop` first.

## Workstream Workflow

For larger tightly connected areas, the project may use one workstream branch.

Examples:

```text
feature/login-page
feature/inventory-products
feature/cart-page
feature/structure-cleanup
feature/checkout
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

This approach is used for complete functional automation, refactor, documentation sync, and stabilization workstreams such as Login Page Automation, Cart Automation, Phase 3C Structure Cleanup, and Checkout Automation.

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
git checkout -b feature/checkout
git checkout -b feature/structure-cleanup
git checkout -b fix/screenshot-hook
git checkout -b docs/update-testing-strategy
git checkout -b docs/portfolio-docs-cleanup
git checkout -b refactor/login-fixtures
```

For documentation cleanup before portfolio promotion, a documentation branch may be used:

```bash
git checkout -b docs/phase-3-portfolio-cleanup
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

For documentation-only or portfolio-promotion cleanup that is not tied to a single task ID, a commit message may omit the task ID if no approved task ID exists.

Examples:

```bash
git commit -m "docs: clean documentation before main promotion"
git commit -m "chore: promote phase 3 portfolio state to main"
```

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

### Marker-Based Validation

Pytest markers support selective local validation.

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

Markers describe different dimensions of test intent and may be combined where useful.

Common examples:

```bash
pytest -m "smoke and ui" -v
pytest -m "regression and ui" -v
pytest -m "smoke and navigation" -v
pytest -m "regression and navigation" -v
```

Marker expressions can also be scoped to a specific test module.

Example:

```bash
pytest tests/test_checkout_page.py -m e2e -v
```

The `e2e` suite represents independent checkpoint tests that collectively form the primary purchase journey. Tests do not depend on shared state or execution order.

Detailed marker meanings and assignment rules are documented in [Testing Strategy](testing-strategy.md).

### Workstream-Specific Validation

Run the relevant test module before the full suite when useful.

Examples:

```bash
pytest -v tests/test_login_page.py
pytest -v tests/test_inventory_page.py
pytest -v tests/test_product_details_page.py
pytest -v tests/test_cart_page.py
pytest -v tests/test_checkout_page.py
```

Additional marker-based validation should be selected according to the changed behavior.

Examples:

```bash
pytest -m security -v
pytest -m sorting -v
pytest -m navigation -v
pytest -m e2e -v
```

The full test suite should still pass before a workstream is considered ready for merge unless a scoped validation exception is explicitly accepted.

For documentation-only changes, full local validation is still recommended before portfolio promotion because `main` should represent a stable public snapshot.

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
git commit -m "refactor(AQA-0032): parametrize login validation scenarios"
git commit -m "test(AQA-0038): add protected inventory route access test"
git commit -m "test(AQA-0057): add product to cart test"
git commit -m "chore(AQA-0064): review and stabilize cart workstream"
git commit -m "chore(AQA-0073): finalize phase 3c structure cleanup"
git commit -m "test(AQA-0078): add checkout information page tests"
git commit -m "test(AQA-0079): add checkout overview tests"
git commit -m "test(AQA-0080): add checkout completion tests"
git commit -m "chore(AQA-0082): finalize checkout automation workstream"
```

For documentation cleanup, checkpoint, or portfolio promotion work without a dedicated task ID, these examples are acceptable:

```bash
git commit -m "docs: clean documentation before main promotion"
git commit -m "chore: promote phase 3 portfolio state to main"
```

Common commit types:

* `feat` — new framework functionality
* `test` — automated tests or test-related changes
* `docs` — documentation changes
* `refactor` — structural improvements without behavior change
* `fix` — bug fixes
* `chore` — maintenance, configuration, review, or promotion changes

## Pull Request Flow

Pull Requests for regular development should usually follow this direction:

```text
feature/* -> develop
fix/* -> develop
docs/* -> develop
refactor/* -> develop
chore/* -> develop
```

Portfolio promotion flow:

```text
develop -> main
```

The `main` branch should only receive stable and validated changes.

The `develop` branch should remain the normal base branch for future implementation, documentation, refactor, and framework maturity work.

## Pull Request Checklist

Before opening a Pull Request, verify:

* local working tree is clean
* relevant commits are pushed
* local quality checks passed
* relevant scoped test module passed when applicable
* relevant marker suites passed when applicable
* full test suite passed
* documentation is updated if needed
* test case documentation is aligned with automated coverage
* marker documentation is aligned with current marker behavior when marker usage changes
* no generated reports or screenshots are tracked
* no cache files or virtual environment files are tracked
* branch target is correct
* implemented features are not mixed with planned future features
* cart-owned checkout entry behavior remains separated from detailed checkout behavior
* checkout information form, checkout overview, and checkout completion behavior remain owned by checkout tests

Recommended pre-PR commands:

```bash
git status
ruff check .
black --check .
isort . --check-only
pytest -v
```

For a workstream checkpoint, also run the relevant scoped test module and marker suites where useful.

Examples:

```bash
pytest -v tests/test_cart_page.py
pytest -v

pytest -v tests/test_checkout_page.py
pytest -m e2e -v
pytest -v
```

## Portfolio Promotion Workflow

Portfolio promotion is used when a completed and validated project state should become the stable public version on `main`.

Recommended portfolio promotion workflow:

1. Ensure `develop` contains the completed and validated project state.
2. Complete required documentation cleanup on `develop` or a dedicated documentation branch.
3. Verify that README and technical documentation describe the implemented state accurately.
4. Verify that planned future work is not described as already implemented.
5. Run local validation when possible.
6. Open a Pull Request from `develop` to `main`.
7. Wait for CI validation.
8. Review the diff from a recruiter or technical reviewer perspective.
9. Squash merge into `main` after validation.
10. Update local `main` and `develop`.
11. Continue future work from `develop`.

Portfolio promotion should not introduce unrelated new implementation scope. It should promote a stable, already validated snapshot.

Recommended promotion Pull Request title:

```text
chore: promote phase 3 portfolio state to main
```

Recommended promotion Pull Request body:

```text
Promotes the completed Phase 3 portfolio state from develop to main.

Includes:
- Login, Inventory, Product Details, Cart, and Checkout automation coverage
- synchronized README, docs, test cases, CI, and quality tooling
- stable portfolio branch validation through CI

Out of scope:
- Phase 4 framework maturity work
- API testing implementation
- Selenium comparison module
- Docker or Jenkins integration
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
* full Pytest test execution
* HTML report generation
* artifact upload

The current CI pipeline executes the full pytest suite rather than separate marker-based jobs.

Marker-based commands documented in this workflow are intended for selective local validation. Separate marker-based CI jobs should only be documented as implemented after the corresponding CI changes are completed.

A Pull Request should not be merged if CI fails.

This applies both to regular Pull Requests into `develop` and portfolio promotion Pull Requests into `main`.

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
chore(AQA-0073): finalize phase 3c structure cleanup
chore(AQA-0082): finalize checkout automation workstream
```

For portfolio promotion into `main`, a `chore` squash commit may be appropriate:

```text
chore: promote phase 3 portfolio state to main
```

## Post-Merge Workflow

### After Merge Into `develop`

After a Pull Request is merged into `develop`, update local `develop`:

```bash
git checkout develop
git pull origin develop
```

Check recent commits:

```bash
git log --oneline --decorate -5
```

Optionally delete the completed local source branch:

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

### After Promotion Into `main`

After a Pull Request is merged into `main`, update local branches:

```bash
git checkout main
git pull origin main
git checkout develop
git pull origin develop
git fetch --prune
```

Check recent commits on `main`:

```bash
git checkout main
git log --oneline --decorate -5
```

Future implementation, documentation, refactor, and framework maturity work should continue from `develop`.

## Phase And Workstream Checkpoint Workflow

Before moving to the next major project phase or before merging a completed workstream, a checkpoint task must be completed.

A checkpoint verifies:

* completed scope
* test coverage
* local validation
* relevant scoped test execution
* relevant marker suite execution where applicable
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
AQA-0073 — Phase 3C Final Validation And Documentation Sync
AQA-0082 — Checkout Workstream Final Validation And Documentation Sync
```

No new functional work should start before the relevant checkpoint is completed.

For portfolio promotion, the checkpoint should also verify that the project is suitable for public presentation through `main`.

## Documentation Updates

Documentation should be updated when changes affect:

* framework architecture
* project structure
* testing strategy
* marker strategy
* CI/CD workflow
* quality tooling
* roadmap
* feature list
* technology stack
* test case coverage
* README instructions

Documentation changes may be committed as part of the relevant task or as a separate documentation cleanup or stabilization task.

For automation work that implements a documented manual test case, update the related test case metadata in the same task when required.

For workstream final validation tasks, documentation should be checked for stale future-facing wording such as planned coverage that has already been implemented.

When pytest marker behavior changes, verify that:

* `pytest.ini` reflects the intended executable markers
* automated test usage matches the registered marker definitions
* test case metadata matches automated marker usage
* `docs/testing-strategy.md` describes the current marker semantics
* workflow and README commands do not reference removed markers

For portfolio promotion, documentation should also be checked for:

* stale workstream-finalization wording
* stale PR-readiness wording
* statements that suggest completed Phase 3 work exists only on `develop`
* implemented features mixed with planned future extensions
* missing distinction between `main` as the stable portfolio branch and `develop` as the integration branch

## Current Workflow Status

The current workflow supports completed Phase 3 page-level automation coverage for Login, Inventory, Product Details, Cart, and Checkout areas.

Phase 3 page-level automation coverage has been completed, reviewed, validated, squash-merged into `develop`, and promoted to `main` as the stable Phase 3 portfolio snapshot.

The `main` branch represents the polished portfolio version of the project. The `develop` branch remains the integration branch and may contain newer work after this document is read from `main`.

Future work should continue from `develop` unless a specific portfolio promotion or release task targets `main`.

## Summary

This workflow ensures that every change is developed, validated, reviewed, and integrated in a controlled way.

It supports:

* clean Git history
* professional Pull Request workflow
* reliable CI validation
* selective local marker-based validation
* readable project evolution
* safe workstream integration
* controlled portfolio promotion to `main`
* phase-based project management
* portfolio-ready repository standards
