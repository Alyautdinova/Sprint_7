import requests
import pytest
import allure

from data.urls import Urls
from data.data_test import ORDER_PAYLOAD, ORDER_COLORS

class TestOrders:
    @allure.title('Создание заказа')
    @allure.description('Проверяем, что создается заказ с одним цветом/с двумя и без цвета самоката')
    @pytest.mark.parametrize("colors", ORDER_COLORS)
    def test_create_order(self, colors):

        with allure.step('Подготовка данных для создания заказа'):
            order_payload = {**ORDER_PAYLOAD, "color": colors}

        with allure.step('Создание заказа'):
            response = requests.post(Urls.CREATE_ORDER_ENDPOINT, json=order_payload)

        with allure.step('Проверка, что заказ создан'):
            assert response.status_code == 201
            assert "track" in response.json()

    @allure.title('Получение заказов')
    @allure.description('Проверяем, что заказы получены')
    def test_get_order(self, create_order):
        with allure.step('Получение заказов'):
            response = requests.get(Urls.CREATE_ORDER_ENDPOINT)

        with allure.step('Проверка, что заказы получены в ответе'):
            assert response.status_code == 200
            assert len(response.json()["orders"]) > 0
