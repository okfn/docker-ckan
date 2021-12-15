#!/bin/bash

# Push Subak Data Catalogue images to AWS container registry for use with ECS

# Retrieve an authentication token and authenticate your Docker client to your registry
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 848094190915.dkr.ecr.us-east-1.amazonaws.com

# Build images
# docker-compose -f docker-compose.yml build

# Tag images
docker tag docker-ckan_ckan:latest 848094190915.dkr.ecr.us-east-1.amazonaws.com/ckan:latest
docker tag docker-ckan_solr:latest 848094190915.dkr.ecr.us-east-1.amazonaws.com/solr:latest
docker tag docker-ckan_db:latest 848094190915.dkr.ecr.us-east-1.amazonaws.com/db:latest
docker tag docker-ckan_datapusher:latest 848094190915.dkr.ecr.us-east-1.amazonaws.com/datapusher:latest

# Push images
docker push 848094190915.dkr.ecr.us-east-1.amazonaws.com/ckan:latest
docker push 848094190915.dkr.ecr.us-east-1.amazonaws.com/solr:latest
docker push 848094190915.dkr.ecr.us-east-1.amazonaws.com/db:latest
docker push 848094190915.dkr.ecr.us-east-1.amazonaws.com/datapusher:latest