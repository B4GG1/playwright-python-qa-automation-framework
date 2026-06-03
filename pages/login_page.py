from playwright.sync_api import Locator, Page


class LoginPage:
    URL = "https://www.saucedemo.com/"

    def __init__(self, page: Page):
        self.page = page

    def open(self) -> None:
        self.page.goto(self.URL)

    def login(self, username: str, password: str) -> None:
        self.get_username_input().fill(username)
        self.get_password_input().fill(password)
        self.get_login_button().click()

    def get_error_message(self) -> str:
        return self.page.locator('[data-test="error"]').inner_text()

    def get_username_input(self) -> Locator:
        return self.page.locator('[data-test="username"]')

    def get_password_input(self) -> Locator:
        return self.page.locator('[data-test="password"]')

    def get_login_button(self) -> Locator:
        return self.page.locator('[data-test="login-button"]')

    def get_credentials_container(self) -> Locator:
        return self.page.locator('[data-test="login-credentials-container"]')

    def get_login_form_container(self) -> Locator:
        return self.page.locator('[data-test="login-credentials"]')

    def get_password_form_container(self):
        return self.page.locator('[data-test="login-password"]')
