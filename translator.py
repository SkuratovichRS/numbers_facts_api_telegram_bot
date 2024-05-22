from googletrans import Translator


def translate(text):
    translator = Translator()
    result = translator.translate(text, "ru")
    return result.text
