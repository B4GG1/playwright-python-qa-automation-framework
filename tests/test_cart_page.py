import pytest
from playwright.sync_api import expect

from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage
from test_data.inventory_test_data import LIST_OF_PRODUCTS

EXAMPLE_PRODUCT = LIST_OF_PRODUCTS[0]


@pytest.mark.smoke
@pytest.mark.ui
@pytest.mark.parametrize("_case_id", ["TC-CART-001"], ids=["TC-CART-001"])
def test_open_cart_page_from_inventory(logged_in_inventory_page: InventoryPage, _case_id: str):
    expect(logged_in_inventory_page.get_shopping_cart_link()).to_be_visible()
    cart_page = logged_in_inventory_page.open_cart()
    expect(cart_page.page).to_have_url(CartPage.URL)
    expect(cart_page.get_cart_contents_container()).to_be_visible()


@pytest.mark.regression
@pytest.mark.positive
@pytest.mark.ui
@pytest.mark.parametrize("_case_id", ["TC-CART-003+TC-CART-007"], ids=["TC-CART-003+TC-CART-007"])
def test_user_can_add_product_to_cart(logged_in_inventory_page: InventoryPage, _case_id: str):
    logged_in_inventory_page.add_product_to_cart(EXAMPLE_PRODUCT["product_name"])
    cart_page = logged_in_inventory_page.open_cart()
    expect(cart_page.get_product_card_by_name(EXAMPLE_PRODUCT["product_name"])).to_be_visible()
