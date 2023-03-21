ARG BASE_IMG=europe-southwest1-docker.pkg.dev/oki-cloud/docker-ckan-images
FROM ${BASE_IMG}/openknowledge/ckan-base:2.9

MAINTAINER Open Knowledge Foundation <info@okfn.org>

ENV APP_DIR=/srv/app
ENV SRC_EXTENSIONS_DIR=/srv/app/src_extensions

# Install packages needed by the dev requirements
RUN apk add --no-cache libffi-dev

# Install CKAN dev requirements
RUN pip3 install -r https://raw.githubusercontent.com/ckan/ckan/${GIT_BRANCH}/dev-requirements.txt

# Create folder for local extensions sources
RUN mkdir $SRC_EXTENSIONS_DIR

COPY 2.9/setup/start_ckan_development.sh ${APP_DIR}


CMD ["/srv/app/start_ckan_development.sh"]
