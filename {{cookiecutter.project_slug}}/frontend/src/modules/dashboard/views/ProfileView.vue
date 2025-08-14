<template>
  <div class="p-8 max-w-6xl mx-auto">
        <PageHeader
      title="Profile Settings" description="Manage your personal information and preferences"
    />

    <div class="space-y-6">
      <!-- Profile Header -->
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-8 mb-6">
        <div class="relative-section">
          <div class="avatar-container">
            <img 
              v-if="user.avatar" 
              :src="user.avatar" 
              :alt="user.name"
              class="w-24 h-24 rounded-full object-cover"
            >
            <div v-else class="w-24 h-24 rounded-full bg-indigo-500 text-white flex items-center justify-center text-2xl font-bold">
              {% raw %}{{ initials }}{% endraw %}
            </div>
            <button class="absolute bottom-0 right-0 p-2 bg-white rounded-full shadow-lg hover:bg-gray-50 transition-colors">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z"></path>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z"></path>
              </svg>
            </button>
          </div>
          <div class="flex-1">
            <h2 class="text-2xl font-bold text-gray-900">{% raw %}{{ user.name }}{% endraw %}</h2>
            <p class="text-gray-600">{% raw %}{{ user.email }}{% endraw %}</p>
            <span class="inline-block mt-2 px-3 py-1 bg-indigo-100 text-indigo-700 rounded-full text-sm font-medium">{% raw %}{{ user.role }}{% endraw %}</span>
          </div>
        </div>
      </div>

      <!-- Profile Form -->
      <form @submit.prevent="handleSubmit" class="space-y-6">
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mb-6">
          <h3 class="text-xl font-semibold text-gray-900 mb-2 dark:text-gray-100">Personal Information</h3>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="mb-6">
              <label for="firstName">First Name</label>
              <input 
                id="firstName"
                v-model="formData.firstName"
                type="text"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 bg-white dark:bg-gray-700 dark:border-gray-600 dark:text-gray-100 dark:focus:ring-indigo-400 dark:focus:border-indigo-400"
                required
              >
            </div>

            <div class="mb-6">
              <label for="lastName">Last Name</label>
              <input 
                id="lastName"
                v-model="formData.lastName"
                type="text"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 bg-white dark:bg-gray-700 dark:border-gray-600 dark:text-gray-100 dark:focus:ring-indigo-400 dark:focus:border-indigo-400"
                required
              >
            </div>

            <div class="mb-6">
              <label for="email">Email Address</label>
              <input 
                id="email"
                v-model="formData.email"
                type="email"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 bg-white dark:bg-gray-700 dark:border-gray-600 dark:text-gray-100 dark:focus:ring-indigo-400 dark:focus:border-indigo-400"
                required
              >
            </div>

            <div class="mb-6">
              <label for="phone">Phone Number</label>
              <input 
                id="phone"
                v-model="formData.phone"
                type="tel"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 bg-white dark:bg-gray-700 dark:border-gray-600 dark:text-gray-100 dark:focus:ring-indigo-400 dark:focus:border-indigo-400"
              >
            </div>

            <div class="mb-6">
              <label for="dateOfBirth">Date of Birth</label>
              <input 
                id="dateOfBirth"
                v-model="formData.dateOfBirth"
                type="date"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 bg-white dark:bg-gray-700 dark:border-gray-600 dark:text-gray-100 dark:focus:ring-indigo-400 dark:focus:border-indigo-400"
              >
            </div>

            <div class="mb-6">
              <label for="country">Country</label>
              <select 
                id="country"
                v-model="formData.country"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 bg-white dark:bg-gray-700 dark:border-gray-600 dark:text-gray-100 dark:focus:ring-indigo-400 dark:focus:border-indigo-400"
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

          <div class="mb-6">
            <label for="bio">Bio</label>
            <textarea 
              id="bio"
              v-model="formData.bio"
              rows="4"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 bg-white dark:bg-gray-700 dark:border-gray-600 dark:text-gray-100 dark:focus:ring-indigo-400 dark:focus:border-indigo-400"
              placeholder="Tell us about yourself..."
            ></textarea>
          </div>
        </div>

        <div class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mb-6">
          <h3 class="text-xl font-semibold text-gray-900 mb-2 dark:text-gray-100">Change Password</h3>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="mb-6">
              <label for="currentPassword">Current Password</label>
              <input 
                id="currentPassword"
                v-model="passwordData.currentPassword"
                type="password"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 bg-white dark:bg-gray-700 dark:border-gray-600 dark:text-gray-100 dark:focus:ring-indigo-400 dark:focus:border-indigo-400"
              >
            </div>

            <div class="mb-6">
              <label for="newPassword">New Password</label>
              <input 
                id="newPassword"
                v-model="passwordData.newPassword"
                type="password"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 bg-white dark:bg-gray-700 dark:border-gray-600 dark:text-gray-100 dark:focus:ring-indigo-400 dark:focus:border-indigo-400"
              >
            </div>

            <div class="mb-6">
              <label for="confirmPassword">Confirm New Password</label>
              <input 
                id="confirmPassword"
                v-model="passwordData.confirmPassword"
                type="password"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 bg-white dark:bg-gray-700 dark:border-gray-600 dark:text-gray-100 dark:focus:ring-indigo-400 dark:focus:border-indigo-400"
              >
            </div>
          </div>
        </div>

        <div class="flex justify-end gap-3 mt-8">
          <button type="button" class="px-4 py-2 bg-gray-200 dark:bg-gray-700 text-gray-700 rounded-lg font-medium hover:bg-gray-300 transition-colors dark:text-gray-300" @click="handleCancel">
            Cancel
          </button>
          <button type="submit" class="px-4 py-2 bg-indigo-600 text-white rounded-lg font-medium hover:bg-indigo-700 transition-colors" :disabled="loading">
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

