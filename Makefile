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
	
# WIP currently having issues running this locally
test.plugins:
	docker-compose -f $(COMPOSE_FILE_PATH) exec -w "/srv/app/src_extensions/ckanext-subakdc-plugins" ckan /bin/bash -c "pip install pytest-ckan requests_mock && pytest --ckan-ini=test.ini"

reload.caddy:
	docker-compose -f ${COMPOSE_FILE_PATH} exec -w /etc/caddy caddy caddy reload