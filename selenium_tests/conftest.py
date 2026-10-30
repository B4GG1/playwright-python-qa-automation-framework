from collections.abc import Generator

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver

from config.settings import settings


@pytest.fixture()
def selenium_driver() -> Generator[WebDriver, None, None]:
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1280,720")

    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(settings.timeout_ms / 1000)

    try:
        yield driver
    finally:
        driver.quit()
