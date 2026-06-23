from playwright.sync_api import Locator, Page

from pages.cart_page import CartPage


class ProductDetailsPage:
    URL = "https://www.saucedemo.com/inventory-item.html?id="

    def __init__(self, page: Page):
        self.page = page

    def open_by_id(self, product_id: int) -> None:
        self.page.goto(f"{self.URL}{product_id}")

    def get_item_details_container(self) -> Locator:
        return self.page.locator('[data-test="inventory-container"]')

    def get_product_name(self) -> Locator:
        return self.page.locator('[data-test="inventory-item-name"]')

    def get_product_description(self) -> Locator:
        return self.page.locator('[data-test="inventory-item-desc"]')

    def get_product_price(self) -> Locator:
        return self.page.locator('[data-test="inventory-item-price"]')

    def get_product_image(self) -> Locator:
        return self.page.locator("img.inventory_details_img")

    def get_add_to_cart_button(self) -> Locator:
        return self.page.locator('[data-test="add-to-cart"]')

    def add_product_to_cart(self):
        self.get_add_to_cart_button().click()

    def get_remove_from_cart_button(self) -> Locator:
        return self.page.locator('[data-test="remove"]')

    def remove_from_cart(self):
        self.get_remove_from_cart_button().click()

    def get_back_to_products_button(self) -> Locator:
        return self.page.locator('[data-test="back-to-products"]')

    def return_to_inventory(self) -> None:
        self.get_back_to_products_button().click()

    def get_shopping_cart_link(self) -> Locator:
        return self.page.locator('[data-test="shopping-cart-link"]')

    def open_cart(self) -> CartPage:
        self.get_shopping_cart_link().click()
        return CartPage(self.page)

    def get_shopping_cart_badge(self) -> Locator:
        return self.page.locator('[data-test="shopping-cart-badge"]')

    def get_cart_badge_count(self) -> int:
        return int(self.get_shopping_cart_badge().inner_text())
