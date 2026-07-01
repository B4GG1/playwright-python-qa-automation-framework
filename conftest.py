import os
from datetime import UTC, datetime

import pytest
from playwright.sync_api import Page

from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from test_data.login_test_data import VALID_USER_CASES
from test_data.product_test_data import LIST_OF_PRODUCTS


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, _call):
    outcome = yield
    report = outcome.get_result()

    if report.when != "call" or not report.failed:
        return

    page = item.funcargs.get("page")
    if page is None:
        return

    reports_dir = os.path.join("reports", "screenshots")
    os.makedirs(reports_dir, exist_ok=True)

    timestamp = datetime.now(UTC).strftime("%Y-%m-%d_%H-%M-%S")
    test_name = item.name.replace("/", "_").replace("::", "_")

    file_path = os.path.join(reports_dir, f"{test_name}_{timestamp}.png")

    try:
        page.screenshot(path=file_path, full_page=True)
    except Exception as e:
        print(f"[screenshot-error] {test_name}: {e}")


@pytest.fixture()
def opened_login_page(page: Page) -> LoginPage:
    login_page = LoginPage(page)
    login_page.open()
    return login_page


@pytest.fixture()
def standard_user() -> dict[str, str]:
    return VALID_USER_CASES[0]


@pytest.fixture()
def logged_in_inventory_page(
    opened_login_page: LoginPage,
    standard_user: dict[str, str],
) -> InventoryPage:
    opened_login_page.login(standard_user["username"], standard_user["password"])
    return InventoryPage(opened_login_page.page)


@pytest.fixture()
def inventory_page_with_one_product_in_cart(
    logged_in_inventory_page: InventoryPage,
) -> tuple[InventoryPage, dict[str, str]]:
    product = LIST_OF_PRODUCTS[0]
    logged_in_inventory_page.add_product_to_cart(product["product_name"])
    return logged_in_inventory_page, product


@pytest.fixture()
def cart_page_with_one_product(
    inventory_page_with_one_product_in_cart: tuple[InventoryPage, dict[str, str]],
) -> tuple[CartPage, dict[str, str]]:
    inventory_page, product = inventory_page_with_one_product_in_cart
    cart_page = inventory_page.open_cart()
    return cart_page, product
