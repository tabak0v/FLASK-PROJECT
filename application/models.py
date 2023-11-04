import re
from application import USERS, CONT


class User:
    def __init__(self, id, first_name, last_name, email, sport):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.sport = sport
        self.contests = []
        self.status = "created"

    @staticmethod
    def is_valid_email(email):
        return re.match(r"[^@]+@[^@]+\.[^@]+", email)

    @staticmethod
    def is_valid_id(user_id):
        return 0 <= user_id < len(USERS) and USERS[user_id].status != "deleted"

    @staticmethod
    def is_valid_sport(user_id, sport):
        return USERS[user_id].sport == sport


class Contests:
    def __init__(self, id, name, sport, participants, winner=None, status=None):
        self.id = id
        self.name = name
        self.sport = sport
        self.winner = winner
        self.participants = participants
        self.status = status

    def start_competition(self):
        self.status = "STARTED"

    def finish_competition(self):
        self.status = "FINISHED"

    def add_winner(self, winner):
        self.winner = winner

    @staticmethod
    def is_valid_id(contest_id):
        return not contest_id < 0 or contest_id >= len(CONT)
