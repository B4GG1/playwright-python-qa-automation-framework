from __future__ import annotations

from typing import TYPE_CHECKING

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from selenium_pages.base_page import SeleniumBasePage

if TYPE_CHECKING:
    from selenium_pages.product_details_page import SeleniumProductDetailsPage


class SeleniumInventoryPage(SeleniumBasePage):
    ROUTE = "/inventory.html"

    INVENTORY_CONTAINER = (By.CSS_SELECTOR, '[data-test="inventory-container"]')
    PRODUCT_ITEMS = (By.CSS_SELECTOR, '[data-test="inventory-item"]')
    PRODUCT_NAME = (By.CSS_SELECTOR, '[data-test="inventory-item-name"]')

    def wait_until_loaded(self) -> WebElement:
        return self.wait_until_visible(self.INVENTORY_CONTAINER)

    def get_product_item_by_name(self, product_name: str) -> WebElement:
        self.wait_until_visible(self.PRODUCT_ITEMS)

        for product_item in self.driver.find_elements(*self.PRODUCT_ITEMS):
            product_name_element = product_item.find_element(*self.PRODUCT_NAME)

            if product_name_element.text == product_name:
                return product_item

        raise AssertionError(f"Product not found on Inventory page: {product_name}")

    def open_product_details_by_name(
        self,
        product_name: str,
    ) -> SeleniumProductDetailsPage:
        from selenium_pages.product_details_page import SeleniumProductDetailsPage

        product_item = self.get_product_item_by_name(product_name)
        product_name_element = product_item.find_element(*self.PRODUCT_NAME)
        product_name_element.click()

        product_details_page = SeleniumProductDetailsPage(self.driver)
        product_details_page.wait_until_loaded()

        return product_details_page

    def get_product_name(self, product_item: WebElement) -> str:
        return product_item.find_element(*self.PRODUCT_NAME).text

    def get_product_description(self, product_item: WebElement) -> str:
        return product_item.find_element(
            By.CSS_SELECTOR,
            '[data-test="inventory-item-desc"]',
        ).text

    def get_product_price(self, product_item: WebElement) -> str:
        return product_item.find_element(
            By.CSS_SELECTOR,
            '[data-test="inventory-item-price"]',
        ).text
