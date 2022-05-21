from server import db
from server.models import *

# Movie.query.delete()
# Genre.query.delete()
# MovieGenre.query.delete()
# UserRatings.query.delete()
# db.session.commit()


from server.readfile import get_csv_data

def create_data(movies_filename, ratings_filename):
    movies, genres, MovieGenres, ratings = get_csv_data(movies_filename, ratings_filename)
    for movie in movies:
        db.session.add(Movie(**movie))

    for genre in genres:
        db.session.add(Genre(**genre))

    for mg in MovieGenres:
        db.engine.execute(MovieGenre.insert().values(**mg))

    for rating in ratings:
        db.session.add(UserRatings(**rating))

    db.session.commit()