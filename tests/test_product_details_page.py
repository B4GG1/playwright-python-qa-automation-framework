import pytest
from playwright.sync_api import Locator, expect

from pages.inventory_page import InventoryPage
from pages.product_details_page import ProductDetailsPage
from test_data.product_test_data import LIST_OF_PRODUCTS

FIRST_EXAMPLE_PRODUCT = LIST_OF_PRODUCTS[0]


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


def _assert_product_details_page_displays_expected_product(
    product_details: ProductDetailsPage, product
) -> None:
    product_item = product_details.get_product_item()

    expect(product_details.page).to_have_url(f"{product_details.URL}{product['product_id']}")

    _assert_product_content_is_displayed(
        product_name=product_details.get_product_name_from_item(product_item),
        product_description=product_details.get_product_description_from_item(product_item),
        product_price=product_details.get_product_price_from_item(product_item),
        product_image=product_details.get_product_image_from_item(product_item),
        add_to_cart_button=product_details.get_add_to_cart_button_from_item(product_item),
        product=product,
    )


@pytest.mark.smoke
@pytest.mark.ui
@pytest.mark.parametrize(
    "_case_id",
    ["TC-PRODUCT-DETAILS-001"],
    ids=["TC-PRODUCT-DETAILS-001"],
)
def test_product_details_content_is_displayed_for_selected_product(
    logged_in_inventory_page: InventoryPage, _case_id: str
):
    product_details = logged_in_inventory_page.open_product_details_by_name(
        FIRST_EXAMPLE_PRODUCT["product_name"]
    )

    _assert_product_details_page_displays_expected_product(
        product_details=product_details,
        product=FIRST_EXAMPLE_PRODUCT,
    )

    expect(product_details.get_back_to_products_button()).to_be_visible()


@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.parametrize(
    "product",
    LIST_OF_PRODUCTS,
    ids=[f"TC-PRODUCT-DETAILS-002-{product['product_id']}" for product in LIST_OF_PRODUCTS],
)
def test_product_details_content_matches_product_data_for_each_product(
    logged_in_inventory_page: InventoryPage, product
):
    product_details = logged_in_inventory_page.open_product_details_by_name(product["product_name"])

    _assert_product_details_page_displays_expected_product(
        product_details=product_details,
        product=product,
    )

    expect(product_details.get_back_to_products_button()).to_be_visible()


@pytest.mark.regression
@pytest.mark.navigation
@pytest.mark.ui
@pytest.mark.parametrize(
    "_case_id",
    ["TC-PRODUCT-DETAILS-003"],
    ids=["TC-PRODUCT-DETAILS-003"],
)
def test_return_from_product_details_to_inventory_page(
    logged_in_inventory_page: InventoryPage, _case_id: str
):
    product = FIRST_EXAMPLE_PRODUCT

    product_details = logged_in_inventory_page.open_product_details_by_name(product["product_name"])

    expect(product_details.page).to_have_url(f"{product_details.URL}{product['product_id']}")

    inventory_page = product_details.return_to_inventory()

    expect(inventory_page.page).to_have_url(InventoryPage.URL)
    expect(inventory_page.get_inventory_container()).to_be_visible()
    expect(inventory_page.get_product_list()).to_be_visible()


@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.parametrize(
    "_case_id",
    ["TC-PRODUCT-DETAILS-004"],
    ids=["TC-PRODUCT-DETAILS-004"],
)
def test_add_to_cart_button_changes_to_remove_after_adding_product_from_details_page(
    logged_in_inventory_page: InventoryPage, _case_id: str
):
    details_page = logged_in_inventory_page.open_product_details_by_name(
        FIRST_EXAMPLE_PRODUCT["product_name"]
    )
    product_item = details_page.get_product_item()

    expect(details_page.get_remove_button_from_item(product_item)).to_be_hidden()
    expect(details_page.get_add_to_cart_button_from_item(product_item)).to_be_visible()

    details_page.add_product_to_cart()

    expect(details_page.get_remove_button_from_item(product_item)).to_be_visible()
    expect(details_page.get_add_to_cart_button_from_item(product_item)).to_be_hidden()

    expect(details_page.page).to_have_url(
        f'{ProductDetailsPage.URL}{FIRST_EXAMPLE_PRODUCT["product_id"]}'
    )
