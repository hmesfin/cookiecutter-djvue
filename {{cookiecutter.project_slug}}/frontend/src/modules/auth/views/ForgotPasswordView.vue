<template>
  <div class="min-h-screen bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center p-8">
    <div class="grid grid-cols-1 lg:grid-cols-2 max-w-5xl w-full bg-white rounded-2xl shadow-xl overflow-hidden dark:bg-gray-900 dark:shadow-2xl dark:shadow-gray-900/60">
      <div class="p-8 lg:p-12 flex flex-col justify-center">
        <div class="mb-8">
          <h1 class="text-3xl font-bold text-gray-900 mb-2 dark:text-gray-100">Forgot Password?</h1>
          <p class="text-gray-600 dark:text-gray-400">
            No worries! Enter your email address and we'll send you instructions to reset your password.
          </p>
        </div>

        <form @submit.prevent="handleSubmit" class="space-y-6">
          <div v-if="!isSubmitted" class="space-y-6">
            <div>
              <label for="email" class="block text-sm font-medium text-gray-700 mb-2 dark:text-gray-300">Email Address</label>
              <input 
                id="email"
                v-model="email"
                type="email"
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-colors disabled:bg-gray-50 disabled:cursor-not-allowed dark:border-gray-600 dark:focus:ring-indigo-400 dark:focus:border-indigo-400"
                placeholder="Enter your email address"
                required
                :disabled="loading"
              >
              <p v-if="error" class="mt-2 text-sm text-red-600">{% raw %}{{ error }}{% endraw %}</p>
            </div>

            <button type="submit" class="w-full py-3 px-4 rounded-lg font-semibold text-white bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed" :disabled="loading">
              {% raw %}{{ loading ? 'Sending...' : 'Send Reset Instructions' }}{% endraw %}
            </button>
          </div>

          <div v-else class="text-center p-8 bg-green-50 rounded-lg border border-green-200 dark:bg-green-900/20">
            <div class="w-16 h-16 mx-auto mb-4 text-green-500">
              <IconLucideCheckCircle class="w-full h-full" />
            </div>
            <h2 class="text-2xl font-semibold text-gray-900 mb-2 dark:text-gray-100">Check Your Email</h2>
            <p class="text-gray-600 mb-4 dark:text-gray-400">
              We've sent password reset instructions to <strong class="text-gray-900 dark:text-gray-100">{% raw %}{{ email }}{% endraw %}</strong>
            </p>
            <p class="text-sm text-gray-500 dark:text-gray-500">
              Didn't receive the email? Check your spam folder or 
              <button type="button" @click="resendEmail" class="font-medium text-indigo-600 hover:text-indigo-500 underline transition-colors disabled:opacity-50 disabled:cursor-not-allowed" :disabled="resending">
                {% raw %}{{ resending ? 'Resending...' : 'click here to resend' }}{% endraw %}
              </button>
            </p>
          </div>
        </form>

        <div class="mt-8 text-center">
          <router-link to="/auth/login" class="inline-flex items-center gap-2 text-sm font-medium text-indigo-600 hover:text-indigo-500 transition-colors">
            <IconLucideArrowLeft class="w-5 h-5" />
            Back to Login
          </router-link>
        </div>
      </div>

      <div class="hidden lg:flex bg-gradient-to-br from-indigo-500 to-purple-600 p-12 items-center justify-center">
        <div class="text-white">
          <h2 class="text-2xl font-semibold mb-8">Password Security Tips</h2>
          <ul class="space-y-4">
            <li class="flex items-start gap-3">
              <IconLucideCheckCircle class="w-5 h-5 flex-shrink-0 mt-0.5" />
              <span class="text-sm leading-relaxed">Use a combination of uppercase and lowercase letters</span>
            </li>
            <li class="flex items-start gap-3">
              <IconLucideCheckCircle class="w-5 h-5 flex-shrink-0 mt-0.5" />
              <span class="text-sm leading-relaxed">Include numbers and special characters</span>
            </li>
            <li class="flex items-start gap-3">
              <IconLucideCheckCircle class="w-5 h-5 flex-shrink-0 mt-0.5" />
              <span class="text-sm leading-relaxed">Make your password at least 12 characters long</span>
            </li>
            <li class="flex items-start gap-3">
              <IconLucideCheckCircle class="w-5 h-5 flex-shrink-0 mt-0.5" />
              <span class="text-sm leading-relaxed">Avoid using personal information</span>
            </li>
            <li class="flex items-start gap-3">
              <IconLucideCheckCircle class="w-5 h-5 flex-shrink-0 mt-0.5" />
              <span class="text-sm leading-relaxed">Use unique passwords for each account</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
{% if cookiecutter.use_typescript == 'y' -%}
import { ref } from 'vue'
import { useRouter } from 'vue-router'
{% else -%}
import { ref } from 'vue'
import { useRouter } from 'vue-router'
{%- endif %}

const router = useRouter()

const email = ref('')
const loading = ref(false)
const error = ref('')
const isSubmitted = ref(false)
const resending = ref(false)

const validateEmail = (email{% if cookiecutter.use_typescript == 'y' %}: string{% endif %}) => {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return re.test(email)
}

const handleSubmit = async () => {
  error.value = ''
  
  if (!validateEmail(email.value)) {
    error.value = 'Please enter a valid email address'
    return
  }
  
  loading.value = true
  
  try {
    // In a real app, send reset email via API
    await new Promise(resolve => setTimeout(resolve, 1500))
    
    // Simulate API response
    const emailExists = Math.random() > 0.3 // 70% chance email exists
    
    if (emailExists) {
      isSubmitted.value = true
    } else {
      error.value = 'No account found with this email address'
    }
  } catch (err) {
    console.error('Error sending reset email:', err)
    error.value = 'An error occurred. Please try again later.'
  } finally {
    loading.value = false
  }
}

const resendEmail = async () => {
  resending.value = true
  
  try {
    // In a real app, resend reset email via API
    await new Promise(resolve => setTimeout(resolve, 1500))
    alert('Reset instructions have been resent to your email')
  } catch (err) {
    console.error('Error resending email:', err)
    alert('Failed to resend email. Please try again.')
  } finally {
    resending.value = false
  }
}
</script>