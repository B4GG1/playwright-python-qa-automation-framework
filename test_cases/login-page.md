# Login Page — Test Cases

## Overview

This document contains manual test cases for the Sauce Demo login page.
The goal of this document is to define login-related test scenarios before automation implementation.

## List of Test Cases

* [TC-LOGIN-001 — Successful login with valid credentials](#tc-login-001--successful-login-with-valid-credentials)
* [TC-LOGIN-002 — Login with invalid username](#tc-login-002--login-with-invalid-username)
* [TC-LOGIN-003 — Login with invalid password](#tc-login-003--login-with-invalid-password)
* [TC-LOGIN-004 — Login with empty username](#tc-login-004--login-with-empty-username)
* [TC-LOGIN-005 — Login with empty password](#tc-login-005--login-with-empty-password)
* [TC-LOGIN-006 — Login with empty credentials](#tc-login-006--login-with-empty-credentials)
* [TC-LOGIN-007 — Locked out user login attempt](#tc-login-007--locked-out-user-login-attempt)
* [TC-LOGIN-008 — Login with invalid username and invalid password](#tc-login-008--login-with-invalid-username-and-invalid-password)
* [TC-LOGIN-009 — Error message can be closed after failed login](#tc-login-009--error-message-can-be-closed-after-failed-login)
* [TC-LOGIN-010 — Login page elements are visible](#tc-login-010--login-page-elements-are-visible)
* [TC-LOGIN-011 — Password field masks entered characters](#tc-login-011--password-field-masks-entered-characters)
* [TC-LOGIN-012 — Login form can be submitted with Enter key](#tc-login-012--login-form-can-be-submitted-with-enter-key)
* [TC-LOGIN-013 — Direct access to inventory page without login is blocked](#tc-login-013--direct-access-to-inventory-page-without-login-is-blocked)

---

## Test Cases

### TC-LOGIN-001 — Successful login with valid credentials

**Type:** Smoke / Positive
**Priority:** High
**Automation Candidate:** Yes

**Preconditions:**

* User is on the login page.

**Test Data:**

* Username: standard_user
* Password: secret_sauce

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

**Type:** Regression / Negative
**Priority:** Medium
**Automation Candidate:** Yes

**Preconditions:**

* User is on the login page.

**Test Data:**

* Username: invalid_username
* Password: secret_sauce

**Steps:**

1. Enter invalid username.
2. Enter valid password.
3. Click the Login button.

**Expected Result:**

* User remains on the login page.
* Red, closable error message is displayed under the login form.
* Login and password fields are visually marked as invalid.

**Notes:**

* Error message should contain the following text:
  "Epic sadface: Username and password do not match any user in this service"

---

### TC-LOGIN-003 — Login with invalid password

**Type:** Regression / Negative
**Priority:** Medium
**Automation Candidate:** Yes

**Preconditions:**

* User is on the login page.

**Test Data:**

* Username: standard_user
* Password: invalid_password

**Steps:**

1. Enter valid username.
2. Enter invalid password.
3. Click the Login button.

**Expected Result:**

* User remains on the login page.
* Red, closable error message is displayed under the login form.
* Login and password fields are visually marked as invalid.

**Notes:**

* Error message should contain the following text:
  "Epic sadface: Username and password do not match any user in this service"

---

### TC-LOGIN-004 — Login with empty username

**Type:** Regression / Negative
**Priority:** Medium
**Automation Candidate:** Yes

**Preconditions:**

* User is on the login page.

**Test Data:**

* Username: empty
* Password: secret_sauce

**Steps:**

1. Leave username field empty.
2. Enter valid password.
3. Click the Login button.

**Expected Result:**

* User remains on the login page.
* Red, closable error message is displayed under the login form.
* Login and password fields are visually marked as invalid.

**Notes:**

* Error message should contain the following text:
  "Epic sadface: Username is required"

---

### TC-LOGIN-005 — Login with empty password

**Type:** Regression / Negative
**Priority:** Medium
**Automation Candidate:** Yes

**Preconditions:**

* User is on the login page.

**Test Data:**

* Username: standard_user
* Password: empty

**Steps:**

1. Enter valid username.
2. Leave password field empty.
3. Click the Login button.

**Expected Result:**

* User remains on the login page.
* Red, closable error message is displayed under the login form.
* Login and password fields are visually marked as invalid.

**Notes:**

* Error message should contain the following text:
  "Epic sadface: Password is required"

---

### TC-LOGIN-006 — Login with empty credentials

**Type:** Regression / Negative
**Priority:** Medium
**Automation Candidate:** Yes

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

**Notes:**

* Error message should contain the following text:
  "Epic sadface: Username is required"

---

### TC-LOGIN-007 — Locked out user login attempt

**Type:** Regression / Negative
**Priority:** Medium
**Automation Candidate:** Yes

**Preconditions:**

* User is on the login page.

**Test Data:**

* Username: locked_out_user
* Password: secret_sauce

**Steps:**

1. Enter locked out user username.
2. Enter valid password.
3. Click the Login button.

**Expected Result:**

* User remains on the login page.
* Red, closable error message is displayed under the login form.
* Login and password fields are visually marked as invalid.

**Notes:**

* Error message should contain the following text:
  "Epic sadface: Sorry, this user has been locked out."

---

### TC-LOGIN-008 — Login with invalid username and invalid password

**Type:** Regression / Negative
**Priority:** Medium
**Automation Candidate:** Yes

**Preconditions:**

* User is on the login page.

**Test Data:**

* Username: invalid_user
* Password: invalid_sauce

**Steps:**

1. Enter invalid username.
2. Enter invalid password.
3. Click the Login button.

**Expected Result:**

* User remains on the login page.
* Red, closable error message is displayed under the login form.
* Login and password fields are visually marked as invalid.

**Notes:**

* Error message should contain the following text:
  "Epic sadface: Username and password do not match any user in this service"

---

### TC-LOGIN-009 — Error message can be closed after failed login

**Type:** UI / Regression
**Priority:** Medium
**Automation Candidate:** Yes

**Preconditions:**

* User is on the login page.
* Failed login attempt has already triggered an error message.

**Test Data:**

* Username: invalid_user
* Password: invalid_sauce

**Steps:**

1. Enter invalid username.
2. Enter invalid password.
3. Click the Login button.
4. Click the close button on the error message.

**Expected Result:**

* User remains on the login page.
* Error message disappears.
* Login and password fields are no longer visually marked as invalid.

**Notes:**

* This scenario validates basic error message interaction.

---

### TC-LOGIN-010 — Login page elements are visible

**Type:** Smoke / UI
**Priority:** High
**Automation Candidate:** Yes

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
* Login form is displayed correctly.

**Notes:**

* This test validates that the login page is available and basic login UI elements are rendered.

---

### TC-LOGIN-011 — Password field masks entered characters

**Type:** UI
**Priority:** Medium
**Automation Candidate:** Yes

**Preconditions:**

* User is on the login page.

**Test Data:**

* Username: N/A
* Password: secret_sauce

**Steps:**

1. Click the password field.
2. Enter password text.

**Expected Result:**

* Entered password is not displayed as plain text.
* Password field masks the entered characters.

**Notes:**

* This is a basic UI/security-related validation.

---

### TC-LOGIN-012 — Login form can be submitted with Enter key

**Type:** UI / Positive
**Priority:** Medium
**Automation Candidate:** Later

**Preconditions:**

* User is on the login page.

**Test Data:**

* Username: standard_user
* Password: secret_sauce

**Steps:**

1. Enter valid username.
2. Enter valid password.
3. Press Enter while focus is inside the login form.

**Expected Result:**

* Login form is submitted.
* User is redirected to the inventory page.
* Product list is visible.

**Notes:**

* This test validates keyboard-based form submission.
* Automation priority can be decided later after core login scenarios are implemented.

---

### TC-LOGIN-013 — Direct access to inventory page without login is blocked

**Type:** Regression / Security
**Priority:** High
**Automation Candidate:** Yes

**Preconditions:**

* User is not logged in.
* Browser session does not contain an active authenticated state.

**Test Data:**

* Username: N/A
* Password: N/A

**Steps:**

1. Open the inventory page URL directly without logging in.

**Expected Result:**

* User is redirected to the login page.
* Inventory page is not accessible.
* Error message informs the user that login is required.

**Notes:**

* This scenario validates basic access control for protected application pages.
