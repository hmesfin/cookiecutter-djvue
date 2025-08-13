<template>
  <div class="forgot-password-view">
    <div class="auth-container">
      <div class="auth-card">
        <div class="auth-header">
          <h1 class="auth-title">Forgot Password?</h1>
          <p class="auth-subtitle">
            No worries! Enter your email address and we'll send you instructions to reset your password.
          </p>
        </div>

        <form @submit.prevent="handleSubmit" class="auth-form">
          <div v-if="!isSubmitted">
            <div class="form-group">
              <label for="email">Email Address</label>
              <input 
                id="email"
                v-model="email"
                type="email"
                class="form-input"
                placeholder="Enter your email address"
                required
                :disabled="loading"
              >
              <p v-if="error" class="error-message">{% raw %}{{ error }}{% endraw %}</p>
            </div>

            <button type="submit" class="btn btn-primary" :disabled="loading">
              {% raw %}{{ loading ? 'Sending...' : 'Send Reset Instructions' }}{% endraw %}
            </button>
          </div>

          <div v-else class="success-message">
            <div class="success-icon">
              <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
            <h2 class="success-title">Check Your Email</h2>
            <p class="success-text">
              We've sent password reset instructions to <strong>{% raw %}{{ email }}{% endraw %}</strong>
            </p>
            <p class="success-note">
              Didn't receive the email? Check your spam folder or 
              <button type="button" @click="resendEmail" class="link-btn" :disabled="resending">
                {% raw %}{{ resending ? 'Resending...' : 'click here to resend' }}{% endraw %}
              </button>
            </p>
          </div>
        </form>

        <div class="auth-footer">
          <router-link to="/auth/login" class="auth-link">
            <svg class="icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path>
            </svg>
            Back to Login
          </router-link>
        </div>
      </div>

      <div class="auth-decoration">
        <div class="decoration-content">
          <h2 class="decoration-title">Password Security Tips</h2>
          <ul class="tips-list">
            <li>
              <svg class="tip-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
              Use a combination of uppercase and lowercase letters
            </li>
            <li>
              <svg class="tip-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
              Include numbers and special characters
            </li>
            <li>
              <svg class="tip-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
              Make your password at least 12 characters long
            </li>
            <li>
              <svg class="tip-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
              Avoid using personal information
            </li>
            <li>
              <svg class="tip-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
              Use unique passwords for each account
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

<style scoped>
.forgot-password-view {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.auth-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  max-width: 1000px;
  width: 100%;
  background: white;
  border-radius: 1rem;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  overflow: hidden;
}

.auth-card {
  padding: 3rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.auth-header {
  margin-bottom: 2rem;
}

.auth-title {
  font-size: 2rem;
  font-weight: 700;
  color: #1a202c;
  margin: 0 0 0.5rem 0;
}

.auth-subtitle {
  color: #718096;
  line-height: 1.5;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-size: 0.875rem;
  font-weight: 500;
  color: #4a5568;
}

.form-input {
  padding: 0.75rem 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.375rem;
  font-size: 1rem;
  transition: all 0.2s;
}

.form-input:focus {
  outline: none;
  border-color: #4299e1;
  box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.1);
}

.form-input:disabled {
  background: #f7fafc;
  cursor: not-allowed;
}

.error-message {
  color: #e53e3e;
  font-size: 0.875rem;
  margin: 0;
}

.btn {
  padding: 0.75rem 1.5rem;
  border-radius: 0.375rem;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
  width: 100%;
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

.success-message {
  text-align: center;
  padding: 2rem;
  background: #f0fdf4;
  border-radius: 0.5rem;
  border: 1px solid #86efac;
}

.success-icon {
  width: 64px;
  height: 64px;
  margin: 0 auto 1rem;
  color: #22c55e;
}

.success-icon svg {
  width: 100%;
  height: 100%;
}

.success-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1a202c;
  margin: 0 0 0.5rem 0;
}

.success-text {
  color: #4a5568;
  margin: 0 0 1rem 0;
}

.success-text strong {
  color: #1a202c;
}

.success-note {
  color: #718096;
  font-size: 0.875rem;
  margin: 0;
}

.link-btn {
  background: none;
  border: none;
  color: #4299e1;
  font-weight: 500;
  cursor: pointer;
  text-decoration: underline;
  transition: color 0.2s;
}

.link-btn:hover:not(:disabled) {
  color: #3182ce;
}

.link-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.auth-footer {
  margin-top: 2rem;
  text-align: center;
}

.auth-link {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  color: #4299e1;
  text-decoration: none;
  font-size: 0.875rem;
  font-weight: 500;
  transition: color 0.2s;
}

.auth-link:hover {
  color: #3182ce;
}

.icon {
  width: 16px;
  height: 16px;
}

.auth-decoration {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 3rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.decoration-content {
  color: white;
}

.decoration-title {
  font-size: 1.5rem;
  font-weight: 600;
  margin: 0 0 2rem 0;
}

.tips-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.tips-list li {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  font-size: 0.875rem;
  line-height: 1.5;
}

.tip-icon {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
  margin-top: 0.125rem;
}

@media (max-width: 768px) {
  .auth-container {
    grid-template-columns: 1fr;
  }
  
  .auth-decoration {
    display: none;
  }
  
  .auth-card {
    padding: 2rem;
  }
  
  .auth-title {
    font-size: 1.5rem;
  }
}
</style>