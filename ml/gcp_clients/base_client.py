import json
import logging
import requests

WEB_IMAGE = 'imageUri'
GCS_IMAGE = 'gcsImageUri'
MAX_RESULTS = 'maxResults'
ENGLISH = 'en'

TEXT_DETECTION = 'TEXT_DETECTION'
LABEL_DETECTION = "LABEL_DETECTION"
WEB_DETECTION = "WEB_DETECTION"
FACE_DETECTION = "FACE_DETECTION"
LANDMARK_DETECTION = "LANDMARK_DETECTION"


class GCPClient(object):
    ENDPOINT = None
    IMAGE_ENDPOINT = 'https://vision.googleapis.com/v1/images:annotate'
    TRANSLATE_ENDPOINT = 'https://translation.googleapis.com/language/translate/v2'
    NLP_ENTITIES_ENDPOINT = 'https://language.googleapis.com/v1/documents:analyzeEntities'
    NLP_SYNTAX_ENDPOINT = 'https://language.googleapis.com/v1/documents:analyzeSyntax'
    CLASSIFY_ENDPOINT = 'https://language.googleapis.com/v1/documents:classifyText'

    def __init__(self, api_key):
        self.headers = {'Content-Type': 'application/json'}
        self.params = {'key': api_key}
        self.endpoint = None

    def post(self, payload, url=None):
        data = json.dumps(payload)
        r = requests.post(url or self.endpoint, headers=self.headers, data=data, params=self.params)

        if r.status_code != 200:
            logging.warning("Request Error Code: %s" % r.status_code)
            message = r.json().get('error', {}).get('message', '')
            logging.warning("Request Error Message: %s" % message)
            return dict()

        return r.json()

    @staticmethod
    def get_image_payload(image_url, features=TEXT_DETECTION, max_results=10):
        if isinstance(features, basestring):
            features = [features]

        image = {
            "source": {WEB_IMAGE: image_url}
        }

        features_props = [
            {"type": feature, MAX_RESULTS: max_results}
            for feature in features
        ]

        return {
            "requests": [
                {"image": image, "features": features_props}
            ]
        }

    @staticmethod
    def text_from_response(result):
        if not result.get('responses'):
            logging.warning("No text response found.")
            return ''
        response = result['responses'][0]
        return response.get('fullTextAnnotation', {}).get('text', '')

    @staticmethod
    def get_translate_payload(text, language="en"):
        return {
            "q": text,
            "target": language
        }

    @staticmethod
    def translation_from_response(result):
        translations = result.get('data', {}).get('translations')
        if not translations:
            logging.warning("No translations found.")
            return ''
        logging.info("Text Source: %s" % translations[0].get('detectedSourceLanguage', ''))
        return translations[0].get('translatedText', '')

    @staticmethod
    def get_doc_payload(text, doc_type="PLAIN_TEXT"):
        # PLAIN_TEXT or HTML
        return {
            "document": {
                "type": doc_type,
                "content": text
            },
            "encodingType": "UTF8"
        }

    @staticmethod
    def nlp_from_response(result):
        if not result.get('tokens'):
            logging.warning("No tokens found.")
            return list()
        return result['tokens']

    @staticmethod
    def format_nlp(result, index=0):
        token = result['tokens'][index] \
            if len(result.get('tokens', [])) > index \
            else dict()
        print("Original Text: %s" % token.get('text', {}).get('content', ''))
        print("Lemma: %s" % token.get('lemma', ''))
        print(json.dumps(token.get('partOfSpeech', {}), indent=3))

    def get_classification(self, text, doc_type="PLAIN_TEXT"):
        payload = {
            "document": {"type": doc_type, "content": text}
        }
        result = self.post(payload, self.CLASSIFY_ENDPOINT)
        return result.get('categories') or []

    @staticmethod
    def format_classification(cats):
        return "\n".join([
            "%s (%s)" % (" -> ".join([x.strip() for x in cat["name"].split('/') if x]), cat.get('confidence'))
            for cat in cats if cat.get("name", '')
        ])

    # ------------------- User Friendly Output -------------------------------

    def text_from_image(self, image_url):
        payload = self.get_image_payload(image_url)
        result = self.post(payload, self.IMAGE_ENDPOINT)
        return self.text_from_response(result)

    def translation_from_text(self, text, locale=ENGLISH):
        payload = self.get_translate_payload(text, locale)
        result = self.post(payload, self.TRANSLATE_ENDPOINT)
        return self.translation_from_response(result)

    def nlp_from_text(self, text):
        payload = self.get_doc_payload(text)
        result = self.post(payload, self.NLP_SYNTAX_ENDPOINT)
        return self.format_nlp(result)

    def english_from_image(self, image, locale=ENGLISH):
        text = self.text_from_image(image)
        return self.translation_from_text(text, locale)
