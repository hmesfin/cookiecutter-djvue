#!/bin/bash
set -e

echo "Starting Celery service..."

{% if cookiecutter.database == 'postgresql' -%}
# Wait for PostgreSQL to be ready and have migrations applied
echo "Waiting for PostgreSQL and migrations..."
until PGPASSWORD=changeme psql -h postgres -U {{ cookiecutter.project_slug }} -d {{ cookiecutter.project_slug }} -c "SELECT 1 FROM django_migrations LIMIT 1;" &>/dev/null; do
  echo "Waiting for database migrations to complete..."
  sleep 2
done
echo "Database is ready with migrations applied"
{% elif cookiecutter.database == 'mysql' -%}
# Wait for MySQL to be ready and have migrations applied
echo "Waiting for MySQL and migrations..."
until mysql -h mysql -u {{ cookiecutter.project_slug }} -pchangeme {{ cookiecutter.project_slug }} -e "SELECT 1 FROM django_migrations LIMIT 1;" &>/dev/null; do
  echo "Waiting for database migrations to complete..."
  sleep 2
done
echo "Database is ready with migrations applied"
{%- endif %}

{% if cookiecutter.use_redis == 'y' -%}
# Wait for Redis
echo "Waiting for Redis..."
while ! nc -z redis 6379; do
  sleep 0.1
done
echo "Redis is ready"
{%- endif %}

# Execute the command passed to the script
exec "$@"