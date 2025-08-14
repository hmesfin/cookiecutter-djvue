<template>
  <div class="min-h-screen bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center p-8">
    <div class="max-w-lg w-full">
      <div class="bg-white rounded-2xl shadow-xl p-12 dark:bg-gray-900 dark:shadow-2xl dark:shadow-gray-900/60">
        <!-- Verification Pending -->
        <div v-if="status === 'pending'" class="text-center">
          <div class="w-20 h-20 mx-auto mb-6 rounded-full bg-blue-100 flex items-center justify-center">
            <IconLucideMail class="w-10 h-10 text-blue-500" />
          </div>
          <h1 class="text-3xl font-bold text-gray-900 mb-2 dark:text-gray-100">Verify Your Email</h1>
          <p class="text-gray-600 mb-2 dark:text-gray-400">
            We've sent a verification email to <strong class="text-gray-800 font-semibold dark:text-gray-200">{% raw %}{{ email || 'your email address' }}{% endraw %}</strong>
          </p>
          <p class="text-gray-500 text-sm mb-8 dark:text-gray-500">
            Please check your inbox and click the verification link to activate your account.
          </p>
          
          <div class="flex gap-4 justify-center mb-12">
            <button @click="resendEmail" class="px-6 py-3 rounded-lg font-medium text-white bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed" :disabled="resending || cooldown > 0">
              {% raw %}{{ cooldown > 0 ? `Resend in ${cooldown}s` : (resending ? 'Sending...' : 'Resend Email') }}{% endraw %}
            </button>
            <router-link to="/auth/login" class="px-6 py-3 rounded-lg font-medium text-gray-700 bg-gray-200 hover:bg-gray-300 transition-all duration-200 dark:text-gray-300 dark:bg-gray-700">
              Back to Login
            </router-link>
          </div>
          
          <div class="mt-12 pt-8 border-t border-gray-200 text-left dark:border-gray-700">
            <h3 class="text-base font-semibold text-gray-800 mb-4 dark:text-gray-200">Didn't receive the email?</h3>
            <ul class="space-y-2">
              <li class="flex items-start">
                <span class="text-gray-400 mr-2 font-bold dark:text-gray-600">•</span>
                <span class="text-gray-600 text-sm dark:text-gray-400">Check your spam or junk folder</span>
              </li>
              <li class="flex items-start">
                <span class="text-gray-400 mr-2 font-bold dark:text-gray-600">•</span>
                <span class="text-gray-600 text-sm dark:text-gray-400">Make sure you entered the correct email address</span>
              </li>
              <li class="flex items-start">
                <span class="text-gray-400 mr-2 font-bold dark:text-gray-600">•</span>
                <span class="text-gray-600 text-sm dark:text-gray-400">Add our email to your contacts to prevent filtering</span>
              </li>
              <li class="flex items-start">
                <span class="text-gray-400 mr-2 font-bold dark:text-gray-600">•</span>
                <span class="text-gray-600 text-sm dark:text-gray-400">Wait a few minutes - emails can sometimes be delayed</span>
              </li>
            </ul>
          </div>
        </div>

        <!-- Verifying -->
        <div v-else-if="status === 'verifying'" class="text-center">
          <div class="w-16 h-16 mx-auto mb-8">
            <div class="w-full h-full border-4 border-gray-200 border-t-indigo-500 rounded-full animate-spin dark:border-gray-700"></div>
          </div>
          <h1 class="text-3xl font-bold text-gray-900 mb-4 dark:text-gray-100">Verifying Your Email</h1>
          <p class="text-gray-600 dark:text-gray-400">Please wait while we verify your email address...</p>
        </div>

        <!-- Success -->
        <div v-else-if="status === 'success'" class="text-center">
          <div class="w-20 h-20 mx-auto mb-6 rounded-full bg-green-100 flex items-center justify-center">
            <IconLucideCheckCircle class="w-10 h-10 text-green-500" />
          </div>
          <h1 class="text-3xl font-bold text-gray-900 mb-4 dark:text-gray-100">Email Verified Successfully!</h1>
          <p class="text-gray-600 mb-8 dark:text-gray-400">
            Your email has been verified and your account is now active.
          </p>
          <div class="flex justify-center">
            <router-link to="/dashboard" class="px-8 py-3 rounded-lg font-semibold text-white bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 transform hover:-translate-y-1 transition-all duration-200 shadow-lg hover:shadow-xl dark:shadow-2xl dark:shadow-gray-900/50">
              Go to Dashboard
            </router-link>
          </div>
        </div>

        <!-- Already Verified -->
        <div v-else-if="status === 'already_verified'" class="text-center">
          <div class="w-20 h-20 mx-auto mb-6 rounded-full bg-teal-100 flex items-center justify-center">
            <IconLucideInfo class="w-10 h-10 text-teal-500" />
          </div>
          <h1 class="text-3xl font-bold text-gray-900 mb-4 dark:text-gray-100">Already Verified</h1>
          <p class="text-gray-600 mb-8 dark:text-gray-400">
            Your email address has already been verified.
          </p>
          <div class="flex gap-4 justify-center">
            <router-link to="/dashboard" class="px-6 py-3 rounded-lg font-semibold text-white bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 transform hover:-translate-y-1 transition-all duration-200 shadow-lg hover:shadow-xl dark:shadow-2xl dark:shadow-gray-900/50">
              Go to Dashboard
            </router-link>
            <router-link to="/auth/login" class="px-6 py-3 rounded-lg font-semibold text-gray-700 bg-gray-200 hover:bg-gray-300 transition-all duration-200 dark:text-gray-300 dark:bg-gray-700">
              Back to Login
            </router-link>
          </div>
        </div>

        <!-- Error -->
        <div v-else-if="status === 'error'" class="text-center">
          <div class="w-20 h-20 mx-auto mb-6 rounded-full bg-red-100 flex items-center justify-center">
            <IconLucideAlertCircle class="w-6 h-6" />
          </div>
          <h1 class="text-3xl font-bold text-gray-900 mb-4 dark:text-gray-100">Verification Failed</h1>
          <p class="text-gray-600 mb-8 dark:text-gray-400">
            {% raw %}{{ errorMessage || 'The verification link is invalid or has expired.' }}{% endraw %}
          </p>
          <div class="flex gap-4 justify-center">
            <button @click="requestNewLink" class="px-6 py-3 rounded-lg font-semibold text-white bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 transition-all duration-200">
              Request New Link
            </button>
            <router-link to="/auth/login" class="px-6 py-3 rounded-lg font-semibold text-gray-700 bg-gray-200 hover:bg-gray-300 transition-all duration-200 dark:text-gray-300 dark:bg-gray-700">
              Back to Login
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup{% if cookiecutter.use_typescript == 'y' %} lang="ts"{% endif %}>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import axios from '@/services/api'

{% if cookiecutter.use_typescript == 'y' -%}
type VerificationStatus = 'pending' | 'verifying' | 'success' | 'already_verified' | 'error'
{%- endif %}

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const status = ref({% if cookiecutter.use_typescript == 'y' %}<VerificationStatus>{% endif %}'pending')
const email = ref('')
const resending = ref(false)
const cooldown = ref(0)
const errorMessage = ref('')
let cooldownInterval = null

onMounted(() => {
  // Check if we have verification token in URL
  const { uid, token } = route.query
  
  if (uid && token) {
    // Automatically verify if we have the token
    verifyEmail(uid, token)
  } else {
    // Show pending verification screen
    // Get email from route params or auth store
    email.value = route.params.email || authStore.user?.email || ''
  }
})

onUnmounted(() => {
  if (cooldownInterval) {
    clearInterval(cooldownInterval)
  }
})

const verifyEmail = async (uid{% if cookiecutter.use_typescript == 'y' %}: string{% endif %}, token{% if cookiecutter.use_typescript == 'y' %}: string{% endif %}) => {
  status.value = 'verifying'
  
  try {
    const response = await axios.post(`/auth/verify-email/${uid}/${token}/`)
    
    if (response.data.already_verified) {
      status.value = 'already_verified'
    } else {
      status.value = 'success'
      
      // Update user in auth store if logged in
      if (authStore.isAuthenticated && response.data.user) {
        authStore.user = response.data.user
      }
      
      // Redirect to dashboard after 3 seconds
      setTimeout(() => {
        router.push('/dashboard')
      }, 3000)
    }
  } catch (error) {
    status.value = 'error'
    errorMessage.value = error.response?.data?.message || 'Verification failed. Please try again.'
  }
}

const resendEmail = async () => {
  if (cooldown.value > 0 || !email.value) return
  
  resending.value = true
  
  try {
    const response = await axios.post('/auth/resend-verification/', {
      email: email.value
    })
    
    if (response.data.already_verified) {
      status.value = 'already_verified'
    } else {
      alert('Verification email sent! Please check your inbox.')
      startCooldown()
    }
  } catch (error) {
    alert('Failed to resend email. Please try again.')
  } finally {
    resending.value = false
  }
}

const startCooldown = () => {
  cooldown.value = 60 // 60 seconds cooldown
  
  cooldownInterval = setInterval(() => {
    cooldown.value--
    if (cooldown.value <= 0) {
      clearInterval(cooldownInterval)
      cooldownInterval = null
    }
  }, 1000)
}

const requestNewLink = () => {
  // Show form to enter email
  const userEmail = prompt('Please enter your email address:')
  if (userEmail) {
    email.value = userEmail
    status.value = 'pending'
    resendEmail()
  }
}
</script>