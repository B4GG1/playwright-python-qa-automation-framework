# Development Workflow

This document describes the day-to-day development workflow used in this project.
For detailed branching rules, see: [Git Branching Strategy](git-branching-strategy.md).

## Standard Task Workflow

For every implementation task, the recommended workflow is:

1. Start from the latest `develop` branch.
2. Create a dedicated feature or fix branch.
3. Implement changes locally.
4. Run local checks.
5. Commit changes with a meaningful message.
6. Push the branch to GitHub.
7. Open a Pull Request into `develop`.
8. Wait for CI validation.
9. Merge using squash merge after validation.

## Branch Creation

Example:

```bash
git checkout develop
git pull origin develop
git checkout -b feature/login-page-object
```

## Local Validation

Before pushing changes, run:
```
ruff check .
black --check .
isort . --check-only
pytest -v
```

## Commit Convention

Commit messages should include the task ID when applicable.

Example:
```
git commit -m "feat(AQA-0026): create login page object model"
```

## Pull Request Flow

Pull Requests should follow this direction:
```
feature/* -> develop
develop -> main
```

The main branch should only receive stable and validated changes.

## CI Integration

GitHub Actions validates changes on:

* push to `main`
* push to `develop` 
* pull requests targeting `main` 
* pull requests targeting `develop` 
* manual workflow dispatch

## Summary

This workflow ensures that every change is developed, validated, and integrated in a controlled way.