#what to do

import csv
import re
from pprint import pprint

def movie_name_without_year(name):
    return re.sub('\(\d{4}\)', "", name).strip()

def extract_year_from_movie_name(name):
    return int(re.search('\(\d{4}\)', name).group()[1:-1])

def make_movie_record(row):
    movie = {}
    movie['title'] = movie_name_without_year(row[1])
    movie['year'] = extract_year_from_movie_name(row[1])
    movie['genres'] = row[2].split("|")
    return movie

def make_rating_record(row):
    rating = {}
    rating['user_id'] = int(row[0])
    rating['movie_id'] = int(row[1])
    rating['rating'] = int(float(row[2]))
    return rating

def read_csv(movies_filename, ratings_filename):
    movie_record = []
    #genre record will be a set
    genre_record = set()

    with open(movies_filename, encoding='utf8') as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            movie_record.append(make_movie_record(row))
            genre_row = row[2].split("|")
            for g in genre_row:
                genre_record.add(g)
    rating_record = []
    with open(ratings_filename, encoding = 'utf8') as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            rating_record.append(make_rating_record(row))

    return movie_record, list(genre_record), rating_record


def get_dicts(movies, genres, ratings):
    all_genres = []
    all_movies = []
    all_MovieGenres = []
    all_ratings = []
    genres_dict = {}
    for index, genre in enumerate(genres):
        genres_dict[genre] = index + 1
        all_genres.append({'id': index + 1, 'title': genre})

    for index, movie in enumerate(movies):
        all_movies.append({'id': index + 1, 'title': movie['title'], 'year': movie['year']})
        for genre in movie['genres']:
            all_MovieGenres.append({ 'movie_id': index + 1, 'genre_id': genres_dict[genre]})
    for index, rating in enumerate(ratings):
        rating['id'] = index + 1
        all_ratings.append(rating)
    return all_movies, all_genres, all_MovieGenres, all_ratings

def get_csv_data(movies_filename, ratings_filename):
    movies, genres, ratings = read_csv(movies_filename, ratings_filename)
    return get_dicts(movies, genres, ratings)



