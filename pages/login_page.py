from playwright.sync_api import Page


class LoginPage:
    URL = "https://www.saucedemo.com/"

    def __init__(self, page: Page):
        self.page = page

    def open(self) -> None:
        self.page.goto(self.URL)

    def login(self, username: str, password: str) -> None:
        self.page.locator('[data-test="username"]').fill(username)
        self.page.locator('[data-test="password"]').fill(password)
        self.page.locator('[data-test="login-button"]').click()

    def get_error_message(self) -> str:
        message = self.page.locator('[data-test="error"]')
        return message.inner_text()
