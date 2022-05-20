from server import db
from server.models import *

Movie.query.delete()
Genre.query.delete()
Movie_Genre.query.delete()
db.session.commit()


db.session.add(Movie(** {
    'id' : 1,
    'title' : 'Toy Story',
    'description' : 'toys coming alive',
    'year' : 1998,
}))

db.session.add(Movie(** {
    'id' : 2,
    'title' : '50 shades of grey',
    'description' : 'billionaire bdsm enthusiast',
    'year' : 2012,
}))

db.session.add(Movie(** {
    'id' : 3,
    'title' : 'krishh',
    'description' : 'indian supe',
    'year' : 2007,
}))

db.session.add(Genre(** {
    'id' : 1,
    'name' : 'comedy',
    'description' : 'funny laughs',
}))

db.session.add(Genre(** {
    'id' : 2,
    'name' : 'animation',
    'description' : '4 kids',
}))

db.session.add(Genre(** {
    'id' : 3,
    'name' : 'action',
    'description' : 'boom boom dishfaisfh',
}))

db.session.add(Genre(** {
    'id' : 4,
    'name' : 'romance',
    'description' : 'love dovey',
}))

db.session.add(Movie_Genre(**{
    'id' : 1,
    'movie_id' : 1,
    'genre_id' : 1
}))

db.session.add(Movie_Genre(**{
    'id' : 2,
    'movie_id' : 1,
    'genre_id' : 2
}))

db.session.add(Movie_Genre(**{
    'id' : 3,
    'movie_id' : 2,
    'genre_id' : 4
}))

db.session.add(Movie_Genre(**{
    'id' : 4,
    'movie_id' : 3,
    'genre_id' : 3
}))

db.session.commit()
