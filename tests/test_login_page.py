import re

import pytest
from playwright.sync_api import Page, expect

from framework.assertions.product_assertions import (
    assert_failed_login_input_error_icons_are_displayed,
)
from pages.cart_page import CartPage
from pages.checkout_page import (
    CheckoutCompletePage,
    CheckoutInformationPage,
    CheckoutOverviewPage,
)
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from pages.product_details_page import ProductDetailsPage
from test_data.login_test_data import (
    ACCESS_DENIED_TEMPLATE_ERROR,
    CART_URL_SUFFIX,
    CHECKOUT_COMPLETE_URL_SUFFIX,
    CHECKOUT_STEP_ONE_URL_SUFFIX,
    CHECKOUT_STEP_TWO_URL_SUFFIX,
    EMPTY_LOGIN_CASES,
    INVALID_LOGIN_CASES,
    INVENTORY_URL_SUFFIX,
    ITEM_URL_SUFFIX,
    LOCKED_OUT_USER_CASES,
    VALID_USER_CASES,
)
from test_data.product_test_data import LIST_OF_PRODUCTS


@pytest.mark.smoke
@pytest.mark.parametrize("_case_id", ["SMOKE"], ids=["SMOKE"])
def test_sauce_demo_smoke(
    opened_login_page: LoginPage,
    _case_id: str,
):
    expect(opened_login_page.page).to_have_title("Swag Labs")
    expect(opened_login_page.get_credentials_container()).to_be_visible()


@pytest.mark.smoke
@pytest.mark.e2e
@pytest.mark.parametrize(
    "case",
    VALID_USER_CASES,
    ids=[case["case_id"] for case in VALID_USER_CASES],
)
def test_valid_user_can_log_in_successfully(
    opened_login_page: LoginPage,
    case,
):
    opened_login_page.login(case["username"], case["password"])
    inventory_page = InventoryPage(opened_login_page.page)

    expect(inventory_page.page).to_have_url(re.compile(rf".*{INVENTORY_URL_SUFFIX}"))
    expect(inventory_page.get_inventory_container()).to_be_visible()


@pytest.mark.ui
@pytest.mark.parametrize(
    "case",
    [
        pytest.param(
            INVALID_LOGIN_CASES[0],
            marks=pytest.mark.smoke,
        ),
        *[
            pytest.param(
                case,
                marks=pytest.mark.regression,
            )
            for case in INVALID_LOGIN_CASES[1:]
        ],
    ],
    ids=[case["case_id"] for case in INVALID_LOGIN_CASES],
)
def test_login_with_invalid_credentials(
    opened_login_page: LoginPage,
    case,
):
    opened_login_page.login(case["username"], case["password"])

    expect(opened_login_page.page).not_to_have_url(re.compile(rf".*{INVENTORY_URL_SUFFIX}"))
    expect(opened_login_page.get_error_message()).to_have_text(case["expected_error"])

    assert_failed_login_input_error_icons_are_displayed(opened_login_page)


@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.parametrize(
    "case",
    EMPTY_LOGIN_CASES,
    ids=[case["case_id"] for case in EMPTY_LOGIN_CASES],
)
def test_login_with_empty_credentials(
    opened_login_page: LoginPage,
    case,
):
    opened_login_page.login(case["username"], case["password"])

    expect(opened_login_page.page).not_to_have_url(re.compile(rf".*{INVENTORY_URL_SUFFIX}"))
    expect(opened_login_page.get_error_message()).to_have_text(case["expected_error"])

    assert_failed_login_input_error_icons_are_displayed(opened_login_page)


@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.parametrize(
    "case",
    LOCKED_OUT_USER_CASES,
    ids=[case["case_id"] for case in LOCKED_OUT_USER_CASES],
)
def test_login_for_locked_out_user(
    opened_login_page: LoginPage,
    case,
):
    opened_login_page.login(case["username"], case["password"])

    expect(opened_login_page.page).not_to_have_url(re.compile(rf".*{INVENTORY_URL_SUFFIX}"))
    expect(opened_login_page.get_error_message()).to_have_text(case["expected_error"])

    assert_failed_login_input_error_icons_are_displayed(opened_login_page)


@pytest.mark.smoke
@pytest.mark.ui
@pytest.mark.parametrize(
    "_case_id",
    ["TC-LOGIN-009"],
    ids=["TC-LOGIN-009"],
)
def test_error_message_can_be_closed(
    opened_login_page: LoginPage,
    _case_id: str,
):
    opened_login_page.login(
        INVALID_LOGIN_CASES[0]["username"],
        INVALID_LOGIN_CASES[0]["password"],
    )

    expect(opened_login_page.page).not_to_have_url(re.compile(rf".*{INVENTORY_URL_SUFFIX}"))
    expect(opened_login_page.get_error_message()).to_be_visible()

    opened_login_page.close_error_message()

    expect(opened_login_page.get_error_message()).to_be_hidden()


@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.parametrize(
    "_case_id",
    ["TC-LOGIN-010"],
    ids=["TC-LOGIN-010"],
)
def test_login_page_elements_are_visible(
    opened_login_page: LoginPage,
    _case_id: str,
):
    expect(opened_login_page.get_username_input()).to_be_visible()
    expect(opened_login_page.get_password_input()).to_be_visible()
    expect(opened_login_page.get_login_button()).to_be_visible()
    expect(opened_login_page.get_credentials_container()).to_be_visible()


@pytest.mark.ui
@pytest.mark.parametrize(
    "_case_id",
    ["TC-LOGIN-011"],
    ids=["TC-LOGIN-011"],
)
def test_password_field_masking_input(
    opened_login_page: LoginPage,
    _case_id: str,
):
    password_field = opened_login_page.get_password_input()

    expect(password_field).to_be_visible()
    expect(password_field).to_have_attribute("type", "password")

    password_field.fill("secret_sauce")

    expect(password_field).to_have_attribute("type", "password")


@pytest.mark.ui
@pytest.mark.parametrize(
    "_case_id",
    ["TC-LOGIN-012"],
    ids=["TC-LOGIN-012"],
)
def test_user_can_log_in_by_pressing_enter_key(
    opened_login_page: LoginPage,
    standard_user: dict[str, str],
    _case_id: str,
):
    opened_login_page.get_username_input().fill(standard_user["username"])
    opened_login_page.get_password_input().fill(standard_user["password"])
    opened_login_page.get_password_input().press("Enter")

    inventory_page = InventoryPage(opened_login_page.page)

    expect(inventory_page.page).to_have_url(re.compile(rf".*{INVENTORY_URL_SUFFIX}"))
    expect(inventory_page.get_inventory_container()).to_be_visible()


@pytest.mark.security
@pytest.mark.parametrize(
    "_case_id",
    ["TC-LOGIN-013"],
    ids=["TC-LOGIN-013"],
)
def test_direct_inventory_access_without_login_is_blocked(
    page: Page,
    _case_id: str,
):
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)

    inventory_page.open()

    expect(page).to_have_url(login_page.URL)
    expect(inventory_page.get_inventory_container()).not_to_be_visible()
    expect(login_page.get_error_message()).to_have_text(
        ACCESS_DENIED_TEMPLATE_ERROR.format(url_suffix=INVENTORY_URL_SUFFIX)
    )


@pytest.mark.security
@pytest.mark.parametrize(
    "_case_id",
    ["TC-LOGIN-014"],
    ids=["TC-LOGIN-014"],
)
def test_direct_cart_access_without_login_is_blocked(
    page: Page,
    _case_id: str,
):
    login_page = LoginPage(page)
    cart_page = CartPage(page)

    cart_page.open()

    expect(page).to_have_url(login_page.URL)
    expect(cart_page.get_cart_contents_container()).not_to_be_visible()
    expect(login_page.get_error_message()).to_have_text(
        ACCESS_DENIED_TEMPLATE_ERROR.format(url_suffix=CART_URL_SUFFIX)
    )


@pytest.mark.security
@pytest.mark.parametrize(
    "_case_id",
    ["TC-LOGIN-015"],
    ids=["TC-LOGIN-015"],
)
def test_direct_item_page_access_without_login_is_blocked(
    page: Page,
    _case_id: str,
):
    login_page = LoginPage(page)
    product = LIST_OF_PRODUCTS[1]
    item_page = ProductDetailsPage(page)

    item_page.open(product["product_id"])

    expect(page).to_have_url(login_page.URL)
    expect(item_page.get_product_item_or_items()).not_to_be_visible()
    expect(login_page.get_error_message()).to_have_text(
        ACCESS_DENIED_TEMPLATE_ERROR.format(url_suffix=ITEM_URL_SUFFIX)
    )


@pytest.mark.security
@pytest.mark.parametrize(
    "_case_id",
    ["TC-LOGIN-017"],
    ids=["TC-LOGIN-017"],
)
def test_direct_access_to_check_out_information_page_without_login_is_blocked(
    page: Page,
    _case_id: str,
):
    login_page = LoginPage(page)
    checkout_step_one = CheckoutInformationPage(page)

    checkout_step_one.open()

    expect(page).to_have_url(login_page.URL)
    expect(checkout_step_one.get_checkout_info_block()).not_to_be_visible()
    expect(login_page.get_error_message()).to_have_text(
        ACCESS_DENIED_TEMPLATE_ERROR.format(url_suffix=CHECKOUT_STEP_ONE_URL_SUFFIX)
    )


@pytest.mark.security
@pytest.mark.parametrize(
    "_case_id",
    ["TC-LOGIN-018"],
    ids=["TC-LOGIN-018"],
)
def test_direct_access_to_check_out_overview_page_without_login_is_blocked(
    page: Page,
    _case_id: str,
):
    login_page = LoginPage(page)
    checkout_step_two = CheckoutOverviewPage(page)

    checkout_step_two.open()

    expect(page).to_have_url(login_page.URL)
    expect(checkout_step_two.get_checkout_summary_container()).not_to_be_visible()
    expect(login_page.get_error_message()).to_have_text(
        ACCESS_DENIED_TEMPLATE_ERROR.format(url_suffix=CHECKOUT_STEP_TWO_URL_SUFFIX)
    )


@pytest.mark.security
@pytest.mark.parametrize(
    "_case_id",
    ["TC-LOGIN-019"],
    ids=["TC-LOGIN-019"],
)
def test_direct_access_to_check_out_complete_page_without_login_is_blocked(
    page: Page,
    _case_id: str,
):
    login_page = LoginPage(page)
    checkout_last_step = CheckoutCompletePage(page)

    checkout_last_step.open()

    expect(page).to_have_url(login_page.URL)
    expect(checkout_last_step.get_checkout_complete_container()).not_to_be_visible()
    expect(login_page.get_error_message()).to_have_text(
        ACCESS_DENIED_TEMPLATE_ERROR.format(url_suffix=CHECKOUT_COMPLETE_URL_SUFFIX)
    )
