import requests
import pytest

from data.urls import Urls

class TestLoginCourier:
    def test_login_success(self, register_new_courier_and_return_login_password):
        
        courier_data = register_new_courier_and_return_login_password

        login_payload = {
            "login": courier_data[0],
            "password": courier_data[1]
        }

        response = requests.post(Urls.LOGIN_COURIER_ENDPOINT, json=login_payload)

        assert response.status_code == 200
        assert "id" in response.json()

    @pytest.mark.parametrize("missing_payload",
        [
            ({"password": "1234"}),
            ({"login": "ninja"}),
            ({},)
        ]
    )
    def test_login_missing_required_fields_returns_error(self, missing_payload):
        response = requests.post(Urls.LOGIN_COURIER_ENDPOINT, json=missing_payload)

        assert response.status_code == 400
        assert response.json()["message"] == 'Недостаточно данных для входа'

    def test_login_with_not_exist_login(self):
        
        login_payload = {
            "login": "login",
            "password": "12345"
        }

        response = requests.post(Urls.LOGIN_COURIER_ENDPOINT, json=login_payload)

        assert response.status_code == 404
        assert response.json()["message"] == 'Учетная запись не найдена'

    def test_login_with_not_exist_password(self, register_new_courier_and_return_login_password):
        
        courier_data = register_new_courier_and_return_login_password
        
        login_payload = {
            "login": courier_data[0],
            "password": "test45678"
        }

        response = requests.post(Urls.LOGIN_COURIER_ENDPOINT, json=login_payload)

        assert response.status_code == 404
        assert response.json()["message"] == 'Учетная запись не найдена'
