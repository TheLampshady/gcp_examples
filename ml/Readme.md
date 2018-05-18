# Getting Started ML
`cd ml`

**Install Dependencies:**
```bash
pip install -r requirements.txt
```

Try installing for autocomplete and syntax highlighting: 
```bash
pip install ipython
```

## Find Resource
1. Take not of the API Key from the code. 
   1. If it is not active, you can create one on your own project
1. Search google for an image with foreign text. Save the URL

## Commands
Run `ipython` or `python`

### Setup
This bit of code will initialize you client for calls to ML API. 
Add API key to environment.
```python
import os
from cloud_client import GCPClient

api_key = os.environ.get('GCP_API_KEY')
client = GCPClient(api_key)
```
### Text From Image
Next, take the image url you found or use mine and be boring.
```python
image = 'https://blogs.transparent.com/italian/files/2016/05/I-cani-vanno-tenuti-1.jpg'
```

Create the payload and make the request. This will print out the text from the image.
```python
payload = client.get_image_payload(image)
result = client.post(client.IMAGE_ENDPOINT, payload)
text = client.text_from_response(result)
print(text)
```

### Translate Text
Keep the text from the previous section or add your own.
```python
text = ....
```

Create the payload and make the request. This will print out the translated text.
```python
payload = client.get_translate_payload(text)
result = client.post(client.TRANSLATE_ENDPOINT, payload)
text = client.translation_from_response(result)
print(text)
```

### Text NLP
Keep the text from the previous section or add your own.
```python
text = ....
```

Create the payload and make the request. This will print out properties of the text.
```python
payload = client.get_doc_payload(text)
result = client.post(client.NLP_SYNTAX_ENDPOINT, payload)
config = client.format_nlp(result)
print(config)
```

## Python GCP Lib Setup
### Google Cloud Client
Used for python libs installed with pip

`Application Default Credentials`_ provides an easy way to obtain
credentials to call Google APIs for server-to-server or local applications.
This function acquires credentials from the environment in the following
order:

1. If the environment variable ``GOOGLE_APPLICATION_CREDENTIALS`` is set
   to the path of a valid service account JSON private key file, then it is
   loaded and returned. The project ID returned is the project ID defined
   in the service account file if available (some older files do not
   contain project ID information).
2. If the `Google Cloud SDK`_ is installed and has application default
   credentials set they are loaded and returned.

   To enable application default credentials with the Cloud SDK run::

        gcloud auth application-default login

   If the Cloud SDK has an active project, the project ID is returned. The
   active project can be set using::

        gcloud config set project

3. If the application is running in the `App Engine standard environment`_
   then the credentials and project ID from the `App Identity Service`_
   are used.
4. If the application is running in `Compute Engine`_ or the
   `App Engine flexible environment`_ then the credentials and project ID
   are obtained from the `Metadata Service`_.
