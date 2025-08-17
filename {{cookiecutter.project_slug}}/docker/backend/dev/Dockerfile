{% if cookiecutter.use_docker == 'y' -%}
# Development Dockerfile for backend
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
    gettext \
    netcat-traditional \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
# This allows Docker to cache the dependency layer
COPY backend/requirements/ /tmp/requirements/
RUN pip install --upgrade pip && \
    pip install -r /tmp/requirements/development.txt

# Copy start script
COPY docker/backend/dev/start /start
RUN chmod +x /start

# The application code will be mounted as a volume

# Create necessary directories
RUN mkdir -p /app/staticfiles /app/media

# Expose port
EXPOSE 8000

# Use start script
CMD ["/start"]
{%- endif %}