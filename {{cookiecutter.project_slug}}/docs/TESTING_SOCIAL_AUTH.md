# Testing Social Authentication

## 1. Setup OAuth Applications

### Google OAuth
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable Google+ API
4. Go to Credentials → Create Credentials → OAuth 2.0 Client ID
5. Add authorized redirect URIs:
   - `http://localhost:8000/api/auth/google/callback/`
   - `http://localhost:5173/auth/callback/google`
6. Copy Client ID and Client Secret

### GitHub OAuth
1. Go to GitHub Settings → Developer settings → OAuth Apps
2. Click "New OAuth App"
3. Fill in:
   - Application name: Your App Name (Dev)
   - Homepage URL: `http://localhost:5173`
   - Authorization callback URL: `http://localhost:8000/api/auth/github/callback/`
4. Copy Client ID and Client Secret

### Update Environment Variables
Add to your `.env` file:
```bash
# Google OAuth
GOOGLE_OAUTH_CLIENT_ID=your-google-client-id
GOOGLE_OAUTH_CLIENT_SECRET=your-google-client-secret

# GitHub OAuth  
GITHUB_OAUTH_CLIENT_ID=your-github-client-id
GITHUB_OAUTH_CLIENT_SECRET=your-github-client-secret
```

## 2. Test Backend Social Auth Endpoints

### Test with curl or HTTPie

```bash
# 1. Get available social auth providers
curl http://localhost:8000/api/auth/social/providers/

# 2. Initiate OAuth flow (this will return a redirect URL)
curl http://localhost:8000/api/auth/social/google/

# 3. Test the connection endpoint (after OAuth callback)
# This would normally be handled by the frontend
```

### Test with Django Shell

```python
python manage.py shell

# Test social auth configuration
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site

# Check if social apps are configured
SocialApp.objects.all()

# Create a test social app if needed
site = Site.objects.get_current()
google_app = SocialApp.objects.create(
    provider='google',
    name='Google',
    client_id='your-client-id',
    secret='your-client-secret',
)
google_app.sites.add(site)
```

## 3. Test Frontend Integration

### Create a Test Component

Create `frontend/src/components/SocialAuthTest.vue`:

{% raw %}
```vue
<template>
  <div class="p-4">
    <h2 class="text-2xl font-bold mb-4">Social Auth Test</h2>
    
    <div class="space-y-4">
      <button 
        @click="loginWithGoogle"
        class="btn btn-primary flex items-center gap-2"
      >
        <Icon name="mdi:google" />
        Login with Google
      </button>
      
      <button 
        @click="loginWithGitHub"
        class="btn btn-secondary flex items-center gap-2"
      >
        <Icon name="mdi:github" />
        Login with GitHub
      </button>
      
      <div v-if="user" class="mt-4 p-4 bg-gray-100 dark:bg-gray-800 rounded">
        <h3 class="font-bold">Logged in as:</h3>
        <pre>{{ JSON.stringify(user, null, 2) }}</pre>
      </div>
      
      <div v-if="error" class="mt-4 p-4 bg-red-100 text-red-700 rounded">
        Error: {{ error }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const user = ref(null)
const error = ref(null)

const loginWithGoogle = async () => {
  try {
    error.value = null
    // Redirect to backend OAuth endpoint
    window.location.href = 'http://localhost:8000/api/auth/social/google/'
  } catch (err) {
    error.value = err.message
  }
}

const loginWithGitHub = async () => {
  try {
    error.value = null
    window.location.href = 'http://localhost:8000/api/auth/social/github/'
  } catch (err) {
    error.value = err.message
  }
}

// Check if we're returning from OAuth callback
const urlParams = new URLSearchParams(window.location.search)
const token = urlParams.get('token')
if (token) {
  authStore.setToken(token)
  user.value = authStore.user
}
</script>
```
{% endraw %}

## 4. Test API Integration

### Create API Test Script

Create `backend/test_social_auth.py`:

```python
#!/usr/bin/env python
import os
import django
import sys

sys.path.append('/app')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from allauth.socialaccount.models import SocialAccount

User = get_user_model()
client = Client()

def test_social_auth_flow():
    """Test social authentication flow."""
    
    # Test provider list endpoint
    response = client.get('/api/auth/social/providers/')
    print(f"Available providers: {response.json()}")
    
    # Test user creation via social auth
    # This would normally happen through OAuth callback
    test_user = User.objects.create_user(
        username='socialuser',
        email='social@example.com'
    )
    
    # Create social account
    social_account = SocialAccount.objects.create(
        user=test_user,
        provider='google',
        uid='12345',
        extra_data={'name': 'Test User', 'email': 'social@example.com'}
    )
    
    print(f"Created social account: {social_account}")
    
    # Test login endpoint
    response = client.post('/api/auth/login/', {
        'email': 'social@example.com',
        'password': 'testpass123'
    })
    
    if response.status_code == 200:
        print(f"Login successful: {response.json()}")
    else:
        print(f"Login failed: {response.status_code}")

if __name__ == '__main__':
    test_social_auth_flow()
```

Run it:
```bash
docker exec -it myproject_backend python /app/test_social_auth.py
```

## 5. Manual Testing Checklist

- [ ] Google OAuth login works
- [ ] GitHub OAuth login works  
- [ ] User is created on first social login
- [ ] Existing user can link social account
- [ ] JWT tokens are properly issued
- [ ] User data is correctly populated from social provider
- [ ] Logout works properly
- [ ] Social account can be disconnected

## 6. Debugging Tips

### Check Django Admin
1. Go to http://localhost:8000/admin/
2. Check Social Accounts → Social applications
3. Check Social Accounts → Social accounts (user connections)

### Enable Debug Logging
```python
# In settings/development.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'allauth': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'dj_rest_auth': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

### Common Issues & Solutions

1. **Redirect URI mismatch**: Ensure callback URLs match exactly in OAuth app settings
2. **CORS errors**: Add frontend URL to CORS_ALLOWED_ORIGINS
3. **Token not persisting**: Check SESSION_COOKIE_SECURE and CSRF settings
4. **User not created**: Check SOCIALACCOUNT_AUTO_SIGNUP setting