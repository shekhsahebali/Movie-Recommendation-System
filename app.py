import streamlit as st
import joblib
import pandas as pd
import requests

API_KEY = st.secrets["TMDB_API_KEY"]

def get_poster(movie_title):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_title}"
    response = requests.get(url).json()
    
    results = response.get("results")
    if results:
        poster_path = results[0]["poster_path"]
        if poster_path:
            full_path = f"https://image.tmdb.org/t/p/w200{poster_path}"  # smaller size
            return full_path
    return None

st.set_page_config(page_title="Movie PaYo", page_icon="🎬")

# ------------------ Load data ------------------
try:
    movie = joblib.load("movie_data.pkl")
except FileNotFoundError:
    st.error("Error: 'movie_data.pkl' not found.")
    st.stop()

try:
    top_recommendations = joblib.load("model20.pkl")  # small dict
except FileNotFoundError:
    st.error("Error: 'model20.pkl' not found.")
    st.stop()

# ------------------ Streamlit UI ------------------
st.title("🎬 Movie Recommendation System")

movie_titles = movie['title'].unique().tolist()
movie_title_input = st.selectbox("Select a movie title:", movie_titles, key="recommend_title_input")

number_of_recommendations = st.slider(
    "How many recommendations to get?",
    min_value=2,
    max_value=20,  
    value=10,
    key="recommend_num"
)

if st.button("Get Recommendations", key="recommend_button"):
    if movie_title_input:
        try:
            recommendations = top_recommendations.get(movie_title_input, [])[:number_of_recommendations]

            if recommendations:
                st.subheader(f"Recommendations for '{movie_title_input}':")
                num_columns = 5 
                for i in range(0, len(recommendations), num_columns):
                    cols = st.columns(num_columns)
                    for j, rec_movie in enumerate(recommendations[i:i+num_columns]):
                        with cols[j]:
                            st.text(rec_movie)
                            poster_url = get_poster(rec_movie)
                            if poster_url:
                                st.image(poster_url, use_column_width=True)
            else:
                st.info(f"No recommendations found for '{movie_title_input}'.")

        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
    else:
        st.warning("Please select a movie title to get recommendations.")
