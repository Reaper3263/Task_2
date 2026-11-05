import allure
import pytest
import requests

from ..config import AUTH_USER_URL, GET_ORDERS_URL
from ..test_data import user_1_username, password


@pytest.mark.usefixtures('create_new_user_before_test_and_clear_after')
class TestGetOrders:
    @allure.title("Проверка заказа пользователя с авторизацией")
    def test_get_orders_with_auth(self):
        body = {
            "email": f"{user_1_username}@mail.ru",
            "name": user_1_username,
            "password": password
        }
        resp = requests.post(AUTH_USER_URL, body)
        headers = {'Authorization': resp.json()['accessToken']}

        resp_with_orders = requests.get(GET_ORDERS_URL, headers=headers)
        assert resp_with_orders.status_code == 200

    @allure.title("Проверка заказа пользователя без авторизации")
    def test_get_orders_without_auth(self):
        resp_with_orders = requests.get(GET_ORDERS_URL)
        assert resp_with_orders.json()['message'] == 'You should be authorised'