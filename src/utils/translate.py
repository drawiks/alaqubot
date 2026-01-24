
from deep_translator import GoogleTranslator
from langdetect import detect, DetectorFactory

DetectorFactory.seed = 0

def get_translate(text: str):
    try:
        source_lang = detect(text)
        target_lang = "en" if source_lang == "ru" else "ru"
        
        translation = GoogleTranslator(source="auto", target=target_lang).translate(text)
        return translation
    
    except Exception as e:
        return f"Ошибка перевода: {e}"