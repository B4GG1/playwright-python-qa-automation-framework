from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from selenium_pages.base_page import SeleniumBasePage


class SeleniumLoginPage(SeleniumBasePage):
    ROUTE = "/"

    USERNAME_INPUT = (By.CSS_SELECTOR, '[data-test="username"]')
    PASSWORD_INPUT = (By.CSS_SELECTOR, '[data-test="password"]')
    LOGIN_BUTTON = (By.CSS_SELECTOR, '[data-test="login-button"]')
    ERROR_MESSAGE = (By.CSS_SELECTOR, '[data-test="error"]')
    CLOSE_ERROR_MESSAGE_BUTTON = (By.CSS_SELECTOR, '[data-test="error-button"]')
    CREDENTIALS_CONTAINER = (
        By.CSS_SELECTOR,
        '[data-test="login-credentials-container"]',
    )
    LOGIN_CREDENTIALS_HINT = (By.CSS_SELECTOR, '[data-test="login-credentials"]')
    PASSWORD_HINT = (By.CSS_SELECTOR, '[data-test="login-password"]')
    INPUT_ERROR_ICON = (By.CSS_SELECTOR, '[data-icon="circle-xmark"]')

    def login(self, username: str, password: str) -> None:
        username_input = self.get_username_input()
        username_input.clear()
        username_input.send_keys(username)

        password_input = self.get_password_input()
        password_input.clear()
        password_input.send_keys(password)

        # Valid and invalid credentials must both be supported.
        # The caller verifies either navigation or the expected error message.
        self.get_login_button().click()

    @staticmethod
    def get_input_error_icon(input_container: WebElement) -> WebElement:
        return input_container.find_element(By.CSS_SELECTOR, '[data-icon="circle-xmark"]')

    def get_error_message(self) -> WebElement:
        return self.wait_until_visible(self.ERROR_MESSAGE)

    def get_close_error_message_button(self) -> WebElement:
        return self.wait_until_clickable(self.CLOSE_ERROR_MESSAGE_BUTTON)

    def close_error_message(self) -> None:
        self.get_close_error_message_button().click()

    def get_username_input(self) -> WebElement:
        return self.wait_until_clickable(self.USERNAME_INPUT)

    def get_password_input(self) -> WebElement:
        return self.wait_until_clickable(self.PASSWORD_INPUT)

    def get_login_button(self) -> WebElement:
        return self.wait_until_clickable(self.LOGIN_BUTTON)

    def get_credentials_container(self) -> WebElement:
        return self.wait_until_visible(self.CREDENTIALS_CONTAINER)

    def get_login_credentials_hint(self) -> WebElement:
        return self.wait_until_visible(self.LOGIN_CREDENTIALS_HINT)

    def get_password_hint(self) -> WebElement:
        return self.wait_until_visible(self.PASSWORD_HINT)
