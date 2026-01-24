
from deep_translator import GoogleTranslator
import re

def get_translate(text: str):
    if re.search(r'[а-яА-Я]', text):
        target_lang = "en"
    else:
        target_lang = "ru"

    translated = GoogleTranslator(source="auto", target=target_lang).translate(text)
    return translated
