from selenium.webdriver.remote.webdriver import WebDriver

from config.settings import settings


class SeleniumBasePage:
    ROUTE = ""

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver

    @classmethod
    def build_url(cls, url_suffix: str | int = "") -> str:
        return f"{settings.base_url}{cls.ROUTE}{url_suffix}"

    def open(self, url_suffix: str | int = "") -> None:
        self.driver.get(self.build_url(url_suffix))
