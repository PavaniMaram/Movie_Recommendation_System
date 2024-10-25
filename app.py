import streamlit as st
import pickle
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

import pandas as pd

# Create a session with retry functionality
session = requests.Session()
retry = Retry(connect=4, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=6554c19b9c4ca07f978823ab2ff98ca5&language=en-US".format(movie_id)
    
    # Use the session to make the request
    data = session.get(url)
    data = data.json()
    
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommended(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies_name = []
    recommended_movies_poster = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies_poster.append(fetch_poster(movie_id))
        recommended_movies_name.append(movies.iloc[i[0]].title)
    return recommended_movies_name, recommended_movies_poster

# ... rest of the code remains unchanged ...




st.header("Movie Recommender System Using Machine learning Algorithum")
movies = pd.read_pickle("artifacts/movie.pkl")

similarity = pd.read_pickle("artifacts/similarity.pkl")


movie_list=movies['title'].values 
selected_movie= st.selectbox(
    'Type or select movie to get the movie recommendation',
    movie_list
)

if st.button('Show recommendation'):
    recommended_movies_name, recommended_movies_poster= recommended(selected_movie)
    col1,col2,col3,col4,col5=st.columns(5)
    with col1:
        st.text(recommended_movies_name[0])
        st.image(recommended_movies_poster[0])
    with col1:
        st.text(recommended_movies_name[1])
        st.image(recommended_movies_poster[1])
    with col1:
        st.text(recommended_movies_name[2])
        st.image(recommended_movies_poster[2])
    with col1:
        st.text(recommended_movies_name[3])
        st.image(recommended_movies_poster[3])
    with col1:
        st.text(recommended_movies_name[4])
        st.image(recommended_movies_poster[4])