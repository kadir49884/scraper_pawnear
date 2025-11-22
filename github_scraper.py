# -*- coding: utf-8 -*-
"""
GitHub Actions için ana scraper
Modüler yapı - Kolayca yeni site eklenebilir
"""
import os
import json
from datetime import datetime
from scrapers.scraper_manager import ScraperManager

def main():
    """Ana fonksiyon"""
    print("\n" + "="*60)
    print("[ROBOT] MULTI-SITE SCRAPER - GitHub Actions")
    print("="*60)
    print(f"[TARIH] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Scraper manager oluştur
    manager = ScraperManager()
    
    # Tüm siteleri tara
    tum_ilanlar = manager.scrape_all()
    
    toplam = len(tum_ilanlar)
    
    # Kategori bazlı sayım
    kedi_sayisi = len([i for i in tum_ilanlar if i['kategori'] == 'Kedi'])
    kopek_sayisi = len([i for i in tum_ilanlar if i['kategori'] == 'Köpek'])
    
    print("\n" + "="*60)
    print(f"[OZET] {toplam} ilan bulundu")
    print(f"   [KEDI] {kedi_sayisi}")
    print(f"   [KOPEK] {kopek_sayisi}")
    print("="*60)
    
    # data/ klasörü oluştur
    os.makedirs('data', exist_ok=True)
    
    # Tarihli dosya adı: ilan_taramasi_2025-11-22.json
    bugun = datetime.now().strftime('%Y-%m-%d')
    tarihli_dosya = f'data/ilan_taramasi_{bugun}.json'
    
    # Tarihli dosyaya kaydet (her gün yeni dosya)
    with open(tarihli_dosya, 'w', encoding='utf-8') as f:
        json.dump(tum_ilanlar, f, ensure_ascii=False, indent=2)
    
    # ilanlar.json'u da güncelle (son durum için)
    with open('data/ilanlar.json', 'w', encoding='utf-8') as f:
        json.dump(tum_ilanlar, f, ensure_ascii=False, indent=2)
    
    print(f"\n[OK] Sonuclar kaydedildi!")
    print(f"   - Tarihli dosya: {tarihli_dosya}")
    print(f"   - Son durum: data/ilanlar.json")
    print(f"   - Toplam {len(tum_ilanlar)} ilan")
    print(f"   - {kedi_sayisi} kedi + {kopek_sayisi} kopek")
    
    return tum_ilanlar

if __name__ == "__main__":
    main()

