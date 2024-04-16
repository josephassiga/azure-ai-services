# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv
import os


def get_credentials():
    load_dotenv()
    key = os.environ.get('SPEECH_KEY')
    endpoint = os.environ.get('SPEECH_ENDPOINT')
    region = os.environ.get('SPEECH_REGION')
    return key, endpoint, region


# Authenticate the client using your key and endpoint
# def authenticate_client():
#    language_key, language_endpoint, _ = get_credentials()
#    ta_credential = AzureKeyCredential(language_key)
#    text_analytics_client = TextAnalyticsClient(
#        endpoint=language_endpoint,
#        credential=ta_credential)
#    return text_analytics_client


def recognize_from_microphone():
    load_dotenv()
    # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
    speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'),
                                           region=os.environ.get('SPEECH_REGION'))
    speech_config.speech_recognition_language = "fr-FR"
    speech_config.enable_dictation()

    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    print("Speak into your microphone.")
    speech_recognition_result = speech_recognizer.recognize_once_async().get()

    match speech_recognition_result.reason:
        case speechsdk.ResultReason.RecognizedSpeech:
            print("Recognized: {}".format(speech_recognition_result.text))
        case speechsdk.ResultReason.NoMatch:
            print("No speech could be recognized: {}".format(speech_recognition_result.no_match_details))
        case speechsdk.ResultReason.Canceled:
            cancellation_details = speech_recognition_result.cancellation_details
            print("Speech Recognition canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(cancellation_details.error_details))
                print("Did you set the speech resource key and region values?")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    recognize_from_microphone()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
