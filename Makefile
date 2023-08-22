COLOR_INFO    = \033[0;36m
COLOR_RESET   = \033[0m

# -- Docker
DOCKER_UID           = $(shell id -u)
DOCKER_GID           = $(shell id -g)

COMPOSE              = DOCKER_USER="$(DOCKER_UID):$(DOCKER_GID)" docker compose
COMPOSE_BUILD        = $(COMPOSE) build
COMPOSE_RUN          = $(COMPOSE) run --rm
COMPOSE_RUN_APP      = $(COMPOSE_RUN) app-dev
WAIT_DB              = $(COMPOSE_RUN) dockerize -wait tcp://db:3306 -timeout 60s

VERSION_FILE = src/backend/core/version.json

# -- Django
MANAGE = $(COMPOSE_RUN_APP) python manage.py

NEXT_TAG := $(shell git tag --sort version:refname | grep release | tail -1 | awk -F\. 'BEGIN {OFS="."} {print $$1,$$2,$$3+1}')
LAST_COMMIT := $(shell git log --format="%h" -n 1)

UNTRACKED := $(shell git status --untracked-files=no --porcelain)

# -- Rules
default: help

bootstrap: \
  stop \
  build-dev \
  run \
  migrate \
  init
bootstrap:  ## install development dependencies
.PHONY: bootstrap

# == Docker
build: ## build all containers
	$(COMPOSE_BUILD) app
	$(COMPOSE_BUILD) nginx
.PHONY: build

deploy: ## deploy app
	$(eval DATE := $(shell date +%Y%m%d%H%M%S))
	$(eval PWD := $(shell pwd))
	rm -Rf $(PWD)/data-new/*
	docker run -v $(PWD)/data-new:/opt/tmp --rm --entrypoint cp swissmooc-extras-nginx:production -r /data /opt/tmp/
	rm -Rf data-new/data/static/swissmooc-extras-staging
	mv data-new/data/static data-new/data/static-$(DATE)
	tar -C data-new/data -czf static-$(DATE).tgz static-$(DATE)
	scp -r static-$(DATE).tgz ubuntu@zh-staging-matomo:/data/
	ssh ubuntu@zh-staging-matomo tar -C /data -xzf /data/static-$(DATE).tgz
	ssh ubuntu@zh-staging-matomo git -C /data/swissmooc-extras-app pull
	ssh ubuntu@zh-staging-matomo unlink /data/static
	ssh ubuntu@zh-staging-matomo ln -s /data/static-$(DATE) /data/static
	ssh ubuntu@zh-staging-matomo sudo systemctl restart swissmooc-extras.service
	ssh ubuntu@zh-staging-matomo sudo systemctl restart nginx.service
.PHONY: deploy

build-dev: ## build all containers
	$(COMPOSE_BUILD) app-dev
.PHONY: build-dev

run-dev: ## start development environment
	@$(COMPOSE) up -d app-dev
	@$(WAIT_DB)
	@echo
	@echo "Open http://localhost:8000"
.PHONY: run-dev

stop: ## stop the development server
	@$(COMPOSE) stop
.PHONY: stop

# == Django
migrate: ## perform database migrations
	@$(COMPOSE) up -d db
	@$(WAIT_DB)
	@$(MANAGE) makemigrations swissmooc-extras
	@$(MANAGE) migrate
.PHONY: migrate

superuser: ## create a DjangoCMS superuser
	@$(COMPOSE) up -d db
	@$(WAIT_DB)
	@$(MANAGE) createsuperuser
.PHONY: superuser


test: ## perform tests
	@$(COMPOSE) up -d db
	@$(WAIT_DB)
	@$(MANAGE) test apps.aswissmooc-extras.tests --settings=core.settings-test --noinput --pattern="*_tests.py"
.PHONY: test

ensure-repo-is-clean:
	@if [ -n "$(UNTRACKED)" ]; then echo ERROR: please ensure git repository is clean; exit 1; fi
.PHONY: ensure-repo-is-clean

create-version-json-file:
	@echo '{"version":"$(shell echo $(NEXT_TAG) | cut -d- -f2)","commit":"$(LAST_COMMIT)"}' > $(VERSION_FILE)
	@git add $(VERSION_FILE)
	@git commit -m "[auto] bump site version to $(NEXT_TAG)" $(VERSION_FILE)
	@git push origin master
.PHONY: create-version-json-file

tag:
	@git tag $(NEXT_TAG)
	@echo tag image epflcede/swissmooc-extras-app:$(NEXT_TAG) and epflcede/swissmooc-extras-nginx:$(NEXT_TAG)
	@docker image tag swissmooc-extras-app:production epflcede/swissmooc-extras-app:$(NEXT_TAG)
	@docker image tag swissmooc-extras-nginx:production epflcede/swissmooc-extras-nginx:$(NEXT_TAG)
.PHONY: tag

release: ## get latest tag for the site, increment minor version, tag Docker images, push them to Docker Hub
release: \
	ensure-repo-is-clean \
	create-version-json-file \
	build \
	tag
.PHONY: release

help:
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
.PHONY: help
