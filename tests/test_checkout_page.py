import pytest
from playwright.sync_api import expect

from framework.assertions.product_assertions import (
    assert_checkout_overview_price_summary_displays_expected_info,
    assert_checkout_product_item_displays_expected_product,
    assert_inventory_product_item_displays_expected_product,
    assert_product_details_page_displays_expected_product,
)
from pages.cart_page import CartPage
from pages.checkout_page import (
    CheckoutCompletePage,
    CheckoutInformationPage,
    CheckoutOverviewPage,
)
from pages.inventory_page import InventoryPage
from test_data.checkout_test_data import (
    CHECKOUT_COMPLETE_HEADER,
    CHECKOUT_COMPLETE_MESSAGE,
    CHECKOUT_REQUIRED_FIRST_NAME_ERROR,
    CHECKOUT_REQUIRED_LAST_NAME_ERROR,
    CHECKOUT_REQUIRED_POSTAL_CODE_ERROR,
    CHECKOUT_STEP_ONE_TITLE,
    VALID_CHECKOUT_CUSTOMER,
)
from test_data.product_test_data import LIST_OF_PRODUCTS

FIRST_EXAMPLE_PRODUCT = LIST_OF_PRODUCTS[0]
SECOND_EXAMPLE_PRODUCT = LIST_OF_PRODUCTS[1]


@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.parametrize(
    "_case_id",
    ["TC-CHECKOUT-001"],
    ids=["TC-CHECKOUT-001"],
)
def test_checkout_information_form_displays_required_customer_fields(
    checkout_step_one_page_with_one_product: tuple[
        CheckoutInformationPage,
        dict[str, str],
    ],
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
@pytest.mark.parametrize(
    "_case_id",
    ["TC-CHECKOUT-003"],
    ids=["TC-CHECKOUT-003"],
)
def test_checkout_information_form_requires_first_name(
    checkout_step_one_page_with_one_product: tuple[
        CheckoutInformationPage,
        dict[str, str],
    ],
    _case_id: str,
):
    checkout_step_one_page, product = checkout_step_one_page_with_one_product

    checkout_step_one_page.fill_checkout_info_form(
        "",
        VALID_CHECKOUT_CUSTOMER["last_name"],
        VALID_CHECKOUT_CUSTOMER["postal_code"],
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
@pytest.mark.parametrize(
    "_case_id",
    ["TC-CHECKOUT-004"],
    ids=["TC-CHECKOUT-004"],
)
def test_checkout_information_form_requires_last_name(
    checkout_step_one_page_with_one_product: tuple[
        CheckoutInformationPage,
        dict[str, str],
    ],
    _case_id: str,
):
    checkout_step_one_page, product = checkout_step_one_page_with_one_product

    checkout_step_one_page.fill_checkout_info_form(
        VALID_CHECKOUT_CUSTOMER["first_name"],
        "",
        VALID_CHECKOUT_CUSTOMER["postal_code"],
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
@pytest.mark.parametrize(
    "_case_id",
    ["TC-CHECKOUT-005"],
    ids=["TC-CHECKOUT-005"],
)
def test_checkout_information_form_requires_postal_code(
    checkout_step_one_page_with_one_product: tuple[
        CheckoutInformationPage,
        dict[str, str],
    ],
    _case_id: str,
):
    checkout_step_one_page, product = checkout_step_one_page_with_one_product

    checkout_step_one_page.fill_checkout_info_form(
        VALID_CHECKOUT_CUSTOMER["first_name"],
        VALID_CHECKOUT_CUSTOMER["last_name"],
        "",
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
    ["TC-CHECKOUT-006"],
    ids=["TC-CHECKOUT-006"],
)
def test_input_error_icons_are_displayed_after_failed_checkout_information_submission(
    checkout_step_one_page_with_one_product: tuple[
        CheckoutInformationPage,
        dict[str, str],
    ],
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
    ["TC-CHECKOUT-007"],
    ids=["TC-CHECKOUT-007"],
)
def test_checkout_information_error_message_can_be_closed_after_validation_failure(
    checkout_step_one_page_with_one_product: tuple[
        CheckoutInformationPage,
        dict[str, str],
    ],
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
@pytest.mark.navigation
@pytest.mark.e2e
@pytest.mark.parametrize(
    "_case_id",
    ["TC-CHECKOUT-008"],
    ids=["TC-CHECKOUT-008"],
)
def test_checkout_information_form_continues_to_overview_when_valid_data_is_provided(
    checkout_step_two_page_with_one_product: tuple[
        CheckoutOverviewPage,
        dict[str, str],
    ],
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
    ["TC-CHECKOUT-009"],
    ids=["TC-CHECKOUT-009"],
)
def test_checkout_information_cancel_returns_to_cart_and_preserves_cart_item(
    checkout_step_one_page_with_one_product: tuple[
        CheckoutInformationPage,
        dict[str, str],
    ],
    _case_id: str,
):
    checkout_step_one, product = checkout_step_one_page_with_one_product

    expect(checkout_step_one.page).to_have_url(CheckoutInformationPage.URL)

    cart_page = checkout_step_one.cancel_checkout()

    expect(cart_page.page).to_have_url(CartPage.URL)
    expect(cart_page.get_product_item_by_name(product["product_name"])).to_be_visible()
    expect(checkout_step_one.get_checkout_info_block()).not_to_be_visible()


@pytest.mark.smoke
@pytest.mark.ui
@pytest.mark.e2e
@pytest.mark.parametrize(
    "_case_id",
    ["TC-CHECKOUT-010"],
    ids=["TC-CHECKOUT-010"],
)
def test_checkout_overview_displays_selected_product(
    checkout_step_two_page_with_one_product: tuple[
        CheckoutOverviewPage,
        dict[str, str],
    ],
    _case_id: str,
):
    checkout_page_two, product = checkout_step_two_page_with_one_product

    expect(checkout_page_two.get_checkout_summary_container()).to_be_visible()

    product_item = checkout_page_two.get_product_item_by_name(product["product_name"])

    expect(checkout_page_two.get_product_name_from_item(product_item)).to_be_visible()
    expect(checkout_page_two.get_product_description_from_item(product_item)).to_be_visible()
    expect(checkout_page_two.get_product_price_from_item(product_item)).to_be_visible()
    expect(checkout_page_two.get_product_quantity_from_item(product_item)).to_be_visible()
    expect(checkout_page_two.get_product_quantity_from_item(product_item)).to_have_text("1")


@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.parametrize(
    "product",
    LIST_OF_PRODUCTS,
    ids=[f"TC-CHECKOUT-011-{product['product_id']}" for product in LIST_OF_PRODUCTS],
)
def test_checkout_overview_displays_each_selected_product(
    logged_in_inventory_page: InventoryPage,
    product,
):
    logged_in_inventory_page.add_product_to_cart(product["product_name"])

    cart_page = logged_in_inventory_page.open_cart()
    checkout_step_one = cart_page.checkout()

    checkout_step_one.fill_checkout_info_form(
        VALID_CHECKOUT_CUSTOMER["first_name"],
        VALID_CHECKOUT_CUSTOMER["last_name"],
        VALID_CHECKOUT_CUSTOMER["postal_code"],
    )

    checkout_step_two = checkout_step_one.continue_checkout()

    assert_checkout_product_item_displays_expected_product(
        checkout_overview_page=checkout_step_two,
        product=product,
        expected_quantity="1",
    )


@pytest.mark.smoke
@pytest.mark.ui
@pytest.mark.e2e
@pytest.mark.parametrize(
    "_case_id",
    ["TC-CHECKOUT-012"],
    ids=["TC-CHECKOUT-012"],
)
def test_checkout_overview_price_summary_is_correct_for_one_product(
    checkout_step_two_page_with_one_product: tuple[
        CheckoutOverviewPage,
        dict[str, str],
    ],
    _case_id: str,
):
    checkout_step_two, product = checkout_step_two_page_with_one_product

    assert_checkout_overview_price_summary_displays_expected_info(
        checkout_step_two,
        product,
    )


@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.parametrize(
    "_case_id",
    ["TC-CHECKOUT-013"],
    ids=["TC-CHECKOUT-013"],
)
def test_checkout_overview_price_summary_is_correct_for_multiple_products(
    logged_in_inventory_page: InventoryPage,
    _case_id: str,
):
    logged_in_inventory_page.add_product_to_cart(FIRST_EXAMPLE_PRODUCT["product_name"])
    logged_in_inventory_page.add_product_to_cart(SECOND_EXAMPLE_PRODUCT["product_name"])

    cart_page = logged_in_inventory_page.open_cart()
    checkout_step_one = cart_page.checkout()

    checkout_step_one.fill_checkout_info_form(
        VALID_CHECKOUT_CUSTOMER["first_name"],
        VALID_CHECKOUT_CUSTOMER["last_name"],
        VALID_CHECKOUT_CUSTOMER["postal_code"],
    )

    checkout_step_two = checkout_step_one.continue_checkout()

    assert_checkout_product_item_displays_expected_product(
        checkout_overview_page=checkout_step_two,
        product=FIRST_EXAMPLE_PRODUCT,
        expected_quantity="1",
    )

    assert_checkout_product_item_displays_expected_product(
        checkout_overview_page=checkout_step_two,
        product=SECOND_EXAMPLE_PRODUCT,
        expected_quantity="1",
    )

    assert_checkout_overview_price_summary_displays_expected_info(
        checkout_step_two,
        FIRST_EXAMPLE_PRODUCT,
        SECOND_EXAMPLE_PRODUCT,
    )


@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.navigation
@pytest.mark.parametrize(
    "_case_id",
    ["TC-CHECKOUT-014"],
    ids=["TC-CHECKOUT-014"],
)
def test_checkout_overview_cancel_returns_to_inventory_page(
    checkout_step_two_page_with_one_product: tuple[
        CheckoutOverviewPage,
        dict[str, str],
    ],
    _case_id: str,
):
    checkout_step_two, product = checkout_step_two_page_with_one_product

    inventory_page = checkout_step_two.cancel_checkout()

    expect(inventory_page.page).to_have_url(InventoryPage.URL)
    expect(inventory_page.get_inventory_container()).to_be_visible()
    expect(checkout_step_two.get_checkout_summary_container()).not_to_be_visible()

    assert_inventory_product_item_displays_expected_product(
        inventory_page,
        product,
        True,
    )

    expect(inventory_page.get_shopping_cart_badge()).to_be_visible()
    expect(inventory_page.get_shopping_cart_badge()).to_have_text("1")


@pytest.mark.smoke
@pytest.mark.ui
@pytest.mark.navigation
@pytest.mark.parametrize(
    "_case_id",
    ["TC-CHECKOUT-015"],
    ids=["TC-CHECKOUT-015"],
)
def test_product_details_can_be_opened_from_checkout_overview_item_name(
    checkout_step_two_page_with_one_product: tuple[
        CheckoutOverviewPage,
        dict[str, str],
    ],
    _case_id: str,
):
    checkout_step_two, product = checkout_step_two_page_with_one_product

    product_details_page = checkout_step_two.open_product_details_by_name(product["product_name"])

    expect(checkout_step_two.get_checkout_summary_container()).not_to_be_visible()
    expect(product_details_page.get_shopping_cart_badge()).to_be_visible()
    expect(product_details_page.get_shopping_cart_badge()).to_have_text("1")

    assert_product_details_page_displays_expected_product(
        product_details_page,
        product,
        is_added=True,
    )


@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.navigation
@pytest.mark.parametrize(
    "product",
    LIST_OF_PRODUCTS,
    ids=[f"TC-CHECKOUT-016-{product['product_id']}" for product in LIST_OF_PRODUCTS],
)
def test_product_details_can_be_opened_from_checkout_overview_item_name_for_each_product(
    logged_in_inventory_page: InventoryPage,
    product,
):
    logged_in_inventory_page.add_product_to_cart(product["product_name"])

    cart_page = logged_in_inventory_page.open_cart()
    checkout_step_one = cart_page.checkout()

    checkout_step_one.fill_checkout_info_form(
        VALID_CHECKOUT_CUSTOMER["first_name"],
        VALID_CHECKOUT_CUSTOMER["last_name"],
        VALID_CHECKOUT_CUSTOMER["postal_code"],
    )

    checkout_step_two = checkout_step_one.continue_checkout()

    product_details_page = checkout_step_two.open_product_details_by_name(product["product_name"])

    expect(checkout_step_two.get_checkout_summary_container()).not_to_be_visible()
    expect(product_details_page.get_shopping_cart_badge()).to_be_visible()
    expect(product_details_page.get_shopping_cart_badge()).to_have_text("1")

    assert_product_details_page_displays_expected_product(
        product_details_page,
        product,
        is_added=True,
    )


@pytest.mark.smoke
@pytest.mark.navigation
@pytest.mark.e2e
@pytest.mark.parametrize(
    "_case_id",
    ["TC-CHECKOUT-017"],
    ids=["TC-CHECKOUT-017"],
)
def test_finish_button_completes_checkout_and_opens_order_confirmation_page(
    checkout_step_two_page_with_one_product: tuple[
        CheckoutOverviewPage,
        dict[str, str],
    ],
    _case_id: str,
):
    checkout_step_two, product = checkout_step_two_page_with_one_product

    checkout_last_step = checkout_step_two.finish_checkout()

    expect(checkout_last_step.page).to_have_url(CheckoutCompletePage.URL)
    expect(checkout_last_step.get_checkout_complete_header()).to_be_visible()
    expect(checkout_last_step.get_checkout_complete_text()).to_be_visible()
    expect(checkout_last_step.get_back_home_button()).to_be_visible()


@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.parametrize(
    "_case_id",
    ["TC-CHECKOUT-018"],
    ids=["TC-CHECKOUT-018"],
)
def test_checkout_complete_page_displays_order_confirmation_message(
    checkout_last_step_page_with_one_product: tuple[
        CheckoutCompletePage,
        dict[str, str],
    ],
    _case_id: str,
):
    checkout_last_step_page = checkout_last_step_page_with_one_product[0]

    expect(checkout_last_step_page.get_checkout_complete_container()).to_be_visible()
    expect(checkout_last_step_page.get_pony_express_img()).to_be_visible()

    expect(checkout_last_step_page.get_checkout_complete_header()).to_be_visible()
    expect(checkout_last_step_page.get_checkout_complete_header()).to_have_text(
        CHECKOUT_COMPLETE_HEADER
    )

    expect(checkout_last_step_page.get_checkout_complete_text()).to_be_visible()
    expect(checkout_last_step_page.get_checkout_complete_text()).to_have_text(
        CHECKOUT_COMPLETE_MESSAGE
    )

    expect(checkout_last_step_page.get_back_home_button()).to_be_visible()


@pytest.mark.smoke
@pytest.mark.navigation
@pytest.mark.e2e
@pytest.mark.parametrize(
    "_case_id",
    ["TC-CHECKOUT-020"],
    ids=["TC-CHECKOUT-020"],
)
def test_back_home_returns_to_inventory_page_after_order_completion(
    checkout_last_step_page_with_one_product: tuple[
        CheckoutCompletePage,
        dict[str, str],
    ],
    _case_id: str,
):
    checkout_last_step_page, product = checkout_last_step_page_with_one_product

    inventory_page = checkout_last_step_page.back_home()

    expect(inventory_page.page).to_have_url(InventoryPage.URL)
    expect(checkout_last_step_page.get_checkout_complete_container()).not_to_be_visible()
    expect(inventory_page.get_inventory_container()).to_be_visible()

    assert_inventory_product_item_displays_expected_product(
        inventory_page,
        product,
        False,
    )
