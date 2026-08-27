# Cart Page — Test Cases

## Overview

This document contains manual test cases for the Sauce Demo cart page.

The goal of this document is to define cart-page-owned scenarios and track their automation coverage. Scenarios are documented here when the main action or validation happens on the cart page.

## Test Case Overview And Automation Coverage

| Test Case ID                                                                                      | Scenario                                                                    | Type                     | Priority | Automation Status | Automated In              |
|---------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------|--------------------------|----------|-------------------|---------------------------|
| [TC-CART-001](#tc-cart-001--cart-is-empty-before-adding-products)                                 | Cart is empty before adding products                                        | Smoke                    | Medium   | Automated         | `tests/test_cart_page.py` |
| [TC-CART-002](#tc-cart-002--added-product-is-displayed-with-correct-content-on-cart-page)         | Added product is displayed with correct content on cart page                | Smoke / UI / E2E         | High     | Automated         | `tests/test_cart_page.py` |
| [TC-CART-003](#tc-cart-003--product-can-be-removed-from-cart-page)                                | Product can be removed from cart page                                       | Smoke                    | High     | Automated         | `tests/test_cart_page.py` |
| [TC-CART-004](#tc-cart-004--cart-badge-is-removed-after-removing-last-product)                    | Cart badge is removed after removing last product                           | Regression / UI          | Medium   | Automated         | `tests/test_cart_page.py` |
| [TC-CART-005](#tc-cart-005--user-can-continue-shopping-from-cart-page)                            | User can continue shopping from cart page                                   | Navigation               | Medium   | Automated         | `tests/test_cart_page.py` |
| [TC-CART-006](#tc-cart-006--cart-state-persists-after-logout-and-re-login)                        | Cart state persists after logout and re-login                               | Regression               | Medium   | Automated         | `tests/test_cart_page.py` |
| [TC-CART-007](#tc-cart-007--all-added-products-are-displayed-with-correct-content-on-cart-page)   | All added products are displayed with correct content on cart page          | Regression / UI          | Medium   | Automated         | `tests/test_cart_page.py` |
| [TC-CART-008](#tc-cart-008--cart-badge-decrements-after-removing-one-of-multiple-products)        | Cart badge decrements after removing one of multiple products               | Regression / UI          | Medium   | Automated         | `tests/test_cart_page.py` |
| [TC-CART-009](#tc-cart-009--product-details-can-be-opened-from-cart-item-name)                    | Product details can be opened from cart item name                           | Navigation               | Medium   | Automated         | `tests/test_cart_page.py` |
| [TC-CART-010](#tc-cart-010--continue-shopping-preserves-cart-state)                               | Continue Shopping preserves cart state                                      | Regression / UI          | Medium   | Automated         | `tests/test_cart_page.py` |
| [TC-CART-011](#tc-cart-011--all-products-can-be-removed-from-cart-page)                           | All products can be removed from cart page                                  | Regression               | Medium   | Automated         | `tests/test_cart_page.py` |
| [TC-CART-012](#tc-cart-012--checkout-button-opens-checkout-information-page-with-product-in-cart) | Checkout button opens checkout information page with product in cart        | Smoke / Navigation / E2E | High     | Automated         | `tests/test_cart_page.py` |

---

## Test Cases

### TC-CART-001 — Cart is empty before adding products

**Type:** Smoke\
**Priority:** Medium\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_cart_page.py`

**Preconditions:**

* User is logged in.
* No products have been added to the cart in the current session.

**Test Data:**

* User: `standard_user`

**Steps:**

1. Log in with valid credentials.
2. Verify that no cart badge is displayed before adding products.
3. Open the cart page.
4. Observe the cart item list.

**Expected Result:**

* Cart page opens successfully.
* No cart badge is displayed.
* Cart contains zero product items.

**Notes:**

* This scenario validates the initial empty-cart state.
* The scenario focuses on cart state rather than general cart-page UI presentation.

---

### TC-CART-002 — Added product is displayed with correct content on cart page

**Type:** Smoke / UI / E2E\
**Priority:** High\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_cart_page.py`

**Preconditions:**

* User is logged in.
* One representative product has been added to the cart.

**Test Data:**

* User: `standard_user`
* Example product: representative product from centralized product test data

**Steps:**

1. Log in with valid credentials.
2. Add one representative product to the cart.
3. Open the cart page.
4. Locate the added product.
5. Verify the product content displayed in the cart.

**Expected Result:**

* Added product is visible on the cart page.
* Product name matches the expected product data.
* Product description matches the expected product data.
* Product price matches the expected product data.
* Product quantity displays `1`.
* Remove button is available for the product.

**Notes:**

* This is the representative smoke validation of cart contents.
* This test is part of the primary E2E purchase flow.
* Full all-products cart content coverage is provided by TC-CART-007.

---

### TC-CART-003 — Product can be removed from cart page

**Type:** Smoke\
**Priority:** High\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_cart_page.py`

**Preconditions:**

* User is logged in.
* One representative product has been added to the cart.
* User is on the cart page.

**Test Data:**

* User: `standard_user`
* Example product: representative product from centralized product test data

**Steps:**

1. Open the cart containing one product.
2. Verify that the selected product is visible.
3. Click Remove for the selected product.
4. Observe the cart item list.

**Expected Result:**

* Selected product is removed from the cart.
* Removed product is no longer visible on the cart page.

**Notes:**

* This is the representative smoke validation of remove-from-cart behavior.
* Full all-products removal coverage is provided by TC-CART-011.

---

### TC-CART-004 — Cart badge is removed after removing last product

**Type:** Regression / UI\
**Priority:** Medium\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_cart_page.py`

**Preconditions:**

* User is logged in.
* Exactly one product has been added to the cart.
* User is on the cart page.

**Test Data:**

* User: `standard_user`
* Example product: representative product from centralized product test data

**Steps:**

1. Open the cart containing one product.
2. Verify that the cart badge is visible and displays `1`.
3. Verify that the product is visible.
4. Remove the product.
5. Observe the cart badge and cart item.

**Expected Result:**

* Cart badge disappears after removing the last product.
* Removed product is no longer visible in the cart.

**Notes:**

* This scenario validates detailed cart badge state after the cart becomes empty.
* Cart badge behavior is shared authenticated-page behavior and may be reorganized into dedicated shared-header coverage in a future approved task.

---

### TC-CART-005 — User can continue shopping from cart page

**Type:** Navigation\
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

1. Open the cart page.
2. Click Continue Shopping.
3. Observe the destination page.

**Expected Result:**

* User is returned to the inventory page.
* Inventory page URL is displayed.
* Product list is visible.

**Notes:**

* The primary purpose of this scenario is Cart → Inventory navigation.
* Cart-state preservation after Continue Shopping is covered separately by TC-CART-010.

---

### TC-CART-006 — Cart state persists after logout and re-login

**Type:** Regression\
**Priority:** Medium\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_cart_page.py`

**Preconditions:**

* User is logged in.
* One representative product has been added to the cart.

**Test Data:**

* User: `standard_user`
* Example product: representative product from centralized product test data

**Steps:**

1. Add one product to the cart.
2. Verify that the product is marked as added.
3. Open the cart and verify that the product is present.
4. Return to the inventory page.
5. Log out.
6. Log in again using the same user.
7. Verify the cart state after re-login.
8. Open the cart again.

**Expected Result:**

* User can log in again successfully.
* Previously added product remains in the cart after re-login.
* Cart badge displays `1`.
* Product state remains consistent on the inventory page.
* Product is still visible on the cart page.

**Notes:**

* This scenario validates cart-state persistence across logout and re-login for the same user.
* The test does not cover browser restart, storage clearing, cross-user behavior, or different-user persistence.

---

### TC-CART-007 — All added products are displayed with correct content on cart page

**Type:** Regression / UI\
**Priority:** Medium\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_cart_page.py`

**Preconditions:**

* User is logged in.
* Cart is empty at the start of the test.
* All products from centralized product test data are available.

**Test Data:**

* User: `standard_user`
* Products: all products from the product test data set

**Steps:**

1. Add all products from the product test data set to the cart.
2. Open the cart page.
3. Verify the number of displayed cart items.
4. For each product, verify its cart item content.

**Expected Result:**

* Cart item count matches the number of added products.
* Every added product is visible in the cart.
* Every product name matches centralized product data.
* Every product description matches centralized product data.
* Every product price matches centralized product data.
* Every product quantity displays `1`.
* Every product has an available Remove button.

**Notes:**

* This is the full regression counterpart of TC-CART-002.
* This scenario combines previous all-products visibility and all-products content-validation coverage into one test case.

---

### TC-CART-008 — Cart badge decrements after removing one of multiple products

**Type:** Regression / UI\
**Priority:** Medium\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_cart_page.py`

**Preconditions:**

* User is logged in.
* At least two products are available.

**Test Data:**

* User: `standard_user`
* First example product: first product from centralized product test data
* Second example product: second product from centralized product test data

**Steps:**

1. Add two products to the cart.
2. Open the cart page.
3. Verify that the cart badge displays `2`.
4. Remove one of the products.
5. Observe the cart badge and cart contents.

**Expected Result:**

* Cart badge decreases from `2` to `1`.
* Removed product is no longer visible.
* Remaining product is still visible.

**Notes:**

* This scenario validates detailed cart badge behavior when removing one item from a non-empty cart.

---

### TC-CART-009 — Product details can be opened from cart item name

**Type:** Navigation\
**Priority:** Medium\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_cart_page.py`

**Preconditions:**

* User is logged in.
* One product has been added to the cart.
* User is on the cart page.

**Test Data:**

* User: `standard_user`
* Example product: representative product from centralized product test data

**Steps:**

1. Open the cart page containing the selected product.
2. Click the product name.
3. Observe the product details page.

**Expected Result:**

* Product details page opens for the selected product.
* Product details page URL contains the expected product ID.
* Product details item is visible.
* Back to products button is visible.

**Notes:**

* The primary purpose of this scenario is Cart → Product Details navigation.

---

### TC-CART-010 — Continue Shopping preserves cart state

**Type:** Regression / UI\
**Priority:** Medium\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_cart_page.py`

**Preconditions:**

* User is logged in.
* One product has been added to the cart.
* At least one additional product is available.

**Test Data:**

* User: `standard_user`
* Added product: representative product from centralized product test data
* Optional product: second representative product from centralized product test data

**Steps:**

1. Add one product to the cart.
2. Open the cart page.
3. Click Continue Shopping.
4. Observe the inventory page.
5. Verify the cart badge.
6. Verify the state of the previously added product.
7. Verify the state of a product that was not added.

**Expected Result:**

* User returns to the inventory page.
* Inventory page remains available.
* Cart badge still displays `1`.
* Previously added product displays Remove.
* Previously added product does not display Add to cart.
* Product not added to the cart displays Add to cart.
* Product not added to the cart does not display Remove.

**Notes:**

* The scenario validates preservation of cart-related UI state after Continue Shopping.
* Navigation is required to perform the scenario but cart-state preservation is the primary validation target.

---

### TC-CART-011 — All products can be removed from cart page

**Type:** Regression\
**Priority:** Medium\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_cart_page.py`

**Preconditions:**

* User is logged in.
* All products from centralized product test data can be added to the cart.

**Test Data:**

* User: `standard_user`
* Products: all products from the product test data set

**Steps:**

1. Add all products from the product test data set to the cart.
2. Open the cart page.
3. Verify the initial cart badge count.
4. Remove the tested product.
5. Verify the updated cart badge count.
6. Verify that the tested product is no longer visible.
7. Repeat independently for every applicable product.

**Expected Result:**

* Every tested product can be removed from the cart.
* Cart badge decreases by one after each isolated removal check.
* Removed product is no longer visible on the cart page.

**Notes:**

* This is the full regression counterpart of TC-CART-003.
* The automated implementation uses parametrized product data to cover every applicable product.

---

### TC-CART-012 — Checkout button opens checkout information page with product in cart

**Type:** Smoke / Navigation / E2E\
**Priority:** High\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_cart_page.py`

**Preconditions:**

* User is logged in.
* One representative product has been added to the cart.
* User is on the cart page.

**Test Data:**

* User: `standard_user`
* Example product: representative product from centralized product test data

**Steps:**

1. Open the cart containing the selected product.
2. Click Checkout.
3. Observe the checkout information page.

**Expected Result:**

* Checkout information page opens successfully.
* Checkout information page URL is displayed.
* Checkout information form container is visible.
* Cart contents container is no longer visible.

**Notes:**

* The primary purpose of this scenario is Cart → Checkout Information navigation.
* This scenario is a required checkpoint in the primary E2E purchase flow.
* Product presence and content in the cart are validated earlier in TC-CART-002.