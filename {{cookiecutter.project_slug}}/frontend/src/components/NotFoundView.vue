<template>
  <div class="not-found">
    {% if cookiecutter.css_framework == 'tailwindcss' -%}
    <div class="min-h-screen flex items-center justify-center px-4 sm:px-6 lg:px-8">
      <div class="max-w-md w-full text-center">
        <h1 class="text-9xl font-bold text-gray-300">404</h1>
        <h2 class="mt-4 text-3xl font-bold text-gray-900 dark:text-gray-100">Page not found</h2>
        <p class="mt-2 text-gray-600 dark:text-gray-400">
          Sorry, we couldn't find the page you're looking for.
        </p>
        <div class="mt-6 space-x-4">
          <RouterLink
            to="/"
            class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
          >
            Go to Homepage
          </RouterLink>
          <button
            @click="goBack"
            class="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 dark:border-gray-600 dark:text-gray-300 dark:bg-gray-900 dark:hover:bg-gray-800"
          >
            Go Back
          </button>
        </div>
      </div>
    </div>
    {% else -%}
    <div class="not-found-container">
      <div class="not-found-content">
        <h1 class="error-code">404</h1>
        <h2 class="error-title">Page not found</h2>
        <p class="error-message">
          Sorry, we couldn't find the page you're looking for.
        </p>
        <div class="error-actions">
          <RouterLink to="/" class="btn btn-primary">
            Go to Homepage
          </RouterLink>
          <button @click="goBack" class="btn btn-secondary">
            Go Back
          </button>
        </div>
      </div>
    </div>
    {%- endif %}
  </div>
</template>

<script setup{% if cookiecutter.use_typescript == 'y' %} lang="ts"{% endif %}>
import { useRouter } from 'vue-router'

const router = useRouter()

const goBack = () => {
  if (window.history.length > 1) {
    router.go(-1)
  } else {
    router.push('/')
  }
}
</script>

<style scoped>
{% if cookiecutter.css_framework == 'none' -%}
.not-found-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.not-found-content {
  text-align: center;
  max-width: 400px;
}

.error-code {
  font-size: 8rem;
  font-weight: bold;
  color: #e0e0e0;
  margin: 0;
  line-height: 1;
}

.error-title {
  font-size: 2rem;
  margin: 1rem 0;
}

.error-message {
  color: #666;
  margin-bottom: 2rem;
}

.error-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
}
{%- endif %}
</style>