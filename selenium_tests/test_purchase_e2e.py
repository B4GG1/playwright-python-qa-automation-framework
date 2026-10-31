import pytest

from selenium_pages.cart_page import SeleniumCartPage
from selenium_pages.checkout_page import (
    SeleniumCheckoutCompletePage,
    SeleniumCheckoutOverviewPage,
)
from selenium_pages.inventory_page import SeleniumInventoryPage
from selenium_pages.login_page import SeleniumLoginPage
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
from test_data.login_test_data import VALID_USER_CASES
from test_data.product_test_data import LIST_OF_PRODUCTS


@pytest.mark.selenium
@pytest.mark.e2e
def test_complete_purchase_journey(selenium_driver) -> None:
    user = VALID_USER_CASES[0]
    product = LIST_OF_PRODUCTS[0]
    customer = VALID_CHECKOUT_CUSTOMER

    login_page = SeleniumLoginPage(selenium_driver)
    login_page.open()

    login_page.login(
        user["username"],
        user["password"],
    )

    inventory_page = SeleniumInventoryPage(selenium_driver)
    inventory_page.wait_until_loaded()

    assert selenium_driver.current_url == inventory_page.build_url()

    product_details_page = inventory_page.open_product_details_by_name(product["product_name"])

    assert selenium_driver.current_url == product_details_page.build_url(product["product_id"])
    assert product_details_page.get_product_name() == product["product_name"]
    assert product_details_page.get_product_description() == product["product_description"]
    assert product_details_page.get_product_price() == product["product_price"]

    product_details_page.add_product_to_cart()

    cart_page = product_details_page.open_cart()

    assert selenium_driver.current_url == SeleniumCartPage.build_url()

    cart_item = cart_page.get_product_item_by_name(product["product_name"])

    assert cart_page.get_product_name(cart_item) == product["product_name"]
    assert cart_page.get_product_description(cart_item) == product["product_description"]
    assert cart_page.get_product_price(cart_item) == product["product_price"]
    assert cart_page.get_product_quantity(cart_item) == "1"

    checkout_information_page = cart_page.checkout()

    checkout_information_page.fill_checkout_info(
        customer["first_name"],
        customer["last_name"],
        customer["postal_code"],
    )

    checkout_overview_page = checkout_information_page.continue_checkout()

    assert selenium_driver.current_url == SeleniumCheckoutOverviewPage.build_url()

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

    checkout_complete_page = checkout_overview_page.finish_checkout()

    assert selenium_driver.current_url == SeleniumCheckoutCompletePage.build_url()
    assert checkout_complete_page.get_complete_header() == CHECKOUT_COMPLETE_HEADER
    assert checkout_complete_page.get_complete_message() == CHECKOUT_COMPLETE_MESSAGE

    inventory_page = checkout_complete_page.back_home()

    assert selenium_driver.current_url == SeleniumInventoryPage.build_url()

    inventory_item = inventory_page.get_product_item_by_name(product["product_name"])

    assert inventory_page.get_product_name(inventory_item) == product["product_name"]
    assert inventory_page.get_product_description(inventory_item) == product["product_description"]
    assert inventory_page.get_product_price(inventory_item) == product["product_price"]
