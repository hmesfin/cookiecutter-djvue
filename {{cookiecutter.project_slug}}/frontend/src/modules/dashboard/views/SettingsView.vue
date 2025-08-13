<template>
  <div class="settings-view">
    <div class="page-header">
      <h1 class="page-title">Settings</h1>
      <p class="page-description">Manage your application preferences and configurations</p>
    </div>

    <div class="settings-content">
      <!-- Settings Navigation -->
      <div class="settings-nav card">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          @click="activeTab = tab.id"
          :class="['nav-item', { active: activeTab === tab.id }]"
        >
          <component :is="tab.icon" class="nav-icon" />
          <span class="nav-label">{% raw %}{{ tab.label }}{% endraw %}</span>
        </button>
      </div>

      <!-- Settings Panel -->
      <div class="settings-panel card">
        <!-- General Settings -->
        <div v-if="activeTab === 'general'" class="panel-content">
          <h2 class="panel-title">General Settings</h2>
          
          <div class="settings-group">
            <h3 class="group-title">Application</h3>
            
            <div class="setting-item">
              <div class="setting-info">
                <label>Language</label>
                <p class="setting-description">Select your preferred language</p>
              </div>
              <select v-model="settings.language" class="form-select">
                <option value="en">English</option>
                <option value="es">Spanish</option>
                <option value="fr">French</option>
                <option value="de">German</option>
                <option value="zh">Chinese</option>
                <option value="ja">Japanese</option>
              </select>
            </div>

            <div class="setting-item">
              <div class="setting-info">
                <label>Time Zone</label>
                <p class="setting-description">Set your local time zone</p>
              </div>
              <select v-model="settings.timezone" class="form-select">
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

            <div class="setting-item">
              <div class="setting-info">
                <label>Date Format</label>
                <p class="setting-description">Choose how dates are displayed</p>
              </div>
              <select v-model="settings.dateFormat" class="form-select">
                <option value="MM/DD/YYYY">MM/DD/YYYY</option>
                <option value="DD/MM/YYYY">DD/MM/YYYY</option>
                <option value="YYYY-MM-DD">YYYY-MM-DD</option>
              </select>
            </div>

            <div class="setting-item">
              <div class="setting-info">
                <label>Theme</label>
                <p class="setting-description">Choose your interface theme</p>
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
        <div v-if="activeTab === 'notifications'" class="panel-content">
          <h2 class="panel-title">Notification Preferences</h2>
          
          <div class="settings-group">
            <h3 class="group-title">Email Notifications</h3>
            
            <div class="setting-item">
              <div class="setting-info">
                <label>Account Activity</label>
                <p class="setting-description">Get notified about account-related activities</p>
              </div>
              <label class="toggle">
                <input type="checkbox" v-model="settings.notifications.accountActivity">
                <span class="toggle-slider"></span>
              </label>
            </div>

            <div class="setting-item">
              <div class="setting-info">
                <label>Security Alerts</label>
                <p class="setting-description">Receive alerts about security events</p>
              </div>
              <label class="toggle">
                <input type="checkbox" v-model="settings.notifications.securityAlerts">
                <span class="toggle-slider"></span>
              </label>
            </div>

            <div class="setting-item">
              <div class="setting-info">
                <label>Newsletter</label>
                <p class="setting-description">Receive our monthly newsletter</p>
              </div>
              <label class="toggle">
                <input type="checkbox" v-model="settings.notifications.newsletter">
                <span class="toggle-slider"></span>
              </label>
            </div>

            <div class="setting-item">
              <div class="setting-info">
                <label>Product Updates</label>
                <p class="setting-description">Get notified about new features and updates</p>
              </div>
              <label class="toggle">
                <input type="checkbox" v-model="settings.notifications.productUpdates">
                <span class="toggle-slider"></span>
              </label>
            </div>
          </div>

          <div class="settings-group">
            <h3 class="group-title">Push Notifications</h3>
            
            <div class="setting-item">
              <div class="setting-info">
                <label>Browser Notifications</label>
                <p class="setting-description">Show desktop notifications</p>
              </div>
              <label class="toggle">
                <input type="checkbox" v-model="settings.notifications.browserNotifications">
                <span class="toggle-slider"></span>
              </label>
            </div>

            <div class="setting-item">
              <div class="setting-info">
                <label>Sound</label>
                <p class="setting-description">Play sound for notifications</p>
              </div>
              <label class="toggle">
                <input type="checkbox" v-model="settings.notifications.sound">
                <span class="toggle-slider"></span>
              </label>
            </div>
          </div>
        </div>

        <!-- Privacy Settings -->
        <div v-if="activeTab === 'privacy'" class="panel-content">
          <h2 class="panel-title">Privacy & Security</h2>
          
          <div class="settings-group">
            <h3 class="group-title">Privacy</h3>
            
            <div class="setting-item">
              <div class="setting-info">
                <label>Profile Visibility</label>
                <p class="setting-description">Control who can see your profile</p>
              </div>
              <select v-model="settings.privacy.profileVisibility" class="form-select">
                <option value="public">Public</option>
                <option value="friends">Friends Only</option>
                <option value="private">Private</option>
              </select>
            </div>

            <div class="setting-item">
              <div class="setting-info">
                <label>Show Online Status</label>
                <p class="setting-description">Let others see when you're online</p>
              </div>
              <label class="toggle">
                <input type="checkbox" v-model="settings.privacy.showOnlineStatus">
                <span class="toggle-slider"></span>
              </label>
            </div>

            <div class="setting-item">
              <div class="setting-info">
                <label>Activity Status</label>
                <p class="setting-description">Show your recent activity to others</p>
              </div>
              <label class="toggle">
                <input type="checkbox" v-model="settings.privacy.activityStatus">
                <span class="toggle-slider"></span>
              </label>
            </div>
          </div>

          <div class="settings-group">
            <h3 class="group-title">Security</h3>
            
            <div class="setting-item">
              <div class="setting-info">
                <label>Two-Factor Authentication</label>
                <p class="setting-description">Add an extra layer of security to your account</p>
              </div>
              <button class="btn btn-secondary">
                {% raw %}{{ settings.security.twoFactorEnabled ? 'Manage' : 'Enable' }}{% endraw %}
              </button>
            </div>

            <div class="setting-item">
              <div class="setting-info">
                <label>Login Notifications</label>
                <p class="setting-description">Get notified of new login attempts</p>
              </div>
              <label class="toggle">
                <input type="checkbox" v-model="settings.security.loginNotifications">
                <span class="toggle-slider"></span>
              </label>
            </div>

            <div class="setting-item">
              <div class="setting-info">
                <label>Active Sessions</label>
                <p class="setting-description">Manage your active login sessions</p>
              </div>
              <button class="btn btn-secondary">View Sessions</button>
            </div>
          </div>
        </div>

        <!-- Integrations Settings -->
        <div v-if="activeTab === 'integrations'" class="panel-content">
          <h2 class="panel-title">Integrations</h2>
          
          <div class="settings-group">
            <h3 class="group-title">Connected Services</h3>
            
            <div class="integration-list">
              <div v-for="integration in integrations" :key="integration.id" class="integration-item">
                <div class="integration-info">
                  <img :src="integration.icon" :alt="integration.name" class="integration-icon">
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
        <div class="settings-actions">
          <button @click="resetSettings" class="btn btn-secondary">
            Reset to Defaults
          </button>
          <button @click="saveSettings" class="btn btn-primary" :disabled="saving">
            {% raw %}{{ saving ? 'Saving...' : 'Save Changes' }}{% endraw %}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
{% if cookiecutter.use_typescript == 'y' -%}
import { ref, reactive } from 'vue'

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
{% else -%}
import { ref, reactive } from 'vue'
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

<style scoped>
.settings-view {
  padding: 2rem;
  max-width: 1400px;
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

.settings-content {
  display: grid;
  grid-template-columns: 250px 1fr;
  gap: 2rem;
}

.card {
  background: white;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
}

.settings-nav {
  padding: 1rem;
  height: fit-content;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  width: 100%;
  padding: 0.75rem 1rem;
  border: none;
  background: transparent;
  color: #4a5568;
  font-size: 0.875rem;
  font-weight: 500;
  border-radius: 0.375rem;
  cursor: pointer;
  transition: all 0.2s;
  text-align: left;
}

.nav-item:hover {
  background: #f7fafc;
  color: #2d3748;
}

.nav-item.active {
  background: #edf2f7;
  color: #4299e1;
}

.nav-icon {
  width: 20px;
  height: 20px;
}

.settings-panel {
  padding: 2rem;
  min-height: 500px;
}

.panel-content {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.panel-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1a202c;
  margin: 0 0 1rem 0;
}

.settings-group {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.group-title {
  font-size: 1rem;
  font-weight: 600;
  color: #2d3748;
  margin: 0 0 0.5rem 0;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid #e2e8f0;
}

.setting-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 0;
}

.setting-info {
  flex: 1;
}

.setting-info label {
  display: block;
  font-weight: 500;
  color: #2d3748;
  margin-bottom: 0.25rem;
}

.setting-description {
  font-size: 0.875rem;
  color: #718096;
  margin: 0;
}

.form-select {
  padding: 0.5rem 2rem 0.5rem 0.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.375rem;
  background: white;
  font-size: 0.875rem;
  cursor: pointer;
  min-width: 150px;
}

.theme-selector {
  display: flex;
  gap: 0.5rem;
}

.theme-option {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem;
  border: 2px solid #e2e8f0;
  border-radius: 0.5rem;
  background: white;
  cursor: pointer;
  transition: all 0.2s;
}

.theme-option:hover {
  border-color: #cbd5e0;
}

.theme-option.active {
  border-color: #4299e1;
  background: #ebf8ff;
}

.theme-icon {
  width: 30px;
  height: 30px;
}

.toggle {
  position: relative;
  display: inline-block;
  width: 48px;
  height: 24px;
}

.toggle input {
  opacity: 0;
  width: 0;
  height: 0;
}

.toggle-slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #cbd5e0;
  transition: 0.3s;
  border-radius: 24px;
}

.toggle-slider:before {
  position: absolute;
  content: "";
  height: 18px;
  width: 18px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  transition: 0.3s;
  border-radius: 50%;
}

.toggle input:checked + .toggle-slider {
  background-color: #4299e1;
}

.toggle input:checked + .toggle-slider:before {
  transform: translateX(24px);
}

.integration-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.integration-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
}

.integration-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.integration-icon {
  width: 40px;
  height: 40px;
  border-radius: 0.375rem;
}

.integration-info h4 {
  margin: 0 0 0.25rem 0;
  font-weight: 500;
  color: #2d3748;
}

.integration-info p {
  margin: 0;
  font-size: 0.875rem;
  color: #718096;
}

.settings-actions {
  display: flex;
  justify-content: space-between;
  padding-top: 2rem;
  margin-top: 2rem;
  border-top: 1px solid #e2e8f0;
}

.btn {
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  font-size: 0.875rem;
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

.btn-danger {
  background: #f56565;
  color: white;
}

.btn-danger:hover {
  background: #e53e3e;
}

@media (max-width: 768px) {
  .settings-view {
    padding: 1rem;
  }
  
  .settings-content {
    grid-template-columns: 1fr;
  }
  
  .settings-nav {
    display: flex;
    overflow-x: auto;
    padding: 0.5rem;
  }
  
  .nav-item {
    white-space: nowrap;
  }
  
  .setting-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .settings-actions {
    flex-direction: column;
    gap: 1rem;
  }
  
  .btn {
    width: 100%;
  }
}
</style>