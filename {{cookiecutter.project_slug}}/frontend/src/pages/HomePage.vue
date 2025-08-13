<template>
  <div class="home-page">
    {% if cookiecutter.css_framework == 'bootstrap-vue-3' -%}
    <b-container>
      <b-row class="mt-5">
        <b-col>
          <h1>Welcome to {{ cookiecutter.project_name }}</h1>
          <p class="lead">{{ cookiecutter.project_description }}</p>
          <div class="mt-4">
            <b-button v-if="!authStore.isAuthenticated" variant="primary" :to="{ name: 'register' }">
              Get Started
            </b-button>
            <b-button v-else variant="primary" :to="{ name: 'dashboard' }">
              Go to Dashboard
            </b-button>
          </div>
        </b-col>
      </b-row>
    </b-container>
    {% elif cookiecutter.css_framework == 'tailwindcss' -%}
    <div class="min-h-screen bg-gray-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-20">
        <div class="text-center">
          <h1 class="text-4xl font-bold text-gray-900 sm:text-5xl md:text-6xl">
            Welcome to {{ cookiecutter.project_name }}
          </h1>
          <p class="mt-3 max-w-md mx-auto text-base text-gray-500 sm:text-lg md:mt-5 md:text-xl md:max-w-3xl">
            {{ cookiecutter.project_description }}
          </p>
          <div class="mt-5 max-w-md mx-auto sm:flex sm:justify-center md:mt-8">
            <RouterLink
              v-if="!authStore.isAuthenticated"
              :to="{ name: 'register' }"
              class="inline-flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 md:py-4 md:text-lg md:px-10"
            >
              Get Started
            </RouterLink>
            <RouterLink
              v-else
              :to="{ name: 'dashboard' }"
              class="inline-flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 md:py-4 md:text-lg md:px-10"
            >
              Go to Dashboard
            </RouterLink>
          </div>
        </div>
      </div>
    </div>
    {% else -%}
    <div class="container">
      <h1>Welcome to {{ cookiecutter.project_name }}</h1>
      <p>{{ cookiecutter.project_description }}</p>
      <div>
        <RouterLink v-if="!authStore.isAuthenticated" :to="{ name: 'register' }">
          Get Started
        </RouterLink>
        <RouterLink v-else :to="{ name: 'dashboard' }">
          Go to Dashboard
        </RouterLink>
      </div>
    </div>
    {%- endif %}
  </div>
</template>

<script setup{% if cookiecutter.use_typescript == 'y' %} lang="ts"{% endif %}>
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
</script>