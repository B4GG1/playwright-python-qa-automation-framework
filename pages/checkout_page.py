from __future__ import annotations

from typing import TYPE_CHECKING

from playwright.sync_api import Locator

from pages.app_page import AppPage

if TYPE_CHECKING:
    from pages.cart_page import CartPage
    from pages.inventory_page import InventoryPage
    from pages.product_details_page import ProductDetailsPage


class CheckoutCompletePage(AppPage):
    URL = "https://www.saucedemo.com/checkout-complete.html"

    def get_checkout_complete_container(self) -> Locator:
        return self.page.locator("[data-test='checkout-complete-container']")

    def get_pony_express_img(self) -> Locator:
        return self.page.locator("[data-test='pony-express']")

    def get_checkout_complete_header(self) -> Locator:
        return self.page.locator("[data-test='complete-header']")

    def get_checkout_complete_text(self) -> Locator:
        return self.page.locator("[data-test='complete-text']")

    def get_back_home_button(self) -> Locator:
        return self.page.locator("[data-test='back-to-products']")

    def back_home(self) -> InventoryPage:
        from pages.inventory_page import InventoryPage

        self.get_back_home_button().click()
        return InventoryPage(self.page)


class CheckoutOverviewPage(AppPage):
    URL = "https://www.saucedemo.com/checkout-step-two.html"

    def get_cart_list(self) -> Locator:
        return self.page.locator("[data-test='cart-list']")

    def get_product_item_by_name(self, product_name: str) -> Locator:
        return self.get_product_item_or_items().filter(has_text=product_name)

    def get_checkout_summary_container(self) -> Locator:
        return self.page.locator("[data-test='checkout-summary-container']")

    def get_payment_info_label(self) -> Locator:
        return self.page.locator("[data-test='payment-info-label']")

    def get_payment_info_value(self) -> Locator:
        return self.page.locator("[data-test='payment-info-value']")

    def get_shipping_info_label(self) -> Locator:
        return self.page.locator("[data-test='shipping-info-label']")

    def get_shipping_info_value(self) -> Locator:
        return self.page.locator("[data-test='shipping-info-value']")

    def get_total_info_label(self) -> Locator:
        return self.page.locator("[data-test='total-info-label']")

    def get_price_item_total_label(self) -> Locator:
        return self.page.locator("[data-test='subtotal-label']")

    def get_price_tax_label(self) -> Locator:
        return self.page.locator("[data-test='tax-label']")

    def get_total_price_label(self) -> Locator:
        return self.page.locator("[data-test='total-label']")

    def get_cancel_button(self) -> Locator:
        return self.page.locator('[data-test="cancel"]')

    def get_finish_button(self) -> Locator:
        return self.page.locator('[data-test="finish"]')

    def cancel_checkout(self) -> InventoryPage:
        from pages.inventory_page import InventoryPage

        self.get_cancel_button().click()
        return InventoryPage(self.page)

    def finish_checkout(self) -> CheckoutCompletePage:
        self.get_finish_button().click()
        return CheckoutCompletePage(self.page)

    def open_product_details_by_name(self, product_name: str) -> ProductDetailsPage:
        from pages.product_details_page import ProductDetailsPage

        product_item = self.get_product_item_by_name(product_name)
        self.get_product_name_from_item(product_item).click()
        return ProductDetailsPage(self.page)


class CheckoutInformationPage(AppPage):
    URL = "https://www.saucedemo.com/checkout-step-one.html"

    def get_first_name_input(self) -> Locator:
        return self.page.locator('[data-test="firstName"]')

    def get_last_name_input(self) -> Locator:
        return self.page.locator('[data-test="lastName"]')

    def get_postal_code_input(self) -> Locator:
        return self.page.locator('[data-test="postalCode"]')

    def get_checkout_info_block(self) -> Locator:
        return self.page.locator(".checkout_info")

    def get_cancel_button(self) -> Locator:
        return self.page.locator('[data-test="cancel"]')

    def get_continue_button(self) -> Locator:
        return self.page.locator('[data-test="continue"]')

    @staticmethod
    def get_input_error_icon(input_container: Locator) -> Locator:
        return input_container.locator("[data-icon='circle-xmark']")

    def get_error_message(self) -> Locator:
        return self.page.locator('[data-test="error"]')

    def get_close_error_message_button(self) -> Locator:
        return self.page.locator('[data-test="error-button"]')

    def cancel_checkout(self) -> CartPage:
        from pages.cart_page import CartPage

        self.get_cancel_button().click()
        return CartPage(self.page)

    def continue_checkout(self) -> CheckoutOverviewPage:
        self.get_continue_button().click()
        return CheckoutOverviewPage(self.page)

    def fill_checkout_info_form(self, first_name, last_name, postal_code) -> None:
        self.get_first_name_input().fill(first_name)
        self.get_last_name_input().fill(last_name)
        self.get_postal_code_input().fill(postal_code)

    def close_error_message(self) -> None:
        self.get_close_error_message_button().click()
