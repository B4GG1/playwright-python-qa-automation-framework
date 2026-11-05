from __future__ import annotations

from typing import TYPE_CHECKING

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec

from selenium_pages.app_page import SeleniumAppPage

if TYPE_CHECKING:
    from selenium_pages.inventory_page import SeleniumInventoryPage


class SeleniumProductDetailsPage(SeleniumAppPage):
    ROUTE = "/inventory-item.html?id="

    PRODUCT_ITEM = (By.CSS_SELECTOR, '[data-test="inventory-item"]')
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, 'button[data-test^="add-to-cart"]')
    REMOVE_BUTTON = (By.CSS_SELECTOR, 'button[data-test^="remove"]')
    BACK_TO_PRODUCTS_BUTTON = (By.CSS_SELECTOR, '[data-test="back-to-products"]')

    def wait_until_loaded(self) -> WebElement:
        return self.wait_until_visible(self.PRODUCT_ITEM)

    def add_product_to_cart(self) -> None:
        self.click_and_confirm(
            lambda: self.wait_until_clickable(self.ADD_TO_CART_BUTTON),
            ec.visibility_of_element_located(self.REMOVE_BUTTON),
            action="Add product to Cart",
        )

    def remove_product_from_cart(self) -> None:
        self.click_and_confirm(
            lambda: self.wait_until_clickable(self.REMOVE_BUTTON),
            ec.visibility_of_element_located(self.ADD_TO_CART_BUTTON),
            action="Remove product from Cart",
        )

    def get_back_to_products_button(self) -> WebElement:
        return self.wait_until_clickable(self.BACK_TO_PRODUCTS_BUTTON)

    def return_to_inventory(self) -> SeleniumInventoryPage:
        from selenium_pages.inventory_page import SeleniumInventoryPage

        inventory_page = SeleniumInventoryPage(self.driver)
        self.click_and_confirm_url(
            self.BACK_TO_PRODUCTS_BUTTON,
            inventory_page.build_url(),
            action="Return to Inventory",
        )
        inventory_page.wait_until_loaded()
        return inventory_page

    def get_product_name(self) -> str:
        return self.get_product_name_from_item(self.wait_until_loaded()).text

    def get_product_description(self) -> str:
        return self.get_product_description_from_item(self.wait_until_loaded()).text

    def get_product_price(self) -> str:
        return self.get_product_price_from_item(self.wait_until_loaded()).text
