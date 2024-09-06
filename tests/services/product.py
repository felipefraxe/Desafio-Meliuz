import pytest
import pandas as pd
from unittest.mock import patch
from src.services.product import calculate_sales_slope, fetch_top_k_recommended


mock_data = pd.DataFrame({
    "sale_date": pd.to_datetime([
        "2024-01-01", "2024-02-01", "2024-03-01",
        "2024-01-01", "2024-02-01",
        "2024-01-01", "2024-02-01", "2024-03-01",
        "2024-01-01", "2024-02-01"
    ]),
    "product_id": [1, 1, 1, 1, 1, 2, 2, 2, 2, 2],
    "product_title": ["Product A", "Product A", "Product A", "Product A", "Product A", 
                      "Product B", "Product B", "Product B", "Product B", "Product B"],
    "product_price": [100, 100, 100, 95, 95, 50, 50, 50, 45, 45],
    "product_image_url": ["imgA", "imgA", "imgA", "imgA", "imgA", 
                          "imgB", "imgB", "imgB", "imgB", "imgB"],
    "store_name": ["Store 1", "Store 1", "Store 1", "Store 2", "Store 2", 
                   "Store 1", "Store 1", "Store 1", "Store 3", "Store 3"],
    "store_id": [1, 1, 1, 2, 2, 1, 1, 1, 3, 3],
    "sales_per_day": [10, 20, 30, 15, 15, 5, 10, 15, 10, 20]
})


@pytest.fixture
def mock_load_products():
    with patch("models.product.load_products", return_value=mock_data):
        yield mock_data


def test_calculate_sales_slope():
    sales_data = [10, 20, 30]
    slope = calculate_sales_slope(sales_data)
    assert slope > 0, "The slope should be positive for increasing sales."
    assert slope == pytest.approx(10, rel=1e-9), "The slope should be approximately 10."

    sales_data = [30, 20, 10]
    slope = calculate_sales_slope(sales_data)
    assert slope < 0, "The slope should be negative for decreasing sales."
    assert slope == pytest.approx(-10, rel=1e-9), "The slope should be approximately -10."

    sales_data = [10, 10, 10]
    slope = calculate_sales_slope(sales_data)
    assert slope == 0, "The slope should be zero for flat sales."

    sales_data = [10]
    slope = calculate_sales_slope(sales_data)
    assert slope == 0, "The slope should be zero if there are fewer than 3 months of data."


def test_fetch_top_k_recommended(mock_load_products):
    result = fetch_top_k_recommended(k=2)

    assert len(result) == 1, "The function should return exactly 1 product."
    
    assert result[0]["product_id"] == 1, "Product A should be returned."
    
    assert result[0]["store_name"] == "Store 2", "Store 2 should correspond to the minimum price for Product A."


def test_sales_slope_filtering(mock_load_products):
    result = fetch_top_k_recommended(k=3)
    
    for product in result:
        assert product["product_price"] >= 0, "All products should have positive sales growth."


def test_less_than_k_products(mock_load_products):
    result = fetch_top_k_recommended(k=10)

    assert len(result) <= 10, "The result should contain the available products if less than k."
