import re

from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from test_data.login_test_data import EMPTY_LOGIN_CASES, INVALID_LOGIN_CASES, LOCKED_OUT_USER


def test_login_with_invalid_credentials(page: Page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login(INVALID_LOGIN_CASES[0]["username"], INVALID_LOGIN_CASES[0]["password"])
    expect(page).not_to_have_url(re.compile(".*inventory.html"))
    assert login_page.get_error_message() == INVALID_LOGIN_CASES[0]["expected_error"]


def test_login_with_empty_credentials(page: Page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login(EMPTY_LOGIN_CASES[0]["username"], EMPTY_LOGIN_CASES[0]["password"])
    expect(page).not_to_have_url(re.compile(".*inventory.html"))
    assert login_page.get_error_message() == EMPTY_LOGIN_CASES[0]["expected_error"]


def test_login_for_locked_out_user(page: Page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login(LOCKED_OUT_USER["username"], LOCKED_OUT_USER["password"])
    expect(page).not_to_have_url(re.compile(".*inventory.html"))
    assert login_page.get_error_message() == LOCKED_OUT_USER["expected_error"]
