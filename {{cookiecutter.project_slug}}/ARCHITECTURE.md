# {{ cookiecutter.project_name }} - System Architecture

## Table of Contents
- [Overview](#overview)
- [System Architecture](#system-architecture)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Backend Architecture](#backend-architecture)
- [Frontend Architecture](#frontend-architecture)
- [Data Flow](#data-flow)
- [Security Architecture](#security-architecture)
- [Deployment Architecture](#deployment-architecture)
- [Scalability Considerations](#scalability-considerations)

## Overview

{{ cookiecutter.project_name }} is a modern full-stack web application built with Django REST Framework and Vue.js. The architecture follows a clean separation of concerns with a RESTful API backend and a reactive SPA frontend.

## System Architecture

```mermaid
graph TB
    subgraph "Client Layer"
        Browser[Web Browser]
        Mobile[Mobile App]
    end
    
    subgraph "CDN Layer"
        CloudFlare[CDN/CloudFlare]
    end
    
    subgraph "Application Layer"
        Nginx[Nginx Reverse Proxy]
        Frontend[Vue.js SPA]
        Backend[Django REST API]
        {% if cookiecutter.use_graphql == 'y' -%}
        GraphQL[GraphQL API]
        {%- endif %}
        {% if cookiecutter.use_channels == 'y' -%}
        WebSocket[WebSocket Server]
        {%- endif %}
    end
    
    subgraph "Services Layer"
        {% if cookiecutter.use_redis == 'y' -%}
        Redis[(Redis Cache)]
        {%- endif %}
        {% if cookiecutter.use_celery == 'y' -%}
        Celery[Celery Workers]
        {%- endif %}
        {% if cookiecutter.database == 'postgresql' -%}
        PostgreSQL[(PostgreSQL)]
        {% elif cookiecutter.database == 'mysql' -%}
        MySQL[(MySQL)]
        {% else -%}
        SQLite[(SQLite)]
        {%- endif %}
    end
    
    subgraph "External Services"
        {% if cookiecutter.use_social_auth == 'y' -%}
        OAuth[OAuth Providers]
        {%- endif %}
        Email[Email Service]
        {% if cookiecutter.cloud_provider != 'none' -%}
        Storage[Cloud Storage]
        {%- endif %}
    end
    
    Browser --> CloudFlare
    Mobile --> CloudFlare
    CloudFlare --> Nginx
    Nginx --> Frontend
    Nginx --> Backend
    {% if cookiecutter.use_graphql == 'y' -%}
    Backend --> GraphQL
    {%- endif %}
    {% if cookiecutter.use_channels == 'y' -%}
    Nginx --> WebSocket
    {%- endif %}
    {% if cookiecutter.database == 'postgresql' -%}
    Backend --> PostgreSQL
    {% elif cookiecutter.database == 'mysql' -%}
    Backend --> MySQL
    {% else -%}
    Backend --> SQLite
    {%- endif %}
    {% if cookiecutter.use_redis == 'y' -%}
    Backend --> Redis
    {%- endif %}
    {% if cookiecutter.use_celery == 'y' -%}
    Backend --> Celery
    Celery --> Redis
    {%- endif %}
    {% if cookiecutter.use_social_auth == 'y' -%}
    Backend --> OAuth
    {%- endif %}
    Backend --> Email
    {% if cookiecutter.cloud_provider != 'none' -%}
    Backend --> Storage
    {%- endif %}
```

## Technology Stack

### Backend
- **Framework**: Django {{ cookiecutter.django_version }}
- **API**: Django REST Framework 3.16
{% if cookiecutter.use_graphql == 'y' -%}
- **GraphQL**: Strawberry GraphQL
{%- endif %}
- **Database**: {% if cookiecutter.database == 'postgresql' %}PostgreSQL{% elif cookiecutter.database == 'mysql' %}MySQL{% else %}SQLite{% endif %}
{% if cookiecutter.use_redis == 'y' -%}
- **Cache**: Redis
{%- endif %}
{% if cookiecutter.use_celery == 'y' -%}
- **Task Queue**: Celery
{%- endif %}
{% if cookiecutter.use_channels == 'y' -%}
- **WebSockets**: Django Channels
{%- endif %}
- **Authentication**: {% if cookiecutter.api_authentication == 'jwt' %}JWT (djangorestframework-simplejwt){% elif cookiecutter.api_authentication == 'token' %}Token Authentication{% else %}Session Authentication{% endif %}

### Frontend
- **Framework**: Vue.js 3
- **Build Tool**: Vite
- **State Management**: Pinia
- **Router**: Vue Router 4
- **HTTP Client**: Axios
- **CSS Framework**: {% if cookiecutter.css_framework == 'tailwind' %}Tailwind CSS{% elif cookiecutter.css_framework == 'bootstrap' %}Bootstrap 5{% else %}Custom CSS{% endif %}
{% if cookiecutter.use_typescript == 'y' -%}
- **Language**: TypeScript
{%- endif %}

### DevOps & Infrastructure
{% if cookiecutter.use_docker == 'y' -%}
- **Containerization**: Docker & Docker Compose
{%- endif %}
- **Web Server**: Nginx
- **Process Manager**: Gunicorn/Uvicorn
{% if cookiecutter.cloud_provider == 'aws' -%}
- **Cloud Provider**: AWS
{% elif cookiecutter.cloud_provider == 'gcp' -%}
- **Cloud Provider**: Google Cloud Platform
{% elif cookiecutter.cloud_provider == 'azure' -%}
- **Cloud Provider**: Microsoft Azure
{%- endif %}
- **CI/CD**: GitHub Actions / GitLab CI

## Project Structure

```
{{ cookiecutter.project_slug }}/
├── backend/                  # Django backend application
│   ├── apps/                # Django applications
│   │   ├── core/           # Core functionality
│   │   ├── users/         # User management
│   │   ├── api/           # API endpoints
│   │   {% if cookiecutter.use_graphql == 'y' -%}
│   │   ├── graphql/       # GraphQL schema
│   │   {%- endif %}
│   │   {% if cookiecutter.use_channels == 'y' -%}
│   │   ├── websockets/    # WebSocket consumers
│   │   {%- endif %}
│   │   └── ...
│   ├── config/             # Django settings
│   │   ├── settings/       # Environment-specific settings
│   │   ├── urls.py        # URL configuration
│   │   └── wsgi.py        # WSGI configuration
│   ├── requirements/       # Python dependencies
│   ├── static/            # Static files
│   ├── media/             # User uploads
│   └── manage.py          # Django management script
│
├── frontend/               # Vue.js frontend application
│   ├── src/
│   │   ├── assets/        # Static assets
│   │   ├── components/    # Vue components
│   │   ├── composables/   # Vue composables
│   │   ├── layouts/       # Layout components
│   │   ├── pages/         # Page components
│   │   ├── router/        # Vue Router configuration
│   │   ├── services/      # API services
│   │   ├── stores/        # Pinia stores
│   │   ├── types/         # TypeScript types
│   │   ├── utils/         # Utility functions
│   │   └── main.ts        # Application entry point
│   ├── public/            # Public assets
│   └── package.json       # Node.js dependencies
│
├── docker/                 # Docker configuration
│   ├── backend/           # Backend Dockerfile
│   ├── frontend/          # Frontend Dockerfile
│   └── nginx/             # Nginx configuration
│
├── scripts/               # Utility scripts
├── docs/                  # Documentation
├── tests/                 # Test suites
├── .github/              # GitHub Actions workflows
├── docker-compose.yml    # Docker Compose configuration
├── Makefile             # Development commands
└── README.md            # Project documentation
```

## Backend Architecture

### Django Applications

The backend follows Django's app-based architecture:

1. **Core App** (`apps.core`)
   - Base models and mixins
   - Common utilities
   - Middleware
   - Permissions

2. **Users App** (`apps.users`)
   - Custom User model
   - Authentication views
   - User profile management
   - Social authentication

3. **API App** (`apps.api`)
   - REST API endpoints
   - Serializers
   - ViewSets
   - API documentation

{% if cookiecutter.use_graphql == 'y' -%}
4. **GraphQL App** (`apps.graphql`)
   - GraphQL schema
   - Types and mutations
   - Resolvers
   - Subscriptions
{%- endif %}

### API Design

The API follows RESTful principles:

- **Versioning**: URL-based (`/api/v1/`)
- **Authentication**: {% if cookiecutter.api_authentication == 'jwt' %}JWT tokens{% elif cookiecutter.api_authentication == 'token' %}Token-based{% else %}Session-based{% endif %}
- **Pagination**: Page number pagination
- **Filtering**: Query parameter filtering
- **Sorting**: Ordering by fields
- **Response Format**: JSON

Example API endpoints:
```
GET    /api/v1/users/           # List users
POST   /api/v1/users/           # Create user
GET    /api/v1/users/{id}/      # Get user
PUT    /api/v1/users/{id}/      # Update user
DELETE /api/v1/users/{id}/      # Delete user
```

{% if cookiecutter.use_graphql == 'y' -%}
### GraphQL Schema

The GraphQL API provides:
- Type-safe queries and mutations
- Nested data fetching
- Real-time subscriptions
- Schema introspection

Example GraphQL query:
```graphql
query GetUser($id: ID!) {
  user(id: $id) {
    id
    email
    username
    profile {
      firstName
      lastName
    }
  }
}
```
{%- endif %}

## Frontend Architecture

### Component Structure

The frontend follows a component-based architecture:

1. **Pages**: Route-level components
2. **Layouts**: Shared layout wrappers
3. **Components**: Reusable UI components
4. **Composables**: Shared logic hooks

### State Management

Pinia stores manage application state:

- **Auth Store**: User authentication state
- **User Store**: Current user data
- **UI Store**: UI preferences and state
{% if cookiecutter.use_redis == 'y' -%}
- **Cache Store**: Client-side caching
{%- endif %}

### Routing

Vue Router handles client-side routing:

- **Public Routes**: Accessible without authentication
- **Protected Routes**: Require authentication
- **Admin Routes**: Require admin privileges
- **Navigation Guards**: Route protection logic

## Data Flow

### Request Flow

1. User interacts with Vue.js frontend
2. Frontend makes API request via Axios
3. Request passes through Nginx reverse proxy
4. Django middleware processes request
5. View/ViewSet handles business logic
6. Database query executed
7. Response serialized to JSON
8. Response returned to frontend
9. Frontend updates UI

### Authentication Flow

{% if cookiecutter.api_authentication == 'jwt' -%}
1. User submits credentials
2. Backend validates credentials
3. JWT token generated
4. Token stored in localStorage/cookie
5. Token included in API headers
6. Backend validates token on each request
{% elif cookiecutter.api_authentication == 'token' -%}
1. User submits credentials
2. Backend validates credentials
3. Token created/retrieved
4. Token stored in localStorage
5. Token included in API headers
6. Backend validates token on each request
{% else -%}
1. User submits credentials
2. Backend validates credentials
3. Session created on server
4. Session cookie sent to browser
5. Cookie included in requests
6. Backend validates session
{%- endif %}

{% if cookiecutter.use_channels == 'y' -%}
### WebSocket Flow

1. Client establishes WebSocket connection
2. Connection authenticated via token
3. Client subscribes to channels
4. Server pushes real-time updates
5. Client receives and processes updates
{%- endif %}

## Security Architecture

### Security Measures

1. **Authentication & Authorization**
   - {% if cookiecutter.api_authentication == 'jwt' %}JWT token authentication{% elif cookiecutter.api_authentication == 'token' %}Token authentication{% else %}Session authentication{% endif %}
   - Role-based access control (RBAC)
   - Permission-based authorization

2. **Data Protection**
   - HTTPS enforcement
   - CORS configuration
   - CSRF protection
   - XSS prevention
   - SQL injection protection (ORM)

3. **Input Validation**
   - Backend validation (serializers)
   - Frontend validation (forms)
   - File upload restrictions

4. **Rate Limiting**
   - API throttling
   - Login attempt limits
   - Request rate limits

5. **Security Headers**
   - Content Security Policy
   - X-Frame-Options
   - X-Content-Type-Options
   - Strict-Transport-Security

## Deployment Architecture

### Development Environment

```yaml
Services:
  - Backend: Django development server (port 8000)
  - Frontend: Vite dev server (port {{ cookiecutter.frontend_port }})
  {% if cookiecutter.database == 'postgresql' -%}
  - Database: PostgreSQL (port 5432)
  {% elif cookiecutter.database == 'mysql' -%}
  - Database: MySQL (port 3306)
  {%- endif %}
  {% if cookiecutter.use_redis == 'y' -%}
  - Cache: Redis (port 6379)
  {%- endif %}
```

### Production Environment

```yaml
Load Balancer:
  - SSL termination
  - Request distribution

Web Servers (Multiple Instances):
  - Nginx: Static files, reverse proxy
  - Gunicorn: Django application
  - Node.js: SSR (if applicable)

Application Servers:
  - Django: API endpoints
  {% if cookiecutter.use_celery == 'y' -%}
  - Celery: Background tasks
  {%- endif %}
  {% if cookiecutter.use_channels == 'y' -%}
  - Daphne: WebSocket connections
  {%- endif %}

Data Layer:
  {% if cookiecutter.database == 'postgresql' -%}
  - PostgreSQL: Primary database
  - Read replicas: Query distribution
  {% elif cookiecutter.database == 'mysql' -%}
  - MySQL: Primary database
  - Read replicas: Query distribution
  {%- endif %}
  {% if cookiecutter.use_redis == 'y' -%}
  - Redis: Cache & sessions
  {%- endif %}

Storage:
  - Static files: CDN
  - Media files: Cloud storage
```

## Scalability Considerations

### Horizontal Scaling

1. **Application Layer**
   - Multiple Django instances
   - Load balancer distribution
   - Sticky sessions (if needed)

2. **Database Layer**
   - Read replicas
   - Connection pooling
   - Query optimization

3. **Caching Strategy**
   {% if cookiecutter.use_redis == 'y' -%}
   - Redis for session storage
   - Query result caching
   - API response caching
   {% else -%}
   - Database query caching
   - HTTP caching headers
   {%- endif %}
   - CDN for static assets

### Performance Optimization

1. **Backend**
   - Database indexing
   - Query optimization (select_related, prefetch_related)
   - Async views (Django 5.x)
   {% if cookiecutter.use_celery == 'y' -%}
   - Background task processing
   {%- endif %}

2. **Frontend**
   - Code splitting
   - Lazy loading
   - Image optimization
   - Bundle optimization

3. **API**
   - Pagination
   - Field filtering
   - Response compression
   {% if cookiecutter.use_graphql == 'y' -%}
   - GraphQL query depth limiting
   {%- endif %}

### Monitoring & Observability

1. **Application Monitoring**
   - Error tracking (Sentry)
   - Performance monitoring
   - Custom metrics

2. **Infrastructure Monitoring**
   - Server metrics
   - Database performance
   - Cache hit rates

3. **Logging**
   - Centralized logging
   - Log aggregation
   - Log analysis

## Development Workflow

### Local Development

1. Clone repository
2. Set up environment variables
3. Install dependencies
4. Run migrations
5. Start development servers
6. Access application

### Testing Strategy

1. **Backend Tests**
   - Unit tests (models, utils)
   - Integration tests (views, APIs)
   - Performance tests

2. **Frontend Tests**
   - Component tests
   - E2E tests
   - Visual regression tests

### CI/CD Pipeline

1. **Continuous Integration**
   - Code linting
   - Test execution
   - Security scanning
   - Build verification

2. **Continuous Deployment**
   - Staging deployment
   - Production deployment
   - Database migrations
   - Cache invalidation

## Future Considerations

### Potential Enhancements

1. **Microservices Architecture**
   - Service decomposition
   - API Gateway
   - Service mesh

2. **Event-Driven Architecture**
   - Message queuing
   - Event sourcing
   - CQRS pattern

3. **Advanced Features**
   - Machine learning integration
   - Real-time analytics
   - Multi-tenancy support

### Technology Upgrades

- Progressive Web App (PWA)
- Server-Side Rendering (SSR)
- GraphQL Federation
- Kubernetes orchestration

## Resources

### Documentation
- [Django Documentation](https://docs.djangoproject.com/)
- [Vue.js Documentation](https://vuejs.org/)
- [Django REST Framework](https://www.django-rest-framework.org/)
{% if cookiecutter.use_graphql == 'y' -%}
- [Strawberry GraphQL](https://strawberry.rocks/)
{%- endif %}

### Tools
- [Django Debug Toolbar](https://django-debug-toolbar.readthedocs.io/)
- [Vue DevTools](https://devtools.vuejs.org/)
- [Postman](https://www.postman.com/) - API testing
- [Redis Commander](https://github.com/joeferner/redis-commander) - Redis GUI