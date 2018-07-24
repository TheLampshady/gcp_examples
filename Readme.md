
# Requirements

## Google Cloud Account
Create a GCP project and initialize your GAE.

1. https://console.cloud.google.com/
1. https://console.cloud.google.com/appengine

## Python
**Check your python version**. If you do no have python, https://www.python.org/downloads/release/python-2715/
```bash
python --version
```

**Create a virtual env**
```bash
pip install virtualenv
virtualenv venv
. venv/bin/activate
```

## Setup gcloud
1. Create a project at: `https://console.cloud.google.com/`
2. Create a Python project at: `https://console.cloud.google.com/appengine/versions`
3. Take note of the project id form the url (Not the User friendly name)

## Google Cloud SDK
Check to see if you have gcloud set up. If you do no have gcloud, install and reopen term
```bash
gcloud --version
```

https://cloud.google.com/sdk/docs/quickstart-macos


See if you have an account.
```bash
gcloud auth list
```

If not, lets login.

```bash
gcloud auth login
```


# Google App Engine
[Tutorial: GAE Multi-Service with Endpoints](gae/Readme.md)

# Google Machine Learning
[Tutorial: Image/Translations/NLP](ml/Readme.md)

# Datalabs
Starting up a GCP Web console with data labs

## Enable API:
Requires cloud source API 

https://console.developers.google.com/apis/api/sourcerepo.googleapis.com/overview?project=<PROJECT_ID>

## Commands
datalab create <my-name>
-  I like option 2 (us-east1-c)
- 'Y' for SSH keys
- Password is up to you (takes 5 min)

## Running
- datalab run <my-name>
- Using the web preview, change the port to the port shown (8081)

