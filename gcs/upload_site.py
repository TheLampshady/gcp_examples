#!/usr/bin/env python
import logging
import os

from client.blob_client import GCSBucket


if __name__ == "__main__":
    bucket_name = os.environ.get('BUCKET_NAME')
    project_name = os.environ.get('PROJECT_NAME')
    # bucket_name = "simple-site-dev"

    if not (bucket_name and project_name):
        logging.warning("Missing project and bucket Name.")
        exit(1)

    print("Project: %s" % project_name)
    print("Bucket: %s" % bucket_name)

    root = "sample-site"

    client = GCSBucket(bucket_name, project_name)

    client.upload_folder(root, make_public=True)
    client.website_config()
    client.upload_file("index.html", make_public=True)
    client.upload_file("404.html", make_public=True)
    print("Done!")

