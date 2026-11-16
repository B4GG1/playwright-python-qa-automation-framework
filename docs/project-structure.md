# Project Structure and Architecture

This document describes the final architecture of the **completed QA automation portfolio project**: how its components interact and where to find tests, configuration, screenshots, reports, and other artifacts. It documents the delivered implementation rather than its development history.

## Architecture at a Glance

The project uses **Playwright with Python and Pytest** as its primary browser automation stack. **Selenium WebDriver** provides a separate, deliberately limited Chrome E2E showcase. Both operate against [Sauce Demo](https://www.saucedemo.com/) and reuse browser-independent test data, but each has its own Page Objects and browser fixtures.

The main responsibilities are separated as follows:

| Layer                | Responsibility                                                                          |
|----------------------|-----------------------------------------------------------------------------------------|
| Test cases           | Human-readable scenarios and links to automation coverage; not executable test modules. |
| Tests                | Assert application behavior and orchestrate scenarios.                                  |
| Page Objects         | Locate UI elements and expose browser-specific interactions.                            |
| Test data            | Provide reusable credentials, products, and checkout inputs.                            |
| Framework utilities  | Supply shared assertions, diagnostics, and image comparison.                            |
| Runtime and fixtures | Configure browsers, contexts, test setup, and cleanup.                                  |
| Reporting            | Collect execution results and diagnostic evidence.                                      |

The Playwright and Selenium implementations do not share browser-specific Page Objects. Pytest coordinates their execution, while configuration and test data can be reused where applicable.

## Repository Map

```text
playwright-python-qa-automation-framework/
├── .github/workflows/ci.yml       # GitHub Actions validation and reporting
├── config/                        # Shared runtime settings
├── docs/                          # Technical and project documentation
├── framework/
│   ├── assertions/                # Reusable application assertions
│   ├── diagnostics.py             # Runtime and failure diagnostic messages
│   └── visual_regression.py       # PNG comparison and visual diff generation
├── pages/                         # Playwright Page Objects
├── resources/                     # Supporting project resources
├── selenium_pages/                # Selenium-specific Page Objects
├── selenium_tests/                # Selenium E2E tests and WebDriver fixtures
│   ├── conftest.py                # Selenium browser lifecycle and fixtures
│   └── test_purchase_e2e.py       # 13 independent E2E checkpoints
├── test_cases/                    # Manual test cases and automation traceability
├── test_data/                     # Shared application test data
├── tests/                         # Primary Playwright tests and utility tests
│   └── conftest.py                # Playwright application scenario fixtures
├── visual_baselines/chromium/     # Version-controlled reference screenshots
├── visual_tests/                  # Dedicated visual screenshot checkpoints
│   └── conftest.py                # Visual-only browser and rendering constraints
├── reports/                       # Generated HTML reports and other evidence
├── conftest.py                    # Framework-wide Pytest integration
├── pytest.ini                     # Test discovery and marker registration
├── pyproject.toml                 # Code quality configuration
├── requirements.txt               # Direct Python dependencies
├── requirements-lock.txt          # Pinned Python dependency versions
├── Dockerfile                     # Reproducible Playwright container environment
├── .dockerignore                  # Docker build-context exclusions
├── .gitignore                     # Local/generated file exclusions
└── README.md                      # Project entry point and documentation index
```

The tree highlights the main responsibilities, not every source file. Paths for generated reports are described below; they may be created only after the corresponding test run.

## Test and Page Object Ownership

### Playwright

`tests/` holds the primary functional suite for Login, Inventory, Product Details, Cart, and Checkout, as well as supporting checks such as runtime configuration and the visual comparison utility. Functional tests call the Page Objects in `pages/` and reuse inputs from `test_data/` and assertions from `framework/assertions/`.

The Playwright Page Object layer encapsulates selectors, interactions, and page-specific behavior. Tests own the expected outcomes; Page Objects do not own test scenarios or reporting configuration.

`tests/conftest.py` provides application-level fixtures, including scenario setup. The repository-root `conftest.py` owns the framework-wide Pytest integration: Playwright runtime options, context timeouts, diagnostics, and failure screenshot handling.

### Selenium

`selenium_tests/` contains **13 independent E2E checkpoints** covering the purchase journey, implemented in `test_purchase_e2e.py`. `selenium_pages/` provides a separate Selenium Page Object hierarchy with explicit waits and WebDriver interactions.

`selenium_tests/conftest.py` creates a fresh headless Chrome WebDriver for each test, prepares Selenium scenarios, and closes the driver after execution. Selenium shares applicable configuration values and test data with Playwright, but not Playwright browser fixtures or Page Objects.

### Visual Regression

`visual_tests/` contains two dedicated screenshot checkpoints: the default Inventory view and a Cart with one product. These tests use the Playwright page layer and `framework/visual_regression.py` to compare captured PNGs with approved baselines.

`visual_tests/conftest.py` enforces Chromium-only, headless execution and a controlled rendering configuration. Approved screenshots live in `visual_baselines/chromium/`; generated screenshots and differences are stored separately under `reports/visual/`.

## Test Discovery and Execution Boundaries

`pytest.ini` sets `testpaths = tests`. Consequently, an ordinary `pytest` run collects the primary test suite, **not** the dedicated Selenium or visual checkpoint directories.

| Execution path                          | Test location     | Browser scope       | How it is selected                                                      |
|-----------------------------------------|-------------------|---------------------|-------------------------------------------------------------------------|
| Primary functional and supporting suite | `tests/`          | Chromium by default | Standard Pytest collection; markers select Smoke or Regression subsets. |
| Representative cross-browser Smoke      | `tests/`          | Firefox or WebKit   | Same Smoke tests with an explicit browser override.                     |
| Selenium E2E showcase                   | `selenium_tests/` | Headless Chrome     | Explicit directory and `selenium` marker selection.                     |
| Visual checkpoints                      | `visual_tests/`   | Headless Chromium   | Explicit directory and `visual` marker selection.                       |

The Selenium E2E suite is selected with:

```bash
pytest selenium_tests -m selenium -v
```

The Playwright suite supports sequential execution and Pytest-xdist parallel workers. The dedicated Selenium E2E and visual screenshot runs are executed sequentially. Browser-specific execution does not require duplicated functional test modules.

`config/settings.py` centralizes supported `QA_*` environment settings for the application URL, browser, headed mode, timeouts, and screenshot/trace/video policies. The Playwright integration uses the applicable settings; Selenium reuses the application URL and timeout subset. See [Testing Strategy](testing-strategy.md) for test selection and [Execution and Configuration](execution-and-configuration.md) for runtime settings and execution commands.

## Configuration and Framework Responsibilities

| File or location                 | Ownership                                                                                     |
|----------------------------------|-----------------------------------------------------------------------------------------------|
| `config/settings.py`             | Reads and validates environment-based runtime settings.                                       |
| Root `conftest.py`               | Integrates Playwright with Pytest and handles common runtime diagnostics.                     |
| `tests/conftest.py`              | Prepares reusable Playwright application scenarios.                                           |
| `selenium_tests/conftest.py`     | Owns ChromeDriver lifecycle and Selenium-specific fixtures.                                   |
| `visual_tests/conftest.py`       | Enforces visual execution constraints and explicit baseline refresh controls.                 |
| `framework/assertions/`          | Provides reusable assertions for application data and behavior.                               |
| `framework/diagnostics.py`       | Formats runtime and failure diagnostics.                                                      |
| `framework/visual_regression.py` | Compares PNG files and produces a highlighted diff when the configured threshold is exceeded. |
| `pytest.ini`                     | Defines collection defaults and test markers.                                                 |
| `pyproject.toml`                 | Configures Ruff, Black, and isort.                                                            |
| `.github/workflows/ci.yml`       | Defines GitHub Actions quality and test jobs.                                                 |

Each test is expected to set up its own prerequisites rather than depend on state left by another test. This isolation supports both sequential runs and Playwright's parallel workers.

## Screenshots, Reports, and Other Artifacts

The repository distinguishes **approved source assets** from **generated execution evidence**.

| Location                                            | What to find there                                                          | Version control     |
|-----------------------------------------------------|-----------------------------------------------------------------------------|---------------------|
| `visual_baselines/chromium/`                        | Approved visual reference PNGs                                              | Tracked             |
| `reports/visual/actual/`                            | Screenshots from visual checkpoint execution                                | Generated / ignored |
| `reports/visual/diff/`                              | Highlighted PNGs produced on visual mismatches                              | Generated / ignored |
| `reports/screenshots/`                              | Playwright failure screenshots                                              | Generated / ignored |
| `reports/selenium/screenshots/`                     | Selenium failure screenshots                                                | Generated / ignored |
| `reports/*.html`                                    | Pytest HTML reports when requested or generated by CI                       | Generated / ignored |
| `reports/allure-results/`, `reports/allure-report/` | Allure results and generated HTML output in the CI layout                   | Generated / ignored |
| `test-results/`                                     | Pytest-Playwright traces, videos, and related browser evidence when enabled | Generated / ignored |
| `allure-results/`, `allure-report/`                 | Optional local Allure output locations                                      | Generated / ignored |

Not every run generates every artifact. Failure screenshots depend on test failures and the configured policy; traces and videos depend on their runtime policies. Visual baseline updates require an explicit command and review; normal comparison does not approve new baselines.

`.gitignore` excludes generated reports and browser artifacts while allowing the repository's `reports/.gitkeep` placeholder. The CI workflow uploads selected reports and evidence as GitHub Actions artifacts; their upload and retention rules are documented in [CI, Quality, and Reporting](ci-quality-and-reporting.md).

## Execution Environments

The same primary Playwright framework can run locally or in the repository's Docker image. Chromium supports the full functional suite; Firefox and WebKit are used for representative Smoke compatibility checks. The visual CI job uses the Docker environment to keep Chromium screenshot conditions consistent.

Selenium E2E runs separately using Chrome on the host or GitHub Actions runner. It is not part of the default Playwright suite or the dedicated visual Docker job.

For setup and execution commands, see [Execution and Configuration](execution-and-configuration.md). For test-selection principles, see [Testing Strategy](testing-strategy.md). For CI jobs, reports, and artifact retention, see [CI, Quality, and Reporting](ci-quality-and-reporting.md). For a high-level project overview, return to the [README](../README.md).