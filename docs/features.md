# Features

This document lists the currently implemented and planned features of the QA automation framework.

The purpose of this file is to provide a quick overview of what the framework already supports and what will be developed in future phases.

The implemented feature set described below represents the stable Phase 3 portfolio snapshot. The `main` branch should contain the polished portfolio version of this snapshot, while `develop` remains the integration branch and may contain newer work after this document is read from `main`.

The current implemented scope focuses on UI automation with Playwright and Pytest. API testing, Selenium comparison, Docker-based execution, Jenkins integration, cross-browser execution, and advanced reporting are planned extensions and are not part of the implemented feature set yet.

## Currently Implemented

### Test Execution

* UI test automation using Playwright
* Pytest-based test execution
* Smoke test execution support
* Regression test execution support
* Sorting test execution support
* Navigation test execution support
* End-to-end marker support
* Marker-based selective test execution
* Centralized pytest configuration
* Playwright Chromium execution in CI
* Full test suite execution in CI

### Page Object Model

* BasePage abstraction implemented
* AppPage abstraction for authenticated shared behavior implemented
* Login Page Object implemented
* Inventory Page Object implemented
* Product Details Page Object implemented
* Cart Page Object implemented
* Checkout Page Objects implemented
* Centralized login page locators
* Centralized authenticated-page shared locators
* Centralized inventory page locators
* Centralized product details page locators
* Centralized cart page locators
* Centralized checkout information page locators
* Centralized checkout overview page locators
* Centralized checkout complete page locators
* Reusable login page actions
* Reusable authenticated-page actions
* Reusable inventory page actions
* Reusable product details page actions
* Reusable cart page actions
* Reusable checkout information page actions
* Reusable checkout overview page actions
* Reusable checkout complete page actions
* Error message interaction support
* Login page UI element access methods
* Input error icon access methods
* Inventory product list and product card access methods
* Product details page element access methods
* Cart item and cart content access methods
* Checkout information form access methods
* Checkout overview product item access methods
* Checkout overview price summary access methods
* Checkout complete confirmation access methods
* Cart badge access methods
* Continue Shopping interaction support
* Add-to-cart interaction support
* Remove-from-cart interaction support
* Checkout navigation support from cart page
* Checkout information form submission support
* Checkout cancellation support
* Checkout finish action support
* Back Home navigation support after checkout completion
* Logout interaction support from authenticated pages
* Application menu interaction support
* Lightweight navigation between Page Objects

### Reusable Assertions

* Reusable product assertion helpers
* Inventory product card content validation helper
* Product details content validation helper
* Cart item content validation helper
* Checkout overview product item content validation helper
* Checkout overview price summary validation helper
* Inventory product item validation helper after checkout-related navigation
* Product price conversion helper for numeric sorting and checkout summary assertions

### Test Data Management

* Centralized login test data
* Centralized product test data
* Centralized checkout test data
* Valid user test data
* Invalid login test data
* Empty credentials test data
* Locked out user test data
* Expected login error messages
* Protected route URL suffixes for access-control validation
* Product IDs, names, descriptions, prices, and image paths
* Valid checkout customer information
* Checkout required field error messages
* Checkout page title expectations
* Checkout overview summary label expectations
* Checkout completion header and message expectations
* Deterministic product data reused by inventory, product details, cart, and checkout tests
* Test case IDs mapped to automated test data where practical

### Login Page Test Coverage

The framework currently includes automated coverage for the login scenarios:

* successful login with valid credentials
* login with invalid username
* login with invalid password
* login with empty username
* login with empty password
* login with empty credentials
* locked out user login attempt
* login with invalid username and invalid password
* closing error message after failed login
* login page elements visibility
* password field masking validation
* login form submission with Enter key
* direct inventory page access without login
* direct cart page access without login
* direct item page access without login
* direct checkout information page access without login
* direct checkout overview page access without login
* direct checkout complete page access without login
* input error icons displayed after failed login

### Inventory Page Test Coverage

The framework currently includes automated coverage for the Sauce Demo inventory page area.

Implemented inventory scenarios:

* inventory page visibility after successful login
* product list visibility
* product card content validation
* cart page navigation from inventory page
* product can be added to cart from inventory page
* inventory-side Add to cart button changes to Remove after adding a product
* cart badge is displayed after adding one product
* cart badge count updates after adding multiple products
* product sorting by name A to Z
* product sorting by name Z to A
* product sorting by price low to high
* product sorting by price high to low
* product details can be opened for all products by product name from inventory page
* product details can be opened for all products by product image from inventory page
* all products can be added to cart from inventory page
* product can be removed from cart from inventory page
* inventory-side Remove button changes back to Add to cart after removing a product
* cart badge count updates after removing one of multiple products from inventory page
* cart badge disappears after removing the last product from inventory page
* all products can be removed from cart from inventory page
* product details can be opened from product name for an example product
* product details can be opened from product image for an example product

### Product Details Page Test Coverage

The framework currently includes automated coverage for the Sauce Demo product details page area.

Implemented product details scenarios:

* product details content is displayed for a selected product
* product details content matches centralized product data for each product
* user can return from product details page to inventory page
* Add to cart button changes to Remove after adding a product from product details page
* product can be added to cart from product details page
* all products can be added to cart from product details page
* product can be removed from cart from product details page
* Remove button changes back to Add to cart after removing product from product details page
* cart badge is displayed after adding product from product details page
* cart badge count updates after adding product from details when cart is not empty
* cart badge count updates after removing one of multiple products from product details page
* cart badge disappears after removing the last product from product details page
* cart page can be opened from product details page
* all products can be removed from cart from product details page

### Cart Page Test Coverage

The framework currently includes automated coverage for the Sauce Demo cart page area.

Implemented cart scenarios:

* cart is empty before adding products
* added product is displayed on cart page
* cart product content matches added product data
* product can be removed from cart page
* cart badge is removed after removing the last product
* user can return from cart page to inventory page
* cart state persists after logout and re-login
* all added products are displayed on cart page
* cart product content matches added product data for each product
* cart badge decrements after removing one of multiple products
* product details can be opened from cart item name
* Continue Shopping preserves cart state
* all products can be removed from cart page
* checkout button opens checkout information page with product in cart

Cart Page coverage owns the user action that starts on the cart page and opens checkout step one. Detailed checkout information, overview, and completion behavior is owned by Checkout Page coverage.

### Checkout Page Test Coverage

The framework currently includes automated coverage for the Sauce Demo checkout flow.

Implemented checkout scenarios:

* checkout information form displays required customer fields
* checkout information form requires first name
* checkout information form requires last name
* checkout information form requires postal code
* input error icons are displayed after failed checkout information submission
* checkout information error message can be closed after validation failure
* checkout information form continues to overview when valid data is provided
* checkout information cancel returns to cart and preserves cart item
* checkout overview displays selected product
* checkout overview displays each selected product
* checkout overview price summary is correct for one product
* checkout overview price summary is correct for multiple products
* checkout overview cancel returns to inventory page
* product details can be opened from checkout overview item name
* product details can be opened from checkout overview item name for each product
* finish button completes checkout and opens order confirmation page
* checkout complete page displays order confirmation message
* Back Home returns to inventory page after order completion

### Test Organization

* One automated test module per covered page area
* One manual test case file per covered page area
* Pytest marker-based test categorization
* Registered smoke, regression, UI, positive, negative, sorting, navigation, API, and e2e markers
* Parametrized negative login scenarios
* Parametrized protected route access scenarios
* Parametrized inventory product scenarios
* Parametrized product details scenarios
* Parametrized cart scenarios using manual test case IDs
* Parametrized checkout scenarios using manual test case IDs where practical
* Parametrized test output with manual test case IDs
* Manual test case documentation under `test_cases/`
* Login test case coverage mapped to automated tests
* Inventory test case coverage mapped to automated tests
* Product Details test case coverage mapped to automated tests
* Cart test case coverage mapped to automated tests
* Checkout test case coverage mapped to automated tests

### Fixtures And Reusable Setup

* Shared pytest fixture for opened login page
* Shared pytest fixture for standard user credentials
* Shared pytest fixture for logged-in inventory page
* Shared pytest fixture for inventory page with one product in cart
* Shared pytest fixture for cart page with one product
* Shared pytest fixture for checkout step one page with one product
* Shared pytest fixture for checkout step two page with one product
* Shared pytest fixture for checkout complete page with one product
* Reusable setup for login page tests
* Reusable setup for inventory tests
* Reusable setup for product details tests
* Reusable setup for cart tests
* Reusable setup for checkout tests
* Screenshot capture hook on test failure

### Code Quality

* Static code analysis with Ruff
* Automated code formatting using Black
* Import standardization with isort
* Automated local quality gates using pre-commit hooks
* CI quality gate for linting, formatting, imports, and test execution

### CI/CD

* GitHub Actions CI pipeline
* Automated dependency installation in CI
* Automated Playwright Chromium browser installation in CI
* Automated linting, formatting validation, and test execution
* CI execution on `main` and `develop`
* CI execution for pull requests targeting `main` and `develop`
* Manual CI execution using `workflow_dispatch`
* Minimal workflow permissions using `contents: read`
* CI artifacts upload for reports and debugging outputs
* Explicit artifact retention configuration
* Stable portfolio branch validation for `main`
* Integration branch validation for `develop`

### Reporting And Debugging

* HTML test report generation using pytest-html
* Self-contained HTML report generation in CI
* Test artifacts uploaded from CI
* Reports directory used for runtime outputs
* Screenshot capture on test failure
* Downloadable CI artifacts for debugging

### Repository And Documentation

* GitHub-based portfolio repository structure
* Lightweight Git branching strategy documentation
* Technical documentation structure under `docs/`
* README used as project landing page and documentation hub
* Linux-based development workflow using WSL2
* Login page manual test cases documented in Markdown
* Inventory page manual test cases documented in Markdown
* Product Details page manual test cases documented in Markdown
* Cart page manual test cases documented in Markdown
* Checkout page manual test cases documented in Markdown
* Login page automation coverage documented and mapped to test files
* Inventory page automation coverage documented and mapped to test files
* Product Details page automation coverage documented and mapped to test files
* Cart page automation coverage documented and mapped to test files
* Checkout page automation coverage documented and mapped to test files
* Stable Phase 3 portfolio baseline documentation

## Planned Features

### Framework Architecture

* Expanded shared pytest fixtures when setup flows grow
* Environment-based configuration management
* Improved configuration structure for base URLs and execution settings
* Additional reusable framework utilities when repeated framework logic appears
* Additional Page Object classes for future application areas only when new page-level scope requires them

### Test Coverage

Planned future automation areas:

* broader multipage user journey tests
* broader session and logout validation if required by future scope
* cross-browser UI execution
* API-level test coverage
* additional edge-case or known-defect coverage if approved during planning

### Test Organization

* Smoke and regression suite separation in CI
* Improved marker-based CI jobs
* More advanced parametrized test scenarios
* Expanded manual test case documentation for new application areas
* Improved traceability between test cases, test data, and automation

### Reporting And Diagnostics

* Improved failure diagnostics
* Better screenshot organization
* Advanced Allure reporting
* Test logs and execution evidence
* Test history and analytics

### CI/CD Improvements

* Dependency caching for faster pipeline execution
* Playwright browser caching
* JUnit XML test result publishing
* Separate smoke and regression CI jobs
* Separate marker-based CI jobs for selected test categories
* Multi-browser CI execution
* Scheduled regression runs

### Future Extensions

* API automation testing layer
* Selenium WebDriver comparison module
* Docker-based execution environment
* Parallel test execution optimization
* Jenkins pipeline integration
* Framework packaging as a reusable automation template
