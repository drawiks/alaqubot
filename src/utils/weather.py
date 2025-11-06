
from deep_translator import GoogleTranslator
from src.config import WEATHER_API
import requests

def get_weather(city: str):
    
    city = GoogleTranslator(source="auto", target="en").translate(city)

    response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API}&units=metric&lang=ru")
    data = response.json()

    if data.get("cod") != 200:
        return f"Не удалось найти город: {city}"

    name = data["name"]
    temp = data["main"]["temp"]
    feels = data["main"]["feels_like"]
    description = data["weather"][0]["description"].capitalize()

    return f"Погода в {name}: {description}, {temp}°C (ощущается как {feels}°C)"
