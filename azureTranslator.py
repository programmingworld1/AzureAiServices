from azure.core.credentials import AzureKeyCredential
from azure.ai.translation.text import TextTranslationClient
from azure.ai.translation.text.models import InputTextItem

# API key and endpoint from Azure Foundry
key = ""
endpoint = "https://dqwdwfsfsdfewf.cognitiveservices.azure.com/"

# Create the translation client using the API key and endpoint
client = TextTranslationClient(credential=AzureKeyCredential(key), endpoint=endpoint)

# The text(s) to translate
input_text_elements = [InputTextItem(text="Hola")]

# Translate to French and English — the source language is auto-detected
translation_results = client.translate(body=input_text_elements, to_language=["fr", "en"])

idx = 0
for translation in translation_results:
    input_text = input_text_elements[idx].text
    idx += 1
    source_language = translation.detected_language  # auto-detected source language
    for translated_text in translation.translations:
        line = f"'{input_text}' was translated from {source_language.language} to {translated_text.to} as '{translated_text.text}'."
        # encode to cp1252 to avoid Unicode errors in the Windows terminal
        print(line.encode("cp1252", errors="replace").decode("cp1252"))
