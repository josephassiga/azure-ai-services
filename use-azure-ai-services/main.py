# This is a sample Python script.
import sys

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from dotenv import load_dotenv
import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


def get_credentials():
    try:
        load_dotenv()
        azure_key = os.getenv('AZURE_KEY')
        azure_endpoint = os.getenv('AZURE_ENDPOINT')
    except FileNotFoundError:
        print_hi('No AZURE KEY and AZURE_ENDPOINT found')

    return azure_key, azure_endpoint


def get_language(text):
    azure_key, azure_endpoint = get_credentials()
    credentials = AzureKeyCredential(azure_key)
    client = TextAnalyticsClient(endpoint=azure_endpoint, credential=credentials)

    detected_language = client.detect_language(documents=[text])[0]
    print("Language detected: {}".format(detected_language.primary_language.name))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    get_language("Bonjour")
    get_language("Hello")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
