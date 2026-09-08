from playwright.sync_api import expect

from pages.login_page import LoginPage
from test_data.checkout_test_data import (
    CHECKOUT_OVERVIEW_PAYMENT_INFO,
    CHECKOUT_OVERVIEW_SHIPPING_INFO,
    ITEM_TOTAL_PREFIX,
    TAX_PERCENTAGE,
    TAX_PREFIX,
    TOTAL_PREFIX,
)


def assert_failed_login_input_error_icons_are_displayed(
    login_page: LoginPage,
) -> None:
    username_input = login_page.get_username_input()
    password_input = login_page.get_password_input()

    username_input_parent = login_page.page.locator("div .form_group").filter(has=username_input)
    password_input_parent = login_page.page.locator("div .form_group").filter(has=password_input)

    expect(login_page.page).to_have_url(LoginPage.URL)
    expect(login_page.get_input_error_icon(username_input_parent)).to_be_visible()
    expect(login_page.get_input_error_icon(password_input_parent)).to_be_visible()


def assert_product_text_content_is_displayed(
    page_object,
    product_item,
    product: dict[str, str],
) -> None:
    expect(product_item).to_be_visible()

    product_name = page_object.get_product_name_from_item(product_item)
    product_description = page_object.get_product_description_from_item(product_item)
    product_price = page_object.get_product_price_from_item(product_item)

    expect(product_name).to_be_visible()
    expect(product_name).to_have_text(product["product_name"])

    expect(product_description).to_be_visible()
    expect(product_description).to_have_text(product["product_description"])

    expect(product_price).to_be_visible()
    expect(product_price).to_have_text(product["product_price"])


def assert_catalog_product_item_displays_expected_product(
    page_object,
    product_item,
    product: dict[str, str],
    is_added: bool = False,
) -> None:
    assert_product_text_content_is_displayed(
        page_object=page_object,
        product_item=product_item,
        product=product,
    )

    product_image = page_object.get_product_image_from_item(product_item)
    expect(product_image).to_be_visible()
    expect(product_image).to_have_attribute("src", product["product_image"])

    if not is_added:
        add_to_cart_button = page_object.get_add_to_cart_button_from_item(product_item)
        expect(add_to_cart_button).to_be_visible()

    if is_added:
        remove_from_cart_button = page_object.get_remove_button_from_item(product_item)
        expect(remove_from_cart_button).to_be_visible()


def assert_inventory_product_item_displays_expected_product(
    inventory_page,
    product: dict[str, str],
    is_added: bool = False,
) -> None:
    product_item = inventory_page.get_product_item_by_name(product["product_name"])

    expect(product_item).to_have_count(1)

    assert_catalog_product_item_displays_expected_product(
        page_object=inventory_page,
        product_item=product_item,
        product=product,
        is_added=is_added,
    )


def assert_product_details_page_displays_expected_product(
    product_details_page,
    product: dict[str, str],
    is_added: bool = False,
) -> None:
    product_item = product_details_page.get_product_item_or_items()

    expect(product_details_page.page).to_have_url(
        f"{product_details_page.URL}{product['product_id']}"
    )

    assert_catalog_product_item_displays_expected_product(
        page_object=product_details_page,
        product_item=product_item,
        product=product,
        is_added=is_added,
    )


def assert_cart_product_item_displays_expected_product(
    cart_page,
    product: dict[str, str],
    expected_quantity: str = "1",
) -> None:
    product_item = cart_page.get_product_item_by_name(product["product_name"])

    expect(product_item).to_have_count(1)

    assert_product_text_content_is_displayed(
        page_object=cart_page,
        product_item=product_item,
        product=product,
    )

    product_quantity = cart_page.get_product_quantity_from_item(product_item)
    remove_button = cart_page.get_remove_button_from_item(product_item)

    expect(product_quantity).to_be_visible()
    expect(product_quantity).to_have_text(expected_quantity)

    expect(remove_button).to_be_visible()


def assert_checkout_product_item_displays_expected_product(
    checkout_overview_page,
    product: dict[str, str],
    expected_quantity: str = "1",
) -> None:
    product_item = checkout_overview_page.get_product_item_by_name(product["product_name"])

    expect(product_item).to_have_count(1)

    assert_product_text_content_is_displayed(
        page_object=checkout_overview_page,
        product_item=product_item,
        product=product,
    )

    product_quantity = checkout_overview_page.get_product_quantity_from_item(product_item)

    expect(product_quantity).to_be_visible()
    expect(product_quantity).to_have_text(expected_quantity)


def assert_checkout_overview_price_summary_displays_expected_info(
    checkout_overview_page, *products: tuple[dict[str, str], ...]
):
    expect(checkout_overview_page.get_payment_info_label()).to_be_visible()
    expect(checkout_overview_page.get_payment_info_value()).to_be_visible()
    expect(checkout_overview_page.get_payment_info_value()).to_have_text(
        CHECKOUT_OVERVIEW_PAYMENT_INFO
    )

    expect(checkout_overview_page.get_shipping_info_label()).to_be_visible()
    expect(checkout_overview_page.get_shipping_info_value()).to_be_visible()
    expect(checkout_overview_page.get_shipping_info_value()).to_have_text(
        CHECKOUT_OVERVIEW_SHIPPING_INFO
    )

    expect(checkout_overview_page.get_total_info_label()).to_be_visible()

    item_total_price = 0.00
    for product in products:
        item_total_price += convert_price_to_float(product["product_price"])
    conferted_item_total_price = format(item_total_price, ".2f")

    expect(checkout_overview_page.get_price_item_total_label()).to_be_visible()
    expect(checkout_overview_page.get_price_item_total_label()).to_have_text(
        ITEM_TOTAL_PREFIX + conferted_item_total_price
    )

    tax_price = calculate_tax_price(conferted_item_total_price, TAX_PERCENTAGE)
    expect(checkout_overview_page.get_price_tax_label()).to_be_visible()
    expect(checkout_overview_page.get_price_tax_label()).to_have_text(TAX_PREFIX + tax_price)

    final_total_price = calculate_final_price(conferted_item_total_price, tax_price)
    expect(checkout_overview_page.get_total_price_label()).to_be_visible()
    expect(checkout_overview_page.get_total_price_label()).to_have_text(
        TOTAL_PREFIX + final_total_price
    )


def convert_price_to_float(price: str) -> float:
    return float(price.replace("$", ""))


def calculate_tax_price(total_item_price: str, tax_percentage: int) -> str:
    return format(float(total_item_price) * tax_percentage / 100, ".2f")


def calculate_final_price(total_item_total: str, total_tax_price: str) -> str:
    final_price = float(total_item_total) + float(total_tax_price)
    return format(final_price, ".2f")
