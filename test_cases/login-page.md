# Login Page — Test Cases

## Overview

This document contains manual test cases for the Sauce Demo login page.
The goal of this document is to define login-related test scenarios before and alongside automation implementation.

## Test Case Overview And Automation Coverage

| Test Case ID                                                                            | Scenario                                                 | Type                       | Priority | Automation Status | Automated In               |
|-----------------------------------------------------------------------------------------|----------------------------------------------------------|----------------------------|----------|-------------------|----------------------------|
| [TC-LOGIN-001](#tc-login-001--successful-login-with-valid-credentials)                  | Successful login with valid credentials                  | Smoke / Positive           | High     | Automated         | `tests/test_login_page.py` |
| [TC-LOGIN-002](#tc-login-002--login-with-invalid-username)                              | Login with invalid username                              | Regression / Negative      | Medium   | Automated         | `tests/test_login_page.py` |
| [TC-LOGIN-003](#tc-login-003--login-with-invalid-password)                              | Login with invalid password                              | Regression / Negative      | Medium   | Automated         | `tests/test_login_page.py` |
| [TC-LOGIN-004](#tc-login-004--login-with-empty-username)                                | Login with empty username                                | Regression / Negative      | Medium   | Automated         | `tests/test_login_page.py` |
| [TC-LOGIN-005](#tc-login-005--login-with-empty-password)                                | Login with empty password                                | Regression / Negative      | Medium   | Automated         | `tests/test_login_page.py` |
| [TC-LOGIN-006](#tc-login-006--login-with-empty-credentials)                             | Login with empty credentials                             | Regression / Negative      | Medium   | Automated         | `tests/test_login_page.py` |
| [TC-LOGIN-007](#tc-login-007--locked-out-user-login-attempt)                            | Locked out user login attempt                            | Regression / Negative      | Medium   | Automated         | `tests/test_login_page.py` |
| [TC-LOGIN-008](#tc-login-008--login-with-invalid-username-and-invalid-password)         | Login with invalid username and invalid password         | Regression / Negative      | Medium   | Automated         | `tests/test_login_page.py` |
| [TC-LOGIN-009](#tc-login-009--error-message-can-be-closed-after-failed-login)           | Error message can be closed after failed login           | UI / Regression            | Medium   | Automated         | `tests/test_login_page.py` |
| [TC-LOGIN-010](#tc-login-010--login-page-elements-are-visible)                          | Login page elements are visible                          | Smoke / UI                 | High     | Automated         | `tests/test_login_page.py` |
| [TC-LOGIN-011](#tc-login-011--password-field-masks-entered-characters)                  | Password field masks entered characters                  | UI / Regression            | Medium   | Automated         | `tests/test_login_page.py` |
| [TC-LOGIN-012](#tc-login-012--login-form-can-be-submitted-with-enter-key)               | Login form can be submitted with Enter key               | UI / Positive / Regression | Medium   | Automated         | `tests/test_login_page.py` |
| [TC-LOGIN-013](#tc-login-013--direct-access-to-inventory-page-without-login-is-blocked) | Direct access to inventory page without login is blocked | Regression / Security      | High     | Automated         | `tests/test_login_page.py` |
| [TC-LOGIN-014](#tc-login-014--direct-access-to-cart-page-without-login-is-blocked)      | Direct access to cart page without login is blocked      | Regression / Security      | High     | Automated         | `tests/test_login_page.py` |
| [TC-LOGIN-015](#tc-login-015--direct-access-to-item-page-without-login-is-blocked)      | Direct access to item page without login is blocked      | Regression / Security      | High     | Automated         | `tests/test_login_page.py` |
| [TC-LOGIN-016](#tc-login-016--input-error-icons-are-displayed-after-failed-login)       | Input error icons are displayed after failed login       | UI / Regression            | Medium   | Automated         | `tests/test_login_page.py` |

---

## Test Cases

### TC-LOGIN-001 — Successful login with valid credentials

**Type:** Smoke / Positive\
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

* This is the main happy path login scenario.

---

### TC-LOGIN-002 — Login with invalid username

**Type:** Regression / Negative\
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
* Login and password fields are visually marked as invalid.

**Expected Error Message:**

```text
Epic sadface: Username and password do not match any user in this service
```

**Notes:**

* This scenario validates username/password mismatch handling.

---

### TC-LOGIN-003 — Login with invalid password

**Type:** Regression / Negative\
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
* Red, closable error message is displayed under the login form.
* Login and password fields are visually marked as invalid.

**Expected Error Message:**

```text
Epic sadface: Username and password do not match any user in this service
```

**Notes:**

* This scenario validates invalid password handling.

---

### TC-LOGIN-004 — Login with empty username

**Type:** Regression / Negative\
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
* Red, closable error message is displayed under the login form.
* Login and password fields are visually marked as invalid.

**Expected Error Message:**

```text
Epic sadface: Username is required
```

**Notes:**

* This scenario validates required username field behavior.

---

### TC-LOGIN-005 — Login with empty password

**Type:** Regression / Negative\
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
* Red, closable error message is displayed under the login form.
* Login and password fields are visually marked as invalid.

**Expected Error Message:**

```text
Epic sadface: Password is required
```

**Notes:**

* This scenario validates required password field behavior.

---

### TC-LOGIN-006 — Login with empty credentials

**Type:** Regression / Negative\
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
* Red, closable error message is displayed under the login form.
* Login and password fields are visually marked as invalid.

**Expected Error Message:**

```text
Epic sadface: Username is required
```

**Notes:**

* When both fields are empty, the username validation message is displayed first.

---

### TC-LOGIN-007 — Locked out user login attempt

**Type:** Regression / Negative\
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
* Red, closable error message is displayed under the login form.
* Login and password fields are visually marked as invalid.

**Expected Error Message:**

```text
Epic sadface: Sorry, this user has been locked out.
```

**Notes:**

* This scenario validates application behavior for a blocked user account.

---

### TC-LOGIN-008 — Login with invalid username and invalid password

**Type:** Regression / Negative\
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
* Red, closable error message is displayed under the login form.
* Login and password fields are visually marked as invalid.

**Expected Error Message:**

```text
Epic sadface: Username and password do not match any user in this service
```

**Notes:**

* This scenario validates behavior when both username and password are invalid.

---

### TC-LOGIN-009 — Error message can be closed after failed login

**Type:** UI / Regression\
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

* This scenario validates basic error message interaction.
* The automated test verifies that the error message becomes hidden after closing it.

---

### TC-LOGIN-010 — Login page elements are visible

**Type:** Smoke / UI\
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

* This test validates that the login page is available and basic login UI elements are rendered.

---

### TC-LOGIN-011 — Password field masks entered characters

**Type:** UI / Regression\
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

**Type:** UI / Positive / Regression\
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
* This scenario supports basic UX and accessibility-oriented validation.

---

### TC-LOGIN-013 — Direct access to inventory page without login is blocked

**Type:** Regression / Security\
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

**Expected Error Message:**

```text
Epic sadface: You can only access '/inventory.html' when you are logged in.
```

**Notes:**

* This scenario validates basic access control for protected application pages.
* The automated test uses a fresh browser context provided by Playwright, so no additional session cleanup is required in the current setup.

---

### TC-LOGIN-014 — Direct access to cart page without login is blocked

**Type:** Regression / Security\
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

**Expected Error Message:**

```text
Epic sadface: You can only access '/cart.html' when you are logged in.
```

**Notes:**

* This scenario validates basic access control for protected application pages.
* The automated test uses a fresh browser context provided by Playwright, so no additional session cleanup is required in the current setup.

---

### TC-LOGIN-015 — Direct access to item page without login is blocked

**Type:** Regression / Security\
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

**Expected Error Message:**

```text
Epic sadface: You can only access '/inventory-item.html' when you are logged in.
```

**Notes:**

* This scenario validates basic access control for protected application pages.
* The automated test uses a fresh browser context provided by Playwright, so no additional session cleanup is required in the current setup.

---

### TC-LOGIN-016 — Input error icons are displayed after failed login

**Type:** UI / Regression\
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
4. Observe the username input field.
5. Observe the password input field.

**Expected Result:**

* User remains on the login page.
* Username input field displays an error icon.
* Password input field displays an error icon.
* Both input error icons use the expected error icon styling.

**Notes:**

* This scenario validates visual invalid-state indicators for login inputs after a failed login attempt.
* Current Page Object support exists through `LoginPage.get_input_error_icon()`.
* Automation should verify that two input error icons are visible after failed login.