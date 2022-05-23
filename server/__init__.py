from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import LoginManager

app = Flask(__name__)
CORS(app)
login_manager = LoginManager()
login_manager.init_app(app)

app.config['SECRET_KEY'] = 'this-is-not-final'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # we don't need real time updates as this is a REST based api
db = SQLAlchemy(app)

from server.models import *
db.create_all()

from server import create_data

create_data.create_data(
    'server/datasets/dummy_movies.csv',
    'server/datasets/dummy_ratings.csv',
    'server/datasets/dummy_users.csv'
)

@app.route('/')
def index_route():
    links = ""
    for i in range(1,11):
        links += f"<a href = '/recommend_movies/{i}' > recommendations for user {i} </a><br>"

    return "<a href='/view_db' > view the database </a><br> " + links


@app.route('/view_db')
def view_db_route():
    return render_template('view_db.html', **{
        'movies' : Movie.query.all(),
        'genres' : Genre.query.all(),
        # 'MovieGenre' : MovieGenre.query.all(),
        'ratings' : UserRatings.query.all(),
    })

from server.collaborative_filtering import make_recommendations

@app.route('/recommend_movies/<int:user_id>')
def recommend_movies_route(user_id):
    movs = make_recommendations(user_id)
    return render_template('recommend_movies.html', **{
        'movs' : movs
    })

@login_manager.user_loader
def load_user(user_id):
    return User.get(int(user_id))

