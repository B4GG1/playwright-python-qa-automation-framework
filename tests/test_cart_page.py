import pytest
from playwright.sync_api import expect

from pages.inventory_page import InventoryPage
from test_data.login_test_data import VALID_USER_CASES
from test_data.product_test_data import LIST_OF_PRODUCTS

VALID_USER = VALID_USER_CASES[0]
FIRST_EXAMPLE_PRODUCT = LIST_OF_PRODUCTS[0]


@pytest.mark.smoke
@pytest.mark.ui
@pytest.mark.parametrize(
    "_case_id",
    ["TC-CART-001"],
    ids=["TC-CART-001"],
)
def test_cart_is_empty_before_adding_products(
    logged_in_inventory_page: InventoryPage, _case_id: str
):
    expect(logged_in_inventory_page.get_shopping_cart_badge()).to_be_hidden()

    cart_page = logged_in_inventory_page.open_cart()

    expect(cart_page.get_shopping_cart_badge()).to_be_hidden()
    expect(cart_page.get_cart_items()).to_have_count(0)


@pytest.mark.regression
@pytest.mark.positive
@pytest.mark.ui
@pytest.mark.parametrize(
    "_case_id",
    ["TC-CART-002"],
    ids=["TC-CART-002"],
)
def test_added_product_is_displayed_on_cart_page(
    logged_in_inventory_page: InventoryPage, _case_id: str
):
    tested_product_name = FIRST_EXAMPLE_PRODUCT["product_name"]

    logged_in_inventory_page.add_product_to_cart(tested_product_name)
    cart_page = logged_in_inventory_page.open_cart()

    expect(cart_page.get_product_card_by_name(tested_product_name)).to_be_visible()


@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.parametrize(
    "_case_id",
    ["TC-CART-003"],
    ids=["TC-CART-003"],
)
def test_cart_product_content_matches_added_product_data(
    logged_in_inventory_page: InventoryPage, _case_id: str
):
    tested_product_name = FIRST_EXAMPLE_PRODUCT["product_name"]

    logged_in_inventory_page.add_product_to_cart(tested_product_name)
    cart_page = logged_in_inventory_page.open_cart()
    added_product_card = cart_page.get_product_card_by_name(tested_product_name)

    expect(added_product_card).to_be_visible()
    expect(cart_page.get_product_name_from_card_in_cart(added_product_card)).to_have_text(
        FIRST_EXAMPLE_PRODUCT["product_name"]
    )
    expect(cart_page.get_product_description_from_card_in_cart(added_product_card)).to_have_text(
        FIRST_EXAMPLE_PRODUCT["product_description"]
    )
    expect(cart_page.get_product_price_from_card_in_cart(added_product_card)).to_have_text(
        FIRST_EXAMPLE_PRODUCT["product_price"]
    )
    expect(cart_page.get_product_quantity_from_card_in_cart(added_product_card)).to_be_visible()
    expect(cart_page.get_product_quantity_from_card_in_cart(added_product_card)).to_have_text("1")
    expect(cart_page.get_remove_button_from_card_in_cart(added_product_card)).to_be_visible()


@pytest.mark.regression
@pytest.mark.positive
@pytest.mark.ui
@pytest.mark.parametrize(
    "_case_id",
    ["TC-CART-004"],
    ids=["TC-CART-004"],
)
def test_product_can_be_removed_from_cart_page(
    logged_in_inventory_page: InventoryPage, _case_id: str
):
    tested_product_name = FIRST_EXAMPLE_PRODUCT["product_name"]

    logged_in_inventory_page.add_product_to_cart(tested_product_name)
    cart_page = logged_in_inventory_page.open_cart()
    added_product_card = cart_page.get_product_card_by_name(tested_product_name)

    expect(added_product_card).to_be_visible()

    cart_page.remove_item_from_cart(tested_product_name)

    expect(added_product_card).to_be_hidden()


@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.parametrize(
    "_case_id",
    ["TC-CART-005"],
    ids=["TC-CART-005"],
)
def test_cart_badge_is_removed_after_removing_last_product(
    logged_in_inventory_page: InventoryPage, _case_id: str
):
    tested_product_name = FIRST_EXAMPLE_PRODUCT["product_name"]

    logged_in_inventory_page.add_product_to_cart(tested_product_name)

    expect(logged_in_inventory_page.get_shopping_cart_badge()).to_be_visible()
    expect(logged_in_inventory_page.get_shopping_cart_badge()).to_have_text("1")

    cart_page = logged_in_inventory_page.open_cart()
    added_product_card = cart_page.get_product_card_by_name(tested_product_name)

    expect(added_product_card).to_be_visible()

    cart_page.remove_item_from_cart(tested_product_name)

    expect(cart_page.get_shopping_cart_badge()).to_be_hidden()
    expect(added_product_card).to_be_hidden()


@pytest.mark.regression
@pytest.mark.navigation
@pytest.mark.ui
@pytest.mark.parametrize(
    "_case_id",
    ["TC-CART-006"],
    ids=["TC-CART-006"],
)
def test_user_can_continue_shopping_from_cart_page(
    logged_in_inventory_page: InventoryPage, _case_id: str
):
    cart_page = logged_in_inventory_page.open_cart()

    cart_page.continue_shopping()

    expect(logged_in_inventory_page.page).to_have_url(InventoryPage.URL)
    expect(logged_in_inventory_page.get_product_list()).to_be_visible()


@pytest.mark.regression
@pytest.mark.positive
@pytest.mark.ui
@pytest.mark.parametrize(
    "_case_id",
    ["TC-CART-007"],
    ids=["TC-CART-007"],
)
def test_cart_state_persists_after_logout_and_relogin(
    logged_in_inventory_page: InventoryPage, _case_id: str
):
    tested_product_name = FIRST_EXAMPLE_PRODUCT["product_name"]
    tested_product_card = logged_in_inventory_page.get_product_card_by_name(tested_product_name)

    logged_in_inventory_page.add_product_to_cart(tested_product_name)

    expect(
        logged_in_inventory_page.get_remove_from_cart_button_from_card(tested_product_card)
    ).to_be_visible()
    expect(logged_in_inventory_page.get_shopping_cart_badge()).to_be_visible()
    expect(logged_in_inventory_page.get_shopping_cart_badge()).to_have_text("1")

    cart_page = logged_in_inventory_page.open_cart()

    expect(cart_page.get_product_card_by_name(tested_product_name)).to_be_visible()

    cart_page.continue_shopping()

    login_page = logged_in_inventory_page.logout()
    login_page.login(VALID_USER["username"], VALID_USER["password"])

    relogged_inventory_page = InventoryPage(login_page.page)
    relogged_product_card = relogged_inventory_page.get_product_card_by_name(tested_product_name)

    expect(relogged_inventory_page.page).to_have_url(InventoryPage.URL)
    expect(
        relogged_inventory_page.get_remove_from_cart_button_from_card(relogged_product_card)
    ).to_be_visible()
    expect(relogged_inventory_page.get_shopping_cart_badge()).to_be_visible()
    expect(relogged_inventory_page.get_shopping_cart_badge()).to_have_text("1")

    cart_page_after_reload = relogged_inventory_page.open_cart()

    expect(cart_page_after_reload.get_product_card_by_name(tested_product_name)).to_be_visible()
