import os
from datetime import datetime

import pytest
from playwright.sync_api import Page

from pages.login_page import LoginPage


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when != "call" or not report.failed:
        return

    page = item.funcargs.get("page")
    if page is None:
        return

    reports_dir = os.path.join("reports", "screenshots")
    os.makedirs(reports_dir, exist_ok=True)

    timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
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
