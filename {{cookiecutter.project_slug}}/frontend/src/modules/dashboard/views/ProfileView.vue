<template>
  <div class="profile-view">
    <div class="page-header">
      <h1 class="page-title">Profile</h1>
      <p class="page-description">Manage your personal information and preferences</p>
    </div>

    <div class="profile-content">
      <!-- Profile Header -->
      <div class="profile-header card">
        <div class="profile-avatar-section">
          <div class="avatar-container">
            <img 
              v-if="user.avatar" 
              :src="user.avatar" 
              :alt="user.name"
              class="avatar-image"
            >
            <div v-else class="avatar-placeholder">
              {% raw %}{{ initials }}{% endraw %}
            </div>
            <button class="avatar-change-btn">
              <svg class="icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z"></path>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z"></path>
              </svg>
            </button>
          </div>
          <div class="profile-info">
            <h2 class="profile-name">{% raw %}{{ user.name }}{% endraw %}</h2>
            <p class="profile-email">{% raw %}{{ user.email }}{% endraw %}</p>
            <span class="profile-role">{% raw %}{{ user.role }}{% endraw %}</span>
          </div>
        </div>
      </div>

      <!-- Profile Form -->
      <form @submit.prevent="handleSubmit" class="profile-form">
        <div class="form-section card">
          <h3 class="section-title">Personal Information</h3>
          
          <div class="form-grid">
            <div class="form-group">
              <label for="firstName">First Name</label>
              <input 
                id="firstName"
                v-model="formData.firstName"
                type="text"
                class="form-input"
                required
              >
            </div>

            <div class="form-group">
              <label for="lastName">Last Name</label>
              <input 
                id="lastName"
                v-model="formData.lastName"
                type="text"
                class="form-input"
                required
              >
            </div>

            <div class="form-group">
              <label for="email">Email Address</label>
              <input 
                id="email"
                v-model="formData.email"
                type="email"
                class="form-input"
                required
              >
            </div>

            <div class="form-group">
              <label for="phone">Phone Number</label>
              <input 
                id="phone"
                v-model="formData.phone"
                type="tel"
                class="form-input"
              >
            </div>

            <div class="form-group">
              <label for="dateOfBirth">Date of Birth</label>
              <input 
                id="dateOfBirth"
                v-model="formData.dateOfBirth"
                type="date"
                class="form-input"
              >
            </div>

            <div class="form-group">
              <label for="country">Country</label>
              <select 
                id="country"
                v-model="formData.country"
                class="form-input"
              >
                <option value="">Select a country</option>
                <option value="US">United States</option>
                <option value="CA">Canada</option>
                <option value="GB">United Kingdom</option>
                <option value="AU">Australia</option>
                <option value="DE">Germany</option>
                <option value="FR">France</option>
                <option value="JP">Japan</option>
                <option value="CN">China</option>
                <option value="IN">India</option>
                <option value="BR">Brazil</option>
              </select>
            </div>
          </div>

          <div class="form-group">
            <label for="bio">Bio</label>
            <textarea 
              id="bio"
              v-model="formData.bio"
              rows="4"
              class="form-input"
              placeholder="Tell us about yourself..."
            ></textarea>
          </div>
        </div>

        <div class="form-section card">
          <h3 class="section-title">Change Password</h3>
          
          <div class="form-grid">
            <div class="form-group">
              <label for="currentPassword">Current Password</label>
              <input 
                id="currentPassword"
                v-model="passwordData.currentPassword"
                type="password"
                class="form-input"
              >
            </div>

            <div class="form-group">
              <label for="newPassword">New Password</label>
              <input 
                id="newPassword"
                v-model="passwordData.newPassword"
                type="password"
                class="form-input"
              >
            </div>

            <div class="form-group">
              <label for="confirmPassword">Confirm New Password</label>
              <input 
                id="confirmPassword"
                v-model="passwordData.confirmPassword"
                type="password"
                class="form-input"
              >
            </div>
          </div>
        </div>

        <div class="form-actions">
          <button type="button" class="btn btn-secondary" @click="handleCancel">
            Cancel
          </button>
          <button type="submit" class="btn btn-primary" :disabled="loading">
            {% raw %}{{ loading ? 'Saving...' : 'Save Changes' }}{% endraw %}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup{% if cookiecutter.use_typescript == 'y' %} lang="ts"{% endif %}>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

{% if cookiecutter.use_typescript == 'y' -%}
interface UserProfile {
  id: string
  name: string
  email: string
  avatar?: string
  role: string
  firstName: string
  lastName: string
  phone?: string
  dateOfBirth?: string
  country?: string
  bio?: string
}

interface ProfileFormData {
  firstName: string
  lastName: string
  email: string
  phone: string
  dateOfBirth: string
  country: string
  bio: string
}

interface PasswordData {
  currentPassword: string
  newPassword: string
  confirmPassword: string
}
{%- endif %}

const authStore = useAuthStore()
const router = useRouter()

const loading = ref(false)
const user = ref({% if cookiecutter.use_typescript == 'y' %}<UserProfile>{% endif %}{
  id: '1',
  name: 'John Doe',
  email: 'john.doe@example.com',
  avatar: '',
  role: 'Administrator',
  firstName: 'John',
  lastName: 'Doe',
  phone: '+1 234 567 8900',
  dateOfBirth: '1990-01-01',
  country: 'US',
  bio: 'Full-stack developer with a passion for creating beautiful and functional web applications.'
})

const formData = ref({% if cookiecutter.use_typescript == 'y' %}<ProfileFormData>{% endif %}{
  firstName: '',
  lastName: '',
  email: '',
  phone: '',
  dateOfBirth: '',
  country: '',
  bio: ''
})

const passwordData = ref({% if cookiecutter.use_typescript == 'y' %}<PasswordData>{% endif %}{
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const initials = computed(() => {
  const names = user.value.name.split(' ')
  return names.map(n => n[0]).join('').toUpperCase()
})

onMounted(() => {
  // Load user profile data
  loadProfile()
})

const loadProfile = async () => {
  // In a real app, fetch user data from API
  formData.value = {
    firstName: user.value.firstName,
    lastName: user.value.lastName,
    email: user.value.email,
    phone: user.value.phone || '',
    dateOfBirth: user.value.dateOfBirth || '',
    country: user.value.country || '',
    bio: user.value.bio || ''
  }
}

const handleSubmit = async () => {
  loading.value = true
  try {
    // Validate password fields if attempting to change password
    if (passwordData.value.currentPassword || passwordData.value.newPassword || passwordData.value.confirmPassword) {
      if (!passwordData.value.currentPassword) {
        alert('Please enter your current password')
        return
      }
      if (passwordData.value.newPassword !== passwordData.value.confirmPassword) {
        alert('New passwords do not match')
        return
      }
      if (passwordData.value.newPassword.length < 8) {
        alert('Password must be at least 8 characters long')
        return
      }
    }

    // In a real app, send data to API
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // Update user data
    user.value = {
      ...user.value,
      ...formData.value,
      name: `${formData.value.firstName} ${formData.value.lastName}`
    }
    
    alert('Profile updated successfully!')
    
    // Clear password fields
    passwordData.value = {
      currentPassword: '',
      newPassword: '',
      confirmPassword: ''
    }
  } catch (error) {
    console.error('Error updating profile:', error)
    alert('Failed to update profile. Please try again.')
  } finally {
    loading.value = false
  }
}

const handleCancel = () => {
  if (confirm('Are you sure you want to discard your changes?')) {
    loadProfile()
    passwordData.value = {
      currentPassword: '',
      newPassword: '',
      confirmPassword: ''
    }
  }
}
</script>

<style scoped>
.profile-view {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 2rem;
}

.page-title {
  font-size: 2rem;
  font-weight: 700;
  color: #1a202c;
  margin: 0 0 0.5rem 0;
}

.page-description {
  color: #718096;
  font-size: 1rem;
}

.profile-content {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.card {
  background: white;
  border-radius: 0.5rem;
  padding: 1.5rem;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
}

.profile-header {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.profile-avatar-section {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.avatar-container {
  position: relative;
}

.avatar-image,
.avatar-placeholder {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  object-fit: cover;
}

.avatar-placeholder {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.5rem;
  font-weight: 600;
  color: white;
}

.avatar-change-btn {
  position: absolute;
  bottom: 0;
  right: 0;
  background: white;
  border: 2px solid #e2e8f0;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
}

.avatar-change-btn:hover {
  background: #f7fafc;
  border-color: #cbd5e0;
}

.icon {
  width: 20px;
  height: 20px;
  color: #4a5568;
}

.profile-info {
  flex: 1;
}

.profile-name {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1a202c;
  margin: 0 0 0.25rem 0;
}

.profile-email {
  color: #718096;
  margin: 0 0 0.5rem 0;
}

.profile-role {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  background: #edf2f7;
  color: #4a5568;
  border-radius: 9999px;
  font-size: 0.875rem;
  font-weight: 500;
}

.profile-form {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.form-section {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.section-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1a202c;
  margin: 0;
  padding-bottom: 1rem;
  border-bottom: 1px solid #e2e8f0;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
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
  padding: 0.5rem 0.75rem;
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

textarea.form-input {
  resize: vertical;
  min-height: 100px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  padding-top: 1rem;
}

.btn {
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
}

.btn-primary {
  background: #4299e1;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #3182ce;
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

@media (max-width: 768px) {
  .profile-view {
    padding: 1rem;
  }
  
  .profile-avatar-section {
    flex-direction: column;
    text-align: center;
  }
  
  .form-grid {
    grid-template-columns: 1fr;
  }
  
  .form-actions {
    flex-direction: column-reverse;
  }
  
  .btn {
    width: 100%;
  }
}
</style>