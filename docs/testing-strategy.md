# Testing Strategy

This document defines the testing approach for the QA automation framework.

The current focus is UI automation testing for the Sauce Demo application using Playwright and Pytest. The project follows an iterative testing strategy: manual test design is created first, then selected scenarios are automated and gradually refactored into reusable framework components.

## System Under Test

* Application: Sauce Demo
* URL: `https://www.saucedemo.com/`

Sauce Demo is used as a stable training application for practicing UI automation, test design, Page Object Model, test data management, parametrization, CI validation, and framework development.

## Testing Approach

The project follows a progressive testing approach:

1. Identify test scenarios manually.
2. Write clear test cases.
3. Decide which scenarios should be automated.
4. Prepare test data when needed.
5. Implement automated tests using Playwright and Pytest.
6. Refactor repeated interactions into Page Object Model components.
7. Use fixtures to reduce repeated setup.
8. Use parametrization for repeated data-driven scenarios.
9. Categorize tests with pytest markers.
10. Validate tests locally and in CI.
11. Update documentation when test coverage changes.

This approach supports both QA thinking and automation engineering practice.

## Test Case Design

Test cases should be documented before or alongside automation work.

Recommended location:

```text
test_cases/
```

Each test case should include:

* test case ID
* title
* preconditions
* test data
* steps
* expected result
* test type
* priority
* automation candidate status
* automation status when implemented
* reference to automated test file when applicable

Current implemented test case documentation:

```text
test_cases/login-page.md
```

Login test cases use `TC-LOGIN-XXX` identifiers. These identifiers are also used in parametrized pytest output where practical.

## Current Test Coverage

The current automated test coverage focuses on the Sauce Demo login page and authentication-related behavior.

Implemented login coverage includes:

* successful login with valid credentials
* login with invalid username
* login with invalid password
* login with empty username
* login with empty password
* login with empty credentials
* locked out user login attempt
* login with invalid username and invalid password
* error message close behavior
* login page elements visibility
* password field masking validation
* login form submission with Enter key
* direct inventory page access without login

## Test Types

### Smoke Tests

Smoke tests validate the most critical application flows and should execute quickly.

Current examples:

* Sauce Demo page availability
* login page basic UI availability
* successful login with valid credentials

Future examples:

* product page availability
* basic cart operation
* basic checkout availability

### Regression Tests

Regression tests validate that existing functionality continues to work after changes.

Current examples:

* negative login scenarios
* empty credential validation
* locked out user validation
* error message behavior
* protected route access validation

Future examples:

* cart update behavior
* checkout validation
* sorting behavior
* full purchase flow

### UI Tests

UI tests validate user-facing browser behavior using Playwright.

Current examples:

* login form visibility
* password field configuration
* error message visibility
* error message close behavior
* inventory page visibility after login

### Positive Tests

Positive tests validate expected successful user behavior.

Current examples:

* valid user can log in successfully
* valid user can submit login form using Enter key

### Negative Tests

Negative tests validate error handling and invalid user behavior.

Current examples:

* invalid login
* empty required fields
* locked out user access
* direct protected route access without login

### Access Control Tests

Access control tests validate that protected application areas cannot be accessed without proper authentication.

Current example:

* unauthenticated user cannot directly access the inventory page

### End-To-End Tests

End-to-end tests will validate complete user journeys across multiple pages.

Current status:

* not fully implemented yet

Planned examples:

* add product to cart
* complete checkout flow
* verify order completion

## Test Design Principles

Automated tests should follow:

* Arrange / Act / Assert structure
* clear and descriptive test names
* stable assertions
* reusable Page Objects
* externalized test data where useful
* no hardcoded waits
* independent test execution
* readable failure output
* clear mapping to manual test cases where practical

Tests should focus on behavior, while page-specific UI interactions should be handled by Page Object classes.

## Page Object Model Strategy

Page Object Model is used to separate test logic from page interaction logic.

Current implementation:

```text
pages/login_page.py
```

The `LoginPage` object is responsible for:

* opening the login page
* filling username and password
* clicking the login button
* reading error messages
* closing error messages
* exposing login page UI locators where needed

Future Page Objects may include:

* InventoryPage
* CartPage
* CheckoutPage

Page Objects should be introduced when they reduce duplication and improve readability.

## Fixture Strategy

Fixtures are used to prepare reusable test setup.

Current fixture:

```text
opened_login_page
```

This fixture:

* creates a `LoginPage` instance
* opens the login page
* returns a ready-to-use Page Object for login-related tests

Fixtures should be added when setup logic becomes repeated across multiple tests.

Avoid creating too many fixtures too early. Fixture growth should follow real framework needs.

## Test Data Strategy

Test data should be separated from test logic when it improves readability, maintainability, or parametrization.

Current test data location:

```text
test_data/login_test_data.py
```

Current login test data includes:

* valid user cases
* invalid login cases
* empty credential cases
* locked out user cases
* expected error messages
* login-related URL values

Test data should support:

* clear test intent
* reduced hardcoding
* parametrized execution
* traceability to manual test case IDs

## Parametrization Strategy

Parametrization is used for repeated scenarios with the same test flow and different input data.

Current parametrized areas:

* invalid login scenarios
* empty credential scenarios
* locked out user scenario
* positive login user case
* selected single-case tests where test case ID visibility in `pytest -v` is desired

Parametrized test IDs should use manual test case IDs where practical, for example:

```text
TC-LOGIN-002
TC-LOGIN-003
TC-LOGIN-004
```

This improves traceability between:

* manual test cases
* automated tests
* terminal output
* CI logs
* test reports

## Marker Strategy

Pytest markers are used to categorize tests.

Current markers:

* `smoke`
* `regression`
* `ui`
* `api`
* `e2e`
* `positive`
* `negative`

Example marker commands:

```bash
pytest -m smoke -v
pytest -m regression -v
pytest -m positive -v
pytest -m negative -v
pytest -m "ui and smoke" -v
pytest -m "ui and regression" -v
```

Markers should be used consistently to support selective local and CI execution.

## Assertion Strategy

Assertions should be stable, meaningful, and focused on user-observable behavior where possible.

Current assertion examples:

* page title is correct
* URL matches expected page
* element is visible
* error message text matches expected value
* password input has `type="password"`
* protected route redirects unauthenticated user to login page

Use Playwright assertions for UI/browser state when possible because they include built-in waiting behavior.

Use plain Python assertions when comparing simple values, such as extracted text.

## Automation Priority

Automation should focus on:

* repeatable scenarios
* critical user flows
* regression-prone functionality
* stable application behavior
* high-value validation
* scenarios that benefit from CI execution

Not every possible case should be automated.

Some scenarios may remain manual or exploratory if automation would be unstable, low-value, or overly complex.

## Reporting And Debugging

Test execution generates:

* pytest console output
* HTML reports using pytest-html
* screenshots on failure
* CI artifacts uploaded by GitHub Actions

Generated reports and screenshots should not be committed to Git.

They should be used as:

* local debugging outputs
* CI artifacts
* failure analysis evidence

## Local Validation Strategy

Recommended full local validation:

```bash
ruff check .
black --check .
isort . --check-only
pytest -v
```

Recommended marker validation when login tests are changed:

```bash
pytest -m smoke -v
pytest -m regression -v
pytest -m positive -v
pytest -m negative -v
pytest -m "ui and smoke" -v
```

## CI Validation Strategy

GitHub Actions validates the project automatically on:

* pushes to `main`
* pushes to `develop`
* pull requests targeting `main`
* pull requests targeting `develop`
* manual workflow execution

The CI pipeline should validate:

* linting
* formatting
* import sorting
* test execution
* report generation
* artifact upload

Failing tests or quality checks should block merging.

## Future Improvements

Planned improvements:

* inventory and product page test coverage
* cart test coverage
* checkout flow automation
* logout and session behavior validation
* broader end-to-end scenarios
* API testing layer
* multi-browser execution
* smoke and regression CI job separation
* Allure reporting integration
* improved diagnostics and logs
* reusable assertion helpers
* environment-based configuration
