import re
import csv

def movie_name_without_year(name):
    return re.sub('\(\d{4}\)', "", name).strip()

def extract_year_from_movie_name(name):
    return int(re.search('\(\d{4}\)', name).group()[1:-1])


def get_movies_csv_data(filename):
    movies = []
    genres = set()
    all_genres = []
    all_MovieGenres = []
    all_movies = [ ]
    genres_dict = {}

    with open(filename, encoding='utf8') as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            print("on movie number ", row[0])
            movies.append({
                'id' : row[0],
                'title' : row[1],
                # 'year' : extract_year_from_movie_name(row[1]),
                'genres' : row[2].split("|")
            })
            genre_row = row[2].split("|")
            for g in genre_row:
                genres.add(g)
    genres = list(genres)
    
    for index, genre in enumerate(genres):
        genres_dict[genre] = index + 1
        all_genres.append({'id': index + 1, 'title': genre})

    for movie in movies:
        all_movies.append({
            'id' : movie['id'],
            'title' : movie['title'],
            # 'year' : movie['year']
        })
        for genre in movie['genres']:
            all_MovieGenres.append({ 'movie_id': movie['id'], 'genre_id': genres_dict[genre]})
    
    return  all_movies, all_genres, all_MovieGenres
    