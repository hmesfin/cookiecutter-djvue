<template>
  <div class="space-y-6">
    {% if cookiecutter.css_framework == 'tailwindcss' -%}
    <div class="space-y-6">
      <div>
        <h2 class="text-3xl font-bold text-center text-gray-900 dark:text-gray-100">Welcome back</h2>
        <p class="mt-2 text-center text-sm text-gray-600 dark:text-gray-400">
          Or
          <RouterLink to="/auth/register" class="font-medium text-indigo-600 hover:text-indigo-500">
            create a new account
          </RouterLink>
        </p>
      </div>
      
      <form @submit.prevent="handleLogin" class="space-y-6">
        <div>
          <label for="email" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Email address</label>
          <input
            id="email"
            v-model="form.email"
            type="email"
            required
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 dark:border-gray-600 dark:shadow-lg dark:shadow-gray-900/30 dark:focus:ring-indigo-400 dark:focus:border-indigo-400"
            :class="{ 'border-red-500': errors.email }"
          >
          <p v-if="errors.email" class="mt-1 text-sm text-red-600">{% raw %}{{ errors.email }}{% endraw %}</p>
        </div>

        <div>
          <label for="password" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Password</label>
          <PasswordInput
            id="password"
            v-model="form.password"
            :required="true"
            placeholder="Enter your password"
            autocomplete="current-password"
            class="mt-1"
          />
          <p v-if="errors.password" class="mt-1 text-sm text-red-600">{% raw %}{{ errors.password }}{% endraw %}</p>
        </div>

        <div class="flex items-center justify-between">
          <div class="flex items-center">
            <input
              id="remember"
              v-model="form.remember"
              type="checkbox"
              class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded dark:focus:ring-indigo-400 dark:border-gray-600"
            >
            <label for="remember" class="ml-2 block text-sm text-gray-900 dark:text-gray-100">
              Remember me
            </label>
          </div>

          <RouterLink to="/auth/forgot-password" class="text-sm text-indigo-600 hover:text-indigo-500">
            Forgot your password?
          </RouterLink>
        </div>

        <div>
          <button
            type="submit"
            :disabled="loading"
            class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed dark:shadow-lg dark:shadow-gray-900/30 dark:focus:ring-indigo-400"
          >
            <span v-if="loading">Signing in...</span>
            <span v-else>Sign in</span>
          </button>
        </div>

        <div v-if="errors.general" class="rounded-md bg-red-50 p-4 dark:bg-red-900/20">
          <p class="text-sm text-red-800">{% raw %}{{ errors.general }}{% endraw %}</p>
        </div>
      </form>
    </div>
    {% else -%}
    <div class="login-form">
      <h2>Welcome back</h2>
      <p class="subtitle">
        Or <RouterLink to="/auth/register">create a new account</RouterLink>
      </p>
      
      <form @submit.prevent="handleLogin">
        <div class="mb-6">
          <label for="email">Email address</label>
          <input
            id="email"
            v-model="form.email"
            type="email"
            required
            :class="{ error: errors.email }"
          >
          <span v-if="errors.email" class="error-message">{% raw %}{{ errors.email }}{% endraw %}</span>
        </div>

        <div class="mb-6">
          <label for="password">Password</label>
          <input
            id="password"
            v-model="form.password"
            type="password"
            required
            :class="{ error: errors.password }"
          >
          <span v-if="errors.password" class="error-message">{% raw %}{{ errors.password }}{% endraw %}</span>
        </div>

        <div class="form-options">
          <label class="checkbox">
            <input v-model="form.remember" type="checkbox">
            <span>Remember me</span>
          </label>
          <RouterLink to="/auth/forgot-password" class="link">Forgot password?</RouterLink>
        </div>

        <button type="submit" :disabled="loading" class="btn btn-primary btn-block">
          {% raw %}{{ loading ? 'Signing in...' : 'Sign in' }}{% endraw %}
        </button>

        <div v-if="errors.general" class="alert alert-error">
          {% raw %}{{ errors.general }}{% endraw %}
        </div>
      </form>
    </div>
    {%- endif %}
  </div>
</template>

<script setup{% if cookiecutter.use_typescript == 'y' %} lang="ts"{% endif %}>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import PasswordInput from '@/components/PasswordInput.vue'

const router = useRouter()
const authStore = useAuthStore()

const loading = ref(false)
const form = reactive({
  email: '',
  password: '',
  remember: false,
})

const errors = reactive({
  email: '',
  password: '',
  general: '',
})

const handleLogin = async () => {
  // Clear errors
  errors.email = ''
  errors.password = ''
  errors.general = ''
  
  loading.value = true
  
  try {
    await authStore.login({
      {% if cookiecutter.api_authentication == 'jwt' or cookiecutter.api_authentication == 'token' -%}
      email: form.email,
      {% else -%}
      username: form.email,
      {%- endif %}
      password: form.password,
    })
    
    // Redirect to dashboard or intended page
    const redirectTo = router.currentRoute.value.query.redirect as string
    router.push(redirectTo || '/dashboard')
  } catch (error{% if cookiecutter.use_typescript == 'y' %}: any{% endif %}) {
    if (error.response?.data) {
      const data = error.response.data
      
      // Check if email verification is required
      if (data.email_verification_required) {
        // Redirect to email verification page
        router.push({
          name: 'EmailVerificationPending',
          params: { email: data.email || form.email }
        })
        return
      }
      
      errors.email = data.email?.[0] || ''
      errors.password = data.password?.[0] || ''
      errors.general = data.detail || data.non_field_errors?.[0] || 'Invalid credentials'
    } else {
      errors.general = 'An error occurred. Please try again.'
    }
  } finally {
    loading.value = false
  }
}
</script>

