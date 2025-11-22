# -*- coding: utf-8 -*-
from typing import List, Dict
from .gorenduyan_scraper import GorenDuyanScraper
from .petcim_scraper import PetcimScraper
from .petlebi_scraper import PetlebiScraper

class ScraperManager:
    def __init__(self):
        self.scrapers = [
            GorenDuyanScraper(),
            PetcimScraper(),
            PetlebiScraper()
        ]
    
    def scrape_all(self) -> List[Dict]:
        all_ilanlar = []
        for scraper in self.scrapers:
            try:
                ilanlar = scraper.scrape()
                all_ilanlar.extend(ilanlar)
            except Exception as e:
                print(f"[HATA] {scraper.name}: {e}")
        return self._remove_duplicates(all_ilanlar)
    
    def _remove_duplicates(self, ilanlar: List[Dict]) -> List[Dict]:
        unique, seen = [], set()
        for ilan in ilanlar:
            key = f"{ilan['baslik']}_{ilan['kategori']}"
            if key not in seen:
                unique.append(ilan)
                seen.add(key)
        return unique

