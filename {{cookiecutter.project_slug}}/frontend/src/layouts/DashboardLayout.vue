<template>
  <div class="dashboard-layout">
    {% if cookiecutter.css_framework == 'tailwindcss' -%}
    <div class="min-h-screen bg-gray-100 dark:bg-gray-800">
      <!-- Sidebar -->
      <aside 
        class="fixed inset-y-0 left-0 z-50 w-64 bg-gray-900 transform transition-transform duration-300 lg:translate-x-0"
        :class="sidebarOpen ? 'translate-x-0' : '-translate-x-full'"
      >
        <div class="flex h-full flex-col">
          <!-- Logo -->
          <div class="flex h-16 items-center justify-between px-4 bg-gray-800">
            <span class="text-xl font-semibold text-white">{{ cookiecutter.project_name }}</span>
            <button 
              @click="sidebarOpen = false"
              class="lg:hidden text-gray-400 hover:text-white dark:text-gray-600"
            >
              <IconLucideX class="h-6 w-6" />
            </button>
          </div>

          <!-- Navigation -->
          <nav class="flex-1 space-y-1 px-2 py-4">
            {% raw %}<RouterLink
              v-for="item in navigation"
              :key="item.name"
              :to="item.to"
              class="group flex items-center px-2 py-2 text-sm font-medium rounded-md transition-colors"
              :class="[
                isActive(item.to)
                  ? 'bg-gray-800 text-white'
                  : 'text-gray-300 hover:bg-gray-700 hover:text-white'
              ]"
            >
              <IconLucideHome v-if="item.icon === 'home'" class="mr-3 h-5 w-5 flex-shrink-0" />
              <IconLucideUser v-else-if="item.icon === 'user'" class="mr-3 h-5 w-5 flex-shrink-0" />
              <IconLucideSettings v-else-if="item.icon === 'settings'" class="mr-3 h-5 w-5 flex-shrink-0" />
              <IconLucideBarChart3 v-else-if="item.icon === 'bar-chart-3'" class="mr-3 h-5 w-5 flex-shrink-0" />
              <IconLucideShoppingCart v-else-if="item.icon === 'shopping-cart'" class="mr-3 h-5 w-5 flex-shrink-0" />
              <IconLucideUsers v-else-if="item.icon === 'users'" class="mr-3 h-5 w-5 flex-shrink-0" />
              {{ item.name }}
            </RouterLink>{% endraw %}
          </nav>

          <!-- User section -->
          <div class="border-t border-gray-700 p-4">
            <div class="flex items-center">
              <img
                class="h-8 w-8 rounded-full"
                :src="userAvatar"
                :alt="userName"
              >
              <div class="ml-3">
                <p class="text-sm font-medium text-white">{% raw %}{{ userName }}{% endraw %}</p>
                <button
                  @click="handleLogout"
                  class="text-xs text-gray-400 hover:text-white dark:text-gray-600"
                >
                  Logout
                </button>
              </div>
            </div>
          </div>
        </div>
      </aside>

      <!-- Main content -->
      <div class="lg:pl-64">
        <!-- Top bar -->
        <header class="sticky top-0 z-40 bg-white shadow dark:bg-gray-900 dark:shadow-xl dark:shadow-gray-900/30">
          <div class="flex h-16 items-center justify-between px-4 sm:px-6 lg:px-8">
            <button
              @click="sidebarOpen = true"
              class="lg:hidden text-gray-500 hover:text-gray-900 dark:text-gray-500 dark:hover:text-gray-100"
            >
              <IconLucideMenu class="h-6 w-6" />
            </button>
            
            <div class="flex items-center space-x-4">
              <h1 class="text-2xl font-semibold text-gray-900 dark:text-gray-100">{% raw %}{{ pageTitle }}{% endraw %}</h1>
            </div>

            <div class="flex items-center space-x-4">
              <!-- Dark mode toggle -->
              <DarkModeToggle />
              
              <!-- Notifications -->
              <button class="relative text-gray-400 hover:text-gray-500 dark:text-gray-600">
                <IconLucideBell class="h-6 w-6" />
                <span class="absolute top-0 right-0 block h-2 w-2 rounded-full bg-red-400 ring-2 ring-white" />
              </button>

              <!-- User dropdown -->
              <div class="relative">
                <button
                  @click="userMenuOpen = !userMenuOpen"
                  class="flex items-center text-sm rounded-full focus:outline-none focus:ring-2 focus:ring-emerald-500 dark:focus:ring-emerald-400"
                >
                  <img class="h-8 w-8 rounded-full" :src="userAvatar" :alt="userName">
                </button>
                
                <div
                  v-if="userMenuOpen"
                  @click.away="userMenuOpen = false"
                  class="absolute right-0 mt-2 w-48 rounded-md bg-white py-1 shadow-lg ring-1 ring-black ring-opacity-5 dark:bg-gray-900 dark:shadow-2xl dark:shadow-gray-900/50"
                >
                  <RouterLink to="/dashboard/profile" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-700">
                    Your Profile
                  </RouterLink>
                  <RouterLink to="/dashboard/settings" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-700">
                    Settings
                  </RouterLink>
                  <hr class="my-1">
                  <button @click="handleLogout" class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-700">
                    Sign out
                  </button>
                </div>
              </div>
            </div>
          </div>
        </header>

        <!-- Page content -->
        <main class="flex-1">
          <div class="py-6 px-4 sm:px-6 lg:px-8">
            <transition name="fade" mode="out-in">
              <RouterView />
            </transition>
          </div>
        </main>
      </div>
    </div>
    {% else -%}
    <div class="dashboard-layout">
      <!-- Simplified layout for non-Tailwind -->
      <aside class="dashboard-sidebar">
        <div class="sidebar-header">
          <h2>{{ cookiecutter.project_name }}</h2>
        </div>
        <nav class="sidebar-nav">
          {% raw %}<RouterLink
            v-for="item in navigation"
            :key="item.name"
            :to="item.to"
            :class="{ active: isActive(item.to) }"
          >
            {{ item.name }}
          </RouterLink>{% endraw %}
        </nav>
        <div class="sidebar-user">
          <img :src="userAvatar" :alt="userName">
          <span>{% raw %}{{ userName }}{% endraw %}</span>
          <button @click="handleLogout">Logout</button>
        </div>
      </aside>
      
      <div class="dashboard-main">
        <header class="dashboard-header">
          <h1>{% raw %}{{ pageTitle }}{% endraw %}</h1>
          <div class="flex items-center gap-3">
            <button @click="handleLogout">Logout</button>
          </div>
        </header>
        
        <main class="dashboard-content">
          <transition name="fade" mode="out-in">
            <RouterView />
          </transition>
        </main>
      </div>
    </div>
    {%- endif %}
    
    <!-- Confirmation Dialog -->
    <ConfirmDialog ref="confirmDialog" />
  </div>
</template>

<script setup{% if cookiecutter.use_typescript == 'y' %} lang="ts"{% endif %}>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import DarkModeToggle from '@/components/DarkModeToggle.vue'
import ConfirmDialog from '@/components/ConfirmDialog.vue'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const sidebarOpen = ref(false)
const userMenuOpen = ref(false)
const confirmDialog = ref()

// Navigation items with Lucide icons
const navigation = [
  { name: 'Dashboard', to: '/dashboard', icon: 'home' },
  { name: 'Profile', to: '/dashboard/profile', icon: 'user' },
  { name: 'Settings', to: '/dashboard/settings', icon: 'settings' },
  { name: 'Analytics', to: '/dashboard/analytics', icon: 'bar-chart-3' },
  { name: 'Orders', to: '/dashboard/orders', icon: 'shopping-cart' },
  { name: 'Users', to: '/dashboard/users', icon: 'users' },
]

// Computed properties
const userName = computed(() => {
  const user = authStore.user
  if (user?.first_name && user?.last_name) {
    return `${user.first_name} ${user.last_name}`
  }
  return user?.username || 'User'
})

const userAvatar = computed(() => {
  return authStore.user?.avatar || `https://ui-avatars.com/api/?name=${userName.value}&background=6366f1&color=fff`
})

const pageTitle = computed(() => {
  const currentRoute = navigation.find(item => isActive(item.to))
  return currentRoute?.name || 'Dashboard'
})

// Methods
const isActive = (path{% if cookiecutter.use_typescript == 'y' %}: string{% endif %}) => {
  return route.path.startsWith(path)
}

const handleLogout = async () => {
  const confirmed = await confirmDialog.value.open({
    title: 'Confirm Logout',
    message: 'Are you sure you want to log out of your account?',
    confirmText: 'Log Out',
    cancelText: 'Cancel',
    confirmClass: 'btn-danger'
  })
  
  if (confirmed) {
    await authStore.logout()
    router.push('/auth/login')
  }
}
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

{% if cookiecutter.css_framework == 'none' -%}
.dashboard-layout {
  display: flex;
  min-height: 100vh;
}

.dashboard-sidebar {
  width: 250px;
  background: #1a1a1a;
  color: white;
  display: flex;
  flex-direction: column;
}

.sidebar-header {
  padding: 1rem;
  background: #111;
  border-bottom: 1px solid #333;
}

.sidebar-header h2 {
  margin: 0;
  font-size: 1.25rem;
}

.sidebar-nav {
  flex: 1;
  padding: 1rem 0;
}

.sidebar-nav a {
  display: block;
  padding: 0.75rem 1rem;
  color: #ccc;
  text-decoration: none;
  transition: all 0.3s;
}

.sidebar-nav a:hover,
.sidebar-nav a.active {
  background: #333;
  color: white;
}

.sidebar-user {
  padding: 1rem;
  border-top: 1px solid #333;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.sidebar-user img {
  width: 32px;
  height: 32px;
  border-radius: 50%;
}

.sidebar-user button {
  margin-left: auto;
  padding: 0.25rem 0.5rem;
  background: #333;
  color: white;
  border: none;
  border-radius: 0.25rem;
  cursor: pointer;
}

.dashboard-main {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.dashboard-header {
  background: white;
  padding: 1rem 2rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.dashboard-header h1 {
  margin: 0;
  font-size: 1.5rem;
}

.dashboard-content {
  flex: 1;
  padding: 2rem;
  background: #f5f5f5;
}
{%- endif %}
</style>