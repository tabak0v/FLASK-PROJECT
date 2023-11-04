from application import app, models, CONT, USERS
from flask import request, Response
import json
from http import HTTPStatus


@app.post("/contests/create")
def create_contest():
    data = request.get_json()
    contest_id = len(CONT)
    name = data["name"]
    sport = data["sport"]
    participants = data["participants"]
    contest = models.Contests(contest_id, name, sport, participants)
    contest.start_competition()
    # adding contests_id to user.contests and checking if users can participate in that competition
    for user_id in participants:
        if not models.User.is_valid_sport(user_id, sport):
            return Response(status=HTTPStatus.BAD_REQUEST)
        USERS[user_id].contests.append(contest_id)

    CONT.append(contest)
    response = Response(
        json.dumps(
            {
                "id": contest.id,
                "name": contest.name,
                "sport": contest.sport,
                "status": contest.status,
                "participants": contest.participants,
                "winner": contest.winner,
            }
        ),
        status=HTTPStatus.OK,
        mimetype="applicaction/json",
    )
    return response


@app.get("/contests/<int:contest_id>")
def get_contest(contest_id):
    cont = CONT[contest_id]
    if not models.Contests.is_valid_id(contest_id):
        return Response(status=HTTPStatus.NOT_FOUND)
    response = Response(
        json.dumps(
            {
                "id": cont.id,
                "name": cont.name,
                "sport": cont.sport,
                "status": cont.status,
                "participants": cont.participants,
                "winner": cont.winner,
            }
        ),
        HTTPStatus.OK,
        mimetype="application/json",
    )
    return response


@app.post("/contests/<int:contest_id>/finish")
def finish_contest(contest_id):
    contest = CONT[contest_id]
    if not models.Contests.is_valid_id(contest_id):
        return Response(status=HTTPStatus.NOT_FOUND)
    data = request.get_json()
    winner = data["winner"]
    contest.add_winner(winner)
    contest.finish_competition()
    response = Response(
        json.dumps(
            {
                "id": contest.id,
                "name": contest.name,
                "sport": contest.sport,
                "status": contest.status,
                "participants": contest.participants,
                "winner": contest.winner,
            }
        ),
        status=HTTPStatus.OK,
        mimetype="applicaction/json",
    )
    return response
