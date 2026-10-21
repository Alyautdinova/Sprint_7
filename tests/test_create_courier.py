import requests
import pytest

from data.urls import Urls

class TestCreateCourier:
    def test_create_new_courier(self, generate_login_data):
        payload = generate_login_data
        response = requests.post(Urls.CREATE_COURIER_ENDPOINT, json=payload)

        assert response.status_code == 201
        assert response.json() == {"ok": True}

    def test_create_two_idential_courier(self, generate_login_data):
        payload = generate_login_data
        response = requests.post(Urls.CREATE_COURIER_ENDPOINT, json=payload)

        assert response.status_code == 201

        response = requests.post(Urls.CREATE_COURIER_ENDPOINT, json=payload)
        assert response.status_code == 409
        assert response.json()["message"] == 'Этот логин уже используется. Попробуйте другой.'

    @pytest.mark.parametrize("missing_payload",
        [
            ({"password": "123", "firstName": "Farida"}),
            ({"login": "login", "firstName": "Farida"}),
            ({},)
        ]
    )
    def test_create_courier_missing_required_field_returns_error(self, missing_payload):
        response = requests.post(Urls.CREATE_COURIER_ENDPOINT, json=missing_payload)

        
        assert response.status_code == 400
        assert response.json()["message"] == 'Недостаточно данных для создания учетной записи'
    