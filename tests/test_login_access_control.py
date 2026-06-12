import pytest
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from test_data.login_test_data import (
    ACCESS_DENIED_CART_ERROR,
    ACCESS_DENIED_INVENTORY_ERROR,
    CART_URL_SUFFIX,
    INVENTORY_URL_SUFFIX,
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
    page.goto(login_page.URL + INVENTORY_URL_SUFFIX)
    expect(page).to_have_url(login_page.URL)
    expect(page.locator("[data-test='inventory-container']")).not_to_be_visible()
    assert login_page.get_error_message_text() == ACCESS_DENIED_INVENTORY_ERROR


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
    page.goto(login_page.URL + CART_URL_SUFFIX)
    expect(page).to_have_url(login_page.URL)
    expect(page.locator("[data-test='inventory-container']")).not_to_be_visible()
    assert login_page.get_error_message_text() == ACCESS_DENIED_CART_ERROR
