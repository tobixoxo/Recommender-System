from server import db
from server.models import *

# Movie.query.delete()
# Genre.query.delete()
# MovieGenre.query.delete()
# UserRatings.query.delete()
# db.session.commit()


db.session.add(Movie(** {
    'id' : 1,
    'title' : 'Toy Story',
    'year' : 1998,
}))

db.session.add(Movie(** {
    'id' : 2,
    'title' : '50 shades of grey',
    'year' : 2012,
}))

db.session.add(Movie(** {
    'id' : 3,
    'title' : 'krishh',
    'year' : 2007,
}))

db.session.add(Genre(** {
    'id' : 1,
    'title' : 'comedy',
}))

db.session.add(Genre(** {
    'id' : 2,
    'title' : 'animation',
}))

db.session.add(Genre(** {
    'id' : 3,
    'title' : 'action',
}))

db.session.add(Genre(** {
    'id' : 4,
    'title' : 'romance',
}))

db.engine.execute(
    MovieGenre.insert().values(**{
    'movie_id' : 1,
    'genre_id' : 1
    }))

db.engine.execute(
    MovieGenre.insert().values(**{
    'movie_id' : 1,
    'genre_id' : 1
}))

db.engine.execute(
    MovieGenre.insert().values(**{
    'movie_id' : 1,
    'genre_id' : 2
}))

db.engine.execute(
    MovieGenre.insert().values(**{
    'movie_id' : 2,
    'genre_id' : 4
}))

db.engine.execute(
    MovieGenre.insert().values(**{
    'movie_id' : 3,
    'genre_id' : 3
}))

db.session.add(UserRatings(**{
    'id':1,
    'movie_id': 1,
    'rating':4,
    'user_id':1
}))

db.session.add(UserRatings(**{
    'id':2,
    'movie_id':1,
    'rating':4,
    'user_id':1
}))

db.session.add(UserRatings(**{
    'id':3,
    'movie_id':2,
    'rating':5,
    'user_id':2,
}))

db.session.add(UserRatings(**{
    'id':4,
    'movie_id':2,
    'rating':1,
    'user_id':2,
}))

db.session.add(UserRatings(**{
    'id':5,
    'movie_id':3,
    'rating':3,
    'user_id':3,
}))

db.session.add(UserRatings(**{
    'id':6,
    'movie_id':3,
    'rating':2,
    'user_id':3,
}))
db.session.commit()
