from playwright.sync_api import Locator, Page


class CartPage:

    URL = "https://www.saucedemo.com/cart.html"

    def __init__(self, page: Page):
        self.page = page

    def open(self) -> None:
        self.page.goto(self.URL)

    def get_cart_contents_container(self) -> Locator:
        return self.page.locator("[data-test='cart-contents-container']")

    def get_cart_list(self) -> Locator:
        return self.page.locator("[data-test='cart-list']")

    def get_cart_items(self) -> Locator:
        return self.page.locator("[data-test='inventory-item']")

    def get_product_card_by_name(self, product_name: str) -> Locator:
        return self.get_cart_items().filter(has_text=product_name)

    @staticmethod
    def get_product_name_from_card_in_cart(product_card: Locator) -> Locator:
        return product_card.locator('[data-test="inventory-item-name"]')

    @staticmethod
    def get_product_description_from_card_in_cart(product_card: Locator) -> Locator:
        return product_card.locator('[data-test="inventory-item-desc"]')

    @staticmethod
    def get_product_price_from_card_in_cart(product_card: Locator) -> Locator:
        return product_card.locator('[data-test="inventory-item-price"]')

    @staticmethod
    def get_product_quantity_from_card_in_cart(product_card: Locator) -> int:
        return int(product_card.locator('[data-test="item-quantity"]').inner_text())

    @staticmethod
    def get_remove_from_cart_button_from_card_in_cart(product_card: Locator) -> Locator:
        return product_card.get_by_role("button", name="Remove")

    def remove_item_from_cart(self, product_name: str) -> None:
        product_card = self.get_product_card_by_name(product_name)
        self.get_remove_from_cart_button_from_card_in_cart(product_card).click()

    def open_product_details_by_name(self, product_name: str) -> None:
        product_card = self.get_product_card_by_name(product_name)
        self.get_product_name_from_card_in_cart(product_card).click()

    def get_continue_shopping_button(self) -> Locator:
        return self.page.locator("[data-test='continue-shopping']")

    def continue_shopping(self) -> None:
        self.get_continue_shopping_button().click()

    def get_checkout_button(self) -> Locator:
        return self.page.locator("[data-test='checkout']")

    def checkout(self) -> None:
        self.get_checkout_button().click()

    def get_shopping_cart_link(self) -> Locator:
        return self.page.locator('[data-test="shopping-cart-link"]')

    def get_shopping_cart_badge(self) -> Locator:
        return self.page.locator('[data-test="shopping-cart-badge"]')

    def get_cart_badge_count(self) -> int:
        return int(self.get_shopping_cart_badge().inner_text())
