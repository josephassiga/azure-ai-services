# This is a sample Python script.
# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import sys

from dotenv import load_dotenv
import os
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from azure.keyvault.secrets import SecretClient
from azure.identity import ClientSecretCredential

from dotenv import load_dotenv
import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient


def get_credentials():
    try:
        load_dotenv()
        azure_endpoint = os.getenv("AZURE_ENDPOINT")
        key_vault = os.getenv("KEY_VAULT")
        tenant_id = os.getenv("TENANT_ID")
        app_id = os.getenv("APP_ID")
        app_password = os.getenv("APP_PASSWORD")

        key_vault_uri = f"https://{key_vault}.vault.azure.net/"
        credential = ClientSecretCredential(tenant_id, app_id, app_password)
        keyvault_client = SecretClient(key_vault_uri, credential)
        secret_key = keyvault_client.get_secret("AI-Services-Key")
        azure_key = secret_key.value

    except FileNotFoundError:
        print("No credentials file found.")

    return azure_endpoint, azure_key

def detect_language(text):

    azure_endpoint, azure_key = get_credentials()
    credential = AzureKeyCredential(azure_key)
    client = TextAnalyticsClient(azure_endpoint, credential)

    detected_language = client.detect_language([text])[0]

    print("Language detected: {}".format(detected_language.primary_language.name))




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
 detect_language("Bonjour")
 detect_language("Salut")
 detect_language("Gut")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
