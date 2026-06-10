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

* inventory page Page Object Model
* product list validation
* product sorting validation
* product details validation
* cart functionality tests
* cart badge validation
* cart page validation
* checkout form validation
* checkout form error handling
* full purchase flow
* logout and session behavior if relevant
* manual test cases for inventory, cart, and checkout areas
* test data expansion for product, cart, and checkout scenarios

Main learning goals:

* multi-page flows
* stateful UI testing
* reusable fixtures
* test data strategy
* end-to-end scenario design
* Page Object interaction between multiple pages
* clearer smoke/regression separation

---

## Phase 3A: Inventory And Products Automation Workstream

**Status:** In Review

Phase 3A focuses on inventory page and product-related validation before cart and checkout scenarios are implemented.

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

Current review scope:

* review completed inventory and products scope
* verify test case coverage
* verify Page Object structure
* verify fixture usage
* verify test data consistency
* verify marker usage
* review documentation updates
* confirm cleanup needs
* prepare the workstream for Pull Request into `develop`

Phase 3A should be completed and merged before starting cart and checkout automation.

---

## Phase 3B: Cart Automation Workstream

**Status:** Planned

Phase 3B will focus on cart-related behavior.

Planned areas:

* cart-related manual test cases
* CartPage Page Object Model if justified
* add product to cart scenarios
* remove product from cart scenarios
* cart badge validation
* cart link navigation
* cart page product validation
* cart state validation across inventory and cart pages
* cart-related test data if needed
* documentation updates

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

### After Phase 3

The project should be strong enough for regular job applications because it will include multi-page UI flows and more realistic application behavior.

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
* readiness for junior and junior+/mid QA automation roles
