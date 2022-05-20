from server import db
from server.models import *

Movie.query.delete()
Genre.query.delete()
Movie_Genre.query.delete()
db.session.commit()


from server.readfile import get_csv_data

movies, genres, movie_genres, ratings = get_csv_data()
for movie in movies:
    db.session.add(Movie(**movie))

for genre in genres:
    db.session.add(Genre(**genre))

for mg in movie_genres:
    db.session.add(Movie_Genre(**mg))

for rating in ratings:
    db.session.add(UserRatings(**rating))

db.session.commit()