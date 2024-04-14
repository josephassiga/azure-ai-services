from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential
from dotenv import load
import os

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
        credential=AzureKeyCredential(key)
    )
    return client


def read_image(file_name):
    image_dir = os.path.join(os.getcwd(), 'images')
    image_path = os.path.join(image_dir, file_name)
    with open(image_path, "rb") as file:
        image_bytes = file.read()
    return image_bytes


def get_image_metadata():
    client = authenticate_client()
    image_data = read_image('married-couples.jpg')
    describe_response = client.analyze(image_data=image_data, language='en',visual_features=[VisualFeatures.DENSE_CAPTIONS,VisualFeatures.TAGS])
    print(describe_response)


if __name__ == "__main__":
    print(get_image_metadata())
