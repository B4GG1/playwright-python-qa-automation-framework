# Testing Strategy

This document describes the testing strategy implemented in the **completed Playwright Python QA Automation Framework portfolio project**: what drives test selection, how automated scenarios are designed, and how the test suites complement one another. The framework tests [Sauce Demo](https://www.saucedemo.com/) with Playwright and Pytest as the primary automation stack, supported by a focused Selenium WebDriver showcase and controlled visual checks.

For the list of implemented capabilities, see [Framework Features](features.md). Component ownership and repository paths are described in [Project Structure](project-structure.md).

## Test Objectives and Priorities

The strategy focuses on observable application behavior and realistic e-commerce workflows. Priority is given to authentication and access protection, product selection, cart state, checkout validation, and order completion.

Tests cover successful and unsuccessful inputs, meaningful UI states, navigation, data consistency, and state transitions. Representative scenarios provide fast feedback; broader and parametrized scenarios check additional products, inputs, and conditions.

Automated checks are selected for their value and repeatability rather than to reproduce every documented manual scenario. Known application behavior and unautomated cases remain visible in the corresponding test case documentation; these do not indicate unfinished framework development.

## Test Cases and Traceability

Human-readable test cases in [`test_cases/`](../test_cases/) define scenario preconditions, steps, expected results, priorities, and automation status:

- [Login](../test_cases/login-page.md)
- [Inventory](../test_cases/inventory-page.md)
- [Product Details](../test_cases/product-details-page.md)
- [Cart](../test_cases/cart-page.md)
- [Checkout](../test_cases/checkout-page.md)

Scenarios are assigned to the area where the principal action or assertion occurs. For example, opening checkout from the Cart belongs to Cart coverage; validating checkout fields and order totals belongs to Checkout coverage.

The test case files record `Automation Status` and `Automated In`. Automated Playwright scenarios use recognizable `TC-...` identifiers in Pytest parameter IDs where applicable, making results easier to relate to the manual cases. A case marked `Planned` has no dedicated automation in the delivered scope and must not be presented as automated merely because a related workflow is covered. Such case-level status does not change the completed status of the project.

Framework configuration and diagnostic unit tests, cross-browser reruns, visual checkpoints, and the secondary Selenium showcase do not establish a second set of application-facing manual test cases.

## Test Suite Organization

Pytest markers express **test intent and selection**, not implementation phases. Tests may carry more than one marker.

| Marker       | Purpose                                                                |
|--------------|------------------------------------------------------------------------|
| `smoke`      | Fast, representative checks of critical application behavior.          |
| `regression` | Broader checks, including additional inputs, products, and states.     |
| `ui`         | Element presentation, visible state, and direct UI behavior.           |
| `security`   | Protected-route and authentication-access checks.                      |
| `sorting`    | Product order by name or price.                                        |
| `navigation` | Page transitions outside the login authentication transition.          |
| `e2e`        | Independent checkpoints along the primary Playwright purchase journey. |
| `visual`     | Screenshot comparison checks and visual-comparison utility tests.      |
| `selenium`   | Tests executed through Selenium WebDriver.                             |

Smoke and Regression are **selected subsets**, not replacements for the complete test collection. The unfiltered primary suite also includes tests without either marker, such as runtime configuration, diagnostics, and image-comparison utility tests. Marker combinations can overlap; they do not introduce additional copies of the same test implementation.

The Selenium showcase is selected independently using the `selenium` marker. Its 13 E2E checkpoints do not require the additional `e2e` marker.

## Test Design and Independence

- **Independent scenarios:** each test prepares its own prerequisites and must not rely on execution order or state produced by another test. This permits isolated execution and Playwright parallel workers.
- **Scenario fixtures:** reusable setup establishes an authenticated user, selected products, cart state, or a specific checkout stage without requiring earlier tests to pass.
- **Data-driven coverage:** shared login, product, and checkout datasets support parametrization, especially when the same behavior should be checked against multiple products or invalid inputs.
- **Page Objects and assertions:** Page Objects encapsulate selectors and interactions; test functions own expected outcomes. Playwright uses locator-based expectations for live UI state and Python assertions for extracted or calculated values. Shared assertion helpers reduce repeated checks.
- **Stable synchronization:** Playwright uses its waiting and assertion mechanisms; Selenium uses explicit waits and post-action conditions rather than depending on fixed sleeps.

The purchase journey is represented through **independently executable checkpoints**, not a chain of tests that share browser state. Selenium similarly starts a fresh Chrome WebDriver for each test and closes it afterward.

## Browser and Automation Strategy

**Playwright on Chromium** is the primary functional regression baseline. The complete suite runs on Chromium, while **Firefox and WebKit** rerun a representative Smoke subset for browser-engine compatibility. This balances useful cross-browser feedback against the cost of duplicating the entire matrix.

**Selenium on Chrome** provides a separate **13-checkpoint purchase-flow showcase**. It validates a representative alternative automation approach, not a second full regression suite. The Selenium tests retain independent setup and are executed sequentially.

**Visual regression** complements behavioral assertions rather than replacing them. Two approved checkpoints capture the default Inventory view and a Cart containing one product in a controlled, headless Chromium Docker environment. The comparison detects missing baselines, incompatible image dimensions, and pixel differences exceeding the configured tolerance. The approved test threshold allows up to **4.5% differing pixels**, so a passing visual check does not mean exact pixel equality.

Visual baselines are version-controlled and updated only through an explicit, reviewed refresh. Firefox and WebKit do not reuse Chromium visual baselines. The normal primary Pytest collection does not include the dedicated Selenium or screenshot-checkpoint directories, although visual-comparison utility tests belong to the primary suite.

## Validation Approach

Validation is proportional to the change and preserves the distinction between test suites:

| Change or risk                                         | Relevant validation                                                             |
|--------------------------------------------------------|---------------------------------------------------------------------------------|
| Application behavior or Page Objects                   | Affected test module and marker suites; complete Chromium suite when warranted. |
| Shared fixtures, data, or execution settings           | Relevant functional tests plus broader isolation or parallel-execution checks.  |
| Cross-browser compatibility                            | Representative Firefox and WebKit Smoke suites.                                 |
| Screenshot comparison or baseline handling             | Visual utility tests and controlled Docker/Chromium visual checkpoints.         |
| Selenium Page Objects, fixtures, or WebDriver behavior | Selenium E2E suite covering all 13 independent checkpoints.                     |
| Framework integration or release-readiness             | Quality checks and the applicable GitHub Actions test jobs.                     |

The CI pipeline independently validates code quality, Chromium Smoke, Regression and the full suite, Firefox/WebKit Smoke, Docker-based visual regression, and Selenium E2E. Its detailed job configuration and reporting behavior are documented in [CI, Quality, and Reporting](ci-quality-and-reporting.md).

## Scope Boundaries

The implemented strategy is focused on **web UI automation**. It does not claim API test coverage, full Firefox/WebKit regression, a multi-browser Selenium matrix, or cross-browser visual baseline coverage. Test outcomes are evidence for the scenarios and environments actually executed, not a guarantee about untested combinations.