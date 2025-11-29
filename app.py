import streamlit as st
import joblib
import random
import pandas as pd
from huggingface_hub import hf_hub_download

st.set_page_config(page_title="Movie PaYo", page_icon="🎬")


try:
    movie = joblib.load('movie_data.pkl')
except FileNotFoundError:
    st.error("Error: 'movie_data.pkl' not found.")
    st.stop() 

@st.cache_resource
def load_similarity_model():
    model_path = hf_hub_download(
        repo_id="ssask12/Movie-Recommendation-Model",
        filename="model.pkl"
    )
    with open(model_path, "rb") as f:
        return joblib.load(f)


try:
    # similarity = joblib.load('model.pkl')
     similarity = load_similarity_model()
    
except FileNotFoundError:
    st.error("Error: 'model.pkl' not found.")
    st.stop()


st.title("🎬 Movie Recommendation System")


movie_titles = movie['title'].unique().tolist()
movie_title_input = st.selectbox("select a movie title:", movie_titles, key="recommend_title_input")

number_of_recommendations = st.slider("how many recommendations to get?", min_value=2, max_value=100, value=10, key="recommend_num")

if st.button("get recommendations", key="recommend_button"):
    if movie_title_input: 
        try:
          
            idx = movie[movie['title'] == movie_title_input].index[0]
            
            distances = list(enumerate(similarity[idx]))
        
            recommended_indices = sorted(distances, key=lambda x: x[1], reverse=True)[1:number_of_recommendations + 1]
            
            recommendations = [movie.iloc[i[0]].title for i in recommended_indices]

            if recommendations:
                st.subheader(f"recommendations for '{movie_title_input}':")
                for i, rec_movie in enumerate(recommendations):
                    st.write(f"{i+1}. {rec_movie}")
            else:
                st.info(f"couldn't find any recommendations for '{movie_title_input}'.")

        except IndexError:
            
            st.warning(f"movie '{movie_title_input}' not found in our database. please try another title.")
        except Exception as e:
            st.error(f"an unexpected error occurred: {e}")
    else:
        st.warning("please select a movie title to get recommendations.")