# -*- coding: utf-8 -*-
from .base_scraper import BaseScraper
from .selenium_scraper import SeleniumScraper
from typing import List, Dict
from bs4 import BeautifulSoup
import re

class PetcimScraper(BaseScraper):
    def __init__(self):
        super().__init__("Petcim")
        self.base_url = "https://www.petcim.com"
        self.selenium = None
    
    def scrape(self) -> List[Dict]:
        print(f"\n[{self.name}] Tarama basliyor (CloudScraper)...")
        try:
            url = f"{self.base_url}/sahibinden-satilik-kedi-ilanlar-40"
            
            # CloudScraper ile sayfa yükle
            self.selenium = SeleniumScraper()
            page_source = self.selenium.get_page_source(url, wait_time=2)
            soup = BeautifulSoup(page_source, 'html.parser')
            
            listings = self.parse_listings(soup)
            result = self.get_last_24_hours_ads(listings)
            
            print(f"[{self.name}] {len(result)} ilan bulundu")
            return result
        except Exception as e:
            print(f"[{self.name}] Hata: {e}")
            import traceback
            traceback.print_exc()
            return []
        finally:
            if self.selenium:
                self.selenium.close()
    
    def parse_listings(self, soup) -> List[Dict]:
        """İlanları parse et"""
        listings = []
        
        # Tablo içindeki tr'ları bul (onclick ile)
        items = soup.select('tr[onclick]')
        print(f"[{self.name}] {len(items)} ilan bulundu sayfada")
        
        for item in items:
            try:
                # Link
                onclick = item.get('onclick', '')
                if 'location.href=' not in onclick:
                    continue
                link_path = onclick.split("'")[1]
                link = f"{self.base_url}/{link_path}"
                
                # Başlık
                title_tag = item.select_one('td.baslik a')
                title = title_tag.get_text(strip=True) if title_tag else ''
                
                # Tarih (DD.MM.YYYY formatında)
                date_tag = item.select_one('td.tarih')
                date = date_tag.get_text(strip=True) if date_tag else ''
                
                # Konum
                location_tag = item.select_one('td.konum')
                location = location_tag.get_text(strip=True).replace('\n', ' / ') if location_tag else ''
                
                # Görsel
                img_tag = item.select_one('td.resim img')
                image = ''
                if img_tag:
                    image = img_tag.get('data-src', img_tag.get('src', ''))
                    if image and not image.startswith('http'):
                        image = f"{self.base_url}/{image}"
                
                # İlan türü
                fiyat_tag = item.select_one('td.fiyat')
                fiyat_text = fiyat_tag.get_text(strip=True) if fiyat_tag else ''
                ilan_turu = 'Sahiplendirme' if 'Sahiplendirme' in fiyat_text else 'Satılık'
                
                listing = {
                    'title': title,
                    'link': link,
                    'date': date,
                    'location': location,
                    'image': image,
                    'type': ilan_turu
                }
                listings.append(listing)
            except Exception as e:
                print(f"[{self.name}] Parse hatasi: {e}")
                continue
        
        return listings
    
    def extract_details(self, ad: Dict) -> Dict:
        """Detay sayfasından açıklama al"""
        try:
            soup = self.fetch_page(ad['link'])
            
            # Açıklama (farklı selector'lar dene)
            desc_tag = soup.find('div', class_=re.compile(r'description|aciklama|content'))
            if not desc_tag:
                desc_tag = soup.find('p', class_=re.compile(r'text|content'))
            
            aciklama = desc_tag.get_text(strip=True) if desc_tag else ad['title']
            
            return {
                'ilan_turu': ad['type'],
                'baslik': ad['title'],
                'aciklama': aciklama,
                'konum': ad['location'],
                'tarih1': ad['date'],
                'tarih2': self.parse_date_string(ad['date']),
                'kategori': 'Kedi',
                'gorsel': ad['image'],
                'link': ad['link']
            }
        except Exception as e:
            print(f"[{self.name}] Detay alma hatasi: {e}")
            # Hata olursa başlığı açıklama olarak kullan
            return {
                'ilan_turu': ad['type'],
                'baslik': ad['title'],
                'aciklama': ad['title'],
                'konum': ad['location'],
                'tarih1': ad['date'],
                'tarih2': self.parse_date_string(ad['date']),
                'kategori': 'Kedi',
                'gorsel': ad['image'],
                'link': ad['link']
            }
