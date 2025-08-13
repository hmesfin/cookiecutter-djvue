{% if cookiecutter.use_docker == 'y' -%}
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
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY backend/requirements/development.txt /tmp/requirements.txt
RUN pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt

# Copy project
COPY backend/ /app/

# Create necessary directories
RUN mkdir -p /app/staticfiles /app/media

# Run as non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
{%- endif %}