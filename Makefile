include $(PWD)/.env

ifeq ($(ENVIRONMENT), dev)
	COMPOSE_FILE_PATH := 
else ifeq ($(ENVIRONMENT), staging)
	COMPOSE_FILE_PATH := -f docker-compose.yml -f docker-compose.staging.yml
else # Production
	COMPOSE_FILE_PATH := -f docker-compose.yml
endif

build.all:
	docker-compose $(COMPOSE_FILE_PATH) build --no-cache

build.ckan:
	docker-compose $(COMPOSE_FILE_PATH) build --no-cache ckan

rebuild.ckan:
	docker-compose $(COMPOSE_FILE_PATH) up -d --no-deps --build ckan

restart.ckan:
	docker-compose $(COMPOSE_FILE_PATH) up -d --no-deps --force-recreate ckan

replace.ckan:
	./update_ckan_container.sh

scaleup.ckan:
	docker-compose $(COMPOSE_FILE_PATH) up -d --no-deps --scale ckan=2 --no-recreate ckan

scaledown.ckan:
	docker-compose $(COMPOSE_FILE_PATH) up -d --no-deps --scale ckan=1 --no-recreate ckan

start: up logs

up:
	docker-compose $(COMPOSE_FILE_PATH) up -d

down:
	docker-compose $(COMPOSE_FILE_PATH) down

logs:
	docker-compose $(COMPOSE_FILE_PATH) logs -f

ps: 
	docker-compose $(COMPOSE_FILE_PATH) ps
	
reload.caddy:
	docker-compose ${COMPOSE_FILE_PATH} exec -w /etc/caddy caddy caddy reload

harvest.gather:
	docker-compose $(COMPOSE_FILE_PATH) exec ckan /bin/bash -c "ckan harvester gather_consumer"

harvest.fetch:
	docker-compose $(COMPOSE_FILE_PATH) exec ckan /bin/bash -c "ckan harvester fetch_consumer"

harvest.run:
	docker-compose $(COMPOSE_FILE_PATH) exec ckan /bin/bash -c "ckan harvester run"

xloader.submit:
	docker-compose $(COMPOSE_FILE_PATH) exec ckan /bin/bash -c "ckan xloader submit all"

# WIP currently having issues running this locally
test.plugins:
	docker-compose $(COMPOSE_FILE_PATH) exec -w "/srv/app/src_extensions/ckanext-subakdc-plugins" ckan /bin/bash -c "pip install pytest-ckan requests_mock && pytest --ckan-ini=test.ini"
