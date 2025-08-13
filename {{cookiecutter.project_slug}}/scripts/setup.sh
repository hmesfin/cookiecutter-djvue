#!/bin/bash

# Setup script for {{ cookiecutter.project_name }}
# This script sets up both backend and frontend development environments

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "🚀 Setting up {{ cookiecutter.project_name }}..."

# Check for required tools
check_command() {
    if ! command -v $1 &> /dev/null; then
        echo -e "${RED}❌ $1 is not installed. Please install it first.${NC}"
        exit 1
    else
        echo -e "${GREEN}✓ $1 found${NC}"
    fi
}

echo "📋 Checking prerequisites..."
check_command python3
check_command pip
check_command node
check_command npm

# Backend Setup
echo ""
echo "🔧 Setting up Backend..."
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements/development.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file from example..."
    cat > .env << EOF
# Django Settings
SECRET_KEY=django-insecure-change-this-in-production-$(openssl rand -hex 32)
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

{% if cookiecutter.database == 'postgresql' -%}
# Database - PostgreSQL
DATABASE_URL=postgres://{{ cookiecutter.project_slug }}:changeme@localhost:5432/{{ cookiecutter.project_slug }}
# If PostgreSQL is not available, you can use SQLite for development:
# DATABASE_URL=sqlite:///db.sqlite3
{% elif cookiecutter.database == 'mysql' -%}
# Database - MySQL
DATABASE_URL=mysql://{{ cookiecutter.project_slug }}:changeme@localhost:3306/{{ cookiecutter.project_slug }}
# If MySQL is not available, you can use SQLite for development:
# DATABASE_URL=sqlite:///db.sqlite3
{% else -%}
# Database - SQLite
DATABASE_URL=sqlite:///db.sqlite3
{%- endif %}

{% if cookiecutter.use_redis == 'y' -%}
# Redis (optional for development)
REDIS_URL=redis://localhost:6379/0
{%- endif %}

{% if cookiecutter.use_celery == 'y' -%}
# Celery (optional for development)
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
USE_CELERY=False  # Set to True if you have Redis running
{%- endif %}

# Email (for development, uses console backend)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
SEND_WELCOME_EMAIL=True

# Frontend URL
FRONTEND_URL=http://localhost:{{ cookiecutter.frontend_port }}

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:{{ cookiecutter.frontend_port }}
EOF
    echo -e "${GREEN}✓ .env file created${NC}"
else
    echo -e "${YELLOW}⚠ .env file already exists, skipping...${NC}"
fi

# Check database availability and migrations
echo "Checking database connection..."
{% if cookiecutter.database == 'postgresql' -%}
# Check if PostgreSQL is running
if pg_isready -h localhost -p 5432 &> /dev/null; then
    echo -e "${GREEN}✓ PostgreSQL is running${NC}"
else
    echo -e "${YELLOW}⚠ PostgreSQL is not running. Using SQLite for development.${NC}"
    # Update .env to use SQLite
    sed -i.bak 's|^DATABASE_URL=postgres://.*|DATABASE_URL=sqlite:///db.sqlite3|' .env
fi
{% elif cookiecutter.database == 'mysql' -%}
# Check if MySQL is running
if mysqladmin ping -h localhost --silent &> /dev/null; then
    echo -e "${GREEN}✓ MySQL is running${NC}"
else
    echo -e "${YELLOW}⚠ MySQL is not running. Using SQLite for development.${NC}"
    # Update .env to use SQLite
    sed -i.bak 's|^DATABASE_URL=mysql://.*|DATABASE_URL=sqlite:///db.sqlite3|' .env
fi
{%- endif %}

# Run migrations
echo "Running database migrations..."
python manage.py migrate

# Create superuser if it doesn't exist
echo ""
echo "Creating superuser (if needed)..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(email='admin@example.com').exists():
    User.objects.create_superuser(
        email='admin@example.com',
        username='admin',
        password='admin123',
        first_name='Admin',
        last_name='User'
    )
    print('✓ Superuser created: admin@example.com / admin123')
else:
    print('✓ Superuser already exists')
" || echo -e "${YELLOW}⚠ Could not create superuser automatically${NC}"

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

cd ..

# Frontend Setup
echo ""
echo "🎨 Setting up Frontend..."
cd frontend

# Install dependencies
echo "Installing Node dependencies..."
npm install

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating frontend .env file..."
    cat > .env << EOF
# API URL
VITE_API_URL=http://localhost:{{ cookiecutter.backend_port }}/api

# App Settings
VITE_APP_NAME={{ cookiecutter.project_name }}
EOF
    echo -e "${GREEN}✓ Frontend .env file created${NC}"
else
    echo -e "${YELLOW}⚠ Frontend .env file already exists, skipping...${NC}"
fi

cd ..

# Final instructions
echo ""
echo "✅ Setup complete!"
echo ""
echo "📝 Development credentials:"
echo "   Admin Email: admin@example.com"
echo "   Admin Password: admin123"
echo ""
echo "🚀 To start development servers:"
echo ""
echo "   Option 1 - Using Make (recommended):"
echo "   $ make dev"
echo ""
echo "   Option 2 - Run separately:"
echo "   Backend:"
echo "   $ cd backend"
echo "   $ source venv/bin/activate"
echo "   $ python manage.py runserver"
echo ""
echo "   Frontend (in a new terminal):"
echo "   $ cd frontend"
echo "   $ npm run dev"
echo ""
echo "🌐 Access points:"
echo "   Frontend: http://localhost:{{ cookiecutter.frontend_port }}"
echo "   Backend API: http://localhost:{{ cookiecutter.backend_port }}/api/"
echo "   Admin Panel: http://localhost:{{ cookiecutter.backend_port }}/admin/"
{% if cookiecutter.use_drf_spectacular == 'y' -%}
echo "   API Docs: http://localhost:{{ cookiecutter.backend_port }}/api/docs/"
{%- endif %}
echo ""
echo "Happy coding! 🎉"