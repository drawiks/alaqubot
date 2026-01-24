
from deep_translator import GoogleTranslator
import langid

def get_translate(text: str):
    if not text or len(text.strip()) < 2:
        return "Текст слишком короткий для перевода."

    try:
        detected_lang = langid.classify(text)[0]
        target_lang = 'en' if detected_lang == 'ru' else 'ru'
        
        result = GoogleTranslator(source='auto', target=target_lang).translate(text)
        
        return result if result else "Не удалось получить перевод."

    except Exception as e:
        return f"Ошибка перевода: {str(e)}"