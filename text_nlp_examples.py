# coding=utf-8
import os
from ml.gcp_clients.base_client import GCPClient
from ml.gcp_clients.image_client import ImageClient

# Setup
api_key = os.environ.get('GCP_API_KEY')
client = GCPClient(api_key)

# Image API
image = 'https://blogs.transparent.com/italian/files/2016/05/I-cani-vanno-tenuti-1.jpg'
text = client.text_from_image(image)
print(text)

# Translate API
text = client.translation_from_text(text)
print(text)

# NLP API
config = client.nlp_from_text(text)
print(config)

# Classify
classy_text = u"A Smoky Lobster Salad With a Tapa Twist. This spin on the Spanish pulpo a la gallega skips the " \
              u"octopus, but keeps the sea salt, olive oil, pimentón and boiled potatoes."

classification = client.get_classification(classy_text)
print(client.format_classification(classification))


# Image Class
image_client = ImageClient(api_key)
image_url = 'https://media.gettyimages.com/photos/large-crowd-of-people-cheering-and-raising-their-fists-picture-iddv1992030'
image_client.process_image(image_url, ['TEXT_DETECTION', 'LABEL_DETECTION', 'WEB_DETECTION', 'FACE_DETECTION', 'LANDMARK_DETECTION'], 10)
image_client.display_faces()
