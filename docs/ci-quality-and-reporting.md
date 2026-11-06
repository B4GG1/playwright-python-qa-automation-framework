# CI, Quality, and Reporting

This document describes the CI pipeline, code-quality controls, reporting, and failure diagnostics implemented in the **completed Playwright Python QA Automation Framework portfolio project**. It also records the Git and Pull Request workflow used during project development.

For test selection and automation principles, see [Testing Strategy](testing-strategy.md). For local setup, execution commands, and runtime settings, see [Execution and Configuration](execution-and-configuration.md). Component ownership and artifact locations are covered in [Project Structure](project-structure.md).

## GitHub Actions Pipeline

The workflow is defined in `.github/workflows/ci.yml`. It runs on pushes and Pull Requests targeting `develop` or `main`, and it supports manual execution through `workflow_dispatch`.

All jobs use GitHub-hosted Ubuntu 24.04 runners. Python-based jobs install Python 3.12 and project dependencies from `requirements-lock.txt`. The workflow uses read-only repository permissions (`contents: read`).

**The `quality` job is the prerequisite for every test job.** Once it succeeds, the independent test jobs can execute concurrently. The cross-browser matrix creates two separate executions, producing eight CI executions in total:

| CI execution                    | Validation                                                            | Environment                                 |
|---------------------------------|-----------------------------------------------------------------------|---------------------------------------------|
| `quality`                       | Ruff, Black, and isort                                                | Python 3.12                                 |
| `smoke`                         | Representative Playwright Smoke tests                                 | Chromium, pytest-xdist                      |
| `regression`                    | Broader Playwright Regression tests                                   | Chromium, pytest-xdist                      |
| `full-suite`                    | Complete default Pytest collection, including framework utility tests | Chromium, pytest-xdist                      |
| `cross-browser-smoke` — Firefox | Existing representative Smoke selection                               | Firefox, pytest-xdist                       |
| `cross-browser-smoke` — WebKit  | Existing representative Smoke selection                               | WebKit, pytest-xdist                        |
| `visual-regression`             | Two reviewed screenshot checkpoints                                   | Headless Chromium inside Docker, sequential |
| `selenium-e2e`                  | 13 independent purchase-journey checkpoints                           | Headless Chrome, sequential                 |

The complete default Pytest collection is rooted at `tests/`; it does not implicitly include `visual_tests/` or `selenium_tests/`. The Selenium CI job explicitly selects the 13 independent E2E tests from `selenium_tests/` using the `selenium` marker:

```bash
pytest selenium_tests -m selenium -v
```

The Playwright functional jobs run natively on GitHub-hosted runners. Only the visual regression job builds and runs the project's Docker image. The Selenium job uses the runner's installed Chrome and Selenium Manager, rather than the Playwright Docker image.

The pipeline does not claim full Regression coverage on Firefox or WebKit, a Selenium browser matrix, or cross-browser visual comparisons. Pytest-xdist distributes Playwright tests across workers; it does not change the test selection or provide test retries.

## Code Quality

The same static checks are available locally and enforced by the `quality` job:

| Tool           | Responsibility                                                     | Configuration             |
|----------------|--------------------------------------------------------------------|---------------------------|
| **Ruff**       | Linting, error detection, and import-related rules (`E`, `F`, `I`) | `pyproject.toml`          |
| **Black**      | Consistent Python formatting                                       | `pyproject.toml`          |
| **isort**      | Consistent import ordering, compatible with Black                  | `pyproject.toml`          |
| **pre-commit** | Runs the configured tool hooks before local commits                | `.pre-commit-config.yaml` |

Run the same non-mutating checks as CI:

```bash
ruff check .
black --check .
isort . --check-only
```

To enable or invoke the local hooks:

```bash
pre-commit install
pre-commit run --all-files
```

The configuration uses Black and isort line lengths of 100, while Ruff has a configured line length of 200. These settings are defined in the repository and should not be assumed to be identical. The `quality` job checks code style and linting; functional tests are executed by separate CI jobs.

## Test Reports and CI Artifacts

**pytest-html** produces self-contained HTML reports for the functional Playwright jobs, browser-specific Smoke runs, and Selenium E2E. **Allure** is additionally generated for the complete Chromium suite, using Pytest result data and the Allure CLI. The full-suite job attempts HTML generation after test execution even if tests fail, provided result data exists.

| CI execution         | Report and uploaded artifact names                                     |
|----------------------|------------------------------------------------------------------------|
| Chromium Smoke       | `smoke-pytest-html-report`, `smoke-test-artifacts`                     |
| Chromium Regression  | `regression-pytest-html-report`, `regression-test-artifacts`           |
| Chromium full suite  | `pytest-html-report`, `full-suite-allure-report`, `test-artifacts`     |
| Firefox/WebKit Smoke | `<browser>-smoke-pytest-html-report`, `<browser>-smoke-test-artifacts` |
| Visual Regression    | `visual-regression-artifacts` (generated actual/diff PNGs)             |
| Selenium E2E         | `selenium-e2e-pytest-html-report`                                      |

The workflow sets artifact retention to **seven days**. Upload steps use `if: always()` so an executed job can publish available evidence even after a test failure. This does not guarantee an artifact when the source file was never generated, or when an earlier prerequisite prevents the job from starting.

The visual job uploads generated comparison images from `reports/visual/`; approved screenshot baselines are version-controlled separately. The Selenium job uploads its HTML report **but not the separate Selenium screenshot directory**. This is an important distinction when reviewing CI failures.

Locally, report output is opt-in through Pytest options and Allure result generation. The standalone Allure CLI is required to render local HTML reports. Setup and command examples are provided in [Execution and Configuration](execution-and-configuration.md).

## Diagnostics and Failure Evidence

The framework complements test reports with contextual evidence:

- **Runtime summary:** the Playwright execution header shows effective browser, URL, headless mode, timeouts, and screenshot/trace/video policies. Under pytest-xdist, the controlling process reports the summary without duplicating it for every worker.
- **Playwright failure diagnostics:** failed setup, call, or teardown reports include the test identity, failure phase, and available page URL. On a failed test call with a Playwright page, the enabled project screenshot policy also attempts to save a screenshot and attach it to Allure when possible.
- **Selenium failure diagnostics:** on failed setup or call phases, the Selenium hook records the available URL and attempts a screenshot if a WebDriver instance exists.
- **Traces and videos:** Playwright supports optional trace and video recording for debugging. Both policies are set to `off` in the functional CI jobs; they are not automatically produced by every run.
- **Visual differences:** the controlled screenshot comparator reports differing pixels and changed bounds; an above-threshold mismatch produces a highlighted diff PNG. A passing comparison can include differences within the approved tolerance and does not imply pixel-perfect equality.

To investigate a failure, start with the failing CI execution and its Pytest report, then inspect the available diagnostic context and uploaded artifacts. For visual mismatches, compare actual and diff images against the reviewed baseline. Reproduce the relevant scenario using the execution guide rather than changing a baseline solely to make a failed job pass.

Generated runtime outputs belong to Git-ignored locations. Only deliberately reviewed reference screenshots under `visual_baselines/` are tracked in Git; output paths and ownership are listed in [Project Structure](project-structure.md).

## Git and Pull Request Workflow

The repository uses two long-lived branch roles: **`develop`** for integrating validated changes and **`main`** for stable portfolio snapshots. During project development, scoped work was prepared on appropriately named feature, fix, documentation, or refactor branches based on `develop`.

The development workflow followed these steps:

1. Create a dedicated branch for scoped changes.
2. Validate the changes locally with relevant tests and code-quality checks.
3. Commit using Conventional Commits and push the branch.
4. Open a Pull Request targeting `develop`.
5. Review the changes and GitHub Actions results, resolve problems, and merge validated changes (normally using squash merge).
6. Update the local integration branch and clean up obsolete work branches when appropriate.

Promotion to `main` was treated as a separate reviewed portfolio decision, not an automatic consequence of merging into `develop`. This section documents the workflow applied to the completed project; it does not imply ongoing implementation or assert that GitHub branch-protection settings technically enforce every rule.

## Documentation Boundaries

This document owns **CI behavior, code-quality checks, report interpretation, failure evidence, and the Git/PR review process**. It does not duplicate the detailed test-selection rationale in [Testing Strategy](testing-strategy.md), the executable setup commands in [Execution and Configuration](execution-and-configuration.md), or the component and artifact directory map in [Project Structure](project-structure.md).