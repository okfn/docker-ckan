#!/bin/bash

echo "***** Set up Postgres POSTGIS"

paster --plugin=ckanext-spatial spatial initdb -c "$CKAN_INI"

psql -d template_postgis -c "UPDATE pg_database SET datistemplate=true WHERE datname='template_postgis';"
psql -d template_postgis -c "CREATE EXTENSION postgis;"
