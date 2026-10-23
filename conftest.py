import random
import requests
import pytest
import string
from data.urls import Urls

# фикстура для удаления курьера
@pytest.fixture
def courier_cleanup():
    payload = {}
        
    # Передаем данные в тест
    yield payload

    # После тестов удаляем курьера
    # 1. Логинимся, чтобы получить id созданного курьера
    login_data = {"login": payload["login"], "password": payload["password"]}
    login_response = requests.post(Urls.LOGIN_COURIER_ENDPOINT, json=login_data)
        
    if login_response.status_code == 200:
        courier_id = login_response.json().get("id")
            
        # 2. Удаляем курьера по его id
        if courier_id:
            requests.delete(f"{Urls.DELETE_COURIER_ENDPOINT}{courier_id}")

# фикстуры для генерации данных курьера и его удаление
@pytest.fixture
def generate_login_data(courier_cleanup):
    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string

    # генерируем логин, пароль и имя курьера
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)
    
    # собираем тело запроса
    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
        }
    
    courier_cleanup.update(payload)

    return payload

# фикстура для создания курьера и его удаление
@pytest.fixture
def register_new_courier_and_return_login_password(generate_login_data, courier_cleanup):

    payload = generate_login_data
    login_pass = []

    # отправляем запрос на регистрацию курьера и сохраняем ответ в переменную response
    response = requests.post(Urls.CREATE_COURIER_ENDPOINT, data=payload)

    # если регистрация прошла успешно (код ответа 201), добавляем в список логин и пароль курьера
    if response.status_code == 201:
        login_pass.append(payload["login"])
        login_pass.append(payload["password"])
        login_pass.append(payload["firstName"])
        
    
    courier_cleanup.update(payload)

    return login_pass

# фикстура для создание заказа
@pytest.fixture
def create_order():
    order_payload = {
            "firstName": "Naruto",
            "lastName": "Uchiha",
            "address": "Konoha, 142 apt.",
            "metroStation": 4,
            "phone": "+7 800 355 35 35",
            "rentTime": 5,
            "deliveryDate": "2020-06-06",
            "comment": "Saske, come back to Konoha",
            "color": ["BLACK"]
    }

    response = requests.post(Urls.CREATE_ORDER_ENDPOINT, json=order_payload)

    assert response.status_code == 201
    