from playwright.sync_api import Page

from config.settings import settings


class BasePage:
    ROUTE = ""

    def __init__(self, page: Page):
        self.page = page

    @classmethod
    def build_url(cls, url_suffix: str | int = "") -> str:
        return f"{settings.base_url}{cls.ROUTE}{url_suffix}"

    def open(self, url_suffix: str | int = "") -> None:
        self.page.goto(self.build_url(url_suffix))
