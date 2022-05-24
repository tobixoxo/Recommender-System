from server import app
from server.models import *
from flask import render_template

@app.route('/')
def index_route():
    return render_template('index.html')

@app.route('/home')
def home_route():
    links = ""
    for i in range(1,11):
        links += f"<a href = '/recommend_movies/{i}' > recommendations for user {i} </a><br>"
    home = "<a href='/home' > home Page </a><br>"
    return home + "<a href='/view_db' > view the database </a><br> " + links

@app.route('/view_db')
def view_db_route():
    return render_template('view_db.html', **{
        'movies' : Movie.query.all(),
        'genres' : Genre.query.all(),
        # 'MovieGenre' : MovieGenre.query.all(),
        'ratings' : UserRatings.query.all(),
    })

from collaborative_filtering.collaborative_filtering import make_recommendations

@app.route('/recommend_movies/<int:user_id>')
def recommend_movies_route(user_id):
    movs = make_recommendations(user_id)
    return render_template('recommend_movies.html', **{
        'movs' : movs
    })

@app.route('/search_movies')
def search_movies_route():
    return "<h1> Search Movies Here! </h1>"

@app.route('/login_form')
def login_form_route():
    return "<h1>Login Form Here!</h1>"
