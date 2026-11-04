from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC

from selenium_pages.base_page import SeleniumBasePage


class SeleniumProductDetailsPage(SeleniumBasePage):
    ROUTE = "/inventory-item.html?id="

    PRODUCT_ITEM = (By.CSS_SELECTOR, '[data-test="inventory-item"]')
    PRODUCT_NAME = (By.CSS_SELECTOR, '[data-test="inventory-item-name"]')
    PRODUCT_DESCRIPTION = (By.CSS_SELECTOR, '[data-test="inventory-item-desc"]')
    PRODUCT_PRICE = (By.CSS_SELECTOR, '[data-test="inventory-item-price"]')
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, '[data-test^="add-to-cart"]')
    SHOPPING_CART_LINK = (By.CSS_SELECTOR, '[data-test="shopping-cart-link"]')
    SHOPPING_CART_BADGE = (By.CSS_SELECTOR, '[data-test="shopping-cart-badge"]')

    def wait_until_loaded(self) -> WebElement:
        return self.wait_until_visible(self.PRODUCT_ITEM)

    def get_product_name(self) -> str:
        return self.wait_until_visible(self.PRODUCT_NAME).text

    def get_product_description(self) -> str:
        return self.wait_until_visible(self.PRODUCT_DESCRIPTION).text

    def get_product_price(self) -> str:
        return self.wait_until_visible(self.PRODUCT_PRICE).text

    def add_product_to_cart(self) -> None:
        self.click_and_confirm(
            lambda: self.wait_until_clickable(self.ADD_TO_CART_BUTTON),
            EC.visibility_of_element_located(self.SHOPPING_CART_BADGE),
            action="Add product to Cart",
        )

    def open_cart(self):
        from selenium_pages.cart_page import SeleniumCartPage

        cart_page = SeleniumCartPage(self.driver)
        self.click_and_confirm_url(
            self.SHOPPING_CART_LINK,
            cart_page.build_url(),
            action="Open Cart from Product Details",
        )
        cart_page.wait_until_loaded()

        return cart_page
