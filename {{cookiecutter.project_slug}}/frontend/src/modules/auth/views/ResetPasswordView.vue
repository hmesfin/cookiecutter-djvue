<template>
  <div class="reset-password-view">
    <div class="auth-container">
      <div class="auth-card">
        <div class="auth-header">
          <h1 class="auth-title">Reset Your Password</h1>
          <p class="auth-subtitle">
            Enter your new password below. Make sure it's strong and secure.
          </p>
        </div>

        <form @submit.prevent="handleSubmit" class="auth-form">
          <div v-if="!isReset">
            <div class="form-group">
              <label for="password">New Password</label>
              <div class="password-input-wrapper">
                <input 
                  id="password"
                  v-model="password"
                  :type="showPassword ? 'text' : 'password'"
                  class="form-input"
                  placeholder="Enter new password"
                  required
                  :disabled="loading"
                  @input="checkPasswordStrength"
                >
                <button 
                  type="button"
                  @click="showPassword = !showPassword"
                  class="password-toggle"
                >
                  <svg v-if="!showPassword" class="icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
                  </svg>
                  <svg v-else class="icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21"></path>
                  </svg>
                </button>
              </div>
              
              <!-- Password Strength Indicator -->
              <div class="password-strength">
                <div class="strength-bar">
                  <div 
                    class="strength-fill"
                    :style="{ width: passwordStrength.percentage + '%' }"
                    :class="passwordStrength.level"
                  ></div>
                </div>
                <span class="strength-text" :class="passwordStrength.level">
                  {% raw %}{{ passwordStrength.text }}{% endraw %}
                </span>
              </div>
              
              <!-- Password Requirements -->
              <ul class="password-requirements">
                <li :class="{ met: requirements.length }">
                  <svg class="requirement-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                  At least 8 characters
                </li>
                <li :class="{ met: requirements.uppercase }">
                  <svg class="requirement-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                  One uppercase letter
                </li>
                <li :class="{ met: requirements.lowercase }">
                  <svg class="requirement-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                  One lowercase letter
                </li>
                <li :class="{ met: requirements.number }">
                  <svg class="requirement-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                  One number
                </li>
                <li :class="{ met: requirements.special }">
                  <svg class="requirement-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                  One special character
                </li>
              </ul>
            </div>

            <div class="form-group">
              <label for="confirmPassword">Confirm New Password</label>
              <div class="password-input-wrapper">
                <input 
                  id="confirmPassword"
                  v-model="confirmPassword"
                  :type="showConfirmPassword ? 'text' : 'password'"
                  class="form-input"
                  placeholder="Confirm new password"
                  required
                  :disabled="loading"
                >
                <button 
                  type="button"
                  @click="showConfirmPassword = !showConfirmPassword"
                  class="password-toggle"
                >
                  <svg v-if="!showConfirmPassword" class="icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
                  </svg>
                  <svg v-else class="icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21"></path>
                  </svg>
                </button>
              </div>
              <p v-if="error" class="error-message">{% raw %}{{ error }}{% endraw %}</p>
            </div>

            <button type="submit" class="btn btn-primary" :disabled="loading || !isValidPassword">
              {% raw %}{{ loading ? 'Resetting...' : 'Reset Password' }}{% endraw %}
            </button>
          </div>

          <div v-else class="success-message">
            <div class="success-icon">
              <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
            <h2 class="success-title">Password Reset Successful!</h2>
            <p class="success-text">
              Your password has been successfully reset. You can now log in with your new password.
            </p>
            <router-link to="/auth/login" class="btn btn-primary">
              Go to Login
            </router-link>
          </div>
        </form>

        <div v-if="!isReset" class="auth-footer">
          <router-link to="/auth/login" class="auth-link">
            <svg class="icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path>
            </svg>
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
{%- endif %}

const router = useRouter()
const route = useRoute()

const password = ref('')
const confirmPassword = ref('')
const showPassword = ref(false)
const showConfirmPassword = ref(false)
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

<style scoped>
.reset-password-view {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.auth-container {
  max-width: 500px;
  width: 100%;
  background: white;
  border-radius: 1rem;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  overflow: hidden;
}

.auth-card {
  padding: 3rem;
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

.password-input-wrapper {
  position: relative;
}

.form-input {
  width: 100%;
  padding: 0.75rem 3rem 0.75rem 1rem;
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

.password-toggle {
  position: absolute;
  right: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: #718096;
  cursor: pointer;
  padding: 0.25rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.password-toggle:hover {
  color: #4a5568;
}

.icon {
  width: 20px;
  height: 20px;
}

.password-strength {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-top: 0.5rem;
}

.strength-bar {
  flex: 1;
  height: 6px;
  background: #e2e8f0;
  border-radius: 3px;
  overflow: hidden;
}

.strength-fill {
  height: 100%;
  transition: all 0.3s ease;
  border-radius: 3px;
}

.strength-fill.weak {
  background: #f56565;
}

.strength-fill.fair {
  background: #ed8936;
}

.strength-fill.good {
  background: #ecc94b;
}

.strength-fill.strong {
  background: #48bb78;
}

.strength-text {
  font-size: 0.75rem;
  font-weight: 500;
  min-width: 50px;
}

.strength-text.weak {
  color: #f56565;
}

.strength-text.fair {
  color: #ed8936;
}

.strength-text.good {
  color: #d69e2e;
}

.strength-text.strong {
  color: #48bb78;
}

.password-requirements {
  list-style: none;
  padding: 0;
  margin: 0.5rem 0 0 0;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.password-requirements li {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.75rem;
  color: #a0aec0;
  transition: color 0.2s;
}

.password-requirements li.met {
  color: #48bb78;
}

.requirement-icon {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
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
  text-align: center;
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
  margin: 0 0 1.5rem 0;
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

@media (max-width: 768px) {
  .auth-card {
    padding: 2rem;
  }
  
  .auth-title {
    font-size: 1.5rem;
  }
}
</style>