# Deploy automation for the personal portfolio.
#
# Manual trigger, automated process: `make deploy` runs the tests, builds the
# image locally, streams it to the droplet (gzipped, no temp tarball), syncs the
# compose/nginx config and restarts the stack.
#
# SSH_HOST has no default and is required for every remote target, e.g.:
#   make deploy SSH_HOST=user@host
#   make logs SSH_HOST=user@host TAG=v0.7.0

SSH_HOST   ?=
REMOTE_DIR ?= ~/personal-portfolio
IMAGE      ?= personal-portfolio-web
TAG        ?= $(shell git rev-parse --short HEAD)
NGINX_MODE ?= proxy

# Fail fast and propagate errors through pipes (docker save | gzip | ssh ...).
SHELL       := bash
.SHELLFLAGS := -e -o pipefail -c

.DEFAULT_GOAL := help
.PHONY: help test build deploy sync-config restart logs ps ssh prune prune-local pull-prod-data regenerate-images require-host

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*?## "} {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

require-host:
	@test -n "$(SSH_HOST)" || { echo "Error: SSH_HOST is required for remote targets, e.g. make $(MAKECMDGOALS) SSH_HOST=user@host"; exit 1; }

test: ## Run the Django test suite
	cd src && uv run python manage.py test

build: ## Build the production image locally (tagged with the git short SHA)
	docker build -t $(IMAGE):$(TAG) -t $(IMAGE):latest .

prune-local: ## Free disk locally: drop old app image tags (keeps :latest) and dangling layers
	docker images $(IMAGE) --format "{{.Tag}}" | { grep -vxE "latest|<none>" || true; } | xargs -r -I{} docker rmi $(IMAGE):{}
	docker image prune -f

sync-config: require-host ## Push the compose file and nginx configs to the server (never touches secrets)
	scp deploy/docker-compose.yml $(SSH_HOST):$(REMOTE_DIR)/docker-compose.yml
	scp deploy/nginx/nginx-standalone.conf $(SSH_HOST):$(REMOTE_DIR)/nginx/nginx-standalone.conf
	scp deploy/nginx/nginx-proxy.conf $(SSH_HOST):$(REMOTE_DIR)/nginx/nginx-proxy.conf

deploy: require-host test build sync-config ## Test, build, ship the image and restart the stack
	@echo ">> Shipping $(IMAGE):$(TAG) to $(SSH_HOST)"
	docker save $(IMAGE):$(TAG) | gzip | ssh $(SSH_HOST) 'gunzip | docker load'
	@echo ">> Restarting stack on $(SSH_HOST)"
	ssh $(SSH_HOST) 'docker tag $(IMAGE):$(TAG) $(IMAGE):latest \
		&& cd $(REMOTE_DIR) && docker compose down && docker compose --profile $(NGINX_MODE) up -d'
	@echo ">> Deployed $(IMAGE):$(TAG)"

restart: require-host ## Restart the remote stack without rebuilding/shipping
	ssh $(SSH_HOST) 'cd $(REMOTE_DIR) && docker compose down && docker compose --profile $(NGINX_MODE) up -d'

logs: require-host ## Tail the remote application logs
	ssh $(SSH_HOST) 'cd $(REMOTE_DIR) && docker compose logs -f --tail=100'

ps: require-host ## Show the status of the remote stack
	ssh $(SSH_HOST) 'cd $(REMOTE_DIR) && docker compose ps'

pull-prod-data: require-host ## Replace the local dev database with a copy of production data (wipes local data)
	tmp=$$(mktemp --suffix=.json) && \
	ssh $(SSH_HOST) 'cd $(REMOTE_DIR) && docker compose exec -T web python manage.py dumpdata \
		--natural-foreign --natural-primary --indent 2 \
		--exclude auth --exclude contenttypes --exclude admin.logentry --exclude sessions --exclude contact' > "$$tmp" && \
	(cd src && uv run python manage.py flush --no-input && uv run python manage.py loaddata "$$tmp"); \
	rm -f "$$tmp"

regenerate-images: require-host ## Clear the imagekit CACHE and regenerate all thumbnails on the server
	ssh $(SSH_HOST) 'cd $(REMOTE_DIR) && docker compose exec -T web sh -c "rm -rf /app/mediafiles/CACHE && python manage.py generateimages"'

prune: require-host ## Free disk on the server: drop old app image tags (keeps :latest) and dangling layers
	ssh $(SSH_HOST) 'docker images $(IMAGE) --format "{{.Tag}}" | grep -vxE "latest|<none>" | xargs -r -I{} docker rmi $(IMAGE):{}; docker image prune -f'

ssh: require-host ## Open an interactive SSH session on the server
	ssh $(SSH_HOST)
