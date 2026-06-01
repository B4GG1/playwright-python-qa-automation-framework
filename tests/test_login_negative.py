import re

import pytest
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from test_data.login_test_data import EMPTY_LOGIN_CASES, INVALID_LOGIN_CASES, LOCKED_OUT_USER

INVENTORY_URL_PATTERN = re.compile(r".*inventory.html")


@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.negative
@pytest.mark.parametrize(
    "case", INVALID_LOGIN_CASES, ids=[case["case_id"] for case in INVALID_LOGIN_CASES]
)
def test_login_with_invalid_credentials(page: Page, case):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login(case["username"], case["password"])
    expect(page).not_to_have_url(INVENTORY_URL_PATTERN)
    assert login_page.get_error_message() == case["expected_error"]


@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.negative
@pytest.mark.parametrize(
    "case", EMPTY_LOGIN_CASES, ids=[case["case_id"] for case in EMPTY_LOGIN_CASES]
)
def test_login_with_empty_credentials(page: Page, case):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login(case["username"], case["password"])
    expect(page).not_to_have_url(INVENTORY_URL_PATTERN)
    assert login_page.get_error_message() == case["expected_error"]


@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.negative
def test_login_for_locked_out_user(page: Page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login(LOCKED_OUT_USER["username"], LOCKED_OUT_USER["password"])
    expect(page).not_to_have_url(INVENTORY_URL_PATTERN)
    assert login_page.get_error_message() == LOCKED_OUT_USER["expected_error"]
