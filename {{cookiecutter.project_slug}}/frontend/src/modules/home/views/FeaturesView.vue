<template>
  <div class="features-view">
    <!-- Hero Section -->
    <section class="hero-section">
      <div class="container">
        <div class="hero-content">
          <h1 class="hero-title">Powerful Features for Modern Teams</h1>
          <p class="hero-description">
            Everything you need to build, deploy, and scale your applications with confidence.
            Our comprehensive feature set empowers teams to work smarter, not harder.
          </p>
        </div>
      </div>
    </section>

    <!-- Main Features Grid -->
    <section class="features-section">
      <div class="container">
        <div class="section-header">
          <h2 class="section-title">Core Features</h2>
          <p class="section-description">
            Built with the latest technologies and best practices
          </p>
        </div>
        
        <div class="features-grid">
          <div v-for="feature in coreFeatures" :key="feature.id" class="feature-card">
            <div class="feature-icon" :style="{ background: feature.color }">
              <svg class="icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path :d="feature.iconPath" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path>
              </svg>
            </div>
            <h3 class="feature-title">{% raw %}{{ feature.title }}{% endraw %}</h3>
            <p class="feature-description">{% raw %}{{ feature.description }}{% endraw %}</p>
            <ul class="feature-list">
              <li v-for="item in feature.items" :key="item">
                <svg class="check-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                </svg>
                {% raw %}{{ item }}{% endraw %}
              </li>
            </ul>
          </div>
        </div>
      </div>
    </section>

    <!-- Technical Stack -->
    <section class="tech-stack-section">
      <div class="container">
        <div class="section-header">
          <h2 class="section-title">Built with Modern Technology</h2>
          <p class="section-description">
            Leveraging the best tools and frameworks for optimal performance
          </p>
        </div>
        
        <div class="tech-grid">
          <div v-for="tech in techStack" :key="tech.name" class="tech-item">
            <div class="tech-logo">
              <img :src="tech.logo" :alt="tech.name">
            </div>
            <h4 class="tech-name">{% raw %}{{ tech.name }}{% endraw %}</h4>
            <p class="tech-description">{% raw %}{{ tech.description }}{% endraw %}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Feature Comparison -->
    <section class="comparison-section">
      <div class="container">
        <div class="section-header">
          <h2 class="section-title">Why Choose Us?</h2>
          <p class="section-description">
            See how we compare to traditional solutions
          </p>
        </div>
        
        <div class="comparison-table">
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
                  <svg class="icon-check" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                  {% raw %}{{ comparison.ours }}{% endraw %}
                </td>
                <td class="other-solution">
                  <svg v-if="comparison.othersHas" class="icon-partial" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                  <svg v-else class="icon-no" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                  {% raw %}{{ comparison.others }}{% endraw %}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="cta-section">
      <div class="container">
        <div class="cta-content">
          <h2 class="cta-title">Ready to Get Started?</h2>
          <p class="cta-description">
            Join thousands of teams already using our platform to build amazing products
          </p>
          <div class="cta-buttons">
            <router-link to="/auth/register" class="btn btn-primary btn-lg">
              Start Free Trial
            </router-link>
            <router-link to="/contact" class="btn btn-outline btn-lg">
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

<style scoped>
.features-view {
  min-height: 100vh;
}

/* Hero Section */
.hero-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 5rem 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1.5rem;
}

.hero-content {
  text-align: center;
  max-width: 800px;
  margin: 0 auto;
}

.hero-title {
  font-size: 3rem;
  font-weight: 700;
  margin: 0 0 1.5rem 0;
  line-height: 1.2;
}

.hero-description {
  font-size: 1.25rem;
  opacity: 0.95;
  line-height: 1.6;
}

/* Features Section */
.features-section {
  padding: 5rem 0;
  background: #f7fafc;
}

.section-header {
  text-align: center;
  margin-bottom: 3rem;
}

.section-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #1a202c;
  margin: 0 0 1rem 0;
}

.section-description {
  font-size: 1.125rem;
  color: #718096;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 2rem;
}

.feature-card {
  background: white;
  padding: 2rem;
  border-radius: 1rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
  transition: transform 0.3s, box-shadow 0.3s;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
}

.feature-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1.5rem;
}

.feature-icon .icon {
  width: 30px;
  height: 30px;
  color: white;
}

.feature-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1a202c;
  margin: 0 0 0.75rem 0;
}

.feature-description {
  color: #718096;
  margin-bottom: 1.5rem;
  line-height: 1.6;
}

.feature-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.feature-list li {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.75rem;
  color: #4a5568;
}

.check-icon {
  width: 20px;
  height: 20px;
  color: #48bb78;
  flex-shrink: 0;
}

/* Tech Stack Section */
.tech-stack-section {
  padding: 5rem 0;
  background: white;
}

.tech-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 3rem;
  margin-top: 3rem;
}

.tech-item {
  text-align: center;
}

.tech-logo {
  width: 80px;
  height: 80px;
  margin: 0 auto 1rem;
}

.tech-logo img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.tech-name {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1a202c;
  margin: 0 0 0.5rem 0;
}

.tech-description {
  font-size: 0.875rem;
  color: #718096;
}

/* Comparison Section */
.comparison-section {
  padding: 5rem 0;
  background: #f7fafc;
}

.comparison-table {
  background: white;
  border-radius: 1rem;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
}

.comparison-table table {
  width: 100%;
  border-collapse: collapse;
}

.comparison-table th {
  background: #4a5568;
  color: white;
  padding: 1.25rem;
  text-align: left;
  font-weight: 600;
}

.comparison-table th.highlight {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.comparison-table td {
  padding: 1.25rem;
  border-bottom: 1px solid #e2e8f0;
}

.comparison-table tr:last-child td {
  border-bottom: none;
}

.feature-name {
  font-weight: 500;
  color: #2d3748;
}

.our-solution {
  color: #059669;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.other-solution {
  color: #718096;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.icon-check {
  width: 20px;
  height: 20px;
  color: #059669;
}

.icon-partial {
  width: 20px;
  height: 20px;
  color: #d97706;
}

.icon-no {
  width: 20px;
  height: 20px;
  color: #dc2626;
}

/* CTA Section */
.cta-section {
  padding: 5rem 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.cta-content {
  text-align: center;
  max-width: 600px;
  margin: 0 auto;
}

.cta-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin: 0 0 1rem 0;
}

.cta-description {
  font-size: 1.125rem;
  margin-bottom: 2rem;
  opacity: 0.95;
}

.cta-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.btn {
  padding: 0.75rem 2rem;
  border-radius: 0.5rem;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s;
  display: inline-block;
  border: 2px solid transparent;
}

.btn-lg {
  padding: 1rem 2.5rem;
  font-size: 1.125rem;
}

.btn-primary {
  background: white;
  color: #667eea;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
}

.btn-outline {
  background: transparent;
  color: white;
  border-color: white;
}

.btn-outline:hover {
  background: white;
  color: #667eea;
}

/* Responsive */
@media (max-width: 768px) {
  .hero-title {
    font-size: 2rem;
  }
  
  .section-title {
    font-size: 1.75rem;
  }
  
  .features-grid {
    grid-template-columns: 1fr;
  }
  
  .tech-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .comparison-table {
    overflow-x: auto;
  }
  
  .comparison-table table {
    min-width: 500px;
  }
}
</style>