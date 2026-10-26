import shutil
from pathlib import Path

import pytest
from playwright.sync_api import Page, expect

from framework.visual_regression import compare_png_images
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from test_data.login_test_data import VALID_USER_CASES
from test_data.product_test_data import LIST_OF_PRODUCTS

pytestmark = pytest.mark.visual

PROJECT_ROOT = Path(__file__).resolve().parents[1]
BASELINES_DIR = PROJECT_ROOT / "visual_baselines" / "chromium"
ACTUAL_DIR = PROJECT_ROOT / "reports" / "visual" / "actual"
DIFF_DIR = PROJECT_ROOT / "reports" / "visual" / "diff"
MAX_DIFFERENT_PIXELS = 10

BACKPACK_NAME = "Sauce Labs Backpack"


def _capture_and_compare(
    page: Page,
    filename: str,
    update_baselines: bool,
) -> None:
    baseline_path = BASELINES_DIR / filename
    actual_path = ACTUAL_DIR / filename
    diff_path = DIFF_DIR / filename

    actual_path.parent.mkdir(parents=True, exist_ok=True)
    diff_path.unlink(missing_ok=True)

    page.screenshot(
        path=str(actual_path),
        type="png",
        full_page=False,
        animations="disabled",
        caret="hide",
        scale="css",
    )

    if update_baselines:
        baseline_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(actual_path, baseline_path)
        return

    compare_png_images(
        baseline_path,
        actual_path,
        diff_path,
        max_different_pixels=MAX_DIFFERENT_PIXELS,
    )


def _login_as_standard_user(page: Page) -> InventoryPage:
    user = VALID_USER_CASES[0]

    login_page = LoginPage(page)
    login_page.open()
    login_page.login(user["username"], user["password"])

    inventory_page = InventoryPage(page)

    expect(page).to_have_url(InventoryPage.build_url())
    expect(inventory_page.get_product_list()).to_be_visible()
    expect(inventory_page.get_product_item_or_items()).to_have_count(len(LIST_OF_PRODUCTS))

    inventory_page.get_product_list().locator("img").evaluate_all(
        "(images) => Promise.all(images.map(image => image.decode()))"
    )

    return inventory_page


def test_inventory_default_visual_checkpoint(
    page: Page,
    update_visual_baselines: bool,
) -> None:
    _login_as_standard_user(page)

    _capture_and_compare(
        page,
        "inventory-default.png",
        update_visual_baselines,
    )


def test_cart_one_product_visual_checkpoint(
    page: Page,
    update_visual_baselines: bool,
) -> None:
    inventory_page = _login_as_standard_user(page)

    inventory_page.add_product_to_cart(BACKPACK_NAME)
    cart_page = inventory_page.open_cart()

    expect(page).to_have_url(cart_page.build_url())
    expect(cart_page.get_product_item_by_name(BACKPACK_NAME)).to_be_visible()
    expect(cart_page.get_shopping_cart_badge()).to_have_text("1")

    _capture_and_compare(
        page,
        "cart-one-product.png",
        update_visual_baselines,
    )
