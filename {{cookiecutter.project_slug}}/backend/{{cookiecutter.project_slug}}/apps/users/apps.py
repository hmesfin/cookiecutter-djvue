from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = '{{ cookiecutter.project_slug }}.apps.users'
    verbose_name = 'Users'
    
    def ready(self):
        """Import signals when app is ready."""
        try:
            import {{ cookiecutter.project_slug }}.apps.users.signals  # noqa
        except ImportError:
            pass