import re
import csv

def movie_name_without_year(name):
    return re.sub('\(\d{4}\)', "", name).strip()

def extract_year_from_movie_name(name):
    return int(re.search('\(\d{4}\)', name).group()[1:-1])

def make_movies(row):
    movie = {}
    movie['title'] = movie_name_without_year(row[1])
    movie['year'] = extract_year_from_movie_name(row[1])
    movie['genres'] = row[2].split("|")
    return movie

def get_movies_csv_data(filename):
    movies = []
    genre_record = set()

    with open(filename, encoding='utf8') as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            movies.append(make_movies(row))
            genre_row = row[2].split("|")
            for g in genre_row:
                genre_record.add(g)
    genres = list(genre_record)

    all_genres = []
    all_movies = []
    all_MovieGenres = []
    genres_dict = {}
    for index, genre in enumerate(genres):
        genres_dict[genre] = index + 1
        all_genres.append({'id': index + 1, 'title': genre})

    for index, movie in enumerate(movies):
        all_movies.append({'id': index + 1, 'title': movie['title'], 'year': movie['year']})
        for genre in movie['genres']:
            all_MovieGenres.append({ 'movie_id': index + 1, 'genre_id': genres_dict[genre]})
    
    return  all_movies, all_genres, all_MovieGenres
    