from __future__ import annotations

from typing import TYPE_CHECKING

from playwright.sync_api import Locator

from pages.app_page import AppPage

if TYPE_CHECKING:
    from pages.inventory_page import InventoryPage


class ProductDetailsPage(AppPage):
    URL = "https://www.saucedemo.com/inventory-item.html?id="

    def add_product_to_cart(self) -> None:
        self.get_add_to_cart_button_from_item(self.get_product_item_or_items()).click()

    def remove_product_from_cart(self) -> None:
        self.get_remove_button_from_item(self.get_product_item_or_items()).click()

    def get_back_to_products_button(self) -> Locator:
        return self.page.locator('[data-test="back-to-products"]')

    def return_to_inventory(self) -> InventoryPage:
        from pages.inventory_page import InventoryPage

        self.get_back_to_products_button().click()
        return InventoryPage(self.page)
