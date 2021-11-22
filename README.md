# CKAN setup for Subak's Data Cooperative

Taking as a starting point the [CKAN-in-docker repository](https://github.com/okfn/docker-ckan) by the Open Knowledge Foundation, the original README and setup instructions can now be found in [SETUP.md](/SETUP.md).

## Local / staging / prod
Local using docker-desktop (for example).   
Staging and prod on AWS Elastic Container Service (ECS) so we can use the same dockerfiles.
Deploy to staging: XXX  
Deploy to prod: XXX  

## Developing locally
`cp .env.example .env`  
`docker-compose build`  
`docker-compose run`  

For staging and production:  
environment variables will be set in EKS.

## Adding plugins
Update the CKAN Dockerfile with the plugins desired and add to the CKAN_PLUGINS section in the `.env` file. Extra config like db updates may need to be done in a docker entryfile or similar.

Rebuild any one container by specifying the service name: `docker-compose build ckan`  
Then `docker-compose up` to recreate again.

Extensions added:  pages, dcat, harvester, scheming (datasets for now)

## Sysadmin
Basic tasks have been done in the `prerun.py` file and other commands can be added to the `start_ckan.sh` entrypoint file under `ckan-base/2.9/setup/start_ckan.sh`  

### Executing CKAN commands
`docker-compose -f docker-compose.yml exec ckan /bin/bash -c "ckan <YOUR COMMAND>"`  



## Basic customisation
Make basic changes with the UI at "http://<my-ckan-url>/ckan-admin/config/"  
Site Title: Subak Data Catalog  
Style: Default  
Site Tag Line: Share the data, save the planet  
Site logo: https://images.squarespace-cdn.com/content/v1/5fbe3c75a5bc066edf9513f2/1606745984909-KHIUHFOBXP5NTTNVMG5B/SUBAK_LOGO.png  
 About:  
 Intro Text:  
 Custom CSS:  
 Homepage: Search, introductory area and stats  
 