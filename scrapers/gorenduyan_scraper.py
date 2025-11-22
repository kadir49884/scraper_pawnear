# -*- coding: utf-8 -*-
from .base_scraper import BaseScraper
from typing import List, Dict
import time
import re

class GorenDuyanScraper(BaseScraper):
    def __init__(self):
        super().__init__("GorenDuyan")
        self.base_url = "https://www.gorenduyan.com"
    
    def scrape(self) -> List[Dict]:
        print(f"\n[{self.name}] Tarama basliyor...")
        ilanlar = []
        ilanlar.extend(self._scrape_category('kedi', 'Kedi'))
        ilanlar.extend(self._scrape_category('kopek', 'Köpek'))
        print(f"[{self.name}] {len(ilanlar)} ilan bulundu")
        return ilanlar
    
    def _scrape_category(self, category: str, kategori_adi: str) -> List[Dict]:
        try:
            url = f"{self.base_url}/category/{category}"
            soup = self.fetch_page(url)
            cards = soup.find_all('div', class_='cl-card')
            
            son_24_saat = []
            for card in cards:
                try:
                    baslik_div = card.find('div', class_='cl-card-title')
                    baslik = baslik_div.get_text(strip=True) if baslik_div else ''
                    
                    durum_div = card.find('div', class_='cl-card-type')
                    durum = durum_div.get_text(strip=True) if durum_div else ''
                    
                    tarih_div = card.find('i', class_='far fa-clock')
                    tarih_text = tarih_div.parent.get_text(strip=True) if tarih_div and tarih_div.parent else ''
                    
                    konum_icon = card.find('i', class_='fa-location-arrow')
                    konum = konum_icon.parent.get_text(strip=True) if konum_icon and konum_icon.parent else ''
                    
                    gorsel_url = ""
                    img_div = card.find('div', class_='cl-card-img')
                    if img_div and 'style' in img_div.attrs:
                        match = re.search(r'url\(([^)]+)\)', img_div['style'])
                        if match:
                            gorsel_url = match.group(1).strip()
                            if gorsel_url and not gorsel_url.startswith('http'):
                                gorsel_url = f"{self.base_url}{gorsel_url}"
                    
                    link = None
                    parent_a = card.find_parent('a')
                    if parent_a and parent_a.get('href'):
                        link = parent_a['href']
                        if not link.startswith('http'):
                            link = f"{self.base_url}{link}"
                    
                    if self._is_within_24_hours(tarih_text):
                        son_24_saat.append({
                            'durum': durum, 'baslik': baslik, 'tarih': tarih_text,
                            'konum': konum, 'gorsel': gorsel_url, 'link': link
                        })
                except:
                    continue
            
            unique = self._remove_duplicates(son_24_saat)
            result = []
            for ilan in unique:
                aciklama = self._fetch_details(ilan['link']) if ilan['link'] else ''
                result.append({
                    'ilan_turu': ilan['durum'], 'baslik': ilan['baslik'],
                    'aciklama': aciklama, 'konum': ilan['konum'],
                    'tarih1': ilan['tarih'], 'tarih2': self.goreli_tarih_hesapla(ilan['tarih']),
                    'kategori': kategori_adi, 'gorsel': ilan['gorsel'], 'link': ilan['link']
                })
                time.sleep(0.5)
            return result
        except Exception as e:
            print(f"[{self.name}] Hata: {e}")
            return []
    
    def _is_within_24_hours(self, tarih_text: str) -> bool:
        tarih_lower = tarih_text.lower()
        if 'saat önce' in tarih_lower or 'saat once' in tarih_lower:
            saat_match = re.search(r'(\d+)\s*saat', tarih_lower)
            if saat_match and int(saat_match.group(1)) <= 24:
                return True
        elif 'dakika önce' in tarih_lower or 'dakika once' in tarih_lower:
            return True
        return False
    
    def _remove_duplicates(self, ilanlar: List[Dict]) -> List[Dict]:
        unique, seen = [], set()
        for ilan in ilanlar:
            if ilan['link'] and ilan['link'] not in seen:
                unique.append(ilan)
                seen.add(ilan['link'])
        return unique
    
    def _fetch_details(self, url: str) -> str:
        try:
            soup = self.fetch_page(url)
            meta = soup.find('meta', attrs={'name': 'description'})
            if meta and meta.get('content'):
                return meta['content']
            article = soup.find('article')
            if article:
                for script in article(['script', 'style']):
                    script.decompose()
                return article.get_text(strip=True)
            return ""
        except:
            return ""

