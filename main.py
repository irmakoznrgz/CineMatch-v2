import streamlit as st
import pickle
import pandas as pd
import requests
import os
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity

load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")

@st.cache_data(show_spinner=False)

def fetch_poster(movie_title, content_type):

    ctype_clean = str(content_type).strip().lower()

    if ctype_clean == "Movie":
        url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_title}"
    else:
        url = f"https://api.themoviedb.org/3/search/tv?api_key={API_KEY}&query={movie_title}"

    default_data = {
        "poster": "https://via.placeholder.com/500x750?text=No+Image",
        "year": "Unknow",
        "info_text": "",
        "rating": 0.0,
    }

    try:
        response = requests.get(url, timeout=5) 
        if response.status_code == 200:
            data = response.json() 
            results = data.get('results', []) 
            
            if results:
                item = results[0]

                tmdb_id = item.get('id')

                poster_path = item.get('poster_path')
                poster_url = f"https://image.tmdb.org/t/p/w300{poster_path}" if poster_path else default_data["poster"]
                
                if content_type == "Movie":
                    date_str = item.get('release_date') 
                else:
                    date_str = item.get('first_air_date')

                year = date_str.split('-')[0] if date_str else "N/A"

                rating = round(item.get('vote_average', 0), 1)

                info_text = "N/A"

                try:
                    target_type = 'movie' if content_type == 'Movie' else 'tv'

                    details_url = f"https://api.themoviedb.org/3/{target_type}/{tmdb_id}?api_key={API_KEY}"

                    details_resp = requests.get(details_url, timeout=3).json()

                    if content_type == 'movie':
                        runtime = details_resp.get('runtime', 0)
                        if runtime > 0:
                            hours = runtime // 60
                            minutes = runtime % 60
                            info_text = f"{hours}h {minutes}m"

                    else:
                        seasons = details_resp.get('number_of_seasons', 0)
                        info_text = f"{seasons} Season"
                except:
                    pass
                
                return {
                    "poster": poster_url,
                    "year": year,
                    "info_text": info_text,
                    "rating": rating
                }

    except Exception as e:
        print(f"Error! {e}")
    
    return default_data

@st.cache_resource
def load_data():
    movies_dict = pickle.load(open('models/movie_dict.pkl', 'rb'))
    movies = pd.DataFrame(movies_dict)
    vectors = pickle.load(open('models/vectors.pkl', 'rb'))
    return movies, vectors

movies, vectors = load_data()

st.set_page_config(page_title="CineMatch v2", layout="wide", page_icon="🎬")
st.title("🎬 CineMatch: Smart Recommendations System")

selected_content = st.selectbox(
    "Which movie or series did you like?",
    movies['title'].unique(),
    index=None,
    placeholder="Write or select a content name...."
)

col_btn, col_filter, col_spacer = st.columns([0.6,0.8,4])

with col_btn:
    btn_clicked = st.button('Get Similar')

with col_filter:
    filtering_content = st.selectbox(
        "Filter:",
        ["All", "Movies Only", "Series Only"],
        index=None,
        placeholder="Filter",
        label_visibility="collapsed"
    )

if btn_clicked:
    if selected_content:
        current_filter = filtering_content if filtering_content else "All"

        with st.spinner('Loading...'):
            idx = movies[movies['title'] == selected_content].index[0]
            distances = cosine_similarity(vectors[idx], vectors).flatten()

            all_indices = distances.argsort()[::-1]

            st.write(f"Recommended for you:")

            cols = st.columns(5)

            recommended_indices = []
            for i in all_indices:
                title = movies.iloc[i].title
                ctype = movies.iloc[i].type

                if title == selected_content:
                    continue

                if current_filter == "Movies Only" and ctype != "Movie":
                    continue
                if current_filter == "Series Only" and ctype != "Series":
                    continue

                recommended_indices.append(i)

                if len(recommended_indices) == 5:
                    break
            
            
            for col_idx, movie_idx in enumerate(recommended_indices):
                title = movies.iloc[movie_idx].title
                movie_type = movies.iloc[movie_idx].type

                info = fetch_poster(title, movie_type)
                
                with cols[col_idx]:
                    st.image(info['poster'], width=150) 
                    st.markdown(f"**{title}**")
                    st.caption(f"{movie_type} ({info['year']}) {info['info_text']}")
                    st.caption(f"⭐ {info['rating']}/10")

    else:
        st.warning("Please select a content first!")