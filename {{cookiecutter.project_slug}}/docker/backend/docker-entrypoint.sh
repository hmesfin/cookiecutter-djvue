#!/bin/bash
set -e

echo "Waiting for database..."

{% if cookiecutter.database == 'postgresql' -%}
# Wait for PostgreSQL
while ! nc -z postgres 5432; do
  sleep 0.1
done
echo "PostgreSQL started"
{% elif cookiecutter.database == 'mysql' -%}
# Wait for MySQL
while ! nc -z mysql 3306; do
  sleep 0.1
done
echo "MySQL started"
{%- endif %}

# Run migrations
echo "Running database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser if it doesn't exist
echo "Creating superuser if needed..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(email='admin@example.com').exists():
    User.objects.create_superuser(
        email='admin@example.com',
        username='admin',
        password='admin123'
    )
    print('Superuser created: admin@example.com / admin123')
else:
    print('Superuser already exists')
" || echo "Could not create superuser automatically"

# Start server
echo "Starting Django development server..."
exec python manage.py runserver 0.0.0.0:8000