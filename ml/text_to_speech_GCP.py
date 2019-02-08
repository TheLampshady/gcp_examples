#!/usr/bin/env python
# coding=utf-8
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function

import argparse

from google.cloud.texttospeech import TextToSpeechClient, types, enums
from google.cloud.texttospeech_v1beta1 import TextToSpeechClient, types, enums

SERVICE_FILE = 'service_account.json'


def get_args():
    parser = argparse.ArgumentParser(description='Text to produce speech')
    parser.add_argument(dest="text", help='URL of an image')

    return parser.parse_args()


def main(text, locale='en-US'):
    client = TextToSpeechClient.from_service_account_file(str(SERVICE_FILE))

    input_text = types.SynthesisInput(text=text)

    # Note: the voice can also be specified by name.
    # Names of voices can be retrieved with client.list_voices().
    voice = types.VoiceSelectionParams(
        language_code=locale,
        # ssml_gender=enums.SsmlVoiceGender.FEMALE,
        name="en-US-Wavenet-A"
    )

    audio_config = types.AudioConfig(
        audio_encoding=enums.AudioEncoding.MP3)

    response = client.synthesize_speech(input_text, voice, audio_config)

    # The response's audio_content is binary.
    with open('output.mp3', 'wb') as out:
        out.write(response.audio_content)
        print('Audio content written to file "output.mp3"')


if __name__ == "__main__":
    text = ''
    # text = "谢谢"
    # text = "I must declare, the uk3 sub-zero is far superior to the uk3 scorpion.."
    args = get_args()
    main(text or args.text)

