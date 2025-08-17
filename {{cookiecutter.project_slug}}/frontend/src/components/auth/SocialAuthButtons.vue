{% if cookiecutter.use_social_auth == 'y' -%}
<template>
  <div class="social-auth-buttons">
    <div class="divider">
      <span>Or continue with</span>
    </div>
    
    <div class="social-buttons">
      {% if 'google' in cookiecutter.social_auth_providers -%}
      <button
        @click="handleSocialLogin('google')"
        class="social-btn google"
        :disabled="loading"
      >
        <IconLucideChrome class="w-5 h-5" />
        <span>Google</span>
      </button>
      {% endif -%}
      
      {% if 'github' in cookiecutter.social_auth_providers -%}
      <button
        @click="handleSocialLogin('github')"
        class="social-btn github"
        :disabled="loading"
      >
        <IconLucideGithub class="w-5 h-5" />
        <span>GitHub</span>
      </button>
      {% endif -%}
      
      {% if 'facebook' in cookiecutter.social_auth_providers -%}
      <button
        @click="handleSocialLogin('facebook')"
        class="social-btn facebook"
        :disabled="loading"
      >
        <IconLucideFacebook class="w-5 h-5" />
        <span>Facebook</span>
      </button>
      {% endif -%}
      
      {% if 'twitter' in cookiecutter.social_auth_providers -%}
      <button
        @click="handleSocialLogin('twitter')"
        class="social-btn twitter"
        :disabled="loading"
      >
        <IconLucideTwitter class="w-5 h-5" />
        <span>Twitter</span>
      </button>
      {% endif -%}
    </div>
  </div>
</template>

<script setup{% if cookiecutter.use_typescript == 'y' %} lang="ts"{% endif %}>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
{% if cookiecutter.use_typescript == 'y' %}

interface SocialAuthProvider {
  name: string
  authUrl: string
  clientId: string
}
{% endif %}

const authStore = useAuthStore()
const router = useRouter()
const loading = ref(false)

const socialProviders{% if cookiecutter.use_typescript == 'y' %}: Record<string, SocialAuthProvider>{% endif %} = {
  {% if 'google' in cookiecutter.social_auth_providers -%}
  google: {
    name: 'Google',
    authUrl: 'https://accounts.google.com/o/oauth2/v2/auth',
    clientId: import.meta.env.VITE_GOOGLE_CLIENT_ID || '',
  },
  {% endif -%}
  {% if 'github' in cookiecutter.social_auth_providers -%}
  github: {
    name: 'GitHub',
    authUrl: 'https://github.com/login/oauth/authorize',
    clientId: import.meta.env.VITE_GITHUB_CLIENT_ID || '',
  },
  {% endif -%}
  {% if 'facebook' in cookiecutter.social_auth_providers -%}
  facebook: {
    name: 'Facebook',
    authUrl: 'https://www.facebook.com/v13.0/dialog/oauth',
    clientId: import.meta.env.VITE_FACEBOOK_CLIENT_ID || '',
  },
  {% endif -%}
  {% if 'twitter' in cookiecutter.social_auth_providers -%}
  twitter: {
    name: 'Twitter',
    authUrl: 'https://twitter.com/i/oauth2/authorize',
    clientId: import.meta.env.VITE_TWITTER_CLIENT_ID || '',
  },
  {% endif -%}
}

const handleSocialLogin = async (provider{% if cookiecutter.use_typescript == 'y' %}: string{% endif %}) => {
  loading.value = true
  
  try {
    const providerConfig = socialProviders[provider]
    if (!providerConfig) {
      throw new Error(`Unknown provider: ${provider}`)
    }
    
    // Generate state for CSRF protection
    const state = Math.random().toString(36).substring(2, 15)
    sessionStorage.setItem('oauth_state', state)
    sessionStorage.setItem('oauth_provider', provider)
    
    // Build OAuth URL
    const redirectUri = `${window.location.origin}/auth/callback`
    const params = new URLSearchParams({
      client_id: providerConfig.clientId,
      redirect_uri: redirectUri,
      response_type: 'code',
      scope: getScope(provider),
      state: state,
    })
    
    // Redirect to OAuth provider
    window.location.href = `${providerConfig.authUrl}?${params.toString()}`
    
  } catch (error) {
    console.error('Social login error:', error)
    loading.value = false
  }
}

const getScope = (provider{% if cookiecutter.use_typescript == 'y' %}: string{% endif %}){% if cookiecutter.use_typescript == 'y' %}: string{% endif %} => {
  const scopes{% if cookiecutter.use_typescript == 'y' %}: Record<string, string>{% endif %} = {
    google: 'openid email profile',
    github: 'user:email',
    facebook: 'email public_profile',
    twitter: 'users.read tweet.read',
  }
  return scopes[provider] || ''
}
</script>

<style scoped>
.social-auth-buttons {
  margin-top: 2rem;
}

.divider {
  position: relative;
  text-align: center;
  margin: 1.5rem 0;
}

.divider::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  height: 1px;
  background-color: #e5e7eb;
}

.dark .divider::before {
  background-color: #374151;
}

.divider span {
  position: relative;
  padding: 0 1rem;
  background-color: white;
  color: #6b7280;
  font-size: 0.875rem;
}

.dark .divider span {
  background-color: #1f2937;
  color: #9ca3af;
}

.social-buttons {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 0.75rem;
}

.social-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.625rem 1rem;
  border: 1px solid #e5e7eb;
  border-radius: 0.375rem;
  background-color: white;
  color: #374151;
  font-weight: 500;
  transition: all 0.2s;
  cursor: pointer;
}

.dark .social-btn {
  border-color: #374151;
  background-color: #1f2937;
  color: #e5e7eb;
}

.social-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.social-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.social-btn.google:hover {
  background-color: #4285f4;
  color: white;
  border-color: #4285f4;
}

.social-btn.github:hover {
  background-color: #24292e;
  color: white;
  border-color: #24292e;
}

.social-btn.facebook:hover {
  background-color: #1877f2;
  color: white;
  border-color: #1877f2;
}

.social-btn.twitter:hover {
  background-color: #1da1f2;
  color: white;
  border-color: #1da1f2;
}
</style>
{%- endif %}