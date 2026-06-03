import pytest
from playwright.sync_api import expect

from pages.login_page import LoginPage


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
