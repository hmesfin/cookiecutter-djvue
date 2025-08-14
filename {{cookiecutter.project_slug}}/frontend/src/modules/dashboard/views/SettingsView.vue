<template>
  <div class="p-8 max-w-7xl mx-auto">
        <PageHeader
      title="Settings" description="Configure your account and application preferences"
    />

    <div class="grid grid-cols-1 lg:grid-cols-4 gap-6">
      <!-- Settings Navigation -->
      <div class="lg:col-span-1 bg-white rounded-lg shadow-md p-6">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          @click="activeTab = tab.id"
          :class="['block px-4 py-2 text-sm font-medium rounded-lg transition-colors cursor-pointer', { active: activeTab === tab.id }]"
        >
          <component :is="tab.icon" class="nav-icon" />
          <span class="nav-label">{% raw %}{{ tab.label }}{% endraw %}</span>
        </button>
      </div>

      <!-- Settings Panel -->
      <div class="lg:col-span-3 bg-white rounded-lg shadow-md p-6">
        <!-- General Settings -->
        <div v-if="activeTab === 'general'" class="space-y-6">
          <h2 class="text-2xl font-semibold text-gray-900 mb-4">General Settings</h2>
          
          <div class="mb-8">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">Application</h3>
            
            <div class="flex items-center justify-between py-4 border-b border-gray-200 last:border-0">
              <div class="flex-1">
                <label>Language</label>
                <p class="text-sm text-gray-500 mt-1">Select your preferred language</p>
              </div>
              <select v-model="settings.language" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 dark:border-gray-600 dark:focus:ring-indigo-400 dark:focus:border-indigo-400">
                <option value="en">English</option>
                <option value="es">Spanish</option>
                <option value="fr">French</option>
                <option value="de">German</option>
                <option value="zh">Chinese</option>
                <option value="ja">Japanese</option>
              </select>
            </div>

            <div class="flex items-center justify-between py-4 border-b border-gray-200 last:border-0">
              <div class="flex-1">
                <label>Time Zone</label>
                <p class="text-sm text-gray-500 mt-1">Set your local time zone</p>
              </div>
              <select v-model="settings.timezone" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 dark:border-gray-600 dark:focus:ring-indigo-400 dark:focus:border-indigo-400">
                <option value="UTC">UTC</option>
                <option value="America/New_York">Eastern Time</option>
                <option value="America/Chicago">Central Time</option>
                <option value="America/Denver">Mountain Time</option>
                <option value="America/Los_Angeles">Pacific Time</option>
                <option value="Europe/London">London</option>
                <option value="Europe/Paris">Paris</option>
                <option value="Asia/Tokyo">Tokyo</option>
              </select>
            </div>

            <div class="flex items-center justify-between py-4 border-b border-gray-200 last:border-0">
              <div class="flex-1">
                <label>Date Format</label>
                <p class="text-sm text-gray-500 mt-1">Choose how dates are displayed</p>
              </div>
              <select v-model="settings.dateFormat" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 dark:border-gray-600 dark:focus:ring-indigo-400 dark:focus:border-indigo-400">
                <option value="MM/DD/YYYY">MM/DD/YYYY</option>
                <option value="DD/MM/YYYY">DD/MM/YYYY</option>
                <option value="YYYY-MM-DD">YYYY-MM-DD</option>
              </select>
            </div>

            <div class="flex items-center justify-between py-4 border-b border-gray-200 last:border-0">
              <div class="flex-1">
                <label>Theme</label>
                <p class="text-sm text-gray-500 mt-1">Choose your interface theme</p>
              </div>
              <div class="theme-selector">
                <button
                  v-for="theme in themes"
                  :key="theme.value"
                  @click="settings.theme = theme.value"
                  :class="['theme-option', { active: settings.theme === theme.value }]"
                >
                  <component :is="theme.icon" class="theme-icon" />
                  <span>{% raw %}{{ theme.label }}{% endraw %}</span>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Notifications Settings -->
        <div v-if="activeTab === 'notifications'" class="space-y-6">
          <h2 class="text-2xl font-semibold text-gray-900 mb-4">Notification Preferences</h2>
          
          <div class="mb-8">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">Email Notifications</h3>
            
            <div class="flex items-center justify-between py-4 border-b border-gray-200 last:border-0">
              <div class="flex-1">
                <label>Account Activity</label>
                <p class="text-sm text-gray-500 mt-1">Get notified about account-related activities</p>
              </div>
              <label class="toggle">
                <input type="checkbox" v-model="settings.notifications.accountActivity">
                <span class="toggle-slider"></span>
              </label>
            </div>

            <div class="flex items-center justify-between py-4 border-b border-gray-200 last:border-0">
              <div class="flex-1">
                <label>Security Alerts</label>
                <p class="text-sm text-gray-500 mt-1">Receive alerts about security events</p>
              </div>
              <label class="toggle">
                <input type="checkbox" v-model="settings.notifications.securityAlerts">
                <span class="toggle-slider"></span>
              </label>
            </div>

            <div class="flex items-center justify-between py-4 border-b border-gray-200 last:border-0">
              <div class="flex-1">
                <label>Newsletter</label>
                <p class="text-sm text-gray-500 mt-1">Receive our monthly newsletter</p>
              </div>
              <label class="toggle">
                <input type="checkbox" v-model="settings.notifications.newsletter">
                <span class="toggle-slider"></span>
              </label>
            </div>

            <div class="flex items-center justify-between py-4 border-b border-gray-200 last:border-0">
              <div class="flex-1">
                <label>Product Updates</label>
                <p class="text-sm text-gray-500 mt-1">Get notified about new features and updates</p>
              </div>
              <label class="toggle">
                <input type="checkbox" v-model="settings.notifications.productUpdates">
                <span class="toggle-slider"></span>
              </label>
            </div>
          </div>

          <div class="mb-8">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">Push Notifications</h3>
            
            <div class="flex items-center justify-between py-4 border-b border-gray-200 last:border-0">
              <div class="flex-1">
                <label>Browser Notifications</label>
                <p class="text-sm text-gray-500 mt-1">Show desktop notifications</p>
              </div>
              <label class="toggle">
                <input type="checkbox" v-model="settings.notifications.browserNotifications">
                <span class="toggle-slider"></span>
              </label>
            </div>

            <div class="flex items-center justify-between py-4 border-b border-gray-200 last:border-0">
              <div class="flex-1">
                <label>Sound</label>
                <p class="text-sm text-gray-500 mt-1">Play sound for notifications</p>
              </div>
              <label class="toggle">
                <input type="checkbox" v-model="settings.notifications.sound">
                <span class="toggle-slider"></span>
              </label>
            </div>
          </div>
        </div>

        <!-- Privacy Settings -->
        <div v-if="activeTab === 'privacy'" class="space-y-6">
          <h2 class="text-2xl font-semibold text-gray-900 mb-4">Privacy & Security</h2>
          
          <div class="mb-8">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">Privacy</h3>
            
            <div class="flex items-center justify-between py-4 border-b border-gray-200 last:border-0">
              <div class="flex-1">
                <label>Profile Visibility</label>
                <p class="text-sm text-gray-500 mt-1">Control who can see your profile</p>
              </div>
              <select v-model="settings.privacy.profileVisibility" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 dark:border-gray-600 dark:focus:ring-indigo-400 dark:focus:border-indigo-400">
                <option value="public">Public</option>
                <option value="friends">Friends Only</option>
                <option value="private">Private</option>
              </select>
            </div>

            <div class="flex items-center justify-between py-4 border-b border-gray-200 last:border-0">
              <div class="flex-1">
                <label>Show Online Status</label>
                <p class="text-sm text-gray-500 mt-1">Let others see when you're online</p>
              </div>
              <label class="toggle">
                <input type="checkbox" v-model="settings.privacy.showOnlineStatus">
                <span class="toggle-slider"></span>
              </label>
            </div>

            <div class="flex items-center justify-between py-4 border-b border-gray-200 last:border-0">
              <div class="flex-1">
                <label>Activity Status</label>
                <p class="text-sm text-gray-500 mt-1">Show your recent activity to others</p>
              </div>
              <label class="toggle">
                <input type="checkbox" v-model="settings.privacy.activityStatus">
                <span class="toggle-slider"></span>
              </label>
            </div>
          </div>

          <div class="mb-8">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">Security</h3>
            
            <div class="flex items-center justify-between py-4 border-b border-gray-200 last:border-0">
              <div class="flex-1">
                <label>Two-Factor Authentication</label>
                <p class="text-sm text-gray-500 mt-1">Add an extra layer of security to your account</p>
              </div>
              <button class="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg font-medium hover:bg-gray-300 transition-colors dark:bg-gray-700 dark:text-gray-300">
                {% raw %}{{ settings.security.twoFactorEnabled ? 'Manage' : 'Enable' }}{% endraw %}
              </button>
            </div>

            <div class="flex items-center justify-between py-4 border-b border-gray-200 last:border-0">
              <div class="flex-1">
                <label>Login Notifications</label>
                <p class="text-sm text-gray-500 mt-1">Get notified of new login attempts</p>
              </div>
              <label class="toggle">
                <input type="checkbox" v-model="settings.security.loginNotifications">
                <span class="toggle-slider"></span>
              </label>
            </div>

            <div class="flex items-center justify-between py-4 border-b border-gray-200 last:border-0">
              <div class="flex-1">
                <label>Active Sessions</label>
                <p class="text-sm text-gray-500 mt-1">Manage your active login sessions</p>
              </div>
              <button class="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg font-medium hover:bg-gray-300 transition-colors dark:bg-gray-700 dark:text-gray-300">View Sessions</button>
            </div>
          </div>
        </div>

        <!-- Integrations Settings -->
        <div v-if="activeTab === 'integrations'" class="space-y-6">
          <h2 class="text-2xl font-semibold text-gray-900 mb-4">Integrations</h2>
          
          <div class="mb-8">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">Connected Services</h3>
            
            <div class="integration-list">
              <div v-for="integration in integrations" :key="integration.id" class="integration-item">
                <div class="flex items-center gap-3">
                  <img :src="integration.icon" :alt="integration.name" class="w-12 h-12 rounded-lg flex items-center justify-center">
                  <div>
                    <h4>{% raw %}{{ integration.name }}{% endraw %}</h4>
                    <p>{% raw %}{{ integration.description }}{% endraw %}</p>
                  </div>
                </div>
                <button 
                  @click="toggleIntegration(integration)"
                  :class="['btn', integration.connected ? 'btn-danger' : 'btn-primary']"
                >
                  {% raw %}{{ integration.connected ? 'Disconnect' : 'Connect' }}{% endraw %}
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Save Button -->
        <div class="flex justify-end gap-3 mt-6">
          <button @click="resetSettings" class="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg font-medium hover:bg-gray-300 transition-colors dark:bg-gray-700 dark:text-gray-300">
            Reset to Defaults
          </button>
          <button @click="saveSettings" class="px-4 py-2 bg-indigo-600 text-white rounded-lg font-medium hover:bg-indigo-700 transition-colors" :disabled="saving">
            {% raw %}{{ saving ? 'Saving...' : 'Save Changes' }}{% endraw %}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup{% if cookiecutter.use_typescript == 'y' %} lang="ts"{% endif %}>
import { ref, reactive } from 'vue'

{% if cookiecutter.use_typescript == 'y' -%}
interface Settings {
  language: string
  timezone: string
  dateFormat: string
  theme: string
  notifications: {
    accountActivity: boolean
    securityAlerts: boolean
    newsletter: boolean
    productUpdates: boolean
    browserNotifications: boolean
    sound: boolean
  }
  privacy: {
    profileVisibility: string
    showOnlineStatus: boolean
    activityStatus: boolean
  }
  security: {
    twoFactorEnabled: boolean
    loginNotifications: boolean
  }
}

interface Integration {
  id: string
  name: string
  description: string
  icon: string
  connected: boolean
}
{%- endif %}

const activeTab = ref('general')
const saving = ref(false)

const tabs = [
  { id: 'general', label: 'General', icon: 'div' },
  { id: 'notifications', label: 'Notifications', icon: 'div' },
  { id: 'privacy', label: 'Privacy', icon: 'div' },
  { id: 'integrations', label: 'Integrations', icon: 'div' }
]

const themes = [
  { value: 'light', label: 'Light', icon: 'div' },
  { value: 'dark', label: 'Dark', icon: 'div' },
  { value: 'auto', label: 'Auto', icon: 'div' }
]

const settings = reactive({% if cookiecutter.use_typescript == 'y' %}<Settings>{% endif %}{
  language: 'en',
  timezone: 'UTC',
  dateFormat: 'MM/DD/YYYY',
  theme: 'light',
  notifications: {
    accountActivity: true,
    securityAlerts: true,
    newsletter: false,
    productUpdates: true,
    browserNotifications: true,
    sound: true
  },
  privacy: {
    profileVisibility: 'public',
    showOnlineStatus: true,
    activityStatus: true
  },
  security: {
    twoFactorEnabled: false,
    loginNotifications: true
  }
})

const integrations = ref({% if cookiecutter.use_typescript == 'y' %}<Integration[]>{% endif %}[
  {
    id: 'google',
    name: 'Google',
    description: 'Connect your Google account',
    icon: 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><rect fill="%23EA4335" width="24" height="24"/></svg>',
    connected: false
  },
  {
    id: 'github',
    name: 'GitHub',
    description: 'Connect your GitHub account',
    icon: 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><rect fill="%23181717" width="24" height="24"/></svg>',
    connected: true
  },
  {
    id: 'slack',
    name: 'Slack',
    description: 'Connect to Slack workspace',
    icon: 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><rect fill="%234A154B" width="24" height="24"/></svg>',
    connected: false
  }
])

const toggleIntegration = (integration{% if cookiecutter.use_typescript == 'y' %}: Integration{% endif %}) => {
  integration.connected = !integration.connected
}

const saveSettings = async () => {
  saving.value = true
  try {
    // In a real app, save settings to API
    await new Promise(resolve => setTimeout(resolve, 1000))
    alert('Settings saved successfully!')
  } catch (error) {
    console.error('Error saving settings:', error)
    alert('Failed to save settings. Please try again.')
  } finally {
    saving.value = false
  }
}

const resetSettings = () => {
  if (confirm('Are you sure you want to reset all settings to defaults?')) {
    // Reset to default values
    Object.assign(settings, {
      language: 'en',
      timezone: 'UTC',
      dateFormat: 'MM/DD/YYYY',
      theme: 'light',
      notifications: {
        accountActivity: true,
        securityAlerts: true,
        newsletter: false,
        productUpdates: true,
        browserNotifications: true,
        sound: true
      },
      privacy: {
        profileVisibility: 'public',
        showOnlineStatus: true,
        activityStatus: true
      },
      security: {
        twoFactorEnabled: false,
        loginNotifications: true
      }
    })
  }
}
</script>

