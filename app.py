import streamlit as st
import joblib
import pandas as pd

st.set_page_config(page_title="Movie PaYo", page_icon="🎬")


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
                for i, rec_movie in enumerate(recommendations):
                    st.write(f"{i+1}. {rec_movie}")
            else:
                st.info(f"No recommendations found for '{movie_title_input}'.")

        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
    else:
        st.warning("Please select a movie title to get recommendations.")
