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
            <h2 class="text-3xl font-bold text-gray-900 mb-4 dark:text-gray-100">Our Mission</h2>
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
              <IconLucideLightbulb class="w-32 h-32 text-emerald-600 dark:text-emerald-400" />
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Values Section -->
    <section class="py-20 bg-gray-50 dark:bg-gray-800">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-12">
          <h2 class="text-3xl font-bold text-gray-900 mb-4 dark:text-gray-100">Our Values</h2>
          <p class="text-lg text-gray-600 dark:text-gray-400">
            The principles that guide everything we do
          </p>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          <div v-for="value in values" :key="value.title" class="card hover-lift">
            <div class="card-body">
              <div class="w-16 h-16 rounded-full flex items-center justify-center text-white mb-4" :style="{ background: value.color }">
                <component :is="value.icon" class="w-8 h-8" />
              </div>
              <h3 class="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-2">{% raw %}{{ value.title }}{% endraw %}</h3>
              <p class="text-gray-600 dark:text-gray-400">{% raw %}{{ value.description }}{% endraw %}</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Team Section -->
    <section class="py-20 bg-white dark:bg-gray-900">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-12">
          <h2 class="text-3xl font-bold text-gray-900 mb-4 dark:text-gray-100">Meet Our Team</h2>
          <p class="text-lg text-gray-600 dark:text-gray-400">
            Passionate professionals dedicated to your success
          </p>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          <div v-for="member in teamMembers" :key="member.name" class="card hover-lift text-center">
            <div class="card-body">
              <div class="w-32 h-32 rounded-full mx-auto mb-4 bg-gray-200 dark:bg-gray-700 flex items-center justify-center">
                <img v-if="member.avatar" :src="member.avatar" :alt="member.name" class="w-full h-full rounded-full object-cover">
                <div v-else class="w-32 h-32 rounded-full bg-emerald-600 text-white flex items-center justify-center text-2xl font-bold">
                  {% raw %}{{ getInitials(member.name) }}{% endraw %}
                </div>
              </div>
              <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100">{% raw %}{{ member.name }}{% endraw %}</h3>
              <p class="text-sm text-emerald-600 dark:text-emerald-400 mb-3">{% raw %}{{ member.role }}{% endraw %}</p>
              <p class="text-gray-600 dark:text-gray-400 text-sm mb-4">{% raw %}{{ member.bio }}{% endraw %}</p>
              <div class="flex justify-center gap-3">
                <a v-for="social in member.socials" :key="social.platform" :href="social.url" class="link-muted">
                  <component :is="social.icon" class="w-5 h-5" />
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Stats Section -->
    <section class="py-20 bg-gradient-to-br from-emerald-500 to-teal-600 text-white">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div v-for="stat in stats" :key="stat.label" class="text-center">
            <div class="text-5xl font-bold mb-2">{% raw %}{{ stat.value }}{% endraw %}</div>
            <div class="text-lg opacity-95">{% raw %}{{ stat.label }}{% endraw %}</div>
          </div>
        </div>
      </div>
    </section>

    <!-- Timeline Section -->
    <section class="py-20 bg-white dark:bg-gray-900">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-12">
          <h2 class="text-3xl font-bold text-gray-900 mb-4 dark:text-gray-100">Our Journey</h2>
          <p class="text-lg text-gray-600 dark:text-gray-400">Milestones that shaped who we are today</p>
        </div>
        
        <!-- Desktop Timeline -->
        <div class="hidden lg:block relative">
          <!-- Timeline line -->
          <div class="absolute left-1/2 transform -translate-x-1/2 w-0.5 h-full bg-gray-300 dark:bg-gray-700"></div>
          
          <div class="space-y-12">
            <div v-for="(milestone, index) in milestones" :key="index" :class="['flex items-center', index % 2 === 0 ? 'flex-row' : 'flex-row-reverse']">
              <!-- Content -->
              <div class="w-5/12">
                <div :class="['card hover-lift', index % 2 === 0 ? 'text-right' : 'text-left']">
                  <div class="card-body">
                    <div class="text-emerald-600 dark:text-emerald-400 font-bold mb-2">{% raw %}{{ milestone.date }}{% endraw %}</div>
                    <h3 class="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-2">{% raw %}{{ milestone.title }}{% endraw %}</h3>
                    <p class="text-gray-600 dark:text-gray-400">{% raw %}{{ milestone.description }}{% endraw %}</p>
                  </div>
                </div>
              </div>
              
              <!-- Marker -->
              <div class="w-2/12 flex justify-center">
                <div class="w-4 h-4 bg-emerald-600 dark:bg-emerald-400 rounded-full ring-4 ring-white dark:ring-gray-900 z-10"></div>
              </div>
              
              <!-- Spacer -->
              <div class="w-5/12"></div>
            </div>
          </div>
        </div>
        
        <!-- Mobile Timeline -->
        <div class="lg:hidden">
          <div class="relative">
            <!-- Timeline line (left side for mobile) -->
            <div class="absolute left-8 top-0 w-0.5 h-full bg-gray-300 dark:bg-gray-700"></div>
            
            <div class="space-y-8">
              <div v-for="(milestone, index) in milestones" :key="index" class="relative flex items-start">
                <!-- Marker -->
                <div class="absolute left-8 w-4 h-4 bg-emerald-600 dark:bg-emerald-400 rounded-full ring-4 ring-white dark:ring-gray-900 -translate-x-1/2"></div>
                
                <!-- Content -->
                <div class="ml-16 card hover-lift">
                  <div class="card-body">
                    <div class="text-emerald-600 dark:text-emerald-400 font-bold mb-2">{% raw %}{{ milestone.date }}{% endraw %}</div>
                    <h3 class="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-2">{% raw %}{{ milestone.title }}{% endraw %}</h3>
                    <p class="text-gray-600 dark:text-gray-400">{% raw %}{{ milestone.description }}{% endraw %}</p>
                  </div>
                </div>
              </div>
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
  icon: string
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
  icon: string
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
    icon: 'IconLucideLightbulb'
  },
  {
    title: 'Quality',
    description: 'Committed to excellence in every line of code, ensuring reliability, performance, and security.',
    color: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
    icon: 'IconLucideShield'
  },
  {
    title: 'Community',
    description: 'Building together with developers worldwide, sharing knowledge and supporting each other.',
    color: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
    icon: 'IconLucideUsers'
  },
  {
    title: 'Transparency',
    description: 'Open communication, clear documentation, and honest relationships with our users.',
    color: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
    icon: 'IconLucideEye'
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
        icon: 'IconLucideTwitter'
      },
      {
        platform: 'linkedin',
        url: 'https://linkedin.com',
        icon: 'IconLucideLinkedin'
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
        icon: 'IconLucideGithub'
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
        icon: 'IconLucidePalette'
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
        icon: 'IconLucideTwitter'
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

