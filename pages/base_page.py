from playwright.sync_api import Page


class BasePage:
    URL = ""

    def __init__(self, page: Page):
        self.page = page

    def open(self, url_suffix: str | int = "") -> None:
        self.page.goto(f"{self.URL}{url_suffix}")
