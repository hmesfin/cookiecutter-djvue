<template>
  <div class="features-view">
    <!-- Hero Section -->
    <section class="bg-gradient-to-br from-emerald-500 to-teal-600 text-white py-20">
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
        <div class="mb-12">
          <h2 class="text-3xl font-bold text-gray-900 mb-4 dark:text-gray-100">Core Features</h2>
          <p class="text-lg text-gray-600 dark:text-gray-400">
            Built with the latest technologies and best practices
          </p>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          <div v-for="feature in coreFeatures" :key="feature.id" class="card hover-lift">
            <div class="card-body">
              <div class="w-16 h-16 rounded-full flex items-center justify-center text-white mb-6" :style="{ background: feature.color }">
                <component :is="feature.icon" class="w-8 h-8" />
              </div>
              <h3 class="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-3">{% raw %}{{ feature.title }}{% endraw %}</h3>
              <p class="text-gray-600 dark:text-gray-400 mb-4">{% raw %}{{ feature.description }}{% endraw %}</p>
              <ul class="space-y-2">
                <li v-for="item in feature.items" :key="item" class="flex items-start gap-2 text-gray-700 dark:text-gray-300">
                  <IconLucideCheck class="w-5 h-5 text-primary flex-shrink-0 mt-0.5" />
                  <span class="text-sm">{% raw %}{{ item }}{% endraw %}</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Technical Stack -->
    <section class="py-20 bg-gray-50 dark:bg-gray-800">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="mb-12">
          <h2 class="text-3xl font-bold text-gray-900 mb-4 dark:text-gray-100">Built with Modern Technology</h2>
          <p class="text-lg text-gray-600 dark:text-gray-400">
            Leveraging the best tools and frameworks for optimal performance
          </p>
        </div>
        
        <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-8">
          <div v-for="tech in techStack" :key="tech.name" class="text-center group">
            <div class="w-20 h-20 mx-auto mb-3 rounded-lg bg-white dark:bg-gray-700 shadow-md flex items-center justify-center group-hover:shadow-lg transition-shadow">
              <img :src="tech.logo" :alt="tech.name" class="w-12 h-12">
            </div>
            <h4 class="text-sm font-medium text-gray-900 dark:text-gray-100">{% raw %}{{ tech.name }}{% endraw %}</h4>
            <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">{% raw %}{{ tech.description }}{% endraw %}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Feature Comparison -->
    <section class="py-20 bg-white dark:bg-gray-900">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="mb-12">
          <h2 class="text-3xl font-bold text-gray-900 mb-4 dark:text-gray-100">Why Choose Us?</h2>
          <p class="text-lg text-gray-600 dark:text-gray-400">
            See how we compare to traditional solutions
          </p>
        </div>
        
        <div class="card overflow-hidden">
          <div class="overflow-x-auto">
            <table class="table">
              <thead class="table-header">
                <tr>
                  <th class="table-header-cell">Feature</th>
                  <th class="table-header-cell text-primary bg-emerald-50 dark:bg-emerald-900/20">Our Platform</th>
                  <th class="table-header-cell">Traditional Solutions</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-200 dark:divide-gray-700">
                <tr v-for="comparison in comparisons" :key="comparison.feature" class="hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors">
                  <td class="table-cell font-medium">{% raw %}{{ comparison.feature }}{% endraw %}</td>
                  <td class="table-cell bg-emerald-50/50 dark:bg-emerald-900/10">
                    <div class="flex items-center gap-2">
                      <IconLucideCheckCircle class="w-5 h-5 text-primary" />
                      <span>{% raw %}{{ comparison.ours }}{% endraw %}</span>
                    </div>
                  </td>
                  <td class="table-cell">
                    <div class="flex items-center gap-2">
                      <IconLucideAlertCircle v-if="comparison.othersHas" class="w-5 h-5 text-amber-500" />
                      <IconLucideXCircle v-else class="w-5 h-5 text-red-500" />
                      <span>{% raw %}{{ comparison.others }}{% endraw %}</span>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="py-20 bg-gradient-to-br from-emerald-500 to-teal-600 text-white text-center">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="max-w-3xl mx-auto">
          <h2 class="text-4xl font-bold mb-4">Ready to Get Started?</h2>
          <p class="text-xl mb-8 opacity-95">
            Join thousands of teams already using our platform to build amazing products
          </p>
          <div class="flex gap-4 justify-center flex-wrap">
            <router-link to="/auth/register" class="btn btn-lg bg-white text-emerald-600 hover:bg-gray-100">
              Start Free Trial
            </router-link>
            <router-link to="/contact" class="btn btn-lg btn-ghost border-2 border-white text-white hover:bg-white hover:text-emerald-600">
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
  icon: string
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
    color: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
    icon: 'IconLucideLock',
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
    color: 'linear-gradient(135deg, #f59e0b 0%, #f97316 100%)',
    icon: 'IconLucideZap',
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
    color: 'linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)',
    icon: 'IconLucideServer',
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
    color: 'linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%)',
    icon: 'IconLucideCode2',
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
    color: 'linear-gradient(135deg, #ec4899 0%, #db2777 100%)',
    icon: 'IconLucideBarChart3',
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
    color: 'linear-gradient(135deg, #06b6d4 0%, #0891b2 100%)',
    icon: 'IconLucideCloud',
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
    logo: 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect fill="%23092E20" width="100" height="100" rx="10"/><text x="50" y="55" text-anchor="middle" fill="white" font-size="40" font-weight="bold">DJ</text></svg>',
    description: 'Python framework'
  },
  {
    name: 'Vue.js',
    logo: 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect fill="%234FC08D" width="100" height="100" rx="10"/><text x="50" y="55" text-anchor="middle" fill="white" font-size="35" font-weight="bold">Vue</text></svg>',
    description: 'JavaScript framework'
  },
  {
    name: 'PostgreSQL',
    logo: 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect fill="%23336791" width="100" height="100" rx="10"/><text x="50" y="55" text-anchor="middle" fill="white" font-size="35" font-weight="bold">PG</text></svg>',
    description: 'Database'
  },
  {
    name: 'Docker',
    logo: 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect fill="%232496ED" width="100" height="100" rx="10"/><text x="50" y="55" text-anchor="middle" fill="white" font-size="35">🐳</text></svg>',
    description: 'Containers'
  },
  {
    name: 'Redis',
    logo: 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect fill="%23DC382D" width="100" height="100" rx="10"/><text x="50" y="55" text-anchor="middle" fill="white" font-size="25" font-weight="bold">Redis</text></svg>',
    description: 'Cache'
  },
  {
    name: 'Celery',
    logo: 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect fill="%2337814A" width="100" height="100" rx="10"/><text x="50" y="55" text-anchor="middle" fill="white" font-size="28" font-weight="bold">CEL</text></svg>',
    description: 'Task queue'
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