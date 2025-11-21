# GitHub Actions Kurulum - Tamamen Ücretsiz! 🎯

## ✅ Avantajlar

- ✅ **Tamamen ücretsiz** (kredi kartı yok!)
- ✅ **Çok kolay kurulum** (5 dakika)
- ✅ **Otomatik çalışır** (günde 1 kez)
- ✅ **JSON dosyaları GitHub'a kaydedilir**
- ✅ **Tarihsel veri** (her çalışma kaydedilir)
- ✅ **2000 dakika/ay ücretsiz** (fazlasıyla yeter)

---

## 🚀 Kurulum (3 Adım)

### 1️⃣ GitHub Repository Oluştur

1. [GitHub](https://github.com/) giriş yap
2. Sağ üst köşe → **"New repository"**
3. Repository adı: `goren-duyan-scraper`
4. **Public** seç (ücretsiz Actions için gerekli)
5. "Create repository"

### 2️⃣ Dosyaları Yükle

**Terminalde:**
```bash
# Git init
git init
git add .
git commit -m "İlk commit"

# Remote ekle (REPO_URL'i değiştir)
git remote add origin https://github.com/USERNAME/goren-duyan-scraper.git

# Push
git branch -M main
git push -u origin main
```

**Veya GitHub Desktop kullan:**
1. File → Add local repository
2. Projeyi seç
3. "Publish repository"

### 3️⃣ GitHub Actions'ı Aktifleştir

1. Repository → **Actions** tab
2. "I understand my workflows, go ahead and enable them"
3. **Tamam! İşlem bitti!** ✅

---

## 📅 Çalışma Zamanı

### Otomatik (Scheduled)
- **Her gün saat 09:00 UTC** (12:00 Türkiye saati)
- Sonuçlar otomatik commit edilir

### Manuel Test
1. Repository → **Actions** tab
2. Sol taraftan "Günlük İlan Scraper" seç
3. Sağ tarafta **"Run workflow"** → **"Run workflow"**
4. ✅ Hemen çalışmaya başlar!

---

## 📊 Sonuçlar Nerede?

### GitHub'da
```
data/
├── latest.json           → En son tarama (hepsi)
├── kedi_latest.json      → Sadece kedi
├── kopek_latest.json     → Sadece köpek
└── 20251122_120000.json  → Tarihli yedek
```

### URL ile Erişim
```
https://raw.githubusercontent.com/USERNAME/goren-duyan-scraper/main/data/latest.json
https://raw.githubusercontent.com/USERNAME/goren-duyan-scraper/main/data/kedi_latest.json
https://raw.githubusercontent.com/USERNAME/goren-duyan-scraper/main/data/kopek_latest.json
```

**Not:** `USERNAME` yerine kendi GitHub kullanıcı adınızı yazın.

---

## 🔔 Bildirim Ekle (İsteğe Bağlı)

### Telegram ile Bildirim

1. **Telegram Bot Oluştur:**
   - [@BotFather](https://t.me/BotFather) aç
   - `/newbot` komutunu gönder
   - Bot adı belirle
   - **Bot token'ı al** (örn: `123456:ABC-DEF...`)

2. **Chat ID Bul:**
   - Bot'una mesaj gönder
   - https://api.telegram.org/bot{TOKEN}/getUpdates aç
   - `"chat":{"id":` kısmından ID'ni bul

3. **GitHub Secrets Ekle:**
   - Repository → Settings → Secrets and variables → Actions
   - **New repository secret**
   - `TELEGRAM_BOT_TOKEN` = bot token
   - `TELEGRAM_CHAT_ID` = chat id

4. **Workflow güncelle** (`.github/workflows/scraper.yml`):
```yaml
    - name: Send Telegram notification
      if: success()
      run: |
        curl -s -X POST "https://api.telegram.org/bot${{ secrets.TELEGRAM_BOT_TOKEN }}/sendMessage" \
          -d chat_id="${{ secrets.TELEGRAM_CHAT_ID }}" \
          -d text="🤖 İlan taraması tamamlandı!%0A📊 Sonuçlar GitHub'a yüklendi."
```

### Email ile Bildirim

GitHub Actions varsayılan olarak başarısız çalışmalarda email gönderir.

---

## ⚙️ Ayarlar

### Zamanı Değiştir

`.github/workflows/scraper.yml` dosyasında:
```yaml
schedule:
  - cron: '0 9 * * *'  # Her gün 09:00 UTC

# Örnekler:
# '0 */6 * * *'  → Her 6 saatte
# '0 12 * * *'   → Her gün 12:00 UTC
# '0 0 * * 1'    → Her Pazartesi 00:00
# '*/30 * * * *' → Her 30 dakikada (dikkatli kullan!)
```

**Not:** Cron UTC saatidir (Türkiye = UTC+3)

### Sadece Kedi veya Sadece Köpek

`github_scraper.py` içinde istediğinizi yoruma alın:
```python
# Sadece kedi için
kedi_ilanlari = ilanlari_cek('https://www.gorenduyan.com/category/kedi', 'Kedi')
# kopek_ilanlari = []  # Köpek ekleme
```

---

## 📱 Frontend'den Kullanım

### JavaScript (Fetch)
```javascript
// En son ilanları çek
fetch('https://raw.githubusercontent.com/USERNAME/goren-duyan-scraper/main/data/latest.json')
  .then(res => res.json())
  .then(data => {
    console.log('Kedi ilanları:', data.kedi);
    console.log('Köpek ilanları:', data.kopek);
  });

// Sadece kedi
fetch('https://raw.githubusercontent.com/USERNAME/goren-duyan-scraper/main/data/kedi_latest.json')
  .then(res => res.json())
  .then(kedi_ilanlari => {
    console.log(kedi_ilanlari);
  });
```

### Python (Requests)
```python
import requests

# En son ilanlar
response = requests.get('https://raw.githubusercontent.com/USERNAME/goren-duyan-scraper/main/data/latest.json')
data = response.json()

print(f"Toplam: {data['toplam']} ilan")
print(f"Kedi: {len(data['kedi'])}")
print(f"Köpek: {len(data['kopek'])}")
```

### cURL
```bash
# En son ilanlar
curl https://raw.githubusercontent.com/USERNAME/goren-duyan-scraper/main/data/latest.json

# Sadece kedi
curl https://raw.githubusercontent.com/USERNAME/goren-duyan-scraper/main/data/kedi_latest.json
```

---

## 📈 Logları Görüntüle

1. Repository → **Actions** tab
2. Son çalışmayı tıkla
3. **"scrape"** job'ı aç
4. Tüm logları görürsün

---

## 🔧 Sorun Giderme

### "Permission denied" hatası
**Çözüm:** Repository → Settings → Actions → General → Workflow permissions
- ✅ "Read and write permissions" seç
- ✅ "Allow GitHub Actions to create and approve pull requests" seç

### Workflow çalışmıyor
**Çözüm:** 
- Actions tab'ı kontrol et
- Repository **public** olmalı (private'da Actions limit var)
- Manuel çalıştır: Actions → Run workflow

### Commit edilmiyor
**Çözüm:** `.github/workflows/scraper.yml` dosyasında:
```yaml
git add data/*.json
```
satırının olduğundan emin olun.

---

## 💰 Maliyet

**TAMAMEN ÜCRETSİZ!** ✅

- Public repository: Unlimited Actions
- Private repository: 2000 dakika/ay ücretsiz
- Bu proje ~2-3 dakika/gün kullanır
- Aylık ~60-90 dakika = **Ücretsiz tier içinde**

---

## 🎯 Özet

1. ✅ GitHub repo oluştur
2. ✅ Dosyaları push et
3. ✅ Actions aktif et
4. ✅ **Tamam!** Her gün otomatik çalışır

**Manuel test:**
- Actions → Run workflow → Hemen çalışır!

**Sonuçlar:**
- `data/latest.json` → GitHub'dan oku

---

## 📞 Yardım

Sorun olursa:
1. Actions loglarını kontrol et
2. Issue aç
3. workflow dosyasını kontrol et

**Başarılar! 🚀**

