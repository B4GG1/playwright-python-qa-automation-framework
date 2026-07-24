# Technology Stack

This document describes the technologies, tools, and planned integrations used in the QA automation framework.

The stack is divided into implemented technologies, installed but not fully integrated tools, and planned future extensions.

The technology stack described below represents the stable Phase 3 portfolio snapshot. The `main` branch should contain the polished portfolio version of this snapshot, while `develop` remains the integration branch and may contain newer work after this document is read from `main`.

## Core Technologies

The project is currently built with:

* Python 3.12
* Pytest
* Playwright
* pytest-playwright
* Git
* GitHub
* GitHub Actions
* WSL2 with Ubuntu Linux

These technologies form the current implemented UI automation foundation.

## Test Automation

Current implemented test automation stack:

* Playwright for browser automation
* Pytest as the test runner
* pytest-playwright for Playwright and Pytest integration
* Page Object Model for page interaction abstraction
* shared authenticated-page behavior through `AppPage`
* reusable assertion helpers for repeated product-related and checkout-related validations
* pytest fixtures for reusable test setup
* pytest parametrization for data-driven test scenarios
* pytest markers for test categorization

Current browser execution:

* Chromium

Current automated UI coverage:

* login page smoke validation
* positive login scenarios
* negative login scenarios
* login UI behavior
* protected inventory route access validation
* protected cart route access validation
* protected item details route access validation
* protected checkout information route access validation
* protected checkout overview route access validation
* protected checkout complete route access validation
* inventory page validation
* product list validation
* product card content validation
* inventory-side product details navigation validation
* product details page validation
* product details add-to-cart behavior validation
* product details remove-from-cart behavior validation
* product sorting validation
* cart page validation
* empty cart state validation
* add-to-cart behavior validation from inventory and product details pages
* cart badge validation
* cart item visibility and content validation
* remove-from-cart validation from inventory, product details, and cart pages
* continue shopping navigation validation
* cart state persistence after logout and re-login
* cart-owned checkout step one navigation validation
* checkout information form validation
* checkout required field validation
* checkout information error handling
* checkout overview product summary validation
* checkout overview price summary validation
* checkout overview cancellation validation
* product details navigation from checkout overview
* checkout finish action validation
* checkout complete page confirmation validation
* Back Home navigation after order completion

Planned browser execution:

* Firefox
* WebKit
* cross-browser test execution strategy

Firefox, WebKit, and cross-browser execution are planned future extensions. The current implemented browser execution uses Chromium.

## Page Object Model

Currently implemented:

* `BasePage`
* `AppPage`
* `LoginPage`
* `InventoryPage`
* `ProductDetailsPage`
* `CartPage`
* `CheckoutInformationPage`
* `CheckoutOverviewPage`
* `CheckoutCompletePage`

Current Page Object responsibilities:

* shared page initialization and open behavior through `BasePage`
* shared authenticated-page behavior through `AppPage`
* login page navigation
* username input interaction
* password input interaction
* login button interaction
* error message handling
* login page UI element locators
* inventory page visibility and product list access
* inventory product card access
* inventory product sorting
* product details navigation from product name
* product details navigation from product image
* product details page element locators
* product details cart actions
* returning from product details to inventory page
* inventory cart actions
* authenticated header cart link and cart badge access
* application menu interactions
* logout support
* cart page navigation
* cart item lookup
* cart item content access
* cart product removal
* product details navigation from cart item name
* continue shopping navigation
* checkout button access and cart-owned checkout step one navigation
* checkout information form field access
* checkout information form submission
* checkout information validation error access
* checkout information input error icon access
* checkout information error close interaction
* checkout information cancellation back to cart
* checkout overview product item access
* checkout overview price summary access
* checkout overview cancellation back to inventory
* product details navigation from checkout overview item name
* checkout finish action
* checkout complete confirmation access
* Back Home navigation after checkout completion

Planned Page Object expansion:

* additional page objects only when future application areas require dedicated page-level ownership

## Reusable Assertions

Currently implemented:

* `framework/assertions/product_assertions.py`

Current reusable assertion helper responsibilities:

* inventory product card content validation
* product details content validation
* cart item content validation
* checkout overview product item content validation
* checkout overview price summary validation
* inventory product state validation after checkout-related navigation
* price string conversion for numeric sorting and checkout summary assertions

Reusable assertion helpers are used when the same validation logic is shared across multiple page areas. They should remain focused on assertions and should not own navigation, setup, or Page Object responsibilities.

## Test Data Management

Currently implemented:

* centralized login test data
* centralized product test data
* centralized checkout test data
* valid user cases
* invalid login cases
* empty credential cases
* locked out user cases
* expected login error messages
* protected route URL suffixes
* product IDs
* product names
* product descriptions
* product prices
* product image paths
* valid checkout customer information
* checkout required field error messages
* checkout page title expectations
* checkout overview summary label expectations
* checkout completion header and message expectations
* deterministic product data reused by inventory, product details, cart, and checkout tests
* test case IDs used in parametrized pytest output where practical

Current test data location:

```
test_data/login_test_data.py
test_data/product_test_data.py
test_data/checkout_test_data.py
```

Planned test data expansion:

* API test data
* environment-specific test data if needed
* additional UI test data only when future approved scope requires it

## Code Quality And Development Tooling

Current quality tools:

* Ruff for linting and static checks
* Black for code formatting
* isort for import sorting
* pre-commit for local quality gates

These tools are used to maintain consistent code style, reduce formatting-related issues, and support a professional development workflow.

Tool configuration is stored in:

```
pyproject.toml
.pre-commit-config.yaml
pytest.ini
```

## CI/CD And Automation

Current CI tool:

* GitHub Actions

Current CI responsibilities:

* repository checkout
* Python setup
* dependency installation
* Playwright Chromium browser installation
* linting with Ruff
* formatting validation with Black
* import sorting validation with isort
* test execution with Pytest
* HTML report generation
* artifact upload

Current CI targets:

* pushes to `main`
* pushes to `develop`
* pull requests targeting `main`
* pull requests targeting `develop`
* manual workflow execution using `workflow_dispatch`

The `main` branch represents the stable portfolio branch. The `develop` branch represents the integration branch for completed and validated work before promotion to `main`.

Planned CI/CD improvements:

* dependency caching
* browser caching
* JUnit XML reporting
* separate smoke and regression jobs
* separate marker-based CI jobs
* multi-browser CI execution
* Docker-based execution
* advanced reporting publication

## Reporting And Debugging

Currently implemented:

* pytest-html
* CI artifact upload
* automatic screenshot capture on test failure
* reports directory for runtime outputs
* downloadable CI artifacts for debugging

Installed but not fully integrated:

* allure-pytest

Current reporting status:

* pytest-html is the implemented reporting solution
* screenshots on failure are implemented through the pytest hook
* CI artifacts are implemented through GitHub Actions
* Allure is planned as an advanced reporting integration and is not fully integrated yet

Planned reporting improvements:

* advanced Allure reporting
* improved screenshot structure
* logs as CI artifacts
* test result history and analytics
* better failure diagnostics

## API Testing

Currently installed:

* requests

Current status:

* API testing layer is not implemented yet

Planned usage:

* API smoke tests
* backend validation support
* hybrid UI and API test scenarios
* test data setup or validation through API calls where appropriate

The presence of `requests` in the dependency list prepares the project for future API testing, but API tests are not part of the current implemented automation scope.

## Test Execution Optimization

Currently installed:

* pytest-xdist

Current status:

* parallel test execution is not optimized yet
* pytest-xdist is not part of the default local or CI execution workflow yet

Planned usage:

* faster regression execution
* parallel UI test runs
* CI execution optimization

Parallel execution will be introduced later, after the test suite grows and stability requirements are better understood.

## Version And Dependency Management

Current dependency files:

* `requirements.txt`
* `requirements-lock.txt`

Current usage:

* `requirements.txt` provides a readable list of main project dependencies
* `requirements-lock.txt` provides locked dependency versions for reproducible setup and CI execution

Main installed dependencies include:

* `pytest`
* `playwright`
* `pytest-playwright`
* `requests`
* `allure-pytest`
* `pytest-html`
* `pytest-xdist`
* `ruff`
* `black`
* `isort`
* `pre-commit`

Some installed dependencies support current functionality, while others prepare the project for future extensions:

* `pytest`, `playwright`, `pytest-playwright`, `pytest-html`, `ruff`, `black`, `isort`, and `pre-commit` support the current implemented framework.
* `requests`, `allure-pytest`, and `pytest-xdist` are installed for planned future expansion and are not fully integrated into the implemented framework scope yet.

Planned improvements:

* dependency update workflow
* optional dependency grouping if the project grows

## Development Environment

Current local development environment:

* Windows host system
* WSL2 with Ubuntu Linux
* Python virtual environment
* PyCharm Community
* Git and GitHub
* browser automation through Playwright

This setup supports Linux-based test execution locally while keeping the project compatible with GitHub Actions CI.

## Planned Integrations

Future planned integrations include:

* Selenium WebDriver comparison module
* Docker-based execution environment
* environment configuration management
* expanded test data management utilities
* Jenkins CI integration
* cross-browser execution support
* Allure reporting
* API testing layer
* framework packaging as a reusable automation template

These integrations are planned future extensions and should not be described as implemented until they are added, validated, and documented in the relevant workstream.

## Current Stack Status

The current stack is sufficient to support completed page-level automation coverage for Login, Inventory, Product Details, Cart, and Checkout areas.

Implemented technical capabilities include:

* UI automation with Playwright
* Chromium browser execution
* test execution with Pytest
* Page Object Model
* shared authenticated-page behavior through `AppPage`
* reusable product and checkout assertion helpers
* reusable pytest fixtures
* centralized login, product, and checkout test data
* parametrized tests
* marker-based test organization
* local quality checks
* CI validation
* HTML reporting
* screenshot capture on failure
* technical documentation

Phase 3 page-level automation coverage has been completed, reviewed, validated, squash-merged into `develop`, and promoted to `main` as the stable Phase 3 portfolio snapshot.

The `main` branch represents the polished portfolio version of the project. The `develop` branch remains the integration branch and may contain newer work after this document is read from `main`.

The next stack expansion should focus on framework maturity, reporting, CI optimization, API testing, cross-browser execution, or other future approved workstreams rather than additional checkout foundation work.
