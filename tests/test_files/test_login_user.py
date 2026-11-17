import allure
import pytest
import requests

from ..config import AUTH_USER_URL
from ..test_data import user_1_username, password


@pytest.mark.usefixtures('create_new_user_before_test_and_clear_after')
class TestLoginUsers:
    @allure.title("Успешная авторизация нового пользователя")
    def test_success_login(self):
        body = {
            "email": f"{user_1_username}@mail.ru",
            "name": user_1_username,
            "password": password
        }
        resp = requests.post(AUTH_USER_URL, body)
        assert resp.status_code == 200

    @allure.title("Неуспешная авторизация нового пользователя")
    def test_fail_login(self):
        body = {
            "email": f"{user_1_username}@mail.ru",
            "name": user_1_username,
            "password": password + "123"
        }
        resp = requests.post(AUTH_USER_URL, body)
        assert resp.json()['message'] == 'email or password are incorrect'
