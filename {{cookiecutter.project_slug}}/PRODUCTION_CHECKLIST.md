# Production Readiness Checklist

Use this checklist to ensure your {{ cookiecutter.project_name }} application is ready for production deployment.

## 🔒 Security

### Authentication & Authorization

- [ ] Strong SECRET_KEY generated and stored securely
- [ ] DEBUG = False in production
- [ ] Admin URL changed from default `/admin/` (optional but recommended)
- [ ] Password validation rules configured
- [ ] Session timeout configured appropriately
- [ ] CSRF protection enabled
- [ ] Two-factor authentication implemented (optional)

### HTTPS & Transport Security

- [ ] SSL certificate installed and configured
- [ ] SECURE_SSL_REDIRECT = True
- [ ] SESSION_COOKIE_SECURE = True
- [ ] CSRF_COOKIE_SECURE = True
- [ ] SECURE_HSTS_SECONDS configured
- [ ] SECURE_HSTS_INCLUDE_SUBDOMAINS = True
- [ ] SECURE_HSTS_PRELOAD = True

### Headers & CORS

- [ ] X-Frame-Options header configured
- [ ] X-Content-Type-Options header configured
- [ ] X-XSS-Protection header configured
- [ ] Content-Security-Policy configured
- [ ] CORS_ALLOWED_ORIGINS restricted to specific domains
- [ ] ALLOWED_HOSTS configured with specific domains

### Database Security

- [ ] Strong database passwords
- [ ] Database connection uses SSL (for remote databases)
- [ ] Database user has minimal required permissions
- [ ] Database backups encrypted
- [ ] Connection pooling configured

### API Security

- [ ] API rate limiting implemented
- [ ] API authentication required for all endpoints
- [ ] Input validation on all API endpoints
- [ ] SQL injection protection (via ORM)
- [ ] XSS protection in responses

## 🚀 Performance

### Frontend Optimization

- [ ] JavaScript minified and bundled
- [ ] CSS minified and bundled
- [ ] Images optimized and compressed
- [ ] Lazy loading implemented for images
- [ ] Code splitting configured
- [ ] Service worker for offline support (optional)
- [ ] Browser caching headers configured

### Backend Optimization

- [ ] Database queries optimized (no N+1 queries)
- [ ] Database indexes created for frequent queries
- [ ] QuerySet pagination implemented
- [ ] select_related() and prefetch_related() used appropriately
- [ ] Database connection pooling configured
- [ ] Caching strategy implemented (Redis/Memcached)

### Static & Media Files

- [ ] Static files collected and served efficiently
- [ ] CDN configured for static files (optional but recommended)
- [ ] Media files stored in cloud storage (S3, GCS, etc.)
- [ ] Image thumbnails generated on upload
- [ ] Gzip compression enabled

### Infrastructure

- [ ] Adequate server resources (CPU, RAM, Storage)
- [ ] Load balancer configured (for multiple instances)
- [ ] Auto-scaling configured (optional)
- [ ] Database replication setup (optional)

## 📊 Monitoring & Logging

### Error Tracking

{% if cookiecutter.use_sentry == 'y' -%}

- [ ] Sentry configured and tested
- [ ] Error alerts configured
- [ ] Performance monitoring enabled
{%- else %}
- [ ] Error tracking service configured (Sentry, Rollbar, etc.)
- [ ] Error alerts configured
{%- endif %}

### Logging

- [ ] Application logging configured
- [ ] Log levels appropriate for production
- [ ] Log rotation configured
- [ ] Logs stored securely
- [ ] Sensitive data excluded from logs
- [ ] Log aggregation service configured (optional)

### Monitoring

- [ ] Uptime monitoring configured
- [ ] Health check endpoint implemented (`/api/health/`)
- [ ] Performance monitoring configured
- [ ] Database monitoring configured
- [ ] Disk space monitoring configured
- [ ] Alert thresholds configured

### Analytics

- [ ] Google Analytics or similar configured (optional)
- [ ] User behavior tracking configured (optional)
- [ ] API usage metrics tracked
- [ ] Custom business metrics tracked

## 🔄 DevOps & CI/CD

### Version Control

- [ ] Code in version control (Git)
- [ ] Sensitive data excluded from repository (.gitignore)
- [ ] Branch protection rules configured
- [ ] Code review process established

### Testing

- [ ] Unit tests written and passing
- [ ] Integration tests written and passing
- [ ] End-to-end tests written and passing
- [ ] Test coverage > 80%
- [ ] Performance tests conducted
- [ ] Security tests conducted

### CI/CD Pipeline

- [ ] Automated testing on pull requests
- [ ] Automated deployment to staging
- [ ] Manual approval for production deployment
- [ ] Rollback procedure documented and tested
- [ ] Database migration strategy tested
- [ ] Zero-downtime deployment configured

### Documentation

- [ ] API documentation complete
- [ ] Deployment documentation complete
- [ ] Environment variables documented
- [ ] Architecture diagram created
- [ ] Runbook for common issues created
- [ ] Disaster recovery plan documented

## 📦 Dependencies

### Package Management

- [ ] All dependencies pinned to specific versions
- [ ] Security vulnerabilities checked (`pip audit`, `npm audit`)
- [ ] Unused dependencies removed
- [ ] License compliance verified
- [ ] Private package repository configured (if needed)

### Updates

- [ ] Update schedule established
- [ ] Security update process defined
- [ ] Dependency update testing process defined
- [ ] Changelog maintained

## 💾 Data Management

### Backup & Recovery

- [ ] Database backup strategy implemented
- [ ] Backup schedule configured (daily minimum)
- [ ] Backup retention policy defined
- [ ] Backup restoration tested
- [ ] Point-in-time recovery available
- [ ] Offsite backups configured

### Data Privacy

- [ ] GDPR compliance (if applicable)
- [ ] Privacy policy published
- [ ] Terms of service published
- [ ] Cookie consent implemented (if applicable)
- [ ] Data retention policy implemented
- [ ] User data export functionality
- [ ] User data deletion functionality

### Database Maintenance

- [ ] Database maintenance schedule defined
- [ ] Vacuum/analyze scheduled (PostgreSQL)
- [ ] Index maintenance scheduled
- [ ] Archive strategy for old data
- [ ] Database monitoring configured

## 🌐 Domain & Networking

### DNS Configuration

- [ ] Domain registered and configured
- [ ] DNS records configured (A, CNAME, MX, TXT)
- [ ] TTL values appropriate
- [ ] DNS failover configured (optional)

### Email Configuration

- [ ] SMTP server configured
- [ ] SPF record configured
- [ ] DKIM configured
- [ ] DMARC configured
- [ ] Email templates tested
- [ ] Bounce handling configured

### Network Security

- [ ] Firewall configured
- [ ] Only necessary ports open
- [ ] DDoS protection configured
- [ ] Rate limiting configured
- [ ] IP whitelisting (if applicable)

## 🔧 Operational Readiness

### Team Preparedness

- [ ] On-call schedule established
- [ ] Incident response process documented
- [ ] Communication channels established
- [ ] Access credentials securely shared
- [ ] Team trained on deployment procedures

### Business Continuity

- [ ] SLA defined
- [ ] Maintenance window scheduled
- [ ] User communication plan
- [ ] Graceful degradation implemented
- [ ] Feature flags configured (optional)

### Compliance

- [ ] Regulatory requirements identified
- [ ] Compliance checks completed
- [ ] Audit logging implemented
- [ ] Data residency requirements met
- [ ] Security certifications obtained (if required)

## 🎯 Final Checks

### Pre-Launch Testing

- [ ] Load testing completed
- [ ] Penetration testing completed (optional)
- [ ] User acceptance testing completed
- [ ] Cross-browser testing completed
- [ ] Mobile responsiveness tested
- [ ] Accessibility testing completed (WCAG compliance)

### Launch Preparation

- [ ] Launch date scheduled
- [ ] Rollback plan prepared
- [ ] Support team briefed
- [ ] Marketing materials ready (if applicable)
- [ ] User documentation published
- [ ] Status page configured

### Post-Launch

- [ ] Monitor error rates
- [ ] Monitor performance metrics
- [ ] Monitor user feedback
- [ ] Address critical issues immediately
- [ ] Schedule retrospective meeting
- [ ] Document lessons learned

## Sign-off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Project Manager | | | |
| Technical Lead | | | |
| Security Officer | | | |
| DevOps Engineer | | | |
| QA Lead | | | |
| Product Owner | | | |

---

**Note**: This checklist should be customized based on your specific requirements, industry regulations, and organizational policies. Not all items may apply to your deployment.

**Last Updated**: {{ cookiecutter.year }}-{{ '%02d' | format(cookiecutter.month|int) }}-{{ '%02d' | format(cookiecutter.day|int) }}
