import streamlit as st
import pickle
import pandas as pd
import requests
import os
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity

load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")

def fetch_poster(title):
    base_url = "https://api.themoviedb.org/3/"
    url = f"{base_url}search/multi?api_key={API_KEY}&query={title}"

    try:
        response = requests.get(url)
        data = respo.json()

        if data['result']:
            poster_path = data['result'][0].get('poster_path')
            if poster_path:
                return "https://image.tmdb.org/t/p/w500/" + poster_path

    except Exception as e:
        print(f"Connection Error: {e}")
    return "https://via.placeholder.com/500x750?text=Poster+Bulunamadi"

@st.cache_resource
def load_data():
    movies_dict = pickle.load(open('models/movie_dict.pkl', 'rb'))
    movies = pd.DataFrame(movies_dict)
    vectors = pickle.load(open('models/vectors.pkl', 'rb'))

    return movies, vectors
movies, vectors = load_data()

st.set_page_config(page_title="CineMatch V2", layout="wide")
st.markdown("<h1 style='text-align: center;'>🎬CineMatch: Smart Recommendations System</h1>", unsafe_allow_html=True)

selected_content = st.selectbox(
    "Which movie or series do you like?",
    movies['title'].values,
    index=None,
    placeholder="Choose or type a name."
)

if st.button('Get Similar'):
    if selected_content:
        idx = movies[movies['title'] == selected_content].index[0]
        similarity_scores = cosine_similarity(vectors[idx], vectors).flatten()

        similar_indices = similarity_scores.argsort()[-6:][::-1]

        st.write(f"###If you liked '{selected_content}', you might like:")

        cols = st.columns(5)

        found_count = 0
        for i in similar_indices:
            if movies.iloc[i].title == selected_content: 
                continue

            if found_count >= 5: 
                break

            title = movies.iloc[i].title
            content_type = movies.iloc[i].type
            poster_url = fetch_poster(title)

            with cols[found_count]:
                st.image(poster_url)
                st.markdown(f"**{title}**")
                st.caption(f"{content_type}")
                
            found_count +=1
    else:
        st.warning("Please select content first!")




