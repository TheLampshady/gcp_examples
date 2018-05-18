#!/usr/bin/env python
import argparse
import os

from ml.gcp_clients.cloud_client import CloudClient


def get_args():
    parser = argparse.ArgumentParser(description='Prints the language from an Image')
    parser.add_argument(dest="image", help='URL of an image')
    parser.add_argument('-l', '--language', dest='language', default='en', help="Language to return")

    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()
    api_key = os.environ.get('GCP_API_KEY')
    client = CloudClient(api_key)
    text = client.english_from_image(args.image, args.image)
    print(text)
