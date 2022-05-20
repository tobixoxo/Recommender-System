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

def read_csv():
    movie_record = []
    #genre record will be a set
    genre_record = set()

    with open('server/movies.csv', encoding='utf8') as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            movie_record.append(make_movie_record(row))
            genre_row = row[2].split("|")
            for g in genre_row:
                genre_record.add(g)
    return movie_record, list(genre_record)


def get_dicts(movies, genres):
    all_genres = []
    all_movies = []
    all_movie_genres = []
    genres_dict = {}
    for index, genre in enumerate(genres):
        genres_dict[genre] = index + 1
        all_genres.append({'id': index + 1, 'title': genre})

    c = 1
    for index, movie in enumerate(movies):
        all_movies.append({'id': index + 1, 'title': movie['title'], 'year': movie['year']})
        for genre in movie['genres']:
            all_movie_genres.append({'id': c, 'movie_id': index + 1, 'genre_id': genres_dict[genre]})
            c += 1
    return all_movies, all_genres, all_movie_genres

def get_csv_data():
    movies, genres = read_csv()
    return get_dicts(movies, genres)

