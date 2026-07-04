# Product Details Page — Test Cases

## Overview

This document contains manual test cases for the Sauce Demo product details page.

The goal of this document is to define product-details-page-owned scenarios and track their automation coverage. Scenarios are documented here when the main action or validation happens on the product details page.

## Test Case Overview And Automation Coverage

| Test Case ID                                                                                                                          | Scenario                                                                           | Type                         | Priority | Automation Status | Automated In                         |
|---------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------|------------------------------|----------|-------------------|--------------------------------------|
| [TC-PRODUCT-DETAILS-001](#tc-product-details-001--product-details-content-is-displayed-for-selected-product)                          | Product details content is displayed for selected product                          | Smoke / UI                   | High     | Automated         | `tests/test_product_details_page.py` |
| [TC-PRODUCT-DETAILS-002](#tc-product-details-002--product-details-content-matches-product-data-for-each-product)                      | Product details content matches product data for each product                      | Regression / UI              | Medium   | Automated         | `tests/test_product_details_page.py` |
| [TC-PRODUCT-DETAILS-003](#tc-product-details-003--user-can-return-from-product-details-to-inventory-page)                             | User can return from product details to inventory page                             | Regression / Navigation / UI | Medium   | Automated         | `tests/test_product_details_page.py` |
| [TC-PRODUCT-DETAILS-004](#tc-product-details-004--add-to-cart-button-changes-to-remove-after-adding-product-from-details-page)        | Add to cart button changes to Remove after adding product from details page        | Regression / UI              | Medium   | Automated         | `tests/test_product_details_page.py` |
| [TC-PRODUCT-DETAILS-005](#tc-product-details-005--product-can-be-added-to-cart-from-product-details-page)                             | Product can be added to cart from product details page                             | Smoke / Positive / UI        | High     | Automated         | `tests/test_product_details_page.py` |
| [TC-PRODUCT-DETAILS-006](#tc-product-details-006--all-products-can-be-added-to-cart-from-product-details-page)                        | All products can be added to cart from product details page                        | Regression / Positive / UI   | Medium   | Automated         | `tests/test_product_details_page.py` |
| [TC-PRODUCT-DETAILS-007](#tc-product-details-007--product-can-be-removed-from-cart-from-product-details-page)                         | Product can be removed from cart from product details page                         | Smoke / Positive / UI        | High     | Automated         | `tests/test_product_details_page.py` |
| [TC-PRODUCT-DETAILS-008](#tc-product-details-008--remove-button-changes-back-to-add-to-cart-after-removing-product-from-details-page) | Remove button changes back to Add to cart after removing product from details page | Regression / UI              | Medium   | Automated         | `tests/test_product_details_page.py` |
| [TC-PRODUCT-DETAILS-009](#tc-product-details-009--cart-badge-is-displayed-after-adding-product-from-product-details-page)             | Cart badge is displayed after adding product from product details page             | Regression / UI              | Medium   | Automated         | `tests/test_product_details_page.py` |
| [TC-PRODUCT-DETAILS-010](#tc-product-details-010--cart-badge-count-updates-after-adding-product-from-details-when-cart-is-not-empty)  | Cart badge count updates after adding product from details when cart is not empty  | Regression / UI              | Medium   | Automated         | `tests/test_product_details_page.py` |
| [TC-PRODUCT-DETAILS-011](#tc-product-details-011--cart-badge-count-updates-after-removing-one-of-multiple-products-from-details-page) | Cart badge count updates after removing one of multiple products from details page | Regression / UI              | Medium   | Automated         | `tests/test_product_details_page.py` |
| [TC-PRODUCT-DETAILS-012](#tc-product-details-012--cart-badge-disappears-after-removing-last-product-from-product-details-page)        | Cart badge disappears after removing last product from product details page        | Regression / UI              | Medium   | Automated         | `tests/test_product_details_page.py` |
| [TC-PRODUCT-DETAILS-013](#tc-product-details-013--cart-page-can-be-opened-from-product-details-page)                                  | Cart page can be opened from product details page                                  | Regression / Navigation / UI | Medium   | Automated         | `tests/test_product_details_page.py` |
| [TC-PRODUCT-DETAILS-014](#tc-product-details-014--all-products-can-be-removed-from-cart-from-product-details-page)                    | All products can be removed from cart from product details page                    | Regression / Positive / UI   | Medium   | Automated         | `tests/test_product_details_page.py` |

---

## Test Cases

### TC-PRODUCT-DETAILS-001 — Product details content is displayed for selected product

**Type:** Smoke / UI
**Priority:** High
**Automation Candidate:** Yes
**Automation Status:** Automated
**Automated In:** `tests/test_product_details_page.py`

**Preconditions:**

* User is logged in.
* User has opened a product details page.

**Test Data:**

* User: `standard_user`
* Example product: `Sauce Labs Backpack`

**Steps:**

1. Log in with valid credentials.
2. Open the selected product details page.
3. Observe the product details page content.

**Expected Result:**

* Product details page item details container is visible.
* Product name is visible.
* Product description is visible.
* Product price is visible.
* Product image is visible.
* Add to cart button is visible when the product has not been added to cart.

**Notes:**

* This scenario validates product details content visibility for one representative product.

---

### TC-PRODUCT-DETAILS-002 — Product details content matches product data for each product

**Type:** Regression / UI
**Priority:** Medium
**Automation Candidate:** Yes
**Automation Status:** Automated
**Automated In:** `tests/test_product_details_page.py`

**Preconditions:**

* User is logged in.
* User can open product details pages for products from the product test data set.

**Test Data:**

* User: `standard_user`
* Products: all products from the product test data set

**Steps:**

1. Log in with valid credentials.
2. For each product from the product test data set, open the product details page.
3. Observe the product details page content.

**Expected Result:**

* Product details page displays the selected product name.
* Product details page displays the selected product description.
* Product details page displays the selected product price.
* Product details page displays the selected product image.
* Product details page displays the Add to cart button when the product has not been added to cart.
* Product details content matches centralized product test data.

**Notes:**

* This is the full regression variant of TC-PRODUCT-DETAILS-001.
* This scenario should remain focused on product details page content, not cart behavior.

---

### TC-PRODUCT-DETAILS-003 — User can return from product details to inventory page

**Type:** Regression / Navigation / UI
**Priority:** Medium
**Automation Candidate:** Yes
**Automation Status:** Automated
**Automated In:** `tests/test_product_details_page.py`

**Preconditions:**

* User is logged in.
* User is on a product details page.

**Test Data:**

* User: `standard_user`
* Example product: `Sauce Labs Backpack`

**Steps:**

1. Log in with valid credentials.
2. Open product details from the inventory page.
3. Click the Back to products button.

**Expected Result:**

* User is returned to the inventory page.
* Inventory page URL contains `inventory.html`.
* Inventory container is visible.
* Product list is visible.

**Notes:**

* This scenario validates navigation back from product details to the inventory page.
* This test should not validate cart behavior.
* One representative product is enough because product details entry paths are tracked separately under Inventory Page ownership.

---

### TC-PRODUCT-DETAILS-004 — Add to cart button changes to Remove after adding product from details page

**Type:** Regression / UI
**Priority:** Medium
**Automation Candidate:** Yes
**Automation Status:** Automated
**Automated In:** `tests/test_product_details_page.py`

**Preconditions:**

* User is logged in.
* User is on the product details page.
* Product details page displays the selected product.

**Test Data:**

* User: `standard_user`
* Example product: `Sauce Labs Backpack`

**Steps:**

1. Log in with valid credentials.
2. Find the selected product on the inventory page.
3. Open the product details page.
4. Click the Add to cart button.
5. Observe the button on the product details page.

**Expected Result:**

* Product is added to the cart.
* Product details page remains open.
* Add to cart button changes to Remove for the tested product.
* Remove button is visible on the product details page.

**Notes:**

* This scenario validates product-details-side UI feedback after adding a product to the cart.
* Core add-to-cart behavior from product details page is tracked separately in TC-PRODUCT-DETAILS-005.
* Cart badge behavior is tracked separately in TC-PRODUCT-DETAILS-009 and TC-PRODUCT-DETAILS-010.

---

### TC-PRODUCT-DETAILS-005 — Product can be added to cart from product details page

**Type:** Smoke / Positive / UI
**Priority:** High
**Automation Candidate:** Yes
**Automation Status:** Automated
**Automated In:** `tests/test_product_details_page.py`

**Preconditions:**

* User is logged in.
* User is on the product details page.
* Selected product has not been added to cart.

**Test Data:**

* User: `standard_user`
* Example product: `Sauce Labs Backpack`

**Steps:**

1. Log in with valid credentials.
2. Open the selected product details page.
3. Click the Add to cart button on the product details page.
4. Observe the product details page.

**Expected Result:**

* Product is added to the cart from the product details page.
* Product details page remains open.
* No error is displayed.
* Product details page reflects the updated cart state for the selected product.

**Notes:**

* This scenario validates the core add-to-cart action initiated from the product details page for one representative product.
* Button state is covered separately in TC-PRODUCT-DETAILS-004.
* Cart badge behavior is covered separately in TC-PRODUCT-DETAILS-009 and TC-PRODUCT-DETAILS-010.
* Cart page item validation remains owned by `cart-page.md`.

---

### TC-PRODUCT-DETAILS-006 — All products can be added to cart from product details page

**Type:** Regression / Positive / UI
**Priority:** Medium
**Automation Candidate:** Yes
**Automation Status:** Automated
**Automated In:** `tests/test_product_details_page.py`

**Preconditions:**

* User is logged in.
* User can open product details pages for products from the product test data set.
* Cart is empty at the start of each product check.

**Test Data:**

* User: `standard_user`
* Products: all products from the product test data set

**Steps:**

1. Log in with valid credentials.
2. For each product from the product test data set, open that product details page in an isolated test iteration.
3. Click the Add to cart button on the product details page.
4. Observe the product details page, cart badge, and cart page item list.

**Expected Result:**

* The tested product can be added to the cart from its product details page.
* Add to cart action does not display an error.
* Product details page remains open after adding the product.
* Cart badge displays `1` for the tested product iteration.
* The tested product is visible on the cart page.

---

### TC-PRODUCT-DETAILS-007 — Product can be removed from cart from product details page

**Type:** Smoke / Positive / UI
**Priority:** High
**Automation Candidate:** Yes
**Automation Status:** Automated
**Automated In:** `tests/test_product_details_page.py`

**Preconditions:**

* User is logged in.
* User is on the product details page.
* Selected product has already been added to cart.

**Test Data:**

* User: `standard_user`
* Example product: `Sauce Labs Backpack`

**Steps:**

1. Log in with valid credentials.
2. Open the selected product details page.
3. Add the selected product to the cart if it is not already added.
4. Click the Remove button on the product details page.
5. Observe the product details page.

**Expected Result:**

* Product is removed from the cart from the product details page.
* Product details page remains open.
* No error is displayed.
* Product details page reflects the updated cart state for the selected product.

**Notes:**

* This scenario validates the core remove-from-cart action initiated from the product details page for one representative product.
* Full all-products remove-from-cart regression coverage is tracked separately in TC-PRODUCT-DETAILS-014.
* Button state after removal is covered separately in TC-PRODUCT-DETAILS-008.
* Cart badge behavior after removal is covered separately in TC-PRODUCT-DETAILS-011 and TC-PRODUCT-DETAILS-012.
* Cart page item validation remains owned by `cart-page.md`.

---

### TC-PRODUCT-DETAILS-008 — Remove button changes back to Add to cart after removing product from details page

**Type:** Regression / UI
**Priority:** Medium
**Automation Candidate:** Yes
**Automation Status:** Automated
**Automated In:** `tests/test_product_details_page.py`

**Preconditions:**

* User is logged in.
* User is on the product details page.
* Selected product has already been added to cart.

**Test Data:**

* User: `standard_user`
* Example product: `Sauce Labs Backpack`

**Steps:**

1. Log in with valid credentials.
2. Open the selected product details page.
3. Add the selected product to the cart if it is not already added.
4. Verify that the Remove button is visible.
5. Click the Remove button.
6. Observe the button on the product details page.

**Expected Result:**

* Product is removed from the cart.
* Remove button becomes hidden for the selected product.
* Add to cart button becomes visible again for the selected product.
* Product details page remains open.

**Notes:**

* This scenario validates product-details-side UI feedback after removing a product from the cart.
* This scenario is the reverse-state counterpart to TC-PRODUCT-DETAILS-004.

---

### TC-PRODUCT-DETAILS-009 — Cart badge is displayed after adding product from product details page

**Type:** Regression / UI
**Priority:** Medium
**Automation Candidate:** Yes
**Automation Status:** Automated
**Automated In:** `tests/test_product_details_page.py`

**Preconditions:**

* User is logged in.
* User is on the product details page.
* Cart is empty at the start of the test.
* Selected product has not been added to cart.

**Test Data:**

* User: `standard_user`
* Example product: `Sauce Labs Backpack`

**Steps:**

1. Log in with valid credentials.
2. Open the selected product details page.
3. Click the Add to cart button.
4. Observe the cart badge in the product details page header.

**Expected Result:**

* Cart badge is visible.
* Cart badge displays `1`.
* Cart badge count matches the number of products currently in the cart.

**Notes:**

* This scenario validates cart badge visibility from a product-details-side add-to-cart action when the cart starts empty.

---

### TC-PRODUCT-DETAILS-010 — Cart badge count updates after adding product from details when cart is not empty

**Type:** Regression / UI
**Priority:** Medium
**Automation Candidate:** Yes
**Automation Status:** Automated
**Automated In:** `tests/test_product_details_page.py`

**Preconditions:**

* User is logged in.
* User is on the product details page.
* One product is already present in the cart.
* Selected product has not been added to cart.

**Test Data:**

* User: `standard_user`
* Existing cart product: `Sauce Labs Backpack`
* Product added from details page: `Sauce Labs Bolt T-Shirt`

**Steps:**

1. Log in with valid credentials.
2. Add the first selected product to the cart.
3. Open the second selected product details page.
4. Click the Add to cart button on the product details page.
5. Observe the cart badge in the product details page header.

**Expected Result:**

* Second product is added to the cart.
* Cart badge remains visible.
* Cart badge count updates from `1` to `2`.
* Badge count matches the number of products currently in the cart.

**Notes:**

* This scenario validates cart badge count update from a product-details-side add-to-cart action when the cart already contains another product.

---

### TC-PRODUCT-DETAILS-011 — Cart badge count updates after removing one of multiple products from details page

**Type:** Regression / UI
**Priority:** Medium
**Automation Candidate:** Yes
**Automation Status:** Automated
**Automated In:** `tests/test_product_details_page.py`

**Preconditions:**

* User is logged in.
* User is on the product details page.
* At least two products are present in the cart.
* Selected product displayed on the product details page is already in the cart.

**Test Data:**

* User: `standard_user`
* Example products:

  * `Sauce Labs Backpack`
  * `Sauce Labs Bolt T-Shirt`

**Steps:**

1. Log in with valid credentials.
2. Add two selected products to the cart.
3. Open the product details page for one of the added products.
4. Verify that the cart badge displays `2`.
5. Click the Remove button on the product details page.
6. Observe the cart badge.

**Expected Result:**

* Selected product is removed from the cart.
* One product remains in the cart.
* Cart badge count decreases from `2` to `1`.
* Badge count matches the number of products currently in the cart.

**Notes:**

* This scenario validates cart badge count update from a product-details-side remove action when another product remains in the cart.

---

### TC-PRODUCT-DETAILS-012 — Cart badge disappears after removing last product from product details page

**Type:** Regression / UI
**Priority:** Medium
**Automation Candidate:** Yes
**Automation Status:** Automated
**Automated In:** `tests/test_product_details_page.py`

**Preconditions:**

* User is logged in.
* User is on the product details page.
* Exactly one product has been added to cart.
* Selected product displayed on the product details page is the only product in the cart.

**Test Data:**

* User: `standard_user`
* Example product: `Sauce Labs Backpack`

**Steps:**

1. Log in with valid credentials.
2. Open the selected product details page.
3. Add the selected product to the cart.
4. Verify that the cart badge displays `1`.
5. Click the Remove button.
6. Observe the cart badge in the product details page header.

**Expected Result:**

* Product is removed from the cart.
* Cart badge is no longer displayed after removing the last product.
* Badge state matches the empty cart state.

**Notes:**

* This scenario validates complete cart badge disappearance after product-details-side removal of the last product.

---

### TC-PRODUCT-DETAILS-013 — Cart page can be opened from product details page

**Type:** Regression / Navigation / UI
**Priority:** Medium
**Automation Candidate:** Yes
**Automation Status:** Automated
**Automated In:** `tests/test_product_details_page.py`

**Preconditions:**

* User is logged in.
* User is on a product details page.

**Test Data:**

* User: `standard_user`
* Example product: `Sauce Labs Backpack`

**Steps:**

1. Log in with valid credentials.
2. Open the selected product details page.
3. Click the cart icon in the product details page header.
4. Observe the cart page.

**Expected Result:**

* Cart page is opened.
* Cart page URL contains `cart.html`.
* Cart page container is visible.
* No error is displayed.

**Notes:**

* This scenario validates cart navigation from the product details page header.
* This test should not validate checkout behavior.

---

### TC-PRODUCT-DETAILS-014 — All products can be removed from cart from product details page

**Type:** Regression / Positive / UI
**Priority:** Medium
**Automation Candidate:** Yes
**Automation Status:** Automated
**Automated In:** `tests/test_product_details_page.py`

**Preconditions:**

* User is logged in.
* User can open product details pages for products from the product test data set.
* All products from the product test data set have been added to the cart before each product removal check.

**Test Data:**

* User: `standard_user`
* Products: all products from the product test data set

**Steps:**

1. Log in with valid credentials.
2. Add all products from the product test data set to the cart.
3. For each product from the product test data set, open that product details page in an isolated test iteration.
4. Click the Remove button on the product details page.
5. Observe the product details page, cart badge, and cart page item list.

**Expected Result:**

* The tested product can be removed from the cart from its product details page.
* Remove action does not display an error.
* Product details page remains open after removing the tested product.
* Cart badge count decreases by one after removing the tested product.
* The tested product is no longer visible on the cart page.
* Other products that were previously added to the cart are not negatively affected by removing the tested product.
