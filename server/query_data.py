from multiprocessing.sharedctypes import Value
from warnings import simplefilter
from server.models import Movie, UserRatings, watch_history_for_user
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

data_list = [ur.make_list() for ur in UserRatings.query.all()]

print(data_list, "\n\n\n")

rating_dataframe = pd.DataFrame(data_list, columns = ['userId','title','rating'])

print(rating_dataframe,"\n\n\n")

user_ratings = rating_dataframe.pivot_table(index = ['userId'],columns = ['title'], values= 'rating')
user_ratings = user_ratings.fillna(3)
print(user_ratings,"\n\n\n")

#   NOTE : DO DROP USERS WITH LESS THAN threshold RATINGS
item_similarity_df = user_ratings.corr(method = 'pearson')
print(item_similarity_df, "\n\n\n")

# similarity score will be multiplied with ratings of the user
def get_similar_movies(movie, user_rating):
    similar_movies = item_similarity_df[movie]*(user_rating - 2.5)
    return similar_movies

dummy_watcher = [("Sudden Death",4), ("Heat", 5),("Toy Story",2)]

real_watcher = watch_history_for_user(5)
print("real user watch history : \n" , real_watcher, "\n\n\n")

similar_movies = pd.DataFrame()
for movie, rating in real_watcher:
    similar_movies = similar_movies.append(get_similar_movies(movie, rating), ignore_index = True)

print(similar_movies, "\n\n\n")
similar_movies = similar_movies.sum().sort_values(ascending = False)
print(similar_movies,"\n\n\n")

similar_movies_dict = similar_movies.to_dict()
print(similar_movies_dict)