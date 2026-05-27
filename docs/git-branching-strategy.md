# Git Branching And Merge Strategy

This document defines the branching strategy, merge workflow, and repository standards used in this project.
The goal is to keep the repository history clean, support isolated development, and ensure that changes are validated before being merged into stable branches.

## Branching Model

This repository follows a lightweight Git workflow inspired by a simplified Git Flow model.

The main goals are:

- clean and traceable history
- isolated feature development
- safe integration into stable branches
- CI validation before merging changes

## Branch Structure

### `main`

The `main` branch represents the stable state of the repository.

Rules:

- should always remain stable
- should contain validated changes only
- should be updated through Pull Requests
- should not receive direct pushes

### `develop`

The `develop` branch is the main integration branch for ongoing development.

Rules:

- used as the base branch for feature work
- receives completed work through Pull Requests
- should remain reasonably stable
- acts as the staging area before changes are promoted to `main`

### Feature Branches

Feature branches are used for new functionality or planned framework improvements.

Naming convention:

```text
feature/<short-description>
```

Examples:

```text
feature/login-page-object
feature/api-client
feature/playwright-setup
```

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
```

## Merge Strategy

The recommended merge strategy is:

> Squash and Merge

Squash merge combines all commits from a feature branch into a single commit on the target branch.

Benefits:

- keeps commit history clean
- one task becomes one logical commit
- simplifies rollback
- improves readability for reviewers and recruiters
- reduces noisy commit history

## Direct Push Policy

Direct pushes should be avoided for:

- `main`
- `develop`

Recommended workflow:

```text
feature branch -> Pull Request -> CI validation -> Review -> Squash Merge
```

## Branch Protection Rules

Recommended GitHub branch protection settings are listed below.

### `main`

Recommended rules:

- require Pull Request before merging
- require CI status checks to pass
- disallow force pushes
- disallow direct commits
- require linear history if appropriate

### `develop`

Recommended rules:

- require Pull Request before merging
- require CI status checks to pass
- disallow force pushes where practical

For a solo portfolio project, these rules can be introduced gradually as the workflow matures.

## Pull Request Workflow

Standard Pull Request workflow:

1. Start from the latest `develop` branch.
2. Create a dedicated feature, fix, or documentation branch.
3. Implement changes locally.
4. Run local checks.
5. Push the branch to GitHub.
6. Open a Pull Request into `develop`.
7. Wait for CI pipeline validation.
8. Review changes manually.
9. Squash merge after validation.

Promotion to `main` should happen only after `develop` contains stable and validated changes.

## Local Validation Before Pull Request

Recommended local checks:

```bash
ruff check .
black --check .
isort . --check-only
pytest -v
```

## Summary

This strategy ensures:

- predictable development process
- clean Git history
- controlled integration workflow
- CI/CD integration safety
- professional repository standards
- scalable workflow for future collaboration