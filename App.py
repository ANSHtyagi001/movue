import streamlit as st
import pickle
import pandas as pd
import requests
import os

st.title('Movie Recommender')


def fetch_poster(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=7082040c7c553ffff59a46ac82ba64ff&language=en-US'.format(
            movie_id))
    data = response.json()
    print(data)

    return 'http://image.tmdb.org/t/p/w500/' + data['poster_path']


def recommend(movie):
    movie_index = DF[DF['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_lst = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommend_movies = []
    recommend_movies_posters = []

    for i in movie_lst:
        recommend_movies.append(DF.iloc[i[0]].title)
        recommend_movies_posters.append(fetch_poster(DF.iloc[i[0]].movie_id))

    return recommend_movies, recommend_movies_posters


similarity = pickle.load(open('similarity.pkl', 'rb'))
DF = pickle.load(open('movies.pkl', 'rb'))
movie_list = DF['title'].values

movie_input = st.selectbox('Enter the Movie Name', movie_list)

if st.button('Recommend'):
    move, posters = recommend(movie_input)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(move[0])
        st.image(posters[0])

    with col2:
        st.text(move[1])
        st.image(posters[1])

    with col3:
        st.text(move[2])
        st.image(posters[2])

    with col4:
        st.text(move[3])
        st.image(posters[3])

    with col5:
        st.text(move[4])
        st.image(posters[4])
