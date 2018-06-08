import base64
import logging
import re

from base_client import GCPClient


class SpeechClient(GCPClient):

    def __init__(self, api_key):
        super(SpeechClient, self).__init__(api_key)
        self.endpoint_file = 'https://speech.googleapis.com/v1/speech:recognize'
        self.endpoint_long = 'https://speech.googleapis.com/v1/speech:longrunningrecognize'
        self.endpoint_operation = "https://speech.googleapis.com/v1/operations/"

        self.endpoint =self.endpoint_long
        self.response = dict()

    @staticmethod
    def build_payload(audio_file):
        with open(audio_file, 'rb') as audio_file:
            audio_content = audio_file.read()
            content = base64.b64encode(audio_content)
        # audio = types.RecognitionAudio(content=content)

        config = {
                "enableAutomaticPunctuation": True,
                "encoding": "LINEAR16",
                "languageCode": "en-US",
                "model": "default"
        }

        return {
            "audio": {
                "content": content
            },
            "config": config
        }

    @staticmethod
    def build_long_payload(audio_url):
        config = {
            "encoding": "AMR_WB",
            "languageCode": "en-US",
            # "sampleRateHertz ": 16000
        }

        return {
            "audio": {
                "uri": audio_url
            },
            "config": config
    }

    @staticmethod
    def build_flac_payload(audio_url):
        config = {
            "encoding": "FLAC",
            "languageCode": "en-US",
        }

        return {
            "audio": {
                "uri": audio_url
            },
            "config": config
    }

    def process_long_audio(self, audio_url):
        payload = self.build_long_payload(audio_url)
        result = self.post(payload)
        if not result.get('responses'):
            logging.warning("No response found.")
            return dict()
        self.response = result['responses'][0]
        return self.response


def camel_to_title(value):
    first = re.compile(r'(.)([A-Z][a-z]+)')
    second = re.compile('([a-z0-9])([A-Z])')

    subbed = first.sub(r'\1 \2', value)
    return second.sub(r'\1 \2', subbed).lower().title()
