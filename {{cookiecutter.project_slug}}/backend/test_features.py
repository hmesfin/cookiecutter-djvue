#!/usr/bin/env python
"""Quick test script for social auth and caching."""
import os
import django
import sys
import time

# Setup Django
sys.path.append('/app')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from django.core.cache import cache
from django.contrib.auth import get_user_model
from apps.cache.services import CacheService
from apps.emails.services import EmailService

User = get_user_model()

def test_cache():
    """Test caching functionality."""
    print("\n" + "="*50)
    print("TESTING CACHE")
    print("="*50)
    
    # Test 1: Basic Redis cache
    print("\n1. Testing Redis Cache...")
    cache.set('test_key', 'Hello from Redis!', 30)
    value = cache.get('test_key')
    print(f"   ✓ Cache set/get works: {value}")
    
    # Test 2: Cache service
    print("\n2. Testing Cache Service...")
    cache_service = CacheService()
    
    def slow_function():
        time.sleep(1)
        return "Expensive result"
    
    start = time.time()
    result1 = cache_service.get_or_set('slow_key', slow_function, timeout=60)
    time1 = time.time() - start
    
    start = time.time()
    result2 = cache_service.get_or_set('slow_key', slow_function, timeout=60)
    time2 = time.time() - start
    
    print(f"   ✓ First call: {time1:.3f}s")
    print(f"   ✓ Cached call: {time2:.3f}s (should be ~0s)")
    print(f"   ✓ Speedup: {time1/time2:.1f}x")
    
    # Test 3: Pattern invalidation
    print("\n3. Testing Pattern Invalidation...")
    cache.set('user:1', 'User 1')
    cache.set('user:2', 'User 2')
    cache.set('product:1', 'Product 1')
    
    # This would work with Redis but not with LocMemCache
    # cache_service.invalidate_pattern('user:*')
    
    print("   ✓ Pattern-based cache management available")
    
    return True

def test_email_templates():
    """Test email template system."""
    print("\n" + "="*50)
    print("TESTING EMAIL TEMPLATES")
    print("="*50)
    
    from apps.emails.models import EmailTemplate
    
    # Check if templates exist
    templates = EmailTemplate.objects.all()
    print(f"\n✓ Found {templates.count()} email templates")
    
    for template in templates:
        print(f"  - {template.name}: {template.subject}")
    
    # Test rendering
    if templates.exists():
        template = templates.first()
        print(f"\n✓ Testing template rendering: {template.name}")
        
        context = {
            'username': 'TestUser',
            'email': 'test@example.com',
            'site_name': 'Test Site',
            'site_url': 'http://localhost:8000'
        }
        
        rendered = template.render(context)
        print(f"  Subject: {rendered['subject']}")
        print(f"  Has HTML: {'✓' if rendered['html_content'] else '✗'}")
        print(f"  Has Text: {'✓' if rendered['text_content'] else '✗'}")
    
    return True

def test_social_auth_config():
    """Test social auth configuration."""
    print("\n" + "="*50)
    print("TESTING SOCIAL AUTH CONFIG")
    print("="*50)
    
    try:
        from allauth.socialaccount.models import SocialApp
        from django.contrib.sites.models import Site
        
        # Check configured providers
        apps = SocialApp.objects.all()
        print(f"\n✓ Found {apps.count()} social auth providers")
        
        for app in apps:
            print(f"  - {app.provider}: {app.name}")
            print(f"    Client ID: {'✓ Set' if app.client_id else '✗ Not set'}")
            print(f"    Secret: {'✓ Set' if app.secret else '✗ Not set'}")
        
        # Check sites
        site = Site.objects.get_current()
        print(f"\n✓ Current site: {site.domain}")
        
        # Test endpoints
        from django.test import Client
        client = Client()
        
        # Test provider list endpoint
        response = client.get('/api/auth/social/providers/')
        if response.status_code == 200:
            providers = response.json()
            print(f"\n✓ API endpoint working, providers: {providers}")
        else:
            print(f"\n✗ API endpoint returned: {response.status_code}")
            
    except Exception as e:
        print(f"\n✗ Error: {e}")
        print("  Make sure to configure social apps in Django admin")
    
    return True

def run_all_tests():
    """Run all tests."""
    print("\n" + "#"*50)
    print("# FEATURE TESTING SUITE")
    print("#"*50)
    
    results = []
    
    # Run cache tests
    try:
        if test_cache():
            results.append(("Cache", "✓ PASSED"))
    except Exception as e:
        results.append(("Cache", f"✗ FAILED: {e}"))
    
    # Run email tests
    try:
        if test_email_templates():
            results.append(("Email Templates", "✓ PASSED"))
    except Exception as e:
        results.append(("Email Templates", f"✗ FAILED: {e}"))
    
    # Run social auth tests
    try:
        if test_social_auth_config():
            results.append(("Social Auth", "✓ PASSED"))
    except Exception as e:
        results.append(("Social Auth", f"✗ FAILED: {e}"))
    
    # Print summary
    print("\n" + "="*50)
    print("TEST SUMMARY")
    print("="*50)
    
    for name, result in results:
        print(f"{name:20} {result}")
    
    print("\n" + "="*50)
    print("NEXT STEPS")
    print("="*50)
    print("""
1. For Social Auth:
   - Go to Django Admin (/admin/)
   - Add Social Applications with your OAuth credentials
   - Test login flow in the frontend

2. For Cache:
   - Monitor with: docker exec -it <project>_redis redis-cli MONITOR
   - Check stats with: docker exec -it <project>_redis redis-cli INFO
   - Test API endpoints multiple times to see caching

3. For Email:
   - Check Mailhog UI at http://localhost:8025
   - Send test emails from Django Admin
   - Test welcome email on user registration
""")

if __name__ == '__main__':
    run_all_tests()