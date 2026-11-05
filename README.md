# Playwright Python QA Automation Framework

A **completed Python UI test automation portfolio project** built around [Sauce Demo](https://www.saucedemo.com/). It demonstrates maintainable test design, browser automation, reproducible execution, and CI-backed quality checks.

**Playwright** is the primary automation framework, covering Login, Inventory, Product Details, Cart, and Checkout. Chromium runs the complete default test suite, while Firefox and WebKit provide representative Smoke coverage. A separate **Selenium WebDriver** suite demonstrates a Chrome-based end-to-end purchase journey. The framework also includes Docker execution, Chromium visual regression, pytest-html and Allure reporting, and automated code-quality checks.

## Repository at a glance

```text
pages/              Playwright Page Objects
tests/              Functional and framework utility tests
selenium_pages/     Selenium Page Objects
selenium_tests/     Selenium Chrome E2E showcase
visual_tests/       Visual regression checkpoints
visual_baselines/   Reviewed Chromium reference screenshots
framework/          Shared assertions, diagnostics, and image comparison
config/, test_data/ Runtime settings and reusable test data
test_cases/         Manual test cases and automation traceability
docs/               Detailed project documentation
.github/workflows/  GitHub Actions CI pipeline
```

## Quick start

Requires **Python 3.12** and a Linux/WSL environment. From a terminal:

```bash
git clone --branch develop https://github.com/B4GG1/playwright-python-qa-automation-framework.git
cd playwright-python-qa-automation-framework
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-lock.txt
playwright install --with-deps chromium
pytest -v
```

The default `pytest` command runs the Playwright functional tests **and framework utility tests** under `tests/`. Selenium and the dedicated visual checkpoints are selected separately.

Other useful entry points:

```bash
pytest -m smoke -v                             # Playwright Smoke
playwright install --with-deps firefox         # One-time setup for Firefox Smoke
QA_BROWSER=firefox pytest -m smoke -v          # Representative Firefox Smoke
pytest selenium_tests -m "selenium and e2e" -v  # Selenium E2E (requires Google Chrome)
```

WebKit, Docker, visual regression, runtime configuration, and reporting are covered in the execution guide.

## Explore the documentation

- [Project structure](docs/project-structure.md) — Explains the architecture, repository layout, component responsibilities, and locations of tests and artifacts.
- [Features](docs/features.md) — Summarizes the completed framework's implemented capabilities and functional test coverage.
- [Testing strategy](docs/testing-strategy.md) — Explains test design, manual-to-automation traceability, suite selection, markers, and isolation.
- [Execution and configuration](docs/execution-and-configuration.md) — Covers prerequisites, local and Docker execution, browser setup, and runtime settings.
- [CI, quality, and reporting](docs/ci-quality-and-reporting.md) — Describes GitHub Actions, quality checks, reports, diagnostics, and the Git/PR workflow.
- [Roadmap](docs/roadmap.md) — Summarizes the five completed development phases and the final project outcome.