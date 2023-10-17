from application import app, models, USERS, CONT
from flask import request, Response, url_for
import json
from http import HTTPStatus
import matplotlib.pyplot as plt
import matplotlib


@app.post("/users/create")
def create_user():
    data = request.get_json()
    user_id = len(USERS)
    first_name = data["first_name"]
    last_name = data["last_name"]
    email = data["email"]
    sport = data["sport"]
    if not models.User.is_valid_email(email):
        return Response(status=HTTPStatus.BAD_REQUEST)
    user = models.User(user_id, first_name, last_name, email, sport)
    USERS.append(user)
    response = Response(
        json.dumps(
            {
                "id": user.id,
                "first_name": user.first_name,
                "last name": user.last_name,
                "email": user.email,
                "contests": user.contests,
            }
        ),
        HTTPStatus.OK,
        mimetype="application/json",
    )
    return response


@app.get("/users/<int:user_id>")
def get_user(user_id):
    user = USERS[user_id]
    if not models.User.is_valid_id(user_id):
        return Response(status=HTTPStatus.NOT_FOUND)
    response = Response(
        json.dumps(
            {
                "id": user.id,
                "first_name": user.first_name,
                "last name": user.last_name,
                "email": user.email,
                "contests": user.contests,
            }
        ),
        HTTPStatus.OK,
        mimetype="application/json",
    )
    return response


@app.get("/users/<int:user_id>/contests")
def get_users_contests(user_id):
    user = USERS[user_id]
    response = Response(
        json.dumps(
            {
                "contests": [
                    {
                        "id": CONT[contest_id].id,
                        "name": CONT[contest_id].name,
                        "sport": CONT[contest_id].sport,
                        "status": CONT[contest_id].status,
                        "participants": CONT[contest_id].participants,
                        "winner": CONT[contest_id].winner,
                    }
                    for contest_id in user.contests
                ]
            }
        ),
        HTTPStatus.OK,
        mimetype="application/json",
    )
    return response


@app.get("/users/leaderboard")
def create_leaderboard():
    data = request.get_json()
    type = data["type"]
    if type == "list":
        sort = data["sort"]
        if sort == "asc":
            USERS_asc = USERS.copy()
            USERS_asc.sort(key=lambda x: len(x.contests))
            response = Response(
                json.dumps(
                    {
                        "users": [
                            {
                                "id": user.id,
                                "first_name": user.first_name,
                                "last_name": user.last_name,
                                "email": user.email,
                                "contests": user.contests,
                            }
                            for user in USERS_asc
                        ]
                    }
                ),
                HTTPStatus.OK,
                mimetype="application/json",
            )
            return response
        elif sort == "desc":
            USERS_desc = USERS.copy()
            USERS_desc.sort(key=lambda x: len(x.contests), reverse=True)
            response = Response(
                json.dumps(
                    {
                        "users": [
                            {
                                "id": user.id,
                                "first_name": user.first_name,
                                "last_name": user.last_name,
                                "email": user.email,
                                "contests": user.contests,
                            }
                            for user in USERS_desc
                        ]
                    }
                ),
                HTTPStatus.OK,
                mimetype="application/json",
            )
            return response
        else:
            return Response(status=HTTPStatus.NOT_FOUND)
    elif type == "graph":
        matplotlib.use('agg')
        plt.plot(
            [f"{user.first_name} {user.last_name}" for user in USERS],
            [len(user.contests) for user in USERS],
        )
        plt.xlabel(xlabel="участники")
        plt.ylabel(ylabel="Количество соревнований")
        plt.title("Графика пользователей по количеству соревнований")
        plt.savefig("application/static/graph.png")
        return Response(
            f"""<img src= "{url_for('static', filename='graph.png')}"> """,
            status=HTTPStatus.OK,
            mimetype="text/html",
        )
    else:
        return Response(status=HTTPStatus.NOT_FOUND)