# Cookiecutter DjVue - Development Instructions

## Project Overview

This is a cookiecutter template that generates a full-stack web application with Django 5.1 backend and Vue.js 3 frontend. The template provides production-ready configuration with Docker, CI/CD, and best practices.

## Template Structure

```markdown
cookiecutter-djvue/
├── {{ cookiecutter.project_slug }}/    # Template directory
├── hooks/                               # Pre/post generation hooks
├── tests/                               # Template tests
├── cookiecutter.json                    # Template configuration
├── COOKIECUTTER_DJVUE.md               # Project planning document
├── CLAUDE.md                           # This file
└── README.md                           # User-facing documentation
```

## Development Commands

### Testing the Template

```bash
# Install cookiecutter
pip install cookiecutter pytest pytest-cookies

# Test template generation
pytest tests/

# Generate a test project
cookiecutter . --no-input

# Generate with custom values
cookiecutter . --overwrite-if-exists
```

### Template Development Workflow

```bash
# 1. Make changes to template files
# 2. Test generation locally
cookiecutter . --no-input --overwrite-if-exists

# 3. Navigate to generated project
cd my_django_vue_project

# 4. Test that generated project works
docker-compose up
# or
make dev

# 5. Run template tests
cd ../
pytest tests/
```

## Key Template Features to Implement

### Backend Template Structure

- Django 5.1 with async support
- Django REST Framework with JWT auth
- PostgreSQL + Redis configuration
- Celery setup (optional)
- pytest testing configuration
- Multi-environment settings
- Custom User model
- API documentation with drf-spectacular

### Frontend Template Structure

- Vue.js 3 with Composition API
- Vite build tool
- Pinia state management
- Vue Router
- Axios with interceptors
- TypeScript support (optional)
- Tailwind CSS or Bootstrap Vue 3
- Testing with Vitest and Playwright

### DevOps Templates

- Docker multi-stage builds
- docker-compose for development
- docker-compose.prod for production
- Nginx configuration
- GitHub Actions workflows
- Kubernetes manifests (optional)
- Makefile with common commands

## Template Variables (cookiecutter.json)

### Required Variables

- `project_name`: Human-readable project name
- `project_slug`: URL-safe project identifier
- `author_name`: Project author
- `author_email`: Author email
- `description`: Project description

### Optional Features

- `use_docker`: Include Docker configuration
- `use_celery`: Include Celery for async tasks
- `use_channels`: Include Django Channels
- `use_typescript`: TypeScript in frontend
- `css_framework`: CSS framework choice
- `database`: Database backend choice
- `cloud_provider`: Deployment target

## Implementation Tasks

### Phase 1: Core Structure

1. Create cookiecutter.json with all variables
2. Set up basic Django project template
3. Set up basic Vue.js project template
4. Create Docker configurations
5. Add Makefile with common commands

### Phase 2: Backend Features

1. Configure Django settings for multiple environments
2. Set up Django REST Framework
3. Add JWT authentication
4. Create custom User model
5. Add API documentation
6. Configure pytest and coverage

### Phase 3: Frontend Features

1. Set up Vue Router with auth guards
2. Configure Pinia stores
3. Create Axios service with interceptors
4. Add authentication components
5. Set up testing infrastructure
6. Configure build optimization

### Phase 4: DevOps & CI/CD

1. Create GitHub Actions workflows
2. Add pre-commit hooks
3. Configure security scanning
4. Set up deployment scripts
5. Add monitoring configuration

### Phase 5: Documentation & Testing

1. Create comprehensive README
2. Add API documentation
3. Write template tests
4. Create example application
5. Add troubleshooting guide

## File Naming Conventions

### Template Files

- Use `{{ cookiecutter.variable }}` for dynamic content
- Use `{% if cookiecutter.use_feature %}` for conditional content
- Prefix optional files with underscore if needed

### Generated Files

- Follow Python PEP 8 for Python files
- Follow Vue.js style guide for Vue files
- Use kebab-case for URLs and file names
- Use PascalCase for Vue components

## Testing Strategy

### Template Tests

```python
# tests/test_generation.py
def test_project_generation(cookies):
    result = cookies.bake(extra_context={'project_name': 'Test Project'})
    assert result.exit_code == 0
    assert result.exception is None

def test_docker_files_created(cookies):
    result = cookies.bake(extra_context={'use_docker': 'y'})
    assert result.exit_code == 0
    assert (result.project_path / 'docker-compose.yml').exists()
```

### Generated Project Tests

- Backend: pytest with coverage > 80%
- Frontend: Vitest unit tests + Playwright E2E
- Integration: Test API endpoints from frontend
- Performance: Load testing with Locust

## Common Patterns

### API Endpoint Structure

```markdown
/api/v1/
├── auth/          # Authentication endpoints
├── users/         # User management
├── [resource]/    # Resource CRUD
└── docs/          # API documentation
```

### Frontend Route Structure

```markdown
/                  # Public landing page
/auth/
├── login          # Login page
├── register       # Registration page
└── logout         # Logout handler
/dashboard         # Authenticated dashboard
/profile           # User profile
/admin             # Admin panel (if admin)
```

### State Management Pattern

```javascript
// stores/auth.js
export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const token = ref(null)
  const isAuthenticated = computed(() => !!token.value)
  
  const login = async (credentials) => { /* ... */ }
  const logout = async () => { /* ... */ }
  const refresh = async () => { /* ... */ }
  
  return { user, token, isAuthenticated, login, logout, refresh }
})
```

## Security Considerations

### Template Security

- Don't include real secrets in templates
- Use environment variables for sensitive data
- Include .env.example files
- Add security headers configuration
- Include CORS configuration

### Generated Project Security

- Automatic SECRET_KEY generation
- Secure default settings
- HTTPS enforcement in production
- Security scanning in CI/CD
- Dependency vulnerability checking

## Performance Optimization

### Backend Optimization

- Database query optimization helpers
- Redis caching configuration
- Pagination utilities
- Async view examples
- Database indexing guidelines

### Frontend Optimization

- Code splitting configuration
- Lazy loading setup
- Image optimization
- Bundle analysis tools
- CDN configuration

## Debugging Tips

### Template Debugging

```bash
# Test specific variable combinations
cookiecutter . --no-input use_docker=n use_celery=y

# Debug hooks
cookiecutter . --debug-file hooks/pre_gen_project.py

# Verbose output
cookiecutter . -v
```

### Generated Project Debugging

- Django Debug Toolbar included
- Vue DevTools configuration
- Comprehensive logging setup
- Error tracking with Sentry (optional)
- Performance profiling tools

## Release Process

### Version Management

1. Update version in cookiecutter.json
2. Update CHANGELOG.md
3. Tag release in git
4. Update documentation

### Testing Checklist

- [ ] Template generates without errors
- [ ] All conditional features work
- [ ] Generated project passes tests
- [ ] Docker builds successfully
- [ ] CI/CD pipelines work
- [ ] Documentation is complete

## Contributing Guidelines

### Code Style

- Python: Black + isort + flake8
- JavaScript: ESLint + Prettier
- Templates: Consistent indentation
- Documentation: Clear and concise

### Pull Request Process

1. Create feature branch
2. Add tests for new features
3. Update documentation
4. Run full test suite
5. Submit PR with description

## Resources

### References

- [Cookiecutter Documentation](https://cookiecutter.readthedocs.io/)
- [Django 5.1 Documentation](https://docs.djangoproject.com/en/5.1/)
- [Vue.js 3 Documentation](https://vuejs.org/)
- [Django REST Framework](https://www.django-rest-framework.org/)

### Similar Projects

- cookiecutter-django
- django-vue-template
- create-vue
- django-react-boilerplate

## Troubleshooting

### Common Issues

1. **Template generation fails**: Check Python version and cookiecutter version
2. **Docker build fails**: Ensure Docker daemon is running
3. **Frontend build fails**: Check Node.js version
4. **Database connection fails**: Verify PostgreSQL is running

### Getting Help

- GitHub Issues for bug reports
- Discussions for questions
- Stack Overflow for general Django/Vue questions

## Future Enhancements

### Planned Features

- GraphQL API option
- Microservices template variant
- Mobile app template (React Native/Flutter)
- AI/ML integration examples
- Advanced monitoring dashboards

### Community Requests

- Multi-language support
- Payment integration examples
- Social authentication
- Real-time features with WebSockets
- Advanced admin panel

## Notes for Development

### Current Focus

- Implementing core Django + Vue.js integration
- Setting up robust testing infrastructure
- Creating comprehensive documentation
- Ensuring production readiness

### Design Decisions

- Separate frontend/backend for scalability
- JWT for stateless authentication
- Docker-first approach for consistency
- Extensive use of environment variables
- Focus on developer experience
