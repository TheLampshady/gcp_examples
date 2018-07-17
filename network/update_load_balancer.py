import json
import logging
import os
from time import sleep

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
from oauth2client.service_account import ServiceAccountCredentials


class NetworkBucket(object):

    def __init__(self, project=None, backend_bucket=None, key_name=None):
        self.operation_id = None
        self.project = project or os.getenv("GCP_PROJECT")
        self.backend_bucket = backend_bucket or os.getenv("BE_BUCKET")

        credentials = ServiceAccountCredentials.from_json_keyfile_name(key_name) \
            if key_name else \
            GoogleCredentials.get_application_default()

        self.service = discovery.build('compute', 'v1', credentials=credentials)

    def update_lb_site(self, gcs_bucket, be_bucket=None):
        result = self.update_bucket(gcs_bucket=gcs_bucket, be_bucket=be_bucket)
        for i in range(3):
            if result.get('status') == 'DONE':
                break
            sleep(2)
            result = self.get_status()
        return self.get_bucket()

    def get_bucket(self, be_bucket=None):
        be_bucket = be_bucket or self.backend_bucket
        request = self.service.backendBuckets().get(
            project=self.project,
            backendBucket=be_bucket
        )
        return request.execute()

    def update_bucket(self, gcs_bucket='sample-site-dev', be_bucket=None):
        be_bucket = be_bucket or self.backend_bucket

        body = {
            'bucketName': gcs_bucket
        }

        request = self.service.backendBuckets().patch(
            project=self.project,
            backendBucket=be_bucket,
            body=body
        )
        result = request.execute()
        self.operation_id = result.get('name')
        return result

    def get_status(self):
        if not self.operation_id:
            logging.warning("No pending requests.")
            raise AttributeError("No pending requests.")

        request = self.service.globalOperations().get(
            project=self.project,
            operation=self.operation_id
        )
        result = request.execute()
        if result.get('error'):
            message = "Invalid Request:\n\n%s" % json.dumps(result['error'], indent=2)
            logging.error(message)

        return result


