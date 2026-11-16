from collections.abc import Callable

from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from config.settings import settings


class SeleniumBasePage:
    ROUTE = ""

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.wait = WebDriverWait(
            driver,
            settings.expect_timeout_ms / 1000,
            ignored_exceptions=(
                NoSuchElementException,
                StaleElementReferenceException,
            ),
        )

    @classmethod
    def build_url(cls, url_suffix: str | int = "") -> str:
        return f"{settings.base_url}{cls.ROUTE}{url_suffix}"

    def open(self, url_suffix: str | int = "") -> None:
        self.driver.get(self.build_url(url_suffix))

    def wait_until_visible(self, locator: tuple[str, str]) -> WebElement:
        return self.wait.until(ec.visibility_of_element_located(locator))

    def wait_until_clickable(self, locator: tuple[str, str]) -> WebElement:
        return self.wait.until(ec.element_to_be_clickable(locator))

    def wait_until_url_is(self, expected_url: str) -> bool:
        return self.wait.until(ec.url_to_be(expected_url))

    def click_and_confirm(
        self,
        find_target: Callable[[], WebElement],
        condition: Callable[[WebDriver], object],
        *,
        action: str,
    ) -> None:
        """Perform one WebDriver click and wait for the expected outcome.

        Do not retry clicks automatically: a delayed first click may already
        be in progress, and repeating an action can change application state.
        """
        find_target().click()

        try:
            self.wait.until(condition)
        except TimeoutException as exc:
            raise TimeoutException(
                f"Selenium action {action!r} had no confirmed effect within "
                f"{settings.expect_timeout_ms} ms. "
                f"Current URL: {self.driver.current_url}"
            ) from exc

    def click_and_confirm_url(
        self,
        locator: tuple[str, str],
        expected_url: str,
        *,
        action: str,
    ) -> None:
        self.click_and_confirm(
            lambda: self.wait_until_clickable(locator),
            ec.url_to_be(expected_url),
            action=action,
        )
