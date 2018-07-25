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



## Speech to Text
Enable API
```
https://console.developers.google.com/apis/api/speech.googleapis.com/overview
```

Encoding
Mac:
```
base64 source_audio_file > dest_audio_file
```
Win
```
Base64.exe -e source_audio_file > dest_audio_file
```

**Audio Converter**

https://www.ffmpeg.org/

```bash
npm i --save linear16
```

**Discovery API**

https://cloud.google.com/speech-to-text/docs/basics



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
