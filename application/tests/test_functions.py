from uuid import uuid4
ENDPOINT = "http://127.0.0.1:5000"


def create_contest(users):
    payload = {
        "name": f"string {uuid4()}",
        "sport": "box",
        "participants": [_ for _ in range(users)],
    }
    return payload


def create_user_payload():
    payload = {
        "first_name": "Vasya" + str(uuid4()),
        "last_name": "Pupkin" + str(uuid4()),
        "email": "test@test.ru",
        "sport": "box",
    }
    return payload
