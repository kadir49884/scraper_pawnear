# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from typing import List, Dict
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re

class BaseScraper(ABC):
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

