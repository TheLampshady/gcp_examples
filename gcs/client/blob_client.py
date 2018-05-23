import logging
from os.path import splitext, join
from os import walk

from google.cloud import storage


class GCSBucket(object):
    CONTENT_TYPE = {
        "html": "text/html",
        "js": "application/javascript",
        "css": "text/css",
        "jpeg": "image/jpeg",
        "jpg": "image/jpeg",
        "gif": "image/gif",
        "png": "image/png",
        "bmp": "image/bmp",
        "webp": "image/webp",
        "pdf": "application/pdf",
        "json": "application/json",
        "xml": "application/xml",
        "webm": "video/webm, ",
        "ogg": "video/ogg",
        "midi": "audio/midi",
        "mpeg": "audio/mpeg",
        "webm_audio": "audio/webm",
        "ogg_audio": "audio/ogg",
        "wav": "audio/wav",
        "ico": "image/x-icon",
        "woff": "font/woff",
        "woff2": "font/woff2",
    }
    CONTENT_TYPE_DEFAULT = "text/plain"

    def __init__(self, bucket_name, project=None):
        self.bucket_name = bucket_name
        self.storage_client = storage.Client(project)

    def create_bucket(self, bucket_name, make_public=False):
        """Creates a new bucket."""
        self._bucket = self.storage_client.create_bucket(bucket_name)
        if make_public:
            self._bucket.make_public(recursive=True, future=True)
        print("Bucket {} created".format(self._bucket.name))

    @property
    def bucket(self):
        if not hasattr(self, "_bucket"):
            self._bucket = self.storage_client.get_bucket(self.bucket_name)
        return self._bucket

    def upload_content(self, content, gcs_path, make_public=False):
        """Uploads a file to the bucket."""
        ext = self.get_ext(gcs_path)
        blob = self.bucket.blob(gcs_path)

        # blob.upload_from_filename(source_file_name)
        content_type = self.CONTENT_TYPE.get(ext)
        if not content_type:
            logging.warning("Unknown File Type: %s" % gcs_path)
        blob.upload_from_string(content, content_type)

        if make_public:
            blob.make_public()

        print("GCS Upload Complete: {}".format(gcs_path))

    def upload_folder(self, dir_src, dir_dest=None, make_public=False):
        site_list = [
            join(dir_path, file_name)
            for (dir_path, _, file_names) in walk(dir_src)
            for file_name in file_names if self.get_ext(file_name) in self.CONTENT_TYPE
        ]

        for file_name in site_list:
            with open(file_name, 'r') as myfile:
                content = myfile.read()
            if dir_dest:
                file_name = file_name.replace(dir_src, dir_dest, 1)
            self.upload_content(content, file_name, make_public=make_public)

    def upload_file(self, gcs_path, make_public=False):
        """Uploads a file to the bucket."""
        ext = self.get_ext(gcs_path)
        blob = self.bucket.blob(gcs_path)

        content_type = self.CONTENT_TYPE.get(ext)
        if not content_type:
            logging.warning("Unknown File Type: %s" % gcs_path)
        blob.upload_from_filename(gcs_path, content_type)

        if make_public:
            blob.make_public()

        print("GCS Upload Complete: {}".format(gcs_path))

    def make_site_public(self, prefix=None):
        if isinstance(prefix, basestring):
            prefix = prefix.strip('/')
        for blob in self.bucket.list_blobs(prefix=prefix):
            blob.make_public()
            print("GCS Made Public: {}".format(blob.name))

    def website_config(self, main_page_suffix="index.html", not_found_page="404.html"):
        """
        Seems to receive a 200 but no update the config (WIP)
        :param index:       index page filename
        :param not_found:   404 page filename
        :param token:       Authorization Bearer
                            Note: https://developers.google.com/oauthplayground/
        """
        self.bucket.configure_website(main_page_suffix, not_found_page)
        self.bucket.update()
        print("GCS Website Config Set: {}".format(self.bucket_name))

    def set_cors(self):
        policies = self.bucket.cors
        policies.append(
            {'origin': '/foo', 'next': '/bar'}
        )
        policies[1]['maxAgeSeconds'] = 3600
        # del policies[0]
        self.bucket.cors = policies
        self.bucket.update()

    @staticmethod
    def get_ext(value):
        return splitext(value)[1].strip(".").lower()
