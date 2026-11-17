import allure
import pytest
import requests

from ..config import AUTH_USER_URL, CREATE_ORDER_URL
from ..test_data import user_1_username, password


@pytest.mark.usefixtures('create_new_user_before_test_and_clear_after')
class TestCreateOrders:
    @allure.title("Создание заказа с авторизацией")
    def test_create_success_order_with_auth(self):
        body = {
            "email": f"{user_1_username}@mail.ru",
            "name": user_1_username,
            "password": password
        }
        resp = requests.post(AUTH_USER_URL, body)
        headers = {'Authorization': resp.json()['accessToken']}
        body = {
            "ingredients": ['6ae327a87e8698001b542b38', '6ae327a87e8698001b542b3f', '6ae327a87e8698001b542b42']
        }

        resp_with_order = requests.post(CREATE_ORDER_URL, headers=headers, data=body)
        assert resp_with_order.status_code == 200

    @allure.title("Создание заказа без авторизации")
    def test_create_success_order_without_auth(self):
        body = {
            "ingredients": ['6ae327a87e8698001b542b38', '6ae327a87e8698001b542b3f', '6ae327a87e8698001b542b42']
        }

        resp_with_order = requests.post(CREATE_ORDER_URL, data=body)
        assert resp_with_order.status_code == 200

    @allure.title("Создание заказа без ингредиентов")
    def test_create_success_order_without_ingredients(self):
        body = {
            "email": f"{user_1_username}@mail.ru",
            "name": user_1_username,
            "password": password
        }
        resp = requests.post(AUTH_USER_URL, body)
        headers = {'Authorization': resp.json()['accessToken']}
        body = {
            "ingredients": []
        }

        resp_with_order = requests.post(CREATE_ORDER_URL, headers=headers, data=body)
        assert resp_with_order.json()['message'] == 'Ingredient ids must be provided'

    @allure.title("Создание заказа с некорректными ингридентами")
    def test_create_fail_order_with_incorrect_ingredients(self):
        body = {
            "email": f"{user_1_username}@mail.ru",
            "name": user_1_username,
            "password": password
        }
        resp = requests.post(AUTH_USER_URL, body)
        headers = {'Authorization': resp.json()['accessToken']}
        body = {
            "ingredients": ['6ae327a87e8698231312001b542b38', '6ae327a87e8sdasd698001b542b3f', '6ae3ds27a87e869800gfsdgsdb542b42']
        }

        resp_with_order = requests.post(CREATE_ORDER_URL, headers=headers, data=body)
        assert resp_with_order.status_code == 500