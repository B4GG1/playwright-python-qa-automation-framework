import pytest
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage


@pytest.mark.smoke
@pytest.mark.ui
def test_sauce_demo_smoke(page: Page):
    login_page = LoginPage(page)
    login_page.open()
    expect(page).to_have_title("Swag Labs")
