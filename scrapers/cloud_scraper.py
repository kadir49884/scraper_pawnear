# -*- coding: utf-8 -*-
"""
CloudScraper - Cloudflare/bot koruması bypass
"""
import cloudscraper
import time

class CloudScraper:
    """
    Cloudflare ve bot koruması olan siteleri aşmak için
    """
    
    def __init__(self):
        self.scraper = cloudscraper.create_scraper(
            browser={
                'browser': 'chrome',
                'platform': 'windows',
                'mobile': False
            }
        )
    
    def get_page_source(self, url: str, wait_time: int = 3) -> str:
        """
        Cloudflare korumalı sayfayı yükle
        """
        try:
            response = self.scraper.get(url, timeout=30)
            response.raise_for_status()
            time.sleep(wait_time)
            return response.text
        except Exception as e:
            print(f"[CloudScraper] Hata: {e}")
            raise
    
    def close(self):
        """Session'ı kapat"""
        if self.scraper:
            self.scraper.close()

