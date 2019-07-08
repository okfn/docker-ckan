#!/bin/bash

echo "***** Set up Harvest"

paster --plugin=ckanext-harvest harvester initdb -c "$CKAN_INI"
