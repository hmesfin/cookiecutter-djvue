<template>
  <div class="home">
    {% if cookiecutter.css_framework == 'tailwindcss' -%}
    <!-- Hero Section -->
    <section class="relative bg-white overflow-hidden dark:bg-gray-900">
      <div class="max-w-7xl mx-auto">
        <div class="relative z-10 pb-8 bg-white sm:pb-16 md:pb-20 lg:max-w-2xl lg:w-full lg:pb-28 xl:pb-32 dark:bg-gray-900">
          <main class="mt-10 mx-auto max-w-7xl px-4 sm:mt-12 sm:px-6 md:mt-16 lg:mt-20 lg:px-8 xl:mt-28">
            <div class="sm:text-center lg:text-left">
              <h1 class="text-4xl tracking-tight font-extrabold text-gray-900 sm:text-5xl md:text-6xl dark:text-gray-100">
                <span class="block xl:inline">{{ cookiecutter.project_name }}</span>
                <span class="block text-emerald-600 xl:inline">made simple</span>
              </h1>
              <p class="mt-3 text-base text-gray-500 sm:mt-5 sm:text-lg sm:max-w-xl sm:mx-auto md:mt-5 md:text-xl lg:mx-0 dark:text-gray-500">
                {{ cookiecutter.project_description }}
              </p>
              <div class="mt-5 sm:mt-8 sm:flex sm:justify-center lg:justify-start">
                <div class="rounded-md shadow dark:shadow-xl dark:shadow-gray-900/30">
                  <RouterLink
                    to="/auth/register"
                    class="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-white bg-emerald-600 hover:bg-emerald-700 md:py-4 md:text-lg md:px-10"
                  >
                    Get started
                  </RouterLink>
                </div>
                <div class="mt-3 sm:mt-0 sm:ml-3">
                  <RouterLink
                    to="/features"
                    class="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-emerald-700 bg-emerald-100 hover:bg-indigo-200 md:py-4 md:text-lg md:px-10"
                  >
                    Learn more
                  </RouterLink>
                </div>
              </div>
            </div>
          </main>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="py-12 bg-gray-50 dark:bg-gray-900">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center">
          <h2 class="text-base text-emerald-600 font-semibold tracking-wide uppercase">Features</h2>
          <p class="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-gray-900 sm:text-4xl dark:text-gray-100">
            Everything you need
          </p>
          <p class="mt-4 max-w-2xl text-xl text-gray-500 mx-auto dark:text-gray-500">
            Built with modern technologies and best practices.
          </p>
        </div>

        <div class="mt-10">
          <dl class="space-y-10 md:space-y-0 md:grid md:grid-cols-2 md:gap-x-8 md:gap-y-10">
            {% raw %}<div v-for="feature in features" :key="feature.name" class="relative">
              <dt>
                <div class="absolute flex items-center justify-center h-12 w-12 rounded-md bg-emerald-600 text-white">
                  <component :is="feature.icon" class="h-6 w-6" aria-hidden="true" />
                </div>
                <p class="ml-16 text-lg leading-6 font-medium text-gray-900 dark:text-gray-100">{{ feature.name }}</p>
              </dt>
              <dd class="mt-2 ml-16 text-base text-gray-500 dark:text-gray-500">{{ feature.description }}</dd>
            </div>{% endraw %}
          </dl>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="bg-emerald-700">
      <div class="max-w-2xl mx-auto text-center py-16 px-4 sm:py-20 sm:px-6 lg:px-8">
        <h2 class="text-3xl font-extrabold text-white sm:text-4xl">
          <span class="block">Ready to get started?</span>
          <span class="block">Start your free trial today.</span>
        </h2>
        <p class="mt-4 text-lg leading-6 text-indigo-200">
          Join thousands of satisfied users who are already using our platform.
        </p>
        <RouterLink
          to="/auth/register"
          class="mt-8 w-full inline-flex items-center justify-center px-5 py-3 border border-transparent text-base font-medium rounded-md text-emerald-600 bg-white hover:bg-emerald-50 sm:w-auto dark:bg-gray-900"
        >
          Sign up for free
        </RouterLink>
      </div>
    </section>
    {% else -%}
    <!-- Hero Section -->
    <section class="hero-section">
      <div class="hero-content">
        <h1>
          <span class="brand">{{ cookiecutter.project_name }}</span>
          <span class="tagline">made simple</span>
        </h1>
        <p class="description">{{ cookiecutter.project_description }}</p>
        <div class="hero-actions">
          <RouterLink to="/auth/register" class="btn btn-primary btn-lg">
            Get started
          </RouterLink>
          <RouterLink to="/features" class="btn btn-secondary btn-lg">
            Learn more
          </RouterLink>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="features-section">
      <div class="container">
        <div class="mb-6">
          <h2 class="section-subtitle">Features</h2>
          <h3 class="text-xl font-semibold text-gray-900 mb-2 dark:text-gray-100">Everything you need</h3>
          <p class="text-gray-600 dark:text-gray-400">
            Built with modern technologies and best practices.
          </p>
        </div>

        <div class="features-grid">
          {% raw %}<div v-for="feature in features" :key="feature.name" class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 dark:bg-gray-900 dark:shadow-xl dark:shadow-gray-900/40">
            <div class="feature-icon">
              <span>{{ feature.emoji }}</span>
            </div>
            <h4 class="feature-name">{{ feature.name }}</h4>
            <p class="feature-description">{{ feature.description }}</p>
          </div>{% endraw %}
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="cta-section">
      <div class="cta-content">
        <h2>Ready to get started?</h2>
        <p>Join thousands of satisfied users who are already using our platform.</p>
        <RouterLink to="/auth/register" class="btn btn-white btn-lg">
          Sign up for free
        </RouterLink>
      </div>
    </section>
    {%- endif %}
  </div>
</template>

<script setup{% if cookiecutter.use_typescript == 'y' %} lang="ts"{% endif %}>
import { ref } from 'vue'

const features = ref([
  {
    name: 'Modern Stack',
    description: 'Built with Django {{ cookiecutter.django_version }} and Vue.js {{ cookiecutter.vue_version }} for optimal performance.',
    icon: 'CodeBracketIcon',
    emoji: '⚡',
  },
  {
    name: 'Authentication',
    description: 'Secure {% if cookiecutter.api_authentication == "jwt" %}JWT-based{% elif cookiecutter.api_authentication == "token" %}token-based{% else %}session-based{% endif %} authentication system.',
    icon: 'LockClosedIcon',
    emoji: '🔒',
  },
  {
    name: 'API First',
    description: 'RESTful API design with comprehensive documentation.',
    icon: 'ServerIcon',
    emoji: '🚀',
  },
  {
    name: 'Responsive Design',
    description: 'Beautiful, responsive UI that works on all devices.',
    icon: 'DevicePhoneMobileIcon',
    emoji: '📱',
  },
])
</script>

<style scoped>
{% if cookiecutter.css_framework == 'none' -%}
.hero-section {
  padding: 4rem 2rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  text-align: center;
}

.hero-content {
  max-width: 800px;
  margin: 0 auto;
}

.hero-content h1 {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.hero-content .brand {
  display: block;
  font-weight: 800;
}

.hero-content .tagline {
  display: block;
  font-weight: 300;
  opacity: 0.9;
}

.hero-content .description {
  font-size: 1.25rem;
  margin-bottom: 2rem;
  opacity: 0.9;
}

.hero-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.features-section {
  padding: 4rem 2rem;
  background: #f8f9fa;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

.section-header {
  text-align: center;
  margin-bottom: 3rem;
}

.section-subtitle {
  color: var(--primary-color);
  font-size: 0.875rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin-bottom: 0.5rem;
}

.section-title {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.section-description {
  color: #666;
  font-size: 1.125rem;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
}

.feature-card {
  background: white;
  padding: 2rem;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.feature-icon {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.feature-name {
  font-size: 1.25rem;
  margin-bottom: 0.5rem;
}

.feature-description {
  color: #666;
  line-height: 1.6;
}

.cta-section {
  padding: 4rem 2rem;
  background: var(--primary-color);
  color: white;
  text-align: center;
}

.cta-content {
  max-width: 600px;
  margin: 0 auto;
}

.cta-content h2 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.cta-content p {
  font-size: 1.125rem;
  margin-bottom: 2rem;
  opacity: 0.9;
}

.btn-white {
  background: white;
  color: var(--primary-color);
}

.btn-white:hover {
  background: #f8f9fa;
}

.btn-lg {
  padding: 0.75rem 2rem;
  font-size: 1.125rem;
}
{%- endif %}
</style>