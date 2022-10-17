#
# HELP
#
# Outputs the help for each task

.PHONY: help

help: ## This help message
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

build: ## Build the containers
	docker-compose --env-file .env build

run: ## Run the containers
	docker-compose --env-file .env up

stop: ## Stop the running containers
	docker-compose stop
