from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from dotenv import load
import os
import sys
import logging

# Acquire the logger for this client library. Use 'azure' to affect both
# 'azure.core` and `azure.ai.vision.imageanalysis' libraries.
logger = logging.getLogger("azure")

# Set the desired logging level. logging.INFO or logging.DEBUG are good options.
logger.setLevel(logging.INFO)

# Direct logging output to stdout (the default):
handler = logging.StreamHandler(stream=sys.stdout)
# Or direct logging output to a file:
# handler = logging.FileHandler(filename = 'sample.log')
logger.addHandler(handler)

# Optional: change the default logging format. Here we add a timestamp.
formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s:%(message)s")
handler.setFormatter(formatter)


env_file_path = os.path.join('app-settings.env')
load(filepath=env_file_path)  # take environment variables from .env.


# Set the values of your computer vision endpoint and computer vision key
# as environment variables:
def get_credentials():
    try:
        endpoint = os.environ["VISION_ENDPOINT"]
        key = os.environ["VISION_KEY"]
    except KeyError:
        print("Missing environment variable 'VISION_ENDPOINT' or 'VISION_KEY'")
        exit()
    return endpoint, key


def authenticate_client():
    endpoint, key = get_credentials()
    # Create an Image Analysis client for synchronous operations
    client = ImageAnalysisClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key),
        logging_enable=True
    )
    return client


def read_image(file_name):
    image_path = os.path.join(os.getcwd(), 'documents', file_name)
    with open(image_path, "rb") as file:
        image_bytes = file.read()
    return image_bytes

def extract_text_from_images():
    client = authenticate_client()
    for filename in os.listdir('documents'):
        print(f"Start ==== Extracting text from: {filename} ======")

        try:
            image_bytes = read_image(filename)
            response = client.analyze(image_bytes, visual_features=[VisualFeatures.READ])
            print(f"  File name: {filename}  Analyzed Text: {response} ")
        except HttpResponseError as e:
            print(f"Status code: {e.status_code}")
            print(f"Reason: {e.reason}")
            print(f"Message: {e.error.message}")
            exit(0)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    extract_text_from_images()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
