import pytest
from playwright.sync_api import expect

from framework.assertions.product_assertions import (
    assert_inventory_product_item_displays_expected_product,
    assert_product_details_page_displays_expected_product,
    convert_price_to_float,
)
from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage
from test_data.product_test_data import LIST_OF_PRODUCTS

FIRST_EXAMPLE_PRODUCT = LIST_OF_PRODUCTS[0]
SECOND_EXAMPLE_PRODUCT = LIST_OF_PRODUCTS[1]


@pytest.mark.smoke
@pytest.mark.ui
@pytest.mark.parametrize(
    "_case_id",
    ["TC-INVENTORY-001"],
    ids=["TC-INVENTORY-001"],
)
def test_inventory_page_is_visible_after_successful_login(
    logged_in_inventory_page: InventoryPage, _case_id: str
):
    expect(logged_in_inventory_page.page).to_have_url(InventoryPage.URL)
    expect(logged_in_inventory_page.get_inventory_container()).to_be_visible()
    expect(logged_in_inventory_page.get_product_list()).to_be_visible()


@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.parametrize(
    "_case_id",
    ["TC-INVENTORY-002"],
    ids=["TC-INVENTORY-002"],
)
def test_product_list_is_displayed_with_expected_products(
    logged_in_inventory_page: InventoryPage, _case_id: str
):
    expected_product_names = [product["product_name"] for product in LIST_OF_PRODUCTS]

    actual_product_names = logged_in_inventory_page.get_product_names()

    expect(logged_in_inventory_page.get_product_list()).to_be_visible()
    expect(logged_in_inventory_page.get_product_item_or_items()).to_have_count(
        len(LIST_OF_PRODUCTS)
    )
    assert set(actual_product_names) == set(expected_product_names), (
        f"Expected product names: {expected_product_names}, " f"but got: {actual_product_names}"
    )


@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.parametrize(
    "product",
    LIST_OF_PRODUCTS,
    ids=[f"TC-INVENTORY-003-{product['product_id']}" for product in LIST_OF_PRODUCTS],
)
def test_product_item_elements_are_displayed(logged_in_inventory_page: InventoryPage, product):
    assert_inventory_product_item_displays_expected_product(
        inventory_page=logged_in_inventory_page,
        product=product,
    )


@pytest.mark.smoke
@pytest.mark.navigation
@pytest.mark.parametrize(
    "_case_id",
    ["TC-INVENTORY-004"],
    ids=["TC-INVENTORY-004"],
)
def test_open_cart_page_from_inventory(logged_in_inventory_page: InventoryPage, _case_id: str):
    expect(logged_in_inventory_page.get_shopping_cart_link()).to_be_visible()

    cart_page = logged_in_inventory_page.open_cart()

    expect(cart_page.page).to_have_url(CartPage.URL)
    expect(cart_page.get_cart_contents_container()).to_be_visible()


@pytest.mark.smoke
@pytest.mark.navigation
@pytest.mark.parametrize(
    "_case_id",
    ["TC-INVENTORY-005"],
    ids=["TC-INVENTORY-005"],
)
def test_user_can_add_product_to_cart_from_inventory(
    logged_in_inventory_page: InventoryPage, _case_id: str
):
    logged_in_inventory_page.add_product_to_cart(FIRST_EXAMPLE_PRODUCT["product_name"])

    cart_page = logged_in_inventory_page.open_cart()

    expect(
        cart_page.get_product_item_by_name(FIRST_EXAMPLE_PRODUCT["product_name"])
    ).to_be_visible()


@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.parametrize(
    "_case_id",
    ["TC-INVENTORY-006"],
    ids=["TC-INVENTORY-006"],
)
def test_add_to_cart_button_changes_to_remove_after_adding_product_from_inventory(
    logged_in_inventory_page: InventoryPage, _case_id: str
):
    first_product = logged_in_inventory_page.get_product_item_by_name(
        FIRST_EXAMPLE_PRODUCT["product_name"]
    )
    second_product = logged_in_inventory_page.get_product_item_by_name(
        SECOND_EXAMPLE_PRODUCT["product_name"]
    )

    expect(logged_in_inventory_page.get_add_to_cart_button_from_item(first_product)).to_be_visible()
    expect(logged_in_inventory_page.get_remove_button_from_item(first_product)).to_be_hidden()

    expect(
        logged_in_inventory_page.get_add_to_cart_button_from_item(second_product)
    ).to_be_visible()
    expect(logged_in_inventory_page.get_remove_button_from_item(second_product)).to_be_hidden()

    logged_in_inventory_page.get_add_to_cart_button_from_item(first_product).click()

    expect(logged_in_inventory_page.get_add_to_cart_button_from_item(first_product)).to_be_hidden()
    expect(logged_in_inventory_page.get_remove_button_from_item(first_product)).to_be_visible()

    expect(
        logged_in_inventory_page.get_add_to_cart_button_from_item(second_product)
    ).to_be_visible()
    expect(logged_in_inventory_page.get_remove_button_from_item(second_product)).to_be_hidden()


@pytest.mark.smoke
@pytest.mark.ui
@pytest.mark.parametrize(
    "_case_id",
    ["TC-INVENTORY-007"],
    ids=["TC-INVENTORY-007"],
)
def test_cart_badge_is_displayed_after_adding_one_product(
    logged_in_inventory_page: InventoryPage, _case_id: str
):
    logged_in_inventory_page.add_product_to_cart(FIRST_EXAMPLE_PRODUCT["product_name"])

    expect(logged_in_inventory_page.get_shopping_cart_badge()).to_be_visible()
    expect(logged_in_inventory_page.get_shopping_cart_badge()).to_have_text("1")


@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.parametrize(
    "_case_id",
    ["TC-INVENTORY-008"],
    ids=["TC-INVENTORY-008"],
)
def test_cart_badge_count_updates_after_adding_multiple_products(
    logged_in_inventory_page: InventoryPage, _case_id: str
):
    tested_products = [
        FIRST_EXAMPLE_PRODUCT,
        SECOND_EXAMPLE_PRODUCT,
    ]

    for product in tested_products:
        logged_in_inventory_page.add_product_to_cart(product["product_name"])

    expect(logged_in_inventory_page.get_shopping_cart_badge()).to_be_visible()
    expect(logged_in_inventory_page.get_shopping_cart_badge()).to_have_text(
        str(len(tested_products))
    )


@pytest.mark.sorting
@pytest.mark.parametrize(
    "_case_id",
    ["TC-INVENTORY-009"],
    ids=["TC-INVENTORY-009"],
)
def test_sorting_products_by_name_a_to_z(logged_in_inventory_page: InventoryPage, _case_id: str):
    sorted_product_names = sorted(product["product_name"] for product in LIST_OF_PRODUCTS)

    logged_in_inventory_page.sort_products_by(InventoryPage.SORT_NAME_ASC)

    actual_product_names = logged_in_inventory_page.get_product_names()

    assert sorted_product_names == actual_product_names, (
        f"Expected product names order: {sorted_product_names}, " f"but got: {actual_product_names}"
    )


@pytest.mark.sorting
@pytest.mark.parametrize(
    "_case_id",
    ["TC-INVENTORY-010"],
    ids=["TC-INVENTORY-010"],
)
def test_sorting_products_by_name_z_to_a(logged_in_inventory_page: InventoryPage, _case_id: str):
    sorted_product_names = sorted(
        (product["product_name"] for product in LIST_OF_PRODUCTS),
        reverse=True,
    )

    logged_in_inventory_page.sort_products_by(InventoryPage.SORT_NAME_DESC)

    actual_product_names = logged_in_inventory_page.get_product_names()

    assert sorted_product_names == actual_product_names, (
        f"Expected product names order: {sorted_product_names}, " f"but got: {actual_product_names}"
    )


@pytest.mark.sorting
@pytest.mark.parametrize(
    "_case_id",
    ["TC-INVENTORY-011"],
    ids=["TC-INVENTORY-011"],
)
def test_sorting_products_by_price_low_to_high(
    logged_in_inventory_page: InventoryPage, _case_id: str
):
    sorted_product_prices = sorted(
        convert_price_to_float(product["product_price"]) for product in LIST_OF_PRODUCTS
    )

    logged_in_inventory_page.sort_products_by(InventoryPage.SORT_PRICE_LOW_HIGH)

    actual_product_prices = [
        convert_price_to_float(price) for price in logged_in_inventory_page.get_product_prices()
    ]

    assert sorted_product_prices == actual_product_prices, (
        f"Expected product prices order: {sorted_product_prices}, "
        f"but got: {actual_product_prices}"
    )


@pytest.mark.sorting
@pytest.mark.parametrize(
    "_case_id",
    ["TC-INVENTORY-012"],
    ids=["TC-INVENTORY-012"],
)
def test_sorting_products_by_price_high_to_low(
    logged_in_inventory_page: InventoryPage, _case_id: str
):
    sorted_product_prices = sorted(
        (convert_price_to_float(product["product_price"]) for product in LIST_OF_PRODUCTS),
        reverse=True,
    )

    logged_in_inventory_page.sort_products_by(InventoryPage.SORT_PRICE_HIGH_LOW)

    actual_product_prices = [
        convert_price_to_float(price) for price in logged_in_inventory_page.get_product_prices()
    ]

    assert sorted_product_prices == actual_product_prices, (
        f"Expected product prices order: {sorted_product_prices}, "
        f"but got: {actual_product_prices}"
    )


@pytest.mark.regression
@pytest.mark.navigation
@pytest.mark.parametrize(
    "product",
    LIST_OF_PRODUCTS,
    ids=[f"TC-INVENTORY-013-{product['product_id']}" for product in LIST_OF_PRODUCTS],
)
def test_product_details_can_be_opened_for_all_products_by_product_name_on_inventory_page(
    logged_in_inventory_page: InventoryPage, product
):
    product_details = logged_in_inventory_page.open_product_details_by_name(product["product_name"])

    assert_product_details_page_displays_expected_product(
        product_details,
        product,
    )

    expect(product_details.get_back_to_products_button()).to_be_visible()


@pytest.mark.regression
@pytest.mark.navigation
@pytest.mark.parametrize(
    "product",
    LIST_OF_PRODUCTS,
    ids=[f"TC-INVENTORY-014-{product['product_id']}" for product in LIST_OF_PRODUCTS],
)
def test_product_details_can_be_opened_for_all_products_by_product_image_on_inventory_page(
    logged_in_inventory_page: InventoryPage, product
):
    product_details = logged_in_inventory_page.open_product_details_by_image(
        product["product_name"]
    )

    assert_product_details_page_displays_expected_product(
        product_details,
        product,
    )

    expect(product_details.get_back_to_products_button()).to_be_visible()


@pytest.mark.regression
@pytest.mark.navigation
@pytest.mark.parametrize(
    "product",
    LIST_OF_PRODUCTS,
    ids=[f"TC-INVENTORY-015-{product['product_id']}" for product in LIST_OF_PRODUCTS],
)
def test_all_products_can_be_added_to_cart_from_inventory_page(
    logged_in_inventory_page: InventoryPage, product
):
    logged_in_inventory_page.add_product_to_cart(product["product_name"])

    cart_page = logged_in_inventory_page.open_cart()

    expect(cart_page.get_product_item_by_name(product["product_name"])).to_be_visible()


@pytest.mark.smoke
@pytest.mark.navigation
@pytest.mark.parametrize(
    "_case_id",
    ["TC-INVENTORY-016"],
    ids=["TC-INVENTORY-016"],
)
def test_product_can_be_removed_from_cart_from_inventory_page(
    inventory_page_with_one_product_in_cart: tuple[
        InventoryPage,
        dict[str, str],
    ],
    _case_id: str,
):
    inventory_page, product = inventory_page_with_one_product_in_cart

    cart_page = inventory_page.open_cart()

    expect(cart_page.get_product_item_by_name(product["product_name"])).to_be_visible()

    inventory_page = cart_page.continue_shopping()

    inventory_page.remove_product_from_cart(product["product_name"])

    cart_page = inventory_page.open_cart()

    expect(cart_page.get_product_item_by_name(product["product_name"])).not_to_be_visible()


@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.parametrize(
    "_case_id",
    ["TC-INVENTORY-017"],
    ids=["TC-INVENTORY-017"],
)
def test_remove_button_changes_back_to_add_to_cart_after_removing_product_from_inventory(
    inventory_page_with_one_product_in_cart: tuple[
        InventoryPage,
        dict[str, str],
    ],
    _case_id: str,
):
    inventory_page, product = inventory_page_with_one_product_in_cart

    product_locator = inventory_page.get_product_item_by_name(product["product_name"])

    expect(inventory_page.get_remove_button_from_item(product_locator)).to_be_visible()
    expect(inventory_page.get_add_to_cart_button_from_item(product_locator)).not_to_be_visible()

    inventory_page.remove_product_from_cart(product["product_name"])

    expect(inventory_page.get_remove_button_from_item(product_locator)).not_to_be_visible()
    expect(inventory_page.get_add_to_cart_button_from_item(product_locator)).to_be_visible()


@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.parametrize(
    "_case_id",
    ["TC-INVENTORY-018"],
    ids=["TC-INVENTORY-018"],
)
def test_cart_badge_count_updates_after_removing_one_of_multiple_products_from_inventory_page(
    logged_in_inventory_page: InventoryPage, _case_id: str
):
    logged_in_inventory_page.add_product_to_cart(FIRST_EXAMPLE_PRODUCT["product_name"])
    logged_in_inventory_page.add_product_to_cart(SECOND_EXAMPLE_PRODUCT["product_name"])

    expect(logged_in_inventory_page.get_shopping_cart_badge()).to_have_text("2")

    logged_in_inventory_page.remove_product_from_cart(FIRST_EXAMPLE_PRODUCT["product_name"])

    expect(logged_in_inventory_page.get_shopping_cart_badge()).to_have_text("1")


@pytest.mark.smoke
@pytest.mark.ui
@pytest.mark.parametrize(
    "_case_id",
    ["TC-INVENTORY-019"],
    ids=["TC-INVENTORY-019"],
)
def test_cart_badge_disappears_after_removing_last_product_from_inventory_page(
    inventory_page_with_one_product_in_cart: tuple[
        InventoryPage,
        dict[str, str],
    ],
    _case_id: str,
):
    inventory_page, product = inventory_page_with_one_product_in_cart

    expect(inventory_page.get_shopping_cart_badge()).to_be_visible()
    expect(inventory_page.get_shopping_cart_badge()).to_have_text("1")

    inventory_page.remove_product_from_cart(product["product_name"])

    expect(inventory_page.get_shopping_cart_badge()).not_to_be_visible()


@pytest.mark.regression
@pytest.mark.navigation
@pytest.mark.parametrize(
    "product",
    LIST_OF_PRODUCTS,
    ids=[f"TC-INVENTORY-020-{product['product_id']}" for product in LIST_OF_PRODUCTS],
)
def test_all_products_can_be_removed_from_cart_from_inventory_page(
    logged_in_inventory_page: InventoryPage, product
):
    for item in LIST_OF_PRODUCTS:
        logged_in_inventory_page.add_product_to_cart(item["product_name"])

    expect(logged_in_inventory_page.get_shopping_cart_badge()).to_have_text(
        str(len(LIST_OF_PRODUCTS))
    )

    logged_in_inventory_page.remove_product_from_cart(product["product_name"])

    expect(logged_in_inventory_page.get_shopping_cart_badge()).to_have_text(
        str(len(LIST_OF_PRODUCTS) - 1)
    )

    cart_page = logged_in_inventory_page.open_cart()

    expect(cart_page.get_product_item_by_name(product["product_name"])).not_to_be_visible()


@pytest.mark.smoke
@pytest.mark.navigation
@pytest.mark.parametrize(
    "_case_id",
    ["TC-INVENTORY-021"],
    ids=["TC-INVENTORY-021"],
)
def test_product_details_can_be_opened_from_product_name_for_example_product(
    logged_in_inventory_page: InventoryPage, _case_id: str
):
    product_details = logged_in_inventory_page.open_product_details_by_name(
        FIRST_EXAMPLE_PRODUCT["product_name"]
    )

    assert_product_details_page_displays_expected_product(
        product_details,
        FIRST_EXAMPLE_PRODUCT,
    )

    expect(product_details.get_back_to_products_button()).to_be_visible()


@pytest.mark.smoke
@pytest.mark.navigation
@pytest.mark.parametrize(
    "_case_id",
    ["TC-INVENTORY-022"],
    ids=["TC-INVENTORY-022"],
)
def test_product_details_can_be_opened_from_product_image_for_example_product(
    logged_in_inventory_page: InventoryPage, _case_id: str
):
    product_details = logged_in_inventory_page.open_product_details_by_image(
        FIRST_EXAMPLE_PRODUCT["product_name"]
    )

    assert_product_details_page_displays_expected_product(
        product_details,
        FIRST_EXAMPLE_PRODUCT,
    )

    expect(product_details.get_back_to_products_button()).to_be_visible()
