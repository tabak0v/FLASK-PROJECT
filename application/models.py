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

    @staticmethod
    def is_valid_email(email):
        if re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return True
        return False

    @staticmethod
    def is_valid_id(user_id):
        if user_id < 0 or user_id >= len(USERS):
            return False
        return True


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

    def add_winner(self, winner):
        self.winner = winner

    def finish_competition(self):
        self.status = "FINISHED"

    @staticmethod
    def is_valid_id(contest_id):
        if contest_id < 0 or contest_id >= len(CONT):
            return False
        return True