ARG BASE_IMG=europe-southwest1-docker.pkg.dev/oki-cloud/docker-ckan-images
FROM ${BASE_IMG}/openknowledge/ckan-base:2.8

MAINTAINER Open Knowledge Foundation <info@okfn.org>

ENV APP_DIR=/srv/app
ENV SRC_EXTENSIONS_DIR=/srv/app/src_extensions

# Install packages needed by the dev requirements
RUN apk add --no-cache libffi-dev

# Install CKAN dev requirements

ADD https://raw.githubusercontent.com/ckan/ckan/${GIT_BRANCH}/dev-requirements.txt /tmp/dev-requirements.txt
RUN sed -i '/coveralls/d' /tmp/dev-requirements.txt && pip install --no-binary :all: -r /tmp/dev-requirements.txt

# Create folder for local extensions sources
RUN mkdir $SRC_EXTENSIONS_DIR

COPY 2.8/setup/start_ckan_development.sh ${APP_DIR}


CMD ["/srv/app/start_ckan_development.sh"]
