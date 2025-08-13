#!/usr/bin/env python
"""
Post-generation hook for cookiecutter-djvue.
Sets up the project after generation.
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path


PROJECT_DIR = Path.cwd()
BACKEND_DIR = PROJECT_DIR / 'backend'
FRONTEND_DIR = PROJECT_DIR / 'frontend'


def remove_file(filepath):
    """Remove a file if it exists."""
    path = Path(filepath)
    if path.exists():
        path.unlink()


def remove_dir(dirpath):
    """Remove a directory if it exists."""
    path = Path(dirpath)
    if path.exists() and path.is_dir():
        shutil.rmtree(path)


def run_command(command, cwd=None, check=True):
    """Run a shell command."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            check=check,
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}")
        print(f"Error output: {e.stderr}")
        return False


def clean_up_files():
    """Remove unnecessary files based on configuration."""
    print("Cleaning up unnecessary files...")
    
    # Remove Docker files if not using Docker
    if '{{ cookiecutter.use_docker }}' != 'y':
        remove_file('docker-compose.yml')
        remove_file('docker-compose.prod.yml')
        remove_dir('docker')
        print("  - Removed Docker files")
    
    # Remove TypeScript files if not using TypeScript
    if '{{ cookiecutter.use_typescript }}' != 'y':
        remove_file(FRONTEND_DIR / 'tsconfig.json')
        remove_file(FRONTEND_DIR / 'tsconfig.node.json')
        remove_file(FRONTEND_DIR / 'src' / 'vite-env.d.ts')
        # Rename .ts files to .js
        for ts_file in FRONTEND_DIR.rglob('*.ts'):
            if not str(ts_file).endswith('.d.ts'):
                js_file = ts_file.with_suffix('.js')
                ts_file.rename(js_file)
        print("  - Removed TypeScript configuration")
    
    # Remove Tailwind files if not using Tailwind
    if '{{ cookiecutter.css_framework }}' != 'tailwindcss':
        remove_file(FRONTEND_DIR / 'tailwind.config.js')
        remove_file(FRONTEND_DIR / 'postcss.config.js')
        remove_file(FRONTEND_DIR / 'src' / 'assets' / 'tailwind.css')
        print("  - Removed Tailwind CSS files")
    
    # Remove test files if not using pytest
    if '{{ cookiecutter.use_pytest }}' != 'y':
        remove_file(BACKEND_DIR / 'pytest.ini')
        remove_dir(BACKEND_DIR / 'tests')
        print("  - Removed pytest configuration")
    
    # Remove celery file if not using Celery
    if '{{ cookiecutter.use_celery }}' != 'y':
        remove_file(BACKEND_DIR / '{{ cookiecutter.project_slug }}' / 'celery.py')
        print("  - Removed Celery configuration")
    
    # Remove CI/CD files based on selection
    if '{{ cookiecutter.ci_tool }}' == 'none':
        remove_dir('.github')
        remove_file('.gitlab-ci.yml')
        print("  - Removed CI/CD configuration")
    elif '{{ cookiecutter.ci_tool }}' == 'github':
        remove_file('.gitlab-ci.yml')
        print("  - Removed GitLab CI configuration")
    elif '{{ cookiecutter.ci_tool }}' == 'gitlab':
        remove_dir('.github')
        print("  - Removed GitHub Actions configuration")


def initialize_git():
    """Initialize git repository."""
    print("\nInitializing git repository...")
    
    if run_command('git init'):
        print("  ✓ Git repository initialized")
        
        # Create initial commit
        run_command('git add .')
        run_command('git commit -m "Initial commit from cookiecutter-djvue"')
        print("  ✓ Initial commit created")
        
        # Set up main branch
        run_command('git branch -M main')
        print("  ✓ Main branch configured")
    else:
        print("  ⚠ Could not initialize git repository")


def create_env_files():
    """Create .env files from examples."""
    print("\nCreating environment files...")
    
    # Backend .env
    backend_env_example = BACKEND_DIR / '.env.example'
    backend_env = BACKEND_DIR / '.env'
    
    # Generate a real secret key
    secret_key = generate_secret_key()
    
    env_content = f"""
# Django Settings
SECRET_KEY={secret_key}
DEBUG=True
DJANGO_ENV=development

# Database
{% if cookiecutter.database == 'postgresql' -%}
# Using DATABASE_URL for flexibility
# If PostgreSQL is not available, change to: sqlite:///db.sqlite3
DATABASE_URL=postgres://{{ cookiecutter.project_slug }}:changeme@localhost:5432/{{ cookiecutter.project_slug }}
{% elif cookiecutter.database == 'mysql' -%}
# Using DATABASE_URL for flexibility
# If MySQL is not available, change to: sqlite:///db.sqlite3
DATABASE_URL=mysql://{{ cookiecutter.project_slug }}:changeme@localhost:3306/{{ cookiecutter.project_slug }}
{% else -%}
# Using SQLite for development
DATABASE_URL=sqlite:///db.sqlite3
{%- endif %}

# Redis
{% if cookiecutter.use_redis == 'y' -%}
REDIS_URL=redis://localhost:6379/0
{%- endif %}

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:{{ cookiecutter.frontend_port }}

# Email
EMAIL_HOST=localhost
EMAIL_PORT=1025
EMAIL_USE_TLS=False
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
DEFAULT_FROM_EMAIL=noreply@{{ cookiecutter.domain_name }}

# Frontend URL
FRONTEND_URL=http://localhost:{{ cookiecutter.frontend_port }}
"""
    
    with open(backend_env, 'w') as f:
        f.write(env_content.strip())
    print("  ✓ Backend .env created")
    
    # Frontend .env
    frontend_env = FRONTEND_DIR / '.env'
    if not frontend_env.exists():
        shutil.copy(FRONTEND_DIR / '.env.example', frontend_env)
        print("  ✓ Frontend .env created")


def generate_secret_key():
    """Generate a secure secret key for Django."""
    try:
        from django.core.management.utils import get_random_secret_key
        return get_random_secret_key()
    except ImportError:
        import random
        import string
        chars = string.ascii_letters + string.digits + '!@#$%^&*(-_=+)'
        return ''.join(random.choice(chars) for _ in range(50))


def create_directories():
    """Create necessary directories."""
    print("\nCreating project directories...")
    
    dirs_to_create = [
        BACKEND_DIR / 'static',
        BACKEND_DIR / 'media',
        BACKEND_DIR / 'staticfiles',
        BACKEND_DIR / 'logs',
        FRONTEND_DIR / 'public',
    ]
    
    for directory in dirs_to_create:
        directory.mkdir(parents=True, exist_ok=True)
    
    print("  ✓ Directories created")


def install_pre_commit():
    """Install pre-commit hooks."""
    if '{{ cookiecutter.use_pre_commit }}' == 'y':
        print("\nSetting up pre-commit hooks...")
        
        # Create pre-commit configuration
        pre_commit_config = """
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-json
      - id: check-toml
      - id: check-merge-conflict
      - id: detect-private-key

{% if cookiecutter.use_ruff == 'y' -%}
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.6.0
    hooks:
      # Run the linter
      - id: ruff
        args: [--fix]
        exclude: ^backend/migrations/
      # Run the formatter
      - id: ruff-format
        exclude: ^backend/migrations/
{%- endif %}

{% if cookiecutter.use_eslint == 'y' -%}
  - repo: https://github.com/pre-commit/mirrors-eslint
    rev: v9.8.0
    hooks:
      - id: eslint
        files: \\.vue$|\\.js$|\\.jsx$|\\.ts$|\\.tsx$
        types: [file]
        additional_dependencies:
          - eslint
          - eslint-plugin-vue
{%- endif %}

{% if cookiecutter.use_prettier == 'y' -%}
  - repo: https://github.com/pre-commit/mirrors-prettier
    rev: v3.1.0
    hooks:
      - id: prettier
        files: \\.vue$|\\.js$|\\.jsx$|\\.ts$|\\.tsx$|\\.json$|\\.css$|\\.scss$|\\.md$
        exclude: ^frontend/dist/
{%- endif %}
"""
        
        with open('.pre-commit-config.yaml', 'w') as f:
            f.write(pre_commit_config.strip())
        
        print("  ✓ Pre-commit configuration created")
    
    # Mark setup script as executable
    setup_file = Path('scripts/setup.sh')
    if setup_file.exists():
        setup_file.chmod(0o755)
        print("  ✓ Setup script made executable")


def create_setup_script():
    """Create a setup script for easy project initialization."""
    print("\nCreating setup script...")
    
    setup_script = """#!/bin/bash
# Setup script for {{ cookiecutter.project_name }}

set -e

echo "Setting up {{ cookiecutter.project_name }}..."

# Colors for output
RED='\\033[0;31m'
GREEN='\\033[0;32m'
YELLOW='\\033[1;33m'
NC='\\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Check required tools
echo "Checking requirements..."

if ! command -v python{{ cookiecutter.python_version.split('.')[0] }} &> /dev/null; then
    print_error "Python {{ cookiecutter.python_version }} is not installed"
    exit 1
fi
print_status "Python {{ cookiecutter.python_version }} found"

if ! command -v node &> /dev/null; then
    print_error "Node.js is not installed"
    exit 1
fi
print_status "Node.js found"

{% if cookiecutter.use_docker == 'y' -%}
if ! command -v docker &> /dev/null; then
    print_warning "Docker is not installed (optional)"
fi

if ! command -v docker-compose &> /dev/null; then
    print_warning "Docker Compose is not installed (optional)"
fi
{%- endif %}

# Backend setup
echo ""
echo "Setting up backend..."
cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    python{{ cookiecutter.python_version.split('.')[0] }} -m venv venv
    print_status "Virtual environment created"
else
    print_status "Virtual environment already exists"
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements/development.txt
print_status "Backend dependencies installed"

# Run migrations
python manage.py migrate
print_status "Database migrations completed"

{% if cookiecutter.use_ruff == 'y' -%}
# Run Ruff formatting on initial code
echo ""
echo "Formatting Python code with Ruff..."
ruff check --fix . --quiet 2>/dev/null || true
ruff format . --quiet 2>/dev/null || true
print_status "Python code formatted"
{%- endif %}

# Create superuser
echo ""
echo "Would you like to create a superuser? (y/n)"
read -r response
if [[ "$response" == "y" ]]; then
    python manage.py createsuperuser
fi

cd ..

# Frontend setup
echo ""
echo "Setting up frontend..."
cd frontend

# Install dependencies
npm install
print_status "Frontend dependencies installed"

cd ..

{% if cookiecutter.use_pre_commit == 'y' -%}
# Install pre-commit hooks
echo ""
echo "Installing pre-commit hooks..."
if command -v pre-commit &> /dev/null; then
    pre-commit install
    print_status "Pre-commit hooks installed"
else
    print_warning "pre-commit not found, skipping hook installation"
    echo "  Install with: pip install pre-commit"
fi
{%- endif %}

echo ""
echo "================================"
echo "Setup completed successfully!"
echo "================================"
echo ""
echo "To start the development servers:"
{% if cookiecutter.use_docker == 'y' -%}
echo "  With Docker:    make dev"
echo "  Without Docker: "
echo "    Backend:  cd backend && source venv/bin/activate && python manage.py runserver"
echo "    Frontend: cd frontend && npm run dev"
{% else -%}
echo "  Backend:  cd backend && source venv/bin/activate && python manage.py runserver"
echo "  Frontend: cd frontend && npm run dev"
{%- endif %}
echo ""
echo "Access the application at:"
echo "  Frontend: http://localhost:{{ cookiecutter.frontend_port }}"
echo "  Backend:  http://localhost:{{ cookiecutter.backend_port }}"
echo "  Admin:    http://localhost:{{ cookiecutter.backend_port }}/admin"
{% if cookiecutter.use_mailhog == 'y' -%}
echo "  Mail:     http://localhost:8025 (MailHog)"
{%- endif %}
echo ""
"""
    
    setup_file = PROJECT_DIR / 'scripts' / 'setup.sh'
    setup_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(setup_file, 'w') as f:
        f.write(setup_script.strip())
    
    # Make script executable
    setup_file.chmod(0o755)
    
    print("  ✓ Setup script created at scripts/setup.sh")


def print_success_message():
    """Print success message with next steps."""
    print("\n" + "="*60)
    print("🎉 Project '{{ cookiecutter.project_name }}' created successfully!")
    print("="*60)
    print("\nNext steps:")
    print("  1. cd {{ cookiecutter.project_slug }}")
    print("  2. ./scripts/setup.sh  # Run the setup script")
    print("  3. make dev            # Start development servers")
    print("\nUseful commands:")
    print("  make help              # Show all available commands")
    print("  make test              # Run tests")
    print("  make lint              # Run linters")
    print("  make format            # Format code")
    
    if '{{ cookiecutter.use_docker }}' == 'y':
        print("\nDocker commands:")
        print("  docker-compose up      # Start all services")
        print("  docker-compose logs -f # View logs")
        print("  make shell             # Django shell")
    
    print("\nDocumentation:")
    print("  - Backend API docs: http://localhost:{{ cookiecutter.backend_port }}/api/docs/")
    print("  - Project README: ./README.md")
    
    print("\nHappy coding! 🚀")


def main():
    """Run all post-generation hooks."""
    print("\n" + "="*60)
    print("Running post-generation setup...")
    print("="*60)
    
    clean_up_files()
    create_directories()
    # Don't create env files - let setup.sh handle database detection
    # create_env_files()
    initialize_git()
    install_pre_commit()
    # Don't create setup script - we already have one in template
    # create_setup_script()
    print_success_message()


if __name__ == '__main__':
    main()