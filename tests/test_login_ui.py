import pytest
from playwright.sync_api import expect

from pages.login_page import LoginPage
from test_data.login_test_data import INVALID_LOGIN_CASES, INVENTORY_URL_PATTERN


@pytest.mark.smoke
@pytest.mark.ui
@pytest.mark.parametrize(
    "_case_id",
    ["TC-LOGIN-010"],
    ids=["TC-LOGIN-010"],
)
def test_login_page_elements_are_visible(opened_login_page: LoginPage, _case_id: str):
    expect(opened_login_page.get_username_input()).to_be_visible()
    expect(opened_login_page.get_password_input()).to_be_visible()
    expect(opened_login_page.get_login_button()).to_be_visible()
    expect(opened_login_page.get_credentials_container()).to_be_visible()


@pytest.mark.ui
@pytest.mark.parametrize(
    "_case_id",
    ["TC-LOGIN-009"],
    ids=["TC-LOGIN-009"],
)
def test_error_message_can_be_close(opened_login_page: LoginPage, _case_id: str):
    opened_login_page.login(INVALID_LOGIN_CASES[0]["username"], INVALID_LOGIN_CASES[0]["password"])
    expect(opened_login_page.page).not_to_have_url(INVENTORY_URL_PATTERN)
    expect(opened_login_page.get_error_message()).to_be_visible()
    opened_login_page.close_error_message()
    expect(opened_login_page.get_error_message()).to_be_hidden()


@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.parametrize(
    "_case_id",
    ["TC-LOGIN-011"],
    ids=["TC-LOGIN-011"],
)
def test_password_field_masking_input(opened_login_page: LoginPage, _case_id: str):
    password_field = opened_login_page.get_password_input()
    expect(password_field).to_be_visible()
    expect(password_field).to_have_attribute("type", "password")
    password_field.fill("secret_sauce")
    expect(password_field).to_have_attribute("type", "password")
