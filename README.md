# Gören Duyan Scraper 🐾

**Otomatik kayıp kedi & köpek ilanı takip sistemi**

[![Günlük İlan Scraper](https://github.com/kadir49884/scraper_pawnear/actions/workflows/scraper.yml/badge.svg)](https://github.com/kadir49884/scraper_pawnear/actions/workflows/scraper.yml)

## 🎯 Özellikler

✅ **GitHub Actions** ile tamamen ücretsiz  
✅ **Günlük otomatik tarama** (her gün 12:00 TR)  
✅ **Telegram bildirimi** 📱  
✅ **Son 24 saat filtreleme**  
✅ **Duplicate temizleme**  
✅ **2 tarih formatı** (Göreceli + ISO 8601)  
✅ **Görsel URL çekme**  
✅ **JSON formatında** sonuçlar  
✅ **Kredi kartı gerektirmez!**  

---

## 🔔 Telegram Bildirimi Kurulumu

### 1️⃣ Telegram Bot Oluştur

1. [@BotFather](https://t.me/BotFather)'a git
2. `/newbot` komutunu gönder
3. Bot adı ve username belirle
4. **Bot Token'ı kopyala**

### 2️⃣ Chat ID Bul

1. Bot'una mesaj gönder
2. Tarayıcıda aç:
   ```
   https://api.telegram.org/bot<TOKEN>/getUpdates
   ```
3. `"chat":{"id":` kısmından **Chat ID**'yi kopyala

### 3️⃣ GitHub Secrets Ekle

1. Repository → **Settings** → **Secrets and variables** → **Actions**
2. **New repository secret** tıkla
3. İki secret ekle:

   **İlk Secret:**
   - Name: `TELEGRAM_BOT_TOKEN`
   - Secret: Bot token'ınız (örn: `123456789:ABCdefGHI...`)
   
   **İkinci Secret:**
   - Name: `TELEGRAM_CHAT_ID`
   - Secret: Chat ID'niz (örn: `123456789`)

4. **Add secret** tıkla

### 4️⃣ Test Et

1. Actions → "Günlük İlan Scraper" → **Run workflow**
2. ✅ Telegram'a bildirim gelecek!

---

## 📊 Sonuçlar

### JSON Dosyaları
```
data/
├── latest.json           → Tüm ilanlar (son tarama)
├── kedi_latest.json      → Sadece kedi
├── kopek_latest.json     → Sadece köpek
└── 20251122_120000.json  → Tarihli yedek
```

### 🌐 URL Erişimi
```
https://raw.githubusercontent.com/kadir49884/scraper_pawnear/main/data/latest.json
https://raw.githubusercontent.com/kadir49884/scraper_pawnear/main/data/kedi_latest.json
https://raw.githubusercontent.com/kadir49884/scraper_pawnear/main/data/kopek_latest.json
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

## 📱 Telegram Bildirimi Örneği

```
🤖 Gören Duyan Scraper

✅ Tarama tamamlandı!

📊 Sonuçlar:
• Toplam: 5 ilan
• 🐱 Kedi: 3
• 🐕 Köpek: 2

🕐 Tarih: 2025-11-22 12:00

🔗 Sonuçları Görüntüle
```

---

## 🔧 Ayarlar

### Workflow Permissions

1. Settings → Actions → General
2. "Workflow permissions" bölümünde:
   - ✅ "Read and write permissions"
   - ✅ "Allow GitHub Actions to create and approve pull requests"
3. Save

### Zamanı Değiştir

`.github/workflows/scraper.yml`:
```yaml
schedule:
  - cron: '0 9 * * *'  # Her gün 09:00 UTC

# Örnekler:
# '0 */6 * * *'  → Her 6 saatte
# '0 12 * * *'   → Her gün 12:00 UTC
# '0 0 * * 1'    → Her Pazartesi 00:00
```

---

## 📝 Yerel Test

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
- Telegram: Ücretsiz
- Kredi kartı **GEREKTIRMEZ**

---

## 📚 Detaylı Dokümantasyon

- [Kurulum Rehberi](GITHUB_ACTIONS_KURULUM.md)

---

## 📄 Lisans

MIT License - Detaylar için [LICENSE](LICENSE) dosyasına bakın.

---

## 🙏 Teşekkürler

[Gören Duyan](https://www.gorenduyan.com/) - Kayıp hayvan ilanları platformu

---

**Made with ❤️ | 🐱 Kedi | 🐕 Köpek | 🤖 GitHub Actions | 📱 Telegram**

