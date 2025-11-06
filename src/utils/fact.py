
from deep_translator import GoogleTranslator
import requests

def get_fact():
    response = requests.get("https://uselessfacts.jsph.pl/api/v2/facts/random")
    if response.status_code != 200:
        return "Иди нахуй!"
    
    fact = GoogleTranslator(source='en', target='ru').translate(response.json().get("text", ""))
    return fact
