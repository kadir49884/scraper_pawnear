# -*- coding: utf-8 -*-
from .base_scraper import BaseScraper
from typing import List, Dict
from bs4 import BeautifulSoup
import re
import time

class PetlebiScraper(BaseScraper):
    def __init__(self):
        super().__init__("Petlebi")
        self.base_url = "https://sosyal.petlebi.com"
    
    def scrape(self) -> List[Dict]:
        print(f"\n[{self.name}] Tarama basliyor...")
        all_results = []
        
        try:
            # 1. Kedi sahiplendirme
            all_results.extend(self._scrape_category('kedi-sahiplenme', 'Kedi'))
            
            # 2. Köpek sahiplendirme
            all_results.extend(self._scrape_category('kopek-sahiplenme', 'Köpek'))
            
            print(f"[{self.name}] Toplam {len(all_results)} ilan bulundu")
            return all_results
        except Exception as e:
            print(f"[{self.name}] Hata: {e}")
            return []
    
    def _scrape_category(self, category: str, kategori_adi: str) -> List[Dict]:
        """Belirli bir kategoriyi tara"""
        try:
            url = f"{self.base_url}/{category}"
            print(f"[{self.name}] {kategori_adi} kategorisi taranıyor...")
            
            soup = self.fetch_page(url)
            listings = self.parse_listings(soup, kategori_adi)
            result = self.get_last_24_hours_ads(listings)
            
            print(f"[{self.name}] {kategori_adi}: {len(result)} ilan")
            return result
        except Exception as e:
            print(f"[{self.name}] {kategori_adi} hatası: {e}")
            return []
    
    def parse_listings(self, soup, kategori: str) -> List[Dict]:
        """İlanları parse et"""
        listings = []
        
        # İlan linklerini bul (kedi veya köpek)
        pattern = r'/(kedi|kopek)-sahiplenme/\d+'
        links = soup.find_all('a', href=re.compile(pattern))
        
        for link in links:
            try:
                # Link ve başlık
                href = link.get('href')
                if not href.startswith('http'):
                    href = f"{self.base_url}{href}" if href.startswith('/') else f"{self.base_url}/{href}"
                
                # Başlık
                title_tag = link.find('p', class_='adopt-title')
                title = title_tag.get_text(strip=True) if title_tag else ''
                
                # Tarih
                date_tag = link.find('span', class_='date')
                date = ''
                if date_tag:
                    date_text = date_tag.get_text(strip=True)
                    # "22.11.2025" formatında
                    date = re.sub(r'[^\d.]', '', date_text)
                
                # Konum
                location_tag = link.find('span', class_='city')
                location = location_tag.get_text(strip=True) if location_tag else ''
                
                # Görsel
                img_tag = link.find('img')
                image = ''
                if img_tag:
                    image = img_tag.get('data-original') or img_tag.get('src', '')
                    if image and not image.startswith('http'):
                        # images.petlebi.com
                        if image.startswith('//'):
                            image = 'https:' + image
                        elif not 'default' in image:  # default resmi atlama
                            image = f"https://images.petlebi.com{image}"
                
                listing = {
                    'title': title,
                    'link': href,
                    'date': date,
                    'location': location,
                    'image': image,
                    'type': 'Sahiplendirme',
                    'category': kategori
                }
                listings.append(listing)
                
            except Exception as e:
                print(f"[{self.name}] Parse hatasi: {e}")
                continue
        
        return listings
    
    def extract_details(self, ad: Dict) -> Dict:
        """Detay sayfasından açıklama al"""
        aciklama = ad['title']  # Varsayılan
        
        try:
            time.sleep(0.5)  # Rate limiting
            soup = self.fetch_page(ad['link'])
            
            # Açıklama
            desc_tag = soup.find('div', class_='adopt-description')
            if desc_tag:
                aciklama = desc_tag.get_text(strip=True)
            
        except Exception as e:
            print(f"[{self.name}] Detay alma hatasi: {e}")
        
        return {
            'ilan_turu': ad['type'],
            'baslik': ad['title'],
            'aciklama': aciklama,
            'konum': ad['location'],
            'tarih1': ad['date'],
            'tarih2': self.parse_date_string(ad['date']),
            'kategori': ad['category'],
            'gorsel': ad['image'],
            'link': ad['link']
        }

