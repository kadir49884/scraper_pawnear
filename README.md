# 🤖 Pawnear - Multi-Site Scraper

Günde bir kez otomatik olarak çalışan, kayıp/sahiplendirme ilanlarını tarayan modüler Python scraper.

## 🌐 Desteklenen Siteler

1. ✅ **GorenDuyan.com** - Kayıp/Bulundu (Kedi & Köpek)
2. ✅ **Petcim.com** - Satılık (Kedi & Köpek)
3. ✅ **Petlebi.com** - Sahiplendirme (Kedi & Köpek)

**Toplam:** 3 site × 2 kategori = 6 veri kaynağı

## 🛠️ Özellikler

- 🔄 Modüler yapı - Yeni siteler kolayca eklenebilir
- 🤖 CloudScraper - Bot korumasını aşar
- 📅 Otomatik tarih filtreleme (son 24 saat)
- 🚫 Duplikasyon önleme
- 📱 Telegram bildirimleri
- ⏰ GitHub Actions ile günlük otomatik çalışma (09:00 UTC)
- 🔄 Rate limiting ve retry mekanizması
- 📁 Tarihli dosya sistemi (günlük arşiv)

## 📦 Kurulum

```bash
pip install -r requirements.txt
```

## 🚀 Kullanım

### Lokal Çalıştırma
```bash
python github_scraper.py
```

### GitHub Actions (Otomatik)
Her gün 09:00 UTC (12:00 TR)'de otomatik çalışır ve:
- Tarihli JSON oluşturur: `data/ilan_taramasi_2025-11-22.json`
- Son durumu günceller: `data/ilanlar.json`
- Telegram'dan bildirim gönderir

## 📁 Çıktı Formatı

```json
[
  {
    "ilan_turu": "Kayıp",
    "baslik": "...",
    "aciklama": "...",
    "konum": "İl / İlçe",
    "tarih1": "2 Saat Önce",
    "tarih2": "2025-11-22T14:00:00Z",
    "kategori": "Kedi",
    "gorsel": "https://...",
    "link": "https://..."
  }
]
```

## ➕ Yeni Site Ekleme

1. `scrapers/` klasörüne yeni scraper ekle
2. `BaseScraper` sınıfından türet
3. Gerekli metodları implement et
4. `scraper_manager.py`'ye ekle

```python
# scrapers/yenisite_scraper.py
from .base_scraper import BaseScraper

class YeniSiteScraper(BaseScraper):
    def __init__(self):
        super().__init__("YeniSite")
        self.base_url = "https://yenisite.com"
    
    def scrape(self) -> List[Dict]:
        # Site-spesifik scraping mantığı
        pass
    
    def parse_listings(self, soup, kategori: str) -> List[Dict]:
        # HTML parse mantığı
        pass
    
    def extract_details(self, ad: Dict) -> Dict:
        # Detay sayfası mantığı
        pass
```

## 📊 Proje Yapısı

```
scrapers/
├── __init__.py
├── base_scraper.py         # Abstract base class
├── cloud_scraper.py        # CloudScraper (bot bypass)
├── gorenduyan_scraper.py   # GorenDuyan implementasyonu
├── petcim_scraper.py       # Petcim implementasyonu
├── petlebi_scraper.py      # Petlebi implementasyonu
└── scraper_manager.py      # Scraper orchestrator

github_scraper.py            # Ana script
send_telegram.py             # Telegram bildirimi
requirements.txt             # Bağımlılıklar
```

## 🔐 GitHub Secrets

Gerekli secrets:
- `TELEGRAM_BOT_TOKEN` - Bot token
- `TELEGRAM_CHAT_ID` - Chat ID
- `GITHUB_TOKEN` - Otomatik sağlanır

## 📝 Lisans

MIT

---

🐾 Made with ❤️ for lost pets
