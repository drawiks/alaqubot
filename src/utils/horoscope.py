
from bs4 import BeautifulSoup
import requests

from .logger import LogManager
from .cache import cache

class Horoscope:
    
    HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; horoscope/1.0)"}
    URLS = {
        "овен": "https://orakul.com/horoscope/astrologic/general/aries/today.html",
        "телец": "https://orakul.com/horoscope/astrologic/general/taurus/today.html",
        "близнецы": "https://orakul.com/horoscope/astrologic/general/gemini/today.html",
        "рак": "https://orakul.com/horoscope/astrologic/general/cancer/today.html",
        "лев": "https://orakul.com/horoscope/astrologic/general/lion/today.html",
        "дева": "https://orakul.com/horoscope/astrologic/general/virgo/today.html",
        "весы": "https://orakul.com/horoscope/astrologic/general/libra/today.html",
        "скорпион": "https://orakul.com/horoscope/astrologic/general/scorpio/today.html",
        "стрелец": "https://orakul.com/horoscope/astrologic/general/sagittarius/today.html",
        "козерог": "https://orakul.com/horoscope/astrologic/general/capricorn/today.html",
        "водолей": "https://orakul.com/horoscope/astrologic/general/aquarius/today.html",
        "рыбы": "https://orakul.com/horoscope/astrologic/general/pisces/today.html",
    }
    
    def __init__(self, log_path):
        self.log = LogManager(log_path).logger
        
    def fetch(self, zodiac: str):
        zodiac = zodiac.lower()
        if zodiac not in self.URLS:
            return "Неверный знак зодиака."
        
        cache_key = f"horoscope:{zodiac}"
        cached_value = cache.get_cache(cache_key)
        if cached_value is not None:
            return cached_value
        
        try:
            response = requests.get(self.URLS[zodiac.lower()], headers=self.HEADERS, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, "html.parser")
            p = soup.find("p", class_="")
            
            if p:
                result = p.get_text(strip=True)
                cache.set_cache(cache_key, result, ttl=86400)
                return result
        except Exception as e:
            self.log.error(f"error fetching horoscope for {zodiac}: {e}")