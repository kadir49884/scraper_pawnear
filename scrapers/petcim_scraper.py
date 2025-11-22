# -*- coding: utf-8 -*-
from .base_scraper import BaseScraper
from .cloud_scraper import CloudScraper
from typing import List, Dict
from bs4 import BeautifulSoup
import time
import re

class PetcimScraper(BaseScraper):
    def __init__(self):
        super().__init__("Petcim")
        self.base_url = "https://www.petcim.com"
        self.cloud_scraper = None
        self.request_delay = 0.5  # Rate limiting: 0.5 saniye bekle
    
    def scrape(self) -> List[Dict]:
        print(f"\n[{self.name}] Tarama basliyor (CloudScraper)...")
        all_results = []
        
        # CloudScraper'ı başlat (her iki kategori için aynı session)
        self.cloud_scraper = CloudScraper()
        
        try:
            # 1. Kedi ilanları
            all_results.extend(self._scrape_category('kedi', 40, 'Kedi'))
            
            # 2. Köpek ilanları
            all_results.extend(self._scrape_category('kopek', 41, 'Köpek'))
            
            print(f"[{self.name}] Toplam {len(all_results)} ilan bulundu")
            return all_results
        except Exception as e:
            print(f"[{self.name}] Hata: {e}")
            return []
        finally:
            if self.cloud_scraper:
                self.cloud_scraper.close()
    
    def _scrape_category(self, category: str, category_id: int, kategori_adi: str) -> List[Dict]:
        """Belirli bir kategoriyi tara"""
        try:
            url = f"{self.base_url}/sahibinden-satilik-{category}-ilanlar-{category_id}"
            print(f"[{self.name}] {kategori_adi} kategorisi taranıyor...")
            
            # Sayfa yükle
            page_source = self.cloud_scraper.get_page_source(url, wait_time=2)
            soup = BeautifulSoup(page_source, 'html.parser')
            
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
        
        # Tablo içindeki tr'ları bul (onclick ile)
        items = soup.select('tr[onclick]')
        
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
                if location_tag:
                    konum_parts = [s.strip() for s in location_tag.stripped_strings]
                    location = ' / '.join(konum_parts)
                else:
                    location = ''
                
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
                    'type': ilan_turu,
                    'category': kategori  # Kategoriyi ekle
                }
                listings.append(listing)
            except Exception as e:
                print(f"[{self.name}] Parse hatasi: {e}")
                continue
        
        return listings
    
    def extract_details(self, ad: Dict) -> Dict:
        """Detay sayfasından açıklama al (CloudScraper ile)"""
        aciklama = ad['title']  # Varsayılan
        
        # Rate limiting - Her request arasında bekle
        time.sleep(self.request_delay)
        
        # Retry mekanizması
        max_retries = 2
        for attempt in range(max_retries):
            try:
                if not self.cloud_scraper:
                    self.cloud_scraper = CloudScraper()
                
                page_source = self.cloud_scraper.get_page_source(ad['link'], wait_time=1)
                soup = BeautifulSoup(page_source, 'html.parser')
                
                # Açıklama - Petcim'de "div.aciklama" içinde
                desc_tag = soup.find('div', class_='aciklama')
                if desc_tag:
                    aciklama = desc_tag.get_text(strip=True)
                break  # Başarılı, döngüden çık
                
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"[{self.name}] Retry {attempt + 1}/{max_retries}")
                    time.sleep(2)  # Hata durumunda daha uzun bekle
                else:
                    print(f"[{self.name}] Detay alma hatasi: {e}")
        
        return {
            'ilan_turu': ad['type'],
            'baslik': ad['title'],
            'aciklama': aciklama,
            'konum': ad['location'],
            'tarih1': ad['date'],
            'tarih2': self.parse_date_string(ad['date']),
            'kategori': ad.get('category', 'Kedi'),
            'gorsel': ad['image'],
            'link': ad['link']
        }
