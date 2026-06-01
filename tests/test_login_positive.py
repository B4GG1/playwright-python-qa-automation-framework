import re

import pytest
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from test_data.login_test_data import VALID_USER


@pytest.mark.smoke
@pytest.mark.ui
@pytest.mark.positive
def test_valid_user_can_log_in_successfully(page: Page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login(VALID_USER["username"], VALID_USER["password"])
    expect(page).to_have_url(re.compile(".*inventory.html"))
    expect(page.locator("[data-test='inventory-container']")).to_be_visible()
