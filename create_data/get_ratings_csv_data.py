import csv

def make_ratings(row):
    rating = {}
    rating['user_id'] = int(row[0])
    rating['movie_id'] = int(row[1])
    rating['rating'] = int(float(row[2]))
    return rating
     
def  get_ratings_csv_data(filename):
    ratings = []
    with open(filename, encoding = 'utf8') as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            ratings.append(make_ratings(row))
    
    all_ratings = []
    for index, rating in enumerate(ratings):
        rating['id'] = index + 1
        all_ratings.append(rating)
    return all_ratings
    


        
