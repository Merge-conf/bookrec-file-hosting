# flask-app
from flask import Flask
from flask_cors import CORS
from flask_uuid import FlaskUUID

app = Flask(__name__)
CORS(app)
FlaskUUID(app)

# database
import os
from flask_sqlalchemy import SQLAlchemy

if os.environ.get("HEROKU"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tracks.db"
    app.config["SQLALCHEMY_ECHO"] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# session
from flask import session
from os import urandom

app.secret_key = urandom(32)

# functionality
from application import views

from application.tracks import models
from application.tracks import views

try:
    db.create_all()
except:
    pass
