# Product Details Page — Test Cases

## Overview

This document contains manual test cases for the Sauce Demo product details page.

The goal of this document is to define product-details-page-related scenarios and track their automation coverage.

This file focuses only on behavior owned by the product details page:

* opening product details from inventory page entry points
* product details content validation
* returning from product details page to inventory page
* product-details-side Add to cart / Remove button behavior

Inventory page scenarios are covered in `inventory-page.md`.

Cart page scenarios are covered in `cart-page.md`.

Checkout scenarios are intentionally excluded and will be covered in a separate checkout test case file.

## Test Case Overview And Automation Coverage

| Test Case ID                                                                                                                   | Scenario                                                                    | Type                       | Priority | Automation Status | Automated In                         |
|--------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------|----------------------------|----------|-------------------|--------------------------------------|
| [TC-PRODUCT-DETAILS-001](#tc-product-details-001--product-details-can-be-opened-from-product-name)                             | Product details can be opened from product name                             | Regression / Positive / UI | Medium   | Automated         | `tests/test_product_details_page.py` |
| [TC-PRODUCT-DETAILS-002](#tc-product-details-002--product-details-can-be-opened-from-product-image)                            | Product details can be opened from product image                            | Regression / Positive / UI | Medium   | Automated         | `tests/test_product_details_page.py` |
| [TC-PRODUCT-DETAILS-003](#tc-product-details-003--user-can-return-from-product-details-to-inventory-page)                      | User can return from product details to inventory page                      | Regression / Positive / UI | Medium   | Automated         | `tests/test_product_details_page.py` |
| [TC-PRODUCT-DETAILS-004](#tc-product-details-004--add-to-cart-button-changes-to-remove-after-adding-product-from-details-page) | Add to cart button changes to Remove after adding product from details page | Regression / UI            | Medium   | Automated         | `tests/test_product_details_page.py` |

---

## Test Cases

### TC-PRODUCT-DETAILS-001 — Product details can be opened from product name

**Type:** Regression / Positive / UI
**Priority:** Medium
**Automation Candidate:** Yes
**Automation Status:** Automated
**Automated In:** `tests/test_product_details_page.py`

**Preconditions:**

* User is logged in.
* User is on the inventory page.
* Product list is visible.

**Test Data:**

* User: `standard_user`
* Products: all products from the inventory product test data set

**Steps:**

1. Log in with valid credentials.
2. For each product from the inventory product test data set, click the product name on the inventory page.
3. Observe the product details page.

**Expected Result:**

* Product details page is opened for the selected product.
* Product details page URL contains the selected product ID.
* Product details page displays the selected product name.
* Product details page displays the selected product description.
* Product details page displays the selected product price.
* Product details page displays the selected product image.
* Product details page displays the Add to cart button.

**Notes:**

* This scenario validates product details navigation from product name.
* During automation, this scenario is executed for all products from the centralized inventory product test data set.
* Product details validation should remain focused on the selected product details page.

---

### TC-PRODUCT-DETAILS-002 — Product details can be opened from product image

**Type:** Regression / Positive / UI
**Priority:** Medium
**Automation Candidate:** Yes
**Automation Status:** Automated
**Automated In:** `tests/test_product_details_page.py`

**Preconditions:**

* User is logged in.
* User is on the inventory page.
* Product list is visible.

**Test Data:**

* User: `standard_user`
* Products: all products from the inventory product test data set

**Steps:**

1. Log in with valid credentials.
2. For each product from the inventory product test data set, click the product image on the inventory page.
3. Observe the product details page.

**Expected Result:**

* Product details page is opened for the selected product.
* Product details page URL contains the selected product ID.
* Product details page displays the selected product name.
* Product details page displays the selected product description.
* Product details page displays the selected product price.
* Product details page displays the selected product image.
* Product details page displays the Add to cart button.

**Notes:**

* This scenario validates product details navigation from product image.
* During automation, this scenario is executed for all products from the centralized inventory product test data set.
* Product details validation should match the selected product, not only confirm that a generic details page was opened.

---

### TC-PRODUCT-DETAILS-003 — User can return from product details to inventory page

**Type:** Regression / Positive / UI
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
* One representative product is enough because product details entry paths are already covered separately.

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
* This test should not validate cart page product content.
