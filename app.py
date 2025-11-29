import streamlit as st
import joblib
import pandas as pd
from huggingface_hub import hf_hub_download

st.set_page_config(page_title="Movie PaYo", page_icon="🎬")

# ---- Load movie data ----
try:
    movie = joblib.load('movie_data.pkl')
except FileNotFoundError:
    st.error("Error: 'movie_data.pkl' not found.")
    st.stop()


# ---- Load similarity model with caching ----
@st.cache_resource
def load_similarity_model():
    model_path = hf_hub_download(
        repo_id="shekhsahebali/Movie-Recommendation-Model",
        filename="model.pkl"
    )
    with open(model_path, "rb") as f:
        return joblib.load(f)

try:
    similarity = load_similarity_model()
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()


# ---- Streamlit UI ----
st.title("🎬 Movie Recommendation System")

movie_titles = movie['title'].unique().tolist()
movie_title_input = st.selectbox("Select a movie title:", movie_titles, key="recommend_title_input")

number_of_recommendations = st.slider(
    "How many recommendations to get?",
    min_value=2,
    max_value=100,
    value=10,
    key="recommend_num"
)

if st.button("Get Recommendations", key="recommend_button"):
    if movie_title_input:
        try:
            idx = movie[movie['title'] == movie_title_input].index[0]
            distances = list(enumerate(similarity[idx]))
            recommended_indices = sorted(distances, key=lambda x: x[1], reverse=True)[1:number_of_recommendations + 1]
            recommendations = [movie.iloc[i[0]].title for i in recommended_indices]

            if recommendations:
                st.subheader(f"Recommendations for '{movie_title_input}':")
                for i, rec_movie in enumerate(recommendations):
                    st.write(f"{i+1}. {rec_movie}")
            else:
                st.info(f"Couldn't find any recommendations for '{movie_title_input}'.")

        except IndexError:
            st.warning(f"Movie '{movie_title_input}' not found in our database. Please try another title.")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
    else:
        st.warning("Please select a movie title to get recommendations.")
