import pytest

from test_data.checkout_test_data import (
    CHECKOUT_COMPLETE_HEADER,
    CHECKOUT_COMPLETE_MESSAGE,
    CHECKOUT_OVERVIEW_PAYMENT_INFO,
    CHECKOUT_OVERVIEW_SHIPPING_INFO,
    ITEM_TOTAL_PREFIX,
    TAX_PERCENTAGE,
    TAX_PREFIX,
    TOTAL_PREFIX,
    VALID_CHECKOUT_CUSTOMER,
)

pytestmark = [
    pytest.mark.selenium,
    pytest.mark.e2e,
]


def test_valid_user_login_opens_inventory(
    selenium_opened_login_page,
    selenium_standard_user,
) -> None:
    selenium_opened_login_page.login(
        selenium_standard_user["username"],
        selenium_standard_user["password"],
    )

    from selenium_pages.inventory_page import SeleniumInventoryPage

    inventory_page = SeleniumInventoryPage(selenium_opened_login_page.driver)
    inventory_page.wait_until_loaded()

    assert selenium_opened_login_page.driver.current_url == inventory_page.build_url()


def test_inventory_product_opens_expected_product_details(
    selenium_logged_in_inventory_page,
    selenium_product,
) -> None:
    product_details_page = selenium_logged_in_inventory_page.open_product_details_by_name(
        selenium_product["product_name"]
    )

    assert product_details_page.driver.current_url == product_details_page.build_url(
        selenium_product["product_id"]
    )
    assert product_details_page.get_product_name() == selenium_product["product_name"]
    assert product_details_page.get_product_description() == selenium_product["product_description"]
    assert product_details_page.get_product_price() == selenium_product["product_price"]


def test_product_added_from_details_is_visible_in_cart(
    selenium_product_details_page,
) -> None:
    product_details_page, product = selenium_product_details_page

    product_details_page.add_product_to_cart()
    cart_page = product_details_page.open_cart()

    assert cart_page.driver.current_url == cart_page.build_url()

    cart_item = cart_page.get_product_item_by_name(product["product_name"])

    assert cart_page.get_product_name(cart_item) == product["product_name"]
    assert cart_page.get_product_description(cart_item) == product["product_description"]
    assert cart_page.get_product_price(cart_item) == product["product_price"]
    assert cart_page.get_product_quantity(cart_item) == "1"


def test_cart_opens_checkout_information(
    selenium_cart_page_with_product,
) -> None:
    cart_page, _ = selenium_cart_page_with_product

    checkout_information_page = cart_page.checkout()

    assert checkout_information_page.driver.current_url == checkout_information_page.build_url()


def test_valid_checkout_information_opens_overview(
    selenium_checkout_information_page_with_product,
) -> None:
    checkout_information_page, product = selenium_checkout_information_page_with_product

    checkout_information_page.fill_checkout_info(
        VALID_CHECKOUT_CUSTOMER["first_name"],
        VALID_CHECKOUT_CUSTOMER["last_name"],
        VALID_CHECKOUT_CUSTOMER["postal_code"],
    )

    checkout_overview_page = checkout_information_page.continue_checkout()

    assert checkout_overview_page.driver.current_url == checkout_overview_page.build_url()

    overview_item = checkout_overview_page.get_product_item_by_name(product["product_name"])

    assert checkout_overview_page.get_product_name(overview_item) == product["product_name"]


def test_checkout_overview_displays_expected_order(
    selenium_checkout_overview_page_with_product,
) -> None:
    checkout_overview_page, product = selenium_checkout_overview_page_with_product

    overview_item = checkout_overview_page.get_product_item_by_name(product["product_name"])

    assert checkout_overview_page.get_product_name(overview_item) == product["product_name"]
    assert (
        checkout_overview_page.get_product_description(overview_item)
        == product["product_description"]
    )
    assert checkout_overview_page.get_product_price(overview_item) == product["product_price"]
    assert checkout_overview_page.get_product_quantity(overview_item) == "1"

    assert checkout_overview_page.get_payment_info() == CHECKOUT_OVERVIEW_PAYMENT_INFO
    assert checkout_overview_page.get_shipping_info() == CHECKOUT_OVERVIEW_SHIPPING_INFO

    item_total = float(product["product_price"].replace("$", ""))
    expected_tax = item_total * TAX_PERCENTAGE / 100
    expected_total = item_total + expected_tax

    assert checkout_overview_page.get_item_total() == f"{ITEM_TOTAL_PREFIX}{item_total:.2f}"
    assert checkout_overview_page.get_tax() == f"{TAX_PREFIX}{expected_tax:.2f}"
    assert checkout_overview_page.get_total() == f"{TOTAL_PREFIX}{expected_total:.2f}"


def test_finish_checkout_displays_order_confirmation(
    selenium_checkout_overview_page_with_product,
) -> None:
    checkout_overview_page, _ = selenium_checkout_overview_page_with_product

    checkout_complete_page = checkout_overview_page.finish_checkout()

    assert checkout_complete_page.driver.current_url == checkout_complete_page.build_url()
    assert checkout_complete_page.get_complete_header() == CHECKOUT_COMPLETE_HEADER
    assert checkout_complete_page.get_complete_message() == CHECKOUT_COMPLETE_MESSAGE


def test_back_home_returns_to_inventory(
    selenium_checkout_complete_page_with_product,
) -> None:
    checkout_complete_page, product = selenium_checkout_complete_page_with_product

    inventory_page = checkout_complete_page.back_home()

    assert inventory_page.driver.current_url == inventory_page.build_url()

    inventory_item = inventory_page.get_product_item_by_name(product["product_name"])

    assert inventory_page.get_product_name(inventory_item) == product["product_name"]
    assert inventory_page.get_product_description(inventory_item) == product["product_description"]
    assert inventory_page.get_product_price(inventory_item) == product["product_price"]
