<template>
  <div class="login-page">
    {% if cookiecutter.css_framework == 'tailwindcss' -%}
    <div class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div class="max-w-md w-full space-y-8">
        <div>
          <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Sign in to your account
          </h2>
        </div>
        <form class="mt-8 space-y-6" @submit.prevent="handleLogin">
          <div class="rounded-md shadow-sm -space-y-px">
            <div>
              <label for="username" class="sr-only">Username</label>
              <input
                id="username"
                v-model="credentials.username"
                name="username"
                type="text"
                autocomplete="username"
                required
                class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                placeholder="Username"
              >
            </div>
            <div>
              <label for="password" class="sr-only">Password</label>
              <input
                id="password"
                v-model="credentials.password"
                name="password"
                type="password"
                autocomplete="current-password"
                required
                class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                placeholder="Password"
              >
            </div>
          </div>

          <div v-if="error" class="rounded-md bg-red-50 p-4">
            <p class="text-sm text-red-800">{% raw %}{{ error }}{% endraw %}</p>
          </div>

          <div>
            <button
              type="submit"
              :disabled="loading"
              class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
            >
              {% raw %}{{ loading ? 'Signing in...' : 'Sign in' }}{% endraw %}
            </button>
          </div>

          <div class="text-center">
            <RouterLink :to="{ name: 'register' }" class="font-medium text-indigo-600 hover:text-indigo-500">
              Don't have an account? Sign up
            </RouterLink>
          </div>
        </form>
      </div>
    </div>
    {% else -%}
    <div class="container">
      <h2>Sign in to your account</h2>
      <form @submit.prevent="handleLogin">
        <div>
          <label for="username">Username</label>
          <input
            id="username"
            v-model="credentials.username"
            type="text"
            required
          >
        </div>
        <div>
          <label for="password">Password</label>
          <input
            id="password"
            v-model="credentials.password"
            type="password"
            required
          >
        </div>
        <div v-if="error">{% raw %}{{ error }}{% endraw %}</div>
        <button type="submit" :disabled="loading">
          {% raw %}{{ loading ? 'Signing in...' : 'Sign in' }}{% endraw %}
        </button>
      </form>
      <RouterLink :to="{ name: 'register' }">
        Don't have an account? Sign up
      </RouterLink>
    </div>
    {%- endif %}
  </div>
</template>

<script setup{% if cookiecutter.use_typescript == 'y' %} lang="ts"{% endif %}>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const credentials = ref({
  username: '',
  password: ''
})

const loading = ref(false)
const error = ref{% if cookiecutter.use_typescript == 'y' %}<string | null>{% endif %}(null)

async function handleLogin() {
  loading.value = true
  error.value = null
  
  try {
    await authStore.login(credentials.value)
    const redirect = route.query.redirect{% if cookiecutter.use_typescript == 'y' %} as string{% endif %} || '/dashboard'
    router.push(redirect)
  } catch (err{% if cookiecutter.use_typescript == 'y' %}: any{% endif %}) {
    error.value = err.response?.data?.detail || 'Invalid credentials'
  } finally {
    loading.value = false
  }
}
</script>