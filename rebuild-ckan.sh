#!/bin/bash

(cd ckan-base && docker build -t alphagov/ckan-base:2.7 -f 2.7/Dockerfile .)
(cd ckan-dev && docker build -t alphagov/ckan-dev:2.7 -f 2.7/Dockerfile .)

docker-compose -f docker-compose.dev.yml build 
