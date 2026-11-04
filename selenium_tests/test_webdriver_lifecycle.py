import pytest
from selenium.webdriver.support.ui import WebDriverWait

from config.settings import settings
from selenium_pages.base_page import SeleniumBasePage


@pytest.mark.selenium
def test_chrome_webdriver_can_open_application(selenium_driver) -> None:
    base_page = SeleniumBasePage(selenium_driver)

    base_page.open()

    WebDriverWait(
        selenium_driver,
        settings.expect_timeout_ms / 1000,
    ).until(lambda driver: driver.current_url.startswith(settings.base_url))

    assert selenium_driver.current_url.startswith(settings.base_url)
