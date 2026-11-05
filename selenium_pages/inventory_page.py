from __future__ import annotations

from typing import TYPE_CHECKING

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import Select

from selenium_pages.app_page import SeleniumAppPage

if TYPE_CHECKING:
    from selenium_pages.product_details_page import SeleniumProductDetailsPage


class SeleniumInventoryPage(SeleniumAppPage):
    ROUTE = "/inventory.html"

    SORT_NAME_ASC = "az"
    SORT_NAME_DESC = "za"
    SORT_PRICE_LOW_HIGH = "lohi"
    SORT_PRICE_HIGH_LOW = "hilo"

    INVENTORY_CONTAINER = (By.CSS_SELECTOR, '[data-test="inventory-container"]')
    PRODUCT_LIST = (By.CSS_SELECTOR, '[data-test="inventory-list"]')
    PRODUCT_NAMES = (By.CSS_SELECTOR, '[data-test="inventory-item-name"]')
    PRODUCT_PRICES = (By.CSS_SELECTOR, '[data-test="inventory-item-price"]')
    PRODUCT_SORTING_DROPDOWN = (By.CSS_SELECTOR, '[data-test="product-sort-container"]')
    BACK_TO_PRODUCTS_BUTTON = (By.CSS_SELECTOR, '[data-test="back-to-products"]')

    def get_inventory_container(self) -> WebElement:
        return self.wait_until_visible(self.INVENTORY_CONTAINER)

    def wait_until_loaded(self) -> WebElement:
        return self.get_inventory_container()

    def get_product_list(self) -> WebElement:
        return self.wait_until_visible(self.PRODUCT_LIST)

    def get_product_item_by_name(self, product_name: str) -> WebElement:
        self.get_product_list()

        def find_product(_driver) -> WebElement | bool:
            for item in self.get_product_item_or_items():
                if self.get_product_name_from_item(item).text == product_name:
                    return item
            return False

        try:
            return self.wait.until(find_product)
        except TimeoutException as exc:
            raise AssertionError(f"Product not found on Inventory page: {product_name}") from exc

    def get_product_names(self) -> list[str]:
        self.wait_until_visible(self.PRODUCT_NAMES)
        return [item.text for item in self.driver.find_elements(*self.PRODUCT_NAMES)]

    def get_product_prices(self) -> list[str]:
        self.wait_until_visible(self.PRODUCT_PRICES)
        return [item.text for item in self.driver.find_elements(*self.PRODUCT_PRICES)]

    def get_product_sorting_dropdown(self) -> WebElement:
        return self.wait_until_clickable(self.PRODUCT_SORTING_DROPDOWN)

    def sort_products_by(self, sort_option_value: str) -> None:
        Select(self.get_product_sorting_dropdown()).select_by_value(sort_option_value)

    def open_product_details_by_name(self, product_name: str) -> SeleniumProductDetailsPage:
        from selenium_pages.product_details_page import SeleniumProductDetailsPage

        self.click_and_confirm(
            lambda: self.get_product_name_from_item(self.get_product_item_by_name(product_name)),
            lambda driver: driver.current_url.startswith(SeleniumProductDetailsPage.build_url()),
            action=f"Open Product Details by name: {product_name}",
        )

        details_page = SeleniumProductDetailsPage(self.driver)
        details_page.wait_until_loaded()
        details_page.wait_until_visible(self.BACK_TO_PRODUCTS_BUTTON)
        return details_page

    def open_product_details_by_image(self, product_name: str) -> SeleniumProductDetailsPage:
        from selenium_pages.product_details_page import SeleniumProductDetailsPage

        self.click_and_confirm(
            lambda: self.get_product_image_from_item(self.get_product_item_by_name(product_name)),
            lambda driver: driver.current_url.startswith(SeleniumProductDetailsPage.build_url()),
            action=f"Open Product Details by image: {product_name}",
        )

        details_page = SeleniumProductDetailsPage(self.driver)
        details_page.wait_until_loaded()
        details_page.wait_until_visible(self.BACK_TO_PRODUCTS_BUTTON)
        return details_page

    def add_product_to_cart(self, product_name: str) -> None:
        product_item = self.get_product_item_by_name(product_name)
        self.get_add_to_cart_button_from_item(product_item).click()
        self.wait.until(
            lambda _driver: self.get_remove_button_from_item(
                self.get_product_item_by_name(product_name)
            ).is_displayed()
        )

    def remove_product_from_cart(self, product_name: str) -> None:
        product_item = self.get_product_item_by_name(product_name)
        self.get_remove_button_from_item(product_item).click()
        self.wait.until(
            lambda _driver: self.get_add_to_cart_button_from_item(
                self.get_product_item_by_name(product_name)
            ).is_displayed()
        )

    # Compatibility with existing Selenium E2E assertions.
    def get_product_name(self, product_item: WebElement) -> str:
        return self.get_product_name_from_item(product_item).text

    def get_product_description(self, product_item: WebElement) -> str:
        return self.get_product_description_from_item(product_item).text

    def get_product_price(self, product_item: WebElement) -> str:
        return self.get_product_price_from_item(product_item).text
