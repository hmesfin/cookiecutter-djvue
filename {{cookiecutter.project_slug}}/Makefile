.PHONY: help dev build test clean

# Variables
DOCKER_COMPOSE = docker-compose
BACKEND_DIR = backend
FRONTEND_DIR = frontend
PYTHON = python
NPM = npm

help: ## Show this help message
	@echo "Usage: make [target]"
	@echo ""
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-15s %s\n", $$1, $$2}'

# Development commands
dev: ## Start development environment
{% if cookiecutter.use_docker == 'y' -%}
	$(DOCKER_COMPOSE) up
{% else -%}
	@echo "Starting backend..."
	cd $(BACKEND_DIR) && $(PYTHON) manage.py runserver &
	@echo "Starting frontend..."
	cd $(FRONTEND_DIR) && $(NPM) run dev
{%- endif %}

dev-build: ## Build and start development environment
{% if cookiecutter.use_docker == 'y' -%}
	$(DOCKER_COMPOSE) up --build
{% else -%}
	@echo "Installing backend dependencies..."
	cd $(BACKEND_DIR) && pip install -r requirements/development.txt
	@echo "Installing frontend dependencies..."
	cd $(FRONTEND_DIR) && $(NPM) install
	make dev
{%- endif %}

# Database commands
migrate: ## Run database migrations
{% if cookiecutter.use_docker == 'y' -%}
	$(DOCKER_COMPOSE) exec backend python manage.py migrate
{% else -%}
	cd $(BACKEND_DIR) && $(PYTHON) manage.py migrate
{%- endif %}

makemigrations: ## Create database migrations
{% if cookiecutter.use_docker == 'y' -%}
	$(DOCKER_COMPOSE) exec backend python manage.py makemigrations
{% else -%}
	cd $(BACKEND_DIR) && $(PYTHON) manage.py makemigrations
{%- endif %}

createsuperuser: ## Create Django superuser
{% if cookiecutter.use_docker == 'y' -%}
	$(DOCKER_COMPOSE) exec backend python manage.py createsuperuser
{% else -%}
	cd $(BACKEND_DIR) && $(PYTHON) manage.py createsuperuser
{%- endif %}

create-dev-superuser: ## Create development superuser (admin/admin123)
{% if cookiecutter.use_docker == 'y' -%}
	$(DOCKER_COMPOSE) exec backend python manage.py create_dev_superuser
{% else -%}
	cd $(BACKEND_DIR) && $(PYTHON) manage.py create_dev_superuser
{%- endif %}

# Testing commands
test: ## Run all tests
	make test-backend
	make test-frontend

test-backend: ## Run backend tests
{% if cookiecutter.use_docker == 'y' -%}
	$(DOCKER_COMPOSE) exec backend pytest
{% else -%}
	cd $(BACKEND_DIR) && pytest
{%- endif %}

test-frontend: ## Run frontend tests
{% if cookiecutter.use_docker == 'y' -%}
	$(DOCKER_COMPOSE) exec frontend npm run test:unit
{% else -%}
	cd $(FRONTEND_DIR) && $(NPM) run test:unit
{%- endif %}

test-e2e: ## Run end-to-end tests
{% if cookiecutter.use_docker == 'y' -%}
	$(DOCKER_COMPOSE) exec frontend npm run test:e2e
{% else -%}
	cd $(FRONTEND_DIR) && $(NPM) run test:e2e
{%- endif %}

# Code quality commands
lint: ## Run linters
	make lint-backend
	make lint-frontend

lint-backend: ## Run backend linters
{% if cookiecutter.use_docker == 'y' -%}
	{% if cookiecutter.use_ruff == 'y' -%}
	$(DOCKER_COMPOSE) exec backend ruff check .
	$(DOCKER_COMPOSE) exec backend ruff format --check .
	{%- endif %}
{% else -%}
	{% if cookiecutter.use_ruff == 'y' -%}
	cd $(BACKEND_DIR) && ruff check .
	cd $(BACKEND_DIR) && ruff format --check .
	{%- endif %}
{%- endif %}

lint-frontend: ## Run frontend linters
{% if cookiecutter.use_docker == 'y' -%}
	{% if cookiecutter.use_eslint == 'y' -%}
	$(DOCKER_COMPOSE) exec frontend npm run lint
	{%- endif %}
{% else -%}
	{% if cookiecutter.use_eslint == 'y' -%}
	cd $(FRONTEND_DIR) && $(NPM) run lint
	{%- endif %}
{%- endif %}

format: ## Format code
	make format-backend
	make format-frontend

format-backend: ## Format backend code
{% if cookiecutter.use_docker == 'y' -%}
	{% if cookiecutter.use_ruff == 'y' -%}
	$(DOCKER_COMPOSE) exec backend ruff check --fix .
	$(DOCKER_COMPOSE) exec backend ruff format .
	{%- endif %}
{% else -%}
	{% if cookiecutter.use_ruff == 'y' -%}
	cd $(BACKEND_DIR) && ruff check --fix .
	cd $(BACKEND_DIR) && ruff format .
	{%- endif %}
{%- endif %}

format-frontend: ## Format frontend code
{% if cookiecutter.use_docker == 'y' -%}
	{% if cookiecutter.use_prettier == 'y' -%}
	$(DOCKER_COMPOSE) exec frontend npm run format
	{%- endif %}
{% else -%}
	{% if cookiecutter.use_prettier == 'y' -%}
	cd $(FRONTEND_DIR) && $(NPM) run format
	{%- endif %}
{%- endif %}

# Build commands
build: ## Build production images
{% if cookiecutter.use_docker == 'y' -%}
	$(DOCKER_COMPOSE) -f docker-compose.prod.yml build
{% else -%}
	cd $(BACKEND_DIR) && $(PYTHON) manage.py collectstatic --noinput
	cd $(FRONTEND_DIR) && $(NPM) run build
{%- endif %}

# Deployment commands
deploy: ## Deploy to production
	@echo "Deployment command not configured. Please set up your deployment process."

# Utility commands
shell: ## Open Django shell
{% if cookiecutter.use_docker == 'y' -%}
	$(DOCKER_COMPOSE) exec backend python manage.py shell_plus
{% else -%}
	cd $(BACKEND_DIR) && $(PYTHON) manage.py shell_plus
{%- endif %}

logs: ## Show logs
{% if cookiecutter.use_docker == 'y' -%}
	$(DOCKER_COMPOSE) logs -f
{% else -%}
	@echo "Logs are in the console where you ran 'make dev'"
{%- endif %}

clean: ## Clean up generated files
{% if cookiecutter.use_docker == 'y' -%}
	$(DOCKER_COMPOSE) down -v
{% endif -%}
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name ".pytest_cache" -delete
	rm -rf $(BACKEND_DIR)/staticfiles
	rm -rf $(BACKEND_DIR)/media
	rm -rf $(FRONTEND_DIR)/dist
	rm -rf $(FRONTEND_DIR)/node_modules

# Docker commands
{% if cookiecutter.use_docker == 'y' -%}
up: ## Start Docker containers
	$(DOCKER_COMPOSE) up -d

down: ## Stop Docker containers
	$(DOCKER_COMPOSE) down

restart: ## Restart Docker containers
	$(DOCKER_COMPOSE) restart

ps: ## Show Docker container status
	$(DOCKER_COMPOSE) ps

exec-backend: ## Open backend container shell
	$(DOCKER_COMPOSE) exec backend /bin/bash

exec-frontend: ## Open frontend container shell
	$(DOCKER_COMPOSE) exec frontend /bin/sh
{%- endif %}

# Dark mode commands
dark-analyze: ## Analyze components for dark mode readiness
	@echo "Analyzing components for dark mode..."
	@python scripts/apply_dark_mode.py --analyze

dark-apply: ## Apply dark mode classes to components
	@echo "Applying dark mode classes..."
	@python scripts/apply_dark_mode.py

dark-dry-run: ## Preview dark mode changes without applying
	@echo "Previewing dark mode changes..."
	@python scripts/apply_dark_mode.py --dry-run --verbose