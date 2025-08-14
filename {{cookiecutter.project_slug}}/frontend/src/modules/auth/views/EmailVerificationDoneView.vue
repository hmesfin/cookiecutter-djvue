<template>
  <div class="min-h-screen bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center p-8">
    <div class="max-w-2xl w-full">
      <div class="bg-white rounded-2xl shadow-xl overflow-hidden dark:bg-gray-900 dark:shadow-2xl dark:shadow-gray-900/60">
        <!-- Success State -->
        <div v-if="verificationStatus === 'success'" class="p-12 text-center">
          <div class="w-20 h-20 mx-auto mb-8 rounded-full bg-gradient-to-br from-green-400 to-green-600 flex items-center justify-center">
            <IconLucideCheckCircle class="w-10 h-10 text-white animate-pulse" />
          </div>
          
          <h1 class="text-3xl font-bold text-gray-900 mb-4 dark:text-gray-100">Email Verified Successfully!</h1>
          
          <p class="text-lg text-gray-600 mb-8 dark:text-gray-400">
            Your email has been verified and your account is now fully activated.
          </p>
          
          <div class="bg-gray-50 border-l-4 border-indigo-500 p-6 mb-8 text-left dark:bg-gray-900">
            <p class="text-gray-700 mb-2 dark:text-gray-300">Welcome to <strong class="text-indigo-600">{{ cookiecutter.project_name }}</strong>!</p>
            <p class="text-gray-600 dark:text-gray-400">You can now access all features of your account.</p>
          </div>
          
          <div class="flex gap-4 justify-center mb-8 flex-wrap">
            <router-link to="/dashboard" class="px-8 py-3 rounded-lg font-semibold text-white bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 transform hover:-translate-y-1 transition-all duration-200 shadow-lg hover:shadow-xl dark:shadow-2xl dark:shadow-gray-900/50">
              Go to Dashboard
            </router-link>
            <router-link to="/profile" class="px-8 py-3 rounded-lg font-semibold text-indigo-600 bg-white border-2 border-indigo-500 hover:bg-indigo-500 hover:text-white transition-all duration-200 dark:bg-gray-900">
              Complete Your Profile
            </router-link>
          </div>
          
          <div class="bg-gray-50 rounded-lg p-6 text-left dark:bg-gray-900">
            <h3 class="text-lg font-semibold text-gray-800 mb-4 dark:text-gray-200">What's Next?</h3>
            <ul class="space-y-2">
              <li class="flex items-start">
                <span class="text-green-500 mr-2 font-bold">✓</span>
                <span class="text-gray-600 dark:text-gray-400">Explore your dashboard</span>
              </li>
              <li class="flex items-start">
                <span class="text-green-500 mr-2 font-bold">✓</span>
                <span class="text-gray-600 dark:text-gray-400">Complete your profile information</span>
              </li>
              <li class="flex items-start">
                <span class="text-green-500 mr-2 font-bold">✓</span>
                <span class="text-gray-600 dark:text-gray-400">Check out our getting started guide</span>
              </li>
              <li class="flex items-start">
                <span class="text-green-500 mr-2 font-bold">✓</span>
                <span class="text-gray-600 dark:text-gray-400">Connect with other users</span>
              </li>
            </ul>
          </div>
        </div>

        <!-- Already Verified State -->
        <div v-else-if="verificationStatus === 'already_verified'" class="p-12 text-center">
          <div class="w-20 h-20 mx-auto mb-8 rounded-full bg-gradient-to-br from-blue-400 to-blue-600 flex items-center justify-center">
            <IconLucideInfo class="w-10 h-10 text-white" />
          </div>
          
          <h1 class="text-3xl font-bold text-gray-900 mb-4 dark:text-gray-100">Already Verified</h1>
          
          <p class="text-lg text-gray-600 mb-8 dark:text-gray-400">
            Your email address has already been verified.
          </p>
          
          <div class="flex gap-4 justify-center flex-wrap">
            <router-link to="/dashboard" class="px-8 py-3 rounded-lg font-semibold text-white bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 transform hover:-translate-y-1 transition-all duration-200 shadow-lg hover:shadow-xl dark:shadow-2xl dark:shadow-gray-900/50">
              Go to Dashboard
            </router-link>
            <router-link to="/auth/login" class="px-8 py-3 rounded-lg font-semibold text-indigo-600 bg-white border-2 border-indigo-500 hover:bg-indigo-500 hover:text-white transition-all duration-200 dark:bg-gray-900">
              Sign In
            </router-link>
          </div>
        </div>

        <!-- Error State -->
        <div v-else-if="verificationStatus === 'error'" class="p-12 text-center">
          <div class="w-20 h-20 mx-auto mb-8 rounded-full bg-gradient-to-br from-red-400 to-red-600 flex items-center justify-center">
            <IconLucideAlertCircle class="w-6 h-6" />
          </div>
          
          <h1 class="text-3xl font-bold text-gray-900 mb-4 dark:text-gray-100">Verification Failed</h1>
          
          <p class="text-lg text-gray-600 mb-8 dark:text-gray-400">
            {% raw %}{{ errorMessage || 'The verification link is invalid or has expired.' }}{% endraw %}
          </p>
          
          <div class="flex gap-4 justify-center mb-8 flex-wrap">
            <router-link to="/auth/verify-email" class="px-8 py-3 rounded-lg font-semibold text-white bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 transform hover:-translate-y-1 transition-all duration-200 shadow-lg hover:shadow-xl dark:shadow-2xl dark:shadow-gray-900/50">
              Request New Link
            </router-link>
            <router-link to="/auth/login" class="px-8 py-3 rounded-lg font-semibold text-indigo-600 bg-white border-2 border-indigo-500 hover:bg-indigo-500 hover:text-white transition-all duration-200 dark:bg-gray-900">
              Back to Login
            </router-link>
          </div>
          
          <div class="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
            <p class="text-gray-500 text-sm dark:text-gray-500">If you continue to have issues, please contact support.</p>
          </div>
        </div>

        <!-- Loading State -->
        <div v-else class="p-12 text-center">
          <div class="w-16 h-16 mx-auto mb-8">
            <div class="w-full h-full border-4 border-gray-200 border-t-indigo-500 rounded-full animate-spin dark:border-gray-700"></div>
          </div>
          <h1 class="text-3xl font-bold text-gray-900 mb-4 dark:text-gray-100">Verifying Your Email</h1>
          <p class="text-lg text-gray-600 dark:text-gray-400">Please wait while we verify your email address...</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup{% if cookiecutter.use_typescript == 'y' %} lang="ts"{% endif %}>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import axios from '@/services/api'

{% if cookiecutter.use_typescript == 'y' -%}
type VerificationStatus = 'loading' | 'success' | 'already_verified' | 'error'
{%- endif %}

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const verificationStatus = ref({% if cookiecutter.use_typescript == 'y' %}<VerificationStatus>{% endif %}'loading')
const errorMessage = ref('')

onMounted(async () => {
  const { uid, token } = route.params
  
  if (!uid || !token) {
    verificationStatus.value = 'error'
    errorMessage.value = 'Invalid verification link'
    return
  }
  
  try {
    const response = await axios.post(`/auth/verify-email/${uid}/${token}/`)
    
    if (response.data.already_verified) {
      verificationStatus.value = 'already_verified'
    } else {
      verificationStatus.value = 'success'
      
      // Update user in auth store if logged in
      if (authStore.isAuthenticated && response.data.user) {
        authStore.user = response.data.user
      }
      
      // Auto-redirect to dashboard after 5 seconds
      setTimeout(() => {
        router.push('/dashboard')
      }, 5000)
    }
  } catch (error{% if cookiecutter.use_typescript == 'y' %}: any{% endif %}) {
    verificationStatus.value = 'error'
    errorMessage.value = error.response?.data?.message || 'Verification failed. Please try again.'
  }
})
</script>