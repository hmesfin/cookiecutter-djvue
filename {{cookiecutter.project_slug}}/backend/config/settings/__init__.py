"""
Django settings for {{ cookiecutter.project_name }} project.
"""
import os

# Determine which settings module to use
environment = os.environ.get('DJANGO_ENV', 'development')

if environment == 'production':
    from .production import *
elif environment == 'testing':
    from .testing import *
else:
    from .development import *