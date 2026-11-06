# Framework Features

This document presents the final, implemented capabilities of the **completed Playwright Python QA Automation Framework portfolio project**. The framework automates the [Sauce Demo](https://www.saucedemo.com/) web application, with Playwright as its primary automation engine and a focused Selenium WebDriver E2E showcase.

## Functional Test Coverage

The primary Playwright suite validates the following application areas:

| Area                 | Automated capabilities                                                                                                                                    |
|----------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Login**            | Valid and invalid authentication, missing credentials, locked-out user, form behavior, keyboard submission, and access protection for application routes. |
| **Inventory**        | Product listing and details, sorting by name or price, cart actions, cart badge updates, and navigation to product details.                               |
| **Product Details**  | Product information, navigation, add/remove actions, and cart badge behavior across representative and parametrized product scenarios.                    |
| **Cart**             | Empty and populated states, product contents, item removal, badge changes, navigation, and cart persistence across logout and login.                      |
| **Checkout**         | Required-field validation, order overview, product and price summaries, checkout completion, confirmation, and return navigation.                         |
| **Purchase journey** | Independently executable end-to-end checkpoints covering the path from login through checkout completion and return to inventory.                         |

Human-readable scenarios and their automation status are maintained in [`test_cases/`](../test_cases/). Test selection and coverage decisions are explained in [Testing Strategy](testing-strategy.md).

## Browser Automation and Visual Testing

| Capability             | What is implemented                                                                                                                                                                                                                                              |
|------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Playwright**         | Primary UI automation with a complete Chromium test suite, plus representative Smoke compatibility checks in Firefox and WebKit.                                                                                                                                 |
| **Selenium WebDriver** | Separate, Chrome-only purchase-flow showcase consisting of 13 independent E2E checkpoints, with its own Page Objects and browser lifecycle.                                                                                                                      |
| **Visual regression**  | Two controlled Chromium screenshot checkpoints: the default Inventory view and a Cart containing one product. Screenshots are compared with approved PNG baselines using an explicit difference threshold; mismatches beyond the threshold produce visual diffs. |

Browser coverage is intentionally asymmetric: **Firefox and WebKit run representative Smoke tests, not the full Chromium regression suite**. Selenium does not duplicate the complete Playwright test coverage, and the visual checkpoints are limited to headless Chromium in the controlled Docker environment.

## Execution and Framework Capabilities

| Capability                            | What is implemented                                                                                                                                                              |
|---------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Test selection**                    | Pytest marker-based suites for Smoke, Regression, UI, Security, Sorting, Navigation, and E2E; dedicated markers for Selenium and visual checks.                                  |
| **Sequential and parallel execution** | Standard sequential Pytest runs and `pytest-xdist` parallel execution for the primary Playwright suite. Selenium E2E and visual checkpoints run separately and sequentially.     |
| **Reusable test design**              | Page Object Model, independent scenario fixtures, centralized test data, parametrization, and shared assertion helpers.                                                          |
| **Runtime configuration**             | Environment-based application URL, browser selection, headless/headed mode, timeouts, and screenshot, trace, and video policies, with input validation.                          |
| **Docker execution**                  | Reproducible Playwright/Pytest execution from a version-aligned container image, supporting selected suites, parallel workers, runtime overrides, and host-persistent artifacts. |

## CI, Reporting, and Diagnostics

| Capability                 | What is implemented                                                                                                                                                                |
|----------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Continuous integration** | GitHub Actions jobs for code quality, Chromium Smoke, Regression and full suite, Firefox and WebKit Smoke, Docker-based visual regression, and Selenium E2E on Chrome.             |
| **Code quality**           | Automated Ruff, Black, and isort checks, with pre-commit hooks available for local development.                                                                                    |
| **Test reporting**         | Pytest HTML reports and Allure results; the Chromium full-suite CI job also generates an Allure HTML report. CI uploads selected reports and other evidence as workflow artifacts. |
| **Failure diagnostics**    | Playwright runtime and failure summaries, configurable failure screenshots, traces and videos, plus Selenium failure screenshots and diagnostic details.                           |
| **Visual evidence**        | Reviewed baselines, generated actual screenshots, highlighted image diffs on threshold-exceeding mismatches, and explicitly controlled baseline updates.                           |

For component ownership and artifact locations, see [Project Structure](project-structure.md). For test execution and runtime settings, see [Execution and Configuration](execution-and-configuration.md). For GitHub Actions, code-quality checks, reporting, and diagnostics, see [CI, Quality, and Reporting](ci-quality-and-reporting.md). Test selection and design rationale are covered in [Testing Strategy](testing-strategy.md).