#!/bin/bash

# Scale CKAN to 2 containers
make scaleup.ckan

# Wait 60s for new container to start
echo "Waiting 60s for new CKAN container to start"
sleep 60

# Stop old CKAN container
echo "Stopping old CKAN container"
docker stop $(docker ps --filter "name=ckan" -q | tail -1)

# Scale back down to 1 container
make scaledown.ckan

echo "New CKAN container now running"