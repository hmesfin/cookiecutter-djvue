<template>
  <div class="features-view">
    <!-- Hero Section -->
    <section class="bg-gradient-to-br from-indigo-500 to-purple-600 text-white py-20">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center max-w-4xl mx-auto">
          <h1 class="text-5xl font-bold mb-4">Powerful Features for Modern Teams</h1>
          <p class="text-xl opacity-95">
            Everything you need to build, deploy, and scale your applications with confidence.
            Our comprehensive feature set empowers teams to work smarter, not harder.
          </p>
        </div>
      </div>
    </section>

    <!-- Main Features Grid -->
    <section class="py-20 bg-white dark:bg-gray-900">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="mb-6">
          <h2 class="text-xl font-semibold text-gray-900 mb-2 dark:text-gray-100">Core Features</h2>
          <p class="text-gray-600 dark:text-gray-400">
            Built with the latest technologies and best practices
          </p>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          <div v-for="feature in coreFeatures" :key="feature.id" class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 dark:bg-gray-900 dark:shadow-xl dark:shadow-gray-900/40">
            <div class="w-16 h-16 rounded-full flex items-center justify-center text-white mb-4" :style="{ background: feature.color }">
              <svg class="icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path :d="feature.iconPath" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path>
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-2">{% raw %}{{ feature.title }}{% endraw %}</h3>
            <p class="text-gray-600 dark:text-gray-400">{% raw %}{{ feature.description }}{% endraw %}</p>
            <ul class="feature-list">
              <li v-for="item in feature.items" :key="item">
                <IconLucideCheck class="w-5 h-5 text-green-500 flex-shrink-0 mt-0.5" />
                {% raw %}{{ item }}{% endraw %}
              </li>
            </ul>
          </div>
        </div>
      </div>
    </section>

    <!-- Technical Stack -->
    <section class="tech-stack-section">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="mb-6">
          <h2 class="text-xl font-semibold text-gray-900 mb-2 dark:text-gray-100">Built with Modern Technology</h2>
          <p class="text-gray-600 dark:text-gray-400">
            Leveraging the best tools and frameworks for optimal performance
          </p>
        </div>
        
        <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-8">
          <div v-for="tech in techStack" :key="tech.name" class="text-center">
            <div class="w-20 h-20 mx-auto mb-3 rounded-lg bg-gray-100 dark:bg-gray-800 flex items-center justify-center">
              <img :src="tech.logo" :alt="tech.name">
            </div>
            <h4 class="text-sm font-medium text-gray-700 dark:text-gray-300">{% raw %}{{ tech.name }}{% endraw %}</h4>
            <p class="text-xs text-gray-500 dark:text-gray-500">{% raw %}{{ tech.description }}{% endraw %}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Feature Comparison -->
    <section class="py-20 bg-gray-50 dark:bg-gray-800 dark:bg-gray-900">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="mb-6">
          <h2 class="text-xl font-semibold text-gray-900 mb-2 dark:text-gray-100">Why Choose Us?</h2>
          <p class="text-gray-600 dark:text-gray-400">
            See how we compare to traditional solutions
          </p>
        </div>
        
        <div class="bg-white dark:bg-gray-900 rounded-lg shadow-lg overflow-hidden dark:shadow-2xl dark:shadow-gray-900/50">
          <table>
            <thead>
              <tr>
                <th>Feature</th>
                <th class="highlight">Our Platform</th>
                <th>Traditional Solutions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="comparison in comparisons" :key="comparison.feature">
                <td class="feature-name">{% raw %}{{ comparison.feature }}{% endraw %}</td>
                <td class="our-solution">
                  <IconLucideCheckCircle class="icon-check" />
                  {% raw %}{{ comparison.ours }}{% endraw %}
                </td>
                <td class="other-solution">
                  <svg v-if="comparison.othersHas" class="icon-partial" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                  <IconLucideXCircle class="icon-no" />
                  {% raw %}{{ comparison.others }}{% endraw %}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="py-20 bg-gradient-to-br from-indigo-500 to-purple-600 text-white text-center">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="max-w-3xl mx-auto">
          <h2 class="text-4xl font-bold mb-4">Ready to Get Started?</h2>
          <p class="text-xl mb-8 opacity-95">
            Join thousands of teams already using our platform to build amazing products
          </p>
          <div class="flex gap-4 justify-center">
            <router-link to="/auth/register" class="btn bg-indigo-600 text-white hover:bg-indigo-700 px-8 py-4 text-lg rounded-lg font-medium transition-all duration-200">
              Start Free Trial
            </router-link>
            <router-link to="/contact" class="btn border-2 border-indigo-600 text-indigo-600 hover:bg-indigo-600 hover:text-white dark:border-indigo-400 dark:text-indigo-400 dark:hover:bg-indigo-400 dark:hover:text-gray-900 px-8 py-4 text-lg rounded-lg font-medium transition-all duration-200">
              Schedule Demo
            </router-link>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup{% if cookiecutter.use_typescript == 'y' %} lang="ts"{% endif %}>
import { ref } from 'vue'

{% if cookiecutter.use_typescript == 'y' -%}
interface Feature {
  id: string
  title: string
  description: string
  color: string
  iconPath: string
  items: string[]
}

interface TechStack {
  name: string
  logo: string
  description: string
}

interface Comparison {
  feature: string
  ours: string
  others: string
  othersHas: boolean
}
{%- endif %}

const coreFeatures = ref({% if cookiecutter.use_typescript == 'y' %}<Feature[]>{% endif %}[
  {
    id: 'authentication',
    title: 'Authentication & Security',
    description: 'Enterprise-grade security with modern authentication',
    color: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    iconPath: 'M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z',
    items: [
      'JWT-based authentication',
      'Email verification',
      'Password recovery',
      'Two-factor authentication ready'
    ]
  },
  {
    id: 'realtime',
    title: 'Real-time Updates',
    description: 'Stay synchronized with WebSocket connections',
    color: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
    iconPath: 'M13 10V3L4 14h7v7l9-11h-7z',
    items: [
      'WebSocket support',
      'Real-time notifications',
      'Live data updates',
      'Collaborative features'
    ]
  },
  {
    id: 'scalability',
    title: 'Built to Scale',
    description: 'Architecture designed for growth',
    color: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
    iconPath: 'M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10',
    items: [
      'Docker containerization',
      'Horizontal scaling',
      'Load balancing ready',
      'Caching strategies'
    ]
  },
  {
    id: 'developer',
    title: 'Developer Experience',
    description: 'Tools and features developers love',
    color: 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
    iconPath: 'M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4',
    items: [
      'Hot module replacement',
      'TypeScript support',
      'Comprehensive API docs',
      'Testing utilities'
    ]
  },
  {
    id: 'analytics',
    title: 'Analytics & Monitoring',
    description: 'Insights into your application performance',
    color: 'linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)',
    iconPath: 'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z',
    items: [
      'Performance monitoring',
      'Error tracking',
      'User analytics',
      'Custom dashboards'
    ]
  },
  {
    id: 'deployment',
    title: 'Easy Deployment',
    description: 'Deploy anywhere with confidence',
    color: 'linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%)',
    iconPath: 'M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12',
    items: [
      'One-click deployment',
      'CI/CD pipelines',
      'Environment management',
      'Rollback capabilities'
    ]
  }
])

const techStack = ref({% if cookiecutter.use_typescript == 'y' %}<TechStack[]>{% endif %}[
  {
    name: 'Django',
    logo: 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect fill="%23092E20" width="100" height="100"/><text x="50" y="50" text-anchor="middle" dy=".3em" fill="white" font-size="40">DJ</text></svg>',
    description: 'High-level Python web framework'
  },
  {
    name: 'Vue.js',
    logo: 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect fill="%234FC08D" width="100" height="100"/><text x="50" y="50" text-anchor="middle" dy=".3em" fill="white" font-size="40">Vue</text></svg>',
    description: 'Progressive JavaScript framework'
  },
  {
    name: 'PostgreSQL',
    logo: 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect fill="%23336791" width="100" height="100"/><text x="50" y="50" text-anchor="middle" dy=".3em" fill="white" font-size="40">PG</text></svg>',
    description: 'Advanced open source database'
  },
  {
    name: 'Docker',
    logo: 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect fill="%232496ED" width="100" height="100"/><text x="50" y="50" text-anchor="middle" dy=".3em" fill="white" font-size="30">🐳</text></svg>',
    description: 'Container platform'
  },
  {
    name: 'Redis',
    logo: 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect fill="%23DC382D" width="100" height="100"/><text x="50" y="50" text-anchor="middle" dy=".3em" fill="white" font-size="30">Redis</text></svg>',
    description: 'In-memory data store'
  },
  {
    name: 'Celery',
    logo: 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect fill="%2337814A" width="100" height="100"/><text x="50" y="50" text-anchor="middle" dy=".3em" fill="white" font-size="30">CEL</text></svg>',
    description: 'Distributed task queue'
  }
])

const comparisons = ref({% if cookiecutter.use_typescript == 'y' %}<Comparison[]>{% endif %}[
  {
    feature: 'Setup Time',
    ours: 'Under 5 minutes',
    others: 'Hours to days',
    othersHas: true
  },
  {
    feature: 'Modern Stack',
    ours: 'Latest versions',
    others: 'Often outdated',
    othersHas: true
  },
  {
    feature: 'Docker Support',
    ours: 'Built-in',
    others: 'Manual setup',
    othersHas: true
  },
  {
    feature: 'Email Verification',
    ours: 'Pre-configured',
    others: 'Not included',
    othersHas: false
  },
  {
    feature: 'Admin Dashboard',
    ours: 'Full-featured',
    others: 'Basic or none',
    othersHas: true
  },
  {
    feature: 'API Documentation',
    ours: 'Auto-generated',
    others: 'Manual creation',
    othersHas: true
  },
  {
    feature: 'Testing Setup',
    ours: 'Pre-configured',
    others: 'Manual setup',
    othersHas: true
  },
  {
    feature: 'CI/CD Pipelines',
    ours: 'GitHub Actions ready',
    others: 'Not included',
    othersHas: false
  }
])
</script>

