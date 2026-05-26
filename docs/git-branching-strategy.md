# Git Branching & Merge Strategy

## Branching Model

This repository follows a lightweight Git workflow inspired by a simplified Git Flow model.
The main goal is to ensure:

* clean and traceable history
* isolated feature development
* safe integration into stable branches

## Branch Structure

``` main ```
* production-ready state of the repository 
* always stable 
* protected branch (no direct pushes allowed)
* updated only via Pull Request (PR)

``` develop ```
* integration branch for ongoing development 
* contains merged features before release to main 
* optional staging area for validation 

### Feature / Bugfix branches

All development work is done on dedicated branches created from develop:

Naming conventions:
```
feature/<short-description>
fix/<short-description>
```
Examples:
```
feature/playwright-setup
feature/api-client
fix/login-timeout
```

## Merge Strategy

### Squash Merge (recommended)

All Pull Requests should be merged using:
> Squash and Merge

Why:
* keeps commit history clean
* one feature = one commit in main / develop
* easier rollback
* better readability for recruiters / reviewers

## Direct Push Policy

Direct pushes are NOT allowed to:

* ``` main ```
* ``` develop ```

All changes must go through:
> Feature branch → Pull Request → Review → Merge

## Branch Protection Rules

Recommended GitHub settings:

``` main ```
* require pull request before merging 
* require status checks (CI pipeline)
* disallow force push 
* disallow direct commits 

``` develop ```
* optional protection (recommended for teams)
* allow PR-only merges

## Pull Request Workflow

1. Create branch from develop 
2. Implement changes 
3. Run local checks 
   * lint (ruff)
   * formatting (black)
   * tests (pytest)
4. Push branch 
5. Open Pull Request 
6. CI pipeline runs automatically 
7. Code review (optional in solo project but recommended practice)
8. Squash merge

## Summary

This workflow ensures:
- predictable development process 
- CI/CD integration safety 
- clean Git history 
- professional QA engineering standards