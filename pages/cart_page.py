from __future__ import annotations

from typing import TYPE_CHECKING

from playwright.sync_api import Locator

from pages.app_page import AppPage

if TYPE_CHECKING:
    from pages.inventory_page import InventoryPage
    from pages.product_details_page import ProductDetailsPage


class CartPage(AppPage):
    URL = "https://www.saucedemo.com/cart.html"

    def get_cart_contents_container(self) -> Locator:
        return self.page.locator("[data-test='cart-contents-container']")

    def get_cart_list(self) -> Locator:
        return self.page.locator("[data-test='cart-list']")

    def get_product_item_or_items(self) -> Locator:
        return self.page.locator("[data-test='inventory-item']")

    def get_product_item_by_name(self, product_name: str) -> Locator:
        return self.get_product_item_or_items().filter(has_text=product_name)

    @staticmethod
    def get_product_quantity_from_item(product_item: Locator) -> Locator:
        return product_item.locator('[data-test="item-quantity"]')

    def remove_product_from_cart(self, product_name: str) -> None:
        product_item = self.get_product_item_by_name(product_name)
        self.get_remove_button_from_item(product_item).click()

    def open_product_details_by_name(self, product_name: str) -> ProductDetailsPage:
        from pages.product_details_page import ProductDetailsPage

        product_item = self.get_product_item_by_name(product_name)
        self.get_product_name_from_item(product_item).click()
        return ProductDetailsPage(self.page)

    def get_continue_shopping_button(self) -> Locator:
        return self.page.locator("[data-test='continue-shopping']")

    def continue_shopping(self) -> InventoryPage:
        from pages.inventory_page import InventoryPage

        self.get_continue_shopping_button().click()
        return InventoryPage(self.page)

    def get_checkout_button(self) -> Locator:
        return self.page.locator("[data-test='checkout']")

    def checkout(self) -> None:
        self.get_checkout_button().click()
