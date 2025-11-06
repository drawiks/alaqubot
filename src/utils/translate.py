
from deep_translator import GoogleTranslator

def get_translate(text: str, target: str = "ru"):
    text = GoogleTranslator(source="auto", target=target).translate(text)
    return text