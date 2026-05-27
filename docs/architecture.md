# Architecture

This document describes the architecture direction of the QA automation framework.
The project is currently in an early framework foundation stage. The architecture is intentionally lightweight and will evolve iteratively as Page Object Model components, reusable fixtures, test data management, and additional test layers are introduced.

## Current Architecture Scope

The current framework foundation includes:

- Pytest-based test execution
- Playwright browser automation
- centralized pytest configuration
- CI execution with GitHub Actions
- code quality tooling
- HTML reporting and CI artifacts
- initial documentation structure

## Project Layers

The framework is organized into the following layers:

- `tests/`  
  Contains automated test cases.

- `pages/`  
  Reserved for Page Object Model classes that represent application pages and reusable UI interactions.

- `framework/`  
  Reserved for shared framework utilities, base classes, helpers, and reusable infrastructure code.

- `config/`  
  Reserved for framework and environment configuration.

- `test_data/`  
  Reserved for externalized test data.

- `reports/`  
  Stores generated reports, screenshots, and debugging artifacts. Runtime files are ignored by Git and published through CI artifacts when needed.

- `docs/`  
  Contains technical documentation related to architecture, workflow, testing strategy, tooling, and roadmap.

## Design Direction

The framework will follow a modular architecture where test logic is separated from page interaction logic.

Planned architecture improvements include:

- Page Object Model implementation
- BasePage abstraction
- reusable pytest fixtures
- centralized test data management
- marker-based test categorization
- improved reporting and diagnostics
- future API testing layer

## Architecture Principles

The framework should prioritize:

- readability
- maintainability
- clear separation of responsibilities
- reusable components
- stable and deterministic test execution
- CI/CD compatibility
- incremental improvement over unnecessary early complexity