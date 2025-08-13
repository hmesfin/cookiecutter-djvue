# Cookiecutter Django-Vue (DjVue) Template

## Project Overview

A production-ready cookiecutter template that combines Django 5.1 backend with Vue.js 3 frontend, providing a modern full-stack web application scaffold with best practices, Docker support, and CI/CD pipelines.

## Key Features

### Backend (Django 5.1)

- Django 5.1 with async support
- Django REST Framework for API development
- JWT authentication (djangorestframework-simplejwt)
- PostgreSQL as default database
- Redis for caching and Celery broker
- Celery for background tasks
- Django Channels for WebSocket support (optional)
- WhiteNoise for static files in production
- Comprehensive test setup with pytest
- API documentation with drf-spectacular
- Django Debug Toolbar for development
- Environment-based settings management
- Custom User model
- Django CORS headers configured
- Django Extensions for development
- Pre-commit hooks for code quality
- Ruff for fast Python linting and formatting

### Frontend (Vue.js 3)

- Vue.js 3 with Composition API
- Vite for fast development and building
- Pinia for state management
- Vue Router for navigation
- Axios for API communication
- TypeScript support (optional)
- Tailwind CSS or Bootstrap Vue 3 (choice)
- Vitest for unit testing
- Playwright for E2E testing
- ESLint and Prettier configured
- Auto-import components
- PWA support (optional)
- Dark mode support
- i18n internationalization ready

### DevOps & Infrastructure

- Docker and Docker Compose setup
- Multi-stage Dockerfile for optimized images
- Nginx configuration for production
- GitHub Actions CI/CD pipelines
- GitLab CI configuration (optional)
- Kubernetes manifests (optional)
- Terraform configuration for AWS/GCP deployment (optional)
- Health check endpoints
- Monitoring with Prometheus/Grafana (optional)
- Sentry error tracking integration

### Development Tools

- Pre-commit hooks for both Python and JavaScript
- Makefile for common commands
- Hot-reload for both backend and frontend
- VS Code configuration and recommended extensions
- EditorConfig for consistent coding styles
- Git hooks for commit message validation
- Dependabot configuration
- Security scanning with Bandit and Safety

## Project Structure

```markdown
{{ cookiecutter.project_slug }}/
├── backend/
│   ├── {{ cookiecutter.project_slug }}/
│   │   ├── settings/
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── development.py
│   │   │   ├── production.py
│   │   │   └── testing.py
│   │   ├── apps/
│   │   │   ├── core/           # Core functionality
│   │   │   ├── users/          # User management
│   │   │   └── api/            # API endpoints
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   ├── asgi.py
│   │   └── celery.py
│   ├── requirements/
│   │   ├── base.txt
│   │   ├── development.txt
│   │   ├── production.txt
│   │   └── testing.txt
│   ├── tests/
│   ├── static/
│   ├── media/
│   ├── manage.py
│   └── pytest.ini
├── frontend/
│   ├── src/
│   │   ├── assets/
│   │   ├── components/
│   │   ├── composables/
│   │   ├── layouts/
│   │   ├── pages/
│   │   ├── router/
│   │   ├── stores/
│   │   ├── services/
│   │   ├── utils/
│   │   ├── App.vue
│   │   └── main.ts
│   ├── public/
│   ├── tests/
│   │   ├── unit/
│   │   └── e2e/
│   ├── index.html
│   ├── vite.config.ts
│   ├── tsconfig.json
│   ├── package.json
│   └── .env.example
├── docker/
│   ├── backend/
│   │   └── Dockerfile
│   ├── frontend/
│   │   └── Dockerfile
│   └── nginx/
│       ├── Dockerfile
│       └── nginx.conf
├── .github/
│   ├── workflows/
│   │   ├── backend.yml
│   │   ├── frontend.yml
│   │   └── deploy.yml
│   └── dependabot.yml
├── scripts/
│   ├── setup.sh
│   ├── deploy.sh
│   └── backup.sh
├── docs/
│   ├── api/
│   ├── deployment/
│   └── development/
├── docker-compose.yml
├── docker-compose.prod.yml
├── .env.example
├── .gitignore
├── .pre-commit-config.yaml
├── Makefile
└── README.md
```

## Cookiecutter Variables

```json
{
  "project_name": "My Django Vue Project",
  "project_slug": "{{ cookiecutter.project_name|lower|replace(' ', '_')|replace('-', '_') }}",
  "description": "A Django + Vue.js project",
  "author_name": "Your Name",
  "author_email": "your.email@example.com",
  "domain_name": "example.com",
  "version": "0.1.0",
  "timezone": "UTC",
  "use_docker": "y",
  "use_celery": "y",
  "use_channels": "n",
  "use_typescript": "y",
  "css_framework": ["tailwindcss", "bootstrap-vue-3", "none"],
  "use_pwa": "n",
  "use_i18n": "y",
  "database": ["postgresql", "mysql", "sqlite"],
  "cloud_provider": ["aws", "gcp", "azure", "digitalocean", "none"],
  "use_sentry": "y",
  "use_mailhog": "y",
  "ci_tool": ["github", "gitlab", "none"],
  "python_version": "3.12",
  "node_version": "20",
  "django_version": "5.1",
  "vue_version": "3"
}
```

## Installation & Usage

### Prerequisites

- Python 3.8+
- Cookiecutter 2.0+
- Git

### Generate Project

```bash
# Install cookiecutter
pip install cookiecutter

# Generate from GitHub
cookiecutter https://github.com/yourusername/cookiecutter-djvue

# Or generate from local directory
cookiecutter /path/to/cookiecutter-djvue
```

### Post-Generation Setup

After generation, the project will have a setup script:

```bash
cd your_project_name
chmod +x scripts/setup.sh
./scripts/setup.sh
```

This will:

1. Create virtual environment
2. Install Python dependencies
3. Install Node dependencies
4. Set up pre-commit hooks
5. Initialize git repository
6. Create initial Django migrations
7. Build frontend assets
8. Start Docker containers (if Docker selected)

## Development Workflow

### Local Development

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements/development.txt
python manage.py migrate
python manage.py runserver

# Frontend (new terminal)
cd frontend
npm install
npm run dev
```

### Docker Development

```bash
# Start all services
docker-compose up

# Or run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Run Django commands
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser

# Run tests
docker-compose exec backend pytest
docker-compose exec frontend npm run test
```

### Makefile Commands

```bash
make help          # Show all available commands
make dev           # Start development environment
make test          # Run all tests
make lint          # Run linters
make format        # Format code
make build         # Build production images
make deploy        # Deploy to production
make clean         # Clean up generated files
```

## API Integration

### Authentication Flow

1. Frontend sends credentials to `/api/auth/login/`
2. Backend returns JWT access and refresh tokens
3. Frontend stores tokens securely
4. Frontend includes access token in API requests
5. Frontend refreshes token when expired

### API Structure

```markdown
/api/
├── auth/
│   ├── login/
│   ├── logout/
│   ├── refresh/
│   └── register/
├── users/
│   ├── profile/
│   └── me/
└── v1/
    └── [your endpoints]
```

## Testing Strategy

### Backend Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=backend --cov-report=html

# Run specific test
pytest tests/test_users.py::TestUserAPI::test_create_user
```

### Frontend Testing

```bash
# Unit tests
npm run test:unit

# E2E tests
npm run test:e2e

# All tests with coverage
npm run test:coverage
```

## Deployment

### Production Build

```bash
# Build with Docker
docker-compose -f docker-compose.prod.yml build

# Or build separately
cd backend && python manage.py collectstatic --noinput
cd frontend && npm run build
```

### Environment Variables

Required environment variables for production:

- `SECRET_KEY`
- `DATABASE_URL`
- `REDIS_URL`
- `ALLOWED_HOSTS`
- `CORS_ALLOWED_ORIGINS`
- `SENTRY_DSN` (if using Sentry)

### Deployment Options

1. **Docker Swarm**

```bash
docker stack deploy -c docker-compose.prod.yml myapp
```

2. **Kubernetes**

```bash
kubectl apply -f k8s/
```

3. **Traditional Server**

```bash
# Use deployment script
./scripts/deploy.sh production
```

## Security Considerations

### Built-in Security Features

- HTTPS enforcement in production
- CSRF protection
- XSS protection
- SQL injection prevention
- Secure password hashing
- Rate limiting on API endpoints
- Security headers configured
- Content Security Policy
- CORS properly configured

### Security Checklist

- [ ] Change default SECRET_KEY
- [ ] Configure ALLOWED_HOSTS
- [ ] Set up HTTPS certificates
- [ ] Configure firewall rules
- [ ] Enable database backups
- [ ] Set up monitoring and alerting
- [ ] Review and update dependencies regularly
- [ ] Configure rate limiting
- [ ] Set up WAF if needed

## Performance Optimization

### Backend Optimization

- Database query optimization with select_related/prefetch_related
- Redis caching for frequently accessed data
- Database indexing on common query fields
- Pagination on list endpoints
- Async views where appropriate
- Connection pooling

### Frontend Optimization

- Code splitting and lazy loading
- Image optimization and lazy loading
- Bundle size optimization
- Service Worker for caching
- CDN for static assets
- Compression (gzip/brotli)

## Monitoring & Logging

### Application Monitoring

- Health check endpoints
- Prometheus metrics endpoint
- Application Performance Monitoring with Sentry
- Custom Django admin dashboard

### Logging Configuration

- Structured JSON logging
- Log aggregation ready
- Different log levels per environment
- Automatic error reporting to Sentry

## Contributing to Template

### Development Setup

```bash
git clone https://github.com/yourusername/cookiecutter-djvue
cd cookiecutter-djvue
pip install -r requirements-dev.txt
pre-commit install
```

### Testing Template

```bash
# Test generation
pytest tests/

# Test generated project
./test_generation.sh
```

### Submitting Changes

1. Fork the repository
2. Create feature branch
3. Make changes with tests
4. Run pre-commit checks
5. Submit pull request

## Roadmap

### Version 1.0

- [x] Basic Django + Vue.js integration
- [x] Docker support
- [x] JWT authentication
- [x] Basic CI/CD pipelines
- [x] Production-ready configuration

### Version 1.1 (Planned)

- [ ] GraphQL API option
- [ ] Social authentication
- [ ] Email templates
- [ ] Advanced caching strategies
- [ ] WebSocket support improvements

### Version 2.0 (Future)

- [ ] Microservices architecture option
- [ ] Multi-tenant support
- [ ] Advanced monitoring dashboard
- [ ] Automated performance testing
- [ ] AI/ML integration templates

## License

This cookiecutter template is licensed under the MIT License.

## Acknowledgments

Inspired by:

- [cookiecutter-django](https://github.com/cookiecutter/cookiecutter-django)
- [django-vue-template](https://github.com/gtalarico/django-vue-template)
- Django and Vue.js communities

## Support

- Documentation: [Link to full docs]
- Issues: [GitHub Issues]
- Discussions: [GitHub Discussions]
- Chat: [Discord/Slack]
