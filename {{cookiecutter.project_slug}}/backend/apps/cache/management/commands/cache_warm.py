"""Management command to warm cache."""
from django.core.management.base import BaseCommand
from django.apps import apps
from apps.cache.services import CacheWarmer


class Command(BaseCommand):
    help = 'Warm cache with commonly accessed data'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--models',
            nargs='+',
            type=str,
            help='Models to warm cache for (app_label.ModelName)',
        )
        parser.add_argument(
            '--endpoints',
            nargs='+',
            type=str,
            help='API endpoints to warm',
        )
    
    def handle(self, *args, **options):
        models = options.get('models', [])
        endpoints = options.get('endpoints', [])
        
        warmer = CacheWarmer()
        
        # Warm model caches
        if models:
            for model_path in models:
                try:
                    app_label, model_name = model_path.split('.')
                    model = apps.get_model(app_label, model_name)
                    
                    # Define common querysets to cache
                    querysets = [
                        model.objects.all()[:100],  # First 100 objects
                        model.objects.filter(is_active=True) if hasattr(model, 'is_active') else model.objects.all(),
                    ]
                    
                    warmer.warm_queryset_cache(model, querysets)
                    self.stdout.write(
                        self.style.SUCCESS(f'Warmed cache for {model_path}')
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'Error warming cache for {model_path}: {str(e)}')
                    )
        
        # Warm API endpoints
        if endpoints:
            warmer.warm_api_endpoints(endpoints)
            self.stdout.write(
                self.style.SUCCESS(f'Warmed cache for {len(endpoints)} endpoints')
            )
        
        if not models and not endpoints:
            # Default warming strategy
            default_endpoints = [
                '/api/config/',
                '/api/users/me/',
            ]
            
            warmer.warm_api_endpoints(default_endpoints)
            self.stdout.write(
                self.style.SUCCESS('Warmed cache with default strategy')
            )