FROM alpine:3.12

# Internals, you probably don't need to change these
ENV APP_DIR=/srv/app
ENV SRC_DIR=/srv/app/src
ENV CKAN_INI=${APP_DIR}/production.ini
ENV PIP_SRC=${SRC_DIR}
ENV CKAN_STORAGE_PATH=/var/lib/ckan
ENV GIT_URL=https://github.com/ckan/ckan.git
# CKAN version to build
ENV GIT_BRANCH=ckan-2.8.12
# Customize these on the .env file if needed
ENV CKAN_SITE_URL=http://localhost:5000
ENV CKAN__PLUGINS image_view text_view recline_view datastore datapusher envvars

WORKDIR ${APP_DIR}

# Install necessary packages to run CKAN
RUN apk add --no-cache tzdata \
        git \
        gettext \
        postgresql-client \
        python2 \
        apache2-utils \
        libxml2 \
        libxslt \
        mailcap \
        musl-dev \
        libmagic \
        curl \
        patch \
        sudo && \
    # Packages to build CKAN requirements and plugins
    apk add --no-cache --virtual .build-deps \
        postgresql-dev \
        gcc \
        make \
        g++ \
        autoconf \
        automake \
	libtool \
        python2-dev \
        libxml2-dev \
        libxslt-dev \
        linux-headers && \
    # Create SRC_DIR
    mkdir -p ${SRC_DIR} && \
    # Install pip, supervisord and uwsgi
    curl -o ${SRC_DIR}/get-pip.py https://bootstrap.pypa.io/pip/2.7/get-pip.py && \
    python ${SRC_DIR}/get-pip.py 'pip==20.3.3' && \
    pip install supervisor uwsgi && \
    mkdir /etc/supervisord.d && \
    #pip wheel --wheel-dir=/wheels uwsgi gevent && \
    rm -rf ${SRC_DIR}/get-pip.py

COPY common/supervisord.conf /etc

# Install CKAN
RUN pip install -e git+${GIT_URL}@${GIT_BRANCH}#egg=ckan && \
    cd ${SRC_DIR}/ckan && \
    cp who.ini ${APP_DIR} && \
    pip install --no-binary :all: -r requirements.txt && \
    # Install CKAN envvars to support loading config from environment variables
    pip install -e git+https://github.com/okfn/ckanext-envvars.git#egg=ckanext-envvars && \
    # Create and update CKAN config
    paster --plugin=ckan make-config ckan ${CKAN_INI} && \
    paster --plugin=ckan config-tool ${CKAN_INI} "beaker.session.secret = " && \
    paster --plugin=ckan config-tool ${CKAN_INI} "ckan.plugins = ${CKAN__PLUGINS}" && \
    paster --plugin=ckan config-tool ${CKAN_INI} "ckan.site_url = ${CKAN__SITE_URL}"

# Create a local user and group to run the app
RUN addgroup -g 92 -S ckan && \
    adduser -u 92 -h /srv/app -H -D -S -G ckan ckan

# Create local storage folder
RUN mkdir -p $CKAN_STORAGE_PATH && \
    chown -R ckan:ckan $CKAN_STORAGE_PATH

COPY 2.8/setup ${APP_DIR}
COPY 2.8/setup/supervisor.worker.conf /etc/supervisord.d/worker.conf
COPY 2.8/setup/start_ckan.sh ${APP_DIR}

# Create entrypoint directory for children image scripts
ONBUILD RUN mkdir /docker-entrypoint.d

RUN chown ckan -R /srv/app

EXPOSE 5000

HEALTHCHECK --interval=60s --timeout=5s --retries=5 CMD curl --fail http://localhost:5000/api/3/action/status_show || exit 1

CMD ["/srv/app/start_ckan.sh"]
