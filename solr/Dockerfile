FROM debian:buster-slim AS jts

RUN apt-get update && apt-get install -qq -y libjts-java

FROM solr:6.6-slim

MAINTAINER Open Knowledge International <info@okfn.org>

# Environment
ARG SOLR_CORE=ckan
ENV SOLR_HOME=/opt/solr/server/solr

USER root

# Install JTS Topology Suite
COPY --from=jts /usr/share/java/jts-core.jar /opt/solr/server/solr-webapp/webapp/WEB-INF/lib

WORKDIR $SOLR_HOME
# Create core and deafult config
RUN precreate-core $SOLR_CORE $SOLR_HOME/configsets/basic_configs && \
    rm $SOLR_CORE/conf/managed-schema && \
    mkdir $SOLR_CORE/data

# Add CKAN custom config
ADD solrconfig.xml \
    schema.xml \
    $SOLR_CORE/conf/
    
# Give ownership to Solr
RUN chown -R $SOLR_USER:$SOLR_USER $SOLR_CORE

USER solr:solr
