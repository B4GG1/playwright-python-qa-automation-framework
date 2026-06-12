import pytest
from playwright.sync_api import Page, expect

from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from pages.product_details_page import ProductDetailsPage
from test_data.inventory_test_data import LIST_OF_PRODUCTS
from test_data.login_test_data import (
    ACCESS_DENIED_TEMPLATE_ERROR,
    CART_URL_SUFFIX,
    INVENTORY_URL_SUFFIX,
    ITEM_URL_SUFFIX,
)


@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.negative
@pytest.mark.parametrize(
    "_case_id",
    ["TC-LOGIN-013"],
    ids=["TC-LOGIN-013"],
)
def test_direct_inventory_access_without_login_is_blocked(page: Page, _case_id: str):
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)
    inventory_page.open()
    expect(page).to_have_url(login_page.URL)
    expect(inventory_page.get_inventory_container()).not_to_be_visible()
    assert login_page.get_error_message_text() == ACCESS_DENIED_TEMPLATE_ERROR.format(
        url_suffix=INVENTORY_URL_SUFFIX
    )


@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.negative
@pytest.mark.parametrize(
    "_case_id",
    ["TC-LOGIN-014"],
    ids=["TC-LOGIN-014"],
)
def test_direct_cart_access_without_login_is_blocked(page: Page, _case_id: str):
    login_page = LoginPage(page)
    cart_page = CartPage(page)
    cart_page.open()
    expect(page).to_have_url(login_page.URL)
    expect(cart_page.get_cart_contents_container()).not_to_be_visible()
    assert login_page.get_error_message_text() == ACCESS_DENIED_TEMPLATE_ERROR.format(
        url_suffix=CART_URL_SUFFIX
    )


@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.negative
@pytest.mark.parametrize(
    "_case_id",
    ["TC-LOGIN-015"],
    ids=["TC-LOGIN-015"],
)
def test_direct_item_page_access_without_login_is_blocked(page: Page, _case_id: str):
    login_page = LoginPage(page)
    product = LIST_OF_PRODUCTS[1]
    item_page = ProductDetailsPage(page)
    item_page.open_by_id(product["product_id"])
    expect(page).to_have_url(login_page.URL)
    expect(item_page.get_item_details_container()).not_to_be_visible()
    assert login_page.get_error_message_text() == ACCESS_DENIED_TEMPLATE_ERROR.format(
        url_suffix=ITEM_URL_SUFFIX
    )
