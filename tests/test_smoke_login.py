import pytest
from playwright.sync_api import expect

from pages.login_page import LoginPage


@pytest.mark.smoke
@pytest.mark.ui
@pytest.mark.parametrize("_case_id", ["SMOKE"], ids=["SMOKE"])
def test_sauce_demo_smoke(opened_login_page: LoginPage, _case_id: str):
    expect(opened_login_page.page).to_have_title("Swag Labs")
