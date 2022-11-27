#
# HELP
#
# Outputs the help for each task

VENV = venv
PIP = $(VENV)/bin/pip
GUNICORN = $(VENV)/bin/gunicorn

.PHONY: help

help: ## This help message
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

build: ## Activate a virtual environment and install application dependencies
	if [ -n ${CLEAN_VENV} ] && [ ${CLEAN_VENV} = "true" ] && [ -d "$(VENV)" ]; then rm -rf $(VENV); fi
	@python3 -m venv $(VENV)
	@$(PIP) install --upgrade pip
	@$(PIP) install wheel
	$(PIP) install -r requirements.txt

run: ## Run the Pyldes
	@. $(VENV)/bin/activate
	@$(GUNICORN) -k eventlet -w 1 --bind 0.0.0.0:5000 --timeout 6000 server:app

clean: ## Clean local build environment
	rm -rf __pycache__
	rm -rf $(VENV)
