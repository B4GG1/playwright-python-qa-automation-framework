from selenium.webdriver.common.by import By

from selenium_pages.base_page import SeleniumBasePage


class SeleniumLoginPage(SeleniumBasePage):
    ROUTE = "/"

    USERNAME_INPUT = (By.CSS_SELECTOR, '[data-test="username"]')
    PASSWORD_INPUT = (By.CSS_SELECTOR, '[data-test="password"]')
    LOGIN_BUTTON = (By.CSS_SELECTOR, '[data-test="login-button"]')

    def login(self, username: str, password: str) -> None:
        self.wait_until_visible(self.USERNAME_INPUT).send_keys(username)
        self.wait_until_visible(self.PASSWORD_INPUT).send_keys(password)
        self.wait_until_clickable(self.LOGIN_BUTTON).click()
