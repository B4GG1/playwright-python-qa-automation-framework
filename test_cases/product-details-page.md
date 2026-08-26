# Product Details Page — Test Cases

## Overview

This document contains manual test cases for the Sauce Demo product details page.

The goal of this document is to define product-details-page-owned scenarios and track their automation coverage. Scenarios are documented here when the main action or validation happens on the product details page.

## Test Case Overview And Automation Coverage

| Test Case ID                                                                                                                          | Scenario                                                                           | Type                    | Priority | Automation Status | Automated In                         |
|---------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------|-------------------------|----------|-------------------|--------------------------------------|
| [TC-PRODUCT-DETAILS-001](#tc-product-details-001--product-details-content-is-displayed-for-selected-product)                          | Product details content is displayed for selected product                          | Smoke / UI              | High     | Automated         | `tests/test_product_details_page.py` |
| [TC-PRODUCT-DETAILS-002](#tc-product-details-002--product-details-content-matches-product-data-for-each-product)                      | Product details content matches product data for each product                      | Regression / UI         | Medium   | Automated         | `tests/test_product_details_page.py` |
| [TC-PRODUCT-DETAILS-003](#tc-product-details-003--user-can-return-from-product-details-to-inventory-page)                             | User can return from product details to inventory page                             | Navigation              | Medium   | Automated         | `tests/test_product_details_page.py` |
| [TC-PRODUCT-DETAILS-004](#tc-product-details-004--add-to-cart-button-changes-to-remove-after-adding-product-from-details-page)        | Add to cart button changes to Remove after adding product from details page        | Regression / UI         | Medium   | Automated         | `tests/test_product_details_page.py` |
| [TC-PRODUCT-DETAILS-005](#tc-product-details-005--product-can-be-added-to-cart-from-product-details-page)                             | Product can be added to cart from product details page                             | Smoke                   | High     | Automated         | `tests/test_product_details_page.py` |
| [TC-PRODUCT-DETAILS-006](#tc-product-details-006--all-products-can-be-added-to-cart-from-product-details-page)                        | All products can be added to cart from product details page                        | Regression              | Medium   | Automated         | `tests/test_product_details_page.py` |
| [TC-PRODUCT-DETAILS-007](#tc-product-details-007--product-can-be-removed-from-cart-from-product-details-page)                         | Product can be removed from cart from product details page                         | Smoke                   | High     | Automated         | `tests/test_product_details_page.py` |
| [TC-PRODUCT-DETAILS-008](#tc-product-details-008--remove-button-changes-back-to-add-to-cart-after-removing-product-from-details-page) | Remove button changes back to Add to cart after removing product from details page | Regression / UI         | Medium   | Automated         | `tests/test_product_details_page.py` |
| [TC-PRODUCT-DETAILS-009](#tc-product-details-009--cart-badge-is-displayed-after-adding-product-from-product-details-page)             | Cart badge is displayed after adding product from product details page             | Smoke / UI              | Medium   | Automated         | `tests/test_product_details_page.py` |
| [TC-PRODUCT-DETAILS-010](#tc-product-details-010--cart-badge-count-updates-after-adding-product-from-details-when-cart-is-not-empty)  | Cart badge count updates after adding product from details when cart is not empty  | Regression / UI         | Medium   | Automated         | `tests/test_product_details_page.py` |
| [TC-PRODUCT-DETAILS-011](#tc-product-details-011--cart-badge-count-updates-after-removing-one-of-multiple-products-from-details-page) | Cart badge count updates after removing one of multiple products from details page | Regression / UI         | Medium   | Automated         | `tests/test_product_details_page.py` |
| [TC-PRODUCT-DETAILS-012](#tc-product-details-012--cart-badge-disappears-after-removing-last-product-from-product-details-page)        | Cart badge disappears after removing last product from product details page        | Smoke / UI              | Medium   | Automated         | `tests/test_product_details_page.py` |
| [TC-PRODUCT-DETAILS-013](#tc-product-details-013--cart-page-can-be-opened-from-product-details-page)                                  | Cart page can be opened from product details page                                  | Smoke / Navigation      | Medium   | Automated         | `tests/test_product_details_page.py` |
| [TC-PRODUCT-DETAILS-014](#tc-product-details-014--all-products-can-be-removed-from-cart-from-product-details-page)                    | All products can be removed from cart from product details page                    | Regression              | Medium   | Automated         | `tests/test_product_details_page.py` |
| [TC-PRODUCT-DETAILS-015](#tc-product-details-015--cart-page-can-be-opened-from-product-details-page-for-each-product)                 | Cart page can be opened from product details page for each product                 | Regression / Navigation | Medium   | Planned           | TBD                                  |

---

## Test Cases

### TC-PRODUCT-DETAILS-001 — Product details content is displayed for selected product

**Type:** Smoke / UI\
**Priority:** High\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_product_details_page.py`

**Preconditions:**

* User is logged in.
* User can open a product details page.

**Test Data:**

* User: `standard_user`
* Example product: `Sauce Labs Backpack`

**Steps:**

1. Log in with valid credentials.
2. Open the selected product details page.
3. Observe the product details page content.

**Expected Result:**

* Product details page displays the selected product.
* Product name is visible.
* Product description is visible.
* Product price is visible.
* Product image is visible.
* Add to cart button is visible when the product has not been added to the cart.
* Back to products button is visible.

**Notes:**

* This is the representative smoke UI validation for product details content.
* Navigation from inventory to product details is covered separately by Inventory Page test cases and is not the classification target of this scenario.
* Full all-products content validation is covered by TC-PRODUCT-DETAILS-002.

---

### TC-PRODUCT-DETAILS-002 — Product details content matches product data for each product

**Type:** Regression / UI\
**Priority:** Medium\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_product_details_page.py`

**Preconditions:**

* User is logged in.
* Product details pages are available for products from the centralized product test data set.

**Test Data:**

* User: `standard_user`
* Products: all products from the product test data set

**Steps:**

1. Log in with valid credentials.
2. Open the product details page for each product in an isolated test iteration.
3. Observe the displayed product content.

**Expected Result:**

* Product details page displays the expected product.
* Product name matches centralized product test data.
* Product description matches centralized product test data.
* Product price matches centralized product test data.
* Product image matches centralized product test data.
* Add to cart button is visible for a product that has not been added to the cart.
* Back to products button is visible.

**Notes:**

* This is the full regression variant of TC-PRODUCT-DETAILS-001.
* The scenario validates product-details content for the complete applicable product data set.
* Navigation into product details is setup for this scenario and is covered separately under Inventory Page ownership.

---

### TC-PRODUCT-DETAILS-003 — User can return from product details to inventory page

**Type:** Navigation\
**Priority:** Medium\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_product_details_page.py`

**Preconditions:**

* User is logged in.
* User is on a product details page.

**Test Data:**

* User: `standard_user`
* Example product: `Sauce Labs Backpack`

**Steps:**

1. Open the selected product details page.
2. Verify that the expected product details page is open.
3. Click the Back to products button.

**Expected Result:**

* User is returned to the inventory page.
* Inventory page URL is displayed.
* Inventory container is visible.
* Product list is visible.

**Notes:**

* The primary purpose of this scenario is Product Details → Inventory navigation.
* Product details content and cart behavior are outside the main classification of this test case.

---

### TC-PRODUCT-DETAILS-004 — Add to cart button changes to Remove after adding product from details page

**Type:** Regression / UI\
**Priority:** Medium\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_product_details_page.py`

**Preconditions:**

* User is logged in.
* User is on the product details page.
* Selected product has not been added to the cart.

**Test Data:**

* User: `standard_user`
* Example product: `Sauce Labs Backpack`

**Steps:**

1. Open the selected product details page.
2. Verify that Add to cart is visible.
3. Verify that Remove is hidden.
4. Click Add to cart.
5. Observe the product controls.

**Expected Result:**

* Remove button becomes visible.
* Add to cart button becomes hidden.
* Product details page remains open for the selected product.

**Notes:**

* This scenario validates detailed UI state change after adding a product.
* Core add-to-cart functionality is covered by TC-PRODUCT-DETAILS-005 and TC-PRODUCT-DETAILS-006.

---

### TC-PRODUCT-DETAILS-005 — Product can be added to cart from product details page

**Type:** Smoke\
**Priority:** High\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_product_details_page.py`

**Preconditions:**

* User is logged in.
* Selected product has not been added to the cart.

**Test Data:**

* User: `standard_user`
* Example product: `Sauce Labs Backpack`

**Steps:**

1. Open the selected product details page.
2. Add the product to the cart.
3. Verify the updated cart state.
4. Open the cart page to verify the result.

**Expected Result:**

* Product can be added to the cart from the product details page.
* Cart badge displays `1`.
* Selected product is present in the cart.
* No error occurs during the operation.

**Notes:**

* This is the representative smoke validation of product-details-side add-to-cart functionality.
* Opening the cart is used to verify the business result and is not the navigation focus of this scenario.
* Full product coverage is provided by TC-PRODUCT-DETAILS-006.

---

### TC-PRODUCT-DETAILS-006 — All products can be added to cart from product details page

**Type:** Regression\
**Priority:** Medium\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_product_details_page.py`

**Preconditions:**

* User is logged in.
* Cart starts empty for each independent product iteration.
* Product details pages are available for all products from centralized test data.

**Test Data:**

* User: `standard_user`
* Products: all products from the product test data set

**Steps:**

1. Open the tested product details page.
2. Add the tested product to the cart.
3. Verify that the product details page remains open.
4. Verify the cart badge.
5. Open the cart page.
6. Verify the tested product is present.
7. Repeat independently for every applicable product.

**Expected Result:**

* Every tested product can be added to the cart from its product details page.
* Cart badge displays `1` for each isolated iteration.
* Cart page contains the tested product.

**Notes:**

* This is the full regression variant of TC-PRODUCT-DETAILS-005.
* Cart navigation performed during result verification is not the primary classification of this scenario.

---

### TC-PRODUCT-DETAILS-007 — Product can be removed from cart from product details page

**Type:** Smoke\
**Priority:** High\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_product_details_page.py`

**Preconditions:**

* User is logged in.
* One representative product has already been added to the cart.

**Test Data:**

* User: `standard_user`
* Example product: representative product from centralized test data

**Steps:**

1. Open the product details page for the product currently in the cart.
2. Click Remove.
3. Verify the updated cart state.
4. Open the cart page to verify the result.

**Expected Result:**

* Product is removed from the cart.
* Cart badge is no longer visible when the removed product was the only cart item.
* Removed product is not present on the cart page.

**Notes:**

* This is the representative smoke validation of product-details-side remove-from-cart functionality.
* Opening the cart is used only to verify the removal result.
* Full product regression coverage is provided by TC-PRODUCT-DETAILS-014.

---

### TC-PRODUCT-DETAILS-008 — Remove button changes back to Add to cart after removing product from details page

**Type:** Regression / UI\
**Priority:** Medium\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_product_details_page.py`

**Preconditions:**

* User is logged in.
* User is on the product details page.
* Selected product can be added to the cart.

**Test Data:**

* User: `standard_user`
* Example product: `Sauce Labs Backpack`

**Steps:**

1. Add the selected product to the cart.
2. Verify that Remove is visible.
3. Verify that Add to cart is hidden.
4. Remove the product.
5. Observe the product controls.

**Expected Result:**

* Remove button becomes hidden.
* Add to cart button becomes visible again.
* Product details page remains open for the selected product.

**Notes:**

* This scenario validates detailed UI feedback after removing a product.
* It is the reverse-state counterpart of TC-PRODUCT-DETAILS-004.

---

### TC-PRODUCT-DETAILS-009 — Cart badge is displayed after adding product from product details page

**Type:** Smoke / UI\
**Priority:** Medium\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_product_details_page.py`

**Preconditions:**

* User is logged in.
* Cart is empty.
* Selected product has not been added to the cart.

**Test Data:**

* User: `standard_user`
* Example product: `Sauce Labs Backpack`

**Steps:**

1. Open the selected product details page.
2. Verify that the cart badge is not visible.
3. Add the product to the cart.
4. Observe the cart badge.

**Expected Result:**

* Cart badge becomes visible.
* Cart badge displays `1`.

**Notes:**

* This is the representative smoke UI validation of the cart badge after a product-details-side add action.
* Broader badge-count behavior is covered by TC-PRODUCT-DETAILS-010.

---

### TC-PRODUCT-DETAILS-010 — Cart badge count updates after adding product from details when cart is not empty

**Type:** Regression / UI\
**Priority:** Medium\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_product_details_page.py`

**Preconditions:**

* User is logged in.
* Cart starts empty.
* At least two products are available.

**Test Data:**

* User: `standard_user`
* First example product: first product from centralized product test data
* Second example product: second product from centralized product test data

**Steps:**

1. Open the first product details page.
2. Add the first product to the cart.
3. Verify that the cart badge displays `1`.
4. Return to the inventory page.
5. Open the second product details page.
6. Add the second product to the cart.
7. Observe the cart badge.

**Expected Result:**

* Cart badge displays `1` after adding the first product.
* Cart badge updates to `2` after adding the second product.
* Badge count matches the number of products currently in the cart.

**Notes:**

* This is the broader regression variant of cart badge add-state behavior.
* Intermediate page transitions are setup actions required to test multiple products and are not the classification target.

---

### TC-PRODUCT-DETAILS-011 — Cart badge count updates after removing one of multiple products from details page

**Type:** Regression / UI\
**Priority:** Medium\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_product_details_page.py`

**Preconditions:**

* User is logged in.
* Two products have been added to the cart.

**Test Data:**

* User: `standard_user`
* First example product: first product from centralized product test data
* Second example product: second product from centralized product test data

**Steps:**

1. Add two products to the cart.
2. Open the product details page for one of the added products.
3. Verify that the cart badge displays `2`.
4. Remove the selected product.
5. Observe the cart badge.

**Expected Result:**

* Cart badge count decreases from `2` to `1`.
* Badge count matches the number of products remaining in the cart.

**Notes:**

* This scenario validates detailed cart badge state after removing one of multiple products.

---

### TC-PRODUCT-DETAILS-012 — Cart badge disappears after removing last product from product details page

**Type:** Smoke / UI\
**Priority:** Medium\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_product_details_page.py`

**Preconditions:**

* User is logged in.
* Cart starts empty.

**Test Data:**

* User: `standard_user`
* Example product: `Sauce Labs Backpack`

**Steps:**

1. Open the selected product details page.
2. Verify that the cart badge is hidden.
3. Add the product to the cart.
4. Verify that the cart badge is visible and displays `1`.
5. Remove the product.
6. Observe the cart badge.

**Expected Result:**

* Cart badge appears after adding the product.
* Cart badge displays `1`.
* Cart badge disappears after removing the last product.

**Notes:**

* This is the representative smoke UI validation of the empty-cart badge state after removal.
* Partial decrement behavior with multiple products is covered by TC-PRODUCT-DETAILS-011.

---

### TC-PRODUCT-DETAILS-013 — Cart page can be opened from product details page

**Type:** Smoke / Navigation\
**Priority:** Medium\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_product_details_page.py`

**Preconditions:**

* User is logged in.
* User can open a product details page.

**Test Data:**

* User: `standard_user`
* Example product: `Sauce Labs Backpack`

**Steps:**

1. Open the selected product details page.
2. Click the cart link.
3. Observe the cart page.

**Expected Result:**

* Cart page is opened.
* Cart page URL is displayed.
* Cart contents container is visible.

**Notes:**

* This is the representative smoke navigation scenario for Product Details → Cart.
* The scenario validates navigation itself rather than cart contents.
* Full all-products navigation coverage is defined by TC-PRODUCT-DETAILS-015.

---

### TC-PRODUCT-DETAILS-014 — All products can be removed from cart from product details page

**Type:** Regression\
**Priority:** Medium\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_product_details_page.py`

**Preconditions:**

* User is logged in.
* All products from the centralized product data set can be added to the cart.

**Test Data:**

* User: `standard_user`
* Products: all products from the product test data set

**Steps:**

1. Add all applicable products to the cart.
2. Open the tested product details page.
3. Remove that product from the cart.
4. Verify that the cart badge count decreases by one.
5. Open the cart page.
6. Verify that the removed product is absent.
7. Repeat independently for every applicable product.

**Expected Result:**

* Every tested product can be removed from the cart from its product details page.
* Cart badge count decreases by one.
* Removed product is not present on the cart page.
* Remaining cart products are not removed by the tested action.

**Notes:**

* This is the full regression variant of TC-PRODUCT-DETAILS-007.
* Opening the cart is used to validate the removal result and is not the navigation focus of this scenario.

---

### TC-PRODUCT-DETAILS-015 — Cart page can be opened from product details page for each product

**Type:** Regression / Navigation\
**Priority:** Medium\
**Automation Candidate:** Yes\
**Automation Status:** Planned\
**Automated In:** TBD

**Preconditions:**

* User is logged in.
* Product details pages are available for all products from the centralized product test data set.

**Test Data:**

* User: `standard_user`
* Products: all products from the product test data set

**Steps:**

1. Open the product details page for the tested product.
2. Click the cart link.
3. Observe the cart page.
4. Repeat the scenario independently for every product from the product test data set.

**Expected Result:**

* Cart page can be opened from every tested product details page.
* Cart page URL is displayed after each transition.
* Cart contents container is visible after each transition.
* Navigation behavior is consistent regardless of which product details page is used as the starting point.

**Notes:**

* This is the full regression navigation counterpart of TC-PRODUCT-DETAILS-013.
* The automated implementation should use parametrized product data so every applicable product details page is covered.
* The scenario validates Product Details → Cart navigation only.
* Product add-to-cart, remove-from-cart, and cart content behavior are covered by separate test cases.