import os
import requests
from dotenv import load_dotenv
import urllib3

urllib3.disable_warnings()
load_dotenv()


api_key = os.getenv("TMDB_API_KEY") 

tum_filmler = []

print("Filmler TMDB'den çekiliyor. Lütfen bekle...")
for sayfa_numarasi in range(1, 16):
    url = f"https://api.themoviedb.org/3/movie/popular?api_key={api_key}&language=tr-TR&page={sayfa_numarasi}"
    response = requests.get(url, verify=False, timeout=10)
    veriler = response.json()
    if 'results' in veriler:
        tum_filmler.extend(veriler['results'])

print("HTML kodları oluşturuluyor...")
datalist_html = ""
filmler_html = ""

for film in tum_filmler:
    datalist_html += f'    <option value="{film["title"]}">\n'

    resim_yolu = "https://via.placeholder.com/500x750?text=Resim+Yok"
    if film.get('poster_path'):
        resim_yolu = "https://image.tmdb.org/t/p/w500" + film['poster_path']

    filmler_html += f"""
    <div class="film-karti">
        <div class="poster-alani">
            <img src="{resim_yolu}" alt="{film['title']}">
            
            <button class="begen-butonu" title="Beğenilenlere Ekle">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12Z" />
                </svg>
            </button>
        </div>
        <div class="film-bilgi">
            <h3>{film['title']}</h3>
            <span class="puan">{round(film['vote_average'], 1)}</span>
        </div>
    </div>
    """

print("sablon.html okunuyor ve index.html dosyası inşa ediliyor...")

with open("sablon.html", "r", encoding="utf-8") as dosya:
    sablon_icerik = dosya.read()

yeni_icerik = sablon_icerik.replace("[DATALIST_BURAYA]", datalist_html)
yeni_icerik = yeni_icerik.replace("[FILMLER_BURAYA]", filmler_html)

with open("index.html", "w", encoding="utf-8") as dosya:
    dosya.write(yeni_icerik)

print("✅ BAŞARILI! 300 film index.html dosyasına sorunsuz bir şekilde yazıldı!")