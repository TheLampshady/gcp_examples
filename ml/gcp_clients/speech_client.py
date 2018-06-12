import base64
import logging
import os
import re

from time import sleep

from base_client import GCPClient


class SpeechClient(GCPClient):

    def __init__(self, api_key):
        super(SpeechClient, self).__init__(api_key)
        self.endpoint_file = 'https://speech.googleapis.com/v1/speech:recognize'
        self.endpoint_long = 'https://speech.googleapis.com/v1/speech:longrunningrecognize'
        self.endpoint_operation = "https://speech.googleapis.com/v1/operations/"

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
        audio = {
                "content": content
        }
        return {
            "audio": audio,
            "config": config
        }


    @staticmethod
    def build_long_payload(audio_url):
        config = {
            'language_code': 'en-US',
        }
        audio = {
                'uri': audio_url
        }

        return {
            'audio': audio,
            'config': config
    }

    def process_long_audio(self, audio_url):
        ext = os.path.splitext(audio_url)[1].lower()
        payload = self.build_long_payload(audio_url)

        # result = self.post(payload, self.endpoint_long)
        # if not result.get('name'):
        #     logging.warning("No response found.")
        #     return dict()
        result = dict(name='8858890520680468903')
        response = self._poll_endpoint(self.endpoint_operation + result['name'])

        self.response = response
        return self.build_response()

    def _poll_endpoint(self, url):
        while True:
            result = self.get(url)
            if not result or result.get('done'):
                return result.get('response')
            sleep(10)
            progress = result.get('metadata', {}).get('progressPercent', 0)
            print("Progress: %d%%" % progress)

    def build_response(self):
        if not self.response.get('results'):
            logging.warning("No result found.")
            return dict()
        return [
            entry.get('alternatives', [dict()])[0].get('transcript', '').strip().capitalize()
            for entry in self.response['results']
        ]


def camel_to_title(value):
    first = re.compile(r'(.)([A-Z][a-z]+)')
    second = re.compile('([a-z0-9])([A-Z])')

    subbed = first.sub(r'\1 \2', value)
    return second.sub(r'\1 \2', subbed).lower().title()
