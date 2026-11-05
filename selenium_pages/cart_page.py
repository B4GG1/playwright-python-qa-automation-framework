from __future__ import annotations

from typing import TYPE_CHECKING

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from selenium_pages.app_page import SeleniumAppPage

if TYPE_CHECKING:
    from selenium_pages.checkout_page import SeleniumCheckoutInformationPage
    from selenium_pages.inventory_page import SeleniumInventoryPage
    from selenium_pages.product_details_page import SeleniumProductDetailsPage


class SeleniumCartPage(SeleniumAppPage):
    ROUTE = "/cart.html"

    CART_CONTENTS_CONTAINER = (By.CSS_SELECTOR, '[data-test="cart-contents-container"]')
    CART_LIST = (By.CSS_SELECTOR, '[data-test="cart-list"]')
    CONTINUE_SHOPPING_BUTTON = (By.CSS_SELECTOR, '[data-test="continue-shopping"]')
    CHECKOUT_BUTTON = (By.CSS_SELECTOR, '[data-test="checkout"]')

    def wait_until_loaded(self) -> WebElement:
        return self.get_cart_contents_container()

    def get_cart_contents_container(self) -> WebElement:
        return self.wait_until_visible(self.CART_CONTENTS_CONTAINER)

    def get_cart_list(self) -> WebElement:
        return self.wait_until_visible(self.CART_LIST)

    def get_product_item_by_name(self, product_name: str) -> WebElement:
        def matching_item(_driver: object) -> WebElement | bool:
            for product_item in self.get_product_item_or_items():
                if self.get_product_name_from_item(product_item).text == product_name:
                    return product_item
            return False

        try:
            return self.wait.until(matching_item)
        except TimeoutException as exc:
            raise AssertionError(f"Product not found in Cart: {product_name}") from exc

    def remove_product_from_cart(self, product_name: str) -> None:
        product_item = self.get_product_item_by_name(product_name)
        self.get_remove_button_from_item(product_item).click()

    def open_product_details_by_name(self, product_name: str) -> SeleniumProductDetailsPage:
        from selenium_pages.product_details_page import SeleniumProductDetailsPage

        product_item = self.get_product_item_by_name(product_name)
        self.get_product_name_from_item(product_item).click()

        product_details_page = SeleniumProductDetailsPage(self.driver)
        self.wait.until(
            lambda driver: driver.current_url.startswith(product_details_page.build_url())
        )
        product_details_page.wait_until_loaded()

        return product_details_page

    def get_continue_shopping_button(self) -> WebElement:
        return self.wait_until_clickable(self.CONTINUE_SHOPPING_BUTTON)

    def continue_shopping(self) -> SeleniumInventoryPage:
        from selenium_pages.inventory_page import SeleniumInventoryPage

        inventory_page = SeleniumInventoryPage(self.driver)
        self.click_and_confirm_url(
            self.CONTINUE_SHOPPING_BUTTON,
            inventory_page.build_url(),
            action="Continue Shopping",
        )
        inventory_page.wait_until_loaded()

        return inventory_page

    def get_checkout_button(self) -> WebElement:
        return self.wait_until_clickable(self.CHECKOUT_BUTTON)

    def checkout(self) -> SeleniumCheckoutInformationPage:
        from selenium_pages.checkout_page import SeleniumCheckoutInformationPage

        checkout_page = SeleniumCheckoutInformationPage(self.driver)
        self.click_and_confirm_url(
            self.CHECKOUT_BUTTON,
            checkout_page.build_url(),
            action="Open Checkout Information",
        )
        checkout_page.wait_until_loaded()

        return checkout_page

    # Compatibility with existing Selenium E2E assertions.
    def get_product_name(self, product_item: WebElement) -> str:
        return self.get_product_name_from_item(product_item).text

    def get_product_description(self, product_item: WebElement) -> str:
        return self.get_product_description_from_item(product_item).text

    def get_product_price(self, product_item: WebElement) -> str:
        return self.get_product_price_from_item(product_item).text

    def get_product_quantity(self, product_item: WebElement) -> str:
        return self.get_product_quantity_from_item(product_item).text
