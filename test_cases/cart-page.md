# Cart Page — Test Cases

## Overview

This document contains manual test cases for the Sauce Demo cart page.

The goal of this document is to define cart-page-owned scenarios and track their automation coverage. Scenarios are documented here when the main action or validation happens on the cart page.

## Test Case Overview And Automation Coverage

| Test Case ID                                                                                      | Scenario                                                             | Type                         | Priority | Automation Status | Automated In              |
|---------------------------------------------------------------------------------------------------|----------------------------------------------------------------------|------------------------------|----------|-------------------|---------------------------|
| [TC-CART-001](#tc-cart-001--cart-is-empty-before-adding-products)                                 | Cart is empty before adding products                                 | Smoke / UI                   | Medium   | Automated         | `tests/test_cart_page.py` |
| [TC-CART-002](#tc-cart-002--added-product-is-displayed-on-cart-page)                              | Added product is displayed on cart page                              | Smoke / Positive / UI        | High     | Automated         | `tests/test_cart_page.py` |
| [TC-CART-003](#tc-cart-003--cart-product-content-matches-added-product-data)                      | Cart product content matches added product data                      | Regression / UI              | Medium   | Automated         | `tests/test_cart_page.py` |
| [TC-CART-004](#tc-cart-004--product-can-be-removed-from-cart-page)                                | Product can be removed from cart page                                | Smoke / Positive / UI        | High     | Automated         | `tests/test_cart_page.py` |
| [TC-CART-005](#tc-cart-005--cart-badge-is-removed-after-removing-last-product)                    | Cart badge is removed after removing last product                    | Regression / UI              | Medium   | Automated         | `tests/test_cart_page.py` |
| [TC-CART-006](#tc-cart-006--user-can-return-from-cart-page-to-inventory-page)                     | User can return from cart page to inventory page                     | Regression / Navigation / UI | Medium   | Automated         | `tests/test_cart_page.py` |
| [TC-CART-007](#tc-cart-007--cart-state-persists-after-logout-and-re-login)                        | Cart state persists after logout and re-login                        | Regression / Positive / UI   | Medium   | Automated         | `tests/test_cart_page.py` |
| [TC-CART-008](#tc-cart-008--all-added-products-are-displayed-on-cart-page)                        | All added products are displayed on cart page                        | Regression / Positive / UI   | Medium   | Automated         | `tests/test_cart_page.py` |
| [TC-CART-009](#tc-cart-009--cart-product-content-matches-added-product-data-for-each-product)     | Cart product content matches added product data for each product     | Regression / UI              | Medium   | Automated         | `tests/test_cart_page.py` |
| [TC-CART-010](#tc-cart-010--cart-badge-decrements-after-removing-one-of-multiple-products)        | Cart badge decrements after removing one of multiple products        | Regression / UI              | Medium   | Automated         | `tests/test_cart_page.py` |
| [TC-CART-011](#tc-cart-011--product-details-can-be-opened-from-cart-item-name)                    | Product details can be opened from cart item name                    | Regression / Navigation / UI | Medium   | Automated         | `tests/test_cart_page.py` |
| [TC-CART-012](#tc-cart-012--continue-shopping-preserves-cart-state)                               | Continue Shopping preserves cart state                               | Regression / Navigation / UI | Medium   | Automated         | `tests/test_cart_page.py` |
| [TC-CART-013](#tc-cart-013--all-products-can-be-removed-from-cart-page)                           | All products can be removed from cart page                           | Regression / Positive / UI   | Medium   | Automated         | `tests/test_cart_page.py` |
| [TC-CART-014](#tc-cart-014--checkout-button-opens-checkout-information-page-with-product-in-cart) | Checkout button opens checkout information page with product in cart | Smoke / Navigation / UI      | High     | Automated         | `tests/test_cart_page.py` |

---

## Test Cases

### TC-CART-001 — Cart is empty before adding products

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

### TC-CART-002 — Added product is displayed on cart page

**Type:** Smoke / Positive / UI\
**Priority:** High\
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
4. Observe the cart item list.

**Expected Result:**

* Cart page is opened.
* Selected product is visible on the cart page.
* Cart item list contains the selected product.

**Notes:**

* This scenario validates that an added product is displayed in the cart.
* This is treated as a smoke scenario because it validates the primary cart visibility flow for one representative product.
* Full all-products cart visibility regression coverage is tracked separately in TC-CART-008.

---

### TC-CART-003 — Cart product content matches added product data

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

* This scenario validates cart item content consistency for one representative product.
* During automation, expected product data should come from centralized product test data.
* Full all-products cart content regression coverage is tracked separately in TC-CART-009.

---

### TC-CART-004 — Product can be removed from cart page

**Type:** Smoke / Positive / UI\
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

* This scenario validates remove-from-cart behavior on the cart page for one representative product.
* Full all-products remove-from-cart regression coverage is tracked separately in TC-CART-013.
* This test should not validate checkout behavior.

---

### TC-CART-005 — Cart badge is removed after removing last product

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

### TC-CART-006 — User can return from cart page to inventory page

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
* Inventory page container is visible.
* Product list is visible.

**Notes:**

* This scenario validates basic navigation from the cart page back to the inventory page.
* Cart state after Continue Shopping is tracked separately in TC-CART-012.
* This test should not validate checkout behavior.

---

### TC-CART-007 — Cart state persists after logout and re-login

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
* This test should use one deterministic product from centralized product test data.
* This test should use the same user before and after logout.
* This test should not validate checkout behavior.
* This test should not validate browser restart, storage clearing, cross-user cart behavior, or persistence across different users.
* This test should not cover multiple logout locations unless a future task explicitly expands the scope.

---

### TC-CART-008 — All added products are displayed on cart page

**Type:** Regression / Positive / UI\
**Priority:** Medium\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_cart_page.py`

**Preconditions:**

* User is logged in.
* User is on the inventory page.
* Product list is visible.
* Cart is empty at the start of the test.

**Test Data:**

* User: `standard_user`
* Products: all products from the product test data set

**Steps:**

1. Log in with valid credentials.
2. Add all products from the product test data set to the cart.
3. Open the cart page.
4. Observe the cart item list.

**Expected Result:**

* Cart page is opened.
* Cart item count matches the number of added products.
* Every added product is displayed on the cart page.
* No unexpected product is displayed.
* No error is displayed.

**Notes:**

* This is the full regression variant of TC-CART-002.
* This scenario may use a loop or parametrized product data.

---

### TC-CART-009 — Cart product content matches added product data for each product

**Type:** Regression / UI\
**Priority:** Medium\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_cart_page.py`

**Preconditions:**

* User is logged in.
* User is on the inventory page.
* Product list is visible.
* Cart is empty at the start of each product check.

**Test Data:**

* User: `standard_user`
* Products: all products from the product test data set

**Steps:**

1. Log in with valid credentials.
2. For each product from the product test data set, add the tested product to the cart in an isolated test iteration.
3. Open the cart page.
4. Observe the cart item content for the tested product.

**Expected Result:**

* Tested cart item name matches the expected product name.
* Tested cart item description matches the expected product description.
* Tested cart item price matches the expected product price.
* Tested cart item quantity is visible.
* Tested cart item quantity displays `1`.
* Tested cart item has a visible Remove button.

**Notes:**

* This is the full regression variant of TC-CART-003.
* Expected product data should come from centralized product test data.

---

### TC-CART-010 — Cart badge decrements after removing one of multiple products

**Type:** Regression / UI\
**Priority:** Medium\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_cart_page.py`

**Preconditions:**

* User is logged in.
* User is on the inventory page.
* At least two products have been added to the cart.
* User is on the cart page.

**Test Data:**

* User: `standard_user`
* Example products:

  * `Sauce Labs Backpack`
  * `Sauce Labs Bolt T-Shirt`

**Steps:**

1. Log in with valid credentials.
2. Add two selected products to the cart.
3. Open the cart page.
4. Verify that the cart badge displays `2`.
5. Remove one selected product from the cart page.
6. Observe the cart badge.

**Expected Result:**

* Removed product is no longer displayed on the cart page.
* Remaining product is still displayed on the cart page.
* Cart badge count changes from `2` to `1`.
* Cart badge count matches the number of products still in the cart.

**Notes:**

* This scenario validates cart badge decrement after removing one product while another product remains in the cart.

---

### TC-CART-011 — Product details can be opened from cart item name

**Type:** Regression / Navigation / UI\
**Priority:** Medium\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_cart_page.py`

**Preconditions:**

* User is logged in.
* Selected product has been added to the cart.
* User is on the cart page.
* Cart item name is visible.

**Test Data:**

* User: `standard_user`
* Example product: `Sauce Labs Backpack`

**Steps:**

1. Log in with valid credentials.
2. Add the selected product to the cart.
3. Open the cart page.
4. Click the cart item product name.
5. Observe the product details page.

**Expected Result:**

* Product details page is opened for the selected product.
* Product details page URL contains the selected product ID.
* Product details page item details container is visible.
* Product details page belongs to the selected product.

**Notes:**

* This scenario is owned by Cart Page because the user action starts from `cart.html`.

---

### TC-CART-012 — Continue Shopping preserves cart state

**Type:** Regression / Navigation / UI\
**Priority:** Medium\
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
* Optional second product: `Sauce Labs Bolt T-Shirt`

**Steps:**

1. Log in with valid credentials.
2. Add the selected product to the cart.
3. Open the cart page.
4. Click the Continue Shopping button.
5. Observe the inventory page.
6. Observe the cart badge.
7. Observe the product card for the selected product.

**Expected Result:**

* User is returned to the inventory page.
* Inventory page URL contains `inventory.html`.
* Inventory page container is visible.
* Product list is visible.
* Cart badge still displays the expected number of products.
* Previously added product still displays the Remove button.
* Product not added to cart still displays the Add to cart button.

**Notes:**

* This scenario validates that navigation from cart back to inventory does not reset cart state.
* Basic Continue Shopping navigation is already covered by TC-CART-006.

---

### TC-CART-013 — All products can be removed from cart page

**Type:** Regression / Positive / UI\
**Priority:** Medium\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_cart_page.py`

**Preconditions:**

* User is logged in.
* User is on the inventory page.
* All products from the product test data set have been added to the cart before each product removal check.
* User is on the cart page.

**Test Data:**

* User: `standard_user`
* Products: all products from the product test data set

**Steps:**

1. Log in with valid credentials.
2. Add all products from the product test data set to the cart.
3. Open the cart page.
4. For each product from the product test data set, remove the tested product from the cart page in an isolated test iteration.
5. Observe the cart item list and cart badge.

**Expected Result:**

* The tested product can be removed from the cart page.
* Removed product is no longer displayed on the cart page.
* Cart badge count decreases by one after removing the tested product.
* Other products that were previously added to the cart are not negatively affected by removing the tested product.
* No error is displayed.

**Notes:**

* This is the full regression variant of TC-CART-004.

---

### TC-CART-014 — Checkout button opens checkout information page with product in cart

**Type:** Smoke / Navigation / UI\
**Priority:** High\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_cart_page.py`

**Preconditions:**

* User is logged in.
* User is on the inventory page.
* Selected product has been added to the cart.
* User is on the cart page.

**Test Data:**

* User: `standard_user`
* Example product: `Sauce Labs Backpack`

**Steps:**

1. Log in with valid credentials.
2. Add the selected product to the cart.
3. Open the cart page.
4. Click the Checkout button.

**Expected Result:**

* User is redirected to the checkout information page.
* Checkout information page URL contains `checkout-step-one.html`.
* Checkout information form is displayed.

**Notes:**

* This scenario is owned by Cart Page because the user action starts from the cart page.
* Checkout information form field behavior is documented in `test_cases/checkout-page.md`.
* Sauce Demo currently allows opening checkout step one from an empty cart, but this scenario uses the realistic checkout precondition: a product is present in the cart.
