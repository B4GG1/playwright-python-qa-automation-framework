from __future__ import annotations

from typing import TYPE_CHECKING

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec

from selenium_pages.app_page import SeleniumAppPage

if TYPE_CHECKING:
    from selenium_pages.cart_page import SeleniumCartPage
    from selenium_pages.inventory_page import SeleniumInventoryPage
    from selenium_pages.product_details_page import SeleniumProductDetailsPage


class SeleniumCheckoutCompletePage(SeleniumAppPage):
    ROUTE = "/checkout-complete.html"

    CHECKOUT_COMPLETE_CONTAINER = (
        By.CSS_SELECTOR,
        '[data-test="checkout-complete-container"]',
    )
    PONY_EXPRESS_IMG = (By.CSS_SELECTOR, '[data-test="pony-express"]')
    COMPLETE_HEADER = (By.CSS_SELECTOR, '[data-test="complete-header"]')
    COMPLETE_MESSAGE = (By.CSS_SELECTOR, '[data-test="complete-text"]')
    BACK_HOME_BUTTON = (By.CSS_SELECTOR, '[data-test="back-to-products"]')

    def get_checkout_complete_container(self) -> WebElement:
        return self.wait_until_visible(self.CHECKOUT_COMPLETE_CONTAINER)

    def wait_until_loaded(self) -> WebElement:
        return self.get_checkout_complete_container()

    def get_pony_express_img(self) -> WebElement:
        return self.wait_until_visible(self.PONY_EXPRESS_IMG)

    def get_checkout_complete_header(self) -> WebElement:
        return self.wait_until_visible(self.COMPLETE_HEADER)

    def get_checkout_complete_text(self) -> WebElement:
        return self.wait_until_visible(self.COMPLETE_MESSAGE)

    def get_back_home_button(self) -> WebElement:
        return self.wait_until_clickable(self.BACK_HOME_BUTTON)

    def back_home(self) -> SeleniumInventoryPage:
        from selenium_pages.inventory_page import SeleniumInventoryPage

        inventory_page = SeleniumInventoryPage(self.driver)
        self.click_and_confirm_url(
            self.BACK_HOME_BUTTON,
            inventory_page.build_url(),
            action="Back Home",
        )
        inventory_page.wait_until_loaded()
        return inventory_page

    # Compatibility with existing Selenium E2E assertions.
    def get_complete_header(self) -> str:
        return self.get_checkout_complete_header().text

    def get_complete_message(self) -> str:
        return self.get_checkout_complete_text().text


class SeleniumCheckoutOverviewPage(SeleniumAppPage):
    ROUTE = "/checkout-step-two.html"

    CART_LIST = (By.CSS_SELECTOR, '[data-test="cart-list"]')
    CHECKOUT_SUMMARY_CONTAINER = (
        By.CSS_SELECTOR,
        '[data-test="checkout-summary-container"]',
    )
    PAYMENT_INFO_LABEL = (By.CSS_SELECTOR, '[data-test="payment-info-label"]')
    PAYMENT_INFO_VALUE = (By.CSS_SELECTOR, '[data-test="payment-info-value"]')
    SHIPPING_INFO_LABEL = (By.CSS_SELECTOR, '[data-test="shipping-info-label"]')
    SHIPPING_INFO_VALUE = (By.CSS_SELECTOR, '[data-test="shipping-info-value"]')
    TOTAL_INFO_LABEL = (By.CSS_SELECTOR, '[data-test="total-info-label"]')
    ITEM_TOTAL = (By.CSS_SELECTOR, '[data-test="subtotal-label"]')
    TAX = (By.CSS_SELECTOR, '[data-test="tax-label"]')
    TOTAL = (By.CSS_SELECTOR, '[data-test="total-label"]')
    CANCEL_BUTTON = (By.CSS_SELECTOR, '[data-test="cancel"]')
    FINISH_BUTTON = (By.CSS_SELECTOR, '[data-test="finish"]')

    def get_cart_list(self) -> WebElement:
        return self.wait_until_visible(self.CART_LIST)

    def get_product_item_by_name(self, product_name: str) -> WebElement:
        def find_product(_driver: object) -> WebElement | bool:
            for item in self.get_product_item_or_items():
                if self.get_product_name_from_item(item).text == product_name:
                    return item
            return False

        try:
            return self.wait.until(find_product)
        except TimeoutException as exc:
            raise AssertionError(f"Product not found on Checkout Overview: {product_name}") from exc

    def get_checkout_summary_container(self) -> WebElement:
        return self.wait_until_visible(self.CHECKOUT_SUMMARY_CONTAINER)

    def wait_until_loaded(self) -> WebElement:
        return self.get_checkout_summary_container()

    def get_payment_info_label(self) -> WebElement:
        return self.wait_until_visible(self.PAYMENT_INFO_LABEL)

    def get_payment_info_value(self) -> WebElement:
        return self.wait_until_visible(self.PAYMENT_INFO_VALUE)

    def get_shipping_info_label(self) -> WebElement:
        return self.wait_until_visible(self.SHIPPING_INFO_LABEL)

    def get_shipping_info_value(self) -> WebElement:
        return self.wait_until_visible(self.SHIPPING_INFO_VALUE)

    def get_total_info_label(self) -> WebElement:
        return self.wait_until_visible(self.TOTAL_INFO_LABEL)

    def get_price_item_total_label(self) -> WebElement:
        return self.wait_until_visible(self.ITEM_TOTAL)

    def get_price_tax_label(self) -> WebElement:
        return self.wait_until_visible(self.TAX)

    def get_total_price_label(self) -> WebElement:
        return self.wait_until_visible(self.TOTAL)

    def get_cancel_button(self) -> WebElement:
        return self.wait_until_clickable(self.CANCEL_BUTTON)

    def get_finish_button(self) -> WebElement:
        return self.wait_until_clickable(self.FINISH_BUTTON)

    def cancel_checkout(self) -> SeleniumInventoryPage:
        from selenium_pages.inventory_page import SeleniumInventoryPage

        inventory_page = SeleniumInventoryPage(self.driver)
        self.click_and_confirm_url(
            self.CANCEL_BUTTON,
            inventory_page.build_url(),
            action="Cancel Checkout from Overview",
        )
        inventory_page.wait_until_loaded()
        return inventory_page

    def finish_checkout(self) -> SeleniumCheckoutCompletePage:
        complete_page = SeleniumCheckoutCompletePage(self.driver)
        self.click_and_confirm_url(
            self.FINISH_BUTTON,
            complete_page.build_url(),
            action="Finish Checkout",
        )
        complete_page.wait_until_loaded()
        return complete_page

    def open_product_details_by_name(self, product_name: str) -> SeleniumProductDetailsPage:
        from selenium_pages.product_details_page import SeleniumProductDetailsPage

        details_page = SeleniumProductDetailsPage(self.driver)
        self.click_and_confirm(
            lambda: self.get_product_name_from_item(self.get_product_item_by_name(product_name)),
            lambda driver: driver.current_url.startswith(details_page.build_url()),
            action=f"Open Product Details from Checkout: {product_name}",
        )
        details_page.wait_until_loaded()
        return details_page

    # Compatibility with existing Selenium E2E assertions.
    def get_product_name(self, product_item: WebElement) -> str:
        return self.get_product_name_from_item(product_item).text

    def get_product_description(self, product_item: WebElement) -> str:
        return self.get_product_description_from_item(product_item).text

    def get_product_price(self, product_item: WebElement) -> str:
        return self.get_product_price_from_item(product_item).text

    def get_product_quantity(self, product_item: WebElement) -> str:
        return self.get_product_quantity_from_item(product_item).text

    def get_payment_info(self) -> str:
        return self.get_payment_info_value().text

    def get_shipping_info(self) -> str:
        return self.get_shipping_info_value().text

    def get_item_total(self) -> str:
        return self.get_price_item_total_label().text

    def get_tax(self) -> str:
        return self.get_price_tax_label().text

    def get_total(self) -> str:
        return self.get_total_price_label().text


class SeleniumCheckoutInformationPage(SeleniumAppPage):
    ROUTE = "/checkout-step-one.html"

    FIRST_NAME_INPUT = (By.CSS_SELECTOR, '[data-test="firstName"]')
    TITLE = (By.CSS_SELECTOR, '[data-test="title"]')
    LAST_NAME_INPUT = (By.CSS_SELECTOR, '[data-test="lastName"]')
    POSTAL_CODE_INPUT = (By.CSS_SELECTOR, '[data-test="postalCode"]')
    CHECKOUT_INFO_CONTAINER = (By.CSS_SELECTOR, ".checkout_info")
    CANCEL_BUTTON = (By.CSS_SELECTOR, '[data-test="cancel"]')
    CONTINUE_BUTTON = (By.CSS_SELECTOR, '[data-test="continue"]')
    ERROR_MESSAGE = (By.CSS_SELECTOR, '[data-test="error"]')
    CLOSE_ERROR_MESSAGE_BUTTON = (By.CSS_SELECTOR, '[data-test="error-button"]')

    def get_first_name_input(self) -> WebElement:
        return self.wait_until_visible(self.FIRST_NAME_INPUT)

    def get_title(self) -> WebElement:
        return self.wait_until_visible(self.TITLE)

    def get_last_name_input(self) -> WebElement:
        return self.wait_until_visible(self.LAST_NAME_INPUT)

    def get_postal_code_input(self) -> WebElement:
        return self.wait_until_visible(self.POSTAL_CODE_INPUT)

    def get_checkout_info_block(self) -> WebElement:
        return self.wait_until_visible(self.CHECKOUT_INFO_CONTAINER)

    def wait_until_loaded(self) -> WebElement:
        return self.get_checkout_info_block()

    def get_cancel_button(self) -> WebElement:
        return self.wait_until_clickable(self.CANCEL_BUTTON)

    def get_continue_button(self) -> WebElement:
        return self.wait_until_clickable(self.CONTINUE_BUTTON)

    def get_input_error_icon(self, input_container: WebElement) -> WebElement:
        form_group = input_container.find_element(
            By.XPATH,
            "./ancestor::*[contains(concat(' ', normalize-space(@class), ' '), "
            "' form_group ')][1]",
        )
        return form_group.find_element(By.CSS_SELECTOR, "[data-icon='circle-xmark']")

    def get_error_message(self) -> WebElement:
        return self.wait_until_visible(self.ERROR_MESSAGE)

    def get_close_error_message_button(self) -> WebElement:
        return self.wait_until_clickable(self.CLOSE_ERROR_MESSAGE_BUTTON)

    def cancel_checkout(self) -> SeleniumCartPage:
        from selenium_pages.cart_page import SeleniumCartPage

        cart_page = SeleniumCartPage(self.driver)
        self.click_and_confirm_url(
            self.CANCEL_BUTTON,
            cart_page.build_url(),
            action="Cancel Checkout Information",
        )
        cart_page.wait_until_loaded()
        return cart_page

    def continue_checkout(self) -> SeleniumCheckoutOverviewPage:
        overview_page = SeleniumCheckoutOverviewPage(self.driver)
        self.get_continue_button().click()
        # A validation error is a legitimate outcome for invalid form inputs.
        # Unlike a success-only URL wait, this preserves Playwright test behavior.
        self.wait.until(
            ec.any_of(
                ec.url_to_be(overview_page.build_url()),
                ec.visibility_of_element_located(self.ERROR_MESSAGE),
            )
        )
        return overview_page

    def fill_checkout_info_form(self, first_name: str, last_name: str, postal_code: str) -> None:
        for locator, value in (
            (self.FIRST_NAME_INPUT, first_name),
            (self.LAST_NAME_INPUT, last_name),
            (self.POSTAL_CODE_INPUT, postal_code),
        ):
            field = self.wait_until_visible(locator)
            field.clear()
            field.send_keys(value)
            # Check the actual input value rather than silently accepting lost keys.
            self.wait.until(
                lambda driver: (driver.find_element(*locator).get_property("value") == value)
            )

    def close_error_message(self) -> None:
        self.get_close_error_message_button().click()

    # Compatibility with the existing Selenium E2E fixtures.
    def fill_checkout_info(self, first_name: str, last_name: str, postal_code: str) -> None:
        self.fill_checkout_info_form(first_name, last_name, postal_code)
