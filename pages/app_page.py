from __future__ import annotations

from typing import TYPE_CHECKING

from playwright.sync_api import Locator

from pages.base_page import BasePage

if TYPE_CHECKING:
    from pages.cart_page import CartPage
    from pages.inventory_page import InventoryPage
    from pages.login_page import LoginPage


class AppPage(BasePage):
    # Shared authenticated header and sidebar actions
    def get_shopping_cart_link(self) -> Locator:
        return self.page.locator('[data-test="shopping-cart-link"]')

    def open_cart(self) -> CartPage:
        from pages.cart_page import CartPage

        self.get_shopping_cart_link().click()
        return CartPage(self.page)

    def get_shopping_cart_badge(self) -> Locator:
        return self.page.locator('[data-test="shopping-cart-badge"]')

    def get_burger_menu_button(self) -> Locator:
        return self.page.get_by_role("button", name="Open Menu")

    def get_close_menu_button(self) -> Locator:
        return self.page.get_by_role("button", name="Close Menu")

    def get_logout_sidebar_link(self) -> Locator:
        return self.page.locator('[data-test="logout-sidebar-link"]')

    def get_all_items_sidebar_link(self) -> Locator:
        return self.page.locator('[data-test="inventory-sidebar-link"]')

    def get_reset_app_state_sidebar_link(self) -> Locator:
        return self.page.locator('[data-test="reset-sidebar-link"]')

    def get_about_sidebar_link(self) -> Locator:
        return self.page.locator('[data-test="about-sidebar-link"]')

    def open_menu(self) -> None:
        self.get_burger_menu_button().click()

    def close_menu(self) -> None:
        self.get_close_menu_button().click()

    def logout(self) -> LoginPage:
        from pages.login_page import LoginPage

        self.open_menu()
        self.get_logout_sidebar_link().click()
        return LoginPage(self.page)

    def reset_app_state(self) -> None:
        self.open_menu()
        self.get_reset_app_state_sidebar_link().click()

    def open_about_page(self) -> None:
        self.open_menu()
        self.get_about_sidebar_link().click()

    def back_to_all_items(self) -> InventoryPage:
        from pages.inventory_page import InventoryPage

        self.open_menu()
        self.get_all_items_sidebar_link().click()

        return InventoryPage(self.page)

    # Shared locators for product-like item containers
    def get_product_item_or_items(self) -> Locator:
        return self.page.locator('[data-test="inventory-item"]')

    @staticmethod
    def get_product_name_from_item(product_item: Locator) -> Locator:
        return product_item.locator('[data-test="inventory-item-name"]')

    @staticmethod
    def get_product_description_from_item(product_item: Locator) -> Locator:
        return product_item.locator('[data-test="inventory-item-desc"]')

    @staticmethod
    def get_product_price_from_item(product_item: Locator) -> Locator:
        return product_item.locator('[data-test="inventory-item-price"]')

    @staticmethod
    def get_product_image_from_item(product_item: Locator) -> Locator:
        return product_item.locator("img.inventory_item_img, img.inventory_details_img")

    @staticmethod
    def get_add_to_cart_button_from_item(product_item: Locator) -> Locator:
        return product_item.get_by_role("button", name="Add to cart")

    @staticmethod
    def get_product_quantity_from_item(product_item: Locator) -> Locator:
        return product_item.locator('[data-test="item-quantity"]')

    @staticmethod
    def get_remove_button_from_item(product_item: Locator) -> Locator:
        return product_item.get_by_role("button", name="Remove")
