[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://io-cinematch.streamlit.app/)

# 🎬 CineMatch v2: Smart Recommendation System

CineMatch is a sophisticated content-based recommendation engine built with **Python** and **Streamlit**. It leverages **Machine Learning (Cosine Similarity)** to suggest personalized movies and TV series, enriched with real-time data from the **TMDB API**.

##  Key Features

* ** Smart Recommendation Engine:** Analyzes over 10,000+ contents to find the best matches based on plot, genre, and keywords.
* **  Dual Support (Movies & Series):** Seamlessly handles recommendations for both Movies and TV Shows.
* ** Real-Time Data Fetching:** Automatically pulls the latest posters, trailers, cast details, and overview from TMDB API.
* ** Advanced Filtering:**
    * Filter by **Year Range** (e.g., 1990-2026).
    * Filter by **IMDB Score** (e.g., 7.0+).
    * Filter by **Content Type** (Movies Only / Series Only).
* **🔖 Bookmarking System:** Users can save their favorite recommendations to a session-based list.
* ** Rich Media Integration:** Watch trailers directly within the app or use the "Google It" button for reviews.
* ** Responsive UI:** A modern, dark-mode interface with an interactive sidebar.

##  Tech Stack

* **Frontend:** Streamlit
* **Backend:** Python 3.x
* **Data Processing:** Pandas
* **Machine Learning:** Scikit-Learn (Cosine Similarity)
* **API:** The Movie Database (TMDB) API

##  Installation & Setup

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/irmakoznrgz/CineMatch-v2.git](https://github.com/irmakoznrgz/CineMatch-v2.git)
    cd CineMatch-v2
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set Up API Key**
    * Create a `.env` file in the root directory.
    * Add your TMDB API Key:
        ```env
        TMDB_API_KEY=your_api_key_here
        ```

4.  **Run the App**
    ```bash
    streamlit run main.py
    ```

##  Project Structure

* `main.py`: The core application code containing UI, logic, and API handling.
* `requirements.txt`: List of dependencies required to run the app.
* `models/`: Contains pre-trained pickle files (`movie_dict.pkl`, `vectors.pkl`).
* `.env`: Stores sensitive API keys (not included in the repo).

---

### 👨‍💻 Developer
**Irmak Öznergiz** Statistics Student @ Ankara University  
[GitHub Profile](https://github.com/irmakoznrgz)
