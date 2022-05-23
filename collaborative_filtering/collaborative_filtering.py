from multiprocessing.sharedctypes import Value
from warnings import simplefilter
from server.models import Movie, UserRatings
import pandas as pd

def watch_history_for_user(uid):
        return [(Movie.query.get(watched_movie.movie_id).title ,watched_movie.rating) 
        for watched_movie in 
        UserRatings.query.filter( UserRatings.user_id == uid )]

def make_list(ur):
        # print("making list for ",ur)
        movie =  Movie.query.get(ur.movie_id)
        if movie == None:
            print(ur.id,"EROORRR ----------------------")
        return [ur.user_id, movie.title, ur.rating]

def get_similar_movies(movie, user_rating, item_similarity_df):
    similar_movies = item_similarity_df[movie]*(user_rating - 2.5)
    return similar_movies


def make_recommendations(user_id):
    print("reached colb filtering")
    data_list = [make_list(ur) for ur in UserRatings.query.all()]

    rating_dataframe = pd.DataFrame(data_list, columns = ['userId','title','rating'])

    user_ratings = rating_dataframe.pivot_table(index = ['userId'],columns = ['title'], values= 'rating')

    #   NOTE (DONE) : DO DROP USERS WITH LESS THAN threshold RATINGS
    user_ratings = user_ratings.dropna(thresh = 10, axis = 1).fillna(0)
    
    item_similarity_df = user_ratings.corr(method = 'pearson')
    # print(item_similarity_df, "\n\n\n")

    print("item_similarity matrix calculated!")
    real_watcher = watch_history_for_user(user_id)[:5]

    similar_movies0 = pd.DataFrame()
    for movie, rating in real_watcher:
        print(movie," calculation \n")
        similar_movies0 = similar_movies0.append(get_similar_movies(movie, rating, item_similarity_df), ignore_index=True)

    similar_movies = similar_movies0
    print("list of row of similar movies \n", similar_movies0,"\n\n")
    print("concatanated df similar movies " ,similar_movies, "\n\n\n")

    similar_movies = similar_movies.sum().sort_values(ascending = False).head(10)

    print(similar_movies,"\n\n\n")

    similar_movies_dict = similar_movies.to_dict()
    similar_movies_names = similar_movies_dict.keys()
    print(similar_movies_names,"\n\n\n")

    # NOTE : head of list = 10
    return similar_movies_names
    # print(similar_movies_dict)