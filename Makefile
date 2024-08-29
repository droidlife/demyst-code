## ----------------------------------------------------------------------
## This is a help comment. The purpose of this Makefile is to demonstrate
## a simple help mechanism that uses comments defined alongside the rules
## they describe without the need of additional help files or echoing of
## descriptions. Help comments are displayed in the order defined within
## the Makefile.
## ----------------------------------------------------------------------

NAME ?= demyst
COVERAGE_THRESHOLD ?= 80
COMMIT_HASH ?= $(shell git rev-parse --verify HEAD)
ENVIRONMENT ?= local
BUILD_NUMBER ?= 1
FILE_SIZE_IN_MB ?= 1


help:
	@sed -ne 's/^\([^[:space:]]*\):.*##/\1:\t/p' $(MAKEFILE_LIST) | column -t -s $$'\t'
install: ## install pip requirements needed to run the server
	pip install -r requirements.txt
install-dev: ## install pip requirements for the local development
	pip install -r requirements.txt
	pip install -r requirements_dev.txt
format: ## format code using black
	black *.py src/*.py
lint: ## linting code using pylint
	pylint src
test: ## running pytest
	pytest -v -s
run-coverage-test: ## generate test coverage report
	coverage run --source=src --module pytest --verbose tests && coverage report
	coverage report --fail-under=$(COVERAGE_THRESHOLD)
build: ## build docker container for deployment
	@docker build -t $(NAME) --build-arg ENVIRONMENT=$(ENVIRONMENT) .
generate_and_mask_csv_file: ## running the job generate_and_mask_csv_file: Args FILE_SIZE_IN_MB={}
	python3 run.py -job generate_and_mask_csv_file -args file_size_in_mb=$(FILE_SIZE_IN_MB)