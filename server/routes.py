# from crypt import methods
from dataclasses import dataclass
from unittest import result
from urllib import request
from server import app
from server.models import *
from flask import render_template, request
from datetime import datetime

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
        'movies' : Movie.query.all()[:30],
        'genres' : Genre.query.all()[:30],
        # 'MovieGenre' : MovieGenre.query.all(),
        'ratings' : UserRatings.query.all()[:30],
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

@app.route('/login_form', methods =['GET','POST'])
def login_form_route():
    if request.method == 'GET':
        return render_template('login_form.html')
    if request.method == 'POST':
        form_data1 = request.form
        form_data = dict(form_data1)
        # print(form_data['dob']," " ,type(form_data['dob']))
        dt = datetime.strptime(form_data['dob'],'%Y-%m-%d')
        d = dt.date()
        form_data['dob'] = d
        print(form_data['dob']," " ,type(form_data['dob']))
        db.session.add(User(** {
            'name': form_data['name'],
            'nickname':form_data['nickname'],
            'email':form_data['email'],
            'dob' : form_data['dob'],
            'bio':form_data['bio'],
            'password': form_data['password']
        }))
        db.session.commit()
        # print(form_data,"\n",form_data1)
        return render_template('login_form.html')

@app.route('/signup_form')
def signup_form_route():
    return render_template('signup_form.html')

@app.route('/dashboard', methods=['GET','POST'])
def dashboard_route():
    credentials = dict(request.form)
    user = User.query.filter(User.email == credentials['email']).first()
    print(user)
    movs = make_recommendations(user.id)
    return render_template('dashboard.html', **{
        'user': user,
        'recommendations' : movs
    })