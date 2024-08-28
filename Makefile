## ----------------------------------------------------------------------
## This is a help comment. The purpose of this Makefile is to demonstrate
## a simple help mechanism that uses comments defined alongside the rules
## they describe without the need of additional help files or echoing of
## descriptions. Help comments are displayed in the order defined within
## the Makefile.
## ----------------------------------------------------------------------

NAME ?= flask-app
WORKERS ?= 2
PORT ?= 5000
COVERAGE_THRESHOLD ?= 80
COMMIT_HASH ?= $(shell git rev-parse --verify HEAD)
SECRET_API_KEY ?= my-secret-api-key
FLASK_ENV ?= local
SQLALCHEMY_DATABASE_URI ?= sqlite:///app.db
BUILD_NUMBER ?= 1


help:
	@sed -ne 's/^\([^[:space:]]*\):.*##/\1:\t/p' $(MAKEFILE_LIST) | column -t -s $$'\t'
install: ## install pip requirements needed to run the server
	pip install -r requirements.txt
install-dev: ## install pip requirements for the local development
	pip install -r requirements.txt
	pip install -r requirements_dev.txt
format: ## format code using black
	black *.py app/*.py
lint: ## linting code using pylint
	pylint app
test: ## running pytest
	pytest -v -s
run-coverage-test: ## generate test coverage report
	coverage run --source=app --module pytest --verbose tests && coverage report
	coverage report --fail-under=$(COVERAGE_THRESHOLD)
build: ## build docker container for deployment
	@docker build -t $(NAME) --build-arg FLASK_ENV=$(FLASK_ENV) --build-arg SQLALCHEMY_DATABASE_URI=$(SQLALCHEMY_DATABASE_URI) \
	--build-arg SECRET_API_KEY=$(SECRET_API_KEY) --build-arg COMMIT_SHA=$(COMMIT_HASH) \
	--build-arg BUILD_NUMBER=$(BUILD_NUMBER) .
run: ## running production grade gunicorn server. Args: PORT={},WORKERS={}. Default: PORT=5000,WORKERS=2
	gunicorn -b 0.0.0.0:$(PORT) -w $(WORKERS) 'run:app'
dev-run: ## Run flask development server on port. Args: PORT={}. Default: PORT=5000
	python3 run.py -p $(PORT)