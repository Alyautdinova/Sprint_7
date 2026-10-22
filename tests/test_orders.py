import requests
import pytest

from data.urls import Urls

class TestOrders:
    @pytest.mark.parametrize("colors",
        [
            ["BLACK"],
            ["GREY"],
            ["BLACK"],
            [],
        ]
    )
    def test_create_order(self, colors):
        order_payload = {
            "firstName": "Naruto",
            "lastName": "Uchiha",
            "address": "Konoha, 142 apt.",
            "metroStation": 4,
            "phone": "+7 800 355 35 35",
            "rentTime": 5,
            "deliveryDate": "2020-06-06",
            "comment": "Saske, come back to Konoha",
            "color": colors
        }

        response = requests.post(Urls.CREATE_ORDER_ENDPOINT, json=order_payload)

        assert response.status_code == 201
        assert "track" in response.json()

    def test_get_order(self, create_order):
        response = requests.get(Urls.CREATE_ORDER_ENDPOINT)
        
        assert response.status_code == 200
        assert len(response.json()["orders"]) > 0
