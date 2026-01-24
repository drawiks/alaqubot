from deep_translator import GoogleTranslator
from lingua import Language, LanguageDetectorBuilder

languages = [Language.ENGLISH, Language.RUSSIAN]
detector = LanguageDetectorBuilder.from_languages(*languages).build()

def get_translate(text: str):
    if not text.strip():
        return "Пустой текст"

    try:
        detected_lang = detector.detect_language_of(text)
        
        match detected_lang:
            case Language.RUSSIAN:
                target = "en"
            case Language.ENGLISH:
                target = "ru"
            case _:
                target = "ru"

        translation = GoogleTranslator(source="auto", target=target).translate(text)
        return translation
        
    except Exception as e:
        return f"Ошибка: {e}"