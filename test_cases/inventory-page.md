# Inventory Page — Test Cases

## Overview

This document contains manual test cases for the Sauce Demo inventory page.

The goal of this document is to define inventory-page-owned scenarios and track their automation coverage. Product details scenarios opened from inventory product cards are documented here because the user action starts on the inventory page.

## Test Case Overview And Automation Coverage

| Test Case ID                                                                                                                | Scenario                                                                             | Type                     | Priority | Automation Status | Automated In                   |
|-----------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------|--------------------------|----------|-------------------|--------------------------------|
| [TC-INVENTORY-001](#tc-inventory-001--inventory-page-is-visible-after-successful-login)                                     | Inventory page is visible after successful login                                     | Smoke / UI               | High     | Automated         | `tests/test_inventory_page.py` |
| [TC-INVENTORY-002](#tc-inventory-002--product-list-is-displayed)                                                            | Product list is displayed                                                            | Regression / UI          | High     | Automated         | `tests/test_inventory_page.py` |
| [TC-INVENTORY-003](#tc-inventory-003--product-cards-contain-name-description-price-and-image)                               | Product cards contain name, description, price, and image                            | Regression / UI          | Medium   | Automated         | `tests/test_inventory_page.py` |
| [TC-INVENTORY-004](#tc-inventory-004--cart-page-can-be-opened-from-inventory-page)                                          | Cart page can be opened from inventory page                                          | Smoke / Navigation       | High     | Automated         | `tests/test_inventory_page.py` |
| [TC-INVENTORY-005](#tc-inventory-005--product-can-be-added-to-cart-from-inventory-page)                                     | Product can be added to cart from inventory page                                     | Smoke / Navigation / E2E | High     | Automated         | `tests/test_inventory_page.py` |
| [TC-INVENTORY-006](#tc-inventory-006--add-to-cart-button-changes-to-remove-after-adding-product-from-inventory)             | Add to cart button changes to Remove after adding product from inventory             | Regression / UI          | Medium   | Automated         | `tests/test_inventory_page.py` |
| [TC-INVENTORY-007](#tc-inventory-007--cart-badge-is-displayed-after-adding-one-product)                                     | Cart badge is displayed after adding one product                                     | Smoke / UI               | Medium   | Automated         | `tests/test_inventory_page.py` |
| [TC-INVENTORY-008](#tc-inventory-008--cart-badge-count-updates-after-adding-multiple-products)                              | Cart badge count updates after adding multiple products                              | Regression / UI          | Medium   | Automated         | `tests/test_inventory_page.py` |
| [TC-INVENTORY-009](#tc-inventory-009--products-can-be-sorted-by-name-a-to-z)                                                | Products can be sorted by name A to Z                                                | Sorting                  | Medium   | Automated         | `tests/test_inventory_page.py` |
| [TC-INVENTORY-010](#tc-inventory-010--products-can-be-sorted-by-name-z-to-a)                                                | Products can be sorted by name Z to A                                                | Sorting                  | Medium   | Automated         | `tests/test_inventory_page.py` |
| [TC-INVENTORY-011](#tc-inventory-011--products-can-be-sorted-by-price-low-to-high)                                          | Products can be sorted by price low to high                                          | Sorting                  | Medium   | Automated         | `tests/test_inventory_page.py` |
| [TC-INVENTORY-012](#tc-inventory-012--products-can-be-sorted-by-price-high-to-low)                                          | Products can be sorted by price high to low                                          | Sorting                  | Medium   | Automated         | `tests/test_inventory_page.py` |
| [TC-INVENTORY-013](#tc-inventory-013--product-details-can-be-opened-for-all-products-by-product-name-on-inventory-page)     | Product details can be opened for all products by product name on inventory page     | Regression / Navigation  | Medium   | Automated         | `tests/test_inventory_page.py` |
| [TC-INVENTORY-014](#tc-inventory-014--product-details-can-be-opened-for-all-products-by-product-image-on-inventory-page)    | Product details can be opened for all products by product image on inventory page    | Regression / Navigation  | Medium   | Automated         | `tests/test_inventory_page.py` |
| [TC-INVENTORY-015](#tc-inventory-015--all-products-can-be-added-to-cart-from-inventory-page)                                | All products can be added to cart from inventory page                                | Regression / Navigation  | Medium   | Automated         | `tests/test_inventory_page.py` |
| [TC-INVENTORY-016](#tc-inventory-016--product-can-be-removed-from-cart-from-inventory-page)                                 | Product can be removed from cart from inventory page                                 | Smoke / Navigation       | High     | Automated         | `tests/test_inventory_page.py` |
| [TC-INVENTORY-017](#tc-inventory-017--remove-button-changes-back-to-add-to-cart-after-removing-product-from-inventory)      | Remove button changes back to Add to cart after removing product from inventory      | Regression / UI          | Medium   | Automated         | `tests/test_inventory_page.py` |
| [TC-INVENTORY-018](#tc-inventory-018--cart-badge-count-updates-after-removing-one-of-multiple-products-from-inventory-page) | Cart badge count updates after removing one of multiple products from inventory page | Regression / UI          | Medium   | Automated         | `tests/test_inventory_page.py` |
| [TC-INVENTORY-019](#tc-inventory-019--cart-badge-disappears-after-removing-last-product-from-inventory-page)                | Cart badge disappears after removing last product from inventory page                | Smoke / UI               | Medium   | Automated         | `tests/test_inventory_page.py` |
| [TC-INVENTORY-020](#tc-inventory-020--all-products-can-be-removed-from-cart-from-inventory-page)                            | All products can be removed from cart from inventory page                            | Regression / Navigation  | Medium   | Automated         | `tests/test_inventory_page.py` |
| [TC-INVENTORY-021](#tc-inventory-021--product-details-can-be-opened-from-product-name-for-example-product)                  | Product details can be opened from product name for example product                  | Smoke / Navigation       | High     | Automated         | `tests/test_inventory_page.py` |
| [TC-INVENTORY-022](#tc-inventory-022--product-details-can-be-opened-from-product-image-for-example-product)                 | Product details can be opened from product image for example product                 | Smoke / Navigation       | High     | Automated         | `tests/test_inventory_page.py` |

---

## Test Cases

### TC-INVENTORY-001 — Inventory page is visible after successful login

**Type:** Smoke / UI\
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

* This is the representative smoke validation for general inventory page availability.
* Detailed validation of the product list and individual product cards is covered by regression scenarios.

---

### TC-INVENTORY-002 — Product list is displayed

**Type:** Regression / UI\
**Priority:** High\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_inventory_page.py`

**Preconditions:**

* User is logged in.
* User is on the inventory page.

**Test Data:**

* User: `standard_user`
* Products: all products from the centralized product test data set

**Steps:**

1. Log in with valid credentials.
2. Observe the inventory page.
3. Check the displayed product list.

**Expected Result:**

* Product list is visible.
* Expected number of products is displayed.
* Displayed product names match the centralized product test data.

**Notes:**

* This scenario extends the general inventory smoke validation with detailed product-list verification.
* Individual product card content is validated separately in TC-INVENTORY-003.

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

* This scenario performs detailed UI validation of all product cards.
* Exact product data is stored in centralized product test data.

---

### TC-INVENTORY-004 — Cart page can be opened from inventory page

**Type:** Smoke / Navigation\
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

**Notes:**

* This scenario validates the primary Inventory → Cart page transition.
* UI is used to perform the transition but is not the primary subject of the scenario.

---

### TC-INVENTORY-005 — Product can be added to cart from inventory page

**Type:** Smoke / Navigation / E2E\
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

* This is the representative smoke validation of inventory-side add-to-cart behavior.
* Full all-products regression coverage is tracked in TC-INVENTORY-015.
* Navigation is included because the automated scenario opens the cart page to verify the result.

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
3. Verify the initial Add to cart button state.
4. Click the Add to cart button for the selected product.
5. Observe the button for the same product and an unaffected product.

**Expected Result:**

* Add to cart button becomes hidden for the selected product.
* Remove button becomes visible for the selected product.
* Other product controls remain unchanged.

**Notes:**

* This scenario validates detailed inventory-side UI state after adding a product.
* Reverse button state after removal is covered by TC-INVENTORY-017.

---

### TC-INVENTORY-007 — Cart badge is displayed after adding one product

**Type:** Smoke / UI\
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

**Notes:**

* This is the representative smoke validation of cart badge visibility and state.
* Multi-product badge behavior is covered by TC-INVENTORY-008.

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

* This is the broader regression variant of the cart badge add-to-cart state covered by TC-INVENTORY-007.

---

### TC-INVENTORY-009 — Products can be sorted by name A to Z

**Type:** Sorting\
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

* Product names are read from the UI and compared with an independently sorted ascending list.
* This scenario belongs to the dedicated Sorting execution category.

---

### TC-INVENTORY-010 — Products can be sorted by name Z to A

**Type:** Sorting\
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

* Product names are read from the UI and compared with an independently sorted descending list.
* This scenario belongs to the dedicated Sorting execution category.

---

### TC-INVENTORY-011 — Products can be sorted by price low to high

**Type:** Sorting\
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

* Product prices are read from the UI and converted to numeric values before comparison.
* This scenario belongs to the dedicated Sorting execution category.

---

### TC-INVENTORY-012 — Products can be sorted by price high to low

**Type:** Sorting\
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

* Product prices are read from the UI and converted to numeric values before comparison.
* This scenario belongs to the dedicated Sorting execution category.

---

### TC-INVENTORY-013 — Product details can be opened for all products by product name on inventory page

**Type:** Regression / Navigation\
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
2. For each product from the product test data set, click the product name on the inventory page.
3. Observe the product details page.

**Expected Result:**

* Product details page is opened for each selected product.
* Product details page URL contains the selected product ID.
* Product details page belongs to the selected product.
* Product details content matches centralized product test data.

**Notes:**

* This is the full regression variant of TC-INVENTORY-021.
* Navigation is the relevant execution category because each scenario performs Inventory → Product Details transition.

---

### TC-INVENTORY-014 — Product details can be opened for all products by product image on inventory page

**Type:** Regression / Navigation\
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
2. For each product from the product test data set, click the product image on the inventory page.
3. Observe the product details page.

**Expected Result:**

* Product details page is opened for each selected product.
* Product details page URL contains the selected product ID.
* Product details page belongs to the selected product.
* Product details content matches centralized product test data.

**Notes:**

* This is the full regression variant of TC-INVENTORY-022.
* Navigation is the relevant execution category because each scenario performs Inventory → Product Details transition.

---

### TC-INVENTORY-015 — All products can be added to cart from inventory page

**Type:** Regression / Navigation\
**Priority:** Medium\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_inventory_page.py`

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
2. Add the tested product to the cart from the inventory page.
3. Open the cart page.
4. Observe the cart item list.
5. Repeat the scenario independently for every product from the test data set.

**Expected Result:**

* Every tested product can be added to the cart from the inventory page.
* Cart page displays the tested product.

**Notes:**

* This is the full regression variant of TC-INVENTORY-005.
* Navigation is included because the cart page is opened to verify the result.

---

### TC-INVENTORY-016 — Product can be removed from cart from inventory page

**Type:** Smoke / Navigation\
**Priority:** High\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_inventory_page.py`

**Preconditions:**

* User is logged in.
* User is on the inventory page.
* Selected product has been added to the cart.

**Test Data:**

* User: `standard_user`
* Example product: representative product from centralized product test data

**Steps:**

1. Open the cart page.
2. Verify that the selected product is present.
3. Use Continue Shopping to return to the inventory page.
4. Remove the selected product from the inventory page.
5. Open the cart page again.
6. Observe the cart item list.

**Expected Result:**

* Product is initially present in the cart.
* User can return to the inventory page.
* Selected product can be removed from the inventory page.
* Removed product is no longer displayed on the cart page.

**Notes:**

* This is the representative smoke validation of inventory-side remove-from-cart behavior.
* Full all-products regression coverage is tracked in TC-INVENTORY-020.
* Navigation is included because the scenario performs Cart → Inventory and Inventory → Cart transitions.

---

### TC-INVENTORY-017 — Remove button changes back to Add to cart after removing product from inventory

**Type:** Regression / UI\
**Priority:** Medium\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_inventory_page.py`

**Preconditions:**

* User is logged in.
* User is on the inventory page.
* Selected product has been added to the cart.

**Test Data:**

* User: `standard_user`
* Example product: representative product from centralized product test data

**Steps:**

1. Verify that the selected product displays the Remove button.
2. Verify that Add to cart is not displayed for that product.
3. Remove the product.
4. Observe the controls for the same product.

**Expected Result:**

* Remove button becomes hidden.
* Add to cart button becomes visible again.

**Notes:**

* This scenario validates detailed inventory-side button state after removing a product.
* It is the reverse-state counterpart of TC-INVENTORY-006.

---

### TC-INVENTORY-018 — Cart badge count updates after removing one of multiple products from inventory page

**Type:** Regression / UI\
**Priority:** Medium\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_inventory_page.py`

**Preconditions:**

* User is logged in.
* User is on the inventory page.
* At least two products are available for cart operations.

**Test Data:**

* User: `standard_user`
* Example products:
  * `Sauce Labs Backpack`
  * `Sauce Labs Bolt T-Shirt`

**Steps:**

1. Add two selected products to the cart.
2. Verify that the cart badge displays `2`.
3. Remove one selected product.
4. Observe the cart badge.

**Expected Result:**

* Cart badge count decreases from `2` to `1`.
* Badge count matches the number of products remaining in the cart.

**Notes:**

* This scenario performs detailed cart badge state validation when one of multiple products is removed.

---

### TC-INVENTORY-019 — Cart badge disappears after removing last product from inventory page

**Type:** Smoke / UI\
**Priority:** Medium\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_inventory_page.py`

**Preconditions:**

* User is logged in.
* User is on the inventory page.
* Exactly one product is present in the cart.

**Test Data:**

* User: `standard_user`
* Example product: representative product from centralized product test data

**Steps:**

1. Verify that the cart badge is visible and displays `1`.
2. Remove the last product from the inventory page.
3. Observe the cart badge.

**Expected Result:**

* Cart badge disappears after the final product is removed.

**Notes:**

* This is the representative smoke validation for the empty-cart badge state.
* The more detailed multi-product decrement scenario is covered by TC-INVENTORY-018.

---

### TC-INVENTORY-020 — All products can be removed from cart from inventory page

**Type:** Regression / Navigation\
**Priority:** Medium\
**Automation Candidate:** Yes\
**Automation Status:** Automated\
**Automated In:** `tests/test_inventory_page.py`

**Preconditions:**

* User is logged in.
* User is on the inventory page.
* All products from the product test data set are available.

**Test Data:**

* User: `standard_user`
* Products: all products from the product test data set

**Steps:**

1. Add all products from the product test data set to the cart.
2. Verify that the cart badge matches the number of added products.
3. Remove the tested product from the inventory page.
4. Verify that the badge count decreases by one.
5. Open the cart page.
6. Verify that the removed product is not displayed.
7. Repeat independently for every product from the test data set.

**Expected Result:**

* Every tested product can be removed from the cart from the inventory page.
* Cart badge count decreases correctly.
* Cart page does not contain the removed product.

**Notes:**

* This is the full regression variant of TC-INVENTORY-016.
* Navigation is included because the cart page is opened to verify the removal result.

---

### TC-INVENTORY-021 — Product details can be opened from product name for example product

**Type:** Smoke / Navigation\
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
* Example product: first representative product from centralized product test data

**Steps:**

1. Click the product name for the example product.
2. Observe the product details page.

**Expected Result:**

* Product details page is opened for the example product.
* Product details page URL contains the expected product ID.
* Displayed product details match the selected product.

**Notes:**

* This is the representative smoke variant of navigation through a product name.
* Full all-products regression coverage is tracked in TC-INVENTORY-013.

---

### TC-INVENTORY-022 — Product details can be opened from product image for example product

**Type:** Smoke / Navigation\
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
* Example product: first representative product from centralized product test data

**Steps:**

1. Click the product image for the example product.
2. Observe the product details page.

**Expected Result:**

* Product details page is opened for the example product.
* Product details page URL contains the expected product ID.
* Displayed product details match the selected product.

**Notes:**

* This is the representative smoke variant of navigation through a product image.
* Full all-products regression coverage is tracked in TC-INVENTORY-014.