from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # we don't need real time updates as this is a REST based api
db = SQLAlchemy(app)

from server.models import *
db.create_all()

from server import dummy_data

@app.route('/')
def index_route():
    return "<a href='/view_db' > view the database </a>"

@app.route('/view_db')
def view_db_route():
    return render_template('view_db.html', **{
        'movies' : Movie.query.all(),
        'genres' : Genre.query.all(),
        'movie_genre' : Movie_Genre.query.all()
    })
    