# NOTE: This does NOT use Microsoft Foundry.
# It uses the Language service resource directly via the Azure Portal.
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

def main():

    # Here I am using Microsoft Foundry Ai Services
    # It's not the project endpoint but the Azure AI Services endpoint, which you can find in the overview of Microsoft Foundry
    endpoint = "https://dqwdwfsfsdfewf.cognitiveservices.azure.com/"
    key = "" # take key from Microsoft Foundry overview page

    # Here I am using the Language service resource directly via the Azure Portal.
    #endpoint = "https://languawiehihekgerg.cognitiveservices.azure.com/"
    #key = "" # take key from Microsoft Foundry overview page

    #both these ways work, because they are both using the same underlying Azure Cognitive Services resource, just accessed through different endpoints.


    client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    # Example text to analyze
    documents = ["Hello World!", "Bonjour le monde!"]

    # Detect language
    response = client.detect_language(documents=documents)
    for doc in response:
        print(f"Document: {doc.id}")
        print(f"\tPrimary Language: {doc.primary_language.name}")
        print(f"\tISO6391 Name: {doc.primary_language.iso6391_name}")
        print(f"\tConfidence Score: {doc.primary_language.confidence_score}")

if __name__ == "__main__":
    main()
