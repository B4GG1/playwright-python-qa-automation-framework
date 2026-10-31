from __future__ import annotations

from typing import TYPE_CHECKING

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from selenium_pages.base_page import SeleniumBasePage

if TYPE_CHECKING:
    from selenium_pages.checkout_page import SeleniumCheckoutInformationPage


class SeleniumCartPage(SeleniumBasePage):
    ROUTE = "/cart.html"

    CART_CONTENTS_CONTAINER = (
        By.CSS_SELECTOR,
        '[data-test="cart-contents-container"]',
    )
    PRODUCT_ITEMS = (By.CSS_SELECTOR, '[data-test="inventory-item"]')
    PRODUCT_NAME = (By.CSS_SELECTOR, '[data-test="inventory-item-name"]')
    PRODUCT_DESCRIPTION = (By.CSS_SELECTOR, '[data-test="inventory-item-desc"]')
    PRODUCT_PRICE = (By.CSS_SELECTOR, '[data-test="inventory-item-price"]')
    PRODUCT_QUANTITY = (By.CSS_SELECTOR, '[data-test="item-quantity"]')
    CHECKOUT_BUTTON = (By.CSS_SELECTOR, '[data-test="checkout"]')

    def wait_until_loaded(self) -> WebElement:
        return self.wait_until_visible(self.CART_CONTENTS_CONTAINER)

    def get_product_item_by_name(self, product_name: str) -> WebElement:
        self.wait_until_visible(self.PRODUCT_ITEMS)

        for product_item in self.driver.find_elements(*self.PRODUCT_ITEMS):
            product_name_element = product_item.find_element(*self.PRODUCT_NAME)

            if product_name_element.text == product_name:
                return product_item

        raise AssertionError(f"Product not found in Cart: {product_name}")

    def get_product_name(self, product_item: WebElement) -> str:
        return product_item.find_element(*self.PRODUCT_NAME).text

    def get_product_description(self, product_item: WebElement) -> str:
        return product_item.find_element(*self.PRODUCT_DESCRIPTION).text

    def get_product_price(self, product_item: WebElement) -> str:
        return product_item.find_element(*self.PRODUCT_PRICE).text

    def get_product_quantity(self, product_item: WebElement) -> str:
        return product_item.find_element(*self.PRODUCT_QUANTITY).text

    def checkout(self) -> SeleniumCheckoutInformationPage:
        from selenium_pages.checkout_page import SeleniumCheckoutInformationPage

        self.wait_until_clickable(self.CHECKOUT_BUTTON).click()

        checkout_page = SeleniumCheckoutInformationPage(self.driver)
        checkout_page.wait_until_loaded()

        return checkout_page
