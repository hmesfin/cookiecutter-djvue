<template>
  <div class="auth-form">
    {% if cookiecutter.css_framework == 'tailwindcss' -%}
    <div class="space-y-6">
      <div>
        <h2 class="text-3xl font-bold text-center text-gray-900">Create your account</h2>
        <p class="mt-2 text-center text-sm text-gray-600">
          Or
          <RouterLink to="/auth/login" class="font-medium text-indigo-600 hover:text-indigo-500">
            sign in to your existing account
          </RouterLink>
        </p>
      </div>
      
      <form @submit.prevent="handleRegister" class="space-y-6">
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label for="firstName" class="block text-sm font-medium text-gray-700">First name</label>
            <input
              id="firstName"
              v-model="form.firstName"
              type="text"
              required
              class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
              :class="{ 'border-red-500': errors.firstName }"
            >
            <p v-if="errors.firstName" class="mt-1 text-sm text-red-600">{% raw %}{{ errors.firstName }}{% endraw %}</p>
          </div>

          <div>
            <label for="lastName" class="block text-sm font-medium text-gray-700">Last name</label>
            <input
              id="lastName"
              v-model="form.lastName"
              type="text"
              required
              class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
              :class="{ 'border-red-500': errors.lastName }"
            >
            <p v-if="errors.lastName" class="mt-1 text-sm text-red-600">{% raw %}{{ errors.lastName }}{% endraw %}</p>
          </div>
        </div>

        <div>
          <label for="email" class="block text-sm font-medium text-gray-700">Email address</label>
          <input
            id="email"
            v-model="form.email"
            type="email"
            required
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            :class="{ 'border-red-500': errors.email }"
          >
          <p v-if="errors.email" class="mt-1 text-sm text-red-600">{% raw %}{{ errors.email }}{% endraw %}</p>
        </div>

        <div>
          <label for="password" class="block text-sm font-medium text-gray-700">Password</label>
          <input
            id="password"
            v-model="form.password"
            type="password"
            required
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            :class="{ 'border-red-500': errors.password }"
          >
          <p v-if="errors.password" class="mt-1 text-sm text-red-600">{% raw %}{{ errors.password }}{% endraw %}</p>
        </div>

        <div>
          <label for="confirmPassword" class="block text-sm font-medium text-gray-700">Confirm password</label>
          <input
            id="confirmPassword"
            v-model="form.confirmPassword"
            type="password"
            required
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            :class="{ 'border-red-500': errors.confirmPassword }"
          >
          <p v-if="errors.confirmPassword" class="mt-1 text-sm text-red-600">{% raw %}{{ errors.confirmPassword }}{% endraw %}</p>
        </div>

        <div class="flex items-center">
          <input
            id="terms"
            v-model="form.acceptTerms"
            type="checkbox"
            required
            class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
          >
          <label for="terms" class="ml-2 block text-sm text-gray-900">
            I agree to the
            <a href="#" class="text-indigo-600 hover:text-indigo-500">Terms and Conditions</a>
          </label>
        </div>

        <div>
          <button
            type="submit"
            :disabled="loading"
            class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="loading">Creating account...</span>
            <span v-else>Create account</span>
          </button>
        </div>

        <div v-if="errors.general" class="rounded-md bg-red-50 p-4">
          <p class="text-sm text-red-800">{% raw %}{{ errors.general }}{% endraw %}</p>
        </div>
      </form>
    </div>
    {% else -%}
    <div class="register-form">
      <h2>Create your account</h2>
      <p class="subtitle">
        Or <RouterLink to="/auth/login">sign in to your existing account</RouterLink>
      </p>
      
      <form @submit.prevent="handleRegister">
        <div class="form-row">
          <div class="form-group">
            <label for="firstName">First name</label>
            <input
              id="firstName"
              v-model="form.firstName"
              type="text"
              required
              :class="{ error: errors.firstName }"
            >
            <span v-if="errors.firstName" class="error-message">{% raw %}{{ errors.firstName }}{% endraw %}</span>
          </div>

          <div class="form-group">
            <label for="lastName">Last name</label>
            <input
              id="lastName"
              v-model="form.lastName"
              type="text"
              required
              :class="{ error: errors.lastName }"
            >
            <span v-if="errors.lastName" class="error-message">{% raw %}{{ errors.lastName }}{% endraw %}</span>
          </div>
        </div>

        <div class="form-group">
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

        <div class="form-group">
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

        <div class="form-group">
          <label for="confirmPassword">Confirm password</label>
          <input
            id="confirmPassword"
            v-model="form.confirmPassword"
            type="password"
            required
            :class="{ error: errors.confirmPassword }"
          >
          <span v-if="errors.confirmPassword" class="error-message">{% raw %}{{ errors.confirmPassword }}{% endraw %}</span>
        </div>

        <label class="checkbox">
          <input v-model="form.acceptTerms" type="checkbox" required>
          <span>I agree to the <a href="#">Terms and Conditions</a></span>
        </label>

        <button type="submit" :disabled="loading" class="btn btn-primary btn-block">
          {% raw %}{{ loading ? 'Creating account...' : 'Create account' }}{% endraw %}
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

const router = useRouter()
const authStore = useAuthStore()

const loading = ref(false)
const form = reactive({
  firstName: '',
  lastName: '',
  email: '',
  password: '',
  confirmPassword: '',
  acceptTerms: false,
})

const errors = reactive({
  firstName: '',
  lastName: '',
  email: '',
  password: '',
  confirmPassword: '',
  general: '',
})

const handleRegister = async () => {
  // Clear errors
  Object.keys(errors).forEach(key => {
    errors[key as keyof typeof errors] = ''
  })
  
  // Validate passwords match
  if (form.password !== form.confirmPassword) {
    errors.confirmPassword = 'Passwords do not match'
    return
  }
  
  loading.value = true
  
  try {
    const response = await authStore.register({
      username: form.email,  // Use email as username
      first_name: form.firstName,
      last_name: form.lastName,
      email: form.email,
      password: form.password,
      password2: form.confirmPassword,  // Changed from password_confirm to password2
    })
    
    // Check if email verification is required
    if (response.email_verification_required) {
      // Redirect to email verification page
      router.push({
        name: 'EmailVerificationPending',
        params: { email: form.email }
      })
    } else {
      // Auto-login after registration if email verification is not required
      await authStore.login({
        {% if cookiecutter.api_authentication == 'jwt' or cookiecutter.api_authentication == 'token' -%}
        email: form.email,
        {% else -%}
        username: form.email,
        {%- endif %}
        password: form.password,
      })
      
      // Redirect to dashboard
      router.push('/dashboard')
    }
  } catch (error{% if cookiecutter.use_typescript == 'y' %}: any{% endif %}) {
    if (error.response?.data) {
      const data = error.response.data
      errors.firstName = data.first_name?.[0] || ''
      errors.lastName = data.last_name?.[0] || ''
      errors.email = data.email?.[0] || ''
      errors.password = data.password?.[0] || ''
      errors.general = data.detail || data.non_field_errors?.[0] || 'Registration failed'
    } else {
      errors.general = 'An error occurred. Please try again.'
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
{% if cookiecutter.css_framework == 'none' -%}
.auth-form {
  background: white;
  padding: 2rem;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.register-form h2 {
  margin: 0 0 0.5rem;
  font-size: 1.875rem;
  text-align: center;
}

.subtitle {
  text-align: center;
  color: #666;
  margin-bottom: 2rem;
}

.subtitle a {
  color: var(--primary-color);
  text-decoration: none;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.form-group input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 0.25rem;
  font-size: 1rem;
}

.form-group input:focus {
  outline: none;
  border-color: var(--primary-color);
}

.form-group input.error {
  border-color: #dc3545;
}

.error-message {
  color: #dc3545;
  font-size: 0.875rem;
  margin-top: 0.25rem;
  display: block;
}

.checkbox {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
}

.checkbox a {
  color: var(--primary-color);
  text-decoration: none;
}

.btn-block {
  width: 100%;
}

.alert {
  padding: 0.75rem;
  border-radius: 0.25rem;
  margin-top: 1rem;
}

.alert-error {
  background: #fee;
  color: #c33;
  border: 1px solid #fcc;
}
{%- endif %}
</style>