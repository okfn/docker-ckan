This folder is used to install local extensions for development.
Clone here any extension that you want to work on. This folder in mounted on
the `ckan-dev` service, so any extension located here will be installed when
booting up Docker Compose in development mode 
(`docker-compose -f docker-compose.dev.yml up`).
If running the CKAN container standalone you will need to mount the folder
yourself.

### Create an extension

You can use the paster template in much the same way as a source install, only executing the command inside the CKAN container and setting the mounted `src/` folder as output:

    docker-compose -f docker-compose.dev.yml exec ckan-dev /bin/bash -c "paster --plugin=ckan create -t ckanext ckanext-myext -o /srv/app/src_extensions"

The new extension will be created in the `src/` folder. You might need to change the owner of its folder to have the appropiate permissions.
