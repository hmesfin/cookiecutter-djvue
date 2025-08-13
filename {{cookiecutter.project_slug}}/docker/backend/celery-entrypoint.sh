#!/bin/bash
set -e

echo "Starting Celery worker..."

{% if cookiecutter.database == 'postgresql' -%}
# Wait for PostgreSQL
echo "Waiting for PostgreSQL..."
while ! nc -z postgres 5432; do
  sleep 0.1
done
echo "PostgreSQL is ready"
{% elif cookiecutter.database == 'mysql' -%}
# Wait for MySQL
echo "Waiting for MySQL..."
while ! nc -z mysql 3306; do
  sleep 0.1
done
echo "MySQL is ready"
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