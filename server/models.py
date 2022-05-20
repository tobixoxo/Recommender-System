from turtle import title
from server import db


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String, unique=False, nullable=False)
    year = db.Column(db.Integer, unique = False, nullable = True)
    genres = db.relationship("Movie_Genre", backref = "movie", lazy = True)

class Genre(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String, unique=False, nullable=False)
    movies = db.relationship("Movie_Genre", backref = "genre", lazy = True)

class Movie_Genre(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    movie_id = db.Column(db.Integer, db.ForeignKey("movie.id"), primary_key = True)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"), primary_key = True )
