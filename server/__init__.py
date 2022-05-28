from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import LoginManager
from datetime import timedelta
import os
from os.path import exists
from flask_jwt_extended import JWTManager

app = Flask(__name__)
CORS(app)
login_manager = LoginManager()
login_manager.init_app(app)

app.config['SECRET_KEY'] = 'this-is-not-final'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # we don't need real time updates as this is a REST based api

app.config["JWT_SECRET_KEY"] = os.environ.get('JWT_SECRET_KEY')
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=2)
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config['JWT_COOKIE_CSRF_PROTECT'] = False
app.config['JWT_CSRF_CHECK_FORM'] = True

jwt = JWTManager(app)
db = SQLAlchemy(app)

from server.models import *
db.create_all()

import create_data

# create_data.create_data(
#     'movies.csv',
#     'ratings.csv',
#     'dummy_users_final.csv',
#     'links.csv'
# )

import server.routes

if not exists('processed_data.h5'):
    print("preprocessing dataframe, kindly wait for few minutes :)")
    from collaborative_filtering.collaborative_filtering import store_df_as_HDF
    store_df_as_HDF()

@login_manager.user_loader
def load_user(user_id):
    return User.get(int(user_id))
