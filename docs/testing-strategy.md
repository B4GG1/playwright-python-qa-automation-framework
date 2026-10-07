# Testing Strategy

This document defines the testing approach for the QA automation framework.

The current focus is UI automation testing for the Sauce Demo application using Playwright and Pytest. The project follows an iterative testing strategy: manual test design is created before or alongside automation, selected scenarios are automated, and repeated interactions are gradually refactored into reusable framework components.

The strategy documented here reflects the current implemented test structure, normalized pytest marker behavior, Phase 4B CI execution strategy, Phase 4C Pytest parallel execution strategy, Phase 4D reporting strategy, Phase 4E runtime configuration strategy, and Phase 4F diagnostics and fixture responsibility cleanup.

The `main` branch represents the stable portfolio version, while `develop` and active workstream branches may contain newer validated changes before they are promoted to `main`.

## System Under Test

* Application: Sauce Demo
* Default URL: `https://www.saucedemo.com`

The default application origin is supplied through the centralized runtime configuration layer.

The application origin can be overridden for a test process through:

    QA_BASE_URL

without editing functional tests or Page Objects.

Sauce Demo is used as a stable training application for practicing UI automation, test design, Page Object Model, test data management, fixtures, parametrization, selective suite execution, parallel test execution, runtime configuration, diagnostics, CI validation, reporting, and framework development.

## Testing Approach

The project follows a progressive testing approach:

1. Identify test scenarios manually.
2. Write clear test cases.
3. Decide which scenarios should be automated.
4. Prepare test data when needed.
5. Implement automated tests using Playwright and Pytest.
6. Refactor repeated interactions into Page Object Model components.
7. Extract shared authenticated-page behavior when it is reused across pages.
8. Extract reusable assertions when the same validation logic is needed across multiple page areas.
9. Use explicit scenario-oriented fixtures to reduce repeated setup.
10. Keep framework-level Pytest hooks separate from application scenario fixtures.
11. Use parametrization for repeated data-driven scenarios.
12. Categorize tests with explicit pytest markers.
13. Keep environment-specific execution behavior outside functional tests.
14. Use centralized runtime configuration for supported execution overrides.
15. Provide lightweight runtime diagnostics without introducing persistent log files.
16. Provide failed-test diagnostic context without changing functional test intent.
17. Validate relevant marker suites and test modules locally.
18. Validate the complete test suite locally when required.
19. Validate supported parallel execution when execution behavior or isolation is affected.
20. Validate runtime configuration behavior when execution settings change.
21. Validate diagnostic behavior with controlled failures when diagnostic hooks change.
22. Collect reporting and failure evidence appropriate to the execution context.
23. Validate code quality and automated suites through GitHub Actions.
24. Update test case and project documentation when coverage or strategy changes.
25. Promote stable validated snapshots from `develop` to `main` when they are ready for portfolio presentation.

This approach supports both QA thinking and automation engineering practice.

## Test Case Design

Test cases should be documented before or alongside automation work.

Recommended location:

    test_cases/

Each test case should include:

* test case ID
* title
* preconditions
* test data
* steps
* expected result
* test type
* priority
* automation candidate status
* automation status
* reference to automated test file when applicable

Current test case documentation:

    test_cases/login-page.md
    test_cases/inventory-page.md
    test_cases/product-details-page.md
    test_cases/cart-page.md
    test_cases/checkout-page.md

Current test case identifiers include:

* `TC-LOGIN-XXX`
* `TC-INVENTORY-XXX`
* `TC-PRODUCT-DETAILS-XXX`
* `TC-CART-XXX`
* `TC-CHECKOUT-XXX`

These identifiers are also used in parametrized pytest output where practical.

A documented test case may be marked as `Planned` before dedicated automation is implemented.

The corresponding test case file remains the authoritative source for individual automation status.

Runtime configuration validation and Phase 4F framework diagnostics do not represent new product-facing manual test cases and therefore do not require separate test case automation metadata.

## Current Automated Test Modules

Current functional automated test modules follow the one-test-file-per-covered-page-area principle:

    tests/test_login_page.py
    tests/test_inventory_page.py
    tests/test_product_details_page.py
    tests/test_cart_page.py
    tests/test_checkout_page.py

Each functional automated test module maps to the corresponding manual test case file:

| Automated Test Module                | Manual Test Case File                | Documented Test Case Range     |
|--------------------------------------|--------------------------------------|--------------------------------|
| `tests/test_login_page.py`           | `test_cases/login-page.md`           | `TC-LOGIN-001`–`019`           |
| `tests/test_inventory_page.py`       | `test_cases/inventory-page.md`       | `TC-INVENTORY-001`–`022`       |
| `tests/test_product_details_page.py` | `test_cases/product-details-page.md` | `TC-PRODUCT-DETAILS-001`–`015` |
| `tests/test_cart_page.py`            | `test_cases/cart-page.md`            | `TC-CART-001`–`013`            |
| `tests/test_checkout_page.py`        | `test_cases/checkout-page.md`        | `TC-CHECKOUT-001`–`020`        |

The documented test case ranges above are currently fully covered by automation.

Individual coverage details and automation metadata remain authoritative in the corresponding test case files.

The framework additionally includes focused runtime configuration validation:

    tests/test_runtime_config.py

This module validates configuration defaults, supported overrides, normalization, and invalid-value behavior.

It is framework validation rather than page-level product coverage.

## Current Test Coverage

The current automated functional test coverage focuses on Sauce Demo Login, Inventory, Product Details, Cart, and Checkout behavior.

### Login Coverage

Implemented Login coverage includes:

* successful login with valid credentials
* invalid username validation
* invalid password validation
* empty username validation
* empty password validation
* empty credentials validation
* locked out user validation
* combined invalid username and password validation
* error message close behavior
* login page elements visibility
* password field masking validation
* login form submission with Enter key
* protected Inventory route access validation
* protected Cart route access validation
* protected Product Details route access validation
* protected Checkout Information route access validation
* protected Checkout Overview route access validation
* protected Checkout Complete route access validation
* input error icon visibility after failed login
* lightweight Sauce Demo smoke availability check

### Inventory Coverage

Implemented Inventory coverage includes:

* Inventory page visibility after successful login
* product list validation
* product card content validation
* Cart page navigation
* representative add-to-cart flow
* Add to cart and Remove button state validation
* cart badge visibility and count validation
* product sorting by name
* product sorting by price
* Product Details navigation through product names
* Product Details navigation through product images
* all-products add-to-cart coverage
* representative remove-from-cart flow
* all-products remove-from-cart coverage
* representative and full product-navigation coverage

### Product Details Coverage

Implemented Product Details coverage includes:

* representative Product Details visibility
* all-products Product Details validation
* return navigation to Inventory
* Add to cart and Remove button state validation
* representative add-to-cart behavior
* all-products add-to-cart coverage
* representative remove-from-cart behavior
* all-products remove-from-cart coverage
* cart badge visibility and count behavior
* Cart navigation from Product Details
* full Product Details → Cart navigation coverage across all products

### Cart Coverage

Implemented Cart coverage includes:

* initial empty-Cart state
* representative Cart item visibility and content
* representative remove-from-Cart behavior
* cart badge removal after removing the last item
* Continue Shopping navigation
* cart state persistence after logout and re-login
* all-products Cart content validation
* cart badge decrement behavior
* representative Product Details navigation from Cart item name
* full Cart → Product Details navigation coverage across all products
* Continue Shopping cart-state preservation
* all-products remove-from-Cart coverage
* Checkout Information page navigation

### Checkout Coverage

Implemented Checkout coverage includes:

* detailed Checkout Information form validation
* representative lightweight Smoke validation of Checkout Information form availability
* required First Name validation
* required Last Name validation
* required Postal Code validation
* checkout input error icon validation
* checkout error message close behavior
* valid customer information transition to Checkout Overview
* Checkout Information cancellation back to Cart
* representative Checkout Overview product validation
* all-products Checkout Overview validation
* representative price summary validation
* multiple-product price summary validation
* Checkout Overview cancellation back to Inventory
* representative Product Details navigation from Checkout Overview
* all-products Product Details navigation from Checkout Overview
* Finish transition to Checkout Complete
* detailed checkout completion content validation
* representative lightweight Smoke validation of Checkout Complete page availability
* Back Home navigation to Inventory

## Marker Strategy

Pytest markers are used to create meaningful, selectively executable test suites.

Markers describe different dimensions of test intent.

They are not mutually exclusive.

A test may therefore legitimately use several markers when it belongs to several suites.

For example:

    @pytest.mark.smoke
    @pytest.mark.navigation
    @pytest.mark.e2e

This means the same test is:

* a representative critical Smoke check
* a Navigation scenario
* a checkpoint in the primary end-to-end purchase journey

Running any matching marker selection should collect that test.

Current executable markers are:

* `smoke`
* `regression`
* `ui`
* `e2e`
* `security`
* `sorting`
* `navigation`

Marker definitions are registered in:

    pytest.ini

The registered marker definitions are the configuration-level source of truth.

Test modules and test case metadata should remain aligned with those definitions.

The project uses:

    --strict-markers

so unknown or unregistered markers should fail collection rather than silently creating accidental test categories.

Runtime configuration, diagnostics, reporting, and parallel execution do not change marker meaning or marker assignment.

### Smoke

`smoke` identifies fast representative validation of critical functionality.

Smoke coverage should answer whether an important feature or flow works at a representative level without attempting to validate every applicable variant.

Typical Smoke patterns include:

* successful login
* representative invalid login handling
* core page availability
* representative add-to-cart or remove-from-cart behavior
* representative page navigation
* representative Cart content validation
* critical checkout flow checkpoints

Where both representative and broader coverage exist, the representative scenario should normally be Smoke while the expanded counterpart should normally be Regression.

A Smoke marker should not automatically imply Regression.

Smoke currently has a dedicated GitHub Actions CI job.

### Regression

`regression` identifies broader validation across expanded or full applicable cases.

Regression coverage is used when a scenario intentionally validates more depth than the representative Smoke equivalent.

Typical Regression patterns include:

* additional credential validation variants
* detailed UI state validation
* validation across every product
* multiple-product behavior
* full navigation coverage across all applicable products
* detailed Cart state transitions
* detailed checkout field validation
* detailed checkout completion content validation

Regression is not a default marker for every test that is not Smoke.

Dedicated categories such as `security`, `sorting`, or `navigation` may stand alone when they already describe the scenario accurately.

Regression currently has a dedicated GitHub Actions CI job.

### UI

`ui` identifies tests whose primary validation includes visibility, presentation, UI state, or direct behavior of user-interface elements.

Typical UI validations include:

* form element visibility
* error message visibility and content
* error icon visibility
* button state changes
* product card content
* cart badge state
* Checkout Overview content
* completion page content

A Playwright test does not automatically require the `ui` marker.

Tests whose primary purpose is navigation, sorting, access control, or another dedicated behavior do not need `ui` unless direct UI state or presentation is also a meaningful part of the validation.

UI remains available for selective execution but does not currently have a dedicated CI job.

### Security

`security` identifies access-control and protected-route tests.

Current Security coverage validates that an unauthenticated user cannot directly access protected application areas.

Current protected routes include:

* Inventory
* Cart
* Product Details
* Checkout Information
* Checkout Overview
* Checkout Complete

These tests are currently owned by Login coverage because authentication state determines access to the protected application areas.

Security is a dedicated marker and does not need to be combined with Regression simply to make the test part of a broader suite.

Security remains available for selective execution but does not currently have a dedicated CI job.

### Sorting

`sorting` identifies product sorting behavior.

Current Sorting coverage validates:

* product name A to Z
* product name Z to A
* product price low to high
* product price high to low

Sorting tests use deterministic product data and plain Python comparisons for extracted product names and numeric product prices.

Sorting is a dedicated marker and does not automatically require `ui` or `regression`.

Sorting remains available for selective execution but does not currently have a dedicated CI job.

### Navigation

`navigation` identifies meaningful page transitions.

Current examples include:

* Inventory → Cart
* Inventory → Product Details
* Product Details → Inventory
* Product Details → Cart
* Cart → Inventory
* Cart → Product Details
* Cart → Checkout Information
* Checkout Information → Cart
* Checkout Information → Checkout Overview
* Checkout Overview → Inventory
* Checkout Overview → Product Details
* Checkout Overview → Checkout Complete
* Checkout Complete → Inventory

The authentication transition from Login to Inventory is intentionally excluded from the Navigation suite.

Navigation may be combined with Smoke or Regression depending on whether the test validates one representative transition or broader applicable coverage.

Navigation may also be combined with UI when meaningful UI state is validated together with the transition.

Navigation remains available for selective execution but does not currently have a dedicated CI job.

### End-to-End

`e2e` identifies tests forming the complete primary purchase journey through checkout completion and return to Inventory.

The E2E suite is intentionally implemented as a collection of independent checkpoint tests rather than one state-sharing monolithic test.

Each checkpoint:

* can run independently
* prepares its own state through scenario fixtures or test-local setup
* validates one important part of the purchase journey
* does not depend on execution order
* does not share browser state with another E2E checkpoint

Running:

    pytest -m e2e -v

collects the current automated checkpoints that together represent the primary purchase journey.

Current automated E2E checkpoints include:

1. successful login to Inventory — `TC-LOGIN-001`
2. representative product add-to-cart flow from Inventory — `TC-INVENTORY-005`
3. representative Cart content validation — `TC-CART-002`
4. Cart → Checkout Information — `TC-CART-012`
5. Checkout Information → Checkout Overview — `TC-CHECKOUT-008`
6. representative selected product validation on Checkout Overview — `TC-CHECKOUT-010`
7. representative price summary validation — `TC-CHECKOUT-012`
8. Finish → Checkout Complete — `TC-CHECKOUT-017`
9. Checkout Complete page availability — `TC-CHECKOUT-019`
10. Back Home → Inventory — `TC-CHECKOUT-020`

The E2E marker therefore describes membership in the logical primary journey, not whether an individual test executes every page of the journey itself.

E2E remains selectively executable but does not currently have a dedicated CI job.

Its tests are still included in complete full-suite CI execution.

## Marker Assignment Principles

Markers should be assigned according to test intent rather than mechanically.

The following principles apply:

* marker dimensions are orthogonal and valid combinations are expected
* Smoke represents fast representative coverage
* Regression represents broader or deeper applicable coverage
* Smoke and Regression should not automatically be applied together
* UI is used when direct UI presentation, visibility, state, or behavior is materially validated
* Security is used for protected-route and access-control coverage
* Sorting is used for product sorting behavior
* Navigation is used for meaningful page transitions
* E2E is used for checkpoints forming the primary purchase journey
* dedicated marker categories may stand alone
* a test should not receive Regression only because it is not Smoke
* markers should remain explicit and readable in test code
* parameter-level marker assignment is acceptable when individual parametrized cases belong to different suites

CI execution responsibility is separate from marker meaning.

The existence or absence of a dedicated CI job does not change the semantic meaning of a marker.

Parallel execution, runtime configuration, diagnostics, and reporting also do not change marker meaning or assignment.

## Marker-Based Suite Execution

Run the complete test suite sequentially:

    pytest -v

Run Smoke sequentially:

    pytest -m smoke -v

Run Regression sequentially:

    pytest -m regression -v

Run UI:

    pytest -m ui -v

Run Security:

    pytest -m security -v

Run Sorting:

    pytest -m sorting -v

Run Navigation:

    pytest -m navigation -v

Run the primary E2E checkpoint suite:

    pytest -m e2e -v

Markers can be combined using normal pytest marker expressions.

Examples:

    pytest -m "smoke and ui" -v
    pytest -m "regression and ui" -v
    pytest -m "smoke and navigation" -v
    pytest -m "regression and navigation" -v

Parallel Smoke:

    pytest -m smoke -n auto -v

Parallel Regression:

    pytest -m regression -n auto -v

Parallel complete suite:

    pytest -n auto -v

Parallel execution changes distribution, not suite membership.

## Parallel Execution Strategy

pytest-xdist provides the implemented worker-level parallel execution model.

The approved parallel execution commands are:

    pytest -m smoke -n auto -v
    pytest -m regression -n auto -v
    pytest -n auto -v

Sequential execution remains supported:

    pytest -m smoke -v
    pytest -m regression -v
    pytest -v

The current suite is designed so that tests:

* do not depend on execution order
* do not depend on browser state created by previous tests
* prepare required application state independently
* do not depend on a specific xdist worker
* keep parametrized cases independent
* keep E2E checkpoints independent
* keep runtime configuration process-oriented rather than test-state-oriented

Phase 4F preserves this execution model.

Moving application scenario fixtures from the root `conftest.py` to `tests/conftest.py` does not change their functional intent or introduce shared state.

## GitHub Actions Concurrency Versus Pytest Parallelism

GitHub Actions job-level concurrency and pytest-xdist worker-level parallelism are separate execution mechanisms.

After `quality` succeeds, GitHub Actions may schedule these jobs independently:

* `smoke`
* `regression`
* `full-suite`

This is **job-level concurrency**.

Inside each of those browser-test jobs, pytest-xdist distributes collected tests between workers.

This is **Pytest worker-level parallelism**.

The execution model can therefore be represented as:

    quality
    ├── smoke
    │   └── xdist workers
    ├── regression
    │   └── xdist workers
    └── full-suite
        └── xdist workers

The `quality` job does not execute browser tests and does not use xdist.

Runtime configuration, diagnostics, and reporting do not introduce additional concurrency layers.

## Runtime Configuration Strategy

Phase 4E provides centralized runtime configuration through:

    config/settings.py

Runtime configuration controls execution settings without requiring changes to functional tests or Page Objects.

The supported configuration surface is:

| Environment Variable   | Default                     | Accepted Values / Behavior                          |
|------------------------|-----------------------------|-----------------------------------------------------|
| `QA_BASE_URL`          | `https://www.saucedemo.com` | valid HTTP/HTTPS application origin                 |
| `QA_BROWSER`           | `chromium`                  | `chromium`, `firefox`, `webkit`                     |
| `QA_HEADED`            | `false`                     | `true`, `false`, `1`, `0`, `yes`, `no`, `on`, `off` |
| `QA_TIMEOUT_MS`        | `30000`                     | non-negative integer milliseconds                   |
| `QA_EXPECT_TIMEOUT_MS` | `5000`                      | non-negative integer milliseconds                   |
| `QA_SCREENSHOT_POLICY` | `only-on-failure`           | `only-on-failure`, `off`                            |
| `QA_TRACE_POLICY`      | `off`                       | `off`, `retain-on-failure`, `on`                    |
| `QA_VIDEO_POLICY`      | `off`                       | `off`, `retain-on-failure`, `on`                    |

### Runtime Configuration Defaults

When no supported environment variables are provided, local execution uses:

    QA_BASE_URL=https://www.saucedemo.com
    QA_BROWSER=chromium
    QA_HEADED=false
    QA_TIMEOUT_MS=30000
    QA_EXPECT_TIMEOUT_MS=5000
    QA_SCREENSHOT_POLICY=only-on-failure
    QA_TRACE_POLICY=off
    QA_VIDEO_POLICY=off

These defaults preserve the approved framework behavior.

### Base URL Strategy

`QA_BASE_URL` defines the application origin.

Page Objects define relative routes and use the configured application origin through `BasePage`.

Example:

    QA_BASE_URL="http://localhost:8000" pytest -m smoke -v

A configured base URL must:

* use `http` or `https`
* contain a valid host
* contain only the application origin rather than an application path
* not contain credentials
* not contain query parameters
* not contain a fragment
* not contain whitespace
* contain a valid port when a port is specified

A trailing slash is normalized away.

This keeps environment-specific application origins outside functional test logic.

### Browser Strategy

`QA_BROWSER` supports:

    chromium
    firefox
    webkit

Browser values are normalized by trimming surrounding whitespace and converting supported values to lowercase.

Example:

    QA_BROWSER=chromium pytest -m smoke -v

The configuration layer recognizes Playwright browser engines.

Recognition does not guarantee that the requested browser is installed in the execution environment.

The current project CI installs Chromium only.

Explicit native pytest-playwright `--browser` options remain usable and take precedence over the project environment-derived browser when supplied explicitly.

Example:

    QA_BROWSER=firefox pytest -m smoke -v --browser chromium

uses the explicit native Chromium option.

### Headed And Headless Strategy

The default is headless:

    QA_HEADED=false

Headed local execution can be requested with:

    QA_HEADED=true pytest -m smoke -v

Accepted true values are:

    true
    1
    yes
    on

Accepted false values are:

    false
    0
    no
    off

Values are normalized case-insensitively.

The native pytest-playwright `--headed` option remains available.

CI explicitly uses `QA_HEADED=false`.

### Timeout Strategy

`QA_TIMEOUT_MS` configures:

* Playwright default action timeout
* Playwright default navigation timeout

Default:

    30000

Example:

    QA_TIMEOUT_MS=45000 pytest -m regression -v

`QA_EXPECT_TIMEOUT_MS` configures the Playwright assertion timeout.

Default:

    5000

Example:

    QA_EXPECT_TIMEOUT_MS=7000 pytest -m smoke -v

Both timeout values must be non-negative integer numbers of milliseconds.

A value of `0` is accepted and follows Playwright timeout semantics.

### Screenshot Policy

The project-level screenshot policy is controlled through:

    QA_SCREENSHOT_POLICY

Supported values:

    only-on-failure
    off

Default:

    only-on-failure

When a browser test fails during the Pytest `call` phase and a Playwright page is available:

* one custom screenshot is captured
* the PNG is written under `reports/screenshots/`
* the same PNG is attached to Allure when Allure result collection is active
* the successfully created screenshot path is added to the Phase 4F failed-test diagnostic summary

The framework does not create a second project-level screenshot mechanism through pytest-playwright.

Setup-phase and teardown-phase failures still receive Phase 4F failure diagnostics but do not trigger the custom project screenshot.

To disable project failure screenshots:

    QA_SCREENSHOT_POLICY=off pytest -m smoke -v

With screenshot policy disabled:

* the custom PNG is not created
* the corresponding Allure screenshot attachment is not created

### Trace Policy

Trace policy is controlled through:

    QA_TRACE_POLICY

Supported values:

    off
    retain-on-failure
    on

Default:

    off

Example:

    QA_TRACE_POLICY=retain-on-failure pytest -m regression -v

Trace generation uses pytest-playwright / Playwright-supported runtime behavior rather than custom project recording logic.

When enabled, generated trace output uses the pytest-playwright runtime artifact structure rooted under:

    test-results/

Explicit native pytest-playwright tracing options remain usable and take precedence when supplied directly.

### Video Policy

Video policy is controlled through:

    QA_VIDEO_POLICY

Supported values:

    off
    retain-on-failure
    on

Default:

    off

Example:

    QA_VIDEO_POLICY=on pytest tests/test_login_page.py -v

Video generation uses pytest-playwright / Playwright-supported runtime behavior rather than custom project recording logic.

Generated video output uses the pytest-playwright runtime artifact structure rooted under:

    test-results/

Explicit native pytest-playwright video options remain usable and take precedence when supplied directly.

### Combined Runtime Overrides

Several runtime values can be supplied for one execution.

Example:

    QA_BASE_URL="https://www.saucedemo.com" \
    QA_BROWSER="chromium" \
    QA_HEADED="false" \
    QA_TIMEOUT_MS="45000" \
    QA_EXPECT_TIMEOUT_MS="7000" \
    QA_SCREENSHOT_POLICY="only-on-failure" \
    QA_TRACE_POLICY="retain-on-failure" \
    QA_VIDEO_POLICY="off" \
    pytest -m smoke -n auto -v

This does not require modification of functional test code.

### Invalid Configuration Strategy

Invalid explicit runtime configuration fails early.

Examples include:

* unsupported browser names
* unsupported artifact policy values
* invalid boolean values
* negative timeout values
* non-integer timeout values
* malformed base URLs

The configuration error identifies the affected environment variable.

The framework should not silently replace an invalid explicit value with a default.

Focused runtime configuration behavior is validated in:

    tests/test_runtime_config.py

### Runtime Configuration Scope Boundaries

Phase 4E does not implement:

* named environment profiles
* automatic `.env` loading
* browser matrices
* cross-browser CI execution
* Firefox or WebKit CI installation
* device emulation
* mobile emulation
* browser channels
* slow motion configuration
* retries

Phase 4F diagnostics and fixture responsibility cleanup are implemented separately and are not part of the remaining runtime configuration scope.

The runtime configuration layer should remain focused on approved execution concerns.

## Runtime Diagnostics Strategy

Phase 4F adds lightweight execution diagnostics without introducing persistent project log files.

Shared diagnostic formatting is implemented in:

    framework/diagnostics.py

Framework-level Pytest integration remains in:

    conftest.py

The diagnostics strategy has three responsibilities:

* describe the effective runtime configuration
* provide concise context for failed Pytest reports
* surface errors encountered while gathering diagnostic evidence

Diagnostics should improve failure investigation without changing the functional behavior of tests.

### Runtime Summary

The runtime summary is emitted through:

    pytest_report_header

The summary includes:

* base URL
* effective browser
* headed/headless mode
* action/navigation timeout
* assertion timeout
* screenshot policy
* trace policy
* video policy

Representative format:

    [runtime] base_url=... | browser=... | mode=... | action_navigation_timeout_ms=... | assertion_timeout_ms=... | screenshot=... | trace=... | video=...

The browser, headed mode, trace policy, and video policy reflect effective Pytest / pytest-playwright configuration.

This is especially relevant when explicit native command-line options override environment-derived defaults.

### Runtime Summary Under pytest-xdist

The runtime header is not emitted independently by each xdist worker.

Worker processes return no additional header from the Phase 4F hook.

This avoids duplicated runtime configuration output during parallel execution.

The controlling Pytest process provides the execution-level summary.

### Failed-Test Diagnostics

Failed-test diagnostics apply to failed Pytest reports from:

    setup
    call
    teardown

Every failed-test summary identifies:

* Pytest node ID
* failure phase

When the Playwright `page` fixture is available, diagnostics additionally attempt to include:

* current page URL

When a custom screenshot has been successfully created, the summary additionally includes:

* screenshot path

Representative format:

    [failure] test=<node-id> | phase=<phase> | url=<current-url> | screenshot=<path>

URL and screenshot fields are optional and are included only when the values are available.

The failed-test diagnostic mechanism therefore does not assume that every failure has an active Playwright page.

### Diagnostic Errors

Diagnostic evidence collection can itself fail.

Current Phase 4F diagnostic-error operations include:

    page-url
    screenshot
    allure-attachment

Representative output:

    [diagnostic-error] operation=<operation> | test=<node-id> | phase=<phase> | error=<error>

Diagnostic errors are:

* emitted through the project diagnostics logger
* added to failed Pytest report sections

The diagnostics logger uses:

    qa_automation.diagnostics

The project does not configure a persistent file handler or persistent diagnostic log files.

### Diagnostic Scope Boundaries

Phase 4F diagnostics do not implement:

* persistent project log files
* browser console capture
* network capture
* custom network tracing beyond Playwright trace support
* HTML or page-source dumps
* automatic trace enablement
* automatic video enablement
* retries
* hosted diagnostic reporting
* diagnostic-specific CI topology

Trace and video remain pytest-playwright-owned runtime capabilities.

The custom failure screenshot remains the project-owned screenshot mechanism.

## Dedicated CI Marker Execution

The GitHub Actions job structure established in Phase 4B and extended with xdist, reporting, runtime configuration, and diagnostics is preserved:

    quality
    ├── smoke
    ├── regression
    └── full-suite

Smoke CI uses:

    pytest -m smoke -n auto -v

Regression CI uses:

    pytest -m regression -n auto -v

The complete full-suite CI execution uses pytest-xdist and additionally collects Allure result data:

    pytest -n auto -v \
      --html=reports/report.html \
      --self-contained-html \
      --alluredir=reports/allure-results \
      --clean-alluredir

Smoke and Regression retain their existing self-contained pytest-html reporting.

Allure reporting is intentionally generated only for the complete `full-suite` CI job.

Phase 4F diagnostics operate through these existing Pytest executions.

Dedicated CI jobs do not currently exist for:

* UI
* Security
* Sorting
* Navigation
* E2E

These marker suites remain selectively executable locally.

Tests assigned to them still participate in the complete unfiltered full-suite CI execution.

## Test Design Principles

Automated tests should follow:

* Arrange / Act / Assert structure
* clear and descriptive test names
* stable assertions
* reusable Page Objects
* shared authenticated-page behavior where appropriate
* reusable assertion helpers where validation is shared across page areas
* externalized test data where useful
* no hardcoded waits
* independent test execution
* compatibility with supported sequential and parallel execution
* environment-specific execution behavior kept outside functional tests
* diagnostic behavior kept outside functional test logic
* readable failure output
* useful reporting and failure evidence
* explicit marker intent
* clear mapping to manual test cases where practical

Tests should focus on behavior, while page-specific UI interactions should be handled by Page Object classes.

Runtime configuration should configure execution rather than change the functional intent of a test.

Diagnostics should describe execution and failure context rather than become functional test assertions.

## Page Object Model Strategy

Page Object Model is used to separate test logic from page interaction logic.

Current implementation:

    pages/base_page.py
    pages/app_page.py
    pages/login_page.py
    pages/inventory_page.py
    pages/product_details_page.py
    pages/cart_page.py
    pages/checkout_page.py

The `BasePage` object is responsible for:

* storing the Playwright `Page` instance
* storing application-relative page route metadata through `ROUTE`
* composing page URLs using `settings.base_url`
* opening page URLs through a shared `open()` method

The application origin should not be hardcoded independently in functional Page Objects.

The `AppPage` object is responsible for shared authenticated-page behavior, including:

* Cart access
* cart badge access
* application menu access
* logout
* reset app state
* All Items navigation
* About navigation
* shared authenticated product-item helpers where reused

The `LoginPage` object is responsible for Login form interaction and Login-specific UI state.

The `InventoryPage` object is responsible for Inventory content, sorting, Inventory-side Cart actions, and Inventory-owned navigation.

The `ProductDetailsPage` object is responsible for Product Details content, Product Details-side Cart actions, return navigation, and authenticated shared navigation inherited through the application page layer.

The `CartPage` object is responsible for Cart contents, Cart item interaction, product removal, Continue Shopping, Product Details navigation, and checkout entry.

The checkout Page Objects are split by checkout stage:

* `CheckoutInformationPage`
* `CheckoutOverviewPage`
* `CheckoutCompletePage`

They own checkout form interaction, checkout summary behavior, checkout completion behavior, and checkout-stage navigation.

Page Objects should be introduced or expanded when they reduce duplication and improve readability.

Page Objects should not independently parse environment variables, own browser runtime policies, collect framework diagnostics, or own failure reporting.

## Reusable Assertion Strategy

Reusable assertions are used when the same product-related or checkout-related validation appears across multiple page areas.

Current reusable assertion helper location:

    framework/assertions/product_assertions.py

Current reusable product and checkout assertions support:

* Inventory product card validation
* Product Details validation
* Cart item validation
* Checkout Overview item validation
* Checkout Overview price summary validation
* Inventory product state validation after checkout-related navigation
* price string conversion for numeric sorting and checkout summary assertions

Reusable assertion helpers should remain focused on shared validation logic.

They should not contain:

* navigation logic
* test setup logic
* fixture responsibilities
* Page Object responsibilities
* runtime configuration parsing
* diagnostic hook logic
* reporting configuration

## Fixture Strategy

Fixtures are used to prepare reusable and isolated test setup.

Phase 4F establishes an explicit boundary between framework-level Pytest responsibilities and application scenario fixtures.

Framework-level Pytest integration remains in:

    conftest.py

Application scenario fixtures are defined in:

    tests/conftest.py

Current application fixtures include:

    opened_login_page
    standard_user
    logged_in_inventory_page
    inventory_page_with_one_product_in_cart
    cart_page_with_one_product
    checkout_step_one_page_with_one_product
    checkout_step_two_page_with_one_product
    checkout_last_step_page_with_one_product

The fixtures progressively prepare common application states while allowing each test to remain independently executable.

Examples:

* `opened_login_page` prepares the Login page
* `standard_user` provides the standard valid user data
* `logged_in_inventory_page` authenticates the standard user
* `inventory_page_with_one_product_in_cart` prepares Inventory with one deterministic product in the Cart
* `cart_page_with_one_product` prepares the Cart with one product
* `checkout_step_one_page_with_one_product` prepares Checkout Information
* `checkout_step_two_page_with_one_product` prepares Checkout Overview
* `checkout_last_step_page_with_one_product` prepares Checkout Complete

This fixture structure is especially important for both the E2E checkpoint strategy and parallel execution because tests must not rely on state created by another test.

The browser lifecycle continues to use the pytest-playwright fixture model.

The project-level browser context fixture remains in the root `conftest.py`.

It is built on pytest-playwright's `new_context` fixture and applies configured action and navigation timeout values.

The Playwright `page` fixture used by functional tests therefore receives configured context behavior without functional tests needing to know how runtime configuration is applied.

Application fixtures remain explicit and scenario-oriented.

Phase 4F does not introduce:

* a generic fixture factory
* dependency-injection infrastructure
* autouse redesign
* a multi-layer fixture package
* fixture scope redesign

The current fixture chains remain compatible with pytest-xdist worker-level parallel execution.

Fixtures should be added when setup logic becomes meaningfully repeated.

Avoid unnecessary fixture growth when a scenario is clearer with direct setup.

## Test Data Strategy

Test data should be separated from test logic when it improves readability, maintainability, or parametrization.

Current test data location:

    test_data/login_test_data.py
    test_data/product_test_data.py
    test_data/checkout_test_data.py

Current Login test data includes:

* valid user cases
* invalid credential cases
* empty credential cases
* locked out user cases
* expected error messages
* protected route URL suffixes

Current product test data includes:

* product IDs
* product names
* product descriptions
* product prices
* product image paths

Current checkout test data includes:

* valid checkout customer information
* checkout required-field error messages
* checkout page title expectations
* Checkout Overview summary label expectations
* Checkout Complete header and message expectations

Inventory, Product Details, Cart, and Checkout tests reuse centralized user and product data.

A separate Cart test data module is not needed at the current stage because Cart tests reuse existing product and user data without introducing unique Cart-only datasets.

Test data should support:

* clear test intent
* reduced hardcoding
* parametrized execution
* traceability to manual test case IDs

Runtime configuration is not test data.

It belongs to:

    config/settings.py

Diagnostics are also not test data.

Shared diagnostic formatting belongs to:

    framework/diagnostics.py

## Parametrization Strategy

Parametrization is used for repeated scenarios with the same test flow and different input data.

Current parametrized areas include:

* valid login cases
* invalid credential cases
* empty credential cases
* locked out user cases
* protected route access
* Inventory product validation
* Inventory → Product Details navigation
* Product Details validation across all products
* add-to-cart and remove-from-cart coverage across product data
* Cart item validation across product data
* Checkout Overview item validation
* Checkout Overview → Product Details navigation
* selected single-case tests where test case ID visibility in `pytest -v` is useful
* focused runtime configuration input validation

Parametrized test IDs should use manual test case IDs where practical for functional product coverage.

Examples:

    TC-LOGIN-002
    TC-INVENTORY-013-0
    TC-PRODUCT-DETAILS-002-0
    TC-CART-011-0
    TC-CHECKOUT-011-0
    TC-CHECKOUT-016-0

The exact suffix depends on centralized product IDs used by the test data.

Meaningful parametrized IDs improve traceability between:

* manual test cases
* automated tests
* terminal output
* CI logs
* reports
* Phase 4F failed-test node IDs

Individual `pytest.param()` cases may receive different markers when one representative dataset belongs to Smoke and remaining datasets belong to Regression.

Parametrized cases must remain independent because xdist may execute separate cases on different workers and in an order different from sequential execution.

Runtime configuration parametrization does not use manual product test case IDs because it validates framework configuration rather than product scenarios.

## Assertion Strategy

Assertions should be stable, meaningful, and focused on user-observable behavior where possible.

Current assertion patterns include:

* page URL matches expected destination
* element is visible
* element is hidden
* error message matches expected text
* password input uses the expected field type
* protected routes redirect unauthenticated users to Login
* Inventory product content matches centralized product data
* Product Details content matches centralized product data
* sorted product names match expected order
* converted product prices match expected order
* cart badge state matches expected Cart state
* Cart item content matches selected product data
* Add to cart and Remove button states match Cart state
* Cart state persists where explicitly expected
* checkout field validation matches expected errors
* Checkout Overview product content matches expected data
* Checkout Overview price calculations match selected products
* checkout completion content matches expected values
* runtime configuration values normalize to expected settings
* invalid explicit runtime values raise clear configuration errors

Use Playwright assertions for browser and UI state when possible because they include built-in waiting behavior.

Use plain Python assertions when comparing extracted or calculated values such as:

* product names
* product prices
* sorted lists
* calculated checkout totals
* configuration values

Use reusable assertion helpers when the same meaningful validation is shared across multiple tests or page areas.

Diagnostic output should not replace functional assertions.

## Automation Priority

Automation should focus on:

* repeatable scenarios
* critical user flows
* regression-prone functionality
* stable application behavior
* high-value validation
* scenarios that benefit from repeated local or CI execution
* scenarios with clear expected results and stable selectors
* framework behavior whose failure would affect broad execution reliability

Not every possible scenario needs dedicated automation.

Some scenarios may remain manual, exploratory, or planned when automation would currently add limited value or when the scenario belongs to later approved scope.

## Scope Boundaries

The project uses explicit scope boundaries to keep workstreams focused and maintainable.

Current page-level automation boundaries include:

* Login behavior belongs to Login coverage.
* Authentication-based protected-route validation belongs to Login coverage.
* Inventory behavior belongs to Inventory coverage.
* Product Details behavior belongs to Product Details coverage.
* Cart behavior belongs to Cart coverage.
* Cart → Checkout Information entry belongs to Cart coverage.
* Checkout Information, Checkout Overview, and Checkout Complete behavior belong to Checkout coverage.

Current functional coverage exclusions include:

* browser restart persistence
* storage clearing behavior
* cross-user Cart persistence
* multi-user Cart behavior
* unapproved edge-case expansion

Cart coverage should not own detailed Checkout Information, Checkout Overview, or Checkout Complete validation.

Runtime configuration is a framework execution concern and should not create duplicate functional page-level test ownership.

Runtime and failed-test diagnostics are framework execution concerns and should not create duplicate functional test ownership.

Fixture organization should preserve scenario readability and independent state preparation rather than introduce abstraction solely for architectural complexity.

## Reporting And Debugging

The reporting and diagnostic strategy uses complementary mechanisms rather than one report format replacing another.

Current reporting and debugging capabilities include:

* Pytest console output
* Phase 4F effective runtime summary
* Phase 4F failed-test summaries
* Phase 4F diagnostic-error output
* pytest-html
* Allure result collection
* generated Allure HTML reports
* configurable screenshots on browser-test call-phase failure
* Allure failure screenshot attachments
* optional Playwright traces
* optional Playwright videos
* GitHub Actions artifacts

### pytest-html

`pytest-html` remains the lightweight HTML reporting mechanism.

It is used by the existing CI browser jobs and can also be used during local execution.

Current CI report paths are:

    reports/smoke-report.html
    reports/regression-report.html
    reports/report.html

Smoke and Regression remain pytest-html-focused CI jobs.

Phase 4D does not add duplicate Allure report generation to those dedicated marker jobs.

Phase 4F diagnostics operate through the same Pytest reports without replacing pytest-html.

### Allure

Allure provides the advanced reporting layer for complete-suite reporting.

The Python integration is provided by `allure-pytest`.

Local Allure result collection can be performed sequentially:

    pytest -v \
      --alluredir=reports/allure-results \
      --clean-alluredir

or through pytest-xdist:

    pytest -n auto -v \
      --alluredir=reports/allure-results \
      --clean-alluredir

The result data is written to:

    reports/allure-results/

The standalone Allure CLI is required to convert this result data into an HTML report.

Verify local CLI availability with:

    allure --version

Generate the local HTML report with:

    allure generate reports/allure-results \
      --clean \
      -o reports/allure-report

The generated report is written to:

    reports/allure-report/

The Allure CLI is a report-generation prerequisite and is separate from the Python `allure-pytest` dependency.

### Failure Screenshots

Browser-test failures during the Pytest `call` phase use the custom screenshot mechanism in the root `conftest.py`.

The default screenshot policy is:

    QA_SCREENSHOT_POLICY=only-on-failure

Failure screenshots are written to:

    reports/screenshots/

Screenshot filenames include the test name and UTC timestamp.

After a screenshot is captured successfully:

* the same PNG file is attached to the Allure result as `Failure screenshot` when Allure result collection is active
* the screenshot path is included in the Phase 4F failed-test diagnostic summary

This does not introduce a second screenshot capture mechanism.

The same failure evidence is reused for runtime screenshot output, failed-test context, and the Allure attachment.

If screenshot capture itself fails:

* no screenshot path is added to the failed-test summary
* no Allure screenshot attachment is attempted
* the screenshot failure is reported through the Phase 4F diagnostic-error mechanism

If Allure attachment fails after a screenshot was successfully created:

* the original screenshot remains available
* its path remains in the failed-test summary
* the attachment failure is reported through the diagnostic-error mechanism

When:

    QA_SCREENSHOT_POLICY=off

the custom failure screenshot is not written and the corresponding Allure attachment is not created.

Setup-phase and teardown-phase failures still receive failed-test diagnostics but do not trigger custom project screenshot capture.

### Trace And Video Diagnostics

Trace and video use pytest-playwright / Playwright-supported runtime mechanisms.

Trace policy:

    QA_TRACE_POLICY

Video policy:

    QA_VIDEO_POLICY

Both support:

    off
    retain-on-failure
    on

and both default to:

    off

When enabled, pytest-playwright-generated files use its runtime artifact structure rooted under:

    test-results/

Representative output includes:

    trace.zip
    video.webm

The project does not implement duplicate custom trace or video recording systems.

Phase 4F does not change trace or video lifecycle ownership.

### Reporting And Diagnostic Compatibility

Current reporting and diagnostic behavior supports both:

* sequential Pytest execution
* pytest-xdist worker-level parallel execution

No sequential-only reporting or diagnostic exception is required.

The existing failure screenshot mechanism and Allure attachment behavior remain compatible with the current parallel execution model.

The runtime header avoids xdist-worker duplication.

Failed-test diagnostic summaries remain tied to their relevant Pytest reports.

Trace and video are runtime policies and do not require alternate functional test implementations.

### Generated Runtime Outputs

Generated reports, screenshots, traces, videos, and Allure outputs are runtime data.

Current generated locations include:

    reports/
    reports/screenshots/
    reports/allure-results/
    reports/allure-report/
    test-results/

These outputs are used for:

* local debugging
* failure analysis
* execution evidence
* CI artifact publishing where configured

They are not repository source content and should not be committed to Git.

The repository ignore policy excludes these generated runtime areas from version control.

Phase 4F runtime and failure summaries do not add another persistent output directory.

Persistent project diagnostic log files are not implemented.

### CI Reporting

GitHub Actions preserves the existing pytest-html reporting strategy while adding advanced Allure reporting to the complete `full-suite` job.

Smoke CI generates:

    reports/smoke-report.html

Regression CI generates:

    reports/regression-report.html

The `full-suite` job generates:

    reports/report.html
    reports/allure-results/
    reports/allure-report/

The full-suite Pytest command is:

    pytest -n auto -v \
      --html=reports/report.html \
      --self-contained-html \
      --alluredir=reports/allure-results \
      --clean-alluredir

After test execution, CI generates the Allure HTML report when usable result data exists:

    allure generate reports/allure-results \
      --clean \
      -o reports/allure-report

Report generation is configured so it can still be attempted after failed test execution when usable Allure result data was produced.

The dedicated GitHub Actions artifact for the generated Allure report is:

    full-suite-allure-report

and its source path is:

    reports/allure-report/

The existing full-suite pytest-html artifact remains:

    pytest-html-report

and the broader runtime-output artifact remains:

    test-artifacts

Smoke and Regression retain their existing pytest-html and runtime artifact behavior.

Detailed CI artifact behavior is documented in:

    docs/ci-cd-pipeline.md

Trace and video are disabled in CI by default and are therefore not introduced as default retained CI artifacts.

Phase 4F does not add a dedicated persistent diagnostic artifact.

Allure history persistence, report hosting, GitHub Pages publishing, retries, and cross-browser reporting are not part of the current implemented scope.

## Local Validation Strategy

Recommended standard sequential local validation:

    ruff check .
    black --check .
    isort . --check-only
    pytest -v

Parallel execution is additionally available for execution validation:

    pytest -n auto -v

The approved parallel marker-suite validation commands are:

    pytest -m smoke -n auto -v
    pytest -m regression -n auto -v

Sequential execution remains supported and may be used for normal development, focused debugging, or when parallel execution is not required.

For reporting validation, Allure result collection can be added to either sequential or parallel execution.

Example parallel full-suite reporting validation:

    pytest -n auto -v \
      --html=reports/report.html \
      --self-contained-html \
      --alluredir=reports/allure-results \
      --clean-alluredir

Generate the corresponding Allure HTML report with:

    allure generate reports/allure-results \
      --clean \
      -o reports/allure-report

### Runtime Configuration Validation

Focused runtime configuration validation uses:

    pytest tests/test_runtime_config.py

Representative environment overrides may be validated through normal suite execution.

Example:

    QA_BROWSER=chromium \
    QA_HEADED=false \
    QA_TIMEOUT_MS=20000 \
    QA_EXPECT_TIMEOUT_MS=4000 \
    pytest -m smoke -v

Runtime artifact policies may be validated with representative controlled executions where required.

Intentionally failing validation scenarios should remain temporary and should not be committed as permanent failing tests.

Generated runtime artifacts should be cleaned before final Git status validation.

### Diagnostic Validation

Changes affecting Phase 4F diagnostics should use controlled failures to validate the applicable behavior.

Validation may include:

* runtime summary visibility
* correct effective runtime values
* no duplicate xdist worker runtime headers
* Pytest node ID in failure diagnostics
* correct `setup`, `call`, or `teardown` phase
* current page URL when a Playwright page is available
* screenshot path after successful custom screenshot capture
* diagnostic-error output when diagnostic evidence collection fails

A failed `call` phase should be used when validating the custom screenshot path because project screenshot capture is intentionally call-phase-only.

Temporary intentionally failing tests used only for diagnostics validation should not be committed.

### Login Changes

    pytest -v tests/test_login_page.py
    pytest -m security -v
    pytest -m "smoke and ui" -v
    pytest -m "regression and ui" -v

### Inventory Changes

    pytest -v tests/test_inventory_page.py
    pytest -m sorting -v
    pytest tests/test_inventory_page.py -m navigation -v

### Product Details Changes

    pytest -v tests/test_product_details_page.py
    pytest tests/test_product_details_page.py -m navigation -v
    pytest tests/test_product_details_page.py -m regression -v

### Cart Changes

    pytest -v tests/test_cart_page.py
    pytest tests/test_cart_page.py -m navigation -v
    pytest tests/test_cart_page.py -m regression -v

### Checkout Changes

    pytest -v tests/test_checkout_page.py
    pytest tests/test_checkout_page.py -m navigation -v
    pytest tests/test_checkout_page.py -m regression -v

### Primary Purchase Journey Changes

When changes affect checkpoints in the main purchase journey, run:

    pytest -m e2e -v

This validates the complete logical checkpoint suite across the covered page areas.

For checkpoint, stabilization, or portfolio-promotion tasks, run relevant scoped modules and full validation when possible:

    pytest -v tests/test_login_page.py
    pytest -v tests/test_inventory_page.py
    pytest -v tests/test_product_details_page.py
    pytest -v tests/test_cart_page.py
    pytest -v tests/test_checkout_page.py
    pytest -v

When parallel safety, fixture responsibility, diagnostics, or execution behavior is part of the validation scope, additionally run:

    pytest -m smoke -n auto -v
    pytest -m regression -n auto -v
    pytest -n auto -v

The full test suite should pass before a workstream is considered ready for merge unless a scoped validation exception is explicitly accepted.

## Phase 4F Validation Status

Final Phase 4F validation confirmed:

    Smoke: 31 passed
    Regression: 109 passed
    Full sequential: 236 passed
    Full pytest-xdist: 236 passed
    Ruff: passed
    Black check: passed
    isort: passed

Controlled failure validation after fixture responsibility separation also confirmed:

* effective runtime header
* Pytest node ID
* failure phase
* current page URL
* screenshot diagnostic path

These validation results confirm that diagnostics and fixture responsibility cleanup preserve the existing test execution model.

## CI Validation Strategy

GitHub Actions validates the project automatically according to the configured workflow triggers.

Current triggers include:

* push to `main`
* push to `develop`
* Pull Requests targeting `main`
* Pull Requests targeting `develop`
* manual execution through `workflow_dispatch`

Regular pushes to feature, refactor, fix, or documentation branches do not automatically trigger CI unless:

* the branch is part of a Pull Request targeting `main` or `develop`
* the workflow is started manually

### Current Job Structure

The current CI pipeline retains the job structure introduced in Phase 4B:

    quality
    ├── smoke
    ├── regression
    └── full-suite

The `quality` job executes first.

Smoke, Regression, and full-suite all declare:

    needs: quality

After successful quality validation, those three browser jobs are independently executable and do not depend on each other.

Phase 4C integrates pytest-xdist worker-level parallel execution into the three existing browser-test jobs.

Phase 4D adds advanced Allure reporting to the existing `full-suite` job without adding another browser job.

Phase 4E adds explicit runtime configuration defaults to the three existing browser-test jobs without changing the job topology.

Phase 4F adds runtime and failed-test diagnostics through the existing Pytest execution path without adding another job or changing the topology.

### Quality Validation

The `quality` job validates:

    ruff check .
    black --check .
    isort . --check-only

It also performs:

* repository checkout
* Python 3.12 setup
* dependency installation

The quality job does not install Playwright Chromium.

It does not use pytest-xdist.

It does not require browser runtime configuration.

A quality failure prevents all browser-test jobs from executing.

### CI Runtime Defaults

Smoke, Regression, and full-suite use:

    QA_BASE_URL=https://www.saucedemo.com
    QA_BROWSER=chromium
    QA_HEADED=false
    QA_TIMEOUT_MS=30000
    QA_EXPECT_TIMEOUT_MS=5000
    QA_SCREENSHOT_POLICY=only-on-failure
    QA_TRACE_POLICY=off
    QA_VIDEO_POLICY=off

These values intentionally match the approved local defaults.

The CI runtime strategy therefore remains:

* Chromium-only
* headless
* parallel through pytest-xdist
* failure screenshot capture enabled
* tracing disabled by default
* video disabled by default
* Phase 4F runtime diagnostics active through normal Pytest execution

The runtime configuration integration does not create:

* browser matrices
* Firefox installation
* WebKit installation
* retries
* `continue-on-error`
* default trace retention
* default video retention
* diagnostic-specific runtime configuration

### Smoke CI Validation

The dedicated Smoke job executes:

    pytest -m smoke -n auto -v

The actual CI command additionally generates a self-contained pytest HTML report.

Smoke failure fails the Smoke job.

Smoke does not generate an Allure report.

### Regression CI Validation

The dedicated Regression job executes:

    pytest -m regression -n auto -v

The actual CI command additionally generates a self-contained pytest HTML report.

Regression failure fails the Regression job.

Regression does not generate an Allure report.

### Full-Suite CI Validation

The full-suite job executes the complete unfiltered automated test suite through pytest-xdist and collects both pytest-html and Allure result data:

    pytest -n auto -v \
      --html=reports/report.html \
      --self-contained-html \
      --alluredir=reports/allure-results \
      --clean-alluredir

It is intentionally not filtered by markers.

After test execution, the workflow attempts to generate:

    reports/allure-report/

from:

    reports/allure-results/

when usable Allure result data exists.

The full-suite job remains the complete automated regression gate and the primary CI source for the advanced Allure report.

Smoke and Regression provide targeted CI feedback but do not replace full-suite execution.

### Marker Suites Without Dedicated CI Jobs

Dedicated CI jobs do not currently exist for:

* UI
* Security
* Sorting
* Navigation
* E2E

These suites remain available for selective local execution.

Tests assigned to those markers still participate in complete full-suite CI validation.

### CI Failure Behavior

Failing required quality or test execution should fail CI.

The current workflow does not use `continue-on-error: true` for required validation.

Browser-job artifact upload steps use:

    if: always()

so available reports and runtime outputs can still be published after a browser-test failure.

The Allure generation step in the full-suite job also uses failure-tolerant workflow control so report generation can be attempted after failed test execution when usable result data exists.

Diagnostics do not convert failed execution into successful validation.

A failed `quality` job prevents browser-test jobs from starting, so no browser-test artifacts are produced in that case.

### Current Browser Scope

The runtime configuration layer recognizes:

    chromium
    firefox
    webkit

Current GitHub Actions browser execution remains Chromium-only.

The CI browser-test jobs install:

    playwright install --with-deps chromium

The current runtime, parallel, reporting, and diagnostic strategies do not introduce:

* Firefox CI execution
* WebKit CI execution
* cross-browser matrices
* cross-browser parallel execution

Cross-browser CI remains outside the current implemented scope.

## Phase 4C Execution Boundaries

Phase 4C extends the existing Phase 4B execution model without changing its job architecture.

Implemented Phase 4C behavior includes:

* validated local pytest-xdist execution
* parallel Smoke execution
* parallel Regression execution
* parallel complete full-suite execution
* sequential execution remaining supported
* validation of fixture and test independence under worker-level execution
* validation of parametrized and E2E checkpoint independence
* xdist integration into existing Smoke, Regression, and full-suite CI jobs
* preservation of the `quality` prerequisite
* preservation of existing pytest-html reporting
* preservation of existing GitHub Actions artifact behavior
* Chromium-only browser scope
* explicit distinction between GitHub Actions job concurrency and pytest-xdist worker concurrency

No sequential-only test exceptions are required.

`pytest-xdist` is an implemented execution capability and should not be described as a future-only dependency.

## Phase 4D Reporting Boundaries

Phase 4D extends the existing execution model with complementary reporting capabilities.

Implemented Phase 4D behavior includes:

* `allure-pytest` integration
* local Allure result collection
* local Allure HTML report generation
* Allure CLI as the local HTML-generation prerequisite
* `reports/allure-results/` as the Allure result location
* `reports/allure-report/` as the generated Allure HTML location
* reuse of existing failure screenshots as Allure attachments
* preservation of the existing screenshot capture mechanism
* support for sequential reporting execution
* support for pytest-xdist parallel reporting execution
* full-suite Allure result collection in GitHub Actions
* full-suite Allure HTML report generation in GitHub Actions
* dedicated `full-suite-allure-report` artifact
* preservation of existing pytest-html reports
* Smoke and Regression remaining pytest-html-focused
* generated reporting output remaining outside version-controlled repository content

Phase 4D does not implement:

* Allure history or trend persistence
* hosted Allure reports
* GitHub Pages reporting
* retries
* additional browser jobs
* cross-browser reporting
* CI matrices

Allure complements pytest-html and the existing screenshot evidence rather than replacing them.

Trace and video policies are implemented separately through Phase 4E runtime configuration and remain disabled by default.

## Phase 4E Runtime Configuration Boundaries

Phase 4E extends the existing framework with centralized runtime execution configuration.

Implemented Phase 4E behavior includes:

* centralized configuration in `config/settings.py`
* `QA_BASE_URL`
* `QA_BROWSER`
* `QA_HEADED`
* `QA_TIMEOUT_MS`
* `QA_EXPECT_TIMEOUT_MS`
* `QA_SCREENSHOT_POLICY`
* `QA_TRACE_POLICY`
* `QA_VIDEO_POLICY`
* approved default values
* string normalization where applicable
* predictable boolean parsing
* non-negative integer timeout validation
* base URL validation and normalization
* fail-fast handling for invalid explicit values
* application URL composition through `BasePage`
* browser/runtime integration through root `conftest.py`
* use of the existing pytest-playwright fixture model
* action and navigation timeout integration
* assertion timeout integration
* preservation of existing failure screenshot and Allure attachment behavior
* screenshot disable policy
* trace integration through pytest-playwright
* video integration through pytest-playwright
* preservation of explicit native pytest-playwright runtime options where applicable
* explicit runtime defaults in Smoke, Regression, and full-suite CI jobs
* preservation of Chromium-only CI
* preservation of existing Phase 4B–4D CI topology, parallelization, reporting, and artifact behavior

Phase 4E does not implement:

* named environment profiles
* `.env` loading
* browser matrices
* cross-browser CI
* Firefox or WebKit CI installation
* device emulation
* mobile emulation
* browser channels
* slow motion configuration
* retries

Phase 4E is implemented and remains the current runtime configuration foundation.

## Phase 4F Diagnostics And Fixture Cleanup Boundaries

Phase 4F extends the existing framework without changing functional test coverage, marker semantics, fixture scopes, browser lifecycle ownership, or CI topology.

Implemented Phase 4F behavior includes:

* `framework/diagnostics.py`
* runtime summary formatting
* failed-test summary formatting
* diagnostic error formatting
* lightweight project diagnostics logger
* effective runtime summary through `pytest_report_header`
* runtime base URL visibility
* effective browser visibility
* headed/headless mode visibility
* action/navigation timeout visibility
* assertion timeout visibility
* screenshot policy visibility
* trace policy visibility
* video policy visibility
* suppression of duplicate runtime headers on pytest-xdist workers
* failed-test Pytest node ID reporting
* `setup`, `call`, and `teardown` failure-phase reporting
* current page URL reporting when a Playwright page is available
* screenshot path reporting after successful custom screenshot capture
* diagnostic error reporting for page URL retrieval
* diagnostic error reporting for screenshot creation
* diagnostic error reporting for Allure attachment
* framework-level responsibilities retained in root `conftest.py`
* application scenario fixtures owned by `tests/conftest.py`
* preserved explicit scenario fixture names
* preserved function-scoped fixture behavior
* preserved pytest-playwright browser lifecycle
* preserved custom screenshot behavior
* preserved pytest-playwright trace ownership
* preserved pytest-playwright video ownership
* preserved reporting architecture
* preserved CI topology
* sequential execution compatibility
* pytest-xdist execution compatibility

Phase 4F does not implement:

* persistent project log files
* browser console capture
* network capture
* custom network tracing
* HTML or page-source dumps
* automatic trace enablement
* automatic video enablement
* retries
* new CI jobs
* generic fixture factories
* dependency-injection infrastructure
* autouse fixture redesign
* multi-layer fixture packages
* fixture scope redesign

## Portfolio Promotion Validation

Before promoting `develop` to `main`, validate that:

* the full test suite passes locally when possible
* CI on the promotion Pull Request passes
* implemented test coverage is accurately described
* planned coverage is not described as already automated
* test case documentation remains aligned with automated test modules
* marker definitions remain aligned with test usage
* sequential and parallel execution documentation remains aligned with actual behavior
* runtime configuration documentation remains aligned with `config/settings.py`, root `conftest.py`, Page Objects, and CI
* diagnostic documentation remains aligned with `framework/diagnostics.py` and root `conftest.py`
* fixture documentation reflects the root `conftest.py` / `tests/conftest.py` responsibility boundary
* local runtime defaults remain aligned with documented defaults
* CI runtime defaults remain aligned with the approved Phase 4E strategy
* reporting documentation remains aligned with actual pytest-html, Allure, screenshot, trace, video, and artifact behavior
* CI documentation remains aligned with actual workflow behavior
* generated reports, screenshots, traces, videos, Allure outputs, cache files, and virtual environment files are not tracked
* the promoted state is suitable as a stable portfolio snapshot

After promotion, `main` should represent the polished portfolio version of the project.

Future implementation work should continue from `develop`.

## Future Improvements

Possible future improvements include:

* broader framework maturity work where justified
* API testing layer
* multi-browser execution when explicitly approved
* additional suite-specific CI jobs where justified
* advanced reporting extensions only when explicitly approved
* environment profiles only if approved by future scope
* persistent structured logging if future requirements justify it
* additional diagnostic evidence such as browser console capture only if explicitly approved

The following are already implemented and should not be treated as future scope:

* dedicated Smoke CI
* dedicated Regression CI
* pytest-xdist parallel execution
* pytest-html reporting
* current Allure reporting
* centralized Phase 4E environment-based runtime configuration
* configurable screenshot, trace, and video policies
* Phase 4F runtime diagnostics
* Phase 4F failed-test diagnostics
* diagnostic error reporting
* separation of framework-level Pytest responsibilities from application scenario fixtures

Allure history persistence, hosted reports, GitHub Pages reporting, `.env` loading, browser matrices, cross-browser CI, retries, device emulation, persistent project log files, browser console capture, network capture, and other advanced capabilities remain future possibilities rather than current implemented behavior.

Future capabilities should not be described as implemented until their corresponding project tasks are completed and validated.