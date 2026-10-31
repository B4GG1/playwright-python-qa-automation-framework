from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from selenium_pages.base_page import SeleniumBasePage


class SeleniumProductDetailsPage(SeleniumBasePage):
    ROUTE = "/inventory-item.html?id="

    PRODUCT_ITEM = (By.CSS_SELECTOR, '[data-test="inventory-item"]')
    PRODUCT_NAME = (By.CSS_SELECTOR, '[data-test="inventory-item-name"]')
    PRODUCT_DESCRIPTION = (By.CSS_SELECTOR, '[data-test="inventory-item-desc"]')
    PRODUCT_PRICE = (By.CSS_SELECTOR, '[data-test="inventory-item-price"]')
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, '[data-test^="add-to-cart"]')
    SHOPPING_CART_LINK = (By.CSS_SELECTOR, '[data-test="shopping-cart-link"]')

    def wait_until_loaded(self) -> WebElement:
        return self.wait_until_visible(self.PRODUCT_ITEM)

    def get_product_name(self) -> str:
        return self.wait_until_visible(self.PRODUCT_NAME).text

    def get_product_description(self) -> str:
        return self.wait_until_visible(self.PRODUCT_DESCRIPTION).text

    def get_product_price(self) -> str:
        return self.wait_until_visible(self.PRODUCT_PRICE).text

    def add_product_to_cart(self) -> None:
        self.wait_until_clickable(self.ADD_TO_CART_BUTTON).click()

    def open_cart(self):
        from selenium_pages.cart_page import SeleniumCartPage

        self.wait_until_clickable(self.SHOPPING_CART_LINK).click()

        cart_page = SeleniumCartPage(self.driver)
        cart_page.wait_until_url_is(cart_page.build_url())
        cart_page.wait_until_loaded()

        return cart_page
