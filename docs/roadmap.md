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

**Status:** Current

The current checkpoint verifies that Phase 2 is fully completed and that the project is ready for the next automation area.

Checkpoint scope:

* review completed login page scope
* verify full local test execution
* verify marker-based test execution
* review CI status after merge
* review documentation
* clean up outdated project information
* confirm Git status
* prepare high-level Phase 3 scope

This checkpoint must be completed before starting Phase 3.

---

## Phase 3: Products, Cart, And Checkout Coverage

**Status:** Planned

Phase 3 will expand automation coverage beyond login.

Planned work:

* inventory page Page Object Model
* product list validation
* product sorting validation
* product details validation if needed
* add to cart scenarios
* remove from cart scenarios
* cart badge validation
* cart page validation
* checkout form validation
* checkout form error handling
* full purchase flow
* logout and session behavior if relevant
* manual test cases for inventory, cart, and checkout areas
* test data expansion for product/cart/checkout scenarios

Main learning goals:

* multi-page flows
* stateful UI testing
* reusable fixtures
* test data strategy
* end-to-end scenario design
* Page Object interaction between multiple pages
* clearer smoke/regression separation

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
