import csv

def get_links_csv_data(filename):
    with open(filename, encoding='utf8') as file:
        csvreader = csv.reader(file)
        # for row in csvreader:
        #     print(row)
        # csvreader.seek(0)
        return [{
            'id' : index + 1,
            'movie_id' : row[0],
            'imdb_id' : row[1],
            'tmdb_id' : row[2]
        }
         for index, row in enumerate(csvreader)]
        