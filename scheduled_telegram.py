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
    
    def _load_shared_ilanlar(self):
        """Bugün paylaşılan ilanları yükle"""
        bugun = datetime.now().strftime('%Y-%m-%d')
        dosya = f'data/shared_{bugun}.json'
        
        if not os.path.exists(dosya):
            return []
        
        try:
            with open(dosya, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    
    def _save_shared_ilan(self, ilan_index):
        """Paylaşılan ilanı kaydet"""
        bugun = datetime.now().strftime('%Y-%m-%d')
        dosya = f'data/shared_{bugun}.json'
        
        shared = self._load_shared_ilanlar()
        if ilan_index not in shared:
            shared.append(ilan_index)
        
        os.makedirs('data', exist_ok=True)
        with open(dosya, 'w', encoding='utf-8') as f:
            json.dump(shared, f)
    
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
        
        print(f"[DEBUG] API'ye gönderiliyor: baslik={payload['baslik'][:50]}...")
        print(f"[DEBUG] Görsel URL: {payload['gorsel']}")
        
        req = urllib.request.Request(
            self.API_URL,
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json; charset=utf-8'}
        )
        
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode('utf-8'))
                print(f"[DEBUG] API Yanıt: {result}")
                return result
        except urllib.error.HTTPError as e:
            error_msg = e.read().decode('utf-8') if e.fp else str(e)
            print(f"[HATA] HTTP {e.code}: {error_msg}")
            return {"success": False, "error": f"HTTP {e.code}: {error_msg}"}
        except Exception as e:
            print(f"[HATA] API Hatası: {str(e)}")
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
    
    def _is_valid_image(self, url):
        """Görsel URL'i kontrol et (404 değilse geçerli)"""
        if not url:
            return False
        
        # 404.png içeren URL'ler geçersiz
        if '404.png' in url.lower() or '404.jpg' in url.lower():
            return False
        
        # Default/placeholder görseller
        if 'default' in url.lower() or 'placeholder' in url.lower():
            return False
        
        return True
    
    def _find_valid_ilan(self, ilanlar, preferred_index):
        """İlan bulamazsa geri geri giderek uygun ilan bul (daha önce paylaşılmamış ve geçerli görsel)"""
        total = len(ilanlar)
        shared = self._load_shared_ilanlar()
        
        # İstenen indeks varsa ve paylaşılmamışsa ve görseli geçerliyse direkt döndür
        if preferred_index < total and preferred_index not in shared:
            ilan = ilanlar[preferred_index]
            if self._is_valid_image(ilan.get('gorsel', '')):
                return preferred_index
            else:
                print(f"[FALLBACK] İlan {preferred_index + 1} geçersiz görsel, atlanıyor...")
        
        # Yoksa geriye doğru ara (paylaşılmamış ve geçerli görsel)
        for i in range(preferred_index - 1, -1, -1):
            if i < total and i not in shared:
                ilan = ilanlar[i]
                if self._is_valid_image(ilan.get('gorsel', '')):
                    print(f"[FALLBACK] İlan {preferred_index + 1} uygun değil, İlan {i + 1} kullanılıyor")
                    return i
        
        # Hiç uygun ilan yoksa
        print(f"[UYARI] Paylaşılabilir ilan bulunamadı")
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
                    # Başarılıysa paylaşılan listeye ekle
                    self._save_shared_ilan(valid_index)
                    print(f"[OK] İlan {valid_index + 1} paylaşıldı ve kaydedildi")
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

