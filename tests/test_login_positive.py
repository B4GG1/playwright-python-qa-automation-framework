import re

import pytest
from playwright.sync_api import expect

from pages.login_page import LoginPage
from test_data.login_test_data import INVENTORY_URL_SUFFIX, VALID_USER_CASES


@pytest.mark.smoke
@pytest.mark.ui
@pytest.mark.positive
@pytest.mark.parametrize(
    "case", VALID_USER_CASES, ids=[case["case_id"] for case in VALID_USER_CASES]
)
def test_valid_user_can_log_in_successfully(opened_login_page: LoginPage, case):
    opened_login_page.login(case["username"], case["password"])
    expect(opened_login_page.page).to_have_url(re.compile(rf".*{INVENTORY_URL_SUFFIX}"))
    expect(opened_login_page.page.locator("[data-test='inventory-container']")).to_be_visible()


@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.positive
@pytest.mark.parametrize(
    "_case_id",
    ["TC-LOGIN-012"],
    ids=["TC-LOGIN-012"],
)
def test_user_can_log_in_by_pressing_enter_key(opened_login_page: LoginPage, _case_id: str):
    case = VALID_USER_CASES[0]
    opened_login_page.get_username_input().fill(case["username"])
    opened_login_page.get_password_input().fill(case["password"])
    opened_login_page.get_password_input().press("Enter")
    expect(opened_login_page.page).to_have_url(re.compile(rf".*{INVENTORY_URL_SUFFIX}"))
    expect(opened_login_page.page.locator("[data-test='inventory-container']")).to_be_visible()
