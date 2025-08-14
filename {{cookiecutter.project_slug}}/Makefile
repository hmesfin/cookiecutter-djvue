# Makefile for {{ cookiecutter.project_name }}
# Run 'make help' for available commands

.PHONY: help dev build test clean

# Variables
DOCKER_COMPOSE = docker-compose
DOCKER_COMPOSE_PROD = docker-compose -f docker-compose.prod.yml
BACKEND_DIR = backend
FRONTEND_DIR = frontend
PYTHON = python
NPM = npm

# Colors for output
RED := \033[0;31m
GREEN := \033[0;32m
YELLOW := \033[0;33m
NC := \033[0m # No Color

help: ## Show this help message
	@echo "{{ cookiecutter.project_name }} - Available Commands"
	@echo "================================================"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

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

# Production commands
prod-up: ## Start production containers
{% if cookiecutter.use_docker == 'y' -%}
	$(DOCKER_COMPOSE_PROD) up -d
{% else -%}
	@echo "Please configure your production deployment"
{%- endif %}

prod-down: ## Stop production containers
{% if cookiecutter.use_docker == 'y' -%}
	$(DOCKER_COMPOSE_PROD) down
{% else -%}
	@echo "Please configure your production deployment"
{%- endif %}

prod-logs: ## Show production logs
{% if cookiecutter.use_docker == 'y' -%}
	$(DOCKER_COMPOSE_PROD) logs -f
{% else -%}
	@echo "Please check your production logs"
{%- endif %}

prod-build: ## Build production images
{% if cookiecutter.use_docker == 'y' -%}
	$(DOCKER_COMPOSE_PROD) build
{% else -%}
	cd $(BACKEND_DIR) && $(PYTHON) manage.py collectstatic --noinput
	cd $(FRONTEND_DIR) && $(NPM) run build
{%- endif %}

# Security commands
security-check: ## Run security checks
	@echo "$(YELLOW)Checking Python dependencies...$(NC)"
	cd $(BACKEND_DIR) && pip audit || true
	@echo "$(YELLOW)Checking Node dependencies...$(NC)"
	cd $(FRONTEND_DIR) && npm audit || true

security-fix: ## Auto-fix security issues
	@echo "$(YELLOW)Fixing Node vulnerabilities...$(NC)"
	cd $(FRONTEND_DIR) && npm audit fix || true
	@echo "$(YELLOW)Python vulnerabilities must be fixed manually$(NC)"

# Deployment commands
deploy: ## Deploy to production
	@echo "$(GREEN)Starting deployment...$(NC)"
	@echo "Please configure your deployment process in this target"
	# Example: git push production main
	# Example: ansible-playbook deploy.yml
	# Example: kubectl apply -f k8s/

health-check: ## Check application health
	@echo "$(GREEN)Checking application health...$(NC)"
	@curl -f http://localhost:8000/api/health/ || echo "$(RED)Backend health check failed$(NC)"
	@curl -f http://localhost:5173/ || echo "$(RED)Frontend health check failed$(NC)"

backup: ## Backup database
	@echo "$(GREEN)Creating database backup...$(NC)"
	@mkdir -p backups
{% if cookiecutter.database == 'postgresql' -%}
{% if cookiecutter.use_docker == 'y' -%}
	$(DOCKER_COMPOSE) exec postgres pg_dump -U {{ cookiecutter.project_slug }} {{ cookiecutter.project_slug }} | gzip > backups/backup_$$(date +%Y%m%d_%H%M%S).sql.gz
{% else -%}
	pg_dump {{ cookiecutter.project_slug }} | gzip > backups/backup_$$(date +%Y%m%d_%H%M%S).sql.gz
{%- endif %}
{% elif cookiecutter.database == 'mysql' -%}
{% if cookiecutter.use_docker == 'y' -%}
	$(DOCKER_COMPOSE) exec mysql mysqldump -u {{ cookiecutter.project_slug }} -p {{ cookiecutter.project_slug }} | gzip > backups/backup_$$(date +%Y%m%d_%H%M%S).sql.gz
{% else -%}
	mysqldump -u {{ cookiecutter.project_slug }} -p {{ cookiecutter.project_slug }} | gzip > backups/backup_$$(date +%Y%m%d_%H%M%S).sql.gz
{%- endif %}
{% else -%}
	cp $(BACKEND_DIR)/db.sqlite3 backups/backup_$$(date +%Y%m%d_%H%M%S).sqlite3
{%- endif %}
	@echo "$(GREEN)Backup created in backups/ directory$(NC)"

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