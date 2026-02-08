# 🎬 CineMatch v2: Smart Recommendation System

CineMatch is a content-based recommendation engine built with **Python** and **Streamlit**. It suggests similar movies and TV series based on user selection, utilizing vector similarity and real-time data from the **TMDB API**.

## Features
* **Smart Recommendation Engine:** Uses Cosine Similarity to find the most relevant content from a dataset of 170,000+ movies and series.
* **Dual Support:** Seamlessly handles both **Movies** and **TV Series**.
* **Advanced Filtering:** Users can filter results to show "All", "Movies Only", or "Series Only".
* **Real-Time Data:** Fetches up-to-date posters, ratings, release years, and duration/season details via TMDB API.
* **Clean UI:** A modern, responsive interface built with Streamlit's latest features.
* **Smart Search:** Handles duplicate titles and case-sensitivity issues for a smooth user experience.

##  Tech Stack
* **Python 3.x**
* **Streamlit** (Frontend)
* **Pandas & Scikit-Learn** (Data Processing & Similarity)
* **TMDB API** (Live Metadata & Images)

##  Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/irmakoznrgz/CineMatch-v2.git](https://github.com/irmakoznrgz/CineMatch-v2.git)
    cd CineMatch-v2
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up API Key:**
    * Create a `.env` file in the root directory.
    * Add your TMDB API key:
        ```env
        TMDB_API_KEY=your_api_key_here
        ```

4.  **Run the App:**
    ```bash
    streamlit run main.py
    ```


##  Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

---
*Developed by Irmak Öznergiz*