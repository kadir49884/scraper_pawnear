# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from typing import List, Dict
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re

class BaseScraper(ABC):
    # İstenmeyen kelimeler (küçük harfe çevrilecek)
    BLOCKED_KEYWORDS = [
        'ödeme', 'para', 'kredi kartı', 'kredi karti',
        'antiparaziter', 'iade', 'nakit', 'taksit',
        'fiyat', 'ücret', 'ucret', 'garantili',
        'anne sütü', 'anne sutu', 'kaliteli',
        'yavru alirken', 'gönderim', 'gonderim'
    ]
    
    def __init__(self, name: str):
        self.name = name
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    @abstractmethod
    def scrape(self) -> List[Dict]:
        pass
    
    def fetch_page(self, url: str, timeout: int = 10) -> BeautifulSoup:
        response = requests.get(url, headers=self.headers, timeout=timeout)
        response.raise_for_status()
        return BeautifulSoup(response.content, 'html.parser')
    
    def goreli_tarih_hesapla(self, tarih_text: str) -> str:
        try:
            tarih_lower = tarih_text.lower()
            simdi = datetime.now()
            
            if 'dakika' in tarih_lower:
                dakika_match = re.search(r'(\d+)\s*dakika', tarih_lower)
                if dakika_match:
                    hedef_tarih = simdi - timedelta(minutes=int(dakika_match.group(1)))
                    return hedef_tarih.strftime('%Y-%m-%dT%H:%M:%SZ')
            elif 'saat' in tarih_lower:
                saat_match = re.search(r'(\d+)\s*saat', tarih_lower)
                if saat_match:
                    hedef_tarih = simdi - timedelta(hours=int(saat_match.group(1)))
                    return hedef_tarih.strftime('%Y-%m-%dT%H:%M:%SZ')
            elif 'gün' in tarih_lower or 'gun' in tarih_lower:
                gun_match = re.search(r'(\d+)\s*g[uü]n', tarih_lower)
                if gun_match:
                    hedef_tarih = simdi - timedelta(days=int(gun_match.group(1)))
                    return hedef_tarih.strftime('%Y-%m-%dT%H:%M:%SZ')
            
            return simdi.strftime('%Y-%m-%dT%H:%M:%SZ')
        except:
            return datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    
    def parse_date_string(self, date_str: str) -> str:
        """
        Tarih string'ini ISO 8601 formatına çevir
        DD.MM.YYYY -> 2025-11-22T00:00:00Z
        """
        try:
            # DD.MM.YYYY formatı (Petcim)
            if re.match(r'\d{2}\.\d{2}\.\d{4}', date_str):
                date_obj = datetime.strptime(date_str, '%d.%m.%Y')
                return date_obj.strftime('%Y-%m-%dT00:00:00Z')
            
            # Göreceli tarih (X Saat Önce)
            return self.goreli_tarih_hesapla(date_str)
        except:
            return datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    
    def _contains_blocked_keywords(self, text: str) -> bool:
        """Metinde istenmeyen kelime var mı kontrol et"""
        if not text:
            return False
        
        text_lower = text.lower()
        for keyword in self.BLOCKED_KEYWORDS:
            if keyword in text_lower:
                return True
        return False
    
    def get_last_24_hours_ads(self, listings: List[Dict]) -> List[Dict]:
        """
        Son 24 saat içindeki ilanları filtrele ve detayları al
        """
        result = []
        now = datetime.now()
        
        for ad in listings:
            try:
                # Tarih kontrolü (DD.MM.YYYY formatı)
                date_str = ad.get('date', '')
                if re.match(r'\d{2}\.\d{2}\.\d{4}', date_str):
                    date_obj = datetime.strptime(date_str, '%d.%m.%Y')
                    diff = now - date_obj
                    if diff.days > 1:  # 1 günden eski
                        continue
                
                # Detayları al
                detailed_ad = self.extract_details(ad)
                if detailed_ad:
                    # İstenmeyen kelime kontrolü
                    baslik = detailed_ad.get('baslik', '')
                    aciklama = detailed_ad.get('aciklama', '')
                    
                    if self._contains_blocked_keywords(baslik) or self._contains_blocked_keywords(aciklama):
                        print(f"[{self.name}] Filtrelendi (istenmeyen kelime): {baslik[:50]}...")
                        continue
                    
                    result.append(detailed_ad)
            except Exception as e:
                print(f"[{self.name}] Detay alma hatasi: {e}")
                continue
        
        return result
    
    @abstractmethod
    def parse_listings(self, soup) -> List[Dict]:
        """İlanları parse et"""
        pass
    
    @abstractmethod
    def extract_details(self, ad: Dict) -> Dict:
        """Detay sayfasından bilgileri al"""
        pass

