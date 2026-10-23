import requests
import pytest
import allure

from data.urls import Urls

class TestLoginCourier:

    @allure.title('Вход под существующим в системе курьером')
    @allure.description('Проверяем, что запрос отдает 200 и id курьера при входе под существующим в системе курьером')
    def test_login_success(self, register_new_courier_and_return_login_password):
        with allure.step('Подготовка данных для входа курьера'):
            courier_data = register_new_courier_and_return_login_password

            login_payload = {
                "login": courier_data[0],
                "password": courier_data[1]
            }

        with allure.step('Логин курьера'):
            response = requests.post(Urls.LOGIN_COURIER_ENDPOINT, json=login_payload)

        with allure.step('Проверка, что вошли под курьером'):
            assert response.status_code == 200
            assert "id" in response.json()

    @allure.title('Вход без обязательных параметров')
    @allure.description('Проверяем, что запрос отдает 400 и ошибку при попытке входа без обязательных параметров')
    @pytest.mark.parametrize("missing_payload",
        [
            ({"password": "1234"}),
            ({"login": "ninja"}),
            ({},)
        ]
    )
    def test_login_missing_required_fields_returns_error(self, missing_payload):
        with allure.step('Логин курьера'):
            response = requests.post(Urls.LOGIN_COURIER_ENDPOINT, json=missing_payload)

        with allure.step('Проверка, что не вошли под курьером'):
            assert response.status_code == 400
            assert response.json()["message"] == 'Недостаточно данных для входа'


    @allure.title('Вход без существующего логина в системе')
    @allure.description('Проверяем, что запрос отдает 404 и ошибку при попытке входа с несуществующим логином')
    def test_login_with_not_exist_login(self):
        
        with allure.step('Данные для входа курьера'):
            login_payload = {
                "login": "login",
                "password": "12345"
            }

        with allure.step('Логин курьера'):
            response = requests.post(Urls.LOGIN_COURIER_ENDPOINT, json=login_payload)

        with allure.step('Проверка, что не вошли под курьером'):
            assert response.status_code == 404
            assert response.json()["message"] == 'Учетная запись не найдена'

    @allure.title('Вход без существующего пароля в системе')
    @allure.description('Проверяем, что запрос отдает 404 и ошибку при попытке входа с несуществующим паролем')
    def test_login_with_not_exist_password(self, register_new_courier_and_return_login_password):

        with allure.step('Подготовка данных для входа курьера'):
            courier_data = register_new_courier_and_return_login_password
        
            login_payload = {
                "login": courier_data[0],
                "password": "test45678"
            }

        with allure.step('Логин курьера'):
            response = requests.post(Urls.LOGIN_COURIER_ENDPOINT, json=login_payload)

        with allure.step('Проверка, что не вошли под курьером'):
            assert response.status_code == 404
            assert response.json()["message"] == 'Учетная запись не найдена'
