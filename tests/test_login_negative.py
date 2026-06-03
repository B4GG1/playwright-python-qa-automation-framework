import pytest
from playwright.sync_api import expect

from pages.login_page import LoginPage
from test_data.login_test_data import (
    EMPTY_LOGIN_CASES,
    INVALID_LOGIN_CASES,
    INVENTORY_URL_PATTERN,
    LOCKED_OUT_USER_CASES,
)


@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.negative
@pytest.mark.parametrize(
    "case", INVALID_LOGIN_CASES, ids=[case["case_id"] for case in INVALID_LOGIN_CASES]
)
def test_login_with_invalid_credentials(opened_login_page: LoginPage, case):
    opened_login_page.login(case["username"], case["password"])
    expect(opened_login_page.page).not_to_have_url(INVENTORY_URL_PATTERN)
    assert opened_login_page.get_error_message_text() == case["expected_error"]


@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.negative
@pytest.mark.parametrize(
    "case", EMPTY_LOGIN_CASES, ids=[case["case_id"] for case in EMPTY_LOGIN_CASES]
)
def test_login_with_empty_credentials(opened_login_page: LoginPage, case):
    opened_login_page.login(case["username"], case["password"])
    expect(opened_login_page.page).not_to_have_url(INVENTORY_URL_PATTERN)
    assert opened_login_page.get_error_message_text() == case["expected_error"]


@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.negative
@pytest.mark.parametrize(
    "case", LOCKED_OUT_USER_CASES, ids=[case["case_id"] for case in LOCKED_OUT_USER_CASES]
)
def test_login_for_locked_out_user(opened_login_page: LoginPage, case):
    opened_login_page.login(case["username"], case["password"])
    expect(opened_login_page.page).not_to_have_url(INVENTORY_URL_PATTERN)
    assert opened_login_page.get_error_message_text() == case["expected_error"]
