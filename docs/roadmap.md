# Roadmap

This document outlines the planned evolution of the QA automation framework.

The roadmap is organized into project phases to keep development focused, realistic, and aligned with portfolio goals.

The roadmap described below treats `main` as the stable portfolio branch and `develop` as the integration branch. When this document is read from `main`, the `develop` branch may already contain newer integration work that has not yet been promoted to the stable portfolio version.

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
* successful login scenario
* invalid credential validation scenarios
* required credential field validation
* locked out user validation
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

The Phase 2 checkpoint verified that the Login workstream was completed and that the project was ready for the next automation area.

Completed checkpoint scope:

* reviewed completed Login scope
* verified full local test execution
* verified marker-based test execution
* reviewed CI status after merge
* reviewed documentation
* cleaned up outdated project information
* confirmed Git status
* prepared high-level Phase 3 scope

This checkpoint allowed the project to move from Login-only automation into broader application coverage.

---

## Phase 3: Products, Cart, And Checkout Coverage

**Status:** Completed and promoted to `main` as stable portfolio snapshot

Phase 3 expanded automation coverage beyond Login into broader Sauce Demo application behavior.

The phase was split into smaller workstreams to keep the scope controlled and reviewable.

Completed work:

* Inventory Page Object Model
* Product Details Page Object Model
* Cart Page Object Model
* Checkout Page Objects
* shared authenticated-page behavior through `AppPage`
* reusable product assertion helpers
* checkout-related assertion support
* product list validation
* product sorting validation
* Product Details validation
* Inventory-side Product Details navigation
* Cart functionality tests
* cart badge validation
* Cart page validation
* Cart product content validation
* Remove validation from Inventory, Product Details, and Cart
* Continue Shopping navigation validation
* Cart state persistence after logout and re-login
* Cart-owned navigation to Checkout Information
* Checkout Information form validation
* Checkout Information error handling
* Checkout Overview validation
* Checkout Overview price summary validation
* Product Details navigation from Checkout Overview
* checkout completion flow
* order confirmation validation
* protected checkout route access validation
* manual test cases for Login, Inventory, Product Details, Cart, and Checkout
* test data expansion for product and checkout scenarios
* documentation synchronization after Checkout workstream
* PR review, CI validation, and squash merge into `develop`
* promotion of the completed Phase 3 state to `main` as the stable portfolio snapshot

Main learning goals completed:

* multi-page flows
* stateful UI testing
* reusable fixtures
* reusable assertion helpers
* test data strategy
* independent E2E checkpoint design
* Page Object interaction between multiple pages
* clearer Smoke and Regression separation
* scope control between Cart and Checkout behavior
* documentation synchronization after structural refactors and workstream completion
* stable portfolio promotion workflow from `develop` to `main`

Phase 3 is complete after the Checkout workstream was validated, synchronized, reviewed in PR #6, passed CI, squash-merged into `develop`, and promoted to `main` as the stable Phase 3 portfolio snapshot.

---

## Phase 3A: Inventory And Products Automation Workstream

**Status:** Completed

Phase 3A focused on Inventory and product-related validation before Cart and Checkout scenarios.

Completed areas:

* Inventory and Products manual test cases
* `InventoryPage` Page Object Model
* `ProductDetailsPage` Page Object Model
* reusable logged-in Inventory fixture
* centralized product test data
* Inventory visibility validation
* product list validation
* product card content validation
* Product Details navigation from product name
* Product Details navigation from product image
* return from Product Details to Inventory
* product sorting by name A to Z
* product sorting by name Z to A
* product sorting by price low to high
* product sorting by price high to low
* Sorting marker registration
* local validation of Inventory tests
* full local test suite validation
* test case coverage mapping
* documentation updates

Completed review scope:

* reviewed completed Inventory and Products scope
* verified test case coverage
* verified Page Object structure
* verified fixture usage
* verified test data consistency
* verified marker usage
* reviewed documentation updates
* confirmed cleanup needs

Phase 3A completed the Inventory and Product validation layer required before Cart automation.

---

## Phase 3B: Cart Automation Workstream

**Status:** Completed

Phase 3B focused on Cart-related behavior.

Completed areas:

* Cart-related manual test cases
* `CartPage` Page Object Model
* Cart page availability validation
* empty Cart state validation
* Add to cart from Inventory
* Cart navigation
* cart badge visibility validation
* cart badge count validation
* Cart product visibility validation
* Cart product content validation
* Remove behavior from Cart
* cart badge removal after removing the last product
* Continue Shopping navigation from Cart to Inventory
* Cart state persistence after logout and re-login
* Product Details-side Add to cart and Remove behavior
* reuse of centralized product test data for Cart scenarios
* reuse of valid user data for persistence scenarios
* Cart test case coverage mapping
* documentation updates

Completed stabilization scope:

* reviewed completed Cart workstream files
* verified Cart test cases against implemented automation
* verified `TC-CART` IDs used in tests
* verified Page Object responsibility boundaries
* verified that tests do not duplicate selectors unnecessarily
* confirmed detailed Checkout behavior remains outside Cart scope
* reviewed README and technical docs
* ran Cart-specific validation
* ran full local test suite
* ran quality checks
* confirmed Git status and cleanup needs
* prepared the workstream for the next project step

Phase 3B completed Cart behavior automation while keeping detailed Checkout behavior outside Cart scope.

---

## Phase 3C: Structure Cleanup, Coverage Completion, And Documentation Sync

**Status:** Completed

Phase 3C focused on final cleanup after the Login, Inventory, Product Details, and Cart page-level coverage work.

The goal of this workstream was to align project structure, test coverage, Page Objects, fixtures, test case files, and documentation before continuing into Checkout automation.

Completed areas:

* one automated test module per covered page area
* one manual test case file per covered page area
* Login, Inventory, Product Details, and Cart test case coverage synchronization
* missing page-level coverage completion after Cart workstream
* Page Object responsibility review
* `BasePage` and `AppPage` structure review
* authenticated shared behavior ownership review
* reusable product assertion helper extraction
* fixture naming and reuse review
* navigation return type review
* TC coverage mapping review
* test case metadata cleanup
* README and technical documentation synchronization
* roadmap readiness review for the Checkout workstream
* local quality validation
* full Pytest validation
* PR readiness confirmation or blocker listing

Phase 3C prepared the framework structure for the dedicated Checkout automation workstream.

---

## Phase 3D: Checkout Automation Workstream

**Status:** Completed and merged into `develop`

Phase 3D focused on Checkout behavior after Inventory, Product Details, and Cart coverage.

The workstream kept responsibility boundaries clear:

* Cart coverage owns navigation from Cart to Checkout Information.
* Checkout coverage owns Checkout Information, Checkout Overview, and Checkout Complete behavior.
* Login coverage owns protected Checkout route access validation.

Completed areas:

* Checkout-related manual test cases
* Checkout Page Objects
* Checkout Information form visibility validation
* Checkout required customer field validation
* Checkout Information error message validation
* Checkout Information input error icon validation
* Checkout Information error close behavior
* Checkout Information submission with valid data
* Checkout Information cancellation back to Cart
* Checkout Overview selected product validation
* Checkout Overview all-products validation
* Checkout Overview one-product price summary validation
* Checkout Overview multiple-products price summary validation
* Checkout Overview cancellation back to Inventory
* Product Details navigation from Checkout Overview item name
* all-products Product Details navigation from Checkout Overview
* Finish validation
* Checkout Complete confirmation validation
* Back Home navigation after order completion
* protected Checkout Information route validation
* protected Checkout Overview route validation
* protected Checkout Complete route validation
* Checkout test data
* Checkout fixtures
* Checkout test case coverage mapping
* documentation synchronization after Checkout implementation
* PR creation from `feature/checkout` into `develop`
* CI validation on PR #6
* squash merge into `develop`

Phase 3D is complete after AQA-0082 final validation and documentation sync, AQA-0083 PR review, successful CI, and squash merge into `develop`.

---

## Phase 3 Completion Review

**Status:** Completed through AQA-0082 and AQA-0083

A separate large Phase 3 checkpoint task was not required after the Checkout merge because the practical checkpoint scope was already covered by:

* AQA-0082 — Checkout workstream final validation and documentation sync
* AQA-0083 — PR creation, PR diff review, CI verification, squash merge into `develop`, local update, and branch cleanup

Covered completion scope:

* reviewed completed Phase 3 Checkout scope
* validated Checkout test coverage
* confirmed full local test suite before PR
* confirmed quality checks before PR
* verified CI status on PR #6
* reviewed and synchronized documentation updates
* reviewed Git status and cleanup needs
* confirmed readiness to move toward Phase 4 planning
* confirmed readiness for stable Phase 3 portfolio promotion to `main`

The next project direction is Phase 4 Framework Maturity.

---

## Phase 3 Portfolio Promotion

**Status:** Completed

Phase 3 portfolio promotion moved the completed and validated Phase 3 project state from `develop` to `main`.

The purpose of this promotion was to make `main` the polished portfolio branch suitable for recruiters, technical reviewers, and CV/GitHub profile links.

Completed promotion scope:

* confirmed Phase 3 page-level automation coverage
* confirmed Login, Inventory, Product Details, Cart, and Checkout documentation synchronization
* confirmed implemented features were separated from planned future features
* removed stale Checkout-finalization and PR-readiness wording
* confirmed generated reports, screenshots, cache files, and virtual environment files were not tracked
* validated the promotion Pull Request through CI
* squash-merged the stable Phase 3 snapshot into `main`

After promotion, future implementation and framework maturity work continues from `develop`.

---

## Phase 4: Framework Maturity

**Status:** In Progress

Phase 4 focuses on improving the scalability, maintainability, execution strategy, reporting, configuration, and diagnostics of the existing automation framework.

Unlike Phase 3, this phase does not primarily expand application feature coverage. Its purpose is to mature the framework built around the completed Login, Inventory, Product Details, Cart, and Checkout automation.

Phase 4 is divided into focused workstreams so that framework improvements can be introduced and validated incrementally.

Planned workstreams:

* Phase 4A — Marker And Suite Strategy
* Phase 4B — CI Execution Strategy
* Phase 4C — Parallel Execution
* Phase 4D — Reporting Upgrade
* Phase 4E — Runtime Configuration
* Phase 4F — Diagnostics And Fixture Cleanup
* Phase 4 Checkpoint

Main learning goals:

* scalable test organization
* predictable marker-based execution
* smoke and regression suite separation
* execution optimization
* CI execution strategy
* parallel test execution
* advanced reporting
* environment-based framework configuration
* stronger failure diagnostics
* maintainable fixture organization
* stronger CI/test feedback loops
* maintainable framework design

---

## Phase 4A: Marker And Suite Strategy

**Status:** In Progress

Phase 4A focuses on normalizing pytest marker semantics and establishing a predictable test-suite execution strategy before CI execution is further expanded.

The goal is to make marker-based execution intentional, maintainable, and suitable for later CI job separation and framework scaling.

Completed work:

* AQA-0084 — Audit Current Pytest Marker Usage
* AQA-0085 — Normalize Pytest Marker Definitions And Usage

Current marker strategy work includes:

* audit of marker definitions in `pytest.ini`
* audit of marker assignments across all automated test modules
* normalization of Smoke and Regression semantics
* normalization of UI marker semantics
* normalization of Navigation marker semantics
* clarification of Security marker usage
* preservation of Sorting as a dedicated executable category
* clarification of E2E execution semantics
* removal of Positive and Negative as executable pytest markers
* removal of the unused API executable marker from the current UI automation suite
* explicit marker assignment through `@pytest.mark.*` decorators
* no dynamic marker assignment through `conftest.py`
* synchronization of affected test case coverage and automation metadata

Remaining Phase 4A work:

* AQA-0086 — Document Marker And Suite Execution Strategy
* AQA-0087 — Validate Phase 4A Marker And Suite Strategy

Phase 4A prepares the framework for CI suite separation without introducing Phase 4B CI workflow changes prematurely.

---

## Phase 4B: CI Execution Strategy

**Status:** Planned

Phase 4B will improve GitHub Actions execution so that CI provides clearer and faster feedback for different test scopes.

Planned areas:

* review the current GitHub Actions workflow
* separate fast quality checks from browser test execution where useful
* introduce CI execution for selected marker-based suites
* support dedicated Smoke and Regression execution
* keep full-suite execution available as final validation
* maintain useful CI artifacts and reports
* improve CI job naming and feedback clarity
* avoid unnecessary workflow complexity for portfolio scope

Phase 4B will use the marker strategy established during Phase 4A.

---

## Phase 4C: Parallel Execution

**Status:** Planned

Phase 4C will introduce and validate parallel pytest execution using `pytest-xdist`.

Planned areas:

* add `pytest-xdist`
* validate test independence under parallel execution
* identify scenarios affected by shared Sauce Demo application state
* define safe parallel execution commands
* verify compatibility with existing fixtures
* verify compatibility with reporting and failure artifacts
* document any test groups that should remain sequential

The goal is execution optimization without sacrificing test reliability.

---

## Phase 4D: Reporting Upgrade

**Status:** Planned

Phase 4D will improve test reporting and failure artifacts.

Planned areas:

* review the current HTML reporting structure
* improve organization of generated reports
* improve screenshot, trace, video, or other failure artifact handling where useful
* improve CI artifact naming and accessibility
* integrate Allure reporting
* generate Allure result data locally
* integrate useful Allure output with CI where appropriate
* document reporting commands and artifact locations

The goal is to make test results easier to review locally, in CI, and during portfolio presentation.

---

## Phase 4E: Runtime Configuration

**Status:** Planned

Phase 4E will introduce environment-based runtime configuration.

Planned areas may include:

* base URL configuration
* browser selection
* headed or headless execution mode
* timeout configuration
* screenshot policy
* trace policy
* video policy
* sensible local defaults
* environment variable handling
* documented configuration usage

The goal is to reduce hardcoded runtime assumptions and make framework execution more flexible.

---

## Phase 4F: Diagnostics And Fixture Cleanup

**Status:** Planned

Phase 4F will review framework diagnostics and fixture organization after the previous maturity improvements.

Planned areas:

* introduce or improve lightweight logging utilities
* expose useful runtime information during test execution
* improve failed-test diagnostics
* review screenshot and trace diagnostics
* review current fixture structure
* identify fixture duplication or unclear responsibility
* reorganize fixtures only where the current structure justifies it
* keep fixture names explicit and scenario-oriented
* avoid refactoring solely for structural complexity

This workstream will provide final framework cleanup before the Phase 4 checkpoint.

---

## Phase 4 Checkpoint

**Status:** Planned

After Phase 4 implementation, a checkpoint will confirm whether the framework maturity work is complete and whether the project is ready for Phase 5 Advanced Extensions.

Checkpoint scope:

* review completed Phase 4A–4F workstreams
* verify marker and suite execution strategy
* verify CI execution strategy
* verify parallel execution behavior
* verify reporting and failure artifacts
* verify environment-based configuration
* verify diagnostics and fixture organization
* run required test and quality validation
* review documentation synchronization
* check repository cleanup and Git status
* confirm readiness for broader portfolio presentation
* confirm readiness for Phase 5 Advanced Extensions

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

The project contains a complete Login automation workstream and can be used as an early proof of structured QA automation learning.

Recommended use:

* internal review
* selective portfolio sharing
* preparation for CV/GitHub profile updates

### After Phase 3A

The project contains Login coverage plus Inventory and Product validation.

Recommended use:

* stronger GitHub portfolio presentation
* early QA Automation application support
* demonstration of Page Object Model beyond a single page
* demonstration of product data validation and Sorting tests

### After Phase 3B

The project contains Login, Inventory, Product Details, and Cart automation coverage.

Recommended use:

* stronger portfolio presentation than Login/Inventory-only state
* demonstration of stateful UI testing
* demonstration of multi-page Page Object interaction
* demonstration of Cart behavior validation without mixing detailed Checkout scope
* continued preparation for regular QA Automation applications

### After Phase 3C

The project contains synchronized page-level coverage, cleaned-up structure, aligned test case documentation, shared authenticated-page behavior, reusable product assertions, and final documentation synchronization after Login, Inventory, Product Details, and Cart coverage.

Recommended use:

* stronger portfolio presentation before Checkout automation
* demonstration of structure cleanup and documentation discipline
* demonstration of traceability between manual test cases and automated tests
* demonstration of reusable framework components
* preparation for Checkout automation

### After Phase 3D

The project contains Checkout automation in addition to Login, Inventory, Product Details, and Cart coverage.

Recommended use:

* stronger regular QA Automation application support
* demonstration of realistic multi-step e-commerce UI automation
* demonstration of form validation, Overview validation, and order completion checks
* demonstration of clear Page Object boundaries across multi-page workflows
* demonstration of documentation synchronization after feature workstream completion

### After Phase 3 Portfolio Promotion

The project has a stable Phase 3 portfolio snapshot available on `main`.

Recommended use:

* regular QA Automation applications
* GitHub portfolio presentation
* CV project section update
* GitHub Profile README project link
* recruiter-facing repository link

### After Phase 4

The project should be close to a mature portfolio-ready QA automation framework with structured execution suites, improved CI feedback, parallel execution support, advanced reporting, runtime configuration, and stronger diagnostics.

Recommended use:

* stronger Junior / Junior+ QA Automation applications
* Technical QA applications
* broader recruiter-facing portfolio presentation
* demonstration of framework maturity beyond feature-level test automation
* demonstration of scalable test execution and reporting strategy

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
* ability to design independent marker-based suites
* ability to design independent E2E journey checkpoints
* ability to keep scope controlled across workstreams
* ability to maintain documentation alongside automation
* stable Git and Pull Request workflow
* readiness for junior and junior+/mid QA automation roles
