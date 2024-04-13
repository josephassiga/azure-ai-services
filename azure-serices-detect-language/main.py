# This is a sample Python script.
from xml.dom.minidom import Document

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
import os

env_file_path = os.path.join('app-settings.env')
load_dotenv(dotenv_path=env_file_path)  # take environment variables from .env.


def get_credentials():
    key = os.environ.get('LANGUAGE_KEY')
    endpoint = os.environ.get('LANGUAGE_ENDPOINT')
    return key, endpoint


# Authenticate the client using your key and endpoint
def authenticate_client():
    language_key, language_endpoint = get_credentials()
    ta_credential = AzureKeyCredential(language_key)
    text_analytics_client = TextAnalyticsClient(
        endpoint=language_endpoint,
        credential=ta_credential)
    return text_analytics_client


client = authenticate_client()


# Example method for detecting the language of text
def language_detection_example(client):
    try:
        input_text = ''
        while input_text.lower() != 'exit':
            input_text = str(input("Enter some text ('exit' to stop) :"))
            documents = []
            if input_text.lower() != 'exit':
                documents.append(input_text.lower())
                response = client.detect_language(documents=documents, country_hint='us', )[0]
                print("Language: ", response.primary_language.name)

    except Exception as err:
        print("Encountered exception. {}".format(err))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    language_detection_example(client)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
