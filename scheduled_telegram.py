#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Zamanlanmış Telegram mesaj gönderimi
Her gün belirli saatlerde ilanları ikişer ikişer gönderir
"""
import json
import os
import sys
import urllib.request
from datetime import datetime


class TelegramScheduler:
    """Zamanlanmış Telegram mesaj yöneticisi"""
    
    def __init__(self):
        self.bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
        self.chat_id = os.environ.get('TELEGRAM_CHAT_ID')
        self._validate_credentials()
    
    def _validate_credentials(self):
        """Telegram kimlik bilgilerini kontrol et"""
        if not self.bot_token or not self.chat_id:
            raise ValueError("TELEGRAM_BOT_TOKEN ve TELEGRAM_CHAT_ID gerekli")
    
    def _load_ilanlar(self):
        """Günlük ilan dosyasını yükle"""
        bugun = datetime.now().strftime('%Y-%m-%d')
        dosya = f'data/ilan_taramasi_{bugun}.json'
        
        if not os.path.exists(dosya):
            raise FileNotFoundError(f"İlan dosyası bulunamadı: {dosya}")
        
        with open(dosya, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _send_message(self, text):
        """Telegram'a mesaj gönder"""
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        data = {
            'chat_id': self.chat_id,
            'text': text,
            'parse_mode': 'HTML'
        }
        
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result.get('ok', False)
    
    def _format_ilan_message(self, ilan):
        """İlanı mesaj formatına çevir"""
        return json.dumps(ilan, ensure_ascii=False, indent=2)
    
    def send_scheduled_ilanlar(self, start_index, count=2):
        """Belirli indeksten başlayarak her ilanı ayrı mesaj olarak gönder"""
        ilanlar = self._load_ilanlar()
        
        if start_index >= len(ilanlar):
            print(f"[UYARI] Yetersiz ilan sayısı. İstenen: {start_index + 1}, Mevcut: {len(ilanlar)}")
            return False
        
        success_count = 0
        end_index = min(start_index + count, len(ilanlar))
        
        for i in range(start_index, end_index):
            ilan = ilanlar[i]
            message = self._format_ilan_message(ilan)
            
            try:
                if self._send_message(message):
                    print(f"[OK] İlan {i + 1} gönderildi (ayrı mesaj)")
                    success_count += 1
                else:
                    print(f"[HATA] İlan {i + 1} gönderilemedi")
            except Exception as e:
                print(f"[HATA] İlan {i + 1} - {e}")
        
        return success_count == (end_index - start_index)


def main():
    """Ana fonksiyon - Saat bazlı gönderim"""
    current_hour = datetime.now().hour
    
    # Saat bazlı ilan indeksleri (0-indexed)
    schedule = {
        17: (0, 2),   # 1. ve 2. ilan
        18: (2, 2),   # 3. ve 4. ilan
        19: (4, 2),   # 5. ve 6. ilan
        20: (6, 2)    # 7. ve 8. ilan
    }
    
    if current_hour not in schedule:
        print(f"[BILGI] Saat {current_hour:02d}:00 için zamanlanmış gönderim yok")
        return
    
    start_index, count = schedule[current_hour]
    
    print(f"\n[BASLANGIC] Saat {current_hour:02d}:00 - İlan {start_index + 1}-{start_index + count} gönderiliyor")
    
    try:
        scheduler = TelegramScheduler()
        success = scheduler.send_scheduled_ilanlar(start_index, count)
        
        if success:
            print(f"[BASARILI] Tüm ilanlar gönderildi")
            sys.exit(0)
        else:
            print(f"[HATA] Bazı ilanlar gönderilemedi")
            sys.exit(1)
    
    except Exception as e:
        print(f"[HATA] {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

