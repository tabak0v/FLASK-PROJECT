from http import HTTPStatus
import requests
from application.tests.test_functions import ENDPOINT, create_contest, create_user_payload
import random


def test_create_contest():
    test_users = []
    for _ in range(3):
        payload = create_user_payload()
        create_response = requests.post(f"{ENDPOINT}/users/create", json=payload)
        assert create_response.status_code == HTTPStatus.OK
        test_users.append(create_response.json()["id"])
    payload = create_contest(3)
    create_response = requests.post(f"{ENDPOINT}/contests/create", json=payload)
    assert create_response.status_code == HTTPStatus.OK
    contest_data = create_response.json()
    assert contest_data["name"] == payload["name"]
    assert contest_data["sport"] == payload["sport"]
    assert contest_data["participants"] == payload["participants"]
    assert contest_data["status"] == "STARTED"
    assert contest_data["winner"] is None
    get_response = requests.get(f'{ENDPOINT}/contests/{contest_data["id"]}')
    assert get_response.json() == contest_data
    for user_id in test_users:
        delete_response = requests.delete(f"{ENDPOINT}/users/{user_id}")
        assert delete_response.status_code == HTTPStatus.OK


def test_create_contest_with_wrong_data():
    test_users = []
    for _ in range(3):
        payload = create_user_payload()
        create_response = requests.post(f"{ENDPOINT}/users/create", json=payload)
        assert create_response.status_code == HTTPStatus.OK
        test_users.append(create_response.json()["id"])
    payload = create_contest(3)
    payload["sport"] = "not_box"
    create_response = requests.post(f"{ENDPOINT}/contests/create", json=payload)
    assert create_response.status_code == HTTPStatus.BAD_REQUEST
    for user_id in test_users:
        delete_response = requests.delete(f"{ENDPOINT}/users/{user_id}")
        assert delete_response.status_code == HTTPStatus.OK


def test_finish_contest():
    test_users = []
    for _ in range(3):
        payload = create_user_payload()
        create_response = requests.post(f"{ENDPOINT}/users/create", json=payload)
        assert create_response.status_code == HTTPStatus.OK
        test_users.append(create_response.json()["id"])
    payload = create_contest(3)
    create_response = requests.post(f"{ENDPOINT}/contests/create", json=payload)
    assert create_response.status_code == HTTPStatus.OK
    winner = random.choice(payload["participants"])
    payload_post = {"winner": f"{winner}"}
    response = requests.post(
        f'{ENDPOINT}/contests/{create_response.json()["id"]}/finish', json=payload_post
    )
    assert response.status_code == HTTPStatus.OK
    contest_data = response.json()
    assert contest_data["name"] == payload["name"]
    assert contest_data["sport"] == payload["sport"]
    assert contest_data["status"] == "FINISHED"
    assert contest_data["participants"] == payload["participants"]
    assert contest_data["winner"] == f"{winner}"
    for user_id in test_users:
        delete_response = requests.delete(f"{ENDPOINT}/users/{user_id}")
        assert delete_response.status_code == HTTPStatus.OK
