import allure
import pytest
import requests

from ..config import USER_URL, AUTH_USER_URL
from ..test_data import user_1_username, password, new_password, new_name, new_email, user_1_email


@pytest.mark.usefixtures('create_new_user_before_test_and_clear_after')
class TestChangingInfo:
    @allure.title("Попытка изменить данные пользователя с авторизацией")
    @pytest.mark.parametrize(
        "auth_email, auth_name, auth_password, field_to_change, new_value",
        [
            (user_1_email, user_1_username, password, "email", new_email),
            (new_email, user_1_username, password, "name", new_name),
            (new_email, new_name, password, "password", new_password),
        ],
        ids=["change_email", "change_name", "change_password"]
    )
    def test_change_user_data_with_auth(self, auth_email, auth_name, auth_password, field_to_change, new_value):
        body = {
            "email": auth_email,
            "name": auth_name,
            "password": auth_password
        }
        resp = requests.post(AUTH_USER_URL, json=body)
        headers = {'Authorization': resp.json()['accessToken']}

        body_for_patch = {
            field_to_change: new_value
        }
        resp_with_user_data = requests.patch(USER_URL, headers=headers, json=body_for_patch)

        assert resp_with_user_data.status_code == 200

    @allure.title("Попытка изменить почту пользователя без авторизации")
    def test_change_email_without_auth(self):
        body_for_patch = {
            "email": "test@mail.ru"
        }
        resp_with_user_data = requests.patch(USER_URL, data=body_for_patch)
        assert resp_with_user_data.json()['message'] == 'You should be authorised'