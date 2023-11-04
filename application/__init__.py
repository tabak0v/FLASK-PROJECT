from flask import Flask

app = Flask(__name__)

USERS = []  # list for objects of type USER
CONT = []

from application import views
from application import models