import pytest
from playwright.sync_api import expect

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutInformationPage, CheckoutOverviewPage
from test_data.checkout_test_data import (
    CHECKOUT_REQUIRED_FIRST_NAME_ERROR,
    CHECKOUT_REQUIRED_LAST_NAME_ERROR,
    CHECKOUT_REQUIRED_POSTAL_CODE_ERROR,
    CHECKOUT_STEP_ONE_TITLE,
    VALID_CHECKOUT_CUSTOMER,
)


@pytest.mark.smoke
@pytest.mark.ui
@pytest.mark.parametrize(
    "_case_id",
    ["TC-CHECKOUT-001"],
    ids=["TC-CHECKOUT-001"],
)
def test_checkout_information_form_displays_required_customer_fields(
    checkout_step_one_page_with_one_product: tuple[CheckoutInformationPage, dict[str, str]],
    _case_id: str,
):
    checkout_page, product = checkout_step_one_page_with_one_product
    expect(checkout_page.get_checkout_info_block()).to_be_visible()
    expect(checkout_page.get_first_name_input()).to_be_visible()
    expect(checkout_page.get_last_name_input()).to_be_visible()
    expect(checkout_page.get_postal_code_input()).to_be_visible()
    expect(checkout_page.get_cancel_button()).to_be_visible()
    expect(checkout_page.get_continue_button()).to_be_visible()
    expect(checkout_page.get_title()).to_have_text(CHECKOUT_STEP_ONE_TITLE)


@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.navigation
@pytest.mark.parametrize(
    "_case_id",
    ["TC-CHECKOUT-002"],
    ids=["TC-CHECKOUT-002"],
)
def test_checkout_information_form_requires_first_name(
    checkout_step_one_page_with_one_product: tuple[CheckoutInformationPage, dict[str, str]],
    _case_id: str,
):
    checkout_step_one_page, product = checkout_step_one_page_with_one_product
    checkout_step_one_page.fill_checkout_info_form(
        "", VALID_CHECKOUT_CUSTOMER["last_name"], VALID_CHECKOUT_CUSTOMER["postal_code"]
    )
    checkout_step_two_page = checkout_step_one_page.continue_checkout()
    expect(checkout_step_one_page.page).to_have_url(CheckoutInformationPage.URL)
    expect(checkout_step_two_page.get_checkout_summary_container()).not_to_be_visible()
    expect(checkout_step_one_page.get_error_message()).to_be_visible()
    expect(checkout_step_one_page.get_error_message()).to_have_text(
        CHECKOUT_REQUIRED_FIRST_NAME_ERROR
    )


@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.navigation
@pytest.mark.parametrize(
    "_case_id",
    ["TC-CHECKOUT-003"],
    ids=["TC-CHECKOUT-003"],
)
def test_checkout_information_form_requires_last_name(
    checkout_step_one_page_with_one_product: tuple[CheckoutInformationPage, dict[str, str]],
    _case_id: str,
):
    checkout_step_one_page, product = checkout_step_one_page_with_one_product
    checkout_step_one_page.fill_checkout_info_form(
        VALID_CHECKOUT_CUSTOMER["first_name"], "", VALID_CHECKOUT_CUSTOMER["postal_code"]
    )
    checkout_step_two_page = checkout_step_one_page.continue_checkout()
    expect(checkout_step_one_page.page).to_have_url(CheckoutInformationPage.URL)
    expect(checkout_step_two_page.get_checkout_summary_container()).not_to_be_visible()
    expect(checkout_step_one_page.get_error_message()).to_be_visible()
    expect(checkout_step_one_page.get_error_message()).to_have_text(
        CHECKOUT_REQUIRED_LAST_NAME_ERROR
    )


@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.navigation
@pytest.mark.parametrize(
    "_case_id",
    ["TC-CHECKOUT-004"],
    ids=["TC-CHECKOUT-004"],
)
def test_checkout_information_form_requires_postal_code(
    checkout_step_one_page_with_one_product: tuple[CheckoutInformationPage, dict[str, str]],
    _case_id: str,
):
    checkout_step_one_page, product = checkout_step_one_page_with_one_product
    checkout_step_one_page.fill_checkout_info_form(
        VALID_CHECKOUT_CUSTOMER["first_name"], VALID_CHECKOUT_CUSTOMER["last_name"], ""
    )
    checkout_step_two_page = checkout_step_one_page.continue_checkout()
    expect(checkout_step_one_page.page).to_have_url(CheckoutInformationPage.URL)
    expect(checkout_step_two_page.get_checkout_summary_container()).not_to_be_visible()
    expect(checkout_step_one_page.get_error_message()).to_be_visible()
    expect(checkout_step_one_page.get_error_message()).to_have_text(
        CHECKOUT_REQUIRED_POSTAL_CODE_ERROR
    )


@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.parametrize(
    "_case_id",
    ["TC-CHECKOUT-005"],
    ids=["TC-CHECKOUT-005"],
)
def test_input_error_icons_are_displayed_after_failed_checkout_information_submission(
    checkout_step_one_page_with_one_product: tuple[CheckoutInformationPage, dict[str, str]],
    _case_id: str,
):
    checkout_step_one_page, product = checkout_step_one_page_with_one_product
    checkout_step_one_page.fill_checkout_info_form("", "", "")
    first_name_input = checkout_step_one_page.get_first_name_input()
    last_name_input = checkout_step_one_page.get_last_name_input()
    postal_code_input = checkout_step_one_page.get_postal_code_input()
    checkout_step_one_page.continue_checkout()
    expect(checkout_step_one_page.page).to_have_url(CheckoutInformationPage.URL)
    expect(checkout_step_one_page.get_error_message()).to_be_visible()
    expect(checkout_step_one_page.get_input_error_icon(first_name_input)).to_be_visible()
    expect(checkout_step_one_page.get_input_error_icon(last_name_input)).to_be_visible()
    expect(checkout_step_one_page.get_input_error_icon(postal_code_input)).to_be_visible()


@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.parametrize(
    "_case_id",
    ["TC-CHECKOUT-006"],
    ids=["TC-CHECKOUT-006"],
)
def test_checkout_information_error_message_can_be_closed_after_validation_failure(
    checkout_step_one_page_with_one_product: tuple[CheckoutInformationPage, dict[str, str]],
    _case_id: str,
):
    checkout_step_one_page, product = checkout_step_one_page_with_one_product
    checkout_step_one_page.fill_checkout_info_form("", "", "")
    checkout_step_two_page = checkout_step_one_page.continue_checkout()
    expect(checkout_step_one_page.get_error_message()).to_be_visible()
    expect(checkout_step_one_page.page).to_have_url(CheckoutInformationPage.URL)
    expect(checkout_step_two_page.get_checkout_summary_container()).not_to_be_visible()
    checkout_step_one_page.close_error_message()
    expect(checkout_step_one_page.get_error_message()).not_to_be_visible()


@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.navigation
@pytest.mark.parametrize(
    "_case_id",
    ["TC-CHECKOUT-007"],
    ids=["TC-CHECKOUT-007"],
)
def test_checkout_information_form_continues_to_overview_when_valid_data_is_provided(
    checkout_step_two_page_with_one_product: tuple[CheckoutOverviewPage, dict[str, str]],
    _case_id: str,
):
    checkout_step_two, product = checkout_step_two_page_with_one_product
    expect(checkout_step_two.page).to_have_url(CheckoutOverviewPage.URL)
    expect(checkout_step_two.get_checkout_summary_container()).to_be_visible()
    expect(checkout_step_two.get_product_item_by_name(product["product_name"])).to_be_visible()
    expect(checkout_step_two.get_finish_button()).to_be_visible()
    expect(checkout_step_two.get_cancel_button()).to_be_visible()


@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.navigation
@pytest.mark.parametrize(
    "_case_id",
    ["TC-CHECKOUT-008"],
    ids=["TC-CHECKOUT-008"],
)
def test_checkout_information_cancel_returns_to_cart_and_preserves_cart_item(
    checkout_step_one_page_with_one_product: tuple[CheckoutInformationPage, dict[str, str]],
    _case_id: str,
):
    checkout_step_one, product = checkout_step_one_page_with_one_product
    expect(checkout_step_one.page).to_have_url(CheckoutInformationPage.URL)
    cart_page = checkout_step_one.cancel_checkout()
    expect(cart_page.page).to_have_url(CartPage.URL)
    expect(cart_page.get_product_item_by_name(product["product_name"])).to_be_visible()
    expect(checkout_step_one.get_checkout_info_block()).not_to_be_visible()
