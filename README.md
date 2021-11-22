# CKAN setup for Subak's Data Cooperative

Taking as a starting point the [CKAN-in-docker repository](https://github.com/okfn/docker-ckan) by the Open Knowledge Foundation, the original README and setup instructions can now be found in [SETUP.md](/SETUP.md).

## Developing locally
`cp .env.example .env`  
`docker-compose build`  
`docker-compose run`  

For staging and production:  
environment variables will be set in EKS.

## Adding plugins
Update the CKAN Dockerfile with the plugins desired and add to the CKAN_PLUGINS section in the `.env` file.
