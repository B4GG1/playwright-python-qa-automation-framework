from playwright.sync_api import Locator, Page


class InventoryPage:
    URL = "https://www.saucedemo.com/inventory.html"

    SORT_NAME_ASC = "az"
    SORT_NAME_DESC = "za"
    SORT_PRICE_LOW_HIGH = "lohi"
    SORT_PRICE_HIGH_LOW = "hilo"

    def __init__(self, page: Page):
        self.page = page

    def open(self) -> None:
        self.page.goto(self.URL)

    def get_inventory_container(self) -> Locator:
        return self.page.locator('[data-test="inventory-container"]')

    def get_product_list(self) -> Locator:
        return self.page.locator('[data-test="inventory-list"]')

    def get_product_cards_locator(self) -> Locator:
        return self.page.locator('[data-test="inventory-item"]')

    def get_product_cards_list(self) -> list[Locator]:
        return self.page.locator('[data-test="inventory-item"]').all()

    def get_product_card_by_name(self, product_name: str) -> Locator:
        return self.get_product_cards_locator().filter(has_text=product_name)

    @staticmethod
    def get_product_name_from_card(product_card: Locator) -> Locator:
        return product_card.locator('[data-test="inventory-item-name"]')

    @staticmethod
    def get_product_description_from_card(product_card: Locator) -> Locator:
        return product_card.locator('[data-test="inventory-item-desc"]')

    @staticmethod
    def get_product_price_from_card(product_card: Locator) -> Locator:
        return product_card.locator('[data-test="inventory-item-price"]')

    @staticmethod
    def get_product_image_from_card(product_card: Locator) -> Locator:
        return product_card.locator("img")

    @staticmethod
    def get_add_to_cart_button_from_card(product_card: Locator) -> Locator:
        return product_card.get_by_role("button", name="Add to cart")

    def get_product_names(self) -> list[str]:
        return self.page.locator('[data-test="inventory-item-name"]').all_inner_texts()

    def get_product_prices(self) -> list[str]:
        return self.page.locator('[data-test="inventory-item-price"]').all_inner_texts()

    def get_product_sorting_dropdown(self) -> Locator:
        return self.page.locator('[data-test="product-sort-container"]')

    def sort_products_by(self, sort_option_value: str) -> None:
        self.get_product_sorting_dropdown().select_option(sort_option_value)

    def open_product_details_by_name(self, product_name: str) -> None:
        product_card = self.get_product_card_by_name(product_name)
        self.get_product_name_from_card(product_card).click()

    def open_product_details_by_image(self, product_name: str) -> None:
        product_card = self.get_product_card_by_name(product_name)
        self.get_product_image_from_card(product_card).click()

    def get_cart_link(self) -> Locator:
        return self.page.locator('[data-test="shopping-cart-link"]')

    def get_cart_badge(self) -> Locator:
        return self.page.locator('[data-test="shopping-cart-badge"]')
