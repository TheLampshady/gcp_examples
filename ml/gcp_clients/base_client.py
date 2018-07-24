import json
import logging
import requests

from six import string_types

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

    def get(self, url=None):
        r = requests.get(url or self.endpoint, headers=self.headers, params=self.params)

        if r.status_code != 200:
            logging.warning("Request Error Code: %s" % r.status_code)
            message = r.json().get('error', {}).get('message', '')
            logging.warning("Request Error Message: %s" % message)
            return dict()

        return r.json()

    @staticmethod
    def get_image_payload(image_url, features=TEXT_DETECTION, max_results=10):
        if isinstance(features, string_types):
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
        """
        Parses a response from annotate image endpoint and returns the text
        :param result: dict
        :return: str
        """
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

    def display_nlp_tokens(self, tokens):
        for token in tokens[:]:
            entry = self.format_entry(token)
            word = entry.pop('word')
            print("%s: %s" % (word, json.dumps(entry['properties'], indent=4)))

    @staticmethod
    def format_entry(token):
        pos_data = token.get('partOfSpeech', {})
        properties = {
            key: value
            for key, value in list(pos_data.items())
            if "UNKNOWN" not in value.upper()
        }
        properties['lemma'] = token.get('lemma', '')
        word = token.get('text', {}).get('content', '')
        return dict(
            word=word,
            properties=properties
        )

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

    def nlp_from_text(self, text, display=True, debug=False):
        """
        Returns a list of tokens with properties of speech
        :param display: Prints user friendly content
        :param text: Text to analyze
        :return: list of dicts
        """
        payload = self.get_doc_payload(text)
        result = self.post(payload, self.NLP_SYNTAX_ENDPOINT)
        tokens = result.get('tokens', [])
        if display:
            self.display_nlp_tokens(tokens)
            if debug:
                print("")
                print("NLP Fields:")
                print(tokens[0].get(u'partOfSpeech',{}).keys())
            print("")

        return tokens

    def english_from_image(self, image, locale=ENGLISH):
        text = self.text_from_image(image)
        return self.translation_from_text(text, locale)
