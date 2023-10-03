from flask import Flask
from app import views
from app import models

app = Flask(__name__)

USERS = []  # list for objects of type USER
CONT = []