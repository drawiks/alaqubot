
import requests
import random

from src.config import KINOPOISK_API
from .logger import LogManager

class Film:
    HEADERS = {"X-API-KEY": KINOPOISK_API, "Content-Type": "application/json"}
    PARAMS = {"type": "TOP_250_BEST_FILMS", "page": random.randint(1, 13)}
    
    def __init__(self, log_path: str):
        self.log = LogManager(log_path).logger
    
    def fetch(self):
        try:
            response = requests.get("https://kinopoiskapiunofficial.tech/api/v2.2/films/top", headers=self.HEADERS, params=self.PARAMS)
            response.raise_for_status() 
            data = response.json()
            
            films = data.get('films', [])
            
            if films:
                movie = random.choice(films)
                data = {
                    "movie": movie.get('nameRu'),
                    "rating": movie.get('rating'),
                    "year": movie.get('year')
                }
                return f"Фильм: {movie.get("nameRu")}|Рейтинг: {movie.get('rating')}|Год:{movie.get('year')}"
            else:
                self.log.error(f"{response.status_code}")
                return "Иди нахуй!"
        except Exception as e:
            self.log.error(f"Error fetching: {e}")
