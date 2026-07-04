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
* input error icon validation after failed login
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

Completed and in-progress work:

* inventory page Page Object Model
* product details Page Object Model
* cart page Page Object Model
* shared authenticated-page behavior through `AppPage`
* reusable product assertion helpers
* product list validation
* product sorting validation
* product details validation
* inventory-side product details navigation
* cart functionality tests
* cart badge validation
* cart page validation
* cart product content validation
* remove-from-cart validation from inventory, product details, and cart pages
* continue shopping navigation validation
* cart state persistence after logout and re-login
* manual test cases for login, inventory, product details, and cart areas
* test data expansion for product scenarios
* documentation synchronization after structure cleanup

Planned later in Phase 3:

* checkout form validation
* checkout form error handling
* checkout overview validation
* full purchase flow
* checkout-related manual test cases
* checkout-related test data where needed

Main learning goals:

* multi-page flows
* stateful UI testing
* reusable fixtures
* reusable assertion helpers
* test data strategy
* end-to-end scenario design
* Page Object interaction between multiple pages
* clearer smoke/regression separation
* scope control between cart and checkout behavior
* documentation synchronization after structural refactors

---

## Phase 3A: Inventory And Products Automation Workstream

**Status:** Completed

Phase 3A focused on inventory page and product-related validation before cart and checkout scenarios.

Completed areas:

* inventory and products manual test cases
* InventoryPage Page Object Model
* ProductDetailsPage Page Object Model
* reusable logged-in inventory page fixture
* centralized product test data
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

**Status:** Completed

Phase 3B focused on cart-related behavior.

Completed areas:

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
* use of existing centralized product test data for cart scenarios
* use of existing valid user test data for persistence scenarios
* cart test case coverage mapping
* documentation updates

Completed stabilization scope:

* reviewed completed cart workstream files
* verified cart test cases against implemented automation
* verified TC-CART IDs used in tests
* verified Page Object responsibility boundaries
* verified that tests do not duplicate selectors unnecessarily
* confirmed checkout behavior remains excluded from cart scope
* reviewed README and technical docs for current project state
* ran cart-specific validation
* ran full local test suite
* ran quality checks
* confirmed Git status and cleanup needs
* prepared the workstream for the next project step

Phase 3B completed cart behavior automation while keeping checkout behavior out of scope.

---

## Phase 3C: Structure Cleanup, Coverage Completion, And Documentation Sync

**Status:** In Final Validation

Phase 3C focuses on final cleanup after the Login, Inventory, Product Details, and Cart page-level coverage work.

The goal of this workstream is to align project structure, test coverage, Page Objects, fixtures, test case files, and documentation before PR and merge.

Completed and in-progress areas:

* one automated test module per covered page area
* one manual test case file per covered page area
* Login, Inventory, Product Details, and Cart test case coverage synchronization
* missing page-level coverage completion after cart workstream
* Page Object responsibility review
* `BasePage` and `AppPage` structure review
* authenticated shared behavior ownership review
* reusable product assertion helper extraction
* fixture naming and reuse review
* navigation return type review
* TC coverage mapping review
* test case metadata cleanup
* README and technical documentation synchronization
* roadmap readiness review for the next workstream
* final local quality validation
* final full pytest validation
* PR readiness confirmation or blocker listing

Current Phase 3C validation scope:

* review test files, test case files, Page Objects, fixtures, and documentation end to end
* confirm that no new feature coverage is added during final validation
* confirm that checkout behavior remains excluded from current coverage
* confirm documentation reflects the final post-refactor state
* confirm full pytest suite and quality checks pass
* confirm branch readiness for PR

Phase 3C should be considered complete after AQA-0073 final validation passes, documentation sync is committed, Git status is clean, and the branch is ready for PR.

---

## Next Phase 3 Workstream: Checkout Automation

**Status:** Planned

The next Phase 3 functional workstream should focus on checkout-related behavior.

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

Checkout work should remain separate from inventory, product details, and cart work to keep scope clear and maintainable.

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

### After Phase 3C

The project contains synchronized page-level coverage, cleaned-up structure, aligned test case documentation, shared authenticated-page behavior, reusable product assertions, and final documentation sync after Login, Inventory, Product Details, and Cart coverage.

Recommended use:

* stronger portfolio presentation before checkout automation
* demonstration of structure cleanup and documentation discipline
* demonstration of traceability between manual test cases and automated tests
* demonstration of reusable framework components
* preparation for PR review and merge readiness

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
