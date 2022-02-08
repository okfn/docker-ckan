#!/bin/bash

# Scale CKAN to 2 containers
make scaleup.ckan

i=1
while [ $i -le 5 ];
do  
    echo "Waiting 60s for new CKAN container to start"
    sleep 60

    # Check if new container is ready
    status=$(docker ps --filter "name=ckan" -q --latest --format "{{.Status}}")
    if [[ $status =~ "healthy" ]]; then
        echo "New CKAN container is ready"
        
        # Stop old CKAN container
        echo "Stopping old CKAN container"
        docker stop $(docker ps --filter "name=ckan" -q | tail -1)

        # Scale back down to 1 container
        make scaledown.ckan
        echo "New CKAN container now running"
        break
    fi

    # If new container is not ready after 5 mins, stop it and scale back down
    if [ $i -eq 5 ]; then
        echo "Giving up..."
        docker stop $(docker ps --filter "name=ckan" -q --latest)
        make scaledown.ckan
        break
    fi
    
    echo "New container not ready, trying again..."
    ((i++))
done