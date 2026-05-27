# Roadmap

This document outlines the planned evolution of the QA automation framework.
The roadmap is organized into project phases to keep development focused, realistic, and aligned with portfolio goals.

## Phase 1: Foundation

Status: Completed

Phase 1 focused on establishing the technical foundation of the project.

Completed areas:

- repository structure
- Python virtual environment setup
- Playwright and Pytest setup
- basic smoke test execution
- pytest configuration
- Ruff configuration
- Black configuration
- isort configuration
- pre-commit hooks
- GitHub Actions CI pipeline
- CI artifact publishing
- HTML report generation
- screenshot capture on failure
- technical documentation structure
- Git workflow documentation
- README documentation hub

Phase 1 established the base required to start real QA automation work.

## Phase 2: Framework Foundation And Login Automation

Status: Current

Phase 2 focuses on building real automation framework capabilities and introducing QA-oriented test design.

Planned work:

- create login page test cases
- implement Page Object Model for login page
- introduce BasePage abstraction
- refactor smoke tests to use Page Object Model
- implement positive login scenarios
- implement negative login scenarios
- introduce centralized login test data
- add pytest parametrization
- improve login assertions
- improve failure diagnostics if needed

Main learning goals:

- Page Object Model
- test design
- test case review
- maintainable test structure
- reusable automation components
- CI-backed automation workflow

## Phase 3: Products, Cart, And Checkout Coverage

Status: Planned

Phase 3 will expand automation coverage beyond login.

Planned work:

- inventory page Page Object Model
- product list validation
- sorting validation
- add to cart scenarios
- remove from cart scenarios
- cart badge validation
- checkout form validation
- full purchase flow
- logout and session behavior

Main learning goals:

- multi-page flows
- stateful UI testing
- reusable fixtures
- test data strategy
- end-to-end scenario design

## Phase 4: Framework Maturity

Status: Planned

Phase 4 will improve framework scalability and maintainability.

Planned work:

- smoke and regression suite separation
- pytest marker strategy improvements
- parallel execution with pytest-xdist
- improved reporting structure
- Allure reporting integration
- environment-based configuration
- reusable assertion helpers
- logging utilities

Main learning goals:

- scalable test organization
- execution optimization
- advanced reporting
- maintainable framework design

## Phase 5: Advanced Extensions

Status: Future

Phase 5 will introduce advanced framework extensions.

Potential work:

- API testing layer using Requests
- hybrid UI + API scenarios
- Docker-based execution environment
- cross-browser execution strategy
- Selenium comparison module
- Jenkins pipeline integration
- test analytics and history tracking
- framework packaging as reusable template

## Strategic Vision

The long-term objective is to evolve this repository into a scalable, portfolio-ready QA automation framework that demonstrates:

- practical QA automation skills
- test design ability
- maintainable test architecture
- CI/CD workflow understanding
- modern Python tooling
- Playwright expertise
- readiness for junior and junior+/mid QA automation roles