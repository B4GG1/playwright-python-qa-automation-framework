import pytest
from playwright.sync_api import expect

from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage


@pytest.mark.smoke
@pytest.mark.ui
@pytest.mark.parametrize("_case_id", ["TC-CART-001"], ids=["TC-CART-001"])
def test_open_cart_page_from_inventory(logged_in_inventory_page: InventoryPage, _case_id: str):
    expect(logged_in_inventory_page.get_shopping_cart_link()).to_be_visible()
    cart_page = logged_in_inventory_page.open_cart()
    expect(cart_page.page).to_have_url(CartPage.URL)
    expect(cart_page.get_cart_contents_container()).to_be_visible()
