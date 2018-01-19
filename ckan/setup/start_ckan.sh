#!/bin/bash
printenv
if [ "$DEVELOPMENT_MODE" = true ]
then
    echo "Starting CKAN in development mode"
    source start_ckan_development.sh
else
    echo "Starting CKAN in production mode"
    source start_ckan_production.sh
fi
