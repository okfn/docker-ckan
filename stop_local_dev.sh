#!/bin/bash

# Stop CKAN running in dev mode and associated services

# Stop SOLR and tomcat
sudo service tomcat9 stop

# Start CKAN helper processes running under supervisorctl
sudo supervisorctl stop ckan-datapusher:ckan-datapusher-00
sudo supervisorctl stop ckan-worker:ckan-worker-00
sudo supervisorctl stop ckan-uwsgi:ckan-uwsgi-00

# Not this one because we want to run with CKAN command rather than full webserver
# sudo supervisorctl start ckan-uwsgi:ckan-uwsgi-00
