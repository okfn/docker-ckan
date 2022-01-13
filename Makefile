include $(PWD)/.env

ifeq ($(ENV), dev)
all:
COMPOSE_FILE_PATH := docker-compose.dev.yml
else
all:
COMPOSE_FILE_PATH := docker-compose.yml
endif

build.all:
	docker-compose -f $(COMPOSE_FILE_PATH) build --no-cache

build.ckan:
	docker-compose -f $(COMPOSE_FILE_PATH) build ckan --no-cache

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
