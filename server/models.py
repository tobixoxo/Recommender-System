from collections import UserList
from enum import unique
from turtle import title
from server import db
from flask_login import UserMixin



MovieGenre = db.Table('MovieGenre',
    db.Column('movie_id', db.Integer, db.ForeignKey("movie.id"), nullable = False),
    db.Column('genre_id',db.Integer, db.ForeignKey("genre.id"), nullable = False )
)

PlaylistContent = db.Table('PlaylistContent',
    db.Column('playlist_id',db.Integer, db.ForeignKey("playlist.id"), nullable = False),
    db.Column('movie_id', db.Integer, db.ForeignKey("movie.id"), nullable = False)
)
#----------------------------'
class UserRatings(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    movie_id = db.Column(db.Integer, db.ForeignKey("movie.id"), nullable = False)
    user_id = db.Column(db.Integer,db.ForeignKey("user.id"), nullable = False)
    rating = db.Column(db.Integer, nullable = False)
    def __str__(self):
        return f"user {self.user_id} gave {self.rating} to {self.movie_id}"
    
        
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String, unique=False, nullable=False)
    year = db.Column(db.Integer, unique = False, nullable = True)
    description = db.Column(db.Text, unique = False, nullable = True)
    genres = db.relationship("Genre",secondary = MovieGenre, backref = "movies", lazy = True)
    # ratings = db.relationship("UserRating", backref = "movie", lazy = True)

class Genre(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String, unique=False, nullable=False)
    description = db.Column(db.Text, unique = False, nullable = True)
    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    #name fix : not nullable
    name = db.Column(db.String, unique = False, nullable = True)
    nickname = db.Column(db.String, unique = False, nullable = True)
    email = db.Column(db.String, unique = False, nullable = True)
    password = db.Column(db.String, unique = False, nullable = True)
    dob = db.Column(db.Date, unique = False, nullable = True)
    bio = db.Column(db.Text, unique = False, nullable = True)
    # playlists = db.relationship("Playlist", backref = db.backref("user", uselist = False), lazy = True)
    # ratings = db.relationship("UserRating", backref = "user", lazy = True)

class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String, unique=False, nullable=False)
    description = db.Column(db.Text, unique = False, nullable = True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key = True)

#----------------------------------------------------

