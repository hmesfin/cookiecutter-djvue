<template>
  <div class="space-y-6">
    <div class="text-center">
      <h2 class="text-3xl font-bold text-gray-900 dark:text-gray-100">Reset your password</h2>
      <p class="mt-2 text-sm text-gray-600 dark:text-gray-400">
        Enter your email address and we'll send you a link to reset your password.
      </p>
    </div>
    
    <BaseCard variant="bordered" padding="lg">
      <form @submit.prevent="handleSubmit" class="space-y-6">
        <BaseInput
          v-model="email"
          type="email"
          label="Email address"
          placeholder="Enter your email"
          required
          :error="error"
          autocomplete="email"
        />

        <BaseButton
          type="submit"
          variant="primary"
          size="lg"
          block
          :loading="loading"
        >
          Send reset link
        </BaseButton>

        <div v-if="success" class="rounded-md bg-green-50 p-4 dark:bg-green-900/20">
          <p class="text-sm text-green-800 dark:text-green-200">
            If an account exists with that email, we've sent a password reset link.
          </p>
        </div>

        <div class="text-center">
          <RouterLink to="/auth/login" class="text-sm text-emerald-600 hover:text-emerald-700">
            Back to login
          </RouterLink>
        </div>
      </form>
    </BaseCard>
  </div>
</template>

<script setup{% if cookiecutter.use_typescript == 'y' %} lang="ts"{% endif %}>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { BaseButton, BaseCard, BaseInput } from '@/components/base'

const authStore = useAuthStore()

const email = ref('')
const loading = ref(false)
const success = ref(false)
const error = ref('')

const handleSubmit = async () => {
  error.value = ''
  success.value = false
  loading.value = true
  
  try {
    await authStore.requestPasswordReset(email.value)
    success.value = true
    email.value = ''
  } catch (err{% if cookiecutter.use_typescript == 'y' %}: any{% endif %}) {
    if (err.response?.data?.email) {
      error.value = err.response.data.email[0]
    } else if (err.response?.data?.detail) {
      error.value = err.response.data.detail
    } else {
      error.value = 'An error occurred. Please try again.'
    }
  } finally {
    loading.value = false
  }
}
</script>