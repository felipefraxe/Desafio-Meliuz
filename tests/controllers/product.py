import pytest
from unittest.mock import patch
from flask import Flask
from src.controllers.product import products_bp


@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(products_bp)

    with app.test_client() as client:
        yield client


def test_get_recommendations_success(client):
    mock_data = [
        {
            "product_id": 1,
            "product_title": "Product A",
            "product_price": 100,
            "store_name": "Store 1",
        },
        {
            "product_id": 2,
            "product_title": "Product B",
            "product_price": 45,
            "store_name": "Store 3",
        },
    ]

    with patch("services.product.fetch_top_k_recommended", return_value=mock_data):
        response = client.get("/recommend/1")

        assert response.status_code == 200

        assert response.json == mock_data


def test_get_recommendations_failure(client):
    with patch("services.product.fetch_top_k_recommended", side_effect=Exception("Service failed")):
        response = client.get("/recommend/1")


        assert response.status_code == 500

        assert response.json == {"error": "Erro interno do servidor: Service failed"}