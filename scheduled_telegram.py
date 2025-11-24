#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Zamanlanmış sosyal medya paylaşımı
Her gün belirli saatlerde ilanları sosyal medyada paylaşır
"""
import json
import os
import sys
import urllib.request
from datetime import datetime


class SocialPublisher:
    """Sosyal medya paylaşım yöneticisi"""
    
    API_URL = "https://web-production-55e2.up.railway.app/api/publish/json"
    
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
    
    def _publish_to_social(self, ilan):
        """İlanı sosyal medyada paylaş"""
        payload = {
            "baslik": ilan.get('baslik', ''),
            "aciklama": ilan.get('aciklama', ''),
            "konum": ilan.get('konum', ''),
            "gorsel": ilan.get('gorsel', ''),
            "platforms": ["facebook", "twitter", "instagram"]
        }
        
        req = urllib.request.Request(
            self.API_URL,
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json; charset=utf-8'}
        )
        
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode('utf-8'))
                return result
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _format_result_message(self, ilan, result):
        """Paylaşım sonucunu Telegram mesajı formatına çevir"""
        baslik = ilan.get('baslik', 'Başlıksız')
        
        if result.get('success'):
            platforms = []
            for platform, data in result.get('results', {}).items():
                if data.get('status') == 'success':
                    platforms.append(f"✅ {platform.capitalize()}")
                else:
                    platforms.append(f"❌ {platform.capitalize()}")
            
            platform_status = "\n".join(platforms)
            return f"📢 PAYLAŞIM YAPILDI\n\n📝 {baslik}\n\n{platform_status}"
        else:
            error = result.get('error', 'Bilinmeyen hata')
            return f"❌ PAYLAŞIM BAŞARISIZ\n\n📝 {baslik}\n\n🚫 Hata: {error}"
    
    def _find_valid_ilan(self, ilanlar, preferred_index):
        """İlan bulamazsa geri geri giderek uygun ilan bul"""
        total = len(ilanlar)
        
        # İstenen indeks varsa direkt döndür
        if preferred_index < total:
            return preferred_index
        
        # Yoksa geriye doğru ara
        for i in range(preferred_index - 1, -1, -1):
            if i < total:
                print(f"[FALLBACK] İlan {preferred_index + 1} yok, İlan {i + 1} kullanılıyor")
                return i
        
        # Hiç ilan yoksa
        return None
    
    def publish_scheduled_ilanlar(self, start_index, count=1):
        """Belirli indeksten başlayarak ilanları sosyal medyada paylaş"""
        ilanlar = self._load_ilanlar()
        
        if not ilanlar:
            print(f"[HATA] Hiç ilan bulunamadı")
            return False
        
        # Uygun ilan indeksini bul
        valid_index = self._find_valid_ilan(ilanlar, start_index)
        
        if valid_index is None:
            print(f"[HATA] Paylaşılacak ilan bulunamadı")
            return False
        
        ilan = ilanlar[valid_index]
        
        try:
            # Sosyal medyada paylaş
            print(f"[PAYLAŞIM] İlan {valid_index + 1} paylaşılıyor...")
            result = self._publish_to_social(ilan)
            
            # Sonucu Telegram'a bildir
            message = self._format_result_message(ilan, result)
            if self._send_message(message):
                if result.get('success'):
                    print(f"[OK] İlan {valid_index + 1} paylaşıldı ve bildirim gönderildi")
                    return True
                else:
                    print(f"[UYARI] İlan {valid_index + 1} paylaşılamadı ama bildirim gönderildi")
                    return False
            else:
                print(f"[HATA] İlan {valid_index + 1} - Telegram bildirimi gönderilemedi")
                return False
        except Exception as e:
            print(f"[HATA] İlan {valid_index + 1} - {e}")
            return False


def main():
    """Ana fonksiyon - Sosyal medya paylaşımı"""
    # GitHub Actions'dan ilan indekslerini al
    start_index = int(os.environ.get('ILAN_START_INDEX', 0))
    count = int(os.environ.get('ILAN_COUNT', 1))
    
    print(f"\n[BASLANGIC] İlan {start_index + 1} sosyal medyada paylaşılıyor")
    print(f"[ZAMAN] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        publisher = SocialPublisher()
        success = publisher.publish_scheduled_ilanlar(start_index, count)
        
        if success:
            print(f"[BASARILI] Paylaşım tamamlandı")
            sys.exit(0)
        else:
            print(f"[HATA] Paylaşım başarısız")
            sys.exit(1)
    
    except Exception as e:
        print(f"[HATA] {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

