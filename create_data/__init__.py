from create_data import get_user_csv_data, get_movies_csv_data, get_ratings_csv_data

from server import db
from server.models import *

def create_data(movies_filename, ratings_filename, users_filename):
    link = "create_data/datasets/"
    movies, genres, MovieGenres = get_movies_csv_data.get_movies_csv_data(link + movies_filename)
    ratings = get_ratings_csv_data.get_ratings_csv_data(link + ratings_filename)
    users = get_user_csv_data.get_user_csv_data(link + users_filename)
    i = 0
    for user in users:
        print("on user no. ",i)
        db.session.add(User(**user))
        i+=1
    i = 0
    for movie in movies:
        print("on movie no. ",i)
        db.session.add(Movie(**movie))
        i+=1
    i = 0
    for genre in genres:
        print("on genre no. ",i)
        db.session.add(Genre(**genre))
        i+=1
    i = 0
    for mg in MovieGenres:
        print("on moviesGenre  ",i)
        db.engine.execute(MovieGenre.insert().values(**mg))
        i+=1
    i = 0
    for rating in ratings:
        print("on rating no. ",i)
        db.session.add(UserRatings(**rating))
        i+=1

    db.session.commit()