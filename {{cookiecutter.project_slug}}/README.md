# {{ cookiecutter.project_name }}

{{ cookiecutter.project_description }}

## 🚀 Features

- **Backend**: Django {{ cookiecutter.django_version }} with REST API
- **Frontend**: Vue.js {{ cookiecutter.vue_version }} with Vite
- **Authentication**: {% if cookiecutter.api_authentication == 'jwt' %}JWT tokens{% elif cookiecutter.api_authentication == 'token' %}Token-based{% else %}Session-based{% endif %}
- **Database**: {% if cookiecutter.database == 'postgresql' %}PostgreSQL{% elif cookiecutter.database == 'mysql' %}MySQL{% else %}SQLite{% endif %}
{% if cookiecutter.use_redis == 'y' -%}
- **Caching**: Redis
{%- endif %}
{% if cookiecutter.use_celery == 'y' -%}
- **Background Tasks**: Celery
{%- endif %}
- **Email System**: Automatic welcome emails with {% if cookiecutter.use_celery == 'y' %}Celery support (falls back to synchronous if disabled){% else %}synchronous sending{% endif %}
{% if cookiecutter.use_docker == 'y' -%}
- **Containerization**: Docker & Docker Compose
{%- endif %}
- **Testing**: {% if cookiecutter.use_pytest == 'y' %}pytest{% else %}Django test{% endif %} (backend), Vitest (frontend)
{% if cookiecutter.ci_tool != 'none' -%}
- **CI/CD**: {% if cookiecutter.ci_tool == 'github' %}GitHub Actions{% else %}GitLab CI{% endif %}
{%- endif %}

## 📋 Prerequisites

- Python {{ cookiecutter.python_version }}+
- Node.js {{ cookiecutter.node_version }}+
{% if cookiecutter.use_docker == 'y' -%}
- Docker and Docker Compose (optional)
{%- endif %}
{% if cookiecutter.database == 'postgresql' -%}
- PostgreSQL {{ cookiecutter.postgres_version }}+
{% elif cookiecutter.database == 'mysql' -%}
- MySQL 8.0+
{%- endif %}
{% if cookiecutter.use_redis == 'y' -%}
- Redis {{ cookiecutter.redis_version }}+
{%- endif %}

## 🛠️ Quick Start

### Using the Setup Script (Recommended)

```bash
# Run the setup script
./scripts/setup.sh

# Start development servers
make dev
```

### Manual Setup

#### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements/development.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

#### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Run development server
npm run dev
```

{% if cookiecutter.use_docker == 'y' -%}
### Using Docker

```bash
# Build and start all services
docker-compose up --build

# Or run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```
{%- endif %}

## 📁 Project Structure

```
{{ cookiecutter.project_slug }}/
├── backend/                    # Django backend
│   ├── {{ cookiecutter.project_slug }}/     # Main Django project
│   │   ├── settings/          # Environment-specific settings
│   │   ├── apps/             # Django applications
│   │   │   ├── core/         # Core functionality
│   │   │   ├── users/        # User management
│   │   │   └── api/          # API endpoints
│   │   └── urls.py           # URL configuration
│   ├── requirements/          # Python dependencies
│   ├── tests/                # Backend tests
│   └── manage.py             # Django management script
├── frontend/                  # Vue.js frontend
│   ├── src/
│   │   ├── assets/           # Static assets
│   │   ├── components/       # Shared Vue components
│   │   ├── layouts/          # Layout components
│   │   ├── modules/          # Feature modules
│   │   │   ├── auth/         # Authentication module
│   │   │   ├── dashboard/    # Dashboard module
│   │   │   └── home/         # Public pages module
│   │   ├── router/           # Vue Router configuration
│   │   ├── stores/           # Pinia stores
│   │   ├── services/         # API services
│   │   └── App.vue           # Root component
│   ├── public/               # Public assets
│   └── package.json          # Node dependencies
{% if cookiecutter.use_docker == 'y' -%}
├── docker/                   # Docker configurations
│   ├── backend/             # Backend Dockerfile
│   ├── frontend/            # Frontend Dockerfile
│   └── nginx/              # Nginx configuration
├── docker-compose.yml       # Development compose file
├── docker-compose.prod.yml  # Production compose file
{%- endif %}
{% if cookiecutter.ci_tool == 'github' -%}
├── .github/                 # GitHub Actions workflows
│   └── workflows/          # CI/CD pipelines
{% elif cookiecutter.ci_tool == 'gitlab' -%}
├── .gitlab-ci.yml          # GitLab CI configuration
{%- endif %}
├── scripts/                # Utility scripts
├── Makefile               # Common commands
└── README.md             # This file
```

## 🧪 Testing

### Run All Tests

```bash
make test
```

### Backend Tests

```bash
# Using Make
make test-backend

# Or manually
cd backend
{% if cookiecutter.use_pytest == 'y' -%}
pytest
pytest --cov={{ cookiecutter.project_slug }} --cov-report=html
{% else -%}
python manage.py test
{%- endif %}
```

### Frontend Tests

```bash
# Using Make
make test-frontend

# Or manually
cd frontend
npm run test:unit
npm run test:e2e
```

## 🎨 Code Quality

### Linting

```bash
# Run all linters
make lint

# Backend linting (using Ruff)
make lint-backend

# Frontend linting
make lint-frontend
```

### Formatting

```bash
# Format all code
make format

# Backend formatting (using Ruff)
make format-backend

# Frontend formatting
make format-frontend
```

{% if cookiecutter.use_ruff == 'y' -%}
### Ruff Configuration

The project uses [Ruff](https://github.com/astral-sh/ruff) for Python linting and formatting. Configuration is in `backend/pyproject.toml`.

```bash
# Check for issues
cd backend && ruff check .

# Auto-fix issues
cd backend && ruff check --fix .

# Format code
cd backend && ruff format .
```
{%- endif %}

## 📝 Available Commands

Run `make help` to see all available commands:

```bash
make help          # Show all available commands
make dev           # Start development environment
make test          # Run all tests
make lint          # Run linters
make format        # Format code
make build         # Build production images
make clean         # Clean up generated files
```

## 🌐 API Documentation

{% if cookiecutter.use_drf_spectacular == 'y' -%}
When the development server is running, you can access:

- **Swagger UI**: http://localhost:{{ cookiecutter.backend_port }}/api/docs/
- **ReDoc**: http://localhost:{{ cookiecutter.backend_port }}/api/redoc/
- **OpenAPI Schema**: http://localhost:{{ cookiecutter.backend_port }}/api/schema/
{%- endif %}

### API Endpoints

- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout  
- `POST /api/auth/register/` - User registration
{% if cookiecutter.api_authentication == 'jwt' -%}
- `POST /api/auth/refresh/` - Refresh JWT token
{%- endif %}
- `GET /api/me/` - Get current user
- `PATCH /api/me/` - Update current user
- `GET /api/users/` - List users
- `GET /api/users/{id}/` - Get user details

## 🚀 Deployment

### Environment Variables

Create `.env` files for your environment with the following variables:

#### Backend (.env)

```env
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.com
DATABASE_URL=postgres://user:pass@host:port/dbname
REDIS_URL=redis://localhost:6379/0
CORS_ALLOWED_ORIGINS=https://your-domain.com
```

#### Frontend (.env)

```env
VITE_API_URL=https://api.your-domain.com
```

### Production Build

```bash
# Build production images
make build

# Or manually
cd backend && python manage.py collectstatic --noinput
cd frontend && npm run build
```

{% if cookiecutter.cloud_provider != 'none' -%}
### Deployment to {{ cookiecutter.cloud_provider | upper }}

Refer to the deployment documentation in `docs/deployment/{{ cookiecutter.cloud_provider }}.md`
{%- endif %}

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Workflow

1. Create a new branch from `develop`
2. Make your changes
3. Write/update tests
4. Run tests and linting
5. Commit with conventional commits
6. Push and create a pull request

### Commit Message Format

We use conventional commits:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes
- `refactor:` Code refactoring
- `test:` Test changes
- `chore:` Build process or auxiliary tool changes

## 📄 License

{% if cookiecutter.open_source_license != 'Not open source' -%}
This project is licensed under the {{ cookiecutter.open_source_license }} - see the [LICENSE](LICENSE) file for details.
{% else -%}
This project is proprietary and confidential.
{%- endif %}

## 👥 Authors

- **{{ cookiecutter.author_name }}** - *Initial work* - [{{ cookiecutter.author_email }}](mailto:{{ cookiecutter.author_email }})

## 🙏 Acknowledgments

- Built with [cookiecutter-djvue](https://github.com/yourusername/cookiecutter-djvue)
- Inspired by Django and Vue.js best practices
- Thanks to all contributors

## 📞 Support

For support, email {{ cookiecutter.author_email }} or open an issue in the repository.

## 🔗 Links

- **Frontend**: http://localhost:{{ cookiecutter.frontend_port }}
- **Backend API Status**: http://localhost:{{ cookiecutter.backend_port }}
- **API Root**: http://localhost:{{ cookiecutter.backend_port }}/api/
- **Admin Panel**: http://localhost:{{ cookiecutter.backend_port }}/admin
- **Health Check**: http://localhost:{{ cookiecutter.backend_port }}/api/health/
{% if cookiecutter.use_drf_spectacular == 'y' -%}
- **API Documentation**: http://localhost:{{ cookiecutter.backend_port }}/api/docs/
{%- endif %}
{% if cookiecutter.use_mailhog == 'y' -%}
- **Mail Server**: http://localhost:8025
{%- endif %}

---

Generated with ❤️ using [cookiecutter-djvue](https://github.com/yourusername/cookiecutter-djvue)