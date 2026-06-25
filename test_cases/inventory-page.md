# Inventory Page — Test Cases

## Overview

This document contains manual test cases for the Sauce Demo inventory page.

The goal of this document is to define inventory-page-owned scenarios and track their automation coverage. Product details scenarios opened from inventory product cards are documented here because the user action starts on the inventory page.

## Test Case Overview And Automation Coverage

| Test Case ID                                                                                                                | Scenario                                                                        | Type                         | Priority | Automation Status  | Automated In                         |
|-----------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------|------------------------------|----------|--------------------|--------------------------------------|
| [TC-INVENTORY-001](#tc-inventory-001--inventory-page-is-visible-after-successful-login)                                     | Inventory page is visible after successful login                                | Smoke / Positive / UI        | High     | Automated          | `tests/test_inventory_page.py`       |
| [TC-INVENTORY-002](#tc-inventory-002--product-list-is-displayed)                                                            | Product list is displayed                                                       | Smoke / UI                   | High     | Automated          | `tests/test_inventory_page.py`       |
| [TC-INVENTORY-003](#tc-inventory-003--product-cards-contain-name-description-price-and-image)                               | Product cards contain name, description, price, and image                       | Regression / UI              | Medium   | Automated          | `tests/test_inventory_page.py`       |
| [TC-INVENTORY-004](#tc-inventory-004--cart-page-can-be-opened-from-inventory-page)                                          | Cart page can be opened from inventory page                                     | Smoke / Navigation / UI      | High     | Automated          | `tests/test_inventory_page.py`       |
| [TC-INVENTORY-005](#tc-inventory-005--product-can-be-added-to-cart-from-inventory-page)                                     | Product can be added to cart from inventory page                                | Smoke / Positive / UI        | High     | Automated          | `tests/test_inventory_page.py`       |
| [TC-INVENTORY-006](#tc-inventory-006--add-to-cart-button-changes-to-remove-after-adding-product-from-inventory)             | Add to cart button changes to Remove after adding product from inventory        | Regression / UI              | Medium   | Automated          | `tests/test_inventory_page.py`       |
| [TC-INVENTORY-007](#tc-inventory-007--cart-badge-is-displayed-after-adding-one-product)                                     | Cart badge is displayed after adding one product                                | Regression / UI              | Medium   | Automated          | `tests/test_inventory_page.py`       |
| [TC-INVENTORY-008](#tc-inventory-008--cart-badge-count-updates-after-adding-multiple-products)                              | Cart badge count updates after adding multiple products                         | Regression / UI              | Medium   | Automated          | `tests/test_inventory_page.py`       |
| [TC-INVENTORY-009](#tc-inventory-009--products-can-be-sorted-by-name-a-to-z)                                                | Products can be sorted by name A to Z                                           | Regression / Sorting / UI    | Medium   | Automated          | `tests/test_inventory_page.py`       |
| [TC-INVENTORY-010](#tc-inventory-010--products-can-be-sorted-by-name-z-to-a)                                                | Products can be sorted by name Z to A                                           | Regression / Sorting / UI    | Medium   | Automated          | `tests/test_inventory_page.py`       |
| [TC-INVENTORY-011](#tc-inventory-011--products-can-be-sorted-by-price-low-to-high)                                          | Products can be sorted by price low to high                                     | Regression / Sorting / UI    | Medium   | Automated          | `tests/test_inventory_page.py`       |
| [TC-INVENTORY-012](#tc-inventory-012--products-can-be-sorted-by-price-high-to-low)                                          | Products can be sorted by price high to low                                     | Regression / Sorting / UI    | Medium   | Automated          | `tests/test_inventory_page.py`       |
| [TC-INVENTORY-013](#tc-inventory-013--product-details-can-be-opened-from-product-name-on-inventory-page)                    | Product details can be opened from product name on inventory page               | Regression / Navigation / UI | Medium   | Refactor Candidate | `tests/test_product_details_page.py` |
| [TC-INVENTORY-014](#tc-inventory-014--product-details-can-be-opened-from-product-image-on-inventory-page)                   | Product details can be opened from product image on inventory page              | Regression / Navigation / UI | Medium   | Refactor Candidate | `tests/test_product_details_page.py` |
| [TC-INVENTORY-015](#tc-inventory-015--all-products-can-be-added-to-cart-from-inventory-page)                                | All products can be added to cart from inventory page                           | Regression / Positive / UI   | Medium   | Planned            | TBD                                  |
| [TC-INVENTORY-016](#tc-inventory-016--product-can-be-removed-from-cart-from-inventory-page)                                 | Product can be removed from cart from inventory page                            | Smoke / Positive / UI        | High     | Planned            | TBD                                  |
| [TC-INVENTORY-017](#tc-inventory-017--remove-button-changes-back-to-add-to-cart-after-removing-product-from-inventory)      | Remove button changes back to Add to cart after removing product from inventory | Regression / UI              | Medium   | Planned            | TBD                                  |
| [TC-INVENTORY-018](#tc-inventory-018--cart-badge-count-updates-after-removing-one-of-multiple-products-from-inventory-page) | Cart badge count updates after removing one of multiple products                | Regression / UI              | Medium   | Planned            | TBD                                  |
| [TC-INVENTORY-019](#tc-inventory-019--cart-badge-disappears-after-removing-last-product-from-inventory-page)                | Cart badge disappears after removing last product from inventory page           | Regression / UI              | Medium   | Planned            | TBD                                  |
| [TC-INVENTORY-020](#tc-inventory-020--all-products-can-be-removed-from-cart-from-inventory-page)                            | All products can be removed from cart from inventory page                       | Regression / Positive / UI   | Medium   | Planned            | TBD                                  |

---

## Test Cases

### TC-INVENTORY-001 — Inventory page is visible after successful login

**Type:** Smoke / Positive / UI\
**Priority:** High\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_inventory_page.py`

**Preconditions:**

* User is on the login page.
* User has valid credentials.

**Test Data:**

* Username: `standard_user`
* Password: `secret_sauce`

**Steps:**

1. Enter valid username.
2. Enter valid password.
3. Click the Login button.
4. Observe the inventory page.

**Expected Result:**

* User is redirected to the inventory page.
* Inventory page URL contains `inventory.html`.
* Inventory container is visible.
* Product list is visible.

**Notes:**

* This is the main smoke validation for inventory page availability after successful login.
* This scenario verifies that login leads to the expected authenticated area.

---

### TC-INVENTORY-002 — Product list is displayed

**Type:** Smoke / UI\
**Priority:** High\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_inventory_page.py`

**Preconditions:**

* User is logged in.
* User is on the inventory page.

**Test Data:**

* User: `standard_user`

**Steps:**

1. Log in with valid credentials.
2. Observe the inventory page.
3. Check the displayed product list.

**Expected Result:**

* Product list is visible.
* Product list contains product items.
* Expected number of products is displayed.

**Notes:**

* Sauce Demo usually displays 6 products on the inventory page.
* This scenario validates that the inventory page is not empty and product data is rendered.

---

### TC-INVENTORY-003 — Product cards contain name, description, price, and image

**Type:** Regression / UI\
**Priority:** Medium\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_inventory_page.py`

**Preconditions:**

* User is logged in.
* User is on the inventory page.
* Product list is visible.

**Test Data:**

* User: `standard_user`
* Products: all products from the product test data set

**Steps:**

1. Log in with valid credentials.
2. Observe the product list.
3. Check product card content for each product from the product test data set.

**Expected Result:**

* Each product card contains a visible product name.
* Each product card contains a visible product description.
* Each product card contains a visible product price.
* Each product card contains a visible product image.
* Each product card contains an Add to cart button.
* Product card content matches expected centralized test data.

**Notes:**

* This scenario validates that product cards contain the minimum user-facing information required to understand and select a product.
* Exact product data is stored in centralized product test data.

---

### TC-INVENTORY-004 — Cart page can be opened from inventory page

**Type:** Smoke / Navigation / UI\
**Priority:** High\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_inventory_page.py`

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

* This scenario validates inventory-page header navigation to the cart page.
* This scenario should not validate product content or checkout behavior.

---

### TC-INVENTORY-005 — Product can be added to cart from inventory page

**Type:** Smoke / Positive / UI\
**Priority:** High\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_inventory_page.py`

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

* This scenario validates the primary inventory-page add-to-cart flow for one representative product.
* Full all-products add-to-cart regression coverage is tracked separately in TC-INVENTORY-015.
* Detailed cart item content validation belongs to `cart-page.md`.

---

### TC-INVENTORY-006 — Add to cart button changes to Remove after adding product from inventory

**Type:** Regression / UI\
**Priority:** Medium\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_inventory_page.py`

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
* Reverse button state after inventory-side removal is tracked separately in TC-INVENTORY-017.

---

### TC-INVENTORY-007 — Cart badge is displayed after adding one product

**Type:** Regression / UI\
**Priority:** Medium\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_inventory_page.py`

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
3. Observe the cart badge in the inventory page header.

**Expected Result:**

* Cart badge is visible.
* Cart badge displays `1`.
* Cart badge is displayed near the cart icon.

**Notes:**

* This scenario validates inventory-page header badge visibility after adding one product.
* During automation, badge text should be read from the UI and compared with the expected count.

---

### TC-INVENTORY-008 — Cart badge count updates after adding multiple products

**Type:** Regression / UI\
**Priority:** Medium\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_inventory_page.py`

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
4. Observe the cart badge in the inventory page header.

**Expected Result:**

* Cart badge is visible.
* Cart badge displays `2`.
* Cart badge count matches the number of added products.

**Notes:**

* This scenario validates cart badge count updates from inventory-side add-to-cart actions.
* Badge count update and disappearance after inventory-side remove actions are tracked separately in TC-INVENTORY-018 and TC-INVENTORY-019.

---

### TC-INVENTORY-009 — Products can be sorted by name A to Z

**Type:** Regression / Sorting / UI\
**Priority:** Medium\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_inventory_page.py`

**Preconditions:**

* User is logged in.
* User is on the inventory page.
* Product list is visible.

**Test Data:**

* Sort option: `Name (A to Z)`

**Steps:**

1. Log in with valid credentials.
2. Open the product sorting dropdown.
3. Select `Name (A to Z)`.
4. Observe the product order.

**Expected Result:**

* Products are sorted alphabetically by name in ascending order.
* Product order matches A to Z sorting.

**Notes:**

* During automation, product names are read from the UI and compared with an ascending sorted list.
* Product card content validation is covered by TC-INVENTORY-003.
* Avoid hardcoded sleeps.

---

### TC-INVENTORY-010 — Products can be sorted by name Z to A

**Type:** Regression / Sorting / UI\
**Priority:** Medium\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_inventory_page.py`

**Preconditions:**

* User is logged in.
* User is on the inventory page.
* Product list is visible.

**Test Data:**

* Sort option: `Name (Z to A)`

**Steps:**

1. Log in with valid credentials.
2. Open the product sorting dropdown.
3. Select `Name (Z to A)`.
4. Observe the product order.

**Expected Result:**

* Products are sorted alphabetically by name in descending order.
* Product order matches Z to A sorting.

**Notes:**

* During automation, product names are read from the UI and compared with a descending sorted list.
* Product card content validation is covered by TC-INVENTORY-003.
* Avoid hardcoded sleeps.

---

### TC-INVENTORY-011 — Products can be sorted by price low to high

**Type:** Regression / Sorting / UI\
**Priority:** Medium\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_inventory_page.py`

**Preconditions:**

* User is logged in.
* User is on the inventory page.
* Product list is visible.

**Test Data:**

* Sort option: `Price (low to high)`

**Steps:**

1. Log in with valid credentials.
2. Open the product sorting dropdown.
3. Select `Price (low to high)`.
4. Observe the product order.

**Expected Result:**

* Products are sorted by price in ascending order.
* Product order matches low to high price sorting.

**Notes:**

* During automation, product prices are read from the UI.
* Price values are converted from strings to numeric values before comparison.
* Product card content validation is covered by TC-INVENTORY-003.
* Do not compare prices as raw strings.
* Avoid hardcoded sleeps.

---

### TC-INVENTORY-012 — Products can be sorted by price high to low

**Type:** Regression / Sorting / UI\
**Priority:** Medium\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_inventory_page.py`

**Preconditions:**

* User is logged in.
* User is on the inventory page.
* Product list is visible.

**Test Data:**

* Sort option: `Price (high to low)`

**Steps:**

1. Log in with valid credentials.
2. Open the product sorting dropdown.
3. Select `Price (high to low)`.
4. Observe the product order.

**Expected Result:**

* Products are sorted by price in descending order.
* Product order matches high to low price sorting.

**Notes:**

* During automation, product prices are read from the UI.
* Price values are converted from strings to numeric values before comparison.
* Product card content validation is covered by TC-INVENTORY-003.
* Do not compare prices as raw strings.
* Avoid hardcoded sleeps.

---

### TC-INVENTORY-013 — Product details can be opened from product name on inventory page

**Type:** Regression / Navigation / UI\
**Priority:** Medium\
**Automation Candidate:** Yes\
**Automation Status:** Refactor Candidate\
**Automated In:** `tests/test_product_details_page.py`

**Preconditions:**

* User is logged in.
* User is on the inventory page.
* Product list is visible.

**Test Data:**

* User: `standard_user`
* Products: all products from the product test data set

**Steps:**

1. Log in with valid credentials.
2. For each product from the product test data set, click the product name on the inventory page.
3. Observe the product details page.

**Expected Result:**

* Product details page is opened for the selected product.
* Product details page URL contains the selected product ID.
* Product details page item details container is visible.
* Product details page belongs to the selected product.

**Notes:**

* This scenario is documented under Inventory Page because the user action starts from the inventory product name.
* Temporary AQA-0068 note: current automation exists in `tests/test_product_details_page.py`; review ownership during AQA-0072 and remove this note after AQA-0072.

---

### TC-INVENTORY-014 — Product details can be opened from product image on inventory page

**Type:** Regression / Navigation / UI\
**Priority:** Medium\
**Automation Candidate:** Yes\
**Automation Status:** Refactor Candidate\
**Automated In:** `tests/test_product_details_page.py`

**Preconditions:**

* User is logged in.
* User is on the inventory page.
* Product list is visible.

**Test Data:**

* User: `standard_user`
* Products: all products from the product test data set

**Steps:**

1. Log in with valid credentials.
2. For each product from the product test data set, click the product image on the inventory page.
3. Observe the product details page.

**Expected Result:**

* Product details page is opened for the selected product.
* Product details page URL contains the selected product ID.
* Product details page item details container is visible.
* Product details page belongs to the selected product.

**Notes:**

* This scenario is documented under Inventory Page because the user action starts from the inventory product image.
* Temporary AQA-0068 note: current automation exists in `tests/test_product_details_page.py`; review ownership during AQA-0072 and remove this note after AQA-0072.

---

### TC-INVENTORY-015 — All products can be added to cart from inventory page

**Type:** Regression / Positive / UI\
**Priority:** Medium\
**Automation Candidate:** Yes\
**Automation Status:** Planned\
**Automated In:** TBD

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
2. For each product from the product test data set, click the Add to cart button on the inventory product card.
3. Observe the inventory page header.
4. Open the cart page.
5. Observe the cart item list.

**Expected Result:**

* Each product can be added to the cart from the inventory page.
* Cart badge count matches the total number of added products.
* Cart page displays all added products.
* No error is displayed.

**Notes:**

* This is the full regression variant of TC-INVENTORY-005.
* Temporary AQA-0068 note: automate in AQA-0072 and remove this note after AQA-0072.
* This scenario should use parametrized or loop-based product data.
* Detailed cart content validation remains owned by `cart-page.md`.

---

### TC-INVENTORY-016 — Product can be removed from cart from inventory page

**Type:** Smoke / Positive / UI\
**Priority:** High\
**Automation Candidate:** Yes\
**Automation Status:** Planned\
**Automated In:** TBD

**Preconditions:**

* User is logged in.
* User is on the inventory page.
* Product list is visible.
* Selected product has been added to the cart from the inventory page.

**Test Data:**

* User: `standard_user`
* Example product: `Sauce Labs Backpack`

**Steps:**

1. Log in with valid credentials.
2. Add the selected product to the cart from the inventory page.
3. Click the Remove button for the same product on the inventory page.
4. Open the cart page.
5. Observe the cart item list.

**Expected Result:**

* Selected product is removed from the cart.
* Removed product is no longer displayed on the cart page.
* Cart page remains available.
* No error is displayed.

**Notes:**

* This scenario validates inventory-side remove-from-cart behavior for one representative product.
* Temporary AQA-0068 note: automate in AQA-0072 and remove this note after AQA-0072.
* Full all-products remove-from-cart regression coverage is tracked separately in TC-INVENTORY-020.
* This scenario should not validate checkout behavior.

---

### TC-INVENTORY-017 — Remove button changes back to Add to cart after removing product from inventory

**Type:** Regression / UI\
**Priority:** Medium\
**Automation Candidate:** Yes\
**Automation Status:** Planned\
**Automated In:** TBD

**Preconditions:**

* User is logged in.
* User is on the inventory page.
* Product list is visible.
* Selected product has been added to the cart from the inventory page.

**Test Data:**

* User: `standard_user`
* Example product: `Sauce Labs Backpack`

**Steps:**

1. Log in with valid credentials.
2. Add the selected product to the cart from the inventory page.
3. Verify that the selected product displays the Remove button.
4. Click the Remove button for the selected product.
5. Observe the button for the same product.

**Expected Result:**

* Product is removed from the cart.
* Remove button becomes hidden for the selected product.
* Add to cart button becomes visible again for the selected product.
* Other product cards remain unchanged.

**Notes:**

* This scenario validates inventory-side button state after removing a product from the cart.
* Temporary AQA-0068 note: automate in AQA-0072 and remove this note after AQA-0072.
* This scenario is the reverse-state counterpart to TC-INVENTORY-006.

---

### TC-INVENTORY-018 — Cart badge count updates after removing one of multiple products from inventory page

**Type:** Regression / UI\
**Priority:** Medium\
**Automation Candidate:** Yes\
**Automation Status:** Planned\
**Automated In:** TBD

**Preconditions:**

* User is logged in.
* User is on the inventory page.
* Product list is visible.
* At least two products have been added to the cart from the inventory page.

**Test Data:**

* User: `standard_user`
* Example products:

  * `Sauce Labs Backpack`
  * `Sauce Labs Bolt T-Shirt`

**Steps:**

1. Log in with valid credentials.
2. Add the first selected product to the cart.
3. Add the second selected product to the cart.
4. Verify that the cart badge displays `2`.
5. Remove one selected product from the inventory page.
6. Observe the cart badge in the inventory page header.

**Expected Result:**

* Removed product is no longer in the cart.
* One product remains in the cart.
* Cart badge count decreases from `2` to `1`.
* Badge count matches the number of products currently in the cart.

**Notes:**

* This scenario validates inventory-side cart badge count update after removing one product while another product remains in the cart.
* Temporary AQA-0068 note: automate in AQA-0072 and remove this note after AQA-0072.

---

### TC-INVENTORY-019 — Cart badge disappears after removing last product from inventory page

**Type:** Regression / UI\
**Priority:** Medium\
**Automation Candidate:** Yes\
**Automation Status:** Planned\
**Automated In:** TBD

**Preconditions:**

* User is logged in.
* User is on the inventory page.
* Product list is visible.
* Exactly one product has been added to the cart from the inventory page.

**Test Data:**

* User: `standard_user`
* Example product: `Sauce Labs Backpack`

**Steps:**

1. Log in with valid credentials.
2. Add one selected product to the cart.
3. Verify that the cart badge displays `1`.
4. Remove the selected product from the inventory page.
5. Observe the cart badge in the inventory page header.

**Expected Result:**

* Product is removed from the cart.
* Cart badge is no longer displayed after removing the last product.
* Badge state matches the empty cart state.

**Notes:**

* This scenario validates complete cart badge disappearance after inventory-side removal of the last product.
* Temporary AQA-0068 note: automate in AQA-0072 and remove this note after AQA-0072.

---

### TC-INVENTORY-020 — All products can be removed from cart from inventory page

**Type:** Regression / Positive / UI\
**Priority:** Medium\
**Automation Candidate:** Yes\
**Automation Status:** Planned\
**Automated In:** TBD

**Preconditions:**

* User is logged in.
* User is on the inventory page.
* Product list is visible.
* All products from the product test data set have been added to the cart from the inventory page.

**Test Data:**

* User: `standard_user`
* Products: all products from the product test data set

**Steps:**

1. Log in with valid credentials.
2. Add all products from the product test data set to the cart from the inventory page.
3. For each added product, click the Remove button on the inventory product card.
4. Observe the inventory page header.
5. Open the cart page.
6. Observe the cart item list.

**Expected Result:**

* Each product can be removed from the cart from the inventory page.
* Cart badge count decreases after each removal.
* Cart badge is no longer displayed after the last product is removed.
* Cart page does not display any removed products.
* No error is displayed.

**Notes:**

* This is the full regression variant of TC-INVENTORY-016.
* Temporary AQA-0068 note: automate in AQA-0072 and remove this note after AQA-0072.