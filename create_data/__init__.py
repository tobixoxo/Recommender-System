from create_data import get_user_csv_data, get_movies_csv_data, get_ratings_csv_data

from server import db
from server.models import *

def create_data(movies_filename, ratings_filename, users_filename):
    link = "create_data/datasets/"
    movies, genres, MovieGenres = get_movies_csv_data.get_movies_csv_data(link + movies_filename)
    ratings = get_ratings_csv_data.get_ratings_csv_data(link + ratings_filename)
    users = get_user_csv_data.get_user_csv_data(link + users_filename)
    
    for user in users:
        db.session.add(User(**user))

    for movie in movies:
        db.session.add(Movie(**movie))

    for genre in genres:
        db.session.add(Genre(**genre))

    for mg in MovieGenres:
        db.engine.execute(MovieGenre.insert().values(**mg))

    for rating in ratings:
        db.session.add(UserRatings(**rating))

    db.session.commit()