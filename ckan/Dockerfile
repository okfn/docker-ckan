FROM openknowledge/ckan-base:2.9

LABEL maintainer="Laurence Watson <laurence@subak.org>"

# Set timezone
ARG TZ
RUN cp /usr/share/zoneinfo/$TZ /etc/localtime
RUN echo $TZ > /etc/timezone

# Install any extensions needed by your CKAN instance
# (Make sure to add the plugins to CKAN__PLUGINS in the .env file)
# For instance:
RUN pip install -e git+https://github.com/ckan/ckanext-pages.git#egg=ckanext-pages && \
    pip install -e git+https://github.com/ckan/ckanext-dcat.git@v1.1.3#egg=ckanext-dcat && \
    pip install -r https://raw.githubusercontent.com/ckan/ckanext-dcat/v1.1.3/requirements.txt && \
    pip install -e git+https://github.com/ckan/ckanext-harvest.git#egg=ckanext-harvest && \
    pip install -r https://raw.githubusercontent.com/ckan/ckanext-harvest/master/pip-requirements.txt && \
    pip install -e git+https://github.com/ckan/ckanext-xloader.git#egg=ckanext-xloader && \
    pip install -r https://raw.githubusercontent.com/ckan/ckanext-xloader/master/requirements.txt && \
    pip install -e git+https://github.com/ckan/ckanext-googleanalytics.git#egg=ckanext-googleanalytics && \
    pip install -r https://raw.githubusercontent.com/ckan/ckanext-googleanalytics/master/requirements.txt && \
    pip install -e git+https://github.com/climatesubak/ckanext-scheming.git#egg=ckanext-scheming && \
    pip install -e git+https://github.com/climatesubak/ckanext-report.git#egg=ckanext-report && \
    pip install -r https://raw.githubusercontent.com/climatesubak/ckanext-report/master/requirements.txt && \
    pip install -e git+https://github.com/climatesubak/ckanext-sentry.git#egg=ckanext-sentry && \
    pip install -r https://raw.githubusercontent.com/climatesubak/ckanext-sentry/master/requirements.txt

# subakdc plugins
COPY src/ckanext-subakdc ${SRC_DIR}/ckanext-subakdc-plugins
RUN pip install -r ${SRC_DIR}/ckanext-subakdc-plugins/requirements.txt

# subakdc theme
COPY src/ckanext-subakdc ${SRC_DIR}/ckanext-subakdc
RUN pip install -r ${SRC_DIR}/ckanext-subakdc/requirements.txt

# Apply any patches needed to CKAN core or any of the built extensions (not the
# runtime mounted ones)
# See https://github.com/okfn/docker-ckan#applying-patches
COPY ckan/patches ${APP_DIR}/patches

RUN for d in $APP_DIR/patches/*; do \
        if [ -d $d ]; then \
            for f in `ls $d/*.patch | sort -g`; do \
                cd $SRC_DIR/`basename "$d"` && echo "$0: Applying patch $f to $SRC_DIR/`basename $d`"; patch -p1 < "$f" ; \
            done ; \
        fi ; \
    done
