# ScraperPawNear 🐾

Otomatik hayvan ilanları scraper ve Telegram bildirimi sistemi.

## Özellikler

- **Multi-Site Scraping**: GorenDuyan, Petcim, Petlebi sitelerinden otomatik ilan çekme
- **Günlük Tarama**: Her gün saat 12:00'da otomatik tarama
- **Sosyal Medya Paylaşımı**: Günde 4 kez otomatik paylaşım (Facebook, Twitter, Instagram)
- **Telegram Bildirimi**: Paylaşım sonuçları Telegram'dan bildirilir
- **GitHub Actions**: Tamamen otomatik, sunucusuz çalışma
- **Clean Code**: Modüler ve genişletilebilir yapı

## Paylaşım Zamanlaması

| Saat  | İlan | Platform |
|-------|------|----------|
| 13:00 | 1.   | Facebook, Twitter, Instagram |
| 18:00 | 11.  | Facebook, Twitter, Instagram |
| 19:00 | 21.  | Facebook, Twitter, Instagram |
| 20:00 | 31.  | Facebook, Twitter, Instagram |

## Kurulum

1. Repository'yi fork edin
2. GitHub Secrets ekleyin:
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`
3. GitHub Actions'ı etkinleştirin

## Dosya Yapısı

```
├── scrapers/                  # Scraper modülleri
│   ├── base_scraper.py       # Temel scraper sınıfı
│   ├── gorenduyan_scraper.py # GorenDuyan sitesi
│   ├── petcim_scraper.py     # Petcim sitesi
│   └── petlebi_scraper.py    # Petlebi sitesi
├── github_scraper.py         # Ana scraper (12:00)
├── scheduled_telegram.py     # Zamanlanmış mesajlar
├── send_telegram.py          # Özet bildirim
└── data/                     # JSON veriler
    ├── ilanlar.json          # Son durum
    └── ilan_taramasi_*.json  # Günlük arşiv
```

## Kullanım

### Lokal Test
```bash
# Scraping
python github_scraper.py

# Telegram bildirimi
python send_telegram.py

# Zamanlanmış mesaj (saat kontrolü yapar)
python scheduled_telegram.py
```

### Manuel Tetikleme
GitHub Actions sekmesinden workflow'ları manuel çalıştırabilirsiniz.

## Lisans

MIT