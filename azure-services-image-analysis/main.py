# This is a sample Python script.
import base64

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from dotenv import load
import os
from PIL import Image, ImageDraw
import sys
from matplotlib import pyplot as plt
from azure.core.exceptions import HttpResponseError
import requests
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential


def get_image_data(image_name):
    image_path = os.path.join(os.getcwd(), 'images', image_name)
    with open(image_path, 'rb') as f:
        image_data = f.read()
    return image_data


def get_client_image_analysis():
    load()
    key = os.getenv("AZURE_SERVICE_KEY")
    endpoint = os.getenv("AZURE_SERVICE_ENDPOINT")
    client = ImageAnalysisClient(endpoint, AzureKeyCredential(key))
    return client


def analyze_image(image_filename):
    client = get_client_image_analysis()
    image_data = get_image_data(image_filename)
    result = client.analyze(
        image_data=image_data,
        visual_features=[
            VisualFeatures.CAPTION,
            VisualFeatures.DENSE_CAPTIONS,
            VisualFeatures.TAGS,
            VisualFeatures.OBJECTS,
            VisualFeatures.PEOPLE])

    # ®print(result)
    # Display analysis results
    # Get image captions
    if result.caption is not None:
        print("\nCaption:")
        print(" Caption: '{}' (confidence: {:.2f}%)".format(result.caption.text, result.caption.confidence * 100))

    # Get image dense captions
    if result.dense_captions is not None:
        print("\nDense Captions:")
        for caption in result.dense_captions.list:
            print(" Caption: '{}' (confidence: {:.2f}%)".format(caption.text, caption.confidence * 100))

    # Get image tags
    if result.tags is not None:
        print("\nTags:")
        for tag in result.tags.list:
            print(" Tag: '{}' (confidence: {:.2f}%)".format(tag.name, tag.confidence * 100))

    # Get people in the image
    if result.people is not None:
        print("\nPeople:")
        for person in result.people.list:
            print(" Person: '{}' (confidence: {:.2f}%)".format(person.bounding_box, person.confidence * 100))

    # Get objects in the image
    if result.objects is not None:
        print("\nObjects in image:")

        # Prepare image for drawing

        image = Image.open(os.path.join(os.getcwd(), 'images', image_filename))
        fig = plt.figure(figsize=(image.width / 100, image.height / 100))
        plt.axis('off')
        draw = ImageDraw.Draw(image)
        color = 'cyan'

        for detected_object in result.objects.list:
            # Print object name
            print(
                " {} (confidence: {:.2f}%)".format(detected_object.tags[0].name,
                                                   detected_object.tags[0].confidence * 100))

            # Draw object bounding box
            r = detected_object.bounding_box
            bounding_box = ((r.x, r.y), (r.x + r.width, r.y + r.height))
            draw.rectangle(bounding_box, outline=color, width=3)
            plt.annotate(detected_object.tags[0].name, (r.x, r.y), backgroundcolor=color)

        # Save annotated image
        plt.imshow(image)
        plt.tight_layout(pad=0)
        outputfile = 'objects.jpg'
        fig.savefig(outputfile)
        print('  Results saved in', outputfile)


def remove_image_background(image_filename):
    # Remove the background from the image or generate a foreground matte
    print('\nRemoving background from image...')

    load()
    key = os.getenv("AZURE_SERVICE_KEY")
    endpoint = os.getenv("AZURE_SERVICE_ENDPOINT")
    api_version = '2023-02-01-preview'
    mode = 'backgroundRemoval'
    url = "{}computervision/imageanalysis:segment?api-version={}&mode={}".format(endpoint, api_version, mode)

    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/octet-stream"  # multipart/form-data
    }

    # image_url = "https://github.com/MicrosoftLearning/mslearn-ai-vision/blob/main/Labfiles/01-analyze-images/Python/image-analysis/images/{}?raw=true".format(
    #   image_filename)

    response = requests.post(url, headers=headers,
                             data=get_image_data(os.path.join(os.getcwd(), 'images', image_filename)))

    image = response.content
    filename_without_bg = image_filename.removesuffix(".jpg") + "_without_background.jpg"
    # print(filename_without_bg)
    with open(filename_without_bg, "wb") as file:
        file.write(image)
    print("  Results saved in {} \n".format(filename_without_bg))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # analyze_image("street.jpg")
    for filename in os.listdir("images"):
        remove_image_background(filename)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
