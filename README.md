# Docker Compose setup for CKAN

**Note**: :warning: This is a work in progress. There is likely to be issues so use with caution :warning:


This is a set of Docker images and configuration files to run a CKAN site

It is largely based on two existing projects:

* Keitaro's [CKAN Docker images](https://github.com/keitaroinc/docker-ckan)
* Docker Compose setup currently included in [CKAN core](https://github.com/ckan/ckan)


It includes the following images, all based on [Alpine Linux](https://alpinelinux.org/):

* CKAN: modified from keitaro/ckan
* DataPusher: modified from keitaro/datapusher
* PostgresSQL: mdillon's PostGIS image
* Solr: official Solr image with CKAN's schema
* Redis: standard Redis image

The site is configured via env vars (the CKAN image loads [ckanext-envvars](https://github.com/okfn/ckanext-envvars)), that you can set in the `.env` file.

To build the images:

	docker-compose build

To start the containers:

	docker-compose up
