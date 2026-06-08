import pytest
from playwright.sync_api import expect

from pages.inventory_page import InventoryPage


@pytest.mark.smoke
@pytest.mark.ui
@pytest.mark.positive
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
