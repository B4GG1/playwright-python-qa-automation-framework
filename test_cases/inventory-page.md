# Inventory Page — Test Cases

## Overview

This document contains manual test cases for the Sauce Demo inventory page.

The goal of this document is to define inventory-page-related scenarios and track their automation coverage.

This file focuses only on behavior owned by the inventory page:

* inventory page availability
* product list visibility
* product card content
* product sorting
* cart navigation from the inventory header
* adding products to cart from inventory product cards
* inventory-side Add to cart / Remove button state
* cart badge behavior visible from the inventory page

Product details page scenarios are covered in `product-details-page.md`.

Cart page scenarios are covered in `cart-page.md`.

Checkout scenarios are intentionally excluded and will be covered in a separate checkout test case file.

## Test Case Overview And Automation Coverage

| Test Case ID                                                                                                    | Scenario                                                                 | Type                       | Priority | Automation Status | Automated In                   |
|-----------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------|----------------------------|----------|-------------------|--------------------------------|
| [TC-INVENTORY-001](#tc-inventory-001--inventory-page-is-visible-after-successful-login)                         | Inventory page is visible after successful login                         | Smoke / Positive / UI      | High     | Automated         | `tests/test_inventory_page.py` |
| [TC-INVENTORY-002](#tc-inventory-002--product-list-is-displayed)                                                | Product list is displayed                                                | Smoke / UI                 | High     | Automated         | `tests/test_inventory_page.py` |
| [TC-INVENTORY-003](#tc-inventory-003--product-cards-contain-name-description-price-and-image)                   | Product cards contain name, description, price, and image                | Regression / UI            | Medium   | Automated         | `tests/test_inventory_page.py` |
| [TC-INVENTORY-004](#tc-inventory-004--cart-page-can-be-opened-from-inventory-page)                              | Cart page can be opened from inventory page                              | Smoke / Navigation / UI    | High     | Automated         | `tests/test_inventory_page.py` |
| [TC-INVENTORY-005](#tc-inventory-005--product-can-be-added-to-cart-from-inventory-page)                         | Product can be added to cart from inventory page                         | Regression / Positive / UI | High     | Automated         | `tests/test_inventory_page.py` |
| [TC-INVENTORY-006](#tc-inventory-006--add-to-cart-button-changes-to-remove-after-adding-product-from-inventory) | Add to cart button changes to Remove after adding product from inventory | Regression / UI            | Medium   | Automated         | `tests/test_inventory_page.py` |
| [TC-INVENTORY-007](#tc-inventory-007--cart-badge-is-displayed-after-adding-one-product)                         | Cart badge is displayed after adding one product                         | Regression / UI            | Medium   | Automated         | `tests/test_inventory_page.py` |
| [TC-INVENTORY-008](#tc-inventory-008--cart-badge-count-updates-after-adding-multiple-products)                  | Cart badge count updates after adding multiple products                  | Regression / UI            | Medium   | Automated         | `tests/test_inventory_page.py` |
| [TC-INVENTORY-009](#tc-inventory-009--products-can-be-sorted-by-name-a-to-z)                                    | Products can be sorted by name A to Z                                    | Regression / Sorting / UI  | Medium   | Automated         | `tests/test_inventory_page.py` |
| [TC-INVENTORY-010](#tc-inventory-010--products-can-be-sorted-by-name-z-to-a)                                    | Products can be sorted by name Z to A                                    | Regression / Sorting / UI  | Medium   | Automated         | `tests/test_inventory_page.py` |
| [TC-INVENTORY-011](#tc-inventory-011--products-can-be-sorted-by-price-low-to-high)                              | Products can be sorted by price low to high                              | Regression / Sorting / UI  | Medium   | Automated         | `tests/test_inventory_page.py` |
| [TC-INVENTORY-012](#tc-inventory-012--products-can-be-sorted-by-price-high-to-low)                              | Products can be sorted by price high to low                              | Regression / Sorting / UI  | Medium   | Automated         | `tests/test_inventory_page.py` |

---

## Test Cases

### TC-INVENTORY-001 — Inventory page is visible after successful login

**Type:** Smoke / Positive / UI\
**Priority:** High
**Automation Candidate:** Yes
**Automation Status:** Automated
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
* Products: all products from the inventory product test data set

**Steps:**

1. Log in with valid credentials.
2. Observe the product list.
3. Check product card content for each product from the inventory product test data set.

**Expected Result:**

* Each product card contains a visible product name.
* Each product card contains a visible product description.
* Each product card contains a visible product price.
* Each product card contains a visible product image.
* Each product card contains an Add to cart button.
* Product card content matches expected centralized test data.

**Notes:**

* This scenario validates that product cards contain the minimum user-facing information required to understand and select a product.
* Exact product data is stored in centralized inventory product test data.

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

**Type:** Regression / Positive / UI\
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

* This scenario validates the basic add-to-cart action initiated from the inventory page.
* During automation, deterministic product data should be used instead of random product selection.
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
* This test should not validate cart page product content.

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

* This scenario validates cart badge count updates from inventory-side actions.
* During automation, deterministic product data should be used instead of random product selection.

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
* Do not compare prices as raw strings.
* Avoid hardcoded sleeps.
