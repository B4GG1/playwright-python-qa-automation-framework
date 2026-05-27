# Testing Strategy

This document defines the testing approach for the QA automation framework.
The current focus is UI automation testing for the Sauce Demo application using Playwright and Pytest.

## System Under Test

- Application: Sauce Demo
- URL: https://www.saucedemo.com/

Sauce Demo is used as a stable training application for practicing UI automation, test design, and framework development.

## Testing Approach

The project follows a progressive testing approach:

1. Identify test scenarios manually.
2. Write clear test cases.
3. Decide which scenarios should be automated.
4. Implement automated tests using Playwright and Pytest.
5. Refactor tests into reusable framework components.

## Test Case Design

Test cases should be documented before or alongside automation work.

Recommended location:

- `test_cases/`

Each test case should include:

- test case ID
- title
- preconditions
- steps
- expected result
- test type
- automation candidate status

## Test Types

### Smoke Tests

Smoke tests validate the most critical application flows and should execute quickly.

Examples:

- successful login
- product page availability
- basic cart operation

### Regression Tests

Regression tests validate that existing functionality continues to work after changes.

Examples:

- negative login scenarios
- cart update behavior
- checkout validation

### UI Tests

UI tests validate user-facing browser behavior using Playwright.

### Negative Tests

Negative tests validate error handling and invalid user behavior.

Examples:

- invalid login
- empty required fields
- locked user access

## Test Design Principles

Automated tests should follow:

- Arrange / Act / Assert structure
- clear test names
- stable assertions
- reusable page objects
- externalized test data where useful
- no hardcoded waits

## Automation Priority

Automation should focus on:

- repeatable scenarios
- critical user flows
- regression-prone functionality
- stable application behavior

Not every possible case should be automated.

## Reporting

Test execution generates:

- pytest console output
- HTML reports using pytest-html
- screenshots on failure
- CI artifacts uploaded by GitHub Actions

## Future Improvements

Planned improvements:

- pytest marker-based test selection
- Page Object Model expansion
- parametrized login scenarios
- inventory and cart test coverage
- checkout flow automation
- API testing layer