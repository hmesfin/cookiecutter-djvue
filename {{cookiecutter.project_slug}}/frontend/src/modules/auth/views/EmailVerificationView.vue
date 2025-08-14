<template>
  <div class="email-verification-view">
    <div class="verification-container">
      <div class="verification-card">
        <!-- Verification Pending -->
        <div v-if="{% raw %}status === 'pending'{% endraw %}" class="verification-content">
          <div class="icon-wrapper pending">
            <svg class="icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
            </svg>
          </div>
          <h1 class="title">Verify Your Email</h1>
          <p class="description">
            We've sent a verification email to <strong>{% raw %}{{ email || 'your email address' }}{% endraw %}</strong>
          </p>
          <p class="instruction">
            Please check your inbox and click the verification link to activate your account.
          </p>
          
          <div class="action-buttons">
            <button @click="resendEmail" class="btn btn-primary" :disabled="resending || cooldown > 0">
              {% raw %}{{ cooldown > 0 ? `Resend in ${cooldown}s` : (resending ? 'Sending...' : 'Resend Email') }}{% endraw %}
            </button>
            <router-link to="/auth/login" class="btn btn-secondary">
              Back to Login
            </router-link>
          </div>
          
          <div class="tips">
            <h3>Didn't receive the email?</h3>
            <ul>
              <li>Check your spam or junk folder</li>
              <li>Make sure you entered the correct email address</li>
              <li>Add our email to your contacts to prevent filtering</li>
              <li>Wait a few minutes - emails can sometimes be delayed</li>
            </ul>
          </div>
        </div>

        <!-- Verifying -->
        <div v-else-if="{% raw %}status === 'verifying'{% endraw %}" class="verification-content">
          <div class="spinner">
            <div class="spinner-circle"></div>
          </div>
          <h1 class="title">Verifying Your Email</h1>
          <p class="description">Please wait while we verify your email address...</p>
        </div>

        <!-- Success -->
        <div v-else-if="{% raw %}status === 'success'{% endraw %}" class="verification-content">
          <div class="icon-wrapper success">
            <svg class="icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
          </div>
          <h1 class="title">Email Verified Successfully!</h1>
          <p class="description">
            Your email has been verified and your account is now active.
          </p>
          <div class="action-buttons">
            <router-link to="/dashboard" class="btn btn-primary">
              Go to Dashboard
            </router-link>
          </div>
        </div>

        <!-- Already Verified -->
        <div v-else-if="{% raw %}status === 'already_verified'{% endraw %}" class="verification-content">
          <div class="icon-wrapper info">
            <svg class="icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
          </div>
          <h1 class="title">Already Verified</h1>
          <p class="description">
            Your email address has already been verified.
          </p>
          <div class="action-buttons">
            <router-link to="/dashboard" class="btn btn-primary">
              Go to Dashboard
            </router-link>
            <router-link to="/auth/login" class="btn btn-secondary">
              Back to Login
            </router-link>
          </div>
        </div>

        <!-- Error -->
        <div v-else-if="{% raw %}status === 'error'{% endraw %}" class="verification-content">
          <div class="icon-wrapper error">
            <svg class="icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
          </div>
          <h1 class="title">Verification Failed</h1>
          <p class="description">
            {% raw %}{{ errorMessage || 'The verification link is invalid or has expired.' }}{% endraw %}
          </p>
          <div class="action-buttons">
            <button @click="requestNewLink" class="btn btn-primary">
              Request New Link
            </button>
            <router-link to="/auth/login" class="btn btn-secondary">
              Back to Login
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
{% if cookiecutter.use_typescript == 'y' -%}
import { ref, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import axios from '@/services/api'

type VerificationStatus = {% raw %}'pending' | 'verifying' | 'success' | 'already_verified' | 'error'{% endraw %}
{% else -%}
import { ref, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import axios from '@/services/api'
{%- endif %}

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const status = ref({% if cookiecutter.use_typescript == 'y' %}<VerificationStatus>{% endif %}{% raw %}'pending'{% endraw %})
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
  status.value = {% raw %}'verifying'{% endraw %}
  
  try {
    const response = await axios.post(`/auth/verify-email/${uid}/${token}/`)
    
    if (response.data.already_verified) {
      status.value = {% raw %}'already_verified'{% endraw %}
    } else {
      status.value = {% raw %}'success'{% endraw %}
      
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
    status.value = {% raw %}'error'{% endraw %}
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
      status.value = {% raw %}'already_verified'{% endraw %}
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
    status.value = {% raw %}'pending'{% endraw %}
    resendEmail()
  }
}
</script>

<style scoped>
.email-verification-view {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.verification-container {
  max-width: 500px;
  width: 100%;
}

.verification-card {
  background: white;
  border-radius: 1rem;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  padding: 3rem;
}

.verification-content {
  text-align: center;
}

.icon-wrapper {
  width: 80px;
  height: 80px;
  margin: 0 auto 1.5rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon-wrapper.pending {
  background: #ebf8ff;
  color: #4299e1;
}

.icon-wrapper.success {
  background: #f0fdf4;
  color: #48bb78;
}

.icon-wrapper.info {
  background: #e6fffa;
  color: #38b2ac;
}

.icon-wrapper.error {
  background: #fff5f5;
  color: #f56565;
}

.icon {
  width: 40px;
  height: 40px;
}

.spinner {
  margin: 2rem auto;
}

.spinner-circle {
  width: 60px;
  height: 60px;
  border: 4px solid #e2e8f0;
  border-top-color: #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.title {
  font-size: 1.75rem;
  font-weight: 700;
  color: #1a202c;
  margin: 0 0 0.5rem 0;
}

.description {
  color: #4a5568;
  font-size: 1rem;
  margin: 0 0 1rem 0;
  line-height: 1.5;
}

.description strong {
  color: #2d3748;
  font-weight: 600;
}

.instruction {
  color: #718096;
  font-size: 0.875rem;
  margin: 0 0 2rem 0;
}

.action-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin: 2rem 0;
}

.btn {
  padding: 0.75rem 1.5rem;
  border-radius: 0.375rem;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
  text-decoration: none;
  display: inline-block;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-secondary {
  background: #e2e8f0;
  color: #4a5568;
}

.btn-secondary:hover {
  background: #cbd5e0;
}

.tips {
  margin-top: 3rem;
  padding-top: 2rem;
  border-top: 1px solid #e2e8f0;
  text-align: left;
}

.tips h3 {
  font-size: 1rem;
  font-weight: 600;
  color: #2d3748;
  margin: 0 0 1rem 0;
}

.tips ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.tips li {
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
  color: #718096;
  font-size: 0.875rem;
}

.tips li:before {
  content: '•';
  color: #a0aec0;
  font-weight: bold;
  flex-shrink: 0;
}

@media (max-width: 640px) {
  .verification-card {
    padding: 2rem;
  }
  
  .title {
    font-size: 1.5rem;
  }
  
  .action-buttons {
    flex-direction: column;
  }
  
  .btn {
    width: 100%;
  }
}
</style>