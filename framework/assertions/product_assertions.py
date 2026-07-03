from playwright.sync_api import expect


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
) -> None:
    assert_product_text_content_is_displayed(
        page_object=page_object,
        product_item=product_item,
        product=product,
    )

    product_image = page_object.get_product_image_from_item(product_item)
    add_to_cart_button = page_object.get_add_to_cart_button_from_item(product_item)

    expect(product_image).to_be_visible()
    expect(product_image).to_have_attribute("src", product["product_image"])

    expect(add_to_cart_button).to_be_visible()


def assert_inventory_product_item_displays_expected_product(
    inventory_page,
    product: dict[str, str],
) -> None:
    product_item = inventory_page.get_product_item_by_name(product["product_name"])

    expect(product_item).to_have_count(1)

    assert_catalog_product_item_displays_expected_product(
        page_object=inventory_page,
        product_item=product_item,
        product=product,
    )


def assert_product_details_page_displays_expected_product(
    product_details_page,
    product: dict[str, str],
) -> None:
    product_item = product_details_page.get_product_item_or_items()

    expect(product_details_page.page).to_have_url(
        f"{product_details_page.URL}{product['product_id']}"
    )

    assert_catalog_product_item_displays_expected_product(
        page_object=product_details_page,
        product_item=product_item,
        product=product,
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


def convert_price_to_float(price: str) -> float:
    return float(price.replace("$", ""))
