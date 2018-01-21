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

You can boot it without changing anything and you'll get a working CKAN instance. There is a sysadmin user created by default with the values defined in `CKAN_SYSADMIN_NAME` and `CKAN_SYSADMIN_PASSWORD`(`ckan_admin` and `test` by default). I shouldn't be telling you this but obviously don't run any public CKAN instance with the default settings.

To build the images:

	docker-compose build

To start the containers:

	docker-compose up

## Development mode

To develop local extensions set `DEVELOPMENT_MODE=true`. This means:

* Any extension cloned on the `src` folder will be installed in the CKAN container when booting up Docker Compose (`docker-compose up`). This includes installing any requirements listed in a `requirements.txt` (or `pip-requirements.txt`) file and running `python setup.py develop`
* CKAN will be started running on the paster development server, with the `--reload` option to watch changes in the extension files.
* Make sure to add the local plugins to the `CKAN__PLUGINS` env var in the `.env` file.

When running in production mode (`DEVELOPMENT_MODE=false`):

* Only extensions included in the CKAN image (eg in `ckan/Dockerfile`) will be included
* CKAN will be started running on uWSGI.
