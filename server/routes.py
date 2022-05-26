from server import app 
from server.models import *
import requests
from datetime import datetime

from flask import  render_template, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from server.jwt_functions import *
from collaborative_filtering.collaborative_filtering import make_recommendations

@app.route('/')
def index_route():
    return render_template('index.html')
@app.route('/view_db')
def view_db_route():
    return render_template('view_db.html', **{
        'movies' : Movie.query.all()[:30],
        'genres' : Genre.query.all()[:30],
        # 'MovieGenre' : MovieGenre.query.all(),
        'ratings' : UserRatings.query.all()[:30],
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

@app.route('/signup', methods =['GET','POST'])
def signup_route():
    if request.method == 'GET':
        return render_template('signup.html')
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
        return redirect('/login')

@app.route('/dashboard')
@jwt_required()
def dashboard_route():
    email = get_jwt_identity()
    user = User.query.filter(User.email == email).first()
    movs = make_recommendations(user.id)
    print("movs : \n", movs)
    return render_template('dashboard.html', **{
        'user': user,
        'recommendations' : movs,
    })

@app.route('/login', methods =['GET','POST'])
def login_route():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        form_data = dict(request.form)
        email = form_data['email']
        password = form_data['password']
        user = User.query.filter(User.email == email).first()
        if user != None:
            if (password == user.password):
                return assign_access_refresh_tokens(email ,'/dashboard') 
            else :
                return "wrong password"
        else :
            return "email doesnt exist"  

def fetch_poster(tmdb_id):
    response = requests.get(f"https://api.themoviedb.org/3/movie/{tmdb_id}?api_key=fe08c428401d53b57647f169311f2c4c&language=en-US").json()
    return "https://image.tmdb.org/t/p/original/" + response['poster_path']

@app.route('/movie_details/<int:movie_id>',methods=['POST','GET'])
def movie_details_route(movie_id):
    movie = Movie.query.get(movie_id)
    obj = Links.query.filter(Links.movie_id == movie_id).first()
    if obj == None:
        return render_template('movie_details.html',movie)
    poster_path = fetch_poster(obj.tmdb_id)
    return render_template('movie_details.html',**{
        'movie' : movie,
        'poster_path' : poster_path
    } )

@app.route('/logout')
@jwt_required()
def logout_route():
    return unset_jwt()
