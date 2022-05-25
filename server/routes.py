# from crypt import methods
from unittest import result
from urllib import request
from server import app
from server.models import *
from flask import render_template, request

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

@app.route('/search_movies', methods=['GET','POST'])
def search_movies_route():
    if request.method == 'GET':
        return render_template("search_movies.html")
    if request.method == 'POST':
        form_data = request.form
        form_data1 = dict(form_data)
        if form_data1['search_string'] == "":
            return render_template("search_movies.html")
        query = Movie.query.filter(Movie.title.contains(form_data1['search_string']))
        results = [movie for movie in query]
        return render_template("search_movies.html",value = results)

@app.route('/login_form')
def login_form_route():
    return render_template('login_form.html')
