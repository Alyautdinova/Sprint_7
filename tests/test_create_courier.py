import requests
import pytest
import allure

from data.urls import Urls

class TestCreateCourier:

    @allure.title('Создание нового курьера')
    @allure.description('Проверяем, что запрос отдает 200 и True при создании курьера с валидными данными')
    def test_create_new_courier(self, generate_login_data):
        with allure.step('Подготовка данных для создании курьера'):
            payload = generate_login_data

        with allure.step('Создание курьера'):    
            response = requests.post(Urls.CREATE_COURIER_ENDPOINT, json=payload)

        with allure.step('Проверка, что создали курьера'):
            assert response.status_code == 201
            assert response.json() == {"ok": True}

    @allure.title('Создание курьера с данными существующими в системе')
    @allure.description('Проверяем, что запрос отдает 409 и ошибку при создании курьера с данными как у существующего курьера в системе')
    def test_create_two_idential_courier(self, register_new_courier):
        with allure.step('Создание второго курьера с такими же данными как первый курьер'):
            payload = register_new_courier
            response = requests.post(Urls.CREATE_COURIER_ENDPOINT, json=payload)

        with allure.step('Проверка, что курьер с данными, которые уже есть в системе, не создается'):  
            assert response.status_code == 409
            assert response.json()["message"] == 'Этот логин уже используется. Попробуйте другой.'

    @allure.title('Создание курьера без обязательных параметров')
    @allure.description('Проверяем, что запрос отдает 400 и ошибку при создании курьера без обязательных параметров')
    @pytest.mark.parametrize("missing_payload",
        [
            ({"password": "123", "firstName": "Farida"}),
            ({"login": "login", "firstName": "Farida"}),
            ({},)
        ]
    )
    def test_create_courier_missing_required_field_returns_error(self, missing_payload):
        with allure.step('Создание курьера без обязательных параметров'):  
            response = requests.post(Urls.CREATE_COURIER_ENDPOINT, json=missing_payload)

        with allure.step('Проверка, что курьер не создался'):
            assert response.status_code == 400
            assert response.json()["message"] == 'Недостаточно данных для создания учетной записи'
    