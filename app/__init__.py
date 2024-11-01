# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import firebase_admin
from firebase_admin import credentials, firestore, auth


# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Initialize Flask app
app = Flask(__name__)
app.config.from_object('app.config.Config')


# Initialize Firebase
cred = credentials.Certificate(r"./app/firebase-cognipath.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
# Initialize extensions
bc = Bcrypt(app)      # flask-bcrypt

# Initialize LoginManager with stronger session protection
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'register'
lm.session_protection = "strong"

# Import the models
from app.models import User

# Setup user loader function for Flask-Login
@lm.user_loader
def load_user(user_id):
    if not user_id:
        return None
    try:
        user_doc = db.collection('users').document(user_id).get()
        if user_doc.exists:
            return User(user_doc.to_dict())
    except Exception as e:
        print(f"Error loading user: {e}")
    return None

# Setup database
# @app.before_first_request
# def initialize_database():
#     db.create_all()

# Import routing after initializing app and extensions
from app import views
