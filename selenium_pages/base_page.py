import logging
from collections.abc import Callable

from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config.settings import settings

LOGGER = logging.getLogger(__name__)


class SeleniumBasePage:
    ROUTE = ""

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.wait = WebDriverWait(
            driver,
            settings.expect_timeout_ms / 1000,
            ignored_exceptions=(StaleElementReferenceException,),
        )

    @classmethod
    def build_url(cls, url_suffix: str | int = "") -> str:
        return f"{settings.base_url}{cls.ROUTE}{url_suffix}"

    def open(self, url_suffix: str | int = "") -> None:
        self.driver.get(self.build_url(url_suffix))

    def wait_until_visible(self, locator: tuple[str, str]) -> WebElement:
        return self.wait.until(EC.visibility_of_element_located(locator))

    def wait_until_clickable(self, locator: tuple[str, str]) -> WebElement:
        return self.wait.until(EC.element_to_be_clickable(locator))

    def wait_until_url_is(self, expected_url: str) -> bool:
        return self.wait.until(EC.url_to_be(expected_url))

    def click_and_confirm(
        self,
        find_target: Callable[[], WebElement],
        condition: Callable[[WebDriver], object],
        *,
        action: str,
    ) -> None:
        """Click through WebDriver; use one DOM fallback only if no effect follows.

        The fallback addresses the observed ChromeDriver case where .click() returns
        successfully but the application receives no pointer/click events. It is
        not a test of native pointer handling. A verified state change is mandatory.
        """
        find_target().click()

        # Normal transitions are fast. Do not wait the full assertion timeout before
        # recovering an apparently lost click. The postcondition prevents repeat
        # clicks once the action has taken effect.
        initial_wait = WebDriverWait(
            self.driver,
            min(3.0, settings.expect_timeout_ms / 1000),
            ignored_exceptions=(StaleElementReferenceException,),
        )
        try:
            initial_wait.until(condition)
            return
        except TimeoutException:
            pass

        if condition(self.driver):
            return

        # Re-locate the live DOM node; never reuse a potentially stale element.
        LOGGER.warning(
            "Selenium native click had no confirmed effect for %s at %s; "
            "trying one DOM click fallback",
            action,
            self.driver.current_url,
        )
        self.driver.execute_script("arguments[0].click();", find_target())

        try:
            self.wait.until(condition)
        except TimeoutException as exc:
            raise TimeoutException(
                f"Selenium action {action!r} had no confirmed effect after both "
                f"native and DOM clicks. Current URL: {self.driver.current_url}"
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
            EC.url_to_be(expected_url),
            action=action,
        )
