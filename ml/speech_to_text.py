#!/usr/bin/env python
import argparse
import os

from ml.gcp_clients.speech_client import SpeechClient


def get_args():
    parser = argparse.ArgumentParser(description='Prints the language from an Image')
    parser.add_argument(dest="audio", help='URL of an image')

    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()
    api_key = os.environ.get('GCP_API_KEY')
    client = SpeechClient(api_key)
    text = client.process_long_audio(args.audio)
    print(text)
