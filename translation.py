import six
import os
from google.cloud import translate_v2 as translate

credential_path = "creds.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credential_path

translate_client = translate.Client()

def translateText(text, targetLang):
    if isinstance(text, six.binary_type):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=targetLang, format_="text")
    return result["translatedText"]