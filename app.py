import streamlit as st
import pandas as pd
import pickle
import requests
import requests
import joblib

session = requests.Session()




def poster_fetch(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=9d5cfde9cf8b5435c9ffd08bde76febf"

    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()

        if "poster_path" in data and data["poster_path"]:
            return "https://image.tmdb.org/t/p/w500/" + data["poster_path"]
        else:
            return None

    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None
movie_dic = pickle.load(open('movies_dic.pkl', 'rb'))
movies = pd.DataFrame(movie_dic)
similarity = joblib.load('similarity.joblib')
st.title("Movie Recommender System")
selected = st.selectbox(
    'Enter the movie : ',
    movies['title'].values
)
def recommend(movie):
    movie_idx = movies[movies['title'] == movie].index[0]
    distance = similarity[movie_idx]
    movie_list = sorted(enumerate(distance), reverse=True, key = lambda x:x[1])[1:6]
    recommend_movie = []
    poster = []
    
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommend_movie.append(movies.iloc[i[0]].title)
        poster.append(poster_fetch(movie_id))
    return recommend_movie, poster
    

if st.button('Recommend'):
    names, poster = recommend(selected)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(poster[0])
        
    with col2:
        st.text(names[1])
        st.image(poster[1])
    with col3:
        st.text(names[2])
        st.image(poster[2])
    with col4:
        st.text(names[3])
        st.image(poster[3])
    with col5:
        st.text(names[4])
        st.image(poster[4])
st.markdown(
    "<h4 style='text-align: center;'>Made by Gitansh Swarnkar ❤️</h4>",
    unsafe_allow_html=True
)