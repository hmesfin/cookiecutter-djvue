<template>
  <div class="main-layout">
    {% if cookiecutter.css_framework == 'tailwindcss' -%}
    <div class="min-h-screen flex flex-col">
      <!-- Navigation -->
      <nav class="bg-white shadow-lg">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="flex justify-between h-16">
            <div class="flex">
              <!-- Logo -->
              <RouterLink to="/" class="flex items-center">
                <span class="text-xl font-bold text-indigo-600">{{ cookiecutter.project_name }}</span>
              </RouterLink>
              
              <!-- Primary navigation -->
              <div class="hidden sm:ml-6 sm:flex sm:space-x-8">
                {% raw %}<RouterLink
                  v-for="item in navigation"
                  :key="item.name"
                  :to="item.to"
                  class="inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium transition-colors"
                  :class="[
                    isActive(item.to)
                      ? 'border-indigo-500 text-gray-900'
                      : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'
                  ]"
                >
                  {{ item.name }}
                </RouterLink>{% endraw %}
              </div>
            </div>

            <!-- Right side -->
            <div class="flex items-center space-x-4">
              <template v-if="!authStore.isAuthenticated">
                <RouterLink
                  to="/auth/login"
                  class="text-gray-500 hover:text-gray-700 px-3 py-2 rounded-md text-sm font-medium"
                >
                  Sign in
                </RouterLink>
                <RouterLink
                  to="/auth/register"
                  class="bg-indigo-600 text-white hover:bg-indigo-700 px-4 py-2 rounded-md text-sm font-medium"
                >
                  Get Started
                </RouterLink>
              </template>
              <template v-else>
                <RouterLink
                  to="/dashboard"
                  class="bg-indigo-600 text-white hover:bg-indigo-700 px-4 py-2 rounded-md text-sm font-medium"
                >
                  Dashboard
                </RouterLink>
              </template>
            </div>

            <!-- Mobile menu button -->
            <div class="flex items-center sm:hidden">
              <button
                @click="mobileMenuOpen = !mobileMenuOpen"
                class="inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100"
              >
                <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    v-if="!mobileMenuOpen"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M4 6h16M4 12h16M4 18h16"
                  />
                  <path
                    v-else
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M6 18L18 6M6 6l12 12"
                  />
                </svg>
              </button>
            </div>
          </div>
        </div>

        <!-- Mobile menu -->
        <div v-if="mobileMenuOpen" class="sm:hidden">
          <div class="pt-2 pb-3 space-y-1">
            {% raw %}<RouterLink
              v-for="item in navigation"
              :key="item.name"
              :to="item.to"
              class="block pl-3 pr-4 py-2 border-l-4 text-base font-medium transition-colors"
              :class="[
                isActive(item.to)
                  ? 'bg-indigo-50 border-indigo-500 text-indigo-700'
                  : 'border-transparent text-gray-500 hover:bg-gray-50 hover:border-gray-300 hover:text-gray-700'
              ]"
              @click="mobileMenuOpen = false"
            >
              {{ item.name }}
            </RouterLink>{% endraw %}
          </div>
          <div class="pt-4 pb-3 border-t border-gray-200">
            <div class="space-y-1">
              <template v-if="!authStore.isAuthenticated">
                <RouterLink
                  to="/auth/login"
                  class="block px-4 py-2 text-base font-medium text-gray-500 hover:text-gray-800 hover:bg-gray-100"
                  @click="mobileMenuOpen = false"
                >
                  Sign in
                </RouterLink>
                <RouterLink
                  to="/auth/register"
                  class="block px-4 py-2 text-base font-medium text-gray-500 hover:text-gray-800 hover:bg-gray-100"
                  @click="mobileMenuOpen = false"
                >
                  Get Started
                </RouterLink>
              </template>
              <template v-else>
                <RouterLink
                  to="/dashboard"
                  class="block px-4 py-2 text-base font-medium text-gray-500 hover:text-gray-800 hover:bg-gray-100"
                  @click="mobileMenuOpen = false"
                >
                  Dashboard
                </RouterLink>
              </template>
            </div>
          </div>
        </div>
      </nav>

      <!-- Main content -->
      <main class="flex-1">
        <transition name="fade" mode="out-in">
          <RouterView />
        </transition>
      </main>

      <!-- Footer -->
      <footer class="bg-gray-900">
        <div class="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
          <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div class="col-span-1 md:col-span-2">
              <span class="text-2xl font-bold text-white">{{ cookiecutter.project_name }}</span>
              <p class="mt-2 text-gray-400">{{ cookiecutter.project_description }}</p>
            </div>
            <div>
              <h3 class="text-sm font-semibold text-gray-400 uppercase tracking-wider">Quick Links</h3>
              <ul class="mt-4 space-y-2">
                <li><a href="#" class="text-gray-300 hover:text-white">About</a></li>
                <li><a href="#" class="text-gray-300 hover:text-white">Features</a></li>
                <li><a href="#" class="text-gray-300 hover:text-white">Pricing</a></li>
              </ul>
            </div>
            <div>
              <h3 class="text-sm font-semibold text-gray-400 uppercase tracking-wider">Legal</h3>
              <ul class="mt-4 space-y-2">
                <li><a href="#" class="text-gray-300 hover:text-white">Privacy Policy</a></li>
                <li><a href="#" class="text-gray-300 hover:text-white">Terms of Service</a></li>
              </ul>
            </div>
          </div>
          <div class="mt-8 border-t border-gray-700 pt-8">
            <p class="text-center text-gray-400">
              © {% raw %}{{ new Date().getFullYear() }}{% endraw %} {{ cookiecutter.project_name }}. All rights reserved.
            </p>
          </div>
        </div>
      </footer>
    </div>
    {% else -%}
    <div class="main-layout">
      <!-- Simplified layout for non-Tailwind -->
      <nav class="main-nav">
        <div class="nav-container">
          <RouterLink to="/" class="nav-logo">{{ cookiecutter.project_name }}</RouterLink>
          <div class="nav-links">
            {% raw %}<RouterLink
              v-for="item in navigation"
              :key="item.name"
              :to="item.to"
              :class="{ active: isActive(item.to) }"
            >
              {{ item.name }}
            </RouterLink>{% endraw %}
          </div>
          <div class="nav-actions">
            <template v-if="!authStore.isAuthenticated">
              <RouterLink to="/auth/login" class="btn-link">Sign in</RouterLink>
              <RouterLink to="/auth/register" class="btn btn-primary">Get Started</RouterLink>
            </template>
            <template v-else>
              <RouterLink to="/dashboard" class="btn btn-primary">Dashboard</RouterLink>
            </template>
          </div>
        </div>
      </nav>
      
      <main class="main-content">
        <transition name="fade" mode="out-in">
          <RouterView />
        </transition>
      </main>
      
      <footer class="main-footer">
        <div class="footer-container">
          <p>© {% raw %}{{ new Date().getFullYear() }}{% endraw %} {{ cookiecutter.project_name }}. All rights reserved.</p>
        </div>
      </footer>
    </div>
    {%- endif %}
  </div>
</template>

<script setup{% if cookiecutter.use_typescript == 'y' %} lang="ts"{% endif %}>
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const authStore = useAuthStore()

const mobileMenuOpen = ref(false)

const navigation = [
  { name: 'Home', to: '/' },
  { name: 'Features', to: '/features' },
  { name: 'Pricing', to: '/pricing' },
  { name: 'About', to: '/about' },
  { name: 'Contact', to: '/contact' },
]

const isActive = (path{% if cookiecutter.use_typescript == 'y' %}: string{% endif %}) => {
  return route.path === path
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
.main-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-nav {
  background: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 100;
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-logo {
  font-size: 1.25rem;
  font-weight: bold;
  color: var(--primary-color);
  text-decoration: none;
}

.nav-links {
  display: flex;
  gap: 2rem;
}

.nav-links a {
  text-decoration: none;
  color: #666;
  transition: color 0.3s;
}

.nav-links a:hover,
.nav-links a.active {
  color: var(--primary-color);
}

.nav-actions {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.main-content {
  flex: 1;
}

.main-footer {
  background: #1a1a1a;
  color: white;
  padding: 3rem 0;
}

.footer-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
  text-align: center;
}
{%- endif %}
</style>