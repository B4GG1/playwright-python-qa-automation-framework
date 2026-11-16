from __future__ import annotations

from typing import TYPE_CHECKING

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from selenium_pages.base_page import SeleniumBasePage

if TYPE_CHECKING:
    from selenium_pages.cart_page import SeleniumCartPage
    from selenium_pages.inventory_page import SeleniumInventoryPage
    from selenium_pages.login_page import SeleniumLoginPage


class SeleniumAppPage(SeleniumBasePage):
    """Shared actions and product elements on authenticated Sauce Demo pages."""

    SHOPPING_CART_LINK = (By.CSS_SELECTOR, '[data-test="shopping-cart-link"]')
    SHOPPING_CART_BADGE = (By.CSS_SELECTOR, '[data-test="shopping-cart-badge"]')
    BURGER_MENU_BUTTON = (By.ID, "react-burger-menu-btn")
    CLOSE_MENU_BUTTON = (By.ID, "react-burger-cross-btn")
    LOGOUT_SIDEBAR_LINK = (By.CSS_SELECTOR, '[data-test="logout-sidebar-link"]')
    ALL_ITEMS_SIDEBAR_LINK = (By.CSS_SELECTOR, '[data-test="inventory-sidebar-link"]')
    RESET_APP_STATE_SIDEBAR_LINK = (By.CSS_SELECTOR, '[data-test="reset-sidebar-link"]')
    ABOUT_SIDEBAR_LINK = (By.CSS_SELECTOR, '[data-test="about-sidebar-link"]')
    PRODUCT_ITEMS = (By.CSS_SELECTOR, '[data-test="inventory-item"]')

    # Shared authenticated header and sidebar actions
    def get_shopping_cart_link(self) -> WebElement:
        return self.wait_until_clickable(self.SHOPPING_CART_LINK)

    def open_cart(self) -> SeleniumCartPage:
        from selenium_pages.cart_page import SeleniumCartPage

        cart_page = SeleniumCartPage(self.driver)
        self.click_and_confirm_url(
            self.SHOPPING_CART_LINK,
            cart_page.build_url(),
            action="Open Cart",
        )
        cart_page.wait_until_loaded()
        return cart_page

    def get_shopping_cart_badge(self) -> WebElement:
        return self.wait_until_visible(self.SHOPPING_CART_BADGE)

    def get_burger_menu_button(self) -> WebElement:
        return self.wait_until_clickable(self.BURGER_MENU_BUTTON)

    def get_close_menu_button(self) -> WebElement:
        return self.wait_until_clickable(self.CLOSE_MENU_BUTTON)

    def get_logout_sidebar_link(self) -> WebElement:
        return self.wait_until_clickable(self.LOGOUT_SIDEBAR_LINK)

    def get_all_items_sidebar_link(self) -> WebElement:
        return self.wait_until_clickable(self.ALL_ITEMS_SIDEBAR_LINK)

    def get_reset_app_state_sidebar_link(self) -> WebElement:
        return self.wait_until_clickable(self.RESET_APP_STATE_SIDEBAR_LINK)

    def get_about_sidebar_link(self) -> WebElement:
        return self.wait_until_clickable(self.ABOUT_SIDEBAR_LINK)

    def open_menu(self) -> None:
        self.get_burger_menu_button().click()
        self.get_logout_sidebar_link()

    def close_menu(self) -> None:
        self.get_close_menu_button().click()

    def logout(self) -> SeleniumLoginPage:
        from selenium_pages.login_page import SeleniumLoginPage

        self.open_menu()
        login_page = SeleniumLoginPage(self.driver)
        self.click_and_confirm_url(
            self.LOGOUT_SIDEBAR_LINK,
            login_page.build_url(),
            action="Log out",
        )
        login_page.wait_until_visible(login_page.USERNAME_INPUT)
        return login_page

    def reset_app_state(self) -> None:
        self.open_menu()
        self.get_reset_app_state_sidebar_link().click()

    def open_about_page(self) -> None:
        self.open_menu()
        self.get_about_sidebar_link().click()

    def back_to_all_items(self) -> SeleniumInventoryPage:
        from selenium_pages.inventory_page import SeleniumInventoryPage

        self.open_menu()
        inventory_page = SeleniumInventoryPage(self.driver)
        self.click_and_confirm_url(
            self.ALL_ITEMS_SIDEBAR_LINK,
            inventory_page.build_url(),
            action="Return to All Items",
        )
        inventory_page.wait_until_loaded()
        return inventory_page

    # Shared elements for product-like item containers
    def get_product_item_or_items(self) -> list[WebElement]:
        """Return a current snapshot, not a lazy Playwright-style locator."""
        return self.driver.find_elements(*self.PRODUCT_ITEMS)

    @staticmethod
    def get_product_name_from_item(product_item: WebElement) -> WebElement:
        return product_item.find_element(By.CSS_SELECTOR, '[data-test="inventory-item-name"]')

    @staticmethod
    def get_product_description_from_item(product_item: WebElement) -> WebElement:
        return product_item.find_element(By.CSS_SELECTOR, '[data-test="inventory-item-desc"]')

    @staticmethod
    def get_product_price_from_item(product_item: WebElement) -> WebElement:
        return product_item.find_element(By.CSS_SELECTOR, '[data-test="inventory-item-price"]')

    @staticmethod
    def get_product_image_from_item(product_item: WebElement) -> WebElement:
        return product_item.find_element(
            By.CSS_SELECTOR,
            "img.inventory_item_img, img.inventory_details_img",
        )

    @staticmethod
    def get_add_to_cart_button_from_item(product_item: WebElement) -> WebElement:
        return product_item.find_element(By.CSS_SELECTOR, 'button[data-test^="add-to-cart"]')

    @staticmethod
    def get_product_quantity_from_item(product_item: WebElement) -> WebElement:
        return product_item.find_element(By.CSS_SELECTOR, '[data-test="item-quantity"]')

    @staticmethod
    def get_remove_button_from_item(product_item: WebElement) -> WebElement:
        return product_item.find_element(By.CSS_SELECTOR, 'button[data-test^="remove"]')
