from server import app , bcrypt
from server.models import *
import requests
from datetime import datetime

from flask import  render_template, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from server.jwt_functions import *
from collaborative_filtering.collaborative_filtering import make_recommendations

#--------------------------------

def fetch_poster(tmdb_id):
    response = requests.get(f"https://api.themoviedb.org/3/movie/{tmdb_id}?api_key=fe08c428401d53b57647f169311f2c4c&language=en-US").json()
    if 'poster_path' not in response or response['poster_path'] == None:
        return ""
    return "https://image.tmdb.org/t/p/original/" + response['poster_path']

def add_rating_to_db(user_email, rating, movie_id):
    user_id = User.query.filter(User.email == user_email).first().id
    db.session.add(UserRatings(**{
        'movie_id':movie_id,
        'user_id': user_id,
        'rating' : rating
    }))
    db.session.commit()

def add_playlist_to_db(user_email, playlist_name):
    user_id = User.query.filter(User.email == user_email).first().id
    # check if playlist with the same name exists
    db.session.add(Playlist(**{
        'title' : playlist_name,
        'user_id' : user_id
    }))
    db.session.commit()
    
def get_previous_rating(user, rating, already_rated, movie_id):
    user_id = User.query.filter(User.email == user).first().id
    ratings = UserRatings.query.filter( 
        UserRatings.user_id == user_id).filter(
            UserRatings.movie_id == movie_id
        ).first()
    if ratings is not None:
        rating = ratings.rating
        already_rated = True 
    return rating, already_rated

def update_playlist(playlist_id, movie_id):
    db.engine.execute(PlaylistContent.insert().values(**{
        'playlist_id' : playlist_id,
        'movie_id' : movie_id
    }))

#---------------------------------

@app.route('/')
def index_route():
    return render_template('index.html')

@app.route('/view_db')
def view_db_route():
    return render_template('view_db.html', **{
        'movies' : Movie.query.all()[:30],
        'genres' : Genre.query.all()[:30],
        'ratings' : UserRatings.query.all()[:30],
    })
    
@app.route('/movie_details/<int:movie_id>',methods=['POST','GET'])
@jwt_required(optional = True)
def movie_details_route(movie_id):
    user = get_jwt_identity()
    already_rated = False
    rating = None
    if user is not None:
        rating, already_rated = get_previous_rating(user,rating, already_rated, movie_id)
    movie = Movie.query.get(movie_id)
    obj = Links.query.filter(Links.movie_id == movie_id).first()
    if obj == None:
        return render_template('movie_details.html',movie)
    poster_path = fetch_poster(obj.tmdb_id)
    playlists = [
        {
            'name' : "ghibli",
            'id' : 1
        },
        {
            'name' : "sad romance",
            'id' : 2
        },
        {
            'name' : "thriller",
            'id' : 3
        }
    ]
    return render_template('movie_details.html',**{
        'movie' : movie,
        'poster_path' : poster_path,
        'already_rated': already_rated,
        'rating' : rating,
        'genres' :[g.title for g in movie.genres],
        'playlists' : playlists
    } )

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
        poster_paths = [fetch_poster(Links.query.filter(Links.movie_id == movie.id).first().tmdb_id) 
                        for movie in results ]
        return render_template("search_movies.html", **{
            'value' : results,
            'poster_paths' : poster_paths
        })

@app.route('/signup', methods =['GET','POST'])
def signup_route():
    if request.method == 'GET':
        return render_template('signup.html')
    if request.method == 'POST':
        form_data1 = request.form
        form_data = dict(form_data1)
        dt = datetime.strptime(form_data['dob'],'%Y-%m-%d')
        d = dt.date()
        form_data['dob'] = d
        pw_hash = bcrypt.generate_password_hash(form_data['password'])
        print(form_data['password']," ", pw_hash)
        db.session.add(User(** {
            'name': form_data['name'],
            'nickname':form_data['nickname'],
            'email':form_data['email'],
            'dob' : form_data['dob'],
            'bio':form_data['bio'],
            'password': pw_hash
        }))
        db.session.commit()
        return redirect('/login')

@app.route('/give_rating/<int:movie_id>', methods = ['POST'])
@jwt_required()
def give_rating(movie_id):
    user = get_jwt_identity()
    form_data = dict(request.form)
    add_rating_to_db(user, form_data['rating'], movie_id)
    return redirect(f'/movie_details/{movie_id}')

@app.route('/add_playlist', methods = ['POST'])
@jwt_required()
def add_playlist():
    user = get_jwt_identity()
    form_data = dict(request.form)
    add_playlist_to_db(user, form_data['playlist-name'])
    return redirect('/dashboard')

@app.route('/add_movie_to_playlist/<int:movie_id>', methods = ['POST'])
@jwt_required()
def add_movie_to_playlist(movie_id):
    user = get_jwt_identity()
    form_data = dict(request.form)
    update_playlist(form_data['playlist-id'],movie_id)
    return redirect('/dashboard')

@app.route('/dashboard')
@jwt_required()
def dashboard_route():
    email = get_jwt_identity()
    user = User.query.filter(User.email == email).first()
    movs = make_recommendations(user.id)
    recommendations = [Movie.query.filter(Movie.title == mov).first() for mov in movs]
    poster_paths = [fetch_poster(Links.query.filter(Links.movie_id == movie.id).first().tmdb_id) 
                        for movie in recommendations ]
    rated_movies = [{
        'title' : Movie.query.get(mr.movie_id).title,
        'rating' : mr.rating
    } for mr in UserRatings.query.filter(UserRatings.user_id == user.id)]

    playlists = [
        {
            'id': 1,
            'name' : "Action",
            'description' : 'my collections',
            'movies' : ['Avengers', 'Avengers 1', 'Avengers Returns']
        },
        {
            'id': 2,
            'name' : "Romance",
            'description' : 'Raat ko dekhunga',
            'movies' : ['50 shades', 'darker']
        }
    ]

    return render_template('dashboard.html', **{
        'user': user,
        'recommendations' : recommendations,
        'poster_paths' : poster_paths,
        'rated_movies' : rated_movies,
        'playlists' : playlists
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
            candidate_hash = bcrypt.generate_password_hash(password)
            print(password, " ", candidate_hash)
            if (bcrypt.check_password_hash(user.password,password)):
                return assign_access_refresh_tokens(email ,'/dashboard') 
            else :
                return "wrong password"
        else :
            return "email doesnt exist"  

@app.route('/logout')
@jwt_required()
def logout_route():
    return unset_jwt()