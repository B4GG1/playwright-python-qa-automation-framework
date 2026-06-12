from playwright.sync_api import Locator, Page


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

    def get_back_to_products_button(self) -> Locator:
        return self.page.locator('[data-test="back-to-products"]')

    def return_to_inventory(self) -> None:
        self.get_back_to_products_button().click()
