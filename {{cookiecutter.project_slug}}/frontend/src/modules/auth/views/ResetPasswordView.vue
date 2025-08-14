<template>
  <div class="min-h-screen bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center p-8">
    <div class="max-w-lg w-full bg-white rounded-2xl shadow-xl overflow-hidden dark:bg-gray-900 dark:shadow-2xl dark:shadow-gray-900/60">
      <div class="p-8">
        <div class="mb-8">
          <h1 class="text-3xl font-bold text-gray-900 mb-2 dark:text-gray-100">Reset Your Password</h1>
          <p class="text-gray-600 dark:text-gray-400">
            Enter your new password below. Make sure it's strong and secure.
          </p>
        </div>

        <form @submit.prevent="handleSubmit" class="space-y-6">
          <div v-if="!isReset" class="space-y-6">
            <div>
              <label for="password" class="block text-sm font-medium text-gray-700 mb-2 dark:text-gray-300">New Password</label>
              <PasswordInput
                id="password"
                v-model="password"
                :required="true"
                placeholder="Enter new password"
                :disabled="loading"
                :show-strength="true"
                @input="checkPasswordStrength"
                class="w-full"
              />
              
              <!-- Password Requirements -->
              <ul class="mt-2 space-y-1 text-xs">
                <li :class="requirements.length ? 'text-green-600' : 'text-gray-400'" class="flex items-center gap-2">
                  <IconLucideCheckCircle class="w-4 h-4" />
                  At least 8 characters
                </li>
                <li :class="requirements.uppercase ? 'text-green-600' : 'text-gray-400'" class="flex items-center gap-2">
                  <IconLucideCheckCircle class="w-4 h-4" />
                  One uppercase letter
                </li>
                <li :class="requirements.lowercase ? 'text-green-600' : 'text-gray-400'" class="flex items-center gap-2">
                  <IconLucideCheckCircle class="w-4 h-4" />
                  One lowercase letter
                </li>
                <li :class="requirements.number ? 'text-green-600' : 'text-gray-400'" class="flex items-center gap-2">
                  <IconLucideCheckCircle class="w-4 h-4" />
                  One number
                </li>
                <li :class="requirements.special ? 'text-green-600' : 'text-gray-400'" class="flex items-center gap-2">
                  <IconLucideCheckCircle class="w-4 h-4" />
                  One special character
                </li>
              </ul>
            </div>

            <div>
              <label for="confirmPassword" class="block text-sm font-medium text-gray-700 mb-2 dark:text-gray-300">Confirm New Password</label>
              <PasswordInput
                id="confirmPassword"
                v-model="confirmPassword"
                :required="true"
                placeholder="Confirm new password"
                :disabled="loading"
                class="w-full"
              />
              <p v-if="error" class="mt-2 text-sm text-red-600">{% raw %}{{ error }}{% endraw %}</p>
            </div>

            <button type="submit" class="w-full py-3 px-4 rounded-lg font-semibold text-white bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed" :disabled="loading || !isValidPassword">
              {% raw %}{{ loading ? 'Resetting...' : 'Reset Password' }}{% endraw %}
            </button>
          </div>

          <div v-else class="text-center p-8 bg-green-50 rounded-lg border border-green-200 dark:bg-green-900/20">
            <div class="w-16 h-16 mx-auto mb-4 text-green-500">
              <IconLucideCheckCircle class="w-full h-full" />
            </div>
            <h2 class="text-2xl font-semibold text-gray-900 mb-2 dark:text-gray-100">Password Reset Successful!</h2>
            <p class="text-gray-600 mb-6 dark:text-gray-400">
              Your password has been successfully reset. You can now log in with your new password.
            </p>
            <router-link to="/auth/login" class="inline-block px-8 py-3 rounded-lg font-semibold text-white bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 transition-all duration-200">
              Go to Login
            </router-link>
          </div>
        </form>

        <div v-if="!isReset" class="mt-8 text-center">
          <router-link to="/auth/login" class="inline-flex items-center gap-2 text-sm font-medium text-indigo-600 hover:text-indigo-500 transition-colors">
            <IconLucideArrowLeft class="w-5 h-5" />
            Back to Login
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
{% if cookiecutter.use_typescript == 'y' -%}
import { ref, computed, reactive, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import PasswordInput from '@/components/PasswordInput.vue'

interface PasswordRequirements {
  length: boolean
  uppercase: boolean
  lowercase: boolean
  number: boolean
  special: boolean
}

interface PasswordStrength {
  percentage: number
  level: string
  text: string
}
{% else -%}
import { ref, computed, reactive, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import PasswordInput from '@/components/PasswordInput.vue'
{%- endif %}

const router = useRouter()
const route = useRoute()

const password = ref('')
const confirmPassword = ref('')
const loading = ref(false)
const error = ref('')
const isReset = ref(false)
const resetToken = ref('')

const requirements = reactive({% if cookiecutter.use_typescript == 'y' %}<PasswordRequirements>{% endif %}{
  length: false,
  uppercase: false,
  lowercase: false,
  number: false,
  special: false
})

const passwordStrength = reactive({% if cookiecutter.use_typescript == 'y' %}<PasswordStrength>{% endif %}{
  percentage: 0,
  level: '',
  text: ''
})

const isValidPassword = computed(() => {
  return Object.values(requirements).every(req => req === true)
})

onMounted(() => {
  // Get reset token from URL query params
  resetToken.value = route.query.token || ''
  
  if (!resetToken.value) {
    // If no token, redirect to forgot password page
    router.push('/auth/forgot-password')
  }
})

const checkPasswordStrength = () => {
  const pwd = password.value
  
  // Check requirements
  requirements.length = pwd.length >= 8
  requirements.uppercase = /[A-Z]/.test(pwd)
  requirements.lowercase = /[a-z]/.test(pwd)
  requirements.number = /\d/.test(pwd)
  requirements.special = /[!@#$%^&*(),.?":{}|<>]/.test(pwd)
  
  // Calculate strength
  let strength = 0
  if (requirements.length) strength += 20
  if (requirements.uppercase) strength += 20
  if (requirements.lowercase) strength += 20
  if (requirements.number) strength += 20
  if (requirements.special) strength += 20
  
  passwordStrength.percentage = strength
  
  if (strength === 0) {
    passwordStrength.level = ''
    passwordStrength.text = ''
  } else if (strength <= 40) {
    passwordStrength.level = 'weak'
    passwordStrength.text = 'Weak'
  } else if (strength <= 60) {
    passwordStrength.level = 'fair'
    passwordStrength.text = 'Fair'
  } else if (strength <= 80) {
    passwordStrength.level = 'good'
    passwordStrength.text = 'Good'
  } else {
    passwordStrength.level = 'strong'
    passwordStrength.text = 'Strong'
  }
}

const handleSubmit = async () => {
  error.value = ''
  
  if (password.value !== confirmPassword.value) {
    error.value = 'Passwords do not match'
    return
  }
  
  if (!isValidPassword.value) {
    error.value = 'Please meet all password requirements'
    return
  }
  
  loading.value = true
  
  try {
    // In a real app, send password reset request to API
    await new Promise(resolve => setTimeout(resolve, 1500))
    
    // Simulate API response
    const success = Math.random() > 0.2 // 80% success rate
    
    if (success) {
      isReset.value = true
    } else {
      error.value = 'Invalid or expired reset token. Please request a new password reset.'
    }
  } catch (err) {
    console.error('Error resetting password:', err)
    error.value = 'An error occurred. Please try again later.'
  } finally {
    loading.value = false
  }
}
</script>