FROM alpine:3.7

RUN apk add --no-cache --virtual .build-deps \
    gcc \
    make \
    g++ \
    autoconf \
    automake

# install geos 3.8.0 as geos 3.7.2-r1 in alpine repository does not install correctly
RUN wget http://download.osgeo.org/geos/geos-3.8.0.tar.bz2
RUN tar xf geos-3.8.0.tar.bz2
RUN (cd geos-3.8.0 && ./configure && make && make install)
