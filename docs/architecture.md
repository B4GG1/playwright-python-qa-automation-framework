# Architecture

This document describes the current architecture of the QA automation framework.

The project follows a lightweight, modular architecture focused on readability, maintainability, traceability, deterministic execution, and incremental framework growth.

The current architecture includes Page Object Model, shared authenticated-page behavior, reusable assertions, reusable pytest fixtures, centralized test data, explicit marker-based test organization, staged CI execution, reporting, screenshot capture, and technical documentation.

## Current Architecture Scope

The current framework includes:

* Pytest-based test execution
* Playwright browser automation
* Page Object Model for Login, Inventory, Product Details, Cart, and Checkout
* shared `BasePage` abstraction
* shared authenticated-page behavior through `AppPage`
* reusable product and checkout assertion helpers
* reusable pytest fixtures
* centralized login, product, and checkout test data
* explicit pytest marker categorization
* strict pytest marker validation
* marker-based selective local execution
* dedicated Smoke CI execution
* dedicated Regression CI execution
* complete unfiltered full-suite CI execution
* parametrized execution with manual test case IDs where practical
* independent E2E purchase-journey checkpoints
* CI execution with GitHub Actions
* separate CI code-quality validation
* code quality tooling
* HTML reporting
* job-specific CI artifacts
* screenshot capture on test failure
* manual test case documentation mapped to automation
* one automated test module per covered page area
* one manual test case file per covered page area

Current automated coverage includes:

* Sauce Demo availability validation
* successful authentication
* invalid credential validation
* empty credential validation
* locked out user validation
* Login UI behavior
* authentication error handling
* protected route access
* Inventory validation
* product list and product card validation
* Inventory → Product Details navigation
* Product Details validation
* product sorting
* Cart navigation
* empty Cart validation
* Add to cart behavior
* Remove behavior
* cart badge behavior
* Cart item visibility and content
* Continue Shopping
* Cart state persistence
* Cart → Checkout Information navigation
* Checkout Information validation
* Checkout required-field validation
* Checkout error-state validation
* Checkout Overview validation
* Checkout Overview price summary validation
* Product Details navigation from Checkout Overview
* Checkout completion
* Checkout Complete validation
* Back Home navigation
* independent E2E purchase-journey checkpoints

Cart coverage owns the user action that starts on the Cart page and opens Checkout Information.

Detailed Checkout Information, Checkout Overview, and Checkout Complete behavior remains owned by Checkout tests.

## Project Layers

The framework is organized into the following layers:

```text
test_cases/
    ↓
test_data/
    ↓
tests/
    ↓
pages/
    ↓
framework/
    ↓
Playwright / Pytest
    ↓
local validation / CI
```

The layers are intentionally lightweight.

New abstractions should be introduced only when repeated behavior or clear responsibility boundaries justify them.

## `tests/`

Contains automated test suites.

Current test modules:

```text
tests/test_login_page.py
tests/test_inventory_page.py
tests/test_product_details_page.py
tests/test_cart_page.py
tests/test_checkout_page.py
```

Current responsibilities:

* describe expected application behavior
* execute test scenarios
* use Page Objects for interactions
* use Playwright assertions for browser and UI state
* use plain Python assertions for already extracted or calculated values
* use reusable assertion helpers when validation logic is shared
* use centralized test data
* use fixtures for reusable setup
* use explicit pytest markers
* preserve traceability to manual test cases where practical

Test modules should not duplicate selectors when Page Objects already expose the required interaction or state.

## `pages/`

Contains Page Object Model classes.

Current implementation:

```text
pages/base_page.py
pages/app_page.py
pages/login_page.py
pages/inventory_page.py
pages/product_details_page.py
pages/cart_page.py
pages/checkout_page.py
```

The Page Object layer is responsible for:

* page-specific locators
* reusable page actions
* browser interactions
* exposing UI state needed by tests
* hiding direct selector usage from tests where practical
* returning the next Page Object when navigation changes page context
* keeping shared authenticated behavior outside individual page classes

The Page Object layer should remain focused on interaction logic.

Assertions should remain in tests or reusable assertion helpers.

## `BasePage`

`BasePage` provides the minimal shared page foundation.

Current responsibilities:

* storing the Playwright `Page`
* shared URL metadata through `URL`
* shared `open()` behavior for directly accessible pages

`BasePage` should remain intentionally small.

It should not become a generic container for unrelated framework helpers.

## `AppPage`

`AppPage` owns shared authenticated-page behavior.

Current responsibilities:

* Cart link access
* opening Cart from authenticated pages
* cart badge access
* cart badge count reading
* application menu access
* closing the application menu
* logout
* reset app state
* All Items navigation
* About link access
* shared product-like item locators where required

`AppPage` is the correct owner for behavior shared by authenticated areas such as:

* Inventory
* Product Details
* Cart
* Checkout

Shared authenticated behavior should not be duplicated across individual Page Objects.

## `LoginPage`

`LoginPage` centralizes Login interactions.

Current responsibilities:

* opening Login
* filling username
* filling password
* clicking Login
* submitting credentials
* reading authentication errors
* closing authentication errors
* exposing Login page UI locators
* exposing input error icon locators

`LoginPage` does not inherit from `AppPage` because Login exists outside the authenticated application area.

## `InventoryPage`

`InventoryPage` centralizes Inventory interactions.

Current responsibilities include:

* Inventory container access
* product list access
* product card access
* locating products by name
* reading product names and prices
* sorting products
* opening Product Details from product names
* opening Product Details from product images
* adding products to Cart
* removing products from Cart

`InventoryPage` inherits authenticated shared behavior through `AppPage`.

## `ProductDetailsPage`

`ProductDetailsPage` centralizes Product Details interactions.

Current responsibilities include:

* opening Product Details by product ID
* accessing Product Details content
* accessing Add to cart
* accessing Remove
* adding a product to Cart
* removing a product from Cart
* accessing Back to products
* returning to Inventory

`ProductDetailsPage` inherits authenticated shared behavior through `AppPage`.

## `CartPage`

`CartPage` centralizes Cart interactions.

Current responsibilities include:

* opening Cart directly
* accessing Cart contents
* accessing Cart items
* locating Cart items by product name
* accessing Cart item name, description, price, quantity, and Remove
* removing products
* opening Product Details from Cart item names
* Continue Shopping
* returning to Inventory
* accessing Checkout
* opening Checkout Information

`CartPage` inherits authenticated shared behavior through `AppPage`.

Cart tests own the transition from Cart to Checkout Information.

Detailed checkout validation remains outside Cart ownership.

## `CheckoutInformationPage`

`CheckoutInformationPage` centralizes Checkout Information interactions.

Current responsibilities include:

* direct page opening where required
* customer information field access
* checkout title access
* Continue access
* Cancel access
* filling customer information
* continuing to Checkout Overview
* cancelling back to Cart
* checkout validation errors
* input error icons
* closing checkout validation errors

`CheckoutInformationPage` inherits authenticated shared behavior through `AppPage`.

## `CheckoutOverviewPage`

`CheckoutOverviewPage` centralizes Checkout Overview interactions.

Current responsibilities include:

* summary container access
* product item access
* locating items by product name
* payment information access
* shipping information access
* subtotal access
* tax access
* total access
* Cancel access
* Finish access
* cancelling back to Inventory
* finishing checkout
* opening Product Details from Checkout Overview

`CheckoutOverviewPage` inherits authenticated shared behavior through `AppPage`.

## `CheckoutCompletePage`

`CheckoutCompletePage` centralizes Checkout Complete interactions.

Current responsibilities include:

* completion container access
* completion image access
* completion header access
* completion message access
* Back Home access
* returning to Inventory

`CheckoutCompletePage` inherits authenticated shared behavior through `AppPage`.

## `framework/`

Contains shared framework logic that is not owned by a specific Page Object.

Current implementation:

```text
framework/assertions/product_assertions.py
```

Current responsibilities include:

* reusable product assertions
* Inventory product card validation
* Product Details validation
* Cart item validation
* Checkout Overview product validation
* Checkout Overview price summary validation
* Inventory product-state validation after navigation
* price conversion for numeric sorting and checkout calculations

Reusable assertion helpers should remain focused on validation.

They should not own:

* navigation
* browser setup
* fixtures
* Page Object interactions

## `test_data/`

Contains centralized test data.

Current implementation:

```text
test_data/login_test_data.py
test_data/product_test_data.py
test_data/checkout_test_data.py
```

Current Login data includes:

* valid user credentials
* invalid credential cases
* empty credential cases
* locked out user case
* expected authentication validation messages
* protected route URL suffixes

Current product data includes:

* product IDs
* product names
* product descriptions
* product prices
* product image paths

Current checkout data includes:

* valid customer information
* required-field validation messages
* checkout titles
* Checkout Overview summary labels
* Checkout Complete header and message expectations

Inventory, Product Details, Cart, and Checkout tests reuse centralized product data.

Cart does not currently require a separate Cart-specific data module.

Checkout-specific data is separated because checkout introduces unique customer data, validation messages, summary labels, and completion content.

## `conftest.py`

Contains shared pytest hooks and fixtures.

Current responsibilities include:

* screenshot capture on failure
* `opened_login_page`
* `standard_user`
* `logged_in_inventory_page`
* `inventory_page_with_one_product_in_cart`
* `cart_page_with_one_product`
* `checkout_step_one_page_with_one_product`
* `checkout_step_two_page_with_one_product`
* `checkout_last_step_page_with_one_product`

Fixtures prepare deterministic state without making tests depend on execution order.

Fixture growth should follow real repeated setup needs rather than speculative abstraction.

## Fixture-Based Test Independence

Reusable fixtures support independent test execution.

For example, Checkout checkpoints prepare the required state through fixture chains rather than relying on a previously executed test.

This supports:

* deterministic execution
* isolated tests
* marker-based selective execution
* independent E2E checkpoints
* dedicated Smoke and Regression CI execution
* complete full-suite CI execution
* CI stability

Tests should not rely on shared browser state produced by earlier test cases.

## `config/`

Reserved for framework and environment configuration.

Potential future usage includes:

* base URL configuration
* environment-specific settings
* browser configuration
* execution configuration

The layer remains intentionally minimal until approved framework maturity scope requires expansion.

Runtime environment configuration is not part of the current Phase 4B implementation.

## `reports/`

Stores generated runtime outputs.

Current usage includes:

* pytest HTML reports
* failure screenshots
* CI artifact source files

Generated runtime outputs should not be committed to Git.

They are intended for:

* debugging
* execution evidence
* CI artifacts

Current CI browser jobs generate separate report files for:

* Smoke
* Regression
* full-suite

Detailed report and artifact naming is documented in `docs/ci-cd-pipeline.md`.

## `test_cases/`

Contains manual test case documentation.

Current files:

```text
test_cases/login-page.md
test_cases/inventory-page.md
test_cases/product-details-page.md
test_cases/cart-page.md
test_cases/checkout-page.md
```

Test cases are mapped to automation through identifiers such as:

* `TC-LOGIN-XXX`
* `TC-INVENTORY-XXX`
* `TC-PRODUCT-DETAILS-XXX`
* `TC-CART-XXX`
* `TC-CHECKOUT-XXX`

The same identifiers are also used in parametrized pytest output where practical.

Test case files remain the source of truth for individual automation status.

## `docs/`

Contains technical documentation for:

* architecture
* framework structure
* workflow
* Git branching strategy
* testing strategy
* pytest marker strategy
* CI/CD
* quality tooling
* technology stack
* features
* roadmap

Documentation should reflect current implemented behavior and clearly separate it from planned functionality.

## Login Test Architecture

The Login test area follows:

```text
Manual Login test cases
        ↓
Centralized Login test data
        ↓
LoginPage
        ↓
Pytest Login module
        ↓
Markers and parametrization
        ↓
Selective local execution
        ↓
CI execution
```

Depending on marker assignment, Login tests may participate in:

* dedicated Smoke CI execution
* dedicated Regression CI execution
* complete full-suite CI execution

Current Login coverage includes:

* successful Login
* invalid username validation
* invalid password validation
* combined invalid username and password validation
* empty username validation
* empty password validation
* empty credentials validation
* locked out user validation
* authentication error close behavior
* Login page visibility
* password masking
* Enter submission
* protected Inventory route
* protected Cart route
* protected Product Details route
* protected Checkout Information route
* protected Checkout Overview route
* protected Checkout Complete route
* input error icons

Credential-validation cases and selected protected-route scenarios use pytest parametrization.

Parametrized IDs use manual test case IDs where practical.

## Inventory Test Architecture

The Inventory test area follows:

```text
Manual Inventory test cases
        ↓
Centralized product data
        ↓
InventoryPage
        ↓
Reusable logged-in fixture
        ↓
Reusable product assertions
        ↓
Pytest Inventory module
        ↓
Markers and parametrization
        ↓
Selective local execution
        ↓
CI execution
```

Depending on marker assignment, Inventory tests may participate in:

* dedicated Smoke CI execution
* dedicated Regression CI execution
* complete full-suite CI execution

Current Inventory coverage includes:

* Inventory visibility
* product list validation
* product card validation
* Cart navigation
* representative Add to cart behavior
* all-products Add to cart coverage
* Add to cart → Remove state validation
* representative Remove behavior
* all-products Remove coverage
* Remove → Add to cart state validation
* cart badge visibility
* cart badge count updates
* cart badge disappearance
* sorting by name
* sorting by price
* Product Details navigation through product names
* Product Details navigation through product images
* representative navigation checkpoints
* broader all-products navigation coverage

Inventory tests reuse `test_data/product_test_data.py`.

## Product Details Test Architecture

The Product Details test area follows:

```text
Manual Product Details test cases
        ↓
Centralized product data
        ↓
ProductDetailsPage
        ↓
Reusable logged-in fixture
        ↓
Reusable product assertions
        ↓
Pytest Product Details module
        ↓
Markers and parametrization
        ↓
Selective local execution
        ↓
CI execution
```

Depending on marker assignment, Product Details tests may participate in:

* dedicated Smoke CI execution
* dedicated Regression CI execution
* complete full-suite CI execution

Current Product Details coverage includes:

* representative Product Details visibility
* all-products Product Details validation
* Back to products navigation
* representative Add to cart
* all-products Add to cart
* Add to cart → Remove state
* representative Remove
* all-products Remove
* Remove → Add to cart state
* cart badge visibility
* cart badge count updates
* cart badge disappearance
* Cart navigation
* full Product Details → Cart navigation coverage across all products

## Cart Test Architecture

The Cart test area follows:

```text
Manual Cart test cases
        ↓
Centralized Login and product data
        ↓
InventoryPage / ProductDetailsPage / CartPage
        ↓
Reusable Cart setup fixtures
        ↓
Reusable product assertions
        ↓
Pytest Cart module
        ↓
Markers and parametrization
        ↓
Selective local execution
        ↓
CI execution
```

Depending on marker assignment, Cart tests may participate in:

* dedicated Smoke CI execution
* dedicated Regression CI execution
* complete full-suite CI execution

Current Cart coverage includes:

* empty Cart
* representative Cart item visibility
* Cart item content validation
* all-products Cart content validation
* representative Remove behavior
* all-products Remove coverage
* cart badge removal
* cart badge decrement
* Continue Shopping
* Continue Shopping state preservation
* Cart persistence after logout and re-login
* Product Details navigation from Cart
* full Cart → Product Details navigation coverage across all products
* Cart → Checkout Information navigation
* Cart-related E2E checkpoints

## Checkout Test Architecture

The Checkout test area follows:

```text
Manual Checkout test cases
        ↓
Centralized Checkout and product data
        ↓
Checkout Page Objects
        ↓
Reusable Checkout setup fixtures
        ↓
Reusable product and checkout assertions
        ↓
Pytest Checkout module
        ↓
Markers and parametrization
        ↓
Selective local execution
        ↓
CI execution
```

Depending on marker assignment, Checkout tests may participate in:

* dedicated Smoke CI execution
* dedicated Regression CI execution
* complete full-suite CI execution

Current Checkout coverage includes:

* Checkout Information form validation
* lightweight Smoke validation of Checkout Information form availability
* required First Name validation
* required Last Name validation
* required Postal Code validation
* input error icons
* validation error messages
* validation error close behavior
* valid data transition to Checkout Overview
* Checkout Information cancellation
* representative Checkout Overview product validation
* all-products Checkout Overview validation
* single-product price summary
* multiple-product price summary
* Checkout Overview cancellation
* representative Product Details navigation
* all-products Product Details navigation from Checkout Overview
* Finish transition
* Checkout Complete validation
* lightweight Smoke validation of Checkout Complete page availability
* Back Home navigation
* Checkout-related E2E checkpoints

## Marker Architecture

Pytest markers provide orthogonal test categorization and selective execution.

Current executable markers are:

* `smoke`
* `regression`
* `ui`
* `security`
* `sorting`
* `navigation`
* `e2e`

Marker intent:

* `smoke` — fast representative validation of critical functionality
* `regression` — broader validation across expanded or full applicable cases
* `ui` — visibility, presentation, state, and direct UI behavior
* `security` — access control and protected-route validation
* `sorting` — product sorting behavior
* `navigation` — meaningful page transitions excluding the authentication Login → Inventory transition
* `e2e` — independent checkpoints forming the primary purchase journey

Markers are not mutually exclusive.

A test may use multiple markers when it legitimately belongs to multiple suites.

Example:

```python
'@pytest.mark.smoke'
'@pytest.mark.navigation'
'@pytest.mark.e2e'
```

This represents a test that is simultaneously:

* a representative critical check
* a Navigation scenario
* an E2E journey checkpoint

Detailed marker semantics are documented in:

```text
docs/testing-strategy.md
```

### Marker Execution Responsibilities

All executable markers remain available for selective local execution.

Dedicated CI jobs currently exist for:

* `smoke`
* `regression`

Dedicated CI jobs do not currently exist for:

* `ui`
* `security`
* `sorting`
* `navigation`
* `e2e`

Tests carrying those markers are still included in complete full-suite CI execution.

Dedicated CI execution and marker semantics are separate concerns:

* markers define test intent and selectable suites
* CI determines which marker expressions receive dedicated workflow jobs

## E2E Architecture

The E2E suite represents independent checkpoints that collectively form the primary purchase journey.

Logical journey:

```text
Login
  ↓
Inventory
  ↓
Product selection
  ↓
Cart
  ↓
Checkout Information
  ↓
Checkout Overview
  ↓
Checkout Complete
  ↓
Back Home
  ↓
Inventory
```

E2E architecture deliberately avoids:

* shared state between test cases
* required test execution order
* one monolithic test containing the entire purchase flow

Each E2E test prepares its own required state through fixtures or local setup.

This allows:

```bash
pytest -m e2e -v
```

to execute a logical purchase-journey checkpoint suite while keeping individual tests isolated.

E2E does not currently have a dedicated GitHub Actions job.

E2E tests remain part of the complete unfiltered full-suite CI execution.

## Local And CI Execution Architecture

Local execution supports both:

* full-suite validation
* selective marker-based validation

Full local execution:

```bash
pytest -v
```

Current marker suites:

```bash
pytest -m smoke -v
pytest -m regression -v
pytest -m ui -v
pytest -m security -v
pytest -m sorting -v
pytest -m navigation -v
pytest -m e2e -v
```

### Current Phase 4B CI Architecture

GitHub Actions separates code-quality validation from browser-test execution.

Current job structure:

```text
quality
├── smoke
├── regression
└── full-suite
```

The `quality` job executes first and validates:

* Ruff
* Black
* isort

The quality job does not install Playwright Chromium.

Smoke, Regression, and full-suite declare:

```yaml
needs: quality
```

After successful quality validation, the three browser jobs are independently executable and do not depend on each other.

### Smoke CI Execution

Smoke executes the approved Smoke marker suite:

```bash
pytest -m smoke -v
```

The actual CI command also generates a self-contained pytest HTML report.

### Regression CI Execution

Regression executes the approved Regression marker suite:

```bash
pytest -m regression -v
```

The actual CI command also generates a self-contained pytest HTML report.

### Full-Suite CI Execution

The full-suite job executes the complete unfiltered Pytest suite:

```bash
pytest -v
```

The full-suite job remains the complete automated regression gate.

Smoke and Regression provide dedicated targeted feedback without replacing full-suite execution.

### Browser Execution

Playwright Chromium is installed only in browser-test jobs:

* Smoke
* Regression
* full-suite

The quality job does not prepare a browser environment.

### CI Artifacts

Each browser job generates its own pytest HTML report and uses non-conflicting GitHub Actions artifact names.

Artifact uploads use `if: always()` so available runtime evidence can still be published when an executing browser-test command fails.

Detailed CI commands, triggers, report paths, artifact names, and retention are documented in:

```text
docs/ci-cd-pipeline.md
```

## CI Execution Boundaries

The current CI architecture represents Phase 4B.

Phase 4B includes:

* separate code-quality validation
* dedicated Smoke CI execution
* dedicated Regression CI execution
* complete full-suite CI execution
* explicit quality-gate dependencies
* job-specific reports and artifacts

The independent browser jobs may be scheduled concurrently by GitHub Actions after `quality` succeeds.

This does not mean Pytest itself executes tests in parallel.

Parallel Pytest execution with `pytest-xdist` is not currently implemented and belongs to Phase 4C.

Advanced Allure reporting is not currently implemented and belongs to Phase 4D.

The current reporting architecture uses:

* `pytest-html`
* screenshots on failure
* GitHub Actions artifacts

Runtime environment configuration and other later framework maturity capabilities are also outside the current Phase 4B architecture.

## Design Direction

The framework follows a modular architecture where:

* tests describe behavior and expectations
* Page Objects handle interactions
* `BasePage` owns minimal common page behavior
* `AppPage` owns shared authenticated behavior
* assertion helpers own reusable validation logic
* test data remains externalized
* fixtures prepare deterministic reusable state
* manual test cases define documented scenario coverage
* markers organize selective test suites
* CI validates code quality before browser execution
* CI provides dedicated Smoke and Regression feedback
* CI preserves complete full-suite regression validation
* documentation describes implemented framework behavior

Future framework maturity work may improve:

* fixture organization
* environment configuration
* logging
* diagnostics
* reporting
* parallel execution

Phase 4C parallel execution and Phase 4D Allure reporting are not part of the current implementation.

Future API, cross-browser, Docker, Selenium, or Jenkins extensions remain separate from the current architecture.

## Architecture Principles

The framework should prioritize:

* readability
* maintainability
* deterministic execution
* test independence
* clear responsibility boundaries
* reusable components
* centralized test data
* traceability
* explicit marker semantics
* selective local validation
* dedicated Smoke and Regression CI feedback
* complete full-suite CI validation
* staged quality-gate execution
* incremental framework growth

The framework should avoid:

* unnecessary helper layers
* duplicated selectors
* duplicated test data
* shared test-state dependencies
* execution-order dependencies
* mixing detailed Checkout behavior into Cart ownership
* moving page-specific behavior into generic helpers prematurely
* moving authenticated shared behavior out of `AppPage`
* treating every Playwright test as automatically belonging to `ui`
* assigning Regression mechanically to every non-Smoke test
* treating CI job-level concurrency as Pytest parallel execution
* describing Allure as active reporting before Phase 4D
* describing future framework capabilities as already implemented

## Current Architecture Status

The current architecture supports automated page-level coverage for:

* Login
* Inventory
* Product Details
* Cart
* Checkout

Current architecture capabilities include:

* `BasePage`
* `AppPage`
* Page Object Model
* reusable assertion helpers
* centralized test data
* reusable fixtures
* test case traceability
* parametrized execution
* normalized pytest marker strategy
* Smoke execution
* Regression execution
* UI execution
* Security execution
* Sorting execution
* Navigation execution
* independent E2E checkpoint execution
* local selective validation
* separate CI code-quality validation
* dedicated Smoke CI execution
* dedicated Regression CI execution
* complete full-suite CI validation
* HTML reporting
* screenshot capture
* job-specific CI artifacts

Current CI architecture:

```text
quality
├── smoke
├── regression
└── full-suite
```

The `quality` job is the prerequisite gate.

Smoke, Regression, and full-suite are independent browser jobs after successful quality validation.

UI, Security, Sorting, Navigation, and E2E do not currently have dedicated CI jobs but remain selectively executable locally and participate in complete full-suite execution.

Parallel Pytest execution and advanced Allure reporting are not currently implemented.

The `main` branch represents the stable portfolio version of the project.

The `develop` branch and active workstream branches may contain newer validated changes before promotion.

The current architecture direction remains Phase 4 Framework Maturity, with Phase 4B CI Execution Strategy implemented and later maturity capabilities kept separate until their approved tasks are completed.
