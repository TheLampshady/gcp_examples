# Google Cloud Storage

# GCS Bucket Lib

https://google-cloud-python.readthedocs.io/en/latest/storage/buckets.html

## Static Website
This tutorial will walk through how to setup a static website on 
Google Cloud Storage with a homepage, SSL custom domain name


**Ref:** https://cloud.google.com/storage/docs/hosting-static-website

### Domain Verification
Before creating a bucket with a domain name, it must be verified.

**Webmaster:** https://www.google.com/webmasters/tools/home?hl=en

**Ref**: https://cloud.google.com/storage/docs/domain-name-verification#verification

### Uploading content
Refer to the upload site code or add files manually.

### Website Config
This allows the website to have a homepage and 404 page. 
This option is only buckets with domain names.

A bucket created with a domain name will have `Edit Website Configuration` available. 

The GCS Python lib also has `website_config` function to manage the congif

MainPageSuffix - Set homepage
NotFoundPage - Sets 404 page

**Ref:** https://cloud.google.com/storage/docs/hosting-static-website#specialty-pages

### Preview website
By default, any site set to public will have the following URLS available for viewing.

* https://storage.googleapis.com/sample-site-dev/sample-site/index.html
* https://sample-site-dev.storage.googleapis.com/sample-site/index.html

### CORS
https://cloud.google.com/storage/docs/configuring-cors

### HTTPS / SSL
Currently GCS Websites do not support HTTPS / SSL. 
To secure the site, a load balancer will need to be set up.

There are 4 steps to creating a load balancer
1) Create Load Balancer
1) Setup Backend Bucket (Serve Content)
1) Choose Routing Rules (Default is all bucket content)
1) Setup Front-End ()

**Create Load Balancer**

Head to GCP Network Service (Load Balancer) and create a load balancer

https://console.cloud.google.com/net-services/loadbalancing/loadBalancers/list

**Note:** Even though the custom domain name will be pointing to the load balancer, 
GCS requires a DNS record to create website buckets to set the website configs.

#### Backend
Create a new backend bucket and have it point to your bucket created above. 
Select `Enable Cloud CDN`

The backend bucket can be named anything. It is another layer ontop of your GCS bucket

#### Host and Path Rules

Select the backend bucket and leave the rules as is (default).

#### Frontend

A certificate will be needed to complete this step

* Selected HTTPS
* Create an IP
* Select the certificate

Save and continue

### SSL Certificates
TODO

**Ref:** https://cloud.google.com/compute/docs/load-balancing/http/ssl-certificates

### DNS

Create an A record pointing to the IP address created by the Load balancer
