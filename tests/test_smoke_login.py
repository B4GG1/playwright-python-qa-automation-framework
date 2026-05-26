from playwright.sync_api import Page, expect


def test_sauce_demo_smoke(page: Page):
    # Arrange
    url = "https://www.saucedemo.com/"
    # Act
    page.goto(url)
    # Assert
    expect(page).to_have_title("Swag Labs")


# def test_sauce_demo_fail_check(page: Page):
#      # Arrange
#      url = "https://www.saucedemo.com/"
#      # Act
#      page.goto(url)
#      # Assert
#      expect(page).to_have_title("WRONG")
