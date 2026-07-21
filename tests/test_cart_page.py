import pytest
from playwright.sync_api import expect

from framework.assertions.product_assertions import (
    assert_cart_product_item_displays_expected_product,
)
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutInformationPage
from pages.inventory_page import InventoryPage
from pages.product_details_page import ProductDetailsPage
from test_data.product_test_data import LIST_OF_PRODUCTS

FIRST_EXAMPLE_PRODUCT = LIST_OF_PRODUCTS[0]
SECOND_EXAMPLE_PRODUCT = LIST_OF_PRODUCTS[1]


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
    expect(cart_page.get_product_item_or_items()).to_have_count(0)


@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.ui
@pytest.mark.parametrize(
    "_case_id",
    ["TC-CART-002"],
    ids=["TC-CART-002"],
)
def test_added_product_is_displayed_on_cart_page(
    cart_page_with_one_product: tuple[CartPage, dict[str, str]],
    _case_id: str,
):
    cart_page, product = cart_page_with_one_product

    expect(cart_page.get_product_item_by_name(product["product_name"])).to_be_visible()


@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.parametrize(
    "_case_id",
    ["TC-CART-003"],
    ids=["TC-CART-003"],
)
def test_cart_product_content_matches_added_product_data(
    cart_page_with_one_product: tuple[CartPage, dict[str, str]],
    _case_id: str,
):
    cart_page, product = cart_page_with_one_product
    added_product_item = cart_page.get_product_item_by_name(product["product_name"])

    expect(added_product_item).to_be_visible()
    expect(cart_page.get_product_name_from_item(added_product_item)).to_have_text(
        product["product_name"]
    )
    expect(cart_page.get_product_description_from_item(added_product_item)).to_have_text(
        product["product_description"]
    )
    expect(cart_page.get_product_price_from_item(added_product_item)).to_have_text(
        product["product_price"]
    )
    expect(cart_page.get_product_quantity_from_item(added_product_item)).to_be_visible()
    expect(cart_page.get_product_quantity_from_item(added_product_item)).to_have_text("1")
    expect(cart_page.get_remove_button_from_item(added_product_item)).to_be_visible()


@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.ui
@pytest.mark.parametrize(
    "_case_id",
    ["TC-CART-004"],
    ids=["TC-CART-004"],
)
def test_product_can_be_removed_from_cart_page(
    cart_page_with_one_product: tuple[CartPage, dict[str, str]],
    _case_id: str,
):
    cart_page, product = cart_page_with_one_product
    added_product_item = cart_page.get_product_item_by_name(product["product_name"])

    expect(added_product_item).to_be_visible()

    cart_page.remove_product_from_cart(product["product_name"])

    expect(added_product_item).to_be_hidden()


@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.parametrize(
    "_case_id",
    ["TC-CART-005"],
    ids=["TC-CART-005"],
)
def test_cart_badge_is_removed_after_removing_last_product(
    cart_page_with_one_product: tuple[CartPage, dict[str, str]],
    _case_id: str,
):
    cart_page, product = cart_page_with_one_product
    added_product_item = cart_page.get_product_item_by_name(product["product_name"])

    expect(cart_page.get_shopping_cart_badge()).to_be_visible()
    expect(cart_page.get_shopping_cart_badge()).to_have_text("1")
    expect(added_product_item).to_be_visible()

    cart_page.remove_product_from_cart(product["product_name"])

    expect(cart_page.get_shopping_cart_badge()).to_be_hidden()
    expect(added_product_item).to_be_hidden()


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

    inventory_page = cart_page.continue_shopping()

    expect(inventory_page.page).to_have_url(InventoryPage.URL)
    expect(inventory_page.get_product_list()).to_be_visible()


@pytest.mark.regression
@pytest.mark.positive
@pytest.mark.ui
@pytest.mark.parametrize(
    "_case_id",
    ["TC-CART-007"],
    ids=["TC-CART-007"],
)
def test_cart_state_persists_after_logout_and_relogin(
    inventory_page_with_one_product_in_cart: tuple[InventoryPage, dict[str, str]],
    standard_user: dict[str, str],
    _case_id: str,
):
    inventory_page, product = inventory_page_with_one_product_in_cart
    tested_product_name = product["product_name"]
    tested_product_item = inventory_page.get_product_item_by_name(tested_product_name)

    expect(inventory_page.get_remove_button_from_item(tested_product_item)).to_be_visible()
    expect(inventory_page.get_shopping_cart_badge()).to_be_visible()
    expect(inventory_page.get_shopping_cart_badge()).to_have_text("1")

    cart_page = inventory_page.open_cart()

    expect(cart_page.get_product_item_by_name(tested_product_name)).to_be_visible()

    inventory_page = cart_page.continue_shopping()

    login_page = inventory_page.logout()
    login_page.login(standard_user["username"], standard_user["password"])

    relogged_inventory_page = InventoryPage(login_page.page)
    relogged_product_item = relogged_inventory_page.get_product_item_by_name(tested_product_name)

    expect(relogged_inventory_page.page).to_have_url(InventoryPage.URL)
    expect(
        relogged_inventory_page.get_remove_button_from_item(relogged_product_item)
    ).to_be_visible()
    expect(relogged_inventory_page.get_shopping_cart_badge()).to_be_visible()
    expect(relogged_inventory_page.get_shopping_cart_badge()).to_have_text("1")

    cart_page_after_reload = relogged_inventory_page.open_cart()

    expect(cart_page_after_reload.get_product_item_by_name(tested_product_name)).to_be_visible()


@pytest.mark.regression
@pytest.mark.positive
@pytest.mark.ui
@pytest.mark.parametrize(
    "_case_id",
    ["TC-CART-008"],
    ids=["TC-CART-008"],
)
def test_all_added_products_are_displayed_on_cart_page(
    logged_in_inventory_page: InventoryPage,
    _case_id: str,
):
    for product in LIST_OF_PRODUCTS:
        logged_in_inventory_page.add_product_to_cart(product["product_name"])

    cart_page = logged_in_inventory_page.open_cart()

    for product in LIST_OF_PRODUCTS:
        expect(cart_page.get_product_item_by_name(product["product_name"])).to_be_visible()


@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.parametrize(
    "product",
    LIST_OF_PRODUCTS,
    ids=[f"TC-CART-009-{product['product_id']}" for product in LIST_OF_PRODUCTS],
)
def test_cart_product_content_matches_added_product_data_for_each_product(
    logged_in_inventory_page: InventoryPage, product
):
    logged_in_inventory_page.add_product_to_cart(product["product_name"])
    cart_page = logged_in_inventory_page.open_cart()
    assert_cart_product_item_displays_expected_product(
        cart_page=cart_page,
        product=product,
        expected_quantity="1",
    )


@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.parametrize(
    "_case_id",
    ["TC-CART-010"],
    ids=["TC-CART-010"],
)
def test_cart_badge_decrements_after_removing_one_of_multiple_products(
    logged_in_inventory_page: InventoryPage,
    _case_id: str,
):
    logged_in_inventory_page.add_product_to_cart(FIRST_EXAMPLE_PRODUCT["product_name"])
    logged_in_inventory_page.add_product_to_cart(SECOND_EXAMPLE_PRODUCT["product_name"])

    cart_page = logged_in_inventory_page.open_cart()

    expect(cart_page.get_shopping_cart_badge()).to_have_text("2")

    cart_page.remove_product_from_cart(FIRST_EXAMPLE_PRODUCT["product_name"])

    expect(cart_page.get_shopping_cart_badge()).to_have_text("1")
    expect(
        cart_page.get_product_item_by_name(FIRST_EXAMPLE_PRODUCT["product_name"])
    ).not_to_be_visible()
    expect(
        cart_page.get_product_item_by_name(SECOND_EXAMPLE_PRODUCT["product_name"])
    ).to_be_visible()


@pytest.mark.regression
@pytest.mark.navigation
@pytest.mark.ui
@pytest.mark.parametrize(
    "_case_id",
    ["TC-CART-011"],
    ids=["TC-CART-011"],
)
def test_product_details_can_be_opened_from_cart_item_name(
    inventory_page_with_one_product_in_cart: tuple[InventoryPage, dict[str, str]],
    _case_id: str,
):
    inventory_page, product = inventory_page_with_one_product_in_cart
    cart_page = inventory_page.open_cart()
    product_details_page = cart_page.open_product_details_by_name(product["product_name"])

    expect(product_details_page.page).to_have_url(
        f"{ProductDetailsPage.URL}{product['product_id']}"
    )
    expect(product_details_page.get_product_item_or_items()).to_be_visible()
    expect(product_details_page.get_back_to_products_button()).to_be_visible()


@pytest.mark.regression
@pytest.mark.navigation
@pytest.mark.ui
@pytest.mark.parametrize(
    "_case_id",
    ["TC-CART-012"],
    ids=["TC-CART-012"],
)
def test_continue_shopping_preserves_cart_state(
    inventory_page_with_one_product_in_cart: tuple[InventoryPage, dict[str, str]],
    _case_id: str,
):
    inventory_page, product = inventory_page_with_one_product_in_cart
    product_card = inventory_page.get_product_item_by_name(product["product_name"])
    optional_product_card = inventory_page.get_product_item_by_name(
        SECOND_EXAMPLE_PRODUCT["product_name"]
    )

    cart_page = inventory_page.open_cart()
    inventory_page = cart_page.continue_shopping()

    expect(inventory_page.page).to_have_url(InventoryPage.URL)
    expect(inventory_page.get_inventory_container()).to_be_visible()
    expect(inventory_page.get_product_list()).to_be_visible()
    expect(inventory_page.get_shopping_cart_badge()).to_have_text("1")

    expect(inventory_page.get_remove_button_from_item(product_card)).to_be_visible()
    expect(inventory_page.get_add_to_cart_button_from_item(product_card)).not_to_be_visible()

    expect(inventory_page.get_add_to_cart_button_from_item(optional_product_card)).to_be_visible()
    expect(inventory_page.get_remove_button_from_item(optional_product_card)).not_to_be_visible()


@pytest.mark.regression
@pytest.mark.positive
@pytest.mark.ui
@pytest.mark.parametrize(
    "product",
    LIST_OF_PRODUCTS,
    ids=[f"TC-CART-013-{product['product_id']}" for product in LIST_OF_PRODUCTS],
)
def test_all_products_can_be_removed_from_cart(logged_in_inventory_page: InventoryPage, product):
    for item in LIST_OF_PRODUCTS:
        logged_in_inventory_page.add_product_to_cart(item["product_name"])

    cart_page = logged_in_inventory_page.open_cart()

    expect(cart_page.get_shopping_cart_badge()).to_have_text((str(len(LIST_OF_PRODUCTS))))
    cart_page.remove_product_from_cart(product["product_name"])

    expect(cart_page.get_shopping_cart_badge()).to_have_text((str(len(LIST_OF_PRODUCTS) - 1)))
    expect(cart_page.get_product_item_by_name(product["product_name"])).not_to_be_visible()


@pytest.mark.smoke
@pytest.mark.navigation
@pytest.mark.ui
@pytest.mark.parametrize(
    "_case_id",
    ["TC-CART-014"],
    ids=["TC-CART-014"],
)
def test_checkout_button_opens_checkout_information_page_with_product_in_cart(
    cart_page_with_one_product: tuple[CartPage, dict[str, str]],
    _case_id: str,
):
    cart_page = cart_page_with_one_product[0]
    checkout_step_one = cart_page.checkout()
    expect(checkout_step_one.page).to_have_url(CheckoutInformationPage.URL)
    expect(checkout_step_one.get_checkout_info_block()).to_be_visible()
    expect(cart_page.get_cart_contents_container()).not_to_be_visible()
