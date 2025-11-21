# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import sys
import io
import json
from datetime import datetime, timedelta
import time

# Windows encoding fix
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def goreli_tarih_hesapla(tarih_text):
    """
    'X Saat Önce' gibi göreceli tarihi ISO 8601 formatına çevirir (2025-11-21T14:02:00Z)
    """
    try:
        tarih_lower = tarih_text.lower()
        simdi = datetime.now()
        
        # Dakika önce
        if 'dakika' in tarih_lower:
            dakika_match = re.search(r'(\d+)\s*dakika', tarih_lower)
            if dakika_match:
                dakika = int(dakika_match.group(1))
                hedef_tarih = simdi - timedelta(minutes=dakika)
                return hedef_tarih.strftime('%Y-%m-%dT%H:%M:%SZ')
        
        # Saat önce
        elif 'saat' in tarih_lower:
            saat_match = re.search(r'(\d+)\s*saat', tarih_lower)
            if saat_match:
                saat = int(saat_match.group(1))
                hedef_tarih = simdi - timedelta(hours=saat)
                return hedef_tarih.strftime('%Y-%m-%dT%H:%M:%SZ')
        
        # Gün önce
        elif 'gün' in tarih_lower or 'gun' in tarih_lower:
            gun_match = re.search(r'(\d+)\s*g[uü]n', tarih_lower)
            if gun_match:
                gun = int(gun_match.group(1))
                hedef_tarih = simdi - timedelta(days=gun)
                return hedef_tarih.strftime('%Y-%m-%dT%H:%M:%SZ')
        
        # Hafta önce
        elif 'hafta' in tarih_lower:
            hafta_match = re.search(r'(\d+)\s*hafta', tarih_lower)
            if hafta_match:
                hafta = int(hafta_match.group(1))
                hedef_tarih = simdi - timedelta(weeks=hafta)
                return hedef_tarih.strftime('%Y-%m-%dT%H:%M:%SZ')
        
        # Ay önce
        elif 'ay' in tarih_lower:
            ay_match = re.search(r'(\d+)\s*ay', tarih_lower)
            if ay_match:
                ay = int(ay_match.group(1))
                hedef_tarih = simdi - timedelta(days=ay*30)
                return hedef_tarih.strftime('%Y-%m-%dT%H:%M:%SZ')
        
        # Yıl önce
        elif 'yıl' in tarih_lower or 'yil' in tarih_lower:
            yil_match = re.search(r'(\d+)\s*y[ıi]l', tarih_lower)
            if yil_match:
                yil = int(yil_match.group(1))
                hedef_tarih = simdi - timedelta(days=yil*365)
                return hedef_tarih.strftime('%Y-%m-%dT%H:%M:%SZ')
        
        # Eğer parse edilemezse şu anki tarihi dön
        return simdi.strftime('%Y-%m-%dT%H:%M:%SZ')
        
    except Exception as e:
        return datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')

def ilan_detay_cek(ilan_url):
    """
    İlan sayfasından açıklamayı çeker
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(ilan_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Açıklamayı bul - farklı yapıları dene
        aciklama = ""
        
        # Yöntem 1: açıklama class'ı
        aciklama_div = soup.find(['div', 'p'], class_=re.compile(r'description|aciklama|content|detail'))
        if aciklama_div:
            aciklama = aciklama_div.get_text(strip=True)
        
        # Yöntem 2: meta description
        if not aciklama:
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if meta_desc and meta_desc.get('content'):
                aciklama = meta_desc['content']
        
        # Yöntem 3: article içeriği
        if not aciklama:
            article = soup.find('article')
            if article:
                # Script ve style taglerini çıkar
                for script in article(['script', 'style']):
                    script.decompose()
                aciklama = article.get_text(strip=True)
        
        # Yöntem 4: Ana içerik divini bul
        if not aciklama:
            main_content = soup.find(['div'], id=re.compile(r'content|main|detail'))
            if main_content:
                for script in main_content(['script', 'style']):
                    script.decompose()
                aciklama = main_content.get_text(strip=True)
        
        return aciklama if aciklama else "Açıklama bulunamadı"
        
    except Exception as e:
        return f"Açıklama alınamadı: {str(e)}"

def son_24_saat_ilanlari_cek():
    """
    gorenduyan.com'dan son 24 saat içindeki kedi ilanlarını çeker
    """
    url = "https://www.gorenduyan.com/category/kedi"
    
    print("Ilanlar cekiliyor...\n")
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # cl-card yapısındaki ilanları bul
        cards = soup.find_all('div', class_='cl-card')
        
        print(f"Toplam {len(cards)} ilan bulundu.")
        print("Son 24 saat kontrolu yapiliyor...\n")
        
        son_24_saat = []
        
        for card in cards:
            try:
                # Başlık
                baslik_div = card.find('div', class_='cl-card-title')
                baslik = baslik_div.get_text(strip=True) if baslik_div else 'Baslik yok'
                
                # Durum (Kayıp, Sahibi Aranıyor, vb.)
                durum_div = card.find('div', class_='cl-card-type')
                durum = durum_div.get_text(strip=True) if durum_div else 'Durum belirtilmemis'
                
                # Tarih - far fa-clock ikonlu div'i bul
                tarih_div = card.find('i', class_='far fa-clock')
                if tarih_div and tarih_div.parent:
                    tarih_text = tarih_div.parent.get_text(strip=True)
                else:
                    tarih_text = 'Tarih yok'
                
                # Konum
                konum_icon = card.find('i', class_='fa-location-arrow')
                if konum_icon and konum_icon.parent:
                    konum = konum_icon.parent.get_text(strip=True)
                else:
                    konum = 'Konum belirtilmemis'
                
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
                
                # Link - card'ın parent'ı a tagı olabilir
                link = None
                parent_a = card.find_parent('a')
                if parent_a and parent_a.get('href'):
                    link = parent_a['href']
                    if not link.startswith('http'):
                        link = f"https://www.gorenduyan.com{link}"
                
                # Son 24 saat kontrolü
                tarih_lower = tarih_text.lower()
                
                # "saat önce" veya "dakika önce" içeriyorsa son 24 saat içinde
                son_24_saat_icinde = False
                
                if 'saat önce' in tarih_lower or 'saat once' in tarih_lower:
                    saat_match = re.search(r'(\d+)\s*saat', tarih_lower)
                    if saat_match:
                        saat_sayisi = int(saat_match.group(1))
                        if saat_sayisi <= 24:
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
                print(f"[UYARI] Bir ilan islenirken hata: {e}")
                continue
        
        print("="*80)
        if son_24_saat:
            # Duplicate ilanları temizle (link'e göre)
            unique_ilanlar = []
            gorulmus_linkler = set()
            
            for ilan in son_24_saat:
                if ilan['link'] and ilan['link'] not in gorulmus_linkler:
                    unique_ilanlar.append(ilan)
                    gorulmus_linkler.add(ilan['link'])
            
            son_24_saat = unique_ilanlar
            
            print(f"\n[BASARILI] Son 24 saat icinde {len(son_24_saat)} benzersiz ilan bulundu!")
            print("Ilan detaylari cekiliyor...\n")
            
            sonuc_ilanlar = []
            
            for i, ilan in enumerate(son_24_saat, 1):
                print(f"[{i}/{len(son_24_saat)}] {ilan['baslik']} - Detay cekiliyor...")
                
                aciklama = "Link bulunamadı"
                if ilan['link']:
                    aciklama = ilan_detay_cek(ilan['link'])
                    time.sleep(0.5)  # Rate limiting için bekle
                
                ilan_formati = {
                    "ilan_turu": ilan['durum'],
                    "baslik": ilan['baslik'],
                    "aciklama": aciklama,
                    "konum": ilan['konum'],
                    "tarih1": ilan['tarih'],
                    "tarih2": goreli_tarih_hesapla(ilan['tarih']),
                    "kategori": "Kedi",
                    "gorsel": ilan['gorsel'] if ilan['gorsel'] else "",
                    "link": ilan['link'] if ilan['link'] else ""
                }
                
                sonuc_ilanlar.append(ilan_formati)
            
            print("\n" + "="*80)
            print("SONUCLAR:")
            print("="*80 + "\n")
            
            for i, ilan in enumerate(sonuc_ilanlar, 1):
                print(f"\n{i}. ILAN:")
                print(f"   Ilan Turu : {ilan['ilan_turu']}")
                print(f"   Baslik    : {ilan['baslik']}")
                print(f"   Aciklama  : {ilan['aciklama'][:100]}..." if len(ilan['aciklama']) > 100 else f"   Aciklama  : {ilan['aciklama']}")
                print(f"   Konum     : {ilan['konum']}")
                print(f"   Tarih1    : {ilan['tarih1']}")
                print(f"   Tarih2    : {ilan['tarih2']}")
                print(f"   Kategori  : {ilan['kategori']}")
                print(f"   Gorsel    : {ilan['gorsel']}")
                print(f"   Link      : {ilan['link']}")
                print("-"*80)
            
            return sonuc_ilanlar
        else:
            print(f"\n[UYARI] Son 24 saat icinde ilan bulunamadi.\n")
            return []
        
    except requests.exceptions.RequestException as e:
        print(f"[HATA] Baglanti hatasi: {e}")
        return []
    except Exception as e:
        print(f"[HATA] Beklenmeyen hata: {e}")
        import traceback
        traceback.print_exc()
        return []

if __name__ == "__main__":
    print("="*80)
    print("GOREN DUYAN - KEDI ILAN SCRAPER")
    print("Son 24 saat icindeki ilanlari cekmek icin...")
    print("="*80)
    print()
    
    ilanlar = son_24_saat_ilanlari_cek()
    
    print("\n" + "="*80)
    print(f"OZET: Toplam {len(ilanlar)} ilan cekildi.")
    print("="*80)
    
    # JSON olarak kaydet
    if ilanlar:
        dosya_adi = f"kedi_ilanlari_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(dosya_adi, 'w', encoding='utf-8') as f:
            json.dump(ilanlar, f, ensure_ascii=False, indent=2)
        print(f"\n[BASARILI] Ilanlar '{dosya_adi}' dosyasina kaydedildi.")
        print(f"\nJSON Format Ornegi:")
        print(json.dumps(ilanlar[0], ensure_ascii=False, indent=2))
