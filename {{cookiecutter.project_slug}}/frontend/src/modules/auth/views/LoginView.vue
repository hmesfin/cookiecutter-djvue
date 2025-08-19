<template>
  <div class="space-y-6">
    <div class="text-center">
      <h2 class="text-3xl font-bold text-gray-900 dark:text-gray-100">Welcome back</h2>
      <p class="mt-2 text-sm text-gray-600 dark:text-gray-400">
        Or
        <RouterLink to="/auth/register" class="font-medium text-emerald-600 hover:text-emerald-600">
          create a new account
        </RouterLink>
      </p>
    </div>
    
    <BaseCard variant="bordered" padding="lg">
      <form @submit.prevent="handleLogin" class="space-y-6">
        <BaseInput
          v-model="form.email"
          type="email"
          label="Email address"
          placeholder="Enter your email"
          required
          :error="errors.email"
          autocomplete="email"
        />

        <BaseInput
          v-model="form.password"
          type="password"
          label="Password"
          placeholder="Enter your password"
          required
          :error="errors.password"
          autocomplete="current-password"
        />

        <div class="flex items-center justify-between">
          <BaseCheckbox
            v-model="form.remember"
            label="Remember me"
          />

          <RouterLink to="/auth/forgot-password" class="text-sm text-emerald-600 hover:text-emerald-600">
            Forgot your password?
          </RouterLink>
        </div>

        <BaseButton
          type="submit"
          variant="primary"
          size="lg"
          block
          :loading="loading"
        >
          Sign in
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