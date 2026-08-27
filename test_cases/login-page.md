# Login Page — Test Cases

## Overview

This document contains manual test cases for the Sauce Demo login page.
The goal of this document is to define login-related test scenarios before and alongside automation implementation.

## Test Case Overview And Automation Coverage

| Test Case ID                                                                                        | Scenario                                                            | Type            | Priority | Automation Status | Automated In               |
|-----------------------------------------------------------------------------------------------------|---------------------------------------------------------------------|-----------------|----------|-------------------|----------------------------|
| [TC-LOGIN-001](#tc-login-001--successful-login-with-valid-credentials)                              | Successful login with valid credentials                             | Smoke / E2E     | High     | Automated         | `tests/test_login_page.py` |
| [TC-LOGIN-002](#tc-login-002--login-with-invalid-username)                                          | Login with invalid username                                         | Smoke / UI      | Medium   | Automated         | `tests/test_login_page.py` |
| [TC-LOGIN-003](#tc-login-003--login-with-invalid-password)                                          | Login with invalid password                                         | Regression / UI | Medium   | Automated         | `tests/test_login_page.py` |
| [TC-LOGIN-004](#tc-login-004--login-with-empty-username)                                            | Login with empty username                                           | Regression / UI | Medium   | Automated         | `tests/test_login_page.py` |
| [TC-LOGIN-005](#tc-login-005--login-with-empty-password)                                            | Login with empty password                                           | Regression / UI | Medium   | Automated         | `tests/test_login_page.py` |
| [TC-LOGIN-006](#tc-login-006--login-with-empty-credentials)                                         | Login with empty credentials                                        | Regression / UI | Medium   | Automated         | `tests/test_login_page.py` |
| [TC-LOGIN-007](#tc-login-007--locked-out-user-login-attempt)                                        | Locked out user login attempt                                       | Regression / UI | Medium   | Automated         | `tests/test_login_page.py` |
| [TC-LOGIN-008](#tc-login-008--login-with-invalid-username-and-invalid-password)                     | Login with invalid username and invalid password                    | Regression / UI | Medium   | Automated         | `tests/test_login_page.py` |
| [TC-LOGIN-009](#tc-login-009--error-message-can-be-closed-after-failed-login)                       | Error message can be closed after failed login                      | Smoke / UI      | Medium   | Automated         | `tests/test_login_page.py` |
| [TC-LOGIN-010](#tc-login-010--login-page-elements-are-visible)                                      | Login page elements are visible                                     | Regression / UI | High     | Automated         | `tests/test_login_page.py` |
| [TC-LOGIN-011](#tc-login-011--password-field-masks-entered-characters)                              | Password field masks entered characters                             | UI              | Medium   | Automated         | `tests/test_login_page.py` |
| [TC-LOGIN-012](#tc-login-012--login-form-can-be-submitted-with-enter-key)                           | Login form can be submitted with Enter key                          | UI              | Medium   | Automated         | `tests/test_login_page.py` |
| [TC-LOGIN-013](#tc-login-013--direct-access-to-inventory-page-without-login-is-blocked)             | Direct access to inventory page without login is blocked            | Security        | High     | Automated         | `tests/test_login_page.py` |
| [TC-LOGIN-014](#tc-login-014--direct-access-to-cart-page-without-login-is-blocked)                  | Direct access to cart page without login is blocked                 | Security        | High     | Automated         | `tests/test_login_page.py` |
| [TC-LOGIN-015](#tc-login-015--direct-access-to-item-page-without-login-is-blocked)                  | Direct access to item page without login is blocked                 | Security        | High     | Automated         | `tests/test_login_page.py` |
| [TC-LOGIN-016](#tc-login-016--input-error-icons-are-displayed-after-failed-login)                   | Input error icons are displayed after failed login                  | Regression / UI | Medium   | Automated         | `tests/test_login_page.py` |
| [TC-LOGIN-017](#tc-login-017--direct-access-to-check-out-information-page-without-login-is-blocked) | Direct access to checkout information page without login is blocked | Security        | High     | Automated         | `tests/test_login_page.py` |
| [TC-LOGIN-018](#tc-login-018--direct-access-to-check-out-overview-page-without-login-is-blocked)    | Direct access to checkout overview page without login is blocked    | Security        | High     | Automated         | `tests/test_login_page.py` |
| [TC-LOGIN-019](#tc-login-019--direct-access-to-check-out-complete-page-without-login-is-blocked)    | Direct access to checkout complete page without login is blocked    | Security        | High     | Automated         | `tests/test_login_page.py` |

---

## Test Cases

### TC-LOGIN-001 — Successful login with valid credentials

**Type:** Smoke / E2E\
**Priority:** High\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_login_page.py`

**Preconditions:**

* User is on the login page.

**Test Data:**

* Username: `standard_user`
* Password: `secret_sauce`

**Steps:**

1. Enter valid username.
2. Enter valid password.
3. Click the Login button.

**Expected Result:**

* User is redirected to the inventory page.
* Product list is visible.

**Notes:**

* This is the main representative successful login scenario.
* Broader valid-user regression coverage is intentionally reserved for later expansion.

---

### TC-LOGIN-002 — Login with invalid username

**Type:** Smoke / UI\
**Priority:** Medium\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_login_page.py`

**Preconditions:**

* User is on the login page.

**Test Data:**

* Username: `invalid_user`
* Password: `secret_sauce`

**Steps:**

1. Enter invalid username.
2. Enter valid password.
3. Click the Login button.

**Expected Result:**

* User remains on the login page.
* Error message is displayed.
* Login and password fields are visually marked as invalid.
* Error icons are displayed for both login inputs.

**Expected Error Message:** `Epic sadface: Username and password do not match any user in this service`

**Notes:**

* This is the representative smoke scenario for failed authentication.
* The automated test also validates the visible failed-login UI state.

---

### TC-LOGIN-003 — Login with invalid password

**Type:** Regression / UI\
**Priority:** Medium\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_login_page.py`

**Preconditions:**

* User is on the login page.

**Test Data:**

* Username: `standard_user`
* Password: `invalid_password`

**Steps:**

1. Enter valid username.
2. Enter invalid password.
3. Click the Login button.

**Expected Result:**

* User remains on the login page.
* Error message is displayed.
* Login and password fields are visually marked as invalid.
* Error icons are displayed for both login inputs.

**Expected Error Message:** `Epic sadface: Username and password do not match any user in this service`

**Notes:**

* This scenario extends failed-authentication coverage with an invalid-password variant.

---

### TC-LOGIN-004 — Login with empty username

**Type:** Regression / UI\
**Priority:** Medium\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_login_page.py`

**Preconditions:**

* User is on the login page.

**Test Data:**

* Username: empty
* Password: `secret_sauce`

**Steps:**

1. Leave username field empty.
2. Enter valid password.
3. Click the Login button.

**Expected Result:**

* User remains on the login page.
* Error message is displayed.
* Login and password fields are visually marked as invalid.
* Error icons are displayed for both login inputs.

**Expected Error Message:** `Epic sadface: Username is required`

**Notes:**

* This scenario validates required username field behavior.

---

### TC-LOGIN-005 — Login with empty password

**Type:** Regression / UI\
**Priority:** Medium\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_login_page.py`

**Preconditions:**

* User is on the login page.

**Test Data:**

* Username: `standard_user`
* Password: empty

**Steps:**

1. Enter valid username.
2. Leave password field empty.
3. Click the Login button.

**Expected Result:**

* User remains on the login page.
* Error message is displayed.
* Login and password fields are visually marked as invalid.
* Error icons are displayed for both login inputs.

**Expected Error Message:** `Epic sadface: Password is required`

**Notes:**

* This scenario validates required password field behavior.

---

### TC-LOGIN-006 — Login with empty credentials

**Type:** Regression / UI\
**Priority:** Medium\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_login_page.py`

**Preconditions:**

* User is on the login page.

**Test Data:**

* Username: empty
* Password: empty

**Steps:**

1. Leave username field empty.
2. Leave password field empty.
3. Click the Login button.

**Expected Result:**

* User remains on the login page.
* Error message is displayed.
* Login and password fields are visually marked as invalid.
* Error icons are displayed for both login inputs.

**Expected Error Message:** `Epic sadface: Username is required`

**Notes:**

* When both fields are empty, the username validation message is displayed first.

---

### TC-LOGIN-007 — Locked out user login attempt

**Type:** Regression / UI\
**Priority:** Medium\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_login_page.py`

**Preconditions:**

* User is on the login page.

**Test Data:**

* Username: `locked_out_user`
* Password: `secret_sauce`

**Steps:**

1. Enter locked out user username.
2. Enter valid password.
3. Click the Login button.

**Expected Result:**

* User remains on the login page.
* Error message is displayed.
* Login and password fields are visually marked as invalid.
* Error icons are displayed for both login inputs.

**Expected Error Message:** `Epic sadface: Sorry, this user has been locked out.`

**Notes:**

* This scenario validates application behavior for a blocked user account.
* It also validates the corresponding user-facing failed-login UI state.

---

### TC-LOGIN-008 — Login with invalid username and invalid password

**Type:** Regression / UI\
**Priority:** Medium\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_login_page.py`

**Preconditions:**

* User is on the login page.

**Test Data:**

* Username: `invalid_user`
* Password: `invalid_sauce`

**Steps:**

1. Enter invalid username.
2. Enter invalid password.
3. Click the Login button.

**Expected Result:**

* User remains on the login page.
* Error message is displayed.
* Login and password fields are visually marked as invalid.
* Error icons are displayed for both login inputs.

**Expected Error Message:** `Epic sadface: Username and password do not match any user in this service`

**Notes:**

* This scenario extends failed-authentication coverage with both credentials invalid.

---

### TC-LOGIN-009 — Error message can be closed after failed login

**Type:** Smoke / UI\
**Priority:** Medium\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_login_page.py`

**Preconditions:**

* User is on the login page.
* Failed login attempt has triggered an error message.

**Test Data:**

* Username: `invalid_user`
* Password: `secret_sauce`

**Steps:**

1. Enter invalid username.
2. Enter valid password.
3. Click the Login button.
4. Verify that the error message is visible.
5. Click the close button on the error message.

**Expected Result:**

* User remains on the login page.
* Error message is visible after failed login.
* Error message disappears after clicking the close button.

**Notes:**

* This is the representative smoke validation for error-message visibility and direct UI interaction.

---

### TC-LOGIN-010 — Login page elements are visible

**Type:** Regression / UI\
**Priority:** High\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_login_page.py`

**Preconditions:**

* User opens the Sauce Demo login page.

**Test Data:**

* Username: N/A
* Password: N/A

**Steps:**

1. Open the login page.
2. Observe the login form.

**Expected Result:**

* Username input field is visible.
* Password input field is visible.
* Login button is visible.
* Login page credential information section is visible.

**Notes:**

* This scenario performs detailed UI validation of individual login page elements.
* General login-page availability is covered by the representative UI smoke validation.

---

### TC-LOGIN-011 — Password field masks entered characters

**Type:** UI\
**Priority:** Medium\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_login_page.py`

**Preconditions:**

* User is on the login page.

**Test Data:**

* Username: N/A
* Password: `secret_sauce`

**Steps:**

1. Click the password field.
2. Enter password text.

**Expected Result:**

* Password field is visible.
* Password field is configured as a password input.
* Entered password is not displayed as plain text to the user.

**Automation Note:**

* Automated validation verifies the technical masking mechanism by checking that the password input uses `type="password"`.
* Visual representation of masked characters is browser-native behavior and is not validated by screenshot comparison.
* The input value may still be technically readable by automation tools, but the field configuration ensures browser-level visual masking.

---

### TC-LOGIN-012 — Login form can be submitted with Enter key

**Type:** UI\
**Priority:** Medium\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_login_page.py`

**Preconditions:**

* User is on the login page.

**Test Data:**

* Username: `standard_user`
* Password: `secret_sauce`

**Steps:**

1. Enter valid username.
2. Enter valid password.
3. Press Enter while focus is inside the password field.

**Expected Result:**

* Login form is submitted.
* User is redirected to the inventory page.
* Product list is visible.

**Notes:**

* This test validates keyboard-based form submission.
* The scenario is classified as UI because the tested behavior is direct interaction with the login form.
* The Login → Inventory transition is intentionally not classified as Navigation.

---

### TC-LOGIN-013 — Direct access to inventory page without login is blocked

**Type:** Security\
**Priority:** High\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_login_page.py`

**Preconditions:**

* User is not logged in.
* Browser session does not contain an active authenticated state.

**Test Data:**

* Username: N/A
* Password: N/A
* Direct URL: `https://www.saucedemo.com/inventory.html`

**Steps:**

1. Open the inventory page URL directly without logging in.

**Expected Result:**

* User is redirected to the login page.
* Inventory page is not accessible.
* Error message informs the user that login is required.

**Expected Error Message:** `Epic sadface: You can only access '/inventory.html' when you are logged in.`

**Notes:**

* This scenario validates access control for a protected application page.
* The automated test uses a fresh browser context provided by Playwright.

---

### TC-LOGIN-014 — Direct access to cart page without login is blocked

**Type:** Security\
**Priority:** High\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_login_page.py`

**Preconditions:**

* User is not logged in.
* Browser session does not contain an active authenticated state.

**Test Data:**

* Username: N/A
* Password: N/A
* Direct URL: `https://www.saucedemo.com/cart.html`

**Steps:**

1. Open the cart page URL directly without logging in.

**Expected Result:**

* User is redirected to the login page.
* Cart page is not accessible.
* Error message informs the user that login is required.

**Expected Error Message:** `Epic sadface: You can only access '/cart.html' when you are logged in.`

**Notes:**

* This scenario validates access control for a protected application page.
* The automated test uses a fresh browser context provided by Playwright.

---

### TC-LOGIN-015 — Direct access to item page without login is blocked

**Type:** Security\
**Priority:** High\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_login_page.py`

**Preconditions:**

* User is not logged in.
* Browser session does not contain an active authenticated state.

**Test Data:**

* Username: N/A
* Password: N/A
* Direct URL: `https://www.saucedemo.com/inventory-item.html?id=4`
* Example product: `Sauce Labs Backpack`

**Steps:**

1. Open the item page URL directly without logging in.

**Expected Result:**

* User is redirected to the login page.
* Item page is not accessible.
* Error message informs the user that login is required.

**Expected Error Message:** `Epic sadface: You can only access '/inventory-item.html' when you are logged in.`

**Notes:**

* This scenario validates access control for a protected application page.
* The automated test uses a fresh browser context provided by Playwright.

---

### TC-LOGIN-016 — Input error icons are displayed after failed login

**Type:** Regression / UI\
**Priority:** Medium\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_login_page.py`

**Preconditions:**

* User is on the login page.
* A failed login attempt is performed.

**Test Data:**

* Failed-login data from TC-LOGIN-002 through TC-LOGIN-008.

**Steps:**

1. Submit the login form using invalid, missing, or blocked-user credentials.
2. Observe the username input field.
3. Observe the password input field.

**Expected Result:**

* User remains on the login page.
* Username input field displays an error icon.
* Password input field displays an error icon.

**Notes:**

* This validation is no longer implemented as a standalone pytest test function.
* Error-icon validation is executed as shared assertion coverage by the automated failed-login scenarios TC-LOGIN-002 through TC-LOGIN-008.
* Shared validation is implemented through `assert_failed_login_input_error_icons_are_displayed()` in `framework/assertions/product_assertions.py`.
* `tests/test_login_page.py` remains the primary automated test module for this coverage.
* TC-LOGIN-016 may be redefined in a later task for broader valid-login regression coverage.

---

### TC-LOGIN-017 — Direct access to check out information page without login is blocked

**Type:** Security\
**Priority:** High\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_login_page.py`

**Preconditions:**

* User is not logged in.
* Browser session does not contain an active authenticated state.

**Test Data:**

* Username: N/A
* Password: N/A
* Direct URL: `https://www.saucedemo.com/checkout-step-one.html`

**Steps:**

1. Open the checkout information page URL directly without logging in.

**Expected Result:**

* User is redirected to the login page.
* Checkout information page is not accessible.
* Error message informs the user that login is required.

**Expected Error Message:** `Epic sadface: You can only access '/checkout-step-one.html' when you are logged in.`

**Notes:**

* This scenario validates access control for checkout step one.
* The automated test uses a fresh browser context so no active authenticated state is present.

---

### TC-LOGIN-018 — Direct access to check out overview page without login is blocked

**Type:** Security\
**Priority:** High\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_login_page.py`

**Preconditions:**

* User is not logged in.
* Browser session does not contain an active authenticated state.

**Test Data:**

* Username: N/A
* Password: N/A
* Direct URL: `https://www.saucedemo.com/checkout-step-two.html`

**Steps:**

1. Open the checkout overview page URL directly without logging in.

**Expected Result:**

* User is redirected to the login page.
* Checkout overview page is not accessible.
* Error message informs the user that login is required.

**Expected Error Message:** `Epic sadface: You can only access '/checkout-step-two.html' when you are logged in.`

**Notes:**

* This scenario validates access control for checkout step two.
* The automated test uses a fresh browser context so no active authenticated state is present.

---

### TC-LOGIN-019 — Direct access to check out complete page without login is blocked

**Type:** Security\
**Priority:** High\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_login_page.py`

**Preconditions:**

* User is not logged in.
* Browser session does not contain an active authenticated state.

**Test Data:**

* Username: N/A
* Password: N/A
* Direct URL: `https://www.saucedemo.com/checkout-complete.html`

**Steps:**

1. Open the checkout complete page URL directly without logging in.

**Expected Result:**

* User is redirected to the login page.
* Checkout complete page is not accessible.
* Error message informs the user that login is required.

**Expected Error Message:** `Epic sadface: You can only access '/checkout-complete.html' when you are logged in.`

**Notes:**

* This scenario validates access control for checkout complete page.
* The automated test uses a fresh browser context so no active authenticated state is present.