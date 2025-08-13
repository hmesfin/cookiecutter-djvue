# Cookiecutter DjVue

A modern, production-ready [Cookiecutter](https://github.com/cookiecutter/cookiecutter) template for building full-stack web applications with Django 5.1 and Vue.js 3.

## ✨ Features

### Backend (Django 5.1)

- **Modern Django Setup**: Latest Django 5.1 with async support
- **RESTful API**: Django REST Framework with customizable authentication (JWT/Token/Session)
- **Custom User Model**: Email-based authentication with flexible UserManager
- **Smart Email System**: Works with or without Celery, automatic fallback
- **Code Quality**: Ruff for fast Python linting and formatting
- **Testing**: Pytest or Django test framework
- **Database Support**: PostgreSQL, MySQL, or SQLite
- **Background Tasks**: Optional Celery integration
- **Caching**: Optional Redis support
- **WebSockets**: Optional Django Channels
- **API Documentation**: Optional drf-spectacular for OpenAPI

### Frontend (Vue.js 3)

- **Vue 3 Composition API**: Modern Vue.js with script setup syntax
- **Modular Architecture**: Organized with layouts and feature modules
- **State Management**: Pinia stores
- **Routing**: Vue Router with auth guards
- **Build Tool**: Vite for fast development
- **TypeScript**: Optional TypeScript support
- **CSS Frameworks**: Tailwind CSS, Bootstrap-Vue-3, or custom CSS
- **Code Quality**: ESLint and Prettier
- **Testing**: Vitest for unit tests

### DevOps & Tooling

- **Docker**: Multi-stage Dockerfiles and docker-compose
- **CI/CD**: GitHub Actions or GitLab CI pipelines
- **Pre-commit Hooks**: Automated code quality checks
- **Environment Management**: Separate settings for dev/staging/production
- **Hot Reload**: Both backend and frontend
- **Makefile**: Common commands for easy development

## 🚀 Quick Start

### Prerequisites

Choose one approach:

**Docker Approach (Recommended):**
- Docker 20.10+
- Docker Compose 2.0+
- Cookiecutter 2.0+

**Local Development Approach:**
- Python 3.8+
- Node.js 18+
- PostgreSQL/MySQL (if selected)
- Redis (if selected)
- Cookiecutter 2.0+

### Installation

1. Install Cookiecutter:

```bash
pip install cookiecutter
```

2. Generate your project:

```bash
cookiecutter https://github.com/hmesfin/cookiecutter-djvue
```

3. Answer the prompts:

```markdown
project_name [My Project]: Your Amazing App
project_slug [your_amazing_app]: 
author_name [Your Name]: John Doe
author_email [your.email@example.com]: john@example.com
use_docker [y]: y  # Recommended!
database [postgresql]: postgresql
...
```

4. Navigate to your project:

```bash
cd your_amazing_app
```

5. Start developing:

```bash
# Using Docker (Recommended) - Everything runs automatically!
docker-compose up

# Or using Make
make dev

# Access your application at:
# Frontend: http://localhost:5173
# Backend API: http://localhost:8000/api
# Admin: http://localhost:8000/admin (admin@example.com / admin123)
```

### Docker-First Development

This template is designed to work seamlessly with Docker:

1. **Database Setup**: PostgreSQL/MySQL automatically starts in Docker
2. **Auto-Migrations**: Database migrations run automatically on startup
3. **Hot Reload**: Both frontend and backend support hot reloading
4. **Zero Config**: No manual database or environment setup needed

### Local Development (Advanced)

If you prefer local development without Docker:

1. Set up your database (PostgreSQL/MySQL)
2. Create a Python virtual environment:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements/development.txt
   ```
3. Configure your database in `backend/.env`
4. Run migrations: `python manage.py migrate`
5. Install frontend dependencies:
   ```bash
   cd frontend
   npm install
   ```
6. Start both servers in separate terminals

## 📦 What You Get

```markdown
your_project/
├── backend/                 # Django backend
│   ├── your_project/       # Main Django project
│   │   ├── apps/           # Django applications
│   │   │   ├── core/       # Core functionality
│   │   │   ├── users/      # User management with custom model
│   │   │   └── api/        # API endpoints
│   │   └── settings/       # Environment-specific settings
│   ├── requirements/        # Python dependencies
│   └── tests/              # Backend tests
├── frontend/               # Vue.js frontend
│   ├── src/
│   │   ├── modules/        # Feature modules
│   │   │   ├── auth/       # Authentication module
│   │   │   ├── dashboard/  # Dashboard module
│   │   │   └── home/       # Public pages module
│   │   ├── layouts/        # Layout components
│   │   ├── stores/         # Pinia stores
│   │   └── services/       # API services
│   └── tests/              # Frontend tests
├── docker/                 # Docker configurations
├── scripts/                # Utility scripts
├── .github/workflows/      # CI/CD pipelines
└── docker-compose.yml      # Development environment
```

## 🛠️ Configuration Options

### Required

- **project_name**: Human-readable project name
- **project_slug**: Python/directory-friendly name
- **author_name**: Your name
- **author_email**: Your email

### Optional Features

- **database**: PostgreSQL, MySQL, or SQLite
- **api_authentication**: JWT, Token, or Session
- **use_celery**: Background task processing
- **use_redis**: Caching layer
- **use_docker**: Containerization
- **css_framework**: Tailwind CSS, Bootstrap-Vue-3, or none
- **use_typescript**: TypeScript for frontend
- **ci_tool**: GitHub Actions or GitLab CI

## 📚 Documentation

After generating your project, you'll find:

- `README.md` - Project-specific documentation
- `docs/` - Additional documentation
- API documentation at `http://localhost:8000/api/docs/` (if enabled)

## 🧪 Testing

The template includes comprehensive test setups:

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm run test:unit
npm run test:e2e

# Or use Make
make test
```

## 🎯 Key Features Explained

### Custom User Model with Manager

The template includes a sophisticated User model with email-based authentication and a custom UserManager that:

- Automatically generates usernames from emails
- Sends welcome emails (with or without Celery)
- Includes user profile fields
- Supports social authentication preparation

### Flexible Email System

Smart email task system that:

- Works with Celery when available
- Falls back to synchronous sending
- Includes beautiful HTML email templates
- Configurable via environment variables

### Modular Frontend Architecture

The Vue.js frontend uses a modular structure:

- **Layouts**: Consistent page structures (Auth, Dashboard, Main)
- **Modules**: Feature-based organization
- **Lazy Loading**: Optimal performance
- **Type Safety**: Optional TypeScript support

### Production-Ready Settings

- Separate settings for different environments
- Security best practices implemented
- Performance optimizations included
- Monitoring and logging configured

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by [cookiecutter-django](https://github.com/cookiecutter/cookiecutter-django)
- Built with modern Django and Vue.js best practices
- Community feedback and contributions

## 🔗 Links

- [Django Documentation](https://docs.djangoproject.com/)
- [Vue.js Documentation](https://vuejs.org/)
- [Cookiecutter Documentation](https://cookiecutter.readthedocs.io/)

---

Made with ❤️ for the Django + Vue.js community
