from http import HTTPStatus
import requests
from application.tests.test_functions import ENDPOINT, create_user_payload


def test_user_create():
    payload = create_user_payload()
    create_response = requests.post(f"{ENDPOINT}/users/create", json=payload)
    assert create_response.status_code == HTTPStatus.OK
    user_data = create_response.json()
    user_id = user_data["id"]
    assert user_data["first_name"] == payload["first_name"]
    assert user_data["last_name"] == payload["last_name"]
    assert user_data["email"] == payload["email"]
    get_response = requests.get(f"{ENDPOINT}/users/{user_id}")
    assert get_response.json()["first_name"] == payload["first_name"]
    assert get_response.json()["last_name"] == payload["last_name"]
    assert get_response.json()["email"] == payload["email"]
    delete_response = requests.delete(f"{ENDPOINT}/users/{user_id}")
    assert delete_response.status_code == HTTPStatus.OK
    assert delete_response.json()["first_name"] == payload["first_name"]
    assert delete_response.json()["last_name"] == payload["last_name"]
    assert delete_response.json()["email"] == payload["email"]
    assert delete_response.json()["status"] == "deleted"


def test_user_create_valid_email():
    payload = create_user_payload()
    payload["email"] = "test.ru"
    create_response = requests.post(f"{ENDPOINT}/users/create", json=payload)
    assert create_response.status_code == HTTPStatus.BAD_REQUEST


def test_get_users_contests():
    payload = create_user_payload()
    create_response = requests.post(f"{ENDPOINT}/users/create", json=payload)
    assert create_response.status_code == HTTPStatus.OK
    user_data = create_response.json()
    user_id = user_data["id"]
    get_response = requests.get(f"{ENDPOINT}/users/{user_id}/contests")
    assert isinstance(get_response.json()["contests"], list)
    delete_response = requests.delete(f"{ENDPOINT}/users/{user_id}")
    assert delete_response.status_code == HTTPStatus.OK


def test_get_users_leaderboard():
    users = 3
    test_users = []
    for _ in range(users):
        payload = create_user_payload()
        create_response = requests.post(f"{ENDPOINT}/users/create", json=payload)
        assert create_response.status_code == HTTPStatus.OK
        test_users.append(create_response.json()["id"])
    payload = {"type": "list", "sort": "asc"}
    get_response = requests.get(f"{ENDPOINT}/users/leaderboard", json=payload)
    leaderboard = get_response.json()["users"]
    assert isinstance(leaderboard, list)
    assert len(leaderboard) == users
    for user_id in test_users:
        delete_response = requests.delete(f"{ENDPOINT}/users/{user_id}")
        assert delete_response.status_code == HTTPStatus.OK
