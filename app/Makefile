#
# HELP
#
# Outputs the help for each task

.PHONY: help

help: ## This help message
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

VENV = venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip

build: requirements.txt
	pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

run: $(VENV)/bin/activate
	gunicorn -k eventlet -w1 --timeout 6000 server:app

$(VENV)/bin/activate: requirements.txt
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt

clean:
	rm -rf __pycache__
	rm -rf $(VENV)
 