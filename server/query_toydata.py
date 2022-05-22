from multiprocessing.sharedctypes import Value
from warnings import simplefilter
from server.models import Movie, UserRatings
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

#---------------------------------------------------------------------------------
ratings = pd.read_csv("server/datasets/toydataset.csv",index_col= 0)
ratings = ratings.fillna(0)

def standardize(row):
    new_row = (row - row.mean()) / (row.max() - row.mean())
    return new_row
ratings_std = ratings.apply(standardize)
# print(ratings_std)
item_similarity_df = cosine_similarity(ratings_std.T)
item_similarity_df = pd.DataFrame(item_similarity_df, index = ratings.columns, columns = ratings.columns)
# print(item_similarity_df)
# print("helllo")
# print("\n\n")

def get_similar_movies(movie, user_rating):
    # print(movie, user_rating)
    similar_movies = item_similarity_df[movie]*(user_rating - 2.5)
    # print(similar_movies)
    return similar_movies

dummy_romance_lover = [ ('romantic3',5),('romantic2', 5),('romantic1',5)]

similar_movies = pd.DataFrame()

for movie, rating in dummy_romance_lover:
    similar_movies = similar_movies.append(get_similar_movies(movie, rating), ignore_index = True)


print(similar_movies)
similar_movies = similar_movies.sum().sort_values(ascending=False)
similar_movies_dict = similar_movies.to_dict()
print(similar_movies_dict)