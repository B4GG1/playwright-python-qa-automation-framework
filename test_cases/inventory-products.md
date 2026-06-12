# Inventory And Products — Test Cases

## Overview

This document contains manual test cases for the Sauce Demo inventory and products area.

The goal of this document is to define inventory and product-related test scenarios before and alongside automation implementation.

This workstream focuses only on:

* inventory page availability
* product list visibility
* product card content
* product details navigation
* product sorting

Cart and checkout scenarios are intentionally excluded from this document and will be covered in separate test case files.

## Test Case Overview And Automation Coverage

| Test Case ID                                                                                  | Scenario                                                  | Type                       | Priority | Automation Status | Automated In                   |
| --------------------------------------------------------------------------------------------- | --------------------------------------------------------- | -------------------------- | -------- | ----------------- | ------------------------------ |
| [TC-INVENTORY-001](#tc-inventory-001--inventory-page-is-visible-after-successful-login)       | Inventory page is visible after successful login          | Smoke / Positive           | High     | Automated         | `tests/test_inventory_page.py` |
| [TC-INVENTORY-002](#tc-inventory-002--product-list-is-displayed)                              | Product list is displayed                                 | Smoke / UI                 | High     | Automated         | `tests/test_inventory_page.py` |
| [TC-INVENTORY-003](#tc-inventory-003--product-cards-contain-name-description-price-and-image) | Product cards contain name, description, price, and image | Regression / UI            | Medium   | Automated         | `tests/test_inventory_page.py` |
| [TC-INVENTORY-004](#tc-inventory-004--product-details-can-be-opened-from-product-name)        | Product details can be opened from product name           | Regression / Positive / UI | Medium   | Automated         | `tests/test_inventory_page.py` |
| [TC-INVENTORY-005](#tc-inventory-005--product-details-can-be-opened-from-product-image)       | Product details can be opened from product image          | Regression / Positive / UI | Medium   | Automated         | `tests/test_inventory_page.py` |
| [TC-INVENTORY-006](#tc-inventory-006--user-can-return-from-product-details-to-inventory-page) | User can return from product details to inventory page    | Regression / Positive / UI | Medium   | Automated         | `tests/test_inventory_page.py` |
| [TC-INVENTORY-007](#tc-inventory-007--products-can-be-sorted-by-name-a-to-z)                  | Products can be sorted by name A to Z                     | Regression / Sorting       | Medium   | Automated         | `tests/test_inventory_page.py` |
| [TC-INVENTORY-008](#tc-inventory-008--products-can-be-sorted-by-name-z-to-a)                  | Products can be sorted by name Z to A                     | Regression / Sorting       | Medium   | Automated         | `tests/test_inventory_page.py` |
| [TC-INVENTORY-009](#tc-inventory-009--products-can-be-sorted-by-price-low-to-high)            | Products can be sorted by price low to high               | Regression / Sorting       | Medium   | Automated         | `tests/test_inventory_page.py` |
| [TC-INVENTORY-010](#tc-inventory-010--products-can-be-sorted-by-price-high-to-low)            | Products can be sorted by price high to low               | Regression / Sorting       | Medium   | Automated         | `tests/test_inventory_page.py` |

---

## Test Cases

### TC-INVENTORY-001 — Inventory page is visible after successful login

**Type:** Smoke / Positive\
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

### TC-INVENTORY-004 — Product details can be opened from product name

**Type:** Regression / Positive / UI\
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
* Product details testing should remain limited to navigation and displayed product information in this workstream.

---

### TC-INVENTORY-005 — Product details can be opened from product image

**Type:** Regression / Positive / UI\
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

### TC-INVENTORY-006 — User can return from product details to inventory page

**Type:** Regression / Positive / UI\
**Priority:** Medium\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_inventory_page.py`

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

### TC-INVENTORY-007 — Products can be sorted by name A to Z

**Type:** Regression / Sorting\
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

### TC-INVENTORY-008 — Products can be sorted by name Z to A

**Type:** Regression / Sorting\
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

### TC-INVENTORY-009 — Products can be sorted by price low to high

**Type:** Regression / Sorting\
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

### TC-INVENTORY-010 — Products can be sorted by price high to low

**Type:** Regression / Sorting\
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
