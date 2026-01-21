
from bs4 import BeautifulSoup
import requests

from .logger import LogManager
from .cache import cache

class CurrencyConverter:
    def __init__(self, log_path: str):
        self.log = LogManager(log_path).logger

    def fetch_rate(self, url: str):
        cache_key = f"rate:{url}"
        cached_value = cache.get_cache(cache_key)
        if cached_value is not None:
            return float(cached_value)
        
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                elem = soup.find("div", {"data-test": "instrument-price-last"})
                if elem:
                    rate = float(elem.text.strip().replace(",", "."))
                    cache.set_cache(cache_key, rate, ttl=3600)
                    self.log.info(f"cached rate for {url}: {rate}")
                    return rate
            else:
                self.log.error(f"{response.status_code} in {url}")
        except Exception as e:
            self.log.error(f"Error fetching {url}: {e}")
        return None

    def currency(self, amount: float | None):
        usd_rub = self.fetch_rate("https://ru.investing.com/currencies/usd-rub-chart")
        usd_uah = self.fetch_rate("https://ru.investing.com/currencies/usd-uah")

        if usd_rub is None or usd_uah is None:
            return "Иди нахуй!"
        
        if amount == None:
            return f"USD: → RUB: {usd_rub:.2f} ₽ | UAH: {usd_uah:.2f} ₴"
        else:
            return f"USD: $ {amount} → RUB: {amount * usd_rub:.2f} ₽ | UAH: {amount * usd_uah:.2f} ₴"
