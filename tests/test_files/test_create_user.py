import allure
import pytest
import requests

from ..config import REGISTER_USER_URL
from ..test_data import user_1_username, password


@pytest.mark.usefixtures("clean_data_before_and_after_test")
class TestCreateUser:
    @allure.title("Успешная регистрация нового пользователя")
    def test_create_unic_user(self):
        body = {
            "email": f"{user_1_username}@mail.ru",
            "password": password,
            "name": user_1_username
        }
        resp = requests.post(REGISTER_USER_URL, body)
        assert resp.status_code == 200

    @allure.title("Регистрация пользователя с дублирующимся логином возвращает ошибку")
    def test_create_two_same_username_returns_conflict_message(self):
        body = {
            "email": f"{user_1_username}@mail.ru",
            "password": password,
            "name": user_1_username
        }
        with allure.step("Создание первого курьера"):
            requests.post(REGISTER_USER_URL, data=body)
        with allure.step("Повторная попытка создания курьера с тем же логином"):
            resp_repeated = requests.post(REGISTER_USER_URL, data=body)

        with allure.step("Проверка сообщения о занятом логине"):
            assert resp_repeated.json().get('message') == 'User already exists'

    @allure.title("Регистрация пользователя без пароля возвращает ошибку")
    def test_create_user_without_password_returns_bad_request_message(self):
        body = {
            "email": f"{user_1_username}@mail.ru",
            "password": "",
            "name": user_1_username
        }
        with allure.step("Создание курьера без передачи обязательного поля password"):
            resp = requests.post(REGISTER_USER_URL, data=body)

        with allure.step("Проверка сообщения о недостаточном количестве данных"):
            assert resp.json().get('message') == 'Email, password and name are required fields'
