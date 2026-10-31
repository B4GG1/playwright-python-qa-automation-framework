from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from selenium_pages.base_page import SeleniumBasePage


class SeleniumCheckoutInformationPage(SeleniumBasePage):
    ROUTE = "/checkout-step-one.html"

    CHECKOUT_INFO_CONTAINER = (By.CSS_SELECTOR, ".checkout_info")
    FIRST_NAME_INPUT = (By.CSS_SELECTOR, '[data-test="firstName"]')
    LAST_NAME_INPUT = (By.CSS_SELECTOR, '[data-test="lastName"]')
    POSTAL_CODE_INPUT = (By.CSS_SELECTOR, '[data-test="postalCode"]')
    CONTINUE_BUTTON = (By.CSS_SELECTOR, '[data-test="continue"]')

    def wait_until_loaded(self) -> WebElement:
        return self.wait_until_visible(self.CHECKOUT_INFO_CONTAINER)

    def fill_checkout_info(
        self,
        first_name: str,
        last_name: str,
        postal_code: str,
    ) -> None:
        self.wait_until_visible(self.FIRST_NAME_INPUT).send_keys(first_name)
        self.wait_until_visible(self.LAST_NAME_INPUT).send_keys(last_name)
        self.wait_until_visible(self.POSTAL_CODE_INPUT).send_keys(postal_code)

    def continue_checkout(self) -> SeleniumCheckoutOverviewPage:
        self.wait_until_clickable(self.CONTINUE_BUTTON).click()

        overview_page = SeleniumCheckoutOverviewPage(self.driver)
        overview_page.wait_until_loaded()

        return overview_page


class SeleniumCheckoutOverviewPage(SeleniumBasePage):
    ROUTE = "/checkout-step-two.html"

    CHECKOUT_SUMMARY_CONTAINER = (
        By.CSS_SELECTOR,
        '[data-test="checkout-summary-container"]',
    )
    PRODUCT_ITEMS = (By.CSS_SELECTOR, '[data-test="inventory-item"]')
    PRODUCT_NAME = (By.CSS_SELECTOR, '[data-test="inventory-item-name"]')
    PRODUCT_DESCRIPTION = (By.CSS_SELECTOR, '[data-test="inventory-item-desc"]')
    PRODUCT_PRICE = (By.CSS_SELECTOR, '[data-test="inventory-item-price"]')
    PRODUCT_QUANTITY = (By.CSS_SELECTOR, '[data-test="item-quantity"]')

    PAYMENT_INFO_VALUE = (By.CSS_SELECTOR, '[data-test="payment-info-value"]')
    SHIPPING_INFO_VALUE = (By.CSS_SELECTOR, '[data-test="shipping-info-value"]')
    ITEM_TOTAL = (By.CSS_SELECTOR, '[data-test="subtotal-label"]')
    TAX = (By.CSS_SELECTOR, '[data-test="tax-label"]')
    TOTAL = (By.CSS_SELECTOR, '[data-test="total-label"]')

    FINISH_BUTTON = (By.CSS_SELECTOR, '[data-test="finish"]')

    def wait_until_loaded(self) -> WebElement:
        return self.wait_until_visible(self.CHECKOUT_SUMMARY_CONTAINER)

    def get_product_item_by_name(self, product_name: str) -> WebElement:
        self.wait_until_visible(self.PRODUCT_ITEMS)

        for product_item in self.driver.find_elements(*self.PRODUCT_ITEMS):
            product_name_element = product_item.find_element(*self.PRODUCT_NAME)

            if product_name_element.text == product_name:
                return product_item

        raise AssertionError(f"Product not found on Checkout Overview: {product_name}")

    def get_product_name(self, product_item: WebElement) -> str:
        return product_item.find_element(*self.PRODUCT_NAME).text

    def get_product_description(self, product_item: WebElement) -> str:
        return product_item.find_element(*self.PRODUCT_DESCRIPTION).text

    def get_product_price(self, product_item: WebElement) -> str:
        return product_item.find_element(*self.PRODUCT_PRICE).text

    def get_product_quantity(self, product_item: WebElement) -> str:
        return product_item.find_element(*self.PRODUCT_QUANTITY).text

    def get_payment_info(self) -> str:
        return self.wait_until_visible(self.PAYMENT_INFO_VALUE).text

    def get_shipping_info(self) -> str:
        return self.wait_until_visible(self.SHIPPING_INFO_VALUE).text

    def get_item_total(self) -> str:
        return self.wait_until_visible(self.ITEM_TOTAL).text

    def get_tax(self) -> str:
        return self.wait_until_visible(self.TAX).text

    def get_total(self) -> str:
        return self.wait_until_visible(self.TOTAL).text

    def finish_checkout(self) -> SeleniumCheckoutCompletePage:
        self.wait_until_clickable(self.FINISH_BUTTON).click()

        complete_page = SeleniumCheckoutCompletePage(self.driver)
        complete_page.wait_until_loaded()

        return complete_page


class SeleniumCheckoutCompletePage(SeleniumBasePage):
    ROUTE = "/checkout-complete.html"

    CHECKOUT_COMPLETE_CONTAINER = (
        By.CSS_SELECTOR,
        '[data-test="checkout-complete-container"]',
    )
    COMPLETE_HEADER = (By.CSS_SELECTOR, '[data-test="complete-header"]')
    COMPLETE_MESSAGE = (By.CSS_SELECTOR, '[data-test="complete-text"]')
    BACK_HOME_BUTTON = (By.CSS_SELECTOR, '[data-test="back-to-products"]')

    def wait_until_loaded(self) -> WebElement:
        return self.wait_until_visible(self.CHECKOUT_COMPLETE_CONTAINER)

    def get_complete_header(self) -> str:
        return self.wait_until_visible(self.COMPLETE_HEADER).text

    def get_complete_message(self) -> str:
        return self.wait_until_visible(self.COMPLETE_MESSAGE).text

    def back_home(self):
        from selenium_pages.inventory_page import SeleniumInventoryPage

        self.wait_until_clickable(self.BACK_HOME_BUTTON).click()

        inventory_page = SeleniumInventoryPage(self.driver)
        inventory_page.wait_until_loaded()

        return inventory_page
