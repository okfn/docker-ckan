This folder is used to install local extensions for development.
Clone here any extension that you want to work on. This folder in mounted on
the `ckan` service, so when `DEVELOPMENT_MODE=true` any extension located here
will be installed when booting up Docker Compose (`docker-compose up`).
If running the CKAN container standalone you will need to mount the folder
yourself.
