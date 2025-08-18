#!/bin/bash

# {{ cookiecutter.project_name }} - Quick Start Script
# This script sets up the development environment quickly

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Banner
echo -e "${BLUE}"
echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║                                                                  ║"
echo "║         {{ cookiecutter.project_name }} - Quick Start           ║"
echo "║                                                                  ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Function to print colored messages
print_step() {
    echo -e "\n${GREEN}▶ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check system requirements
check_requirements() {
    print_step "Checking system requirements..."
    
    local missing_deps=()
    
    {% if cookiecutter.use_docker == 'y' -%}
    # Check for Docker
    if ! command_exists docker; then
        missing_deps+=("docker")
    else
        print_success "Docker found: $(docker --version)"
    fi
    
    # Check for Docker Compose
    if ! command_exists docker-compose; then
        missing_deps+=("docker-compose")
    else
        print_success "Docker Compose found: $(docker-compose --version)"
    fi
    {% else -%}
    # Check for Python
    if ! command_exists python3; then
        missing_deps+=("python3")
    else
        print_success "Python found: $(python3 --version)"
    fi
    
    # Check for pip
    if ! command_exists pip; then
        missing_deps+=("pip")
    else
        print_success "pip found: $(pip --version)"
    fi
    
    # Check for Node.js
    if ! command_exists node; then
        missing_deps+=("nodejs")
    else
        print_success "Node.js found: $(node --version)"
    fi
    
    # Check for npm
    if ! command_exists npm; then
        missing_deps+=("npm")
    else
        print_success "npm found: $(npm --version)"
    fi
    
    {% if cookiecutter.database == 'postgresql' -%}
    # Check for PostgreSQL
    if ! command_exists psql; then
        print_warning "PostgreSQL client not found (optional for local development)"
    else
        print_success "PostgreSQL found: $(psql --version)"
    fi
    {% elif cookiecutter.database == 'mysql' -%}
    # Check for MySQL
    if ! command_exists mysql; then
        print_warning "MySQL client not found (optional for local development)"
    else
        print_success "MySQL found: $(mysql --version)"
    fi
    {%- endif %}
    
    {% if cookiecutter.use_redis == 'y' -%}
    # Check for Redis
    if ! command_exists redis-cli; then
        print_warning "Redis client not found (optional for local development)"
    else
        print_success "Redis found: $(redis-cli --version)"
    fi
    {%- endif %}
    {%- endif %}
    
    # Check for Make
    if ! command_exists make; then
        print_warning "Make not found (optional but recommended)"
    else
        print_success "Make found: $(make --version | head -n1)"
    fi
    
    # Check for Git
    if ! command_exists git; then
        missing_deps+=("git")
    else
        print_success "Git found: $(git --version)"
    fi
    
    # Report missing dependencies
    if [ ${#missing_deps[@]} -gt 0 ]; then
        print_error "Missing required dependencies: ${missing_deps[*]}"
        echo ""
        echo "Please install the missing dependencies and run this script again."
        
        # Provide installation hints
        if [[ "$OSTYPE" == "darwin"* ]]; then
            echo "On macOS, you can use Homebrew:"
            for dep in "${missing_deps[@]}"; do
                echo "  brew install $dep"
            done
        elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
            echo "On Ubuntu/Debian, you can use apt:"
            for dep in "${missing_deps[@]}"; do
                echo "  sudo apt-get install $dep"
            done
        fi
        exit 1
    fi
    
    print_success "All requirements met!"
}

# Function to setup environment files
setup_env_files() {
    print_step "Setting up environment files..."
    
    # Backend .env
    if [ ! -f backend/.env ]; then
        if [ -f backend/.env.example ]; then
            cp backend/.env.example backend/.env
            print_success "Created backend/.env from template"
            print_warning "Please update backend/.env with your configuration"
        else
            print_error "backend/.env.example not found!"
            exit 1
        fi
    else
        print_success "backend/.env already exists"
    fi
    
    # Frontend .env
    if [ ! -f frontend/.env ]; then
        if [ -f frontend/.env.example ]; then
            cp frontend/.env.example frontend/.env
            print_success "Created frontend/.env from template"
        else
            print_error "frontend/.env.example not found!"
            exit 1
        fi
    else
        print_success "frontend/.env already exists"
    fi
}

{% if cookiecutter.use_docker == 'y' -%}
# Function to setup Docker environment
setup_docker() {
    print_step "Setting up Docker environment..."
    
    # Build Docker images
    print_step "Building Docker images..."
    docker-compose build
    
    if [ $? -eq 0 ]; then
        print_success "Docker images built successfully"
    else
        print_error "Failed to build Docker images"
        exit 1
    fi
    
    # Start services
    print_step "Starting services..."
    docker-compose up -d
    
    if [ $? -eq 0 ]; then
        print_success "Services started successfully"
    else
        print_error "Failed to start services"
        exit 1
    fi
    
    # Wait for database to be ready
    print_step "Waiting for database to be ready..."
    sleep 5
    
    {% if cookiecutter.database == 'postgresql' -%}
    docker-compose exec -T db pg_isready -U {{ cookiecutter.project_slug }}
    {% elif cookiecutter.database == 'mysql' -%}
    docker-compose exec -T db mysqladmin ping -h localhost --silent
    {%- endif %}
    
    if [ $? -eq 0 ]; then
        print_success "Database is ready"
    else
        print_warning "Database might not be ready yet, continuing anyway..."
    fi
}

# Function to run migrations
run_migrations() {
    print_step "Running database migrations..."
    docker-compose exec -T backend python manage.py migrate
    
    if [ $? -eq 0 ]; then
        print_success "Migrations completed"
    else
        print_error "Failed to run migrations"
        exit 1
    fi
}

# Function to create superuser
create_superuser() {
    print_step "Creating superuser account..."
    echo ""
    echo "Please enter credentials for the admin account:"
    docker-compose exec backend python manage.py createsuperuser
}

# Function to load sample data
load_sample_data() {
    if [ -f backend/fixtures/sample_data.json ]; then
        print_step "Loading sample data..."
        docker-compose exec -T backend python manage.py loaddata fixtures/sample_data.json
        print_success "Sample data loaded"
    else
        print_warning "No sample data found (backend/fixtures/sample_data.json)"
    fi
}

{% else -%}
# Function to setup Python environment
setup_python() {
    print_step "Setting up Python environment..."
    
    # Create virtual environment if it doesn't exist
    if [ ! -d "backend/venv" ]; then
        print_step "Creating Python virtual environment..."
        python3 -m venv backend/venv
        print_success "Virtual environment created"
    else
        print_success "Virtual environment already exists"
    fi
    
    # Activate virtual environment
    source backend/venv/bin/activate
    
    # Upgrade pip
    print_step "Upgrading pip..."
    pip install --upgrade pip
    
    # Install dependencies
    print_step "Installing Python dependencies..."
    pip install -r backend/requirements/development.txt
    
    if [ $? -eq 0 ]; then
        print_success "Python dependencies installed"
    else
        print_error "Failed to install Python dependencies"
        exit 1
    fi
}

# Function to setup Node.js environment
setup_node() {
    print_step "Setting up Node.js environment..."
    
    cd frontend
    
    # Install dependencies
    print_step "Installing Node.js dependencies..."
    npm install
    
    if [ $? -eq 0 ]; then
        print_success "Node.js dependencies installed"
    else
        print_error "Failed to install Node.js dependencies"
        exit 1
    fi
    
    cd ..
}

# Function to setup database
setup_database() {
    print_step "Setting up database..."
    
    {% if cookiecutter.database == 'postgresql' -%}
    # Check if database exists
    if psql -lqt | cut -d \| -f 1 | grep -qw {{ cookiecutter.project_slug }}; then
        print_success "Database '{{ cookiecutter.project_slug }}' already exists"
    else
        print_step "Creating PostgreSQL database..."
        createdb {{ cookiecutter.project_slug }}
        print_success "Database created"
    fi
    {% elif cookiecutter.database == 'mysql' -%}
    # Check if database exists
    if mysql -e "USE {{ cookiecutter.project_slug }};" 2>/dev/null; then
        print_success "Database '{{ cookiecutter.project_slug }}' already exists"
    else
        print_step "Creating MySQL database..."
        mysql -e "CREATE DATABASE {{ cookiecutter.project_slug }};"
        print_success "Database created"
    fi
    {%- endif %}
}

# Function to run migrations
run_migrations() {
    print_step "Running database migrations..."
    
    source backend/venv/bin/activate
    cd backend
    python manage.py migrate
    
    if [ $? -eq 0 ]; then
        print_success "Migrations completed"
    else
        print_error "Failed to run migrations"
        exit 1
    fi
    
    cd ..
}

# Function to create superuser
create_superuser() {
    print_step "Creating superuser account..."
    echo ""
    echo "Please enter credentials for the admin account:"
    
    source backend/venv/bin/activate
    cd backend
    python manage.py createsuperuser
    cd ..
}

# Function to load sample data
load_sample_data() {
    if [ -f backend/fixtures/sample_data.json ]; then
        print_step "Loading sample data..."
        source backend/venv/bin/activate
        cd backend
        python manage.py loaddata fixtures/sample_data.json
        cd ..
        print_success "Sample data loaded"
    else
        print_warning "No sample data found (backend/fixtures/sample_data.json)"
    fi
}

# Function to start services
start_services() {
    print_step "Starting development servers..."
    
    # Start backend
    source backend/venv/bin/activate
    cd backend
    python manage.py runserver &
    BACKEND_PID=$!
    cd ..
    
    # Start frontend
    cd frontend
    npm run dev &
    FRONTEND_PID=$!
    cd ..
    
    print_success "Development servers started"
    echo ""
    echo "Backend PID: $BACKEND_PID"
    echo "Frontend PID: $FRONTEND_PID"
    echo ""
    echo "To stop servers, run: kill $BACKEND_PID $FRONTEND_PID"
}
{%- endif %}

# Function to show completion message
show_completion() {
    echo ""
    echo -e "${GREEN}╔══════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║                                                                  ║${NC}"
    echo -e "${GREEN}║              🎉 Setup Complete! 🎉                              ║${NC}"
    echo -e "${GREEN}║                                                                  ║${NC}"
    echo -e "${GREEN}╚══════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${BLUE}Your application is ready!${NC}"
    echo ""
    echo "📍 Access points:"
    echo "   • Frontend:    http://localhost:{{ cookiecutter.frontend_port }}"
    echo "   • Backend API: http://localhost:8000"
    echo "   • Admin Panel: http://localhost:8000/admin"
    {% if cookiecutter.use_drf_spectacular == 'y' -%}
    echo "   • API Docs:    http://localhost:8000/api/docs"
    {%- endif %}
    {% if cookiecutter.use_graphql == 'y' -%}
    echo "   • GraphQL:     http://localhost:8000/graphql"
    {%- endif %}
    {% if cookiecutter.use_celery == 'y' -%}
    echo "   • Flower:      http://localhost:5555"
    {%- endif %}
    echo ""
    echo "📚 Useful commands:"
    echo "   • View all commands:  make help"
    echo "   • Start development:  make dev"
    echo "   • Run tests:          make test"
    echo "   • View logs:          make logs"
    {% if cookiecutter.use_docker == 'y' -%}
    echo "   • Stop services:      make down"
    echo "   • Shell access:       docker-compose exec backend bash"
    {% else -%}
    echo "   • Django shell:       cd backend && python manage.py shell"
    echo "   • Stop servers:       Press Ctrl+C"
    {%- endif %}
    echo ""
    echo "📖 Documentation:"
    echo "   • README.md:          Project overview and setup"
    echo "   • ARCHITECTURE.md:    System architecture"
    echo "   • DEPLOYMENT.md:      Deployment guide"
    echo ""
    echo -e "${YELLOW}⚠  Next steps:${NC}"
    echo "   1. Update environment variables in .env files"
    echo "   2. Configure your database settings"
    {% if cookiecutter.use_social_auth == 'y' -%}
    echo "   3. Set up OAuth credentials for social login"
    {%- endif %}
    echo ""
    echo -e "${GREEN}Happy coding! 🚀${NC}"
}

# Main execution
main() {
    echo "Starting quick setup for {{ cookiecutter.project_name }}..."
    echo "This will set up your development environment automatically."
    echo ""
    
    # Check requirements
    check_requirements
    
    # Setup environment files
    setup_env_files
    
    {% if cookiecutter.use_docker == 'y' -%}
    # Docker setup
    setup_docker
    
    # Run migrations
    run_migrations
    
    # Ask about creating superuser
    echo ""
    read -p "Would you like to create a superuser account now? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        create_superuser
    else
        print_warning "Skipping superuser creation. You can create one later with: make createsuperuser"
    fi
    
    # Ask about loading sample data
    echo ""
    read -p "Would you like to load sample data? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        load_sample_data
    fi
    {% else -%}
    # Setup Python environment
    setup_python
    
    # Setup Node.js environment
    setup_node
    
    # Setup database
    setup_database
    
    # Run migrations
    run_migrations
    
    # Ask about creating superuser
    echo ""
    read -p "Would you like to create a superuser account now? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        create_superuser
    else
        print_warning "Skipping superuser creation. You can create one later with: cd backend && python manage.py createsuperuser"
    fi
    
    # Ask about loading sample data
    echo ""
    read -p "Would you like to load sample data? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        load_sample_data
    fi
    
    # Ask about starting services
    echo ""
    read -p "Would you like to start the development servers now? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        start_services
    else
        print_warning "You can start servers later with: make dev"
    fi
    {%- endif %}
    
    # Show completion message
    show_completion
}

# Run main function
main