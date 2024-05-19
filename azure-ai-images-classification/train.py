# This is a sample Python script.
import os

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from dotenv import load_dotenv
from msrest.authentication import ApiKeyCredentials
from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateBatch, ImageFileCreateEntry, \
    Region, Project
import time


def get_credentials():
    try:
        load_dotenv()
        training_endpoint = os.getenv("TrainingEndpoint")
        training_key = os.getenv("TrainingKey")
        project_id = os.getenv("ProjectID")
    except Exception as exception:
        print(exception)
    return training_endpoint, training_key, project_id


def classifier_images():
    # Get credentials
    training_endpoint, training_key, project_id = get_credentials()

    # Authenticate a client to the training API
    credentials = ApiKeyCredentials(in_headers={"Training-key": training_key})
    training_client = CustomVisionTrainingClient(training_endpoint, credentials)

    # Get the custom vision project
    custom_vision_project = training_client.get_project(project_id)

    # Upload and tag images
    upload_images("train-images", training_client, custom_vision_project)

    # Train the model
    train_model(training_client, custom_vision_project)


def upload_images(image_directory, training_client: CustomVisionTrainingClient, custom_vision_project: Project):
    print("Uploading images ......")
    tags = training_client.get_tags(custom_vision_project.id)

    for tag in tags:
        print(tag.name)
        for image in os.listdir(os.path.join(image_directory, tag.name)):
            image_data = open(os.path.join(image_directory, tag.name, image), "rb").read()
            training_client.create_images_from_data(custom_vision_project.id, image_data, [tag.id])


def train_model(training_client: CustomVisionTrainingClient, custom_vision_project: Project):
    print("Training model ......")
    iteration = training_client.train_project(custom_vision_project.id)
    while iteration.status != "Completed":
        iteration = training_client.get_iteration(custom_vision_project.id, iteration.id)
        print(iteration.status, '...')
        time.sleep(5)
    print("Training model completed")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    classifier_images()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
