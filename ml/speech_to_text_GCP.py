#!/usr/bin/env python
import argparse
import os

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

from google.auth.credentials import Credentials

def get_args():
    parser = argparse.ArgumentParser(description='Prints the language from an Image')
    parser.add_argument(dest="audio", help='URL of an image')

    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()
    # api_key = os.environ.get('GCP_API_KEY')
    # project_name = os.environ.get('PROJECT_NAME')
    project_name = os.environ['GOOGLE_APPLICATION_CREDENTIALS'] == 'service_account.json'

    client = speech.SpeechClient()

    audio = types.RecognitionAudio(uri=args.audio)
    config = types.RecognitionConfig(language_code='en-US')

    operation = client.long_running_recognize(config, audio)

    print('Waiting for operation to complete...')
    response = operation.result(timeout=90)

    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        print(u'Transcript: {}'.format(result.alternatives[0].transcript))
        print('Confidence: {}'.format(result.alternatives[0].confidence))
