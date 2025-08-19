<template>
  <div class="space-y-6">
    <div class="text-center">
      <h2 class="text-3xl font-bold text-gray-900 dark:text-gray-100">Create your account</h2>
      <p class="mt-2 text-sm text-gray-600 dark:text-gray-400">
        Or
        <RouterLink to="/auth/login" class="font-medium text-emerald-600 hover:text-emerald-600">
          sign in to your existing account
        </RouterLink>
      </p>
    </div>
    
    <BaseCard variant="bordered" padding="lg">
      <form @submit.prevent="handleRegister" class="space-y-6">
        <div class="grid grid-cols-2 gap-4">
          <BaseInput
            v-model="form.firstName"
            type="text"
            label="First name"
            placeholder="John"
            required
            :error="errors.firstName"
            autocomplete="given-name"
          />

          <BaseInput
            v-model="form.lastName"
            type="text"
            label="Last name"
            placeholder="Doe"
            required
            :error="errors.lastName"
            autocomplete="family-name"
          />
        </div>

        <BaseInput
          v-model="form.email"
          type="email"
          label="Email address"
          placeholder="john.doe@example.com"
          required
          :error="errors.email"
          autocomplete="email"
        />

        <BaseInput
          v-model="form.password"
          type="password"
          label="Password"
          placeholder="Create a strong password"
          required
          :error="errors.password"
          autocomplete="new-password"
          hint="Must be at least 8 characters"
        />

        <BaseInput
          v-model="form.confirmPassword"
          type="password"
          label="Confirm password"
          placeholder="Re-enter your password"
          required
          :error="errors.confirmPassword"
          autocomplete="new-password"
        />

        <BaseCheckbox
          v-model="form.acceptTerms"
          required
        >
          I agree to the
          <a href="#" class="text-emerald-600 hover:text-emerald-600">Terms and Conditions</a>
        </BaseCheckbox>

        <BaseButton
          type="submit"
          variant="primary"
          size="lg"
          block
          :loading="loading"
        >
          Create account
        </BaseButton>

        <div v-if="errors.general" class="rounded-md bg-red-50 p-4 dark:bg-red-900/20">
          <p class="text-sm text-red-800 dark:text-red-200">{% raw %}{{ errors.general }}{% endraw %}</p>
        </div>
      </form>

      {% if cookiecutter.use_social_auth == 'y' -%}
      <div class="mt-6">
        <div class="relative">
          <div class="absolute inset-0 flex items-center">
            <div class="w-full border-t border-gray-300 dark:border-gray-600"></div>
          </div>
          <div class="relative flex justify-center text-sm">
            <span class="px-2 bg-white text-gray-500 dark:bg-gray-800 dark:text-gray-400">Or continue with</span>
          </div>
        </div>

        <div class="mt-6">
          <SocialAuthButtons />
        </div>
      </div>
      {%- endif %}
    </BaseCard>
  </div>
</template>

<script setup{% if cookiecutter.use_typescript == 'y' %} lang="ts"{% endif %}>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { BaseButton, BaseCard, BaseInput, BaseCheckbox } from '@/components/base'
{% if cookiecutter.use_social_auth == 'y' -%}
import SocialAuthButtons from '@/components/auth/SocialAuthButtons.vue'
{%- endif %}

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

const validateForm = () => {
  let isValid = true
  
  // Clear errors
  Object.keys(errors).forEach(key => {
    errors[key] = ''
  })
  
  // Validate first name
  if (!form.firstName.trim()) {
    errors.firstName = 'First name is required'
    isValid = false
  }
  
  // Validate last name
  if (!form.lastName.trim()) {
    errors.lastName = 'Last name is required'
    isValid = false
  }
  
  // Validate email
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!emailRegex.test(form.email)) {
    errors.email = 'Please enter a valid email address'
    isValid = false
  }
  
  // Validate password
  if (form.password.length < 8) {
    errors.password = 'Password must be at least 8 characters'
    isValid = false
  }
  
  // Validate password confirmation
  if (form.password !== form.confirmPassword) {
    errors.confirmPassword = 'Passwords do not match'
    isValid = false
  }
  
  // Validate terms acceptance
  if (!form.acceptTerms) {
    errors.general = 'You must accept the terms and conditions'
    isValid = false
  }
  
  return isValid
}

const handleRegister = async () => {
  if (!validateForm()) {
    return
  }
  
  loading.value = true
  
  try {
    await authStore.register({
      first_name: form.firstName,
      last_name: form.lastName,
      email: form.email,
      {% if cookiecutter.api_authentication == 'jwt' or cookiecutter.api_authentication == 'token' -%}
      username: form.email,
      {%- endif %}
      password: form.password,
      password_confirm: form.confirmPassword,
    })
    
    // Check if email verification is required
    if (authStore.requiresEmailVerification) {
      router.push({
        name: 'EmailVerificationPending',
        params: { email: form.email }
      })
    } else {
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
      errors.confirmPassword = data.password_confirm?.[0] || ''
      errors.general = data.detail || data.non_field_errors?.[0] || 'Registration failed'
    } else {
      errors.general = 'An error occurred. Please try again.'
    }
  } finally {
    loading.value = false
  }
}
</script>