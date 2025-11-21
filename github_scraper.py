# -*- coding: utf-8 -*-
"""
GitHub Actions için scraper
Her gün çalışır, sonuçları JSON olarak data/ klasörüne kaydeder
"""
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta
import time
import json
import os

def goreli_tarih_hesapla(tarih_text):
    """'X Saat Önce' gibi göreceli tarihi ISO 8601 formatına çevirir"""
    try:
        tarih_lower = tarih_text.lower()
        simdi = datetime.now()
        
        if 'dakika' in tarih_lower:
            dakika_match = re.search(r'(\d+)\s*dakika', tarih_lower)
            if dakika_match:
                dakika = int(dakika_match.group(1))
                hedef_tarih = simdi - timedelta(minutes=dakika)
                return hedef_tarih.strftime('%Y-%m-%dT%H:%M:%SZ')
        
        elif 'saat' in tarih_lower:
            saat_match = re.search(r'(\d+)\s*saat', tarih_lower)
            if saat_match:
                saat = int(saat_match.group(1))
                hedef_tarih = simdi - timedelta(hours=saat)
                return hedef_tarih.strftime('%Y-%m-%dT%H:%M:%SZ')
        
        elif 'gün' in tarih_lower or 'gun' in tarih_lower:
            gun_match = re.search(r'(\d+)\s*g[uü]n', tarih_lower)
            if gun_match:
                gun = int(gun_match.group(1))
                hedef_tarih = simdi - timedelta(days=gun)
                return hedef_tarih.strftime('%Y-%m-%dT%H:%M:%SZ')
        
        return simdi.strftime('%Y-%m-%dT%H:%M:%SZ')
        
    except Exception as e:
        return datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')

def ilan_detay_cek(ilan_url):
    """İlan sayfasından açıklamayı çeker"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(ilan_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            return meta_desc['content']
        
        # Article içeriği
        article = soup.find('article')
        if article:
            for script in article(['script', 'style']):
                script.decompose()
            return article.get_text(strip=True)
        
        return "Açıklama bulunamadı"
        
    except Exception as e:
        return f"Açıklama alınamadı: {str(e)}"

def ilanlari_cek(kategori_url, kategori_adi):
    """Belirtilen kategoriden son 24 saat içindeki ilanları çeker"""
    print(f"\n{'='*60}")
    print(f"{kategori_adi} ilanlari cekiliyor...")
    print('='*60)
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(kategori_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        cards = soup.find_all('div', class_='cl-card')
        
        print(f"Toplam {len(cards)} ilan bulundu.")
        
        son_24_saat = []
        
        for card in cards:
            try:
                # Başlık
                baslik_div = card.find('div', class_='cl-card-title')
                baslik = baslik_div.get_text(strip=True) if baslik_div else 'Baslik yok'
                
                # Durum
                durum_div = card.find('div', class_='cl-card-type')
                durum = durum_div.get_text(strip=True) if durum_div else 'Durum belirtilmemis'
                
                # Tarih
                tarih_div = card.find('i', class_='far fa-clock')
                tarih_text = tarih_div.parent.get_text(strip=True) if tarih_div and tarih_div.parent else 'Tarih yok'
                
                # Konum
                konum_icon = card.find('i', class_='fa-location-arrow')
                konum = konum_icon.parent.get_text(strip=True) if konum_icon and konum_icon.parent else 'Konum belirtilmemis'
                
                # Görsel URL
                gorsel_url = ""
                img_div = card.find('div', class_='cl-card-img')
                if img_div and 'style' in img_div.attrs:
                    style = img_div['style']
                    match = re.search(r'url\(([^)]+)\)', style)
                    if match:
                        gorsel_url = match.group(1).strip()
                        if gorsel_url and not gorsel_url.startswith('http'):
                            gorsel_url = f"https://www.gorenduyan.com{gorsel_url}"
                
                # Link
                link = None
                parent_a = card.find_parent('a')
                if parent_a and parent_a.get('href'):
                    link = parent_a['href']
                    if not link.startswith('http'):
                        link = f"https://www.gorenduyan.com{link}"
                
                # Son 24 saat kontrolü
                tarih_lower = tarih_text.lower()
                son_24_saat_icinde = False
                
                if 'saat önce' in tarih_lower or 'saat once' in tarih_lower:
                    saat_match = re.search(r'(\d+)\s*saat', tarih_lower)
                    if saat_match and int(saat_match.group(1)) <= 24:
                        son_24_saat_icinde = True
                elif 'dakika önce' in tarih_lower or 'dakika once' in tarih_lower:
                    son_24_saat_icinde = True
                
                if son_24_saat_icinde:
                    son_24_saat.append({
                        'baslik': baslik,
                        'durum': durum,
                        'tarih': tarih_text,
                        'konum': konum,
                        'gorsel': gorsel_url,
                        'link': link
                    })
                
            except Exception as e:
                continue
        
        # Duplicate temizle
        unique_ilanlar = []
        gorulmus_linkler = set()
        
        for ilan in son_24_saat:
            if ilan['link'] and ilan['link'] not in gorulmus_linkler:
                unique_ilanlar.append(ilan)
                gorulmus_linkler.add(ilan['link'])
        
        print(f"Son 24 saat: {len(unique_ilanlar)} benzersiz ilan")
        
        # Detayları çek
        sonuc_ilanlar = []
        for idx, ilan in enumerate(unique_ilanlar, 1):
            print(f"  [{idx}/{len(unique_ilanlar)}] {ilan['baslik'][:40]}... detay cekiliyor")
            
            aciklama = "Link bulunamadı"
            if ilan['link']:
                aciklama = ilan_detay_cek(ilan['link'])
                time.sleep(0.5)  # Rate limiting
            
            ilan_formati = {
                "ilan_turu": ilan['durum'],
                "baslik": ilan['baslik'],
                "aciklama": aciklama,
                "konum": ilan['konum'],
                "tarih1": ilan['tarih'],
                "tarih2": goreli_tarih_hesapla(ilan['tarih']),
                "kategori": kategori_adi,
                "gorsel": ilan['gorsel'] if ilan['gorsel'] else "",
                "link": ilan['link'] if ilan['link'] else "",
                "scraped_at": datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
            }
            
            sonuc_ilanlar.append(ilan_formati)
        
        print(f"[OK] {kategori_adi}: {len(sonuc_ilanlar)} ilan tamamlandi")
        return sonuc_ilanlar
        
    except Exception as e:
        print(f"[HATA] {e}")
        return []

def main():
    """Ana fonksiyon"""
    print("\n" + "="*60)
    print("[ROBOT] GOREN DUYAN SCRAPER - GitHub Actions")
    print("="*60)
    print(f"[TARIH] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Kedi ilanları
    kedi_ilanlari = ilanlari_cek('https://www.gorenduyan.com/category/kedi', 'Kedi')
    
    # Köpek ilanları
    kopek_ilanlari = ilanlari_cek('https://www.gorenduyan.com/category/kopek', 'Köpek')
    
    # Toplam sonuç
    toplam = len(kedi_ilanlari) + len(kopek_ilanlari)
    
    print("\n" + "="*60)
    print(f"[OZET] {toplam} ilan bulundu")
    print(f"   [KEDI] {len(kedi_ilanlari)}")
    print(f"   [KOPEK] {len(kopek_ilanlari)}")
    print("="*60)
    
    # data/ klasörü oluştur
    os.makedirs('data', exist_ok=True)
    
    # Tüm ilanları tek listede birleştir (kedi + köpek)
    tum_ilanlar = kedi_ilanlari + kopek_ilanlari
    
    # Tek dosyaya kaydet - sadece ilan listesi
    with open('data/ilanlar.json', 'w', encoding='utf-8') as f:
        json.dump(tum_ilanlar, f, ensure_ascii=False, indent=2)
    
    print(f"\n[OK] Sonuclar 'data/ilanlar.json' dosyasina kaydedildi!")
    print(f"   - Toplam {len(tum_ilanlar)} ilan")
    print(f"   - {len(kedi_ilanlari)} kedi + {len(kopek_ilanlari)} kopek")
    
    return tum_ilanlar

if __name__ == "__main__":
    main()

