from multiprocessing.sharedctypes import Value
from warnings import simplefilter
from server.models import Movie, UserRatings, watch_history_for_user
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def get_similar_movies(movie, user_rating):
    data_list = [ur.make_list() for ur in UserRatings.query.all()]

    rating_dataframe = pd.DataFrame(data_list, columns = ['userId','title','rating'])

    user_ratings = rating_dataframe.pivot_table(index = ['userId'],columns = ['title'], values= 'rating')
    user_ratings = user_ratings.fillna(3)

    #   NOTE : DO DROP USERS WITH LESS THAN threshold RATINGS
    item_similarity_df = user_ratings.corr(method = 'pearson')
    # print(item_similarity_df, "\n\n\n")

    similar_movies = item_similarity_df[movie]*(user_rating - 2.5)
    return similar_movies

def make_recommendations(user_id):
    
    real_watcher = watch_history_for_user(user_id)
    print("real user watch history : \n" , real_watcher, "\n\n\n")

    similar_movies = pd.DataFrame()
    for movie, rating in real_watcher:
        similar_movies = similar_movies.append(get_similar_movies(movie, rating), ignore_index = True)

    # print(similar_movies, "\n\n\n")
    similar_movies = similar_movies.sum().sort_values(ascending = False)
    print(similar_movies,"\n\n\n")

    similar_movies_dict = similar_movies.to_dict()
    similar_movies_names = similar_movies_dict.keys()
    print(similar_movies_names,"\n\n\n")

    # NOTE : head of list = 10
    return similar_movies_names
    # print(similar_movies_dict)