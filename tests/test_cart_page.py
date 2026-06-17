import pytest
from playwright.sync_api import expect

from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage
from test_data.inventory_test_data import LIST_OF_PRODUCTS

EXAMPLE_PRODUCT = LIST_OF_PRODUCTS[0]
MULTIPLE_EXAMPLE_PRODUCTS = LIST_OF_PRODUCTS[0:2]


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


@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.parametrize("_case_id", ["TC-CART-005"], ids=["TC-CART-005"])
def test_cart_badge_is_displayed_after_adding_one_product(
    logged_in_inventory_page: InventoryPage, _case_id: str
):
    logged_in_inventory_page.add_product_to_cart(EXAMPLE_PRODUCT["product_name"])
    expect(logged_in_inventory_page.get_shopping_cart_badge()).to_be_visible()
    expect(logged_in_inventory_page.get_shopping_cart_badge()).to_have_text("1")


@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.parametrize("_case_id", ["TC-CART-006"], ids=["TC-CART-006"])
def test_cart_badge_count_updates_after_adding_multiple_products(
    logged_in_inventory_page: InventoryPage, _case_id: str
):
    for product in MULTIPLE_EXAMPLE_PRODUCTS:
        logged_in_inventory_page.add_product_to_cart(product["product_name"])
    expect(logged_in_inventory_page.get_shopping_cart_badge()).to_be_visible()
    expect(logged_in_inventory_page.get_shopping_cart_badge()).to_have_text(
        str(len(MULTIPLE_EXAMPLE_PRODUCTS))
    )
