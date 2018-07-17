import argparse
import json

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from update_load_balancer import NetworkBucket


def get_args():
    parser = argparse.ArgumentParser(description='Updates the BE Bucket of a load balancer.')
    parser.add_argument("-b", "--be-bucket", dest="be_bucket", help='Backend bucket to target')
    parser.add_argument("-s", "--gcs-bucket", dest="gcs_bucket", help='GCS bucket gor the backend bucket to reference.')
    parser.add_argument("-p", "--project", dest="gcp_project", help='Google Cloud Platform Project.')
    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()
    nb = NetworkBucket(backend_bucket=args.be_bucket, key_name='service.json')
    result = nb.update_lb_site(args.gcs_bucket)
    logger.info(json.dumps(result, indent=2))
