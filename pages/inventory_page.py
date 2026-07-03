from __future__ import annotations

from typing import TYPE_CHECKING

from playwright.sync_api import Locator

from pages.app_page import AppPage

if TYPE_CHECKING:
    from pages.product_details_page import ProductDetailsPage


class InventoryPage(AppPage):
    URL = "https://www.saucedemo.com/inventory.html"

    SORT_NAME_ASC = "az"
    SORT_NAME_DESC = "za"
    SORT_PRICE_LOW_HIGH = "lohi"
    SORT_PRICE_HIGH_LOW = "hilo"

    def get_inventory_container(self) -> Locator:
        return self.page.locator('[data-test="inventory-container"]')

    def get_product_list(self) -> Locator:
        return self.page.locator('[data-test="inventory-list"]')

    def get_product_item_by_name(self, product_name: str) -> Locator:
        return self.get_product_item_or_items().filter(has_text=product_name)

    def get_product_names(self) -> list[str]:
        return self.page.locator('[data-test="inventory-item-name"]').all_inner_texts()

    def get_product_prices(self) -> list[str]:
        return self.page.locator('[data-test="inventory-item-price"]').all_inner_texts()

    def get_product_sorting_dropdown(self) -> Locator:
        return self.page.locator('[data-test="product-sort-container"]')

    def sort_products_by(self, sort_option_value: str) -> None:
        self.get_product_sorting_dropdown().select_option(sort_option_value)

    def open_product_details_by_name(self, product_name: str) -> ProductDetailsPage:
        from pages.product_details_page import ProductDetailsPage

        product_item = self.get_product_item_by_name(product_name)
        self.get_product_name_from_item(product_item).click()
        return ProductDetailsPage(self.page)

    def open_product_details_by_image(self, product_name: str) -> ProductDetailsPage:
        from pages.product_details_page import ProductDetailsPage

        product_item = self.get_product_item_by_name(product_name)
        self.get_product_image_from_item(product_item).click()
        return ProductDetailsPage(self.page)

    def add_product_to_cart(self, product_name: str) -> None:
        product_item = self.get_product_item_by_name(product_name)
        self.get_add_to_cart_button_from_item(product_item).click()

    def remove_product_from_cart(self, product_name: str) -> None:
        product_item = self.get_product_item_by_name(product_name)
        self.get_remove_button_from_item(product_item).click()
