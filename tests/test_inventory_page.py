import pytest
from playwright.sync_api import Locator, expect

from pages.inventory_page import InventoryPage
from pages.product_details_page import ProductDetailsPage
from test_data.inventory_test_data import LIST_OF_PRODUCTS


def _assert_product_content_is_displayed(
    product_name: Locator,
    product_description: Locator,
    product_price: Locator,
    product_image: Locator,
    add_to_cart_button: Locator,
    product,
) -> None:
    expect(product_name).to_be_visible()
    expect(product_name).to_have_text(product["product_name"])

    expect(product_description).to_be_visible()
    expect(product_description).to_have_text(product["product_description"])

    expect(product_price).to_be_visible()
    expect(product_price).to_have_text(product["product_price"])

    expect(product_image).to_be_visible()
    expect(product_image).to_have_attribute("src", product["product_image"])

    expect(add_to_cart_button).to_be_visible()


def _assert_inventory_product_card_displays_expected_product(
    inventory_page: InventoryPage, product
) -> None:
    actual_product = inventory_page.get_product_card_by_name(product["product_name"])

    expect(actual_product).to_have_count(1)
    expect(actual_product).to_be_visible()

    _assert_product_content_is_displayed(
        product_name=inventory_page.get_product_name_from_card(actual_product),
        product_description=inventory_page.get_product_description_from_card(actual_product),
        product_price=inventory_page.get_product_price_from_card(actual_product),
        product_image=inventory_page.get_product_image_from_card(actual_product),
        add_to_cart_button=inventory_page.get_add_to_cart_button_from_card(actual_product),
        product=product,
    )


def _assert_product_details_page_displays_expected_product(
    product_details: ProductDetailsPage, product
) -> None:
    expect(product_details.page).to_have_url(f"{product_details.URL}{product['product_id']}")

    _assert_product_content_is_displayed(
        product_name=product_details.get_product_name(),
        product_description=product_details.get_product_description(),
        product_price=product_details.get_product_price(),
        product_image=product_details.get_product_image(),
        add_to_cart_button=product_details.get_add_to_cart_button(),
        product=product,
    )


@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.ui
@pytest.mark.parametrize(
    "_case_id",
    ["TC-INVENTORY-001"],
    ids=["TC-INVENTORY-001"],
)
def test_inventory_page_is_visible_after_successful_login(
    logged_in_inventory_page: InventoryPage, _case_id: str
):
    expect(logged_in_inventory_page.page).to_have_url(InventoryPage.URL)
    expect(logged_in_inventory_page.get_inventory_container()).to_be_visible()
    expect(logged_in_inventory_page.get_product_list()).to_be_visible()


@pytest.mark.smoke
@pytest.mark.ui
@pytest.mark.parametrize(
    "_case_id",
    ["TC-INVENTORY-002"],
    ids=["TC-INVENTORY-002"],
)
def test_product_list_is_displayed_with_expected_products(
    logged_in_inventory_page: InventoryPage, _case_id: str
):
    expected_product_names = [product["product_name"] for product in LIST_OF_PRODUCTS]

    actual_product_names = logged_in_inventory_page.get_product_names()

    expect(logged_in_inventory_page.get_product_list()).to_be_visible()
    expect(logged_in_inventory_page.get_product_cards()).to_have_count(len(LIST_OF_PRODUCTS))
    assert set(actual_product_names) == set(expected_product_names), (
        f"Expected product names: {expected_product_names}, " f"but got: {actual_product_names}"
    )


@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.parametrize(
    "product",
    LIST_OF_PRODUCTS,
    ids=[f"TC-INVENTORY-003-{product['product_id']}" for product in LIST_OF_PRODUCTS],
)
def test_product_card_elements_are_displayed(logged_in_inventory_page: InventoryPage, product):
    _assert_inventory_product_card_displays_expected_product(
        inventory_page=logged_in_inventory_page,
        product=product,
    )


@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.positive
@pytest.mark.parametrize(
    "product",
    LIST_OF_PRODUCTS,
    ids=[f"TC-INVENTORY-004-{product['product_id']}" for product in LIST_OF_PRODUCTS],
)
def test_product_details_opened_from_product_name(logged_in_inventory_page: InventoryPage, product):
    product_details = logged_in_inventory_page.open_product_details_by_name(product["product_name"])

    _assert_product_details_page_displays_expected_product(product_details, product)

    expect(product_details.get_back_to_products_button()).to_be_visible()


@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.positive
@pytest.mark.parametrize(
    "product",
    LIST_OF_PRODUCTS,
    ids=[f"TC-INVENTORY-005-{product['product_id']}" for product in LIST_OF_PRODUCTS],
)
def test_product_details_opened_from_product_image(
    logged_in_inventory_page: InventoryPage, product
):
    product_details = logged_in_inventory_page.open_product_details_by_image(
        product["product_name"]
    )

    _assert_product_details_page_displays_expected_product(product_details, product)

    expect(product_details.get_back_to_products_button()).to_be_visible()


@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.positive
@pytest.mark.parametrize(
    "_case_id",
    ["TC-INVENTORY-006"],
    ids=["TC-INVENTORY-006"],
)
def test_return_from_product_details_to_inventory_page(
    logged_in_inventory_page: InventoryPage, _case_id: str
):
    product = LIST_OF_PRODUCTS[0]
    product_details = logged_in_inventory_page.open_product_details_by_name(product["product_name"])

    expect(product_details.page).to_have_url(f"{product_details.URL}{product['product_id']}")

    product_details.return_to_inventory()

    expect(logged_in_inventory_page.page).to_have_url(InventoryPage.URL)
    expect(logged_in_inventory_page.get_inventory_container()).to_be_visible()
    expect(logged_in_inventory_page.get_product_list()).to_be_visible()


@pytest.mark.sorting
@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.parametrize(
    "_case_id",
    ["TC-INVENTORY-007"],
    ids=["TC-INVENTORY-007"],
)
def test_sorting_products_by_name_a_to_z(logged_in_inventory_page: InventoryPage, _case_id: str):
    sorted_product_names = sorted(product["product_name"] for product in LIST_OF_PRODUCTS)
    logged_in_inventory_page.sort_products_by(InventoryPage.SORT_NAME_ASC)
    actual_product_names = logged_in_inventory_page.get_product_names()
    assert sorted_product_names == actual_product_names, (
        f"Expected product names order: {sorted_product_names}, " f"but got: {actual_product_names}"
    )


def _convert_price_to_float(price: str) -> float:
    return float(price.replace("$", ""))


@pytest.mark.sorting
@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.parametrize(
    "_case_id",
    ["TC-INVENTORY-008"],
    ids=["TC-INVENTORY-008"],
)
def test_sorting_products_by_name_z_to_a(logged_in_inventory_page: InventoryPage, _case_id: str):
    sorted_product_names = sorted(
        (product["product_name"] for product in LIST_OF_PRODUCTS), reverse=True
    )
    logged_in_inventory_page.sort_products_by(InventoryPage.SORT_NAME_DESC)
    actual_product_names = logged_in_inventory_page.get_product_names()
    assert sorted_product_names == actual_product_names, (
        f"Expected product names order: {sorted_product_names}, " f"but got: {actual_product_names}"
    )


@pytest.mark.sorting
@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.parametrize(
    "_case_id",
    ["TC-INVENTORY-009"],
    ids=["TC-INVENTORY-009"],
)
def test_sorting_products_by_price_low_to_high(
    logged_in_inventory_page: InventoryPage, _case_id: str
):
    sorted_product_prices = sorted(
        _convert_price_to_float(product["product_price"]) for product in LIST_OF_PRODUCTS
    )
    logged_in_inventory_page.sort_products_by(InventoryPage.SORT_PRICE_LOW_HIGH)
    actual_product_prices = [
        _convert_price_to_float(price) for price in logged_in_inventory_page.get_product_prices()
    ]
    assert sorted_product_prices == actual_product_prices, (
        f"Expected product prices order: {sorted_product_prices}, "
        f"but got: {actual_product_prices}"
    )


@pytest.mark.sorting
@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.parametrize(
    "_case_id",
    ["TC-INVENTORY-010"],
    ids=["TC-INVENTORY-010"],
)
def test_sorting_products_by_price_high_to_low(
    logged_in_inventory_page: InventoryPage, _case_id: str
):
    sorted_product_prices = sorted(
        (_convert_price_to_float(product["product_price"]) for product in LIST_OF_PRODUCTS),
        reverse=True,
    )
    logged_in_inventory_page.sort_products_by(InventoryPage.SORT_PRICE_HIGH_LOW)
    actual_product_prices = [
        _convert_price_to_float(price) for price in logged_in_inventory_page.get_product_prices()
    ]
    assert sorted_product_prices == actual_product_prices, (
        f"Expected product prices order: {sorted_product_prices}, "
        f"but got: {actual_product_prices}"
    )
