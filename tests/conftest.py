import pytest
import requests

from tests.config import USER_URL, AUTH_USER_URL, REGISTER_USER_URL
from tests.test_data import user_1_username, user_2_username, user_3_username, password, new_password, new_name, \
    new_email


def clear_users():
    for user in [user_1_username, user_2_username, user_3_username]:
        body = {
            "email": f"{user}@mail.ru",
            "name": user,
            "password": password
        }
        resp = requests.post(AUTH_USER_URL, body)
        if resp.status_code == 200:
            headers = {'Authorization': resp.json()['accessToken']}
            resp = requests.delete(USER_URL, headers=headers)

    body = {
        "email": new_email,
        "name": new_name,
        "password": new_password
    }
    resp = requests.post(AUTH_USER_URL, body)
    if resp.status_code == 200:
        headers = {'Authorization': resp.json()['accessToken']}
        resp = requests.delete(USER_URL, headers=headers)
        pass


@pytest.fixture(scope="class")
def clean_data_before_and_after_test():
    clear_users()
    yield
    clear_users()


@pytest.fixture(scope="class")
def create_new_user_before_test_and_clear_after():
    body = {
        "email": f"{user_1_username}@mail.ru",
        "password": password,
        "name": user_1_username
    }
    resp = requests.post(REGISTER_USER_URL, body)
    yield
    clear_users()
