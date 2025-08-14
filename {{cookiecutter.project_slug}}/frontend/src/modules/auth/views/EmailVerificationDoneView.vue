<template>
  <div class="email-verification-done-view">
    <div class="verification-container">
      <div class="verification-card">
        <!-- Success State -->
        <div v-if="verificationStatus === 'success'" class="verification-content">
          <div class="icon-wrapper success">
            <svg class="icon animated-check" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
          </div>
          
          <h1 class="title">Email Verified Successfully!</h1>
          
          <p class="description">
            Your email has been verified and your account is now fully activated.
          </p>
          
          <div class="welcome-message">
            <p>Welcome to <strong>{{ cookiecutter.project_name }}</strong>!</p>
            <p>You can now access all features of your account.</p>
          </div>
          
          <div class="action-buttons">
            <router-link to="/dashboard" class="btn btn-primary">
              Go to Dashboard
            </router-link>
            <router-link to="/profile" class="btn btn-secondary">
              Complete Your Profile
            </router-link>
          </div>
          
          <div class="next-steps">
            <h3>What's Next?</h3>
            <ul>
              <li>Explore your dashboard</li>
              <li>Complete your profile information</li>
              <li>Check out our getting started guide</li>
              <li>Connect with other users</li>
            </ul>
          </div>
        </div>

        <!-- Already Verified State -->
        <div v-else-if="verificationStatus === 'already_verified'" class="verification-content">
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
              Sign In
            </router-link>
          </div>
        </div>

        <!-- Error State -->
        <div v-else-if="verificationStatus === 'error'" class="verification-content">
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
            <router-link to="/auth/verify-email" class="btn btn-primary">
              Request New Link
            </router-link>
            <router-link to="/auth/login" class="btn btn-secondary">
              Back to Login
            </router-link>
          </div>
          
          <div class="help-text">
            <p>If you continue to have issues, please contact support.</p>
          </div>
        </div>

        <!-- Loading State -->
        <div v-else class="verification-content">
          <div class="spinner">
            <div class="spinner-circle"></div>
          </div>
          <h1 class="title">Verifying Your Email</h1>
          <p class="description">Please wait while we verify your email address...</p>
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

<style scoped>
.email-verification-done-view {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.verification-container {
  max-width: 600px;
  width: 100%;
}

.verification-card {
  background: white;
  border-radius: 1rem;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  overflow: hidden;
}

.verification-content {
  padding: 3rem;
  text-align: center;
}

/* Icon Styles */
.icon-wrapper {
  width: 80px;
  height: 80px;
  margin: 0 auto 2rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon-wrapper.success {
  background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
}

.icon-wrapper.info {
  background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%);
}

.icon-wrapper.error {
  background: linear-gradient(135deg, #fc8181 0%, #f56565 100%);
}

.icon {
  width: 40px;
  height: 40px;
  color: white;
}

/* Animated check icon */
.animated-check {
  animation: checkmark 0.5s ease-in-out;
}

@keyframes checkmark {
  0% {
    stroke-dasharray: 0 100;
  }
  100% {
    stroke-dasharray: 100 100;
  }
}

/* Content Styles */
.title {
  font-size: 2rem;
  font-weight: 700;
  color: #1a202c;
  margin: 0 0 1rem 0;
}

.description {
  font-size: 1.125rem;
  color: #718096;
  margin-bottom: 2rem;
  line-height: 1.6;
}

.welcome-message {
  background: #f7fafc;
  border-left: 4px solid #667eea;
  padding: 1.5rem;
  margin-bottom: 2rem;
  text-align: left;
}

.welcome-message p {
  margin: 0.5rem 0;
  color: #4a5568;
}

.welcome-message strong {
  color: #667eea;
}

/* Action Buttons */
.action-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.btn {
  padding: 0.75rem 2rem;
  border-radius: 0.5rem;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s;
  display: inline-block;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(102, 126, 234, 0.4);
}

.btn-secondary {
  background: white;
  color: #667eea;
  border: 2px solid #667eea;
}

.btn-secondary:hover {
  background: #667eea;
  color: white;
}

/* Next Steps */
.next-steps {
  background: #f7fafc;
  border-radius: 0.5rem;
  padding: 1.5rem;
  text-align: left;
}

.next-steps h3 {
  font-size: 1.125rem;
  font-weight: 600;
  color: #2d3748;
  margin: 0 0 1rem 0;
}

.next-steps ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.next-steps li {
  padding: 0.5rem 0;
  padding-left: 1.5rem;
  position: relative;
  color: #4a5568;
}

.next-steps li:before {
  content: '✓';
  position: absolute;
  left: 0;
  color: #48bb78;
  font-weight: bold;
}

/* Help Text */
.help-text {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #e2e8f0;
}

.help-text p {
  color: #718096;
  font-size: 0.875rem;
}

/* Spinner */
.spinner {
  margin: 0 auto 2rem;
  width: 60px;
  height: 60px;
  position: relative;
}

.spinner-circle {
  width: 100%;
  height: 100%;
  border: 4px solid #e2e8f0;
  border-top-color: #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* Responsive */
@media (max-width: 640px) {
  .verification-content {
    padding: 2rem 1.5rem;
  }
  
  .title {
    font-size: 1.5rem;
  }
  
  .action-buttons {
    flex-direction: column;
  }
  
  .btn {
    width: 100%;
    text-align: center;
  }
}
</style>