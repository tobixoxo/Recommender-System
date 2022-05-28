from server.models import Movie, UserRatings
import pandas as pd

def store_df_as_HDF():
    data_list = [make_list(ur) for ur in UserRatings.query.all()]

    rating_dataframe = pd.DataFrame(data_list, columns = ['userId','title','rating'])
    user_ratings = rating_dataframe.pivot_table(index = ['userId'],columns = ['title'], values= 'rating')
    user_ratings = user_ratings.fillna(0)
    item_similarity_df = user_ratings.corr(method = 'pearson')
    df_store = pd.HDFStore('processed_data.h5')
    df_store['preprocessed_df'] = item_similarity_df
    df_store.close()

def watch_history_for_user(uid):
        return [(Movie.query.get(watched_movie.movie_id).title ,watched_movie.rating) 
        for watched_movie in 
        UserRatings.query.filter( UserRatings.user_id == uid )]

def make_list(ur):
        movie =  Movie.query.get(ur.movie_id)
        return [ur.user_id, movie.title, ur.rating]

def get_similar_movies(movie, user_rating, item_similarity_df):
    similar_movies = item_similarity_df[movie]*(user_rating - 2.5)
    return similar_movies


def make_recommendations(user_id):
    data_store = pd.HDFStore('processed_data.h5')
    item_similarity_df =  data_store['preprocessed_df']

    real_watcher = watch_history_for_user(user_id)

    similar_movies0 = pd.DataFrame()
    for movie, rating in real_watcher:
        similar_movies0 = similar_movies0.append(get_similar_movies(movie, rating, item_similarity_df), ignore_index=True)

    similar_movies = similar_movies0

    similar_movies = similar_movies.sum().sort_values(ascending = False).head(18)


    similar_movies_dict = similar_movies.to_dict()
    similar_movies_names = list(similar_movies_dict.keys())

    # NOTE : head of list = 10

    return similar_movies_names