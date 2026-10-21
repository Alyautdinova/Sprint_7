import random
import requests
import pytest
import string
from data.urls import Urls

@pytest.fixture
def courier_cleanup():

    # метод генерирует строку, состоящую только из букв нижнего регистра, в качестве параметра передаём длину строки
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
    