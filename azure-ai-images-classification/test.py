
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials
import os
from dotenv import load_dotenv


def get_credentials():
    try:
        load_dotenv()
        prediction_endpoint = os.getenv("PredictionEndpoint")
        prediction_key = os.getenv("PredictionKey")
        project_id = os.getenv("ProjectID")
        model_name = os.getenv("ModelName")
    except Exception as exception:
        print(exception)
    return prediction_endpoint, prediction_key, project_id, model_name


def images_prediction():
    try:
        # Get credentials
        prediction_endpoint, prediction_key, project_id, model_name = get_credentials()

        # Authenticate the client for the training API
        credentials = ApiKeyCredentials(prediction_key)
        client = CustomVisionPredictionClient(endpoint=prediction_endpoint, credentials=credentials)

        # Classify test images
        for image in os.listdir("test-images"):
            image_data = open(os.path.join("test-images", image), "rb").read()
            results = client.classify_image(project_id=project_id, published_name=model_name, image_data=image_data)

            # loop over each label prediction and print any with probability > 50%
            for prediction in results.predictions:
                if prediction.probability > 0.5:
                    print(image, ': {} ({:.0%})'.format(prediction.tag_name, prediction.probability))
    except Exception as exception:
        print(exception)


if __name__ == '__main__':
    #print(get_credentials())
    print(images_prediction())
