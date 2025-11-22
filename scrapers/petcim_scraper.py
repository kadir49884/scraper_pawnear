# -*- coding: utf-8 -*-
from .base_scraper import BaseScraper
from typing import List, Dict
import time
import re

class PetcimScraper(BaseScraper):
    def __init__(self):
        super().__init__("Petcim")
        self.base_url = "https://www.petcim.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'tr-TR,tr;q=0.9',
            'Referer': 'https://www.petcim.com/'
        }
    
    def scrape(self) -> List[Dict]:
        print(f"\n[{self.name}] Tarama basliyor...")
        try:
            url = f"{self.base_url}/sahibinden-satilik-kedi-ilanlar-40"
            soup = self.fetch_page(url)
            
            # İlan kartlarını bul (Petcim yapısına göre)
            ilanlar = soup.find_all('div', class_=re.compile(r'col-lg-3|col-md-4|item|card'))
            
            if not ilanlar:
                ilanlar = soup.find_all('a', href=re.compile(r'/ilan-detay/'))
            
            result = []
            for card in ilanlar[:20]:  # İlk 20 ilan
                try:
                    ilan = self._parse_card(card)
                    if ilan and self._is_within_24_hours(ilan.get('tarih1', '')):
                        result.append(ilan)
                        time.sleep(0.3)
                except:
                    continue
            
            print(f"[{self.name}] {len(result)} ilan bulundu")
            return result
        except Exception as e:
            print(f"[{self.name}] Hata: {e}")
            return []
    
    def _parse_card(self, card) -> Dict:
        try:
            # Başlık
            baslik_tag = card.find(['h3', 'h4', 'h5', 'a'], class_=re.compile(r'title|name|baslik'))
            if not baslik_tag:
                baslik_tag = card.find('a')
            baslik = baslik_tag.get_text(strip=True) if baslik_tag else ''
            
            if not baslik or len(baslik) < 5:
                return None
            
            # Link
            link_tag = card if card.name == 'a' else card.find('a')
            link = link_tag.get('href', '') if link_tag else ''
            if link and not link.startswith('http'):
                link = f"{self.base_url}{link}"
            
            # Görsel
            img_tag = card.find('img')
            gorsel = ''
            if img_tag:
                gorsel = img_tag.get('src', '') or img_tag.get('data-src', '') or img_tag.get('data-lazy', '')
                if gorsel and not gorsel.startswith('http'):
                    gorsel = f"{self.base_url}{gorsel}"
            
            # Konum - span veya div içinde olabilir
            konum = ''
            konum_tag = card.find(string=re.compile(r'İl|İlçe', re.I))
            if konum_tag:
                konum = konum_tag.strip()
            
            # Tarih - "bugün", "dün" veya "X gün önce" formatında
            tarih_tag = card.find(string=re.compile(r'bugün|dün|gün önce|saat önce', re.I))
            tarih1 = tarih_tag.strip() if tarih_tag else 'Bugün'
            
            return {
                'ilan_turu': 'Sahiplendirme',
                'baslik': baslik,
                'aciklama': baslik,  # Detay sayfası 403 verirse başlık kullan
                'konum': konum or 'Türkiye',
                'tarih1': tarih1,
                'tarih2': self.goreli_tarih_hesapla(tarih1),
                'kategori': 'Kedi',
                'gorsel': gorsel,
                'link': link
            }
        except:
            return None
    
    def _is_within_24_hours(self, tarih_text: str) -> bool:
        tarih_lower = tarih_text.lower()
        if any(x in tarih_lower for x in ['bugün', 'bugun', 'saat önce', 'saat once', 'dakika']):
            return True
        if 'dün' in tarih_lower or 'dun' in tarih_lower:
            return True
        return False

