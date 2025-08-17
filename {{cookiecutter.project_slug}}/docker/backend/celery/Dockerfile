{% if cookiecutter.use_celery == 'y' -%}
# Celery Worker/Beat Dockerfile
FROM python:{{ cookiecutter.python_version }}-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    {% if cookiecutter.database == 'postgresql' -%}
    libpq-dev \
    postgresql-client \
    {% elif cookiecutter.database == 'mysql' -%}
    default-libmysqlclient-dev \
    default-mysql-client \
    {%- endif %}
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY backend/requirements/ /tmp/requirements/
RUN pip install --upgrade pip && \
    pip install -r /tmp/requirements/development.txt

# Copy start scripts
COPY docker/backend/celery/start-worker /start-worker
COPY docker/backend/celery/start-beat /start-beat
RUN chmod +x /start-worker /start-beat

# The application code will be mounted as a volume

# Default to worker, can be overridden
CMD ["/start-worker"]
{%- endif %}