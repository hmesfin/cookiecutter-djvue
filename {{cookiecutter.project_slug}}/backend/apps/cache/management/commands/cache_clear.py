"""Management command to clear cache."""
from django.core.management.base import BaseCommand
from django.core.cache import cache, caches
from apps.cache.services import CacheService


class Command(BaseCommand):
    help = 'Clear cache entries'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--pattern',
            type=str,
            help='Clear keys matching pattern (Redis only)',
        )
        parser.add_argument(
            '--cache',
            type=str,
            default='default',
            help='Cache backend to clear',
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='Clear all cache entries',
        )
    
    def handle(self, *args, **options):
        cache_name = options['cache']
        pattern = options.get('pattern')
        clear_all = options.get('all')
        
        try:
            if clear_all:
                # Clear all cache entries
                cache_backend = caches[cache_name]
                cache_backend.clear()
                self.stdout.write(
                    self.style.SUCCESS(f'Cleared all entries from {cache_name} cache')
                )
            elif pattern:
                # Clear by pattern
                cache_service = CacheService(cache_alias=cache_name)
                cache_service.invalidate_pattern(pattern)
                self.stdout.write(
                    self.style.SUCCESS(f'Cleared entries matching pattern: {pattern}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING('No action specified. Use --all or --pattern')
                )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error clearing cache: {str(e)}')
            )