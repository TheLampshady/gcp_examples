# Getting Started GAE
This project is GAE scaffold for webapp2 and Google endpoints. It contains two service, one for each 
which can be ran locally and deployed to GAE

**Install Dependencies:**
```bash
pip install -r apis/requirements.txt -t apis/lib
```

## Single Service
The first part will be a single web app with a single page. No special setup.

### Run the App Locally
```bash
dev_appserver.py core/app.yaml
```

Local Site: 
```bash
http://localhost:8080
```

Local GAE Admin:
```bash
http://localhost:8000
```


### Deploy the app
This will take your code and yaml configs and send them up to GAE
```bash
gcloud app deploy --project <my-project> core/app.yaml
```

Live Site:
```bash
https://<project-id>.appspot.com
```

## Multiple Services (API)
Lets add an API as a separate service

### Run the app locally
Google Endpoints has a web app for using your new api. This even connects to your localhost.
```bash
dev_appserver.py dispatch.yaml apis/api.yaml core/app.yaml --port 8080
```

Local Site:
```
http://localhost:8080/api/test/v1/get
```

Local Endpoint Tool:
```
https://apis-explorer.appspot.com/apis-explorer/?base=http://localhost:8080/api#p/
```


### Deploy the app
Now we will deploy an additional service and a config for routing. Take note of the dispatch.yaml file

Using the project id, deploy both services
Run: 
```bash
gcloud app deploy --project <my-project> core/app.yaml apis/api.yaml
```

Now deploy a dispatch for routing
Run: 
```bash
gcloud app deploy --project <my-project> dispatch.yaml
```

Endpoint: 

https://PROJECT-ID.appspot.com/api/test/v1/get

Tool: 
```
https://apis-explorer.appspot.com/apis-explorer/?base=https://[project-id].appspot.com/api#p/
```


# FAQ

**Why i get this?**

* `google.appengine.tools.devappserver2.wsgi_server.BindError: Unable to bind localhost:8080`
    * Another app is using that port. Select a new port.


* `fatal error: 'gmp.h' file not found`
    * Run: `env "CFLAGS=-I/usr/local/include -L/usr/local/lib" pip install pycrypto -t apis/lib`

* `something something datastore`
    * You are running two app engines. Find it and kill it or:
    * `ps aux | grep dev_appserver.py`
    * `kill -9 <id>`
