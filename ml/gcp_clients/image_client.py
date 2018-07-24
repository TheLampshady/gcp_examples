import re
import logging
import json

from .base_client import GCPClient

WEB_IMAGE = 'imageUri'
GCS_IMAGE = 'gcsImageUri'
MAX_RESULTS = 'maxResults'
ENGLISH = 'en'

# All features
# https://cloud.google.com/vision/docs/reference/rest/v1/images/annotate#Feature
TEXT_DETECTION = 'TEXT_DETECTION'
LABEL_DETECTION = "LABEL_DETECTION"
WEB_DETECTION = "WEB_DETECTION"
FACE_DETECTION = "FACE_DETECTION"
LANDMARK_DETECTION = "LANDMARK_DETECTION"


MAX_LIST = [
    TEXT_DETECTION,
    LABEL_DETECTION,
    WEB_DETECTION
]

API_CONFIG = {
    TEXT_DETECTION: ['fullTextAnnotation', 'textAnnotations'],
    LABEL_DETECTION: ['labelAnnotations'],
    WEB_DETECTION: ['webDetection'],
    FACE_DETECTION: ['faceAnnotations'],
    LANDMARK_DETECTION: ['landmarkAnnotations'],
}

LIKELIHOOD = dict(
    UNKNOWN=0,
    VERY_UNLIKELY=1,
    UNLIKELY=2,
    POSSIBLE=3,
    LIKELY=4,
    VERY_LIKELY=5
)

THRESHOLD = 3


class ImageClient(GCPClient):

    def __init__(self, api_key):
        super(ImageClient, self).__init__(api_key)
        self.endpoint = 'https://vision.googleapis.com/v1/images:annotate'
        self.response = dict()

    @staticmethod
    def build_payload(image_url, features, max_results=None):
        if not features:
            features = (TEXT_DETECTION,)
        if isinstance(features, basestring):
            if features.lower() == 'all':
                features = API_CONFIG.keys()
            else:
                features = [features]
        source = GCS_IMAGE if image_url.startswith("gs://") else WEB_IMAGE
        image = {
            "source": {source: image_url}
        }

        features_props = [
            {"type": feature, MAX_RESULTS: max_results} if feature in MAX_LIST and max_results else {"type": feature}
            for feature in features
        ]

        return {
            "requests": [
                {"image": image, "features": features_props}
            ]
        }

    def process_image(self, image_url, features, max_results=10):
        payload = self.get_image_payload(image_url, features, max_results)
        result = self.post(payload)
        if not result.get('responses'):
            logging.warning("No text response found.")
            return dict()
        self.response = result['responses'][0]
        return self.response

    def display_text(self):
        response_name = API_CONFIG.get(TEXT_DETECTION, [''])[0]
        if not self.response.get(response_name, None):
            logging.warning("No Text Detected.")
            return ''
        return self.response[response_name].get('text', '')

    def display_landmark(self):
        response_name = API_CONFIG.get(LANDMARK_DETECTION, [''])[0]
        if not self.response.get(response_name):
            logging.warning("No Landmark Detected.")
            return ''
        return self.response[response_name][0].get('description', '')

    def display_faces(self, debug=False):
        """
        Formats the response and parses the face detection features
        :return:
        """
        response_name = API_CONFIG.get(FACE_DETECTION, [''])[0]
        if not self.response.get(response_name):
            logging.warning("No Faces Detected.")
            return ''
        result = []
        faces = self.response[response_name]
        for face in faces:
            values = [
                (camel_to_title(key.replace('Likelihood', '')), LIKELIHOOD[value])
                for key, value in face.items()
                if isinstance(value, basestring) and LIKELIHOOD.get(value, 0) > THRESHOLD
            ]

            result.append(
                [x[0] for x in sorted(values, key=lambda x: x[1])]
                if values else []
            )
        print("Faces Found: %d" % len(faces))
        print("\n".join([", ".join(entry) if entry else "Empty" for entry in result]))

        if debug:
            print("")
            print("Example Fields:")
            print(faces[0].keys())


def camel_to_title(value):
    first = re.compile(r'(.)([A-Z][a-z]+)')
    second = re.compile('([a-z0-9])([A-Z])')

    subbed = first.sub(r'\1 \2', value)
    return second.sub(r'\1 \2', subbed).lower().title()
