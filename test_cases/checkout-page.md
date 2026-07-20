# Checkout Page — Test Cases

## Overview

This document contains manual test cases for the Sauce Demo checkout flow.

The goal of this document is to define checkout-related scenarios before automation implementation begins. Scenarios are documented here when the main action or validation happens on the checkout information page, checkout overview page, or checkout complete page.

Checkout automation is not implemented yet. All checkout scenarios in this file are currently planned for future automation.

Navigation from the cart page to check out step one is owned by Cart Page coverage and is documented in `test_cases/cart-page.md`.

## Known SUT Behavior Notes

Sauce Demo currently allows opening checkout step one from an empty cart. This appears to be a product behavior limitation rather than desired e-commerce behavior.

Core checkout test cases use a product in cart as the expected realistic precondition. Empty-cart checkout behavior is documented here but is not treated as the primary checkout happy path.

If this behavior needs to be explicitly tracked later, it should be handled as a dedicated edge-case or known-defect scenario after planning approval.

## Test Case Overview And Automation Coverage

**Type:** Regression / Navigation / UI\
**Priority:** Medium\

| Test Case ID                                                                                                         | Scenario                                                                        | Checkout Area     | Type                          | Priority | Automation Status | Automated In                  |
|----------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------|-------------------|-------------------------------|----------|-------------------|-------------------------------|
| [TC-CHECKOUT-001](#tc-checkout-001--checkout-information-form-displays-required-customer-fields)                     | Checkout information form displays required customer fields                     | Checkout Step One | Smoke / UI                    | High     | Automated         | `tests/test_checkout_page.py` |
| [TC-CHECKOUT-002](#tc-checkout-002--checkout-information-form-requires-first-name)                                   | Checkout information form requires first name                                   | Checkout Step One | Regression / Negative / UI    | High     | Automated         | `tests/test_checkout_page.py` |
| [TC-CHECKOUT-003](#tc-checkout-003--checkout-information-form-requires-last-name)                                    | Checkout information form requires last name                                    | Checkout Step One | Regression / Negative / UI    | High     | Automated         | `tests/test_checkout_page.py` |
| [TC-CHECKOUT-004](#tc-checkout-004--checkout-information-form-requires-postal-code)                                  | Checkout information form requires postal code                                  | Checkout Step One | Regression / Negative / UI    | High     | Automated         | `tests/test_checkout_page.py` |
| [TC-CHECKOUT-005](#tc-checkout-005--input-error-icons-are-displayed-after-failed-checkout-information-submission)    | Input error icons are displayed after failed checkout information submission    | Checkout Step One | UI / Regression               | Medium   | Automated         | `tests/test_checkout_page.py` |
| [TC-CHECKOUT-006](#tc-checkout-006--checkout-information-error-message-can-be-closed-after-validation-failure)       | Checkout information error message can be closed after validation failure       | Checkout Step One | UI / Regression               | Medium   | Automated         | `tests/test_checkout_page.py` |
| [TC-CHECKOUT-007](#tc-checkout-007--checkout-information-form-continues-to-overview-when-valid-data-is-provided)     | Checkout information form continues to overview when valid data is provided     | Checkout Step One | Smoke / Positive / Navigation | High     | Automated         | `tests/test_checkout_page.py` |
| [TC-CHECKOUT-008](#tc-checkout-008--checkout-information-cancel-returns-to-cart-and-preserves-cart-item)             | Checkout information cancel returns to cart and preserves cart item             | Checkout Step One | Regression / Navigation / UI  | Medium   | Automated         | `tests/test_checkout_page.py` |
| [TC-CHECKOUT-009](#tc-checkout-009--checkout-overview-displays-selected-product)                                     | Checkout overview displays selected product                                     | Checkout Step Two | Smoke / UI                    | High     | Automated         | `tests/test_checkout_page.py` |
| [TC-CHECKOUT-010](#tc-checkout-010--checkout-overview-displays-each-selected-product)                                | Checkout overview displays each selected product                                | Checkout Step Two | Regression / UI               | Medium   | Automated         | `tests/test_checkout_page.py` |
| [TC-CHECKOUT-011](#tc-checkout-011--checkout-overview-price-summary-is-correct-for-one-product)                      | Checkout overview price summary is correct for one product                      | Checkout Step Two | Smoke / UI                    | High     | Automated         | `tests/test_checkout_page.py` |
| [TC-CHECKOUT-012](#tc-checkout-012--checkout-overview-price-summary-is-correct-for-multiple-products)                | Checkout overview price summary is correct for multiple products                | Checkout Step Two | Regression / UI               | High     | Automated         | `tests/test_checkout_page.py` |
| [TC-CHECKOUT-013](#tc-checkout-013--checkout-overview-cancel-returns-to-inventory-page)                              | Checkout overview cancel returns to inventory page                              | Checkout Step Two | Regression / Navigation / UI  | Medium   | Automated         | `tests/test_checkout_page.py` |
| [TC-CHECKOUT-014](#tc-checkout-014--product-details-can-be-opened-from-checkout-overview-item-name)                  | Product details can be opened from checkout overview item name                  | Checkout Step Two | Smoke / Navigation / UI       | Medium   | Automated         | `tests/test_checkout_page.py` |
| [TC-CHECKOUT-015](#tc-checkout-015--product-details-can-be-opened-from-checkout-overview-item-name-for-each-product) | Product details can be opened from checkout overview item name for each product | Checkout Step Two | Regression / Navigation / UI  | Medium   | Automated         | `tests/test_checkout_page.py` |
| [TC-CHECKOUT-016](#tc-checkout-016--finish-button-completes-checkout-and-opens-order-confirmation-page)              | Finish button completes checkout and opens order confirmation page              | Checkout Step Two | Smoke / Positive / E2E        | High     | Automated         | `tests/test_checkout_page.py` |
| [TC-CHECKOUT-017](#tc-checkout-017--checkout-complete-page-displays-order-confirmation-message)                      | Checkout complete page displays order confirmation message                      | Checkout Complete | Regression / UI               | High     | Planned           | TBD                           |
| [TC-CHECKOUT-018](#tc-checkout-018--back-home-returns-to-inventory-page-after-order-completion)                      | Back Home returns to inventory page after order completion                      | Checkout Complete | Regression / Navigation / UI  | Medium   | Planned           | TBD                           |

---

## Test Cases

### Checkout Step One — Customer Information

#### TC-CHECKOUT-001 — Checkout information form displays required customer fields

**Type:** Smoke / UI\
**Priority:** High\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_checkout_page.py`

**Preconditions:**

* User is logged in.
* Selected product has been added to the cart.
* User has opened the checkout information page from the cart page.

**Test Data:**

* User: `standard_user`
* Example product: `Sauce Labs Backpack`

**Steps:**

1. Open the checkout information page.
2. Observe the checkout information form.

**Expected Result:**

* Checkout information form is visible.
* First Name input is visible.
* Last Name input is visible.
* Zip/Postal Code input is visible.
* Continue button is visible.
* Cancel button is visible.
* Page title indicates checkout information step.

**Notes:**

* This scenario validates basic checkout step one UI availability.
* Navigation from the cart page to check out step one is documented in `test_cases/cart-page.md`.
* Required field validation behavior is covered by separate negative scenarios.

---

#### TC-CHECKOUT-002 — Checkout information form requires first name

**Type:** Regression / Negative / UI\
**Priority:** High\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_checkout_page.py`

**Preconditions:**

* User is logged in.
* Selected product has been added to the cart.
* User has opened the checkout information page from the cart page.

**Test Data:**

* First Name: empty
* Last Name: `User`
* Postal Code: `12345`

**Steps:**

1. Leave First Name empty.
2. Enter valid last name.
3. Enter valid postal code.
4. Click the Continue button.

**Expected Result:**

* User remains on the checkout information page.
* Checkout overview page is not opened.
* Error message is displayed.
* First Name validation error indicates that first name is required.

**Expected Error Message:**

```text
Error: First Name is required
```

**Notes:**

* This scenario validates required field handling for the First Name field.
* Input error icon visibility is covered separately in TC-CHECKOUT-005.

---

#### TC-CHECKOUT-003 — Checkout information form requires last name

**Type:** Regression / Negative / UI\
**Priority:** High\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_checkout_page.py`

**Preconditions:**

* User is logged in.
* Selected product has been added to the cart.
* User has opened the checkout information page from the cart page.

**Test Data:**

* First Name: `Standard`
* Last Name: empty
* Postal Code: `12345`

**Steps:**

1. Enter valid first name.
2. Leave Last Name empty.
3. Enter valid postal code.
4. Click the Continue button.

**Expected Result:**

* User remains on the checkout information page.
* Checkout overview page is not opened.
* Error message is displayed.
* Last Name validation error indicates that last name is required.

**Expected Error Message:**

```text
Error: Last Name is required
```

**Notes:**

* This scenario validates required field handling for the Last Name field.
* Input error icon visibility is covered separately in TC-CHECKOUT-005.

---

#### TC-CHECKOUT-004 — Checkout information form requires postal code

**Type:** Regression / Negative / UI\
**Priority:** High\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_checkout_page.py`

**Preconditions:**

* User is logged in.
* Selected product has been added to the cart.
* User has opened the checkout information page from the cart page.

**Test Data:**

* First Name: `Standard`
* Last Name: `User`
* Postal Code: empty

**Steps:**

1. Enter valid first name.
2. Enter valid last name.
3. Leave Zip/Postal Code empty.
4. Click the Continue button.

**Expected Result:**

* User remains on the checkout information page.
* Checkout overview page is not opened.
* Error message is displayed.
* Postal Code validation error indicates that postal code is required.

**Expected Error Message:**

```text
Error: Postal Code is required
```

**Notes:**

* This scenario validates required field handling for the Zip/Postal Code field.
* Input error icon visibility is covered separately in TC-CHECKOUT-005.

---

#### TC-CHECKOUT-005 — Input error icons are displayed after failed checkout information submission

**Type:** UI / Regression\
**Priority:** Medium\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_checkout_page.py`

**Preconditions:**

* User is logged in.
* Selected product has been added to the cart.
* User has opened the checkout information page from the cart page.

**Test Data:**

* First Name: empty
* Last Name: empty
* Postal Code: empty

**Steps:**

1. Leave all checkout information fields empty.
2. Click the Continue button.
3. Observe the checkout information form fields.

**Expected Result:**

* User remains on the checkout information page.
* Error message is displayed.
* First Name field is visually marked as invalid.
* Last Name field is visually marked as invalid.
* Zip/Postal Code field is visually marked as invalid.
* Input error icons are displayed for the invalid fields.

**Notes:**

* This scenario validates checkout information form UI error state after failed submission.
* It mirrors the login page input error icon coverage pattern.

---

#### TC-CHECKOUT-006 — Checkout information error message can be closed after validation failure

**Type:** UI / Regression\
**Priority:** Medium\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_checkout_page.py`

**Preconditions:**

* User is logged in.
* Selected product has been added to the cart.
* User has opened the checkout information page from the cart page.
* Checkout information validation error is displayed.

**Test Data:**

* First Name: empty
* Last Name: empty
* Postal Code: empty

**Steps:**

1. Leave all checkout information fields empty.
2. Click the Continue button.
3. Verify that validation error message is displayed.
4. Click the error close button.

**Expected Result:**

* Error message is removed from the checkout information page.
* User remains on the checkout information page.
* Checkout overview page is not opened.
* Checkout information form remains available for correction.

**Notes:**

* This scenario validates that the checkout information error message can be dismissed.
* It mirrors the login page error message close coverage pattern.

---

#### TC-CHECKOUT-007 — Checkout information form continues to overview when valid data is provided

**Type:** Smoke / Positive / Navigation\
**Priority:** High\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_checkout_page.py`

**Preconditions:**

* User is logged in.
* Selected product has been added to the cart.
* User has opened the checkout information page from the cart page.

**Test Data:**

* First Name: `Standard`
* Last Name: `User`
* Postal Code: `12345`
* Example product: `Sauce Labs Backpack`

**Steps:**

1. Enter valid first name.
2. Enter valid last name.
3. Enter valid postal code.
4. Click the Continue button.

**Expected Result:**

* User is redirected to the checkout overview page.
* Checkout overview page is displayed.
* Selected product is still included in the order summary.
* Finish button is visible.
* Cancel button is visible.

**Notes:**

* This is the main positive checkout information form scenario.
* This scenario belongs to check out step one because the main action is submitting the customer information form.
* Detailed overview content validation is covered by separate checkout overview scenarios.

---

#### TC-CHECKOUT-008 — Checkout information cancel returns to cart and preserves cart item

**Type:** Regression / Navigation / UI\
**Priority:** Medium\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_checkout_page.py`

**Preconditions:**

* User is logged in.
* Selected product has been added to the cart.
* User has opened the checkout information page from the cart page.

**Test Data:**

* User: `standard_user`
* Example product: `Sauce Labs Backpack`

**Steps:**

1. Open the checkout information page.
2. Click the Cancel button.

**Expected Result:**

* User is redirected back to the cart page.
* Previously added product is still visible in the cart.
* Checkout information form is no longer displayed.

**Notes:**

* This scenario validates cancellation from checkout step one.
* Cart state should be preserved after returning from checkout information page.

---

### Checkout Step Two — Order Overview

#### TC-CHECKOUT-009 — Checkout overview displays selected product

**Type:** Smoke / UI\
**Priority:** High\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_checkout_page.py`

**Preconditions:**

* User is logged in.
* Selected product has been added to the cart.
* User has submitted valid checkout information.
* User is on the checkout overview page.

**Test Data:**

* First Name: `Standard`
* Last Name: `User`
* Postal Code: `12345`
* Example product: `Sauce Labs Backpack`

**Steps:**

1. Add the selected product to the cart.
2. Open the checkout information page.
3. Submit valid checkout information.
4. Observe the checkout overview item summary.

**Expected Result:**

* Checkout overview page is displayed.
* Selected product name is visible.
* Selected product description is visible.
* Selected product price is visible.
* Selected product quantity is visible.
* Selected product quantity displays `1`.

**Notes:**

* This scenario validates checkout overview item summary for one representative product.
* Full all-products checkout overview item coverage is tracked separately in TC-CHECKOUT-010.
* During automation, expected product data should come from centralized product test data.

---

#### TC-CHECKOUT-010 — Checkout overview displays each selected product

**Type:** Regression / UI\
**Priority:** Medium\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_checkout_page.py`

**Preconditions:**

* User is logged in.
* User is on the inventory page.
* Product list is visible.
* Product under test has been added to the cart.
* User has submitted valid checkout information.
* User is on the checkout overview page.

**Test Data:**

* First Name: `Standard`
* Last Name: `User`
* Postal Code: `12345`
* Product data: each product from centralized product test data

**Steps:**

1. Log in with valid credentials.
2. Add the product under test to the cart.
3. Open the cart page.
4. Open the checkout information page.
5. Submit valid checkout information.
6. Observe the checkout overview item summary.

**Expected Result:**

* Checkout overview page is displayed.
* Product under test is visible in the checkout overview.
* Product name matches expected product data.
* Product description matches expected product data.
* Product price matches expected product data.
* Product quantity is visible.
* Product quantity displays `1`.

**Notes:**

* This scenario validates checkout overview item summary for each product.
* During automation, this scenario should be parametrized with centralized product test data.
* Each parametrized run should start from an isolated browser/page state.

---

#### TC-CHECKOUT-011 — Checkout overview price summary is correct for one product

**Type:** Smoke / UI\
**Priority:** High\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_checkout_page.py`

**Preconditions:**

* User is logged in.
* Selected product has been added to the cart.
* User has submitted valid checkout information.
* User is on the checkout overview page.

**Test Data:**

* First Name: `Standard`
* Last Name: `User`
* Postal Code: `12345`
* Example product: `Sauce Labs Backpack`

**Steps:**

1. Add the selected product to the cart.
2. Open the checkout information page.
3. Submit valid checkout information.
4. Observe the checkout overview price summary.

**Expected Result:**

* Item total is visible.
* Tax value is visible.
* Total value is visible.
* Item total matches the selected product price.
* Total value equals item total plus tax.
* Price values are displayed in currency format.

**Notes:**

* This scenario validates checkout price summary for one representative product.
* Exact tax value should be verified during automation based on the value displayed by the application.

---

#### TC-CHECKOUT-012 — Checkout overview price summary is correct for multiple products

**Type:** Regression / UI\
**Priority:** High\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_checkout_page.py`

**Preconditions:**

* User is logged in.
* Multiple products have been added to the cart.
* User has submitted valid checkout information.
* User is on the checkout overview page.

**Test Data:**

* First Name: `Standard`
* Last Name: `User`
* Postal Code: `12345`
* Example products:

  * `Sauce Labs Backpack`
  * `Sauce Labs Bike Light`

**Steps:**

1. Add multiple selected products to the cart.
2. Open the cart page.
3. Open the checkout information page.
4. Submit valid checkout information.
5. Observe the checkout overview item summary.
6. Observe the checkout overview price summary.

**Expected Result:**

* Checkout overview page is displayed.
* All selected products are visible in the checkout overview.
* Item total is visible.
* Item total matches the sum of selected product prices.
* Tax value is visible.
* Total value is visible.
* Total value equals item total plus tax.
* Price values are displayed in currency format.

**Notes:**

* This scenario validates checkout price summary for multiple products.
* During automation, expected item total should be calculated from centralized product test data.
* Exact tax value should be verified based on the value displayed by the application.

---

#### TC-CHECKOUT-013 — Checkout overview cancel returns to inventory page

**Type:** Regression / Navigation / UI\
**Priority:** Medium\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_checkout_page.py`

**Preconditions:**

* User is logged in.
* Selected product has been added to the cart.
* User has submitted valid checkout information.
* User is on the checkout overview page.

**Test Data:**

* First Name: `Standard`
* Last Name: `User`
* Postal Code: `12345`
* Example product: `Sauce Labs Backpack`

**Steps:**

1. Add the selected product to the cart.
2. Open the checkout information page.
3. Submit valid checkout information.
4. Click the Cancel button on the checkout overview page.

**Expected Result:**

* User is redirected to the inventory page.
* Inventory product list is visible.
* Checkout overview page is no longer displayed.
* Product is still presented in the cart (remove button is visible)
* Cart badge still indicates that the product is in the shopping cart 

**Notes:**

* This scenario validates cancellation from checkout step two.
* Cart state behavior after checkout overview cancellation can be verified in a later automation task if required.

---

#### TC-CHECKOUT-014 — Product details can be opened from checkout overview item name

**Type:** Smoke / Navigation / UI\
**Priority:** Medium\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_checkout_page.py`

**Preconditions:**

* User is logged in.
* Selected product has been added to the cart.
* User has submitted valid checkout information.
* User is on the checkout overview page.

**Test Data:**

* First Name: `Standard`
* Last Name: `User`
* Postal Code: `12345`
* Example product: `Sauce Labs Backpack`

**Steps:**

1. Add the selected product to the cart.
2. Open the checkout information page.
3. Submit valid checkout information.
4. Click the selected product name on the checkout overview page.

**Expected Result:**

* Product details page is opened for the selected product.
* Product details page displays the selected product.
* Product name matches the product clicked from checkout overview.
* Product details content is visible.
* Product is still presented in the cart (remove button is visible).
* Cart badge still indicates that the product is in the shopping cart. 

**Notes:**

* This scenario validates product details navigation from checkout overview for one representative product.
* Full all-products navigation coverage is tracked separately in TC-CHECKOUT-015.

---

#### TC-CHECKOUT-015 — Product details can be opened from checkout overview item name for each product

**Type:** Regression / Navigation / UI\
**Priority:** Medium\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_checkout_page.py`

**Preconditions:**

* User is logged in.
* Product under test has been added to the cart.
* User has submitted valid checkout information.
* User is on the checkout overview page.

**Test Data:**

* First Name: `Standard`
* Last Name: `User`
* Postal Code: `12345`
* Product data: each product from centralized product test data

**Steps:**

1. Log in with valid credentials.
2. Add the product under test to the cart.
3. Open the cart page.
4. Open the checkout information page.
5. Submit valid checkout information.
6. Click the product name on the checkout overview page.

**Expected Result:**

* Product details page is opened for the product under test.
* Product details page displays the correct product.
* Product name matches the product clicked from checkout overview.
* Product details content matches expected product data.
* Product is still presented in the cart (remove button is visible).
* Cart badge still indicates that the product is in the shopping cart.

**Notes:**

* This scenario validates product details navigation from checkout overview for each product.
* During automation, this scenario should be parametrized with centralized product test data.
* Each parametrized run should start from an isolated browser/page state.

---

#### TC-CHECKOUT-016 — Finish button completes checkout and opens order confirmation page

**Type:** Smoke / Positive / E2E\
**Priority:** High\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_checkout_page.py`

**Preconditions:**

* User is logged in.
* Selected product has been added to the cart.
* User has submitted valid checkout information.
* User is on the checkout overview page.

**Test Data:**

* First Name: `Standard`
* Last Name: `User`
* Postal Code: `12345`
* Example product: `Sauce Labs Backpack`

**Steps:**

1. Add the selected product to the cart.
2. Open the checkout information page.
3. Submit valid checkout information.
4. Verify that checkout overview page is displayed.
5. Click the Finish button.

**Expected Result:**

* Order is completed.
* User is redirected to the checkout complete page.
* Checkout complete page is displayed.
* Order completion confirmation is visible.

**Notes:**

* This scenario belongs to check out step two because the main action is clicking Finish on the checkout overview page.
* Detailed confirmation message validation is covered separately in TC-CHECKOUT-017.

---

### Checkout Complete — Order Confirmation

#### TC-CHECKOUT-017 — Checkout complete page displays order confirmation message

**Type:** Regression / UI
**Priority:** High
**Automation Candidate:** Yes
**Automation Status:** Planned
**Automated In:** TBD

**Preconditions:**

* User is logged in.
* User has completed checkout with valid customer information.
* User is on the checkout complete page.

**Test Data:**

* First Name: `Standard`
* Last Name: `User`
* Postal Code: `12345`
* Example product: `Sauce Labs Backpack`

**Steps:**

1. Complete checkout with valid customer information.
2. Observe the checkout complete page.

**Expected Result:**

* Checkout complete page is displayed.
* Completion header is visible.
* Completion message is visible.
* Back Home button is visible.

**Expected Completion Header:**

```text
Thank you for your order!
```

**Expected Completion Message:**

```text
Your order has been dispatched, and will arrive just as fast as the pony can get there!
```

**Notes:**

* This scenario validates final order confirmation content.
* The full finish action is covered by TC-CHECKOUT-016.

---

#### TC-CHECKOUT-018 — Back Home returns to inventory page after order completion

**Type:** Regression / Navigation / UI
**Priority:** Medium
**Automation Candidate:** Yes
**Automation Status:** Planned
**Automated In:** TBD

**Preconditions:**

* User is logged in.
* User has completed checkout with valid customer information.
* User is on the checkout complete page.

**Test Data:**

* First Name: `Standard`
* Last Name: `User`
* Postal Code: `12345`
* Example product: `Sauce Labs Backpack`

**Steps:**

1. Complete checkout with valid customer information.
2. Click the Back Home button.

**Expected Result:**

* User is redirected to the inventory page.
* Inventory product list is visible.
* Checkout complete page is no longer displayed.

**Notes:**

* This scenario validates navigation after order completion.
* It closes the basic checkout happy path from cart to inventory after successful order completion.
