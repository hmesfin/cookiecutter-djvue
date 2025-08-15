<template>
  <div class="auth-layout">
    {% if cookiecutter.css_framework == 'tailwindcss' -%}
    <div class="min-h-screen flex flex-col">
      <!-- Auth Header -->
      <header class="bg-white shadow-sm dark:bg-gray-900 dark:shadow-lg dark:shadow-gray-900/30">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="flex justify-between items-center py-4">
            <RouterLink to="/" class="flex items-center">
              <AppLogo size="lg" />
            </RouterLink>
            <nav class="flex space-x-4">
              <RouterLink 
                to="/auth/login" 
                class="text-gray-600 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium dark:text-gray-400 dark:hover:text-gray-100"
                :class="{ 'bg-gray-100': $route.path === '/auth/login' }"
              >
                Login
              </RouterLink>
              <RouterLink 
                to="/auth/register"
                class="text-gray-600 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium dark:text-gray-400 dark:hover:text-gray-100"
                :class="{ 'bg-gray-100': $route.path === '/auth/register' }"
              >
                Register
              </RouterLink>
            </nav>
          </div>
        </div>
      </header>

      <!-- Main Content -->
      <main class="flex-1 flex items-center justify-center px-4 sm:px-6 lg:px-8 bg-gray-50 dark:bg-gray-900">
        <div class="w-full max-w-md">
          <transition name="fade" mode="out-in">
            <RouterView />
          </transition>
        </div>
      </main>

      <!-- Footer -->
      <footer class="bg-white border-t dark:bg-gray-900">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <p class="text-center text-sm text-gray-500 dark:text-gray-500">
            © {% raw %}{{ new Date().getFullYear() }}{% endraw %} {{ cookiecutter.project_name }}. All rights reserved.
          </p>
        </div>
      </footer>
    </div>
    {% elif cookiecutter.css_framework == 'bootstrap-vue-3' -%}
    <div class="auth-layout d-flex flex-column min-vh-100">
      <!-- Auth Header -->
      <b-navbar toggleable="lg" type="light" variant="white" class="shadow-sm dark:shadow-lg dark:shadow-gray-900/30">
        <b-container>
          <b-navbar-brand to="/">
            <span class="fs-4 fw-bold text-primary">{{ cookiecutter.project_name }}</span>
          </b-navbar-brand>
          <b-navbar-nav class="ms-auto">
            <b-nav-item to="/auth/login" :active="$route.path === '/auth/login'">
              Login
            </b-nav-item>
            <b-nav-item to="/auth/register" :active="$route.path === '/auth/register'">
              Register
            </b-nav-item>
          </b-navbar-nav>
        </b-container>
      </b-navbar>

      <!-- Main Content -->
      <b-container fluid class="flex-grow-1 d-flex align-items-center justify-content-center bg-light py-5">
        <div style="width: 100%; max-width: 400px;">
          <transition name="fade" mode="out-in">
            <RouterView />
          </transition>
        </div>
      </b-container>

      <!-- Footer -->
      <footer class="bg-white border-top py-3 dark:bg-gray-900">
        <b-container>
          <p class="text-center text-muted mb-0">
            © {% raw %}{{ new Date().getFullYear() }}{% endraw %} {{ cookiecutter.project_name }}. All rights reserved.
          </p>
        </b-container>
      </footer>
    </div>
    {% else -%}
    <div class="auth-layout">
      <header class="auth-header">
        <div class="container">
          <RouterLink to="/" class="logo">{{ cookiecutter.project_name }}</RouterLink>
          <nav class="auth-nav">
            <RouterLink to="/auth/login" :class="{ active: $route.path === '/auth/login' }">
              Login
            </RouterLink>
            <RouterLink to="/auth/register" :class="{ active: $route.path === '/auth/register' }">
              Register
            </RouterLink>
          </nav>
        </div>
      </header>
      
      <main class="auth-main">
        <div class="auth-container">
          <transition name="fade" mode="out-in">
            <RouterView />
          </transition>
        </div>
      </main>
      
      <footer class="auth-footer">
        <p>© {% raw %}{{ new Date().getFullYear() }}{% endraw %} {{ cookiecutter.project_name }}. All rights reserved.</p>
      </footer>
    </div>
    {%- endif %}
  </div>
</template>

<script setup{% if cookiecutter.use_typescript == 'y' %} lang="ts"{% endif %}>
import AppLogo from '@/components/AppLogo.vue'
import { RouterView, RouterLink } from 'vue-router'
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
.auth-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.auth-header {
  background: white;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  padding: 1rem 0;
}

.auth-header .container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

.logo {
  font-size: 1.5rem;
  font-weight: bold;
  color: var(--primary-color);
  text-decoration: none;
}

.auth-nav {
  display: flex;
  gap: 1rem;
}

.auth-nav a {
  padding: 0.5rem 1rem;
  text-decoration: none;
  color: #666;
  border-radius: 0.25rem;
  transition: all 0.3s;
}

.auth-nav a:hover,
.auth-nav a.active {
  background: #f0f0f0;
  color: var(--primary-color);
}

.auth-main {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f5f5;
  padding: 2rem;
}

.auth-container {
  width: 100%;
  max-width: 400px;
}

.auth-footer {
  background: white;
  border-top: 1px solid #e0e0e0;
  padding: 1rem;
  text-align: center;
  color: #666;
}
{%- endif %}
</style>