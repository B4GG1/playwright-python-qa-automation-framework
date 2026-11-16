import pytest
from selenium.webdriver.support import expected_conditions as ec

from selenium_pages.cart_page import SeleniumCartPage
from selenium_pages.checkout_page import SeleniumCheckoutCompletePage, SeleniumCheckoutOverviewPage
from selenium_pages.inventory_page import SeleniumInventoryPage
from selenium_pages.login_page import SeleniumLoginPage
from selenium_pages.product_details_page import SeleniumProductDetailsPage
from test_data.checkout_test_data import (
    CHECKOUT_OVERVIEW_PAYMENT_INFO,
    CHECKOUT_OVERVIEW_SHIPPING_INFO,
    ITEM_TOTAL_PREFIX,
    TAX_PERCENTAGE,
    TAX_PREFIX,
    TOTAL_PREFIX,
)


@pytest.mark.selenium
def test_valid_user_can_log_in_successfully(
    selenium_opened_login_page: SeleniumLoginPage,
    selenium_standard_user: dict[str, str],
) -> None:
    selenium_opened_login_page.login(
        selenium_standard_user["username"],
        selenium_standard_user["password"],
    )

    inventory_page = SeleniumInventoryPage(selenium_opened_login_page.driver)

    inventory_page.wait_until_url_is(inventory_page.build_url())

    assert inventory_page.get_inventory_container().is_displayed()
    assert inventory_page.get_product_list().is_displayed()


@pytest.mark.selenium
def test_product_details_can_be_opened_from_product_name_for_example_product(
    selenium_logged_in_inventory_page: SeleniumInventoryPage,
    selenium_product: dict,
) -> None:
    product_details_page = selenium_logged_in_inventory_page.open_product_details_by_name(
        selenium_product["product_name"]
    )

    product_details_page.wait_until_url_is(
        product_details_page.build_url(selenium_product["product_id"])
    )

    product_item = product_details_page.wait_until_loaded()

    assert product_details_page.get_product_name_from_item(product_item).text == (
        selenium_product["product_name"]
    )
    assert product_details_page.get_product_description_from_item(product_item).text == (
        selenium_product["product_description"]
    )
    assert product_details_page.get_product_price_from_item(product_item).text == (
        selenium_product["product_price"]
    )

    product_image = product_details_page.get_product_image_from_item(product_item)
    assert product_image.is_displayed()
    assert product_image.get_dom_attribute("src") == selenium_product["product_image"]

    assert product_details_page.get_add_to_cart_button_from_item(product_item).is_displayed()
    assert product_details_page.get_back_to_products_button().is_displayed()


@pytest.mark.selenium
def test_product_details_content_is_displayed_for_selected_product(
    selenium_product_details_page: tuple[SeleniumProductDetailsPage, dict],
) -> None:
    product_details_page, product = selenium_product_details_page

    product_details_page.wait_until_url_is(product_details_page.build_url(product["product_id"]))

    product_item = product_details_page.wait_until_loaded()
    assert product_item.is_displayed()

    product_name = product_details_page.get_product_name_from_item(product_item)
    assert product_name.is_displayed()
    assert product_name.text == product["product_name"]

    product_description = product_details_page.get_product_description_from_item(product_item)
    assert product_description.is_displayed()
    assert product_description.text == product["product_description"]

    product_price = product_details_page.get_product_price_from_item(product_item)
    assert product_price.is_displayed()
    assert product_price.text == product["product_price"]

    product_image = product_details_page.get_product_image_from_item(product_item)
    assert product_image.is_displayed()
    assert product_image.get_dom_attribute("src") == product["product_image"]

    add_to_cart_button = product_details_page.get_add_to_cart_button_from_item(product_item)
    assert add_to_cart_button.is_displayed()

    assert product_details_page.get_back_to_products_button().is_displayed()


@pytest.mark.selenium
def test_product_can_be_added_to_cart_from_product_details_page(
    selenium_product_details_page: tuple[SeleniumProductDetailsPage, dict],
) -> None:
    product_details_page, product = selenium_product_details_page

    product_details_page.add_product_to_cart()

    product_details_page.wait_until_url_is(product_details_page.build_url(product["product_id"]))

    assert product_details_page.get_shopping_cart_badge().text == "1"

    cart_page = product_details_page.open_cart()

    assert cart_page.get_product_item_by_name(product["product_name"]).is_displayed()


@pytest.mark.selenium
def test_cart_page_can_be_opened_from_product_details_page(
    selenium_product_details_page: tuple[SeleniumProductDetailsPage, dict],
) -> None:
    product_details_page, _ = selenium_product_details_page

    cart_page = product_details_page.open_cart()

    cart_page.wait_until_url_is(cart_page.build_url())

    assert cart_page.get_cart_contents_container().is_displayed()


@pytest.mark.selenium
def test_added_product_is_displayed_with_correct_content_on_cart_page(
    selenium_cart_page_with_one_product: tuple[SeleniumCartPage, dict],
) -> None:
    cart_page, product = selenium_cart_page_with_one_product

    product_item = cart_page.get_product_item_by_name(product["product_name"])

    assert product_item.is_displayed()

    product_name = cart_page.get_product_name_from_item(product_item)
    assert product_name.is_displayed()
    assert product_name.text == product["product_name"]

    product_description = cart_page.get_product_description_from_item(product_item)
    assert product_description.is_displayed()
    assert product_description.text == product["product_description"]

    product_price = cart_page.get_product_price_from_item(product_item)
    assert product_price.is_displayed()
    assert product_price.text == product["product_price"]

    product_quantity = cart_page.get_product_quantity_from_item(product_item)
    assert product_quantity.is_displayed()
    assert product_quantity.text == "1"

    remove_button = cart_page.get_remove_button_from_item(product_item)
    assert remove_button.is_displayed()


@pytest.mark.selenium
def test_checkout_button_opens_checkout_information_page_with_product_in_cart(
    selenium_cart_page_with_one_product: tuple[SeleniumCartPage, dict],
) -> None:
    cart_page, _ = selenium_cart_page_with_one_product

    checkout_step_one = cart_page.checkout()

    checkout_step_one.wait_until_url_is(checkout_step_one.build_url())

    assert checkout_step_one.get_checkout_info_block().is_displayed()

    assert checkout_step_one.wait.until(
        ec.invisibility_of_element_located(cart_page.CART_CONTENTS_CONTAINER)
    )


@pytest.mark.selenium
def test_checkout_information_form_continues_to_overview_when_valid_data_is_provided(
    selenium_checkout_step_two_page_with_one_product: tuple[SeleniumCheckoutOverviewPage, dict],
) -> None:
    checkout_step_two, product = selenium_checkout_step_two_page_with_one_product

    checkout_step_two.wait_until_url_is(checkout_step_two.build_url())

    assert checkout_step_two.get_checkout_summary_container().is_displayed()

    assert checkout_step_two.get_product_item_by_name(product["product_name"]).is_displayed()

    assert checkout_step_two.get_finish_button().is_displayed()
    assert checkout_step_two.get_cancel_button().is_displayed()


@pytest.mark.selenium
def test_checkout_overview_displays_selected_product(
    selenium_checkout_step_two_page_with_one_product: tuple[SeleniumCheckoutOverviewPage, dict],
) -> None:
    checkout_page_two, product = selenium_checkout_step_two_page_with_one_product

    assert checkout_page_two.get_checkout_summary_container().is_displayed()

    product_item = checkout_page_two.get_product_item_by_name(product["product_name"])

    assert checkout_page_two.get_product_name_from_item(product_item).is_displayed()
    assert checkout_page_two.get_product_description_from_item(product_item).is_displayed()
    assert checkout_page_two.get_product_price_from_item(product_item).is_displayed()

    product_quantity = checkout_page_two.get_product_quantity_from_item(product_item)

    assert product_quantity.is_displayed()
    assert product_quantity.text == "1"


@pytest.mark.selenium
def test_checkout_overview_price_summary_is_correct_for_one_product(
    selenium_checkout_step_two_page_with_one_product: tuple[SeleniumCheckoutOverviewPage, dict],
) -> None:
    checkout_step_two, product = selenium_checkout_step_two_page_with_one_product

    assert checkout_step_two.get_payment_info_label().is_displayed()
    assert checkout_step_two.get_payment_info_value().text == CHECKOUT_OVERVIEW_PAYMENT_INFO

    assert checkout_step_two.get_shipping_info_label().is_displayed()
    assert checkout_step_two.get_shipping_info_value().text == CHECKOUT_OVERVIEW_SHIPPING_INFO

    assert checkout_step_two.get_total_info_label().is_displayed()

    item_total_price = format(
        float(product["product_price"].replace("$", "")),
        ".2f",
    )

    tax_price = format(
        float(item_total_price) * TAX_PERCENTAGE / 100,
        ".2f",
    )

    final_total_price = format(
        float(item_total_price) + float(tax_price),
        ".2f",
    )

    assert (
        checkout_step_two.get_price_item_total_label().text == ITEM_TOTAL_PREFIX + item_total_price
    )
    assert checkout_step_two.get_price_tax_label().text == TAX_PREFIX + tax_price
    assert checkout_step_two.get_total_price_label().text == TOTAL_PREFIX + final_total_price


@pytest.mark.selenium
def test_finish_button_completes_checkout_and_opens_order_confirmation_page(
    selenium_checkout_step_two_page_with_one_product: tuple[SeleniumCheckoutOverviewPage, dict],
) -> None:
    checkout_step_two, _ = selenium_checkout_step_two_page_with_one_product

    checkout_last_step = checkout_step_two.finish_checkout()

    checkout_last_step.wait_until_url_is(checkout_last_step.build_url())

    assert checkout_last_step.get_checkout_complete_container().is_displayed()
    assert checkout_last_step.get_checkout_complete_header().is_displayed()
    assert checkout_last_step.get_checkout_complete_text().is_displayed()
    assert checkout_last_step.get_back_home_button().is_displayed()


@pytest.mark.selenium
def test_checkout_complete_page_elements_are_visible(
    selenium_checkout_last_step_page_with_one_product: tuple[SeleniumCheckoutCompletePage, dict],
) -> None:
    checkout_last_step_page, _ = selenium_checkout_last_step_page_with_one_product

    assert checkout_last_step_page.get_checkout_complete_container().is_displayed()
    assert checkout_last_step_page.get_checkout_complete_header().is_displayed()
    assert checkout_last_step_page.get_checkout_complete_text().is_displayed()
    assert checkout_last_step_page.get_back_home_button().is_displayed()


@pytest.mark.selenium
def test_back_home_returns_to_inventory_page_after_order_completion(
    selenium_checkout_last_step_page_with_one_product: tuple[SeleniumCheckoutCompletePage, dict],
) -> None:
    checkout_last_step_page, product = selenium_checkout_last_step_page_with_one_product

    inventory_page = checkout_last_step_page.back_home()

    inventory_page.wait_until_url_is(inventory_page.build_url())

    assert inventory_page.wait.until(
        ec.invisibility_of_element_located(checkout_last_step_page.CHECKOUT_COMPLETE_CONTAINER)
    )

    assert inventory_page.get_inventory_container().is_displayed()
    assert inventory_page.get_product_list().is_displayed()

    product_item = inventory_page.get_product_item_by_name(product["product_name"])

    assert product_item.is_displayed()
    assert inventory_page.get_product_name_from_item(product_item).text == (product["product_name"])
    assert inventory_page.get_product_description_from_item(product_item).text == (
        product["product_description"]
    )
    assert inventory_page.get_product_price_from_item(product_item).text == (
        product["product_price"]
    )

    product_image = inventory_page.get_product_image_from_item(product_item)
    assert product_image.is_displayed()
    assert product_image.get_dom_attribute("src") == product["product_image"]

    assert inventory_page.get_add_to_cart_button_from_item(product_item).is_displayed()

    assert inventory_page.wait.until(
        ec.invisibility_of_element_located(inventory_page.SHOPPING_CART_BADGE)
    )
