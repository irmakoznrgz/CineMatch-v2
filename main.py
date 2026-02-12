import streamlit as st
import pickle
import pandas as pd
import requests
import os
import urllib.parse
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity

load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")

GENRE_MAP = { 
    28: 'Action', 12: 'Adventure', 16: 'Animation', 35: 'Comedy', 80: 'Crime', 
    99: 'Documentary', 18: 'Drama', 10751: 'Family', 14: 'Fantasy', 36: 'History', 
    27: 'Horror', 10402: 'Music', 9648: 'Mystery', 10749: 'Romance', 878: 'Sci-Fi', 
    10770: 'TV Movie', 53: 'Thriller', 10752: 'War', 37: 'Western', 
    10759: 'Action & Adventure', 10762: 'Kids', 10763: 'News', 10764: 'Reality', 
    10765: 'Sci-Fi & Fantasy', 10766: 'Soap', 10767: 'Talk', 10768: 'War & Politics'
}

if 'bookmarks' not in st.session_state:
    st.session_state.bookmarks = []

if 'search_state' not in st.session_state:
    st.session_state.search_state = False
if 'last_selected_movie' not in st.session_state:
    st.session_state.last_selected_movie = ""

@st.cache_data(show_spinner=False)
def fetch_poster(movie_title, content_type):
    encoded_title = urllib.parse.quote(movie_title)

    default_data = {
        "poster": "https://via.placeholder.com/154x231?text=No+Image",
        "year": "N/A",
        "year_int": 0,
        "info_text": "",
        "rating": 0.0,
        "genres": "",
        "type_label": "Unknown",
        "trailer": None,
        "overview": "No overview available.", 
        "cast": [] 
    }

    url = f"https://api.themoviedb.org/3/search/multi?api_key={API_KEY}&query={encoded_title}"

    try:
        response = requests.get(url, timeout=3) 
        if response.status_code == 200:
            data = response.json() 
            results = data.get('results', []) 
            
            if results:
                item = results[0]
                tmdb_id = item.get('id')
                media_type = item.get('media_type', str(content_type).lower())
                
                type_label = "Movie" if media_type == 'movie' else "Series"

                poster_path = item.get('poster_path')
                poster_url = f"https://image.tmdb.org/t/p/w400{poster_path}" if poster_path else default_data["poster"]
                
                date_str = item.get('release_date') if 'release_date' in item else item.get('first_air_date')
                year = date_str.split('-')[0] if date_str else "N/A"

                year_int = int(year) if year.isdigit() else 0

                rating = round(item.get('vote_average', 0), 1)

                overview = item.get('overview', 'No overview available.')

                genre_ids = item.get('genre_ids', [])
                genre_names = [GENRE_MAP.get(g_id) for g_id in genre_ids if g_id in GENRE_MAP]
                genres_str = " / ".join(genre_names[:2]) 

                info_text = ""
                trailer_url = None
                cast_list = []

                try:
                    target_endpoint = 'movie' if media_type == 'movie' else 'tv'
                    
                    details_url = f"https://api.themoviedb.org/3/{target_endpoint}/{tmdb_id}?api_key={API_KEY}&append_to_response=videos,credits"
        
                    details = requests.get(details_url, timeout=2).json()

                    if target_endpoint == 'movie':   
                        runtime = details.get('runtime', 0)
                        if runtime > 0:
                            h = runtime // 60
                            m = runtime % 60
                            info_text = f"{h}h {m}m"
                    else:
                        seasons = details.get('number_of_seasons', 0)
                        if seasons > 0:
                            suffix = "Season" if seasons == 1 else "Seasons"
                            info_text = f"{seasons} {suffix}"
                    
                    videos = details.get('videos', {}).get('results', [])
                    for video in videos:
                        if video.get('site') == 'YouTube' and video.get('type') == 'Trailer':
                            trailer_url = f"https://www.youtube.com/watch?v={video.get('key')}"
                            break
                    if not trailer_url:
                        for video in videos:
                            if video.get('site') == 'YouTube' and video.get('type') == 'Teaser':
                                trailer_url = f"https://www.youtube.com/watch?v={video.get('key')}"
                                break
                    
                
                    credits = details.get('credits', {})
                    cast_data = credits.get('cast', [])
                    
                    for actor in cast_data[:5]:
                        cast_list.append(actor.get('name'))

                except:
                    pass
                
                return {
                    "poster": poster_url,
                    "year": year,
                    "year_int": year_int,
                    "info_text": info_text,
                    "rating": rating,
                    "genres": genres_str,
                    "type_label": type_label,
                    "trailer": trailer_url,
                    "overview": overview, 
                    "cast": cast_list     
                }

    except Exception:
        pass
    
    return default_data

@st.cache_resource
def load_data():
    movies_dict = pickle.load(open('models/movie_dict.pkl', 'rb'))
    movies = pd.DataFrame(movies_dict)
    vectors = pickle.load(open('models/vectors.pkl', 'rb'))
    return movies, vectors

movies, vectors = load_data()

st.set_page_config(page_title="CineMatch v2", layout="wide", page_icon="🎬")

with st.sidebar:
    st.title("Menu")

    st.markdown("Filters")
    filter_type = st.radio("Content Type", ["All", "Movies Only", "Series Only"])
    year_range = st.slider("Year Range", 1980, 2026, (1990, 2026))
    min_rating = st.slider("Min IMDB Scroe", 0.0, 10.0, 5.0)

    st.markdown("---")

    st.markdown("🔖 Bookmarked")
    if st.session_state.bookmarks:
        for i, bookmarked_item in enumerate(st.session_state.bookmarks):
            st.write(f"{i+1}. {bookmarked_item}")

        if st.button("Clear All Bookmarks"):
            st.session_state.bookmarks = []
            st.rerun()
    else:
        st.caption("Your bookmarks list is empty.")

    st.markdown("---")
    st.markdown("### 👨‍💻 Developer")
    st.info("**Irmak Öznergiz**\n\nStatistic Student @Ankara Uni.\n\n[GitHub Profile](https://github.com/irmakoznrgz)")

st.title("🎬 CineMatch: Smart Recommendations System")

selected_content = st.selectbox(
    "Which movie or series did you like?",
    movies['title'].unique(),
    index=None,
    placeholder="Write or select a content name...."
)

if st.button('Find Recommendations', type="primary", use_container_width=True):
    st.session_state.search_state = True

    st.session_state.last_selected_movie = selected_content

if st.session_state.search_state and st.session_state.last_selected_movie:

    target_movie = st.session_state.last_selected_movie

    with st.spinner('Applying filters & Searching database...'):
        try:
            idx = movies[movies['title'] == target_movie].index[0]
            distances = cosine_similarity(vectors[idx], vectors).flatten()
            all_indices = distances.argsort()[::-1]

            st.write(f"### Recommended For You:")

            cols = st.columns(5)
            count = 0

            for i in all_indices:
                title = movies.iloc[i].title
                local_type = str(movies.iloc[i].type).strip().lower()

                if title == selected_content: continue

                if filter_type == "Movies Only" and local_type != "movie": continue
                if filter_type == "Series Only" and local_type != "series": continue


                info = fetch_poster(title, movies.iloc[i].type)
                
                if info['year_int'] < year_range[0] or info['year_int'] > year_range[1]: continue

                if info['rating'] < min_rating: continue

                with cols[count]:
                    try:
                        st.image(info['poster'], width=150) 
                    except:
                        st.write("🖼️")

                    st.markdown(f"**{title}**")

                    row1 = []
                    if info['type_label'] != "Unknown": row1.append(info['type_label'])
                    if info['info_text']: row1.append(info['info_text'])
                    if row1:
                        st.caption(" • ".join(row1))

                    row2 = []
                    if info['year']: row2.append(f"({info['year']})")
                    if info['genres']: row2.append(info['genres'])
                    if row2:
                        st.caption(" • ".join(row2))
                    
                    if info['rating'] > 0:
                        st.caption(f"⭐ {info['rating']}/10")

                    is_bookmarked = title in st.session_state.bookmarks

                    bookmark_label = "✅" if is_bookmarked else "🔖"
                    btn_type = "primary" if is_bookmarked else "secondary"

                    if st.button(bookmark_label, type=btn_type, key=f"save_{i}", use_container_width=True):
                        if is_bookmarked:
                            st.session_state.bookmarks.remove(title)
                            st.toast(f"Removed: {title}", icon="🗑️")
                        else:
                            st.session_state.bookmarks.append(title)
                            st.toast(f"Saved: {title}", icon="🔖")
                        st.rerun()
                   
                    if info['trailer']:
                        st.link_button("▶ Watch Trailer", info['trailer'], use_container_width=True)
                    else:
                        st.caption("No Trailer Available")

                    search_url = f"https://www.google.com/search?q={title} {info['year']} review"
                    st.link_button("🔍 Google It", search_url, use_container_width=True)
                   
                    with st.expander("Details"):
                        if info['cast']:
                            st.markdown("**Cast:**")
                            st.caption(", ".join(info['cast']))
                        
                        if info['overview']:
                            st.markdown("**Plot:**")
                            st.caption(info['overview'][:300] + "..." if len(info['overview']) > 300 else info['overview'])
                count += 1
                if count == 5: break

            if count == 0:
                st.error("No results found. Try adjusting the filters.")

        except IndexError:
            st.error("Movie not found in database. Please try another one.")
