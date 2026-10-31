from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config.settings import settings


class SeleniumBasePage:
    ROUTE = ""

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.wait = WebDriverWait(
            driver,
            settings.expect_timeout_ms / 1000,
        )

    @classmethod
    def build_url(cls, url_suffix: str | int = "") -> str:
        return f"{settings.base_url}{cls.ROUTE}{url_suffix}"

    def open(self, url_suffix: str | int = "") -> None:
        self.driver.get(self.build_url(url_suffix))

    def wait_until_visible(self, locator: tuple[By, str]) -> WebElement:
        return self.wait.until(EC.visibility_of_element_located(locator))

    def wait_until_clickable(self, locator: tuple[By, str]) -> WebElement:
        return self.wait.until(EC.element_to_be_clickable(locator))

    def wait_until_url_is(self, expected_url: str) -> bool:
        return self.wait.until(EC.url_to_be(expected_url))
