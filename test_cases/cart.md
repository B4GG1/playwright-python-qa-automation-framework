# Cart — Test Cases

## Overview

This document contains manual test cases for the Sauce Demo cart functionality.

The goal of this document is to define cart-related test scenarios and track their automation coverage.

This workstream focuses only on:

* cart page availability
* empty cart state
* adding products to cart
* inventory-side cart button behavior
* cart badge behavior
* cart item visibility
* cart item content validation
* removing products from cart
* navigation between cart and inventory page
* cart state persistence after logout and re-login

Checkout scenarios are intentionally excluded from this document and will be covered in a separate checkout test case file.

## Test Case Overview And Automation Coverage

| Test Case ID                                                                                             | Scenario                                                                    | Type                       | Priority | Automation Status | Automated In |
|----------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------|----------------------------|----------| --- | --- |
| [TC-CART-001](#tc-cart-001--cart-page-can-be-opened-from-inventory-page)                                 | Cart page can be opened from inventory page                                 | Smoke / Navigation / UI    | High     | Automated         | `tests/test_cart_page.py` |
| [TC-CART-002](#tc-cart-002--cart-is-empty-before-adding-products)                                        | Cart is empty before adding products                                        | Smoke / UI                 | Medium   | Automated         | `tests/test_cart_page.py` |
| [TC-CART-003](#tc-cart-003--product-can-be-added-to-cart-from-inventory-page)                            | Product can be added to cart from inventory page                            | Regression / Positive / UI | High     | Automated         | `tests/test_cart_page.py` |
| [TC-CART-004](#tc-cart-004--add-to-cart-button-changes-to-remove-after-adding-product-from-inventory)    | Add to cart button changes to Remove after adding product from inventory    | Regression / UI            | Medium   | Automated         | `tests/test_cart_page.py` |
| [TC-CART-005](#tc-cart-005--cart-badge-is-displayed-after-adding-one-product)                            | Cart badge is displayed after adding one product                            | Regression / UI            | Medium   | Automated         | `tests/test_cart_page.py` |
| [TC-CART-006](#tc-cart-006--cart-badge-count-updates-after-adding-multiple-products)                     | Cart badge count updates after adding multiple products                     | Regression / UI            | Medium   | Automated         | `tests/test_cart_page.py` |
| [TC-CART-007](#tc-cart-007--added-product-is-displayed-on-cart-page)                                     | Added product is displayed on cart page                                     | Regression / Positive / UI | High     | Automated         | `tests/test_cart_page.py` |
| [TC-CART-008](#tc-cart-008--cart-product-content-matches-added-product-data)                             | Cart product content matches added product data                             | Regression / UI            | Medium   | Automated         | `tests/test_cart_page.py` |
| [TC-CART-009](#tc-cart-009--product-can-be-removed-from-cart-page)                                       | Product can be removed from cart page                                       | Regression / Positive / UI | High     | Automated         | `tests/test_cart_page.py` |
| [TC-CART-010](#tc-cart-010--cart-badge-is-removed-after-removing-last-product)                           | Cart badge is removed after removing last product                           | Regression / UI            | Medium   | Automated         | `tests/test_cart_page.py` |
| [TC-CART-011](#tc-cart-011--user-can-return-from-cart-page-to-inventory-page)                            | User can return from cart page to inventory page                            | Regression / Navigation / UI | Medium   | Automated         | `tests/test_cart_page.py` |
| [TC-CART-012](#tc-cart-012--cart-state-persists-after-logout-and-re-login)                               | Cart state persists after logout and re-login                               | Regression / Positive / UI | Medium   | Automated         | `tests/test_cart_page.py`  |
| [TC-CART-013](#tc-cart-013--add-to-cart-button-changes-to-remove-after-adding-product-from-details-page) | Add to cart button changes to Remove after adding product from details page | Regression / UI            | Medium   | Automated         | `tests/test_cart_page.py` |

---

## Test Cases

### TC-CART-001 — Cart page can be opened from inventory page

**Type:** Smoke / Navigation / UI\
**Priority:** High\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_cart_page.py`

**Preconditions:**

* User is logged in.
* User is on the inventory page.

**Test Data:**

* User: `standard_user`

**Steps:**

1. Log in with valid credentials.
2. Click the cart icon on the inventory page.
3. Observe the cart page.

**Expected Result:**

* Cart page is opened.
* Cart page URL contains `cart.html`.
* Cart page container is visible.
* Cart page displays the expected cart layout.

**Notes:**

* This is the main smoke validation for cart page availability.
* This scenario should not validate product content or checkout behavior.

---

### TC-CART-002 — Cart is empty before adding products

**Type:** Smoke / UI\
**Priority:** Medium\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_cart_page.py`

**Preconditions:**

* User is logged in.
* User is on the inventory page.
* No products have been added to the cart in the current session.

**Test Data:**

* User: `standard_user`

**Steps:**

1. Log in with valid credentials.
2. Open the cart page.
3. Observe the cart item list.

**Expected Result:**

* Cart page is opened.
* No cart items are displayed.
* Cart badge is not displayed on the inventory/cart header.
* Cart page remains available and does not display an error.

**Notes:**

* Sauce Demo does not display a dedicated empty cart message.
* During automation, this scenario should verify that the cart item list does not contain product items.

---

### TC-CART-003 — Product can be added to cart from inventory page

**Type:** Regression / Positive / UI\
**Priority:** High\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_cart_page.py`

**Preconditions:**

* User is logged in.
* User is on the inventory page.
* Product list is visible.

**Test Data:**

* User: `standard_user`
* Example product: `Sauce Labs Backpack`

**Steps:**

1. Log in with valid credentials.
2. Find the selected product on the inventory page.
3. Click the Add to cart button for the selected product.
4. Open the cart page.
5. Observe the cart item list.

**Expected Result:**

* Selected product is added to the cart.
* Cart page displays the selected product.
* No error is displayed.

**Notes:**

* This scenario validates the basic add-to-cart flow.
* During automation, deterministic product data should be used instead of random product selection.

---

### TC-CART-004 — Add to cart button changes to Remove after adding product from inventory

**Type:** Regression / UI\
**Priority:** Medium\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_cart_page.py`

**Preconditions:**

* User is logged in.
* User is on the inventory page.
* Product list is visible.

**Test Data:**

* User: `standard_user`
* Example product: `Sauce Labs Backpack`

**Steps:**

1. Log in with valid credentials.
2. Find the selected product on the inventory page.
3. Click the Add to cart button for the selected product.
4. Observe the button for the same product.

**Expected Result:**

* Product is added to the cart.
* Add to cart button changes to Remove for the selected product.
* Remove button is visible for the selected product.
* Other products remain unchanged.

**Notes:**

* This scenario validates inventory-side UI feedback after adding a product to the cart.
* This test should not validate cart page product content.

---

### TC-CART-005 — Cart badge is displayed after adding one product

**Type:** Regression / UI\
**Priority:** Medium\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_cart_page.py`

**Preconditions:**

* User is logged in.
* User is on the inventory page.
* Product list is visible.

**Test Data:**

* User: `standard_user`
* Example product: `Sauce Labs Backpack`

**Steps:**

1. Log in with valid credentials.
2. Add one selected product to the cart.
3. Observe the cart badge in the header.

**Expected Result:**

* Cart badge is visible.
* Cart badge displays `1`.
* Cart badge is displayed near the cart icon.

**Notes:**

* This scenario validates badge visibility after adding one product.
* During automation, badge text should be read from the UI and compared with the expected count.

---

### TC-CART-006 — Cart badge count updates after adding multiple products

**Type:** Regression / UI\
**Priority:** Medium\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_cart_page.py`

**Preconditions:**

* User is logged in.
* User is on the inventory page.
* Product list is visible.

**Test Data:**

* User: `standard_user`
* Example products:

  * `Sauce Labs Backpack`
  * `Sauce Labs Bolt T-Shirt`

**Steps:**

1. Log in with valid credentials.
2. Add the first selected product to the cart.
3. Add the second selected product to the cart.
4. Observe the cart badge in the header.

**Expected Result:**

* Cart badge is visible.
* Cart badge displays `2`.
* Cart badge count matches the number of added products.

**Notes:**

* This scenario validates cart badge count updates for multiple products.
* During automation, deterministic product data should be used instead of random product selection.

---

### TC-CART-007 — Added product is displayed on cart page

**Type:** Regression / Positive / UI\
**Priority:** High\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_cart_page.py`

**Preconditions:**

* User is logged in.
* User is on the inventory page.
* Product list is visible.

**Test Data:**

* User: `standard_user`
* Example product: `Sauce Labs Backpack`

**Steps:**

1. Log in with valid credentials.
2. Add the selected product to the cart.
3. Open the cart page.
4. Observe the cart item list.

**Expected Result:**

* Cart page is opened.
* Selected product is visible on the cart page.
* Cart item list contains the selected product.

**Notes:**

* This scenario validates that an added product is displayed in the cart.
* This test should not fully validate product name, description, price, and quantity. Detailed content validation is covered by a separate test case.

---

### TC-CART-008 — Cart product content matches added product data

**Type:** Regression / UI\
**Priority:** Medium\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_cart_page.py`

**Preconditions:**

* User is logged in.
* User is on the inventory page.
* Product list is visible.
* Selected product has been added to the cart.

**Test Data:**

* User: `standard_user`
* Example product: `Sauce Labs Backpack`

**Steps:**

1. Log in with valid credentials.
2. Add the selected product to the cart.
3. Open the cart page.
4. Observe the cart item content.

**Expected Result:**

* Cart item name matches the selected product name.
* Cart item description matches the selected product description.
* Cart item price matches the selected product price.
* Cart item quantity is visible.
* Cart item quantity displays `1`.
* Remove button is visible for the cart item.

**Notes:**

* This scenario validates cart item content consistency.
* During automation, expected product data should come from centralized inventory/product test data.

---

### TC-CART-009 — Product can be removed from cart page

**Type:** Regression / Positive / UI\
**Priority:** High\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_cart_page.py`

**Preconditions:**

* User is logged in.
* User is on the inventory page.
* Selected product has been added to the cart.

**Test Data:**

* User: `standard_user`
* Example product: `Sauce Labs Backpack`

**Steps:**

1. Log in with valid credentials.
2. Add the selected product to the cart.
3. Open the cart page.
4. Click the Remove button for the selected product.
5. Observe the cart item list.

**Expected Result:**

* Selected product is removed from the cart.
* Removed product is no longer visible on the cart page.
* Cart page remains available.
* No error is displayed.

**Notes:**

* This scenario validates remove-from-cart behavior on the cart page.
* This test should not validate checkout behavior.

---

### TC-CART-010 — Cart badge is removed after removing last product

**Type:** Regression / UI\
**Priority:** Medium\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_cart_page.py`

**Preconditions:**

* User is logged in.
* User is on the inventory page.
* Exactly one product has been added to the cart.

**Test Data:**

* User: `standard_user`
* Example product: `Sauce Labs Backpack`

**Steps:**

1. Log in with valid credentials.
2. Add one selected product to the cart.
3. Open the cart page.
4. Remove the selected product from the cart.
5. Observe the cart badge.

**Expected Result:**

* Selected product is removed from the cart.
* Cart badge is no longer displayed after removing the last product.
* Cart item list no longer contains the removed product.

**Notes:**

* This scenario validates cart badge update after removing the last product.
* During automation, this scenario may be combined with remove-from-cart validation if it remains readable.

---

### TC-CART-011 — User can return from cart page to inventory page

**Type:** Regression / Navigation / UI\
**Priority:** Medium\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_cart_page.py`

**Preconditions:**

* User is logged in.
* User is on the cart page.

**Test Data:**

* User: `standard_user`

**Steps:**

1. Log in with valid credentials.
2. Open the cart page.
3. Click the Continue Shopping button.
4. Observe the inventory page.

**Expected Result:**

* User is returned to the inventory page.
* Inventory page URL contains `inventory.html`.
* Product list is visible.

**Notes:**

* This scenario validates navigation from the cart page back to the inventory page.
* This test should not validate checkout behavior.

---

### TC-CART-012 — Cart state persists after logout and re-login

**Type:** Regression / Positive / UI\
**Priority:** Medium\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_cart_page.py`

**Preconditions:**

* User is logged in.
* User is on the inventory page.
* Product list is visible.

**Test Data:**

* User: `standard_user`
* Example product: `Sauce Labs Backpack`

**Steps:**

1. Log in with valid credentials.
2. Add the selected product to the cart.
3. Log out from the application.
4. Log in again with the same valid user.
5. Open the cart page.
6. Observe the cart item list.

**Expected Result:**

* User is successfully logged in again.
* Inventory page is opened after re-login.
* Previously added product is still visible in the cart.
* Cart item list contains the previously added product.
* No error is displayed.

**Notes:**

* This scenario validates cart state persistence after logout and re-login.
* This test should use one deterministic product from centralized inventory product test data.
* This test should use the same user before and after logout.
* This test should not validate checkout behavior.
* This test should not validate browser restart, storage clearing, cross-user cart behavior, or persistence across different users.
* This test should not cover multiple logout locations unless a future task explicitly expands the scope.

---

### TC-CART-013 — Add to cart button changes to Remove after adding product from details page

**Type:** Regression / UI\
**Priority:** Medium\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_cart_page.py`

**Preconditions:**

* User is logged in.
* User is on the inventory page.
* Product list is visible.

**Test Data:**

* User: `standard_user`
* Example product: `Sauce Labs Backpack`

**Steps:**

1. Log in with valid credentials.
2. Find the selected product on the inventory page.
3. Open product details page.
4. Click the Add to cart button.
5. Observe the button on the product details page.

**Expected Result:**

* Product is added to the cart.
* Product details page remains open.
* Add to cart button changes to Remove for the tested product.
* Remove button is visible on the product details page.

**Notes:**

* This scenario validates product-details-side UI feedback after adding a product to the cart.
* This test should not validate cart page product content.