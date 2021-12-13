#!/bin/bash

# Start CKAN running in dev mode and associated services

# Start SOLR and tomcat
sudo service tomcat9 start

# Start CKAN helper processes running under supervisorctl
sudo supervisorctl start ckan-datapusher:ckan-datapusher-00
sudo supervisorctl start ckan-worker:ckan-worker-00

# Not this one because we want to run with CKAN command rather than full webserver
# sudo supervisorctl start ckan-uwsgi:ckan-uwsgi-00

# activate virtual environment
. /usr/lib/ckan/default/bin/activate
# Start CKAN webserver
sudo ckan -c /etc/ckan/default/ckan.ini run