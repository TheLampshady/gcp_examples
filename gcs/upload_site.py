#!/usr/bin/env python
import logging
import os

from client.blob_client import GCSBucket


if __name__ == "__main__":
    bucket_name = os.environ.get('BUCKET_NAME')
    project_name = os.environ.get('PROJECT_NAME')
    token = os.environ.get('PROJECT_TOKEN', '')
    if not (bucket_name and project_name):
        logging.warning("Missing project and bucket Name.")
        exit(1)

    print("Project: %s" % project_name)
    print("Bucket: %s" % bucket_name)

    client = GCSBucket(bucket_name, project_name)

    root = "sample_site"
    # client.upload_folder(root, True)
    # client.upload_file(root + "/404.html", True)
    client.website_config(root + "/index.html", root + "/404.html", token=token)
    print("Done!")

