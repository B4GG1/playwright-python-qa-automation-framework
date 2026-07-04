import pytest
from playwright.sync_api import expect

from framework.assertions.product_assertions import (
    assert_product_details_page_displays_expected_product,
)
from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage
from pages.product_details_page import ProductDetailsPage
from test_data.product_test_data import LIST_OF_PRODUCTS

FIRST_EXAMPLE_PRODUCT = LIST_OF_PRODUCTS[0]
SECOND_EXAMPLE_PRODUCT = LIST_OF_PRODUCTS[1]


@pytest.mark.smoke
@pytest.mark.ui
@pytest.mark.parametrize(
    "_case_id",
    ["TC-PRODUCT-DETAILS-001"],
    ids=["TC-PRODUCT-DETAILS-001"],
)
def test_product_details_content_is_displayed_for_selected_product(
    logged_in_inventory_page: InventoryPage, _case_id: str
):
    product_details = logged_in_inventory_page.open_product_details_by_name(
        FIRST_EXAMPLE_PRODUCT["product_name"]
    )

    assert_product_details_page_displays_expected_product(
        product_details_page=product_details,
        product=FIRST_EXAMPLE_PRODUCT,
    )

    expect(product_details.get_back_to_products_button()).to_be_visible()


@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.parametrize(
    "product",
    LIST_OF_PRODUCTS,
    ids=[f"TC-PRODUCT-DETAILS-002-{product['product_id']}" for product in LIST_OF_PRODUCTS],
)
def test_product_details_content_matches_product_data_for_each_product(
    logged_in_inventory_page: InventoryPage, product
):
    product_details = logged_in_inventory_page.open_product_details_by_name(product["product_name"])

    assert_product_details_page_displays_expected_product(
        product_details_page=product_details,
        product=product,
    )

    expect(product_details.get_back_to_products_button()).to_be_visible()


@pytest.mark.regression
@pytest.mark.navigation
@pytest.mark.ui
@pytest.mark.parametrize(
    "_case_id",
    ["TC-PRODUCT-DETAILS-003"],
    ids=["TC-PRODUCT-DETAILS-003"],
)
def test_return_from_product_details_to_inventory_page(
    logged_in_inventory_page: InventoryPage, _case_id: str
):
    product = FIRST_EXAMPLE_PRODUCT

    product_details = logged_in_inventory_page.open_product_details_by_name(product["product_name"])

    expect(product_details.page).to_have_url(f"{product_details.URL}{product['product_id']}")

    inventory_page = product_details.return_to_inventory()

    expect(inventory_page.page).to_have_url(InventoryPage.URL)
    expect(inventory_page.get_inventory_container()).to_be_visible()
    expect(inventory_page.get_product_list()).to_be_visible()


@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.parametrize(
    "_case_id",
    ["TC-PRODUCT-DETAILS-004"],
    ids=["TC-PRODUCT-DETAILS-004"],
)
def test_add_to_cart_button_changes_to_remove_after_adding_product_from_details_page(
    logged_in_inventory_page: InventoryPage, _case_id: str
):
    details_page = logged_in_inventory_page.open_product_details_by_name(
        FIRST_EXAMPLE_PRODUCT["product_name"]
    )
    product_item = details_page.get_product_item_or_items()

    expect(details_page.get_remove_button_from_item(product_item)).to_be_hidden()
    expect(details_page.get_add_to_cart_button_from_item(product_item)).to_be_visible()

    details_page.add_product_to_cart()

    expect(details_page.get_remove_button_from_item(product_item)).to_be_visible()
    expect(details_page.get_add_to_cart_button_from_item(product_item)).to_be_hidden()

    expect(details_page.page).to_have_url(
        f'{ProductDetailsPage.URL}{FIRST_EXAMPLE_PRODUCT["product_id"]}'
    )


@pytest.mark.smoke
@pytest.mark.ui
@pytest.mark.positive
@pytest.mark.parametrize(
    "_case_id",
    ["TC-PRODUCT-DETAILS-005"],
    ids=["TC-PRODUCT-DETAILS-005"],
)
def test_product_can_be_added_to_cart_from_product_details_page(
    logged_in_inventory_page: InventoryPage, _case_id: str
):
    details_page = logged_in_inventory_page.open_product_details_by_name(
        FIRST_EXAMPLE_PRODUCT["product_name"]
    )
    details_page.add_product_to_cart()
    expect(details_page.page).to_have_url(
        f'{ProductDetailsPage.URL}{FIRST_EXAMPLE_PRODUCT["product_id"]}'
    )
    expect(details_page.get_shopping_cart_badge()).to_have_text("1")
    cart_page = details_page.open_cart()
    expect(
        cart_page.get_product_item_by_name(FIRST_EXAMPLE_PRODUCT["product_name"])
    ).to_be_visible()


@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.positive
@pytest.mark.parametrize(
    "product",
    LIST_OF_PRODUCTS,
    ids=[f"TC-PRODUCT-DETAILS-006-{product['product_id']}" for product in LIST_OF_PRODUCTS],
)
def test_all_products_can_be_added_to_cart_from_product_details_page(
    logged_in_inventory_page: InventoryPage, product
):
    details_page = logged_in_inventory_page.open_product_details_by_name(product["product_name"])
    details_page.add_product_to_cart()
    expect(details_page.page).to_have_url(f'{ProductDetailsPage.URL}{product["product_id"]}')
    expect(details_page.get_shopping_cart_badge()).to_have_text("1")
    cart_page = details_page.open_cart()
    expect(cart_page.get_product_item_by_name(product["product_name"])).to_be_visible()


@pytest.mark.smoke
@pytest.mark.ui
@pytest.mark.positive
@pytest.mark.parametrize(
    "_case_id",
    ["TC-PRODUCT-DETAILS-007"],
    ids=["TC-PRODUCT-DETAILS-007"],
)
def test_product_can_be_removed_from_cart_from_product_details_page(
    inventory_page_with_one_product_in_cart: tuple[InventoryPage, dict[str, str]], _case_id: str
):
    inventory_page, product = inventory_page_with_one_product_in_cart
    details_page = inventory_page.open_product_details_by_name(product["product_name"])
    details_page.remove_product_from_cart()
    expect(details_page.page).to_have_url(f'{ProductDetailsPage.URL}{product["product_id"]}')
    expect(details_page.get_shopping_cart_badge()).not_to_be_visible()

    cart_page = details_page.open_cart()
    expect(cart_page.get_product_item_by_name(product["product_name"])).not_to_be_visible()


@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.parametrize(
    "_case_id",
    ["TC-PRODUCT-DETAILS-008"],
    ids=["TC-PRODUCT-DETAILS-008"],
)
def test_remove_button_changes_to_add_to_cart_after_removing_product_from_details_page(
    logged_in_inventory_page: InventoryPage, _case_id: str
):
    details_page = logged_in_inventory_page.open_product_details_by_name(
        FIRST_EXAMPLE_PRODUCT["product_name"]
    )
    product_item = details_page.get_product_item_or_items()

    details_page.add_product_to_cart()

    expect(details_page.get_remove_button_from_item(product_item)).to_be_visible()
    expect(details_page.get_add_to_cart_button_from_item(product_item)).to_be_hidden()

    details_page.remove_product_from_cart()

    expect(details_page.get_remove_button_from_item(product_item)).to_be_hidden()
    expect(details_page.get_add_to_cart_button_from_item(product_item)).to_be_visible()

    expect(details_page.page).to_have_url(
        f'{ProductDetailsPage.URL}{FIRST_EXAMPLE_PRODUCT["product_id"]}'
    )


@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.parametrize(
    "_case_id",
    ["TC-PRODUCT-DETAILS-009"],
    ids=["TC-PRODUCT-DETAILS-009"],
)
def test_cart_badge_is_displayed_after_adding_product_from_product_details_page(
    logged_in_inventory_page: InventoryPage, _case_id: str
):
    details_page = logged_in_inventory_page.open_product_details_by_name(
        FIRST_EXAMPLE_PRODUCT["product_name"]
    )
    expect(details_page.get_shopping_cart_badge()).to_be_hidden()
    details_page.add_product_to_cart()
    expect(details_page.get_shopping_cart_badge()).to_be_visible()
    expect(details_page.get_shopping_cart_badge()).to_have_text("1")


@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.parametrize(
    "_case_id",
    ["TC-PRODUCT-DETAILS-010"],
    ids=["TC-PRODUCT-DETAILS-010"],
)
def test_cart_badge_count_updates_after_adding_product_from_details_page(
    logged_in_inventory_page: InventoryPage, _case_id: str
):
    details_page = logged_in_inventory_page.open_product_details_by_name(
        FIRST_EXAMPLE_PRODUCT["product_name"]
    )
    expect(details_page.get_shopping_cart_badge()).to_be_hidden()
    details_page.add_product_to_cart()
    expect(details_page.get_shopping_cart_badge()).to_be_visible()
    expect(details_page.get_shopping_cart_badge()).to_have_text("1")

    inventory_page = details_page.return_to_inventory()
    details_page = inventory_page.open_product_details_by_name(
        SECOND_EXAMPLE_PRODUCT["product_name"]
    )
    details_page.add_product_to_cart()
    expect(details_page.get_shopping_cart_badge()).to_be_visible()
    expect(details_page.get_shopping_cart_badge()).to_have_text("2")


@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.parametrize(
    "_case_id",
    ["TC-PRODUCT-DETAILS-011"],
    ids=["TC-PRODUCT-DETAILS-011"],
)
def test_cart_badge_count_updates_after_removing_one_of_multiple_products_from_details_page(
    logged_in_inventory_page: InventoryPage, _case_id: str
):
    logged_in_inventory_page.add_product_to_cart(FIRST_EXAMPLE_PRODUCT["product_name"])
    logged_in_inventory_page.add_product_to_cart(SECOND_EXAMPLE_PRODUCT["product_name"])

    details_page = logged_in_inventory_page.open_product_details_by_name(
        FIRST_EXAMPLE_PRODUCT["product_name"]
    )
    expect(details_page.get_shopping_cart_badge()).to_have_text("2")

    details_page.remove_product_from_cart()
    expect(details_page.get_shopping_cart_badge()).to_have_text("1")


@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.parametrize(
    "_case_id",
    ["TC-PRODUCT-DETAILS-012"],
    ids=["TC-PRODUCT-DETAILS-012"],
)
def test_cart_badge_disappears_after_removing_last_product_from_product_details_page(
    logged_in_inventory_page: InventoryPage, _case_id: str
):
    details_page = logged_in_inventory_page.open_product_details_by_name(
        FIRST_EXAMPLE_PRODUCT["product_name"]
    )
    expect(details_page.get_shopping_cart_badge()).to_be_hidden()
    details_page.add_product_to_cart()
    expect(details_page.get_shopping_cart_badge()).to_be_visible()
    expect(details_page.get_shopping_cart_badge()).to_have_text("1")
    details_page.remove_product_from_cart()
    expect(details_page.get_shopping_cart_badge()).to_be_hidden()


@pytest.mark.regression
@pytest.mark.navigation
@pytest.mark.ui
@pytest.mark.parametrize(
    "_case_id",
    ["TC-PRODUCT-DETAILS-013"],
    ids=["TC-PRODUCT-DETAILS-013"],
)
def test_cart_page_can_be_opened_from_product_details_page(
    logged_in_inventory_page: InventoryPage, _case_id: str
):
    details_page = logged_in_inventory_page.open_product_details_by_name(
        FIRST_EXAMPLE_PRODUCT["product_name"]
    )
    cart_page = details_page.open_cart()
    expect(cart_page.page).to_have_url(CartPage.URL)
    expect(cart_page.get_cart_contents_container()).to_be_visible()


@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.positive
@pytest.mark.parametrize(
    "product",
    LIST_OF_PRODUCTS,
    ids=[f"TC-PRODUCT-DETAILS-014-{product['product_id']}" for product in LIST_OF_PRODUCTS],
)
def test_all_products_can_be_removed_from_cart_from_product_details_page(
    logged_in_inventory_page: InventoryPage, product
):
    for item in LIST_OF_PRODUCTS:
        logged_in_inventory_page.add_product_to_cart(item["product_name"])

    details_page = logged_in_inventory_page.open_product_details_by_name(product["product_name"])
    details_page.remove_product_from_cart()
    expect(details_page.get_shopping_cart_badge()).to_have_text(str(len(LIST_OF_PRODUCTS) - 1))
    cart_page = details_page.open_cart()
    expect(cart_page.get_product_item_by_name(product["product_name"])).to_be_hidden()
