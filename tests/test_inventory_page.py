import pytest
from playwright.sync_api import expect

from pages.inventory_page import InventoryPage
from test_data.inventory_test_data import LIST_OF_PRODUCTS


@pytest.mark.smoke
@pytest.mark.ui
@pytest.mark.positive
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


@pytest.mark.smoke
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
    expect(logged_in_inventory_page.get_product_cards()).to_have_count(len(LIST_OF_PRODUCTS))
    assert set(actual_product_names) == set(expected_product_names), (
        f"Expected product names: {expected_product_names}, " f"but got: {actual_product_names}"
    )


@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.parametrize(
    "product",
    LIST_OF_PRODUCTS,
    ids=[f"TC-INVENTORY-003-{index}" for index, _product in enumerate(LIST_OF_PRODUCTS, start=1)],
)
def test_product_card_elements_are_displayed(logged_in_inventory_page: InventoryPage, product):
    actual_product = logged_in_inventory_page.get_product_card_by_name(product["product_name"])
    expect(actual_product).to_have_count(1)
    expect(actual_product).to_be_visible()

    actual_product_name = logged_in_inventory_page.get_product_name_from_card(actual_product)
    expect(actual_product_name).to_be_visible()
    expect(actual_product_name).to_have_text(product["product_name"])

    actual_product_description = logged_in_inventory_page.get_product_description_from_card(
        actual_product
    )
    expect(actual_product_description).to_be_visible()
    expect(actual_product_description).to_have_text(product["product_description"])

    actual_product_price = logged_in_inventory_page.get_product_price_from_card(actual_product)
    expect(actual_product_price).to_be_visible()
    expect(actual_product_price).to_have_text(product["product_price"])

    actual_product_img = logged_in_inventory_page.get_product_image_from_card(actual_product)
    expect(actual_product_img).to_be_visible()
    expect(actual_product_img).to_have_attribute("src", product["product_image"])

    expect(
        logged_in_inventory_page.get_add_to_cart_button_from_card(actual_product)
    ).to_be_visible()
