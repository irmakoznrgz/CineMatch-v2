# CineMatch - HTML/CSS & Python Static Generator Version

CineMatch projesinin bu dalı (branch), sıfır JavaScript kullanılarak, tamamen HTML, CSS ve Python arka uç (backend) gücüyle inşa edilmiştir. Python, TMDB API'den film verilerini çeker ve anında statik bir `index.html` dosyası üretir.

## Özellikler
- **Python Static Site Generator:** Kendi yazdığımız `main.py` scripti, `sablon.html` dosyasını okur ve API'den gelen verilerle doldurup `index.html` üretir.
- **Karanlık Tema & Full Screen Hero:** Tamamen CSS ile yapılmış sinematik tasarım ve yumuşak kaydırma (smooth scroll) efektleri.
- **Dinamik Film Kartları:** Fare ile üzerine gelindiğinde etkileşime giren şık kalp (beğen) butonları.

## Nasıl Çalıştırılır?

1. Projeyi klonlayın ve bu branch'e geçin.
2. Gerekli kütüphaneleri kurun:
   `pip install -r requirements.txt`
3. Ana dizinde bir `.env` dosyası oluşturun ve TMDB API anahtarınızı ekleyin:
   `TMDB_API_KEY=sizin_api_anahtariniz_buraya`
4. Python scriptini çalıştırarak `index.html` dosyasını üretin:
   `python main.py`
5. Oluşan `index.html` dosyasını herhangi bir tarayıcıda açarak siteyi görüntüleyin.