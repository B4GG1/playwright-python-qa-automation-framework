# Roadmap

This document outlines the planned evolution of the QA automation framework.

The roadmap is organized into project phases to keep development focused, realistic, and aligned with portfolio goals.

## Phase 1: Foundation

**Status:** Completed

Phase 1 focused on establishing the technical foundation of the project.

Completed areas:

* repository structure
* Python virtual environment setup
* Playwright and Pytest setup
* basic smoke test execution
* pytest configuration
* Ruff configuration
* Black configuration
* isort configuration
* pre-commit hooks
* GitHub Actions CI pipeline
* CI artifact publishing
* HTML report generation
* screenshot capture on failure
* technical documentation structure
* Git workflow documentation
* README documentation hub

Phase 1 established the base required to start real QA automation work.

---

## Phase 2: Login Page Automation Workstream

**Status:** Completed

Phase 2 focused on building the first complete functional automation workstream for the Sauce Demo login page.

Completed areas:

* login page manual test cases
* LoginPage Page Object Model
* reusable pytest fixture for opened login page
* centralized login test data
* positive login scenario
* negative login scenarios
* pytest parametrization
* pytest marker usage
* login page UI visibility test
* error message close test
* password field masking validation
* login form submission with Enter key
* protected inventory route access validation
* protected cart route access validation
* protected item details route access validation
* login test case coverage mapping
* login suite stabilization
* Pull Request workflow
* Squash merge into `develop`

Main learning goals completed:

* Page Object Model
* test design
* test case review
* maintainable test structure
* reusable automation components
* centralized test data
* pytest parametrization
* marker-based test execution
* CI-backed automation workflow
* Pull Request and Squash merge workflow

Phase 2 produced the first complete and reviewed automation workstream in the project.

---

## Phase 2 Checkpoint: Review And Phase 3 Preparation

**Status:** Completed

The Phase 2 checkpoint verified that the login page workstream was completed and that the project was ready for the next automation area.

Completed checkpoint scope:

* reviewed completed login page scope
* verified full local test execution
* verified marker-based test execution
* reviewed CI status after merge
* reviewed documentation
* cleaned up outdated project information
* confirmed Git status
* prepared high-level Phase 3 scope

This checkpoint allowed the project to move from login-only automation into broader application coverage.

---

## Phase 3: Products, Cart, And Checkout Coverage

**Status:** In Progress

Phase 3 expands automation coverage beyond login.

The phase is split into smaller workstreams to keep the scope controlled and reviewable.

Planned and completed work:

* inventory page: Page Object Model
* product details Page Object Model
* product list validation
* product sorting validation
* product details validation
* cart page: Page Object Model
* cart functionality tests
* cart badge validation
* cart page validation
* cart product content validation
* remove-from-cart validation
* continue shopping navigation validation
* cart state persistence after logout and re-login
* checkout form validation
* checkout form error handling
* checkout overview validation
* full purchase flow
* manual test cases for inventory, cart, and checkout areas
* test data expansion for product, cart, and checkout scenarios where needed

Main learning goals:

* multi-page flows
* stateful UI testing
* reusable fixtures
* test data strategy
* end-to-end scenario design
* Page Object interaction between multiple pages
* clearer smoke/regression separation
* scope control between cart and checkout behavior

---

## Phase 3A: Inventory And Products Automation Workstream

**Status:** Completed

Phase 3A focused on inventory page and product-related validation before cart and checkout scenarios.

Completed areas:

* inventory and products manual test cases
* InventoryPage Page Object Model
* ProductDetailsPage Page Object Model
* reusable logged-in inventory page fixture
* centralized inventory product test data
* inventory page visibility test
* product list validation
* product card content validation
* product details navigation from product name
* product details navigation from product image
* return from product details page to inventory page
* product sorting by name A to Z
* product sorting by name Z to A
* product sorting by price low to high
* product sorting by price high to low
* sorting marker registration
* local validation of inventory tests
* full local test suite validation
* test case coverage mapping
* documentation updates

Completed review scope:

* reviewed completed inventory and products scope
* verified test case coverage
* verified Page Object structure
* verified fixture usage
* verified test data consistency
* verified marker usage
* reviewed documentation updates
* confirmed cleanup needs

Phase 3A completed the inventory and product validation layer required before cart automation.

---

## Phase 3B: Cart Automation Workstream

**Status:** In Final Review / Stabilization

Phase 3B focuses on cart-related behavior.

Implemented areas:

* cart-related manual test cases
* CartPage Page Object Model
* cart page availability validation
* empty cart state validation
* add product to cart from inventory page
* cart link navigation
* cart badge visibility validation
* cart badge count validation
* cart page product visibility validation
* cart product content validation
* remove product from cart page
* cart badge removal after removing the last product
* continue shopping navigation from cart to inventory
* cart state persistence after logout and re-login
* product-details-side Add to cart and Remove button behavior
* use of existing centralized inventory product test data for cart scenarios
* use of existing valid user test data for persistence scenarios
* cart test case coverage mapping
* documentation updates

Current stabilization scope:

* review completed cart workstream files
* verify cart test cases against implemented automation
* verify TC-CART IDs used in tests
* verify Page Object responsibility boundaries
* verify that tests do not duplicate selectors unnecessarily
* confirm checkout behavior remains excluded from cart scope
* review README and technical docs for current project state
* run cart-specific validation
* run full local test suite
* run quality checks
* confirm Git status and cleanup needs
* prepare the workstream for the next project step

Phase 3B should be considered complete after the final stabilization checkpoint passes and the branch is ready for merge preparation.

---

## Phase 3B Checkpoint: Review And Stabilize Cart Workstream

**Status:** In Progress

The Phase 3B checkpoint verifies that the completed Cart Automation Workstream is consistent, stable, documented, and ready for the next project step.

Checkpoint scope:

* review cart test case documentation
* review cart automated tests
* review cart-related Page Object methods
* review shared fixtures and test data usage
* review README and technical documentation updates
* verify checkout scope exclusion
* verify local quality checks
* verify cart test module execution
* verify full test suite execution
* confirm no generated files or local artifacts are tracked
* commit documentation and cleanup changes
* push the branch to GitHub

This checkpoint prevents checkout work from being built on top of outdated cart documentation or unstable cart automation.

---

## Phase 3C: Checkout Automation Workstream

**Status:** Planned

Phase 3C will focus on checkout-related behavior.

Planned areas:

* checkout-related manual test cases
* CheckoutPage Page Object Model if justified
* checkout information form validation
* checkout error handling
* checkout overview validation
* complete order flow
* order confirmation validation
* checkout-related test data
* documentation updates

Checkout work should remain separate from the cart workstream to keep scope clear and maintainable.

---

## Phase 3 Checkpoint

**Status:** Planned

After Phase 3 implementation, a checkpoint task will be required before moving to Phase 4.

Checkpoint scope:

* review completed Phase 3 scope
* validate test coverage
* run full local test suite
* run marker-based test groups
* verify CI status
* review documentation updates
* review Git status and cleanup needs
* confirm readiness for Phase 4

This checkpoint should happen after checkout coverage is completed and stabilized.

---

## Phase 4: Framework Maturity

**Status:** Planned

Phase 4 will improve framework scalability and maintainability.

Planned work:

* smoke and regression suite separation improvements
* CI jobs for selected test groups
* pytest marker strategy improvements
* parallel execution with pytest-xdist
* improved reporting structure
* Allure reporting integration
* environment-based configuration
* reusable assertion helpers
* logging utilities
* improved fixture organization
* stronger diagnostics for failed tests

Main learning goals:

* scalable test organization
* execution optimization
* advanced reporting
* maintainable framework design
* stronger CI/test feedback loops

---

## Phase 4 Checkpoint

**Status:** Planned

After Phase 4 implementation, a checkpoint task will be required before moving to advanced extensions.

Checkpoint scope:

* review framework maturity improvements
* verify reporting and diagnostics
* verify CI execution strategy
* review documentation
* check cleanup needs
* confirm whether the project is ready for broader portfolio presentation or advanced extensions

---

## Phase 5: Advanced Extensions

**Status:** Future

Phase 5 will introduce advanced framework extensions.

Potential work:

* API testing layer using Requests
* hybrid UI + API scenarios
* Docker-based execution environment
* cross-browser execution strategy
* Selenium WebDriver comparison module
* Jenkins pipeline integration
* test analytics and history tracking
* framework packaging as reusable template

Main learning goals:

* broader QA automation tooling
* API testing fundamentals
* CI/CD maturity
* cross-browser strategy
* framework extensibility
* portfolio differentiation

---

## Portfolio Milestones

### After Phase 2

The project contains a complete login page automation workstream and can be used as an early proof of structured QA automation learning.

Recommended use:

* internal review
* selective portfolio sharing
* preparation for CV/GitHub profile updates

### After Phase 3A

The project contains login coverage plus inventory and product validation.

Recommended use:

* stronger GitHub portfolio presentation
* early QA Automation application support
* demonstration of Page Object Model beyond a single page
* demonstration of product data validation and sorting tests

### After Phase 3B

The project contains login, inventory, product details, and cart automation coverage.

Recommended use:

* stronger portfolio presentation than login/inventory-only state
* demonstration of stateful UI testing
* demonstration of multipage Page Object interaction
* demonstration of cart behavior validation without mixing checkout scope
* continued preparation for regular QA Automation applications

### After Phase 3

The project should be strong enough for regular job applications because it will include multipage UI flows, cart behavior, checkout behavior, and more realistic application coverage.

Recommended use:

* regular QA Automation applications
* GitHub portfolio presentation
* CV project section update

### After Phase 4

The project should be close to a mature portfolio-ready QA automation framework.

Recommended use:

* stronger Junior / Junior+ QA Automation applications
* Technical QA applications
* broader recruiter-facing portfolio presentation

---

## Strategic Vision

The long-term objective is to evolve this repository into a scalable, portfolio-ready QA automation framework that demonstrates:

* practical QA automation skills
* test design ability
* maintainable test architecture
* CI/CD workflow understanding
* modern Python tooling
* Playwright expertise
* ability to work with Page Object Model
* ability to organize test data and parametrized tests
* ability to keep scope controlled across workstreams
* ability to maintain documentation alongside automation
* readiness for junior and junior+/mid QA automation roles
