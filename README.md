# Gören Duyan Scraper 🐾

**Otomatik kayıp kedi & köpek ilanı takip sistemi**

[![Günlük İlan Scraper](https://github.com/USERNAME/goren-duyan-scraper/actions/workflows/scraper.yml/badge.svg)](https://github.com/USERNAME/goren-duyan-scraper/actions/workflows/scraper.yml)

## 🎯 Özellikler

✅ **GitHub Actions** ile tamamen ücretsiz  
✅ **Günlük otomatik tarama** (her gün 12:00 TR)  
✅ **Son 24 saat filtreleme**  
✅ **Duplicate temizleme**  
✅ **2 tarih formatı** (Göreceli + ISO 8601)  
✅ **Görsel URL çekme**  
✅ **JSON formatında** sonuçlar  
✅ **Kredi kartı gerektirmez!**  

---

## 🚀 Hızlı Başlangıç

### 1. Repository Oluştur
```bash
git init
git add .
git commit -m "İlk commit"
git branch -M main
git remote add origin https://github.com/USERNAME/goren-duyan-scraper.git
git push -u origin main
```

### 2. Actions Aktifleştir
1. Repository → **Actions** tab
2. "Enable workflows" tıkla
3. ✅ Tamam!

### 3. Manuel Test
1. Actions → "Günlük İlan Scraper"
2. **Run workflow** → Run workflow
3. ✅ Hemen çalışır!

**Detaylı kurulum:** [`GITHUB_ACTIONS_KURULUM.md`](GITHUB_ACTIONS_KURULUM.md)

---

## 📊 Sonuçlar

### JSON Dosyaları
```
data/
├── latest.json           → Tüm ilanlar (son tarama)
├── kedi_latest.json      → Sadece kedi ilanları
├── kopek_latest.json     → Sadece köpek ilanları
└── 20251122_120000.json  → Tarihli yedek
```

### URL Erişimi
```
https://raw.githubusercontent.com/USERNAME/goren-duyan-scraper/main/data/latest.json
https://raw.githubusercontent.com/USERNAME/goren-duyan-scraper/main/data/kedi_latest.json
https://raw.githubusercontent.com/USERNAME/goren-duyan-scraper/main/data/kopek_latest.json
```

### JSON Formatı
```json
{
  "ilan_turu": "Kayıp",
  "baslik": "Köpeğim kayboldu",
  "aciklama": "...",
  "konum": "İstanbul / Kadıköy",
  "tarih1": "10 Saat Önce",
  "tarih2": "2025-11-21T14:00:00Z",
  "kategori": "Köpek",
  "gorsel": "https://www.gorenduyan.com/images/...",
  "link": "https://www.gorenduyan.com/...",
  "scraped_at": "2025-11-21T14:00:00Z"
}
```

---

## ⏰ Çalışma Zamanı

- **Otomatik:** Her gün 09:00 UTC (12:00 TR)
- **Manuel:** Actions → Run workflow

**Zamanı değiştirmek için:** `.github/workflows/scraper.yml` → `cron` değerini düzenle

---

## 📱 Kullanım Örnekleri

### JavaScript
```javascript
fetch('https://raw.githubusercontent.com/USERNAME/goren-duyan-scraper/main/data/latest.json')
  .then(res => res.json())
  .then(data => console.log(data));
```

### Python
```python
import requests
data = requests.get('https://raw.githubusercontent.com/USERNAME/goren-duyan-scraper/main/data/latest.json').json()
print(f"Toplam: {data['toplam']} ilan")
```

### cURL
```bash
curl https://raw.githubusercontent.com/USERNAME/goren-duyan-scraper/main/data/latest.json
```

---

## 🔧 Yerel Test

```bash
# Dependencies kur
pip install -r requirements.txt

# Scraper'ı çalıştır
python github_scraper.py

# Sonuçlar data/ klasöründe
ls data/
```

---

## 💰 Maliyet

**TAMAMEN ÜCRETSİZ!** ✅

- GitHub Actions: 2000 dakika/ay ücretsiz
- Bu proje: ~2-3 dakika/gün (~60-90 dakika/ay)
- Kredi kartı **GEREKTIRMEZ**

---

## 📝 Loglar

1. Repository → **Actions**
2. Son çalışmayı tıkla
3. "scrape" job'ı aç
4. Tüm detayları gör

---

## 🤝 Katkıda Bulunun

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing`)
3. Commit edin (`git commit -m 'Add amazing feature'`)
4. Push edin (`git push origin feature/amazing`)
5. Pull Request açın

---

## 📄 Lisans

MIT License

---

## 🙏 Teşekkürler

[Gören Duyan](https://www.gorenduyan.com/) - Kayıp hayvan ilanları platformu

---

**Made with ❤️ | 🐱 Kedi | 🐕 Köpek | 🤖 GitHub Actions**

