from collections.abc import Generator
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver

from config.settings import settings
from selenium_pages.cart_page import SeleniumCartPage
from selenium_pages.checkout_page import (
    SeleniumCheckoutCompletePage,
    SeleniumCheckoutInformationPage,
    SeleniumCheckoutOverviewPage,
)
from selenium_pages.inventory_page import SeleniumInventoryPage
from selenium_pages.login_page import SeleniumLoginPage
from selenium_pages.product_details_page import SeleniumProductDetailsPage
from test_data.checkout_test_data import VALID_CHECKOUT_CUSTOMER
from test_data.login_test_data import VALID_USER_CASES
from test_data.product_test_data import LIST_OF_PRODUCTS


@pytest.fixture()
def selenium_driver() -> Generator[WebDriver, None, None]:
    options = Options()
    options.add_experimental_option(
        "prefs",
        {
            "profile.password_manager_leak_detection": False,
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
        },
    )
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(settings.timeout_ms / 1000)

    try:
        yield driver
    finally:
        driver.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo[object]):
    outcome = yield
    report = outcome.get_result()

    if not report.failed or report.when not in {"setup", "call"}:
        return

    if not isinstance(item, pytest.Function):
        return

    driver = item.funcargs.get("selenium_driver")
    if not isinstance(driver, WebDriver):
        return

    details = []

    try:
        details.append(f"url={driver.current_url}")
    except Exception as exc:
        details.append(f"url_unavailable={type(exc).__name__}: {exc}")

    try:
        screenshots_dir = Path("reports/selenium/screenshots")
        screenshots_dir.mkdir(parents=True, exist_ok=True)
        screenshot_path = screenshots_dir / f"{item.name}_{report.when}.png"
        if driver.save_screenshot(str(screenshot_path)):
            details.append(f"screenshot={screenshot_path}")
        else:
            details.append("screenshot=not_saved")
    except Exception as exc:
        details.append(f"screenshot_error={type(exc).__name__}: {exc}")

    report.sections.append(("selenium diagnostics", "\n".join(details)))


@pytest.fixture()
def selenium_standard_user() -> dict[str, str]:
    return VALID_USER_CASES[0]


@pytest.fixture()
def selenium_product() -> dict:
    return LIST_OF_PRODUCTS[0]


@pytest.fixture()
def selenium_opened_login_page(
    selenium_driver: WebDriver,
) -> SeleniumLoginPage:
    login_page = SeleniumLoginPage(selenium_driver)
    login_page.open()
    return login_page


@pytest.fixture()
def selenium_logged_in_inventory_page(
    selenium_opened_login_page: SeleniumLoginPage,
    selenium_standard_user: dict[str, str],
) -> SeleniumInventoryPage:
    selenium_opened_login_page.login(
        selenium_standard_user["username"],
        selenium_standard_user["password"],
    )

    inventory_page = SeleniumInventoryPage(selenium_opened_login_page.driver)
    inventory_page.wait_until_loaded()
    return inventory_page


@pytest.fixture()
def selenium_inventory_page_with_one_product_in_cart(
    selenium_logged_in_inventory_page: SeleniumInventoryPage,
    selenium_product: dict,
) -> tuple[SeleniumInventoryPage, dict]:
    selenium_logged_in_inventory_page.add_product_to_cart(selenium_product["product_name"])
    return selenium_logged_in_inventory_page, selenium_product


@pytest.fixture()
def selenium_cart_page_with_one_product(
    selenium_inventory_page_with_one_product_in_cart: tuple[SeleniumInventoryPage, dict],
) -> tuple[SeleniumCartPage, dict]:
    inventory_page, product = selenium_inventory_page_with_one_product_in_cart
    cart_page = inventory_page.open_cart()
    return cart_page, product


@pytest.fixture()
def selenium_checkout_step_one_page_with_one_product(
    selenium_cart_page_with_one_product: tuple[SeleniumCartPage, dict],
) -> tuple[SeleniumCheckoutInformationPage, dict]:
    cart_page, product = selenium_cart_page_with_one_product
    checkout_page = cart_page.checkout()
    return checkout_page, product


@pytest.fixture()
def selenium_checkout_step_two_page_with_one_product(
    selenium_checkout_step_one_page_with_one_product: tuple[SeleniumCheckoutInformationPage, dict],
) -> tuple[SeleniumCheckoutOverviewPage, dict]:
    checkout_step_one, product = selenium_checkout_step_one_page_with_one_product
    checkout_step_one.fill_checkout_info_form(
        VALID_CHECKOUT_CUSTOMER["first_name"],
        VALID_CHECKOUT_CUSTOMER["last_name"],
        VALID_CHECKOUT_CUSTOMER["postal_code"],
    )
    checkout_step_two = checkout_step_one.continue_checkout()
    checkout_step_two.wait_until_loaded()
    return checkout_step_two, product


@pytest.fixture()
def selenium_checkout_last_step_page_with_one_product(
    selenium_checkout_step_two_page_with_one_product: tuple[SeleniumCheckoutOverviewPage, dict],
) -> tuple[SeleniumCheckoutCompletePage, dict]:
    checkout_step_two, product = selenium_checkout_step_two_page_with_one_product
    checkout_last_step = checkout_step_two.finish_checkout()
    return checkout_last_step, product


@pytest.fixture()
def selenium_product_details_page(
    selenium_logged_in_inventory_page: SeleniumInventoryPage,
    selenium_product: dict,
) -> tuple[SeleniumProductDetailsPage, dict]:
    product_details_page = selenium_logged_in_inventory_page.open_product_details_by_name(
        selenium_product["product_name"]
    )
    return product_details_page, selenium_product
