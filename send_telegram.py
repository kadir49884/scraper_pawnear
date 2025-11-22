#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram bildirim scripti - GitHub Actions için
"""
import json
import os
import sys
from datetime import datetime
import urllib.request
import urllib.parse

def send_telegram_message():
    """Telegram'a özet mesaj gönder"""
    
    # Token ve Chat ID (GitHub Secrets'tan)
    bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
    chat_id = os.environ.get('TELEGRAM_CHAT_ID')
    
    if not bot_token or not chat_id:
        print("HATA: TELEGRAM_BOT_TOKEN veya TELEGRAM_CHAT_ID bulunamadi")
        sys.exit(1)
    
    # Bugünün dosyası
    bugun = datetime.now().strftime('%Y-%m-%d')
    dosya = f'data/ilan_taramasi_{bugun}.json'
    
    if not os.path.exists(dosya):
        print(f"HATA: {dosya} bulunamadi")
        sys.exit(1)
    
    # JSON'u oku
    with open(dosya, 'r', encoding='utf-8') as f:
        ilanlar = json.load(f)
    
    # İstatistikleri hesapla
    toplam = len(ilanlar)
    kedi = len([i for i in ilanlar if i.get('kategori') == 'Kedi'])
    kopek = len([i for i in ilanlar if i.get('kategori') == 'Köpek'])
    
    # Mesaj oluştur
    mesaj = f"""Gunluk Ilan Taramasi - {bugun}

Ozet:
- Toplam: {toplam} ilan
- Kedi: {kedi}
- Kopek: {kopek}

Dosya: {dosya}
GitHub: https://github.com/{os.environ.get('GITHUB_REPOSITORY')}/blob/main/{dosya}

Tarama basariyla tamamlandi!"""
    
    # Telegram API'ye gönder
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        'chat_id': chat_id,
        'text': mesaj
    }
    
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))
            
            if result.get('ok'):
                print(f"[OK] Telegram mesaji gonderildi! (chat_id: {chat_id})")
                return True
            else:
                print(f"[HATA] Telegram hatasi: {result}")
                return False
    
    except Exception as e:
        print(f"[HATA] {e}")
        return False

if __name__ == "__main__":
    success = send_telegram_message()
    sys.exit(0 if success else 1)

