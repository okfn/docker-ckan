include $(PWD)/.env

ifeq ($(ENVIRONMENT), dev)
	COMPOSE_FILE_PATH := docker-compose.dev.yml
else
	COMPOSE_FILE_PATH := docker-compose.yml
endif

build.all:
	docker-compose -f $(COMPOSE_FILE_PATH) build --no-cache

build.ckan:
	docker-compose -f $(COMPOSE_FILE_PATH) build --no-cache ckan

rebuild.ckan:
	docker-compose -f $(COMPOSE_FILE_PATH) up -d --no-deps --build ckan

restart.ckan:
	docker-compose -f $(COMPOSE_FILE_PATH) up -d --no-deps ckan

start: up logs

up:
	docker-compose -f $(COMPOSE_FILE_PATH) up -d

down:
	docker-compose -f $(COMPOSE_FILE_PATH) down

logs:
	docker-compose -f $(COMPOSE_FILE_PATH) logs -f

ps: 
	docker-compose -f $(COMPOSE_FILE_PATH) ps

harvest.gather:
	docker-compose -f $(COMPOSE_FILE_PATH) exec ckan /bin/bash -c "ckan harvester gather_consumer"

harvest.fetch:
	docker-compose -f $(COMPOSE_FILE_PATH) exec ckan /bin/bash -c "ckan harvester fetch_consumer"

harvest.run:
	docker-compose -f $(COMPOSE_FILE_PATH) exec ckan /bin/bash -c "ckan harvester run"

# WIP currently having issues running this locally
test.plugins:
	docker-compose -f $(COMPOSE_FILE_PATH) exec -it -w "/srv/app/src_extensions/ckanext-subakdc-plugins" ckan /bin/bash -c "pip install pytest-ckan requests_mock && pytest --ckan-ini=test.ini"
