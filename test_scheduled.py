#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test scripti - Zamanlanmış mesaj sistemini test eder
"""
import json
import os
from datetime import datetime


def test_format():
    """Mesaj formatını test et"""
    print("\n" + "="*60)
    print("MESAJ FORMATI TESTİ")
    print("="*60)
    
    # Bugünkü ilanları yükle
    bugun = datetime.now().strftime('%Y-%m-%d')
    dosya = f'data/ilan_taramasi_{bugun}.json'
    
    if not os.path.exists(dosya):
        print(f"[HATA] {dosya} bulunamadı")
        return
    
    with open(dosya, 'r', encoding='utf-8') as f:
        ilanlar = json.load(f)
    
    print(f"\n[BILGI] Toplam {len(ilanlar)} ilan bulundu\n")
    
    # Her zaman dilimi için mesajları göster
    zamanlar = [
        (17, 0, 2, "1. ve 2."),
        (18, 2, 2, "3. ve 4."),
        (19, 4, 2, "5. ve 6."),
        (20, 6, 2, "7. ve 8.")
    ]
    
    for saat, start, count, aciklama in zamanlar:
        print(f"\n{'='*60}")
        print(f"SAAT {saat:02d}:00 - {aciklama} İLAN")
        print(f"{'='*60}")
        
        end = min(start + count, len(ilanlar))
        
        if start >= len(ilanlar):
            print(f"[UYARI] Yeterli ilan yok (istenen: {start + 1}, mevcut: {len(ilanlar)})")
            continue
        
        for i in range(start, end):
            ilan = ilanlar[i]
            print(f"\n--- İlan {i + 1} ---")
            print(json.dumps(ilan, ensure_ascii=False, indent=2))
            print()


def test_schedule_logic():
    """Zamanlama mantığını test et"""
    print("\n" + "="*60)
    print("ZAMANLAMA MANTIĞI TESTİ")
    print("="*60)
    
    schedule = {
        17: (0, 2),
        18: (2, 2),
        19: (4, 2),
        20: (6, 2)
    }
    
    print("\nKonfigürasyon:")
    for saat, (start, count) in schedule.items():
        print(f"  {saat:02d}:00 -> İlan {start + 1}-{start + count}")
    
    print(f"\nŞu anki saat: {datetime.now().strftime('%H:%M')}")
    current_hour = datetime.now().hour
    
    if current_hour in schedule:
        start, count = schedule[current_hour]
        print(f"[AKTİF] Bu saatte {start + 1}. ve {start + count}. ilanlar gönderilecek")
    else:
        print(f"[PASİF] Bu saat için zamanlanmış mesaj yok")


if __name__ == "__main__":
    test_format()
    test_schedule_logic()
    
    print("\n" + "="*60)
    print("TEST TAMAMLANDI")
    print("="*60)
    print("\nÖNEMLİ:")
    print("  - Telegram gönderimi yapmaz, sadece formatı gösterir")
    print("  - Gerçek gönderi için: python scheduled_telegram.py")
    print("  - Env vars gerekli: TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID")
    print()

