# Production Deployment Guide for {{ cookiecutter.project_name }}

This guide covers deploying {{ cookiecutter.project_name }} to production environments.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Environment Setup](#environment-setup)
3. [Security Checklist](#security-checklist)
4. [Deployment Methods](#deployment-methods)
5. [Post-Deployment](#post-deployment)
6. [Monitoring & Maintenance](#monitoring--maintenance)
7. [Troubleshooting](#troubleshooting)

## Prerequisites

### Required Tools
- Docker & Docker Compose (v2.0+)
- Git
- SSL certificates for your domain
- Access to your deployment infrastructure

### Infrastructure Requirements
- **Minimum Server Requirements:**
  - 2 CPU cores
  - 4GB RAM
  - 20GB storage
  - Ubuntu 22.04 LTS or similar

- **Recommended Production Setup:**
  - 4+ CPU cores
  - 8GB+ RAM
  - 50GB+ SSD storage
  - Load balancer for high availability
  - Managed database service
  - Object storage for media files (S3, GCS, etc.)
  - CDN for static assets

## Environment Setup

### 1. Create Production Environment File

Copy the example environment file and configure for production:

```bash
cp backend/.env.example .env.production
```

### 2. Required Environment Variables

Edit `.env.production` with your production values:

```bash
# Django Settings
SECRET_KEY=<generate-strong-secret-key>  # Use: python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
DEBUG=False
DJANGO_ENV=production
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database
{% if cookiecutter.database == 'postgresql' -%}
DATABASE_URL=postgres://user:password@db-host:5432/dbname
POSTGRES_PASSWORD=<strong-password>
{% elif cookiecutter.database == 'mysql' -%}
DATABASE_URL=mysql://user:password@db-host:3306/dbname
MYSQL_ROOT_PASSWORD=<strong-root-password>
MYSQL_PASSWORD=<strong-password>
{% else -%}
# For production, consider using PostgreSQL or MySQL instead of SQLite
DATABASE_URL=postgres://user:password@db-host:5432/dbname
{%- endif %}

{% if cookiecutter.use_redis == 'y' -%}
# Redis
REDIS_URL=redis://:password@redis-host:6379/0
{%- endif %}

{% if cookiecutter.use_celery == 'y' -%}
# Celery
CELERY_BROKER_URL=redis://:password@redis-host:6379/0
CELERY_RESULT_BACKEND=redis://:password@redis-host:6379/0
{%- endif %}

# CORS
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Email Configuration
EMAIL_HOST=smtp.your-email-provider.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=<email-password>
DEFAULT_FROM_EMAIL=noreply@yourdomain.com

# Frontend
FRONTEND_URL=https://yourdomain.com

{% if cookiecutter.use_sentry == 'y' -%}
# Sentry (Error Tracking)
SENTRY_DSN=https://xxxx@sentry.io/yyyy
{%- endif %}

# Admin
ADMIN_NAME=Admin Name
ADMIN_EMAIL=admin@yourdomain.com

# Security
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

### 3. Frontend Environment Variables

Create `frontend/.env.production`:

```bash
VITE_API_URL=https://yourdomain.com/api
VITE_APP_NAME={{ cookiecutter.project_name }}
VITE_APP_URL=https://yourdomain.com
```

## Security Checklist

Before deploying to production, ensure:

- [ ] **Secret Key**: Generate a new, strong SECRET_KEY
- [ ] **Debug Mode**: Ensure DEBUG=False
- [ ] **Allowed Hosts**: Configure ALLOWED_HOSTS properly
- [ ] **HTTPS**: SSL certificates are installed and configured
- [ ] **Database**: Use strong passwords and secure connections
- [ ] **CORS**: Configure CORS_ALLOWED_ORIGINS restrictively
- [ ] **File Permissions**: Ensure proper file permissions (especially for .env files)
- [ ] **Firewall**: Configure firewall rules (allow only necessary ports)
- [ ] **Updates**: All dependencies are up to date
- [ ] **Backups**: Database backup strategy is in place
- [ ] **Monitoring**: Error tracking and monitoring are configured
- [ ] **Rate Limiting**: API rate limiting is configured
- [ ] **Content Security Policy**: CSP headers are configured in nginx

## Deployment Methods

### Option 1: Docker Compose Deployment

#### 1. Prepare the Server

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo apt install docker-compose-plugin

# Add user to docker group
sudo usermod -aG docker $USER
```

#### 2. Clone and Configure

```bash
# Clone repository
git clone https://github.com/yourusername/{{ cookiecutter.project_slug }}.git
cd {{ cookiecutter.project_slug }}

# Copy production environment file
cp .env.production .env

# Build and start services
docker compose -f docker-compose.prod.yml up -d --build
```

#### 3. Initial Setup

```bash
# Run database migrations
docker compose -f docker-compose.prod.yml exec backend python manage.py migrate

# Create superuser
docker compose -f docker-compose.prod.yml exec backend python manage.py createsuperuser

# Collect static files
docker compose -f docker-compose.prod.yml exec backend python manage.py collectstatic --noinput
```

### Option 2: Kubernetes Deployment

For Kubernetes deployment, create the following manifests:

#### `k8s/deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ cookiecutter.project_slug }}-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: {{ cookiecutter.project_slug }}-backend
  template:
    metadata:
      labels:
        app: {{ cookiecutter.project_slug }}-backend
    spec:
      containers:
      - name: backend
        image: your-registry/{{ cookiecutter.project_slug }}-backend:latest
        envFrom:
        - secretRef:
            name: {{ cookiecutter.project_slug }}-secrets
        - configMapRef:
            name: {{ cookiecutter.project_slug }}-config
        ports:
        - containerPort: 8000
        livenessProbe:
          httpGet:
            path: /api/health/
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /api/health/
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ cookiecutter.project_slug }}-frontend
spec:
  replicas: 2
  selector:
    matchLabels:
      app: {{ cookiecutter.project_slug }}-frontend
  template:
    metadata:
      labels:
        app: {{ cookiecutter.project_slug }}-frontend
    spec:
      containers:
      - name: frontend
        image: your-registry/{{ cookiecutter.project_slug }}-frontend:latest
        ports:
        - containerPort: 80
```

### Option 3: Platform-as-a-Service Deployment

#### Heroku

```bash
# Install Heroku CLI
# Create Heroku app
heroku create {{ cookiecutter.project_slug }}

# Add PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Set environment variables
heroku config:set SECRET_KEY="your-secret-key"
heroku config:set DJANGO_ENV=production
heroku config:set ALLOWED_HOSTS=your-app.herokuapp.com

# Deploy
git push heroku main

# Run migrations
heroku run python manage.py migrate
```

#### DigitalOcean App Platform

1. Connect your GitHub repository
2. Configure environment variables in the App Platform dashboard
3. Set build commands:
   - Backend: `pip install -r requirements/production.txt`
   - Frontend: `npm ci && npm run build`
4. Set run commands:
   - Backend: `gunicorn {{ cookiecutter.project_slug }}.wsgi:application`
   - Frontend: Serve static files

### Option 4: Traditional Server Deployment

#### 1. Install Dependencies

```bash
# Python and Node.js
sudo apt install python{{ cookiecutter.python_version }} python3-pip nodejs npm

# PostgreSQL
sudo apt install postgresql postgresql-contrib

# Nginx
sudo apt install nginx

# Redis (if using)
sudo apt install redis-server
```

#### 2. Setup Application

```bash
# Create application directory
sudo mkdir -p /var/www/{{ cookiecutter.project_slug }}
cd /var/www/{{ cookiecutter.project_slug }}

# Clone repository
sudo git clone https://github.com/yourusername/{{ cookiecutter.project_slug }}.git .

# Setup Python virtual environment
python -m venv venv
source venv/bin/activate
pip install -r backend/requirements/production.txt

# Setup frontend
cd frontend
npm ci
npm run build
cd ..

# Setup database
sudo -u postgres createdb {{ cookiecutter.project_slug }}
sudo -u postgres createuser {{ cookiecutter.project_slug }}

# Run migrations
python backend/manage.py migrate
python backend/manage.py collectstatic --noinput
```

#### 3. Configure Nginx

Create `/etc/nginx/sites-available/{{ cookiecutter.project_slug }}`:

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline';" always;

    # Frontend
    location / {
        root /var/www/{{ cookiecutter.project_slug }}/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # API
    location /api {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Admin
    location /admin {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Static files
    location /static {
        alias /var/www/{{ cookiecutter.project_slug }}/backend/staticfiles;
    }

    # Media files
    location /media {
        alias /var/www/{{ cookiecutter.project_slug }}/backend/media;
    }

    # Gzip
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;
}
```

#### 4. Setup Systemd Service

Create `/etc/systemd/system/{{ cookiecutter.project_slug }}.service`:

```ini
[Unit]
Description={{ cookiecutter.project_name }} Django Application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/{{ cookiecutter.project_slug }}/backend
Environment="PATH=/var/www/{{ cookiecutter.project_slug }}/venv/bin"
EnvironmentFile=/var/www/{{ cookiecutter.project_slug }}/.env.production
ExecStart=/var/www/{{ cookiecutter.project_slug }}/venv/bin/gunicorn \
          --workers 3 \
          --bind 127.0.0.1:8000 \
          --error-logfile /var/log/{{ cookiecutter.project_slug }}/error.log \
          --access-logfile /var/log/{{ cookiecutter.project_slug }}/access.log \
          {{ cookiecutter.project_slug }}.wsgi:application

Restart=always

[Install]
WantedBy=multi-user.target
```

Start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable {{ cookiecutter.project_slug }}
sudo systemctl start {{ cookiecutter.project_slug }}
```

## SSL Certificate Setup

### Using Let's Encrypt

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal is configured automatically
# Test renewal
sudo certbot renew --dry-run
```

## Post-Deployment

### 1. Verify Deployment

```bash
# Check health endpoint
curl https://yourdomain.com/api/health/

# Check static files
curl -I https://yourdomain.com/static/admin/css/base.css

# Check frontend
curl -I https://yourdomain.com/
```

### 2. Create Admin User

```bash
# Docker deployment
docker compose -f docker-compose.prod.yml exec backend python manage.py createsuperuser

# Traditional deployment
cd /var/www/{{ cookiecutter.project_slug }}
source venv/bin/activate
python backend/manage.py createsuperuser
```

### 3. Configure Backups

#### Database Backup Script

Create `/usr/local/bin/backup-{{ cookiecutter.project_slug }}.sh`:

```bash
#!/bin/bash
BACKUP_DIR="/var/backups/{{ cookiecutter.project_slug }}"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR

# Database backup
{% if cookiecutter.database == 'postgresql' -%}
pg_dump -h localhost -U {{ cookiecutter.project_slug }} {{ cookiecutter.project_slug }} | gzip > $BACKUP_DIR/db_$DATE.sql.gz
{% elif cookiecutter.database == 'mysql' -%}
mysqldump -u {{ cookiecutter.project_slug }} -p {{ cookiecutter.project_slug }} | gzip > $BACKUP_DIR/db_$DATE.sql.gz
{%- endif %}

# Media files backup
tar -czf $BACKUP_DIR/media_$DATE.tar.gz /var/www/{{ cookiecutter.project_slug }}/backend/media

# Keep only last 30 days of backups
find $BACKUP_DIR -type f -mtime +30 -delete

# Optional: Upload to cloud storage
# aws s3 cp $BACKUP_DIR/db_$DATE.sql.gz s3://your-backup-bucket/
```

Add to crontab:

```bash
# Run daily at 2 AM
0 2 * * * /usr/local/bin/backup-{{ cookiecutter.project_slug }}.sh
```

## Monitoring & Maintenance

### 1. Application Monitoring

{% if cookiecutter.use_sentry == 'y' -%}
#### Sentry Setup

1. Create account at https://sentry.io
2. Create a new project
3. Copy DSN to SENTRY_DSN environment variable
4. Verify integration:

```python
# Test Sentry integration
from sentry_sdk import capture_message
capture_message("Test message from production")
```
{%- endif %}

#### Health Checks

Add monitoring for:
- `https://yourdomain.com/api/health/` - API health
- `https://yourdomain.com/` - Frontend availability
- Database connectivity
- Redis connectivity (if using)

### 2. Log Management

#### View Logs

```bash
# Docker logs
docker compose -f docker-compose.prod.yml logs -f backend
docker compose -f docker-compose.prod.yml logs -f frontend

# Systemd logs
sudo journalctl -u {{ cookiecutter.project_slug }} -f

# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

#### Log Rotation

Create `/etc/logrotate.d/{{ cookiecutter.project_slug }}`:

```
/var/log/{{ cookiecutter.project_slug }}/*.log {
    daily
    rotate 30
    compress
    delaycompress
    notifempty
    create 640 www-data www-data
    sharedscripts
    postrotate
        systemctl reload {{ cookiecutter.project_slug }}
    endscript
}
```

### 3. Performance Monitoring

#### Key Metrics to Monitor

- **Response Time**: API endpoint response times
- **Error Rate**: 5xx and 4xx error rates
- **Database**: Query performance, connection pool
- **Memory Usage**: Application memory consumption
- **CPU Usage**: Server CPU utilization
- **Disk Space**: Available storage space

#### Recommended Tools

- **Application Performance**: New Relic, DataDog, or AppDynamics
- **Infrastructure**: Prometheus + Grafana
- **Uptime Monitoring**: UptimeRobot, Pingdom, or StatusCake
- **Log Aggregation**: ELK Stack (Elasticsearch, Logstash, Kibana) or Loki

## Update Procedures

### 1. Code Updates

```bash
# Create backup before updating
./backup-{{ cookiecutter.project_slug }}.sh

# Pull latest code
git pull origin main

# Update dependencies
pip install -r backend/requirements/production.txt
cd frontend && npm ci && npm run build && cd ..

# Run migrations
python backend/manage.py migrate

# Collect static files
python backend/manage.py collectstatic --noinput

# Restart services
sudo systemctl restart {{ cookiecutter.project_slug }}
sudo systemctl reload nginx

# Or for Docker
docker compose -f docker-compose.prod.yml down
docker compose -f docker-compose.prod.yml up -d --build
```

### 2. Security Updates

```bash
# Check for security vulnerabilities
pip audit
npm audit

# Update packages with security issues
pip install --upgrade package-name
npm audit fix
```

## Troubleshooting

### Common Issues

#### 1. 502 Bad Gateway

**Cause**: Backend service not running or not responding

**Solution**:
```bash
# Check backend service status
sudo systemctl status {{ cookiecutter.project_slug }}
# or
docker compose -f docker-compose.prod.yml ps

# Check logs for errors
sudo journalctl -u {{ cookiecutter.project_slug }} -n 100
# or
docker compose -f docker-compose.prod.yml logs backend
```

#### 2. Static Files Not Loading

**Cause**: Static files not collected or nginx misconfiguration

**Solution**:
```bash
# Collect static files
python backend/manage.py collectstatic --noinput

# Check nginx configuration
sudo nginx -t
sudo systemctl reload nginx
```

#### 3. Database Connection Errors

**Cause**: Database service down or credentials incorrect

**Solution**:
```bash
# Check database service
sudo systemctl status postgresql
# or
docker compose -f docker-compose.prod.yml ps postgres

# Test connection
psql -h localhost -U {{ cookiecutter.project_slug }} -d {{ cookiecutter.project_slug }}
```

#### 4. CORS Errors

**Cause**: CORS_ALLOWED_ORIGINS not configured correctly

**Solution**:
- Ensure CORS_ALLOWED_ORIGINS includes your frontend URL
- Check that the protocol (http/https) matches

#### 5. Email Not Sending

**Cause**: Email configuration incorrect

**Solution**:
```bash
# Test email configuration
python backend/manage.py shell
>>> from django.core.mail import send_mail
>>> send_mail('Test', 'Test message', 'from@example.com', ['to@example.com'])
```

### Debug Mode (Emergency Only)

If you need to temporarily enable debug mode in production:

```bash
# Set DEBUG=True in environment
# WARNING: Only do this temporarily for debugging!
export DEBUG=True

# Restart service
sudo systemctl restart {{ cookiecutter.project_slug }}

# IMPORTANT: Disable debug mode immediately after debugging
export DEBUG=False
sudo systemctl restart {{ cookiecutter.project_slug }}
```

## Scaling Considerations

### Horizontal Scaling

1. **Load Balancer**: Use nginx, HAProxy, or cloud load balancer
2. **Multiple Backend Instances**: Run multiple gunicorn/uwsgi workers
3. **Database Replication**: Setup primary-replica database configuration
4. **Redis Cluster**: For session storage and caching
5. **CDN**: Use CloudFlare, AWS CloudFront for static/media files

### Vertical Scaling

1. **Increase Server Resources**: More CPU, RAM
2. **Database Optimization**: Indexes, query optimization
3. **Caching Strategy**: Implement Redis caching
4. **Async Tasks**: Use Celery for background tasks

## Support

For issues and questions:
- GitHub Issues: https://github.com/yourusername/{{ cookiecutter.project_slug }}/issues
- Documentation: https://github.com/yourusername/{{ cookiecutter.project_slug }}/wiki
- Email: {{ cookiecutter.author_email }}

## License

{{ cookiecutter.project_name }} - {{ cookiecutter.open_source_license }}