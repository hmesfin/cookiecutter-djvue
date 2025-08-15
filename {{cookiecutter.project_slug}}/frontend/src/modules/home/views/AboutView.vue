<template>
  <div class="about-view">
    <!-- Hero Section -->
    <section class="bg-gradient-to-br from-indigo-500 to-purple-600 text-white py-20">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center max-w-4xl mx-auto">
          <h1 class="text-5xl font-bold mb-4">About {{ cookiecutter.project_name }}</h1>
          <p class="text-xl opacity-95">
            Building the future of web applications with modern technology and passionate people
          </p>
        </div>
      </div>
    </section>

    <!-- Mission Section -->
    <section class="py-20 bg-white dark:bg-gray-900">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
          <div class="space-y-6">
            <h2 class="text-xl font-semibold text-gray-900 mb-2 dark:text-gray-100">Our Mission</h2>
            <p class="text-gray-600 dark:text-gray-400 leading-relaxed">
              We believe in empowering developers and businesses with tools that make 
              building web applications faster, easier, and more enjoyable. Our mission 
              is to provide a robust, scalable foundation that lets you focus on what 
              makes your application unique.
            </p>
            <p class="text-gray-600 dark:text-gray-400 leading-relaxed">
              By combining the power of Django and Vue.js with modern development practices, 
              we're creating a platform that grows with your needs—from startup to enterprise.
            </p>
          </div>
          <div class="flex justify-center">
            <div class="w-64 h-64 bg-gray-100 dark:bg-gray-800 rounded-lg flex items-center justify-center">
              <IconLucideLightbulb class="w-6 h-6" />
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Values Section -->
    <section class="py-20 bg-gray-50 dark:bg-gray-800 dark:bg-gray-900">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="mb-6">
          <h2 class="text-xl font-semibold text-gray-900 mb-2 dark:text-gray-100">Our Values</h2>
          <p class="text-gray-600 dark:text-gray-400">
            The principles that guide everything we do
          </p>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          <div v-for="value in values" :key="value.title" class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 dark:bg-gray-900 dark:shadow-xl dark:shadow-gray-900/40">
            <div class="w-16 h-16 rounded-full flex items-center justify-center text-white mb-4" :style="{ background: value.color }">
              <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path :d="value.iconPath" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path>
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-2">{% raw %}{{ value.title }}{% endraw %}</h3>
            <p class="text-gray-600 dark:text-gray-400">{% raw %}{{ value.description }}{% endraw %}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Team Section -->
    <section class="py-20 bg-white dark:bg-gray-900">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="mb-6">
          <h2 class="text-xl font-semibold text-gray-900 mb-2 dark:text-gray-100">Meet Our Team</h2>
          <p class="text-gray-600 dark:text-gray-400">
            Passionate professionals dedicated to your success
          </p>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          <div v-for="member in teamMembers" :key="member.name" class="team-bg-white rounded-lg shadow-md p-6 dark:shadow-xl dark:shadow-gray-900/40">
            <div class="w-32 h-32 rounded-full mx-auto mb-4 bg-gray-200 dark:bg-gray-700">
              <img v-if="member.avatar" :src="member.avatar" :alt="member.name">
              <div v-else class="w-24 h-24 rounded-full bg-emerald-600 text-white flex items-center justify-center text-2xl font-bold">
                {% raw %}{{ getInitials(member.name) }}{% endraw %}
              </div>
            </div>
            <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100">{% raw %}{{ member.name }}{% endraw %}</h3>
            <p class="text-sm text-gray-600 dark:text-gray-400 mb-3">{% raw %}{{ member.role }}{% endraw %}</p>
            <p class="member-bio">{% raw %}{{ member.bio }}{% endraw %}</p>
            <div class="flex justify-center gap-3">
              <a v-for="social in member.socials" :key="social.platform" :href="social.url" class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors dark:text-gray-600 dark:hover:text-gray-400">
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path :d="social.iconPath"></path>
                </svg>
              </a>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Stats Section -->
    <section class="stats-section">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div v-for="stat in stats" :key="stat.label" class="stat-bg-white rounded-lg shadow-md p-6 dark:shadow-xl dark:shadow-gray-900/40">
            <div class="text-3xl font-bold text-gray-900 dark:text-gray-100">{% raw %}{{ stat.value }}{% endraw %}</div>
            <div class="text-sm font-medium text-gray-600 dark:text-gray-400">{% raw %}{{ stat.label }}{% endraw %}</div>
          </div>
        </div>
      </div>
    </section>

    <!-- Timeline Section -->
    <section class="timeline-section">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="mb-6">
          <h2 class="text-xl font-semibold text-gray-900 mb-2 dark:text-gray-100">Our Journey</h2>
        </div>
        
        <div class="timeline">
          <div v-for="(milestone, index) in milestones" :key="index" class="timeline-item">
            <div class="timeline-marker"></div>
            <div class="timeline-content">
              <div class="timeline-date">{% raw %}{{ milestone.date }}{% endraw %}</div>
              <h3 class="timeline-title">{% raw %}{{ milestone.title }}{% endraw %}</h3>
              <p class="timeline-description">{% raw %}{{ milestone.description }}{% endraw %}</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="py-20 bg-gradient-to-br from-indigo-500 to-purple-600 text-white text-center">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="max-w-3xl mx-auto">
          <h2 class="text-4xl font-bold mb-4">Ready to Build Something Amazing?</h2>
          <p class="text-xl mb-8 opacity-95">
            Join our community and start building your next project today
          </p>
          <div class="flex gap-4 justify-center">
            <router-link to="/auth/register" class="btn bg-emerald-600 text-white hover:bg-emerald-700 px-8 py-4 text-lg rounded-lg font-medium transition-all duration-200">
              Get Started Free
            </router-link>
            <router-link to="/contact" class="btn border-2 border-emerald-600 text-emerald-600 hover:bg-emerald-600 hover:text-white dark:border-emerald-400 dark:text-emerald-400 dark:hover:bg-indigo-400 dark:hover:text-gray-900 px-8 py-4 text-lg rounded-lg font-medium transition-all duration-200">
              Get in Touch
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
interface Value {
  title: string
  description: string
  color: string
  iconPath: string
}

interface TeamMember {
  name: string
  role: string
  bio: string
  avatar?: string
  socials: Social[]
}

interface Social {
  platform: string
  url: string
  iconPath: string
}

interface Stat {
  value: string
  label: string
}

interface Milestone {
  date: string
  title: string
  description: string
}
{%- endif %}

const values = ref({% if cookiecutter.use_typescript == 'y' %}<Value[]>{% endif %}[
  {
    title: 'Innovation',
    description: 'Constantly pushing boundaries and embracing new technologies to deliver cutting-edge solutions.',
    color: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    iconPath: 'M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z'
  },
  {
    title: 'Quality',
    description: 'Committed to excellence in every line of code, ensuring reliability, performance, and security.',
    color: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
    iconPath: 'M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z'
  },
  {
    title: 'Community',
    description: 'Building together with developers worldwide, sharing knowledge and supporting each other.',
    color: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
    iconPath: 'M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z'
  },
  {
    title: 'Transparency',
    description: 'Open communication, clear documentation, and honest relationships with our users.',
    color: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
    iconPath: 'M15 12a3 3 0 11-6 0 3 3 0 016 0z M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z'
  }
])

const teamMembers = ref({% if cookiecutter.use_typescript == 'y' %}<TeamMember[]>{% endif %}[
  {
    name: 'Alex Johnson',
    role: 'Founder & CEO',
    bio: 'Passionate about building tools that empower developers. 10+ years in web development.',
    avatar: '',
    socials: [
      {
        platform: 'twitter',
        url: 'https://twitter.com',
        iconPath: 'M23 3a10.9 10.9 0 01-3.14 1.53 4.48 4.48 0 00-7.86 3v1A10.66 10.66 0 013 4s-4 9 5 13a11.64 11.64 0 01-7 2c9 5 20 0 20-11.5a4.5 4.5 0 00-.08-.83A7.72 7.72 0 0023 3z'
      },
      {
        platform: 'linkedin',
        url: 'https://linkedin.com',
        iconPath: 'M16 8a6 6 0 016 6v7h-4v-7a2 2 0 00-2-2 2 2 0 00-2 2v7h-4v-7a6 6 0 016-6zM2 9h4v12H2z M4 6a2 2 0 100-4 2 2 0 000 4z'
      }
    ]
  },
  {
    name: 'Sarah Chen',
    role: 'CTO',
    bio: 'Full-stack architect with a love for scalable systems and clean code.',
    avatar: '',
    socials: [
      {
        platform: 'github',
        url: 'https://github.com',
        iconPath: 'M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z'
      }
    ]
  },
  {
    name: 'Mike Torres',
    role: 'Head of Design',
    bio: 'Creating beautiful, intuitive interfaces that users love.',
    avatar: '',
    socials: [
      {
        platform: 'dribbble',
        url: 'https://dribbble.com',
        iconPath: 'M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10c5.51 0 10-4.48 10-10S17.51 2 12 2zm6.605 4.61a8.502 8.502 0 011.93 5.314c-.281-.054-3.101-.629-5.943-.271-.065-.141-.12-.293-.184-.445a25.416 25.416 0 00-.564-1.236c3.145-1.28 4.577-3.124 4.761-3.362zM12 3.475c2.17 0 4.154.813 5.662 2.148-.152.216-1.443 1.941-4.48 3.08-1.399-2.57-2.95-4.675-3.189-5A8.687 8.687 0 0112 3.475zm-3.633.803a53.896 53.896 0 013.167 4.935c-3.992 1.063-7.517 1.04-7.896 1.04a8.581 8.581 0 014.729-5.975zM3.453 12.01v-.26c.37.01 4.512.065 8.775-1.215.25.477.477.965.694 1.453-.109.033-.228.065-.336.098-4.404 1.42-6.747 5.303-6.942 5.629a8.522 8.522 0 01-2.19-5.705zM12 20.547a8.482 8.482 0 01-5.239-1.8c.152-.315 1.888-3.656 6.703-5.337.022-.01.033-.01.054-.022a35.318 35.318 0 011.823 6.475 8.4 8.4 0 01-3.341.684zm4.761-1.465c-.086-.52-.542-3.015-1.659-6.084 2.679-.423 5.022.271 5.314.369a8.468 8.468 0 01-3.655 5.715z'
      }
    ]
  },
  {
    name: 'Emily Davis',
    role: 'Developer Advocate',
    bio: 'Helping developers succeed with great documentation and community support.',
    avatar: '',
    socials: [
      {
        platform: 'twitter',
        url: 'https://twitter.com',
        iconPath: 'M23 3a10.9 10.9 0 01-3.14 1.53 4.48 4.48 0 00-7.86 3v1A10.66 10.66 0 013 4s-4 9 5 13a11.64 11.64 0 01-7 2c9 5 20 0 20-11.5a4.5 4.5 0 00-.08-.83A7.72 7.72 0 0023 3z'
      }
    ]
  }
])

const stats = ref({% if cookiecutter.use_typescript == 'y' %}<Stat[]>{% endif %}[
  {
    value: '10K+',
    label: 'Active Users'
  },
  {
    value: '50K+',
    label: 'Projects Created'
  },
  {
    value: '99.9%',
    label: 'Uptime'
  },
  {
    value: '24/7',
    label: 'Support'
  }
])

const milestones = ref({% if cookiecutter.use_typescript == 'y' %}<Milestone[]>{% endif %}[
  {
    date: '2020',
    title: 'The Beginning',
    description: 'Started as a side project to solve our own development challenges.'
  },
  {
    date: '2021',
    title: 'Open Source Release',
    description: 'Released the first version to the open-source community.'
  },
  {
    date: '2022',
    title: 'Community Growth',
    description: 'Reached 1,000 active users and established a thriving community.'
  },
  {
    date: '2023',
    title: 'Enterprise Ready',
    description: 'Launched enterprise features and secured major corporate clients.'
  },
  {
    date: '2024',
    title: 'Global Expansion',
    description: 'Expanded to serve developers in over 50 countries worldwide.'
  }
])

const getInitials = (name{% if cookiecutter.use_typescript == 'y' %}: string{% endif %}) => {
  return name.split(' ').map(n => n[0]).join('').toUpperCase()
}
</script>

