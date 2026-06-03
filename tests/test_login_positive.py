import pytest
from playwright.sync_api import expect

from pages.login_page import LoginPage
from test_data.login_test_data import INVENTORY_URL_PATTERN, VALID_USER_CASES


@pytest.mark.smoke
@pytest.mark.ui
@pytest.mark.positive
@pytest.mark.parametrize(
    "case", VALID_USER_CASES, ids=[case["case_id"] for case in VALID_USER_CASES]
)
def test_valid_user_can_log_in_successfully(opened_login_page: LoginPage, case):
    opened_login_page.login(case["username"], case["password"])
    expect(opened_login_page.page).to_have_url(INVENTORY_URL_PATTERN)
    expect(opened_login_page.page.locator("[data-test='inventory-container']")).to_be_visible()
