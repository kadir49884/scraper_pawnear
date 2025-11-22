# 🤖 Pawnear - Multi-Site Scraper

Günde bir kez otomatik olarak çalışan, kayıp/sahiplendirme ilanlarını tarayan modüler Python scraper.

## 🌐 Desteklenen Siteler

- ✅ **GorenDuyan.com** - Kedi & Köpek (Son 24 saat)
- ✅ **Petcim.com** - Satılık Kedi İlanları (Son 24 saat)

## 🛠️ Özellikler

- 🔄 Modüler yapı - Yeni siteler kolayca eklenebilir
- 🤖 CloudScraper - Bot korumasını aşar
- 📅 Otomatik tarih filtreleme (son 24 saat)
- 🚫 Duplikasyon önleme
- 📱 Telegram bildirimleri
- ⏰ GitHub Actions ile günlük otomatik çalışma (09:00 UTC)

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
Her gün 09:00 UTC'de otomatik çalışır ve sonuçları:
- `data/ilanlar.json` dosyasına kaydeder
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

1. `scrapers/` klasörüne yeni scraper ekle (örn: `yenisite_scraper.py`)
2. `BaseScraper` sınıfından türet
3. `scrape()`, `parse_listings()`, `extract_details()` metodlarını implement et
4. `scraper_manager.py`'ye ekle

Örnek:
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
```

## 📊 Yapı

```
scrapers/
├── __init__.py
├── base_scraper.py         # Abstract base class
├── selenium_scraper.py     # CloudScraper wrapper
├── gorenduyan_scraper.py   # GorenDuyan implementasyonu
├── petcim_scraper.py       # Petcim implementasyonu
└── scraper_manager.py      # Tüm scraper'ları yönetir

github_scraper.py            # Ana script
requirements.txt             # Bağımlılıklar
```

## 🔐 Secrets (GitHub Actions)

Gerekli secrets:
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`
- `GITHUB_TOKEN` (otomatik)

## 📝 Lisans

MIT

---

🐾 Made with ❤️ for lost pets
