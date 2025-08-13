<template>
  <div class="about-view">
    <!-- Hero Section -->
    <section class="hero-section">
      <div class="container">
        <div class="hero-content">
          <h1 class="hero-title">About {{ cookiecutter.project_name }}</h1>
          <p class="hero-description">
            Building the future of web applications with modern technology and passionate people
          </p>
        </div>
      </div>
    </section>

    <!-- Mission Section -->
    <section class="mission-section">
      <div class="container">
        <div class="mission-grid">
          <div class="mission-content">
            <h2 class="section-title">Our Mission</h2>
            <p class="mission-text">
              We believe in empowering developers and businesses with tools that make 
              building web applications faster, easier, and more enjoyable. Our mission 
              is to provide a robust, scalable foundation that lets you focus on what 
              makes your application unique.
            </p>
            <p class="mission-text">
              By combining the power of Django and Vue.js with modern development practices, 
              we're creating a platform that grows with your needs—from startup to enterprise.
            </p>
          </div>
          <div class="mission-image">
            <div class="image-placeholder">
              <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
              </svg>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Values Section -->
    <section class="values-section">
      <div class="container">
        <div class="section-header">
          <h2 class="section-title">Our Values</h2>
          <p class="section-description">
            The principles that guide everything we do
          </p>
        </div>
        
        <div class="values-grid">
          <div v-for="value in values" :key="value.title" class="value-card">
            <div class="value-icon" :style="{ background: value.color }">
              <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path :d="value.iconPath" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path>
              </svg>
            </div>
            <h3 class="value-title">{% raw %}{{ value.title }}{% endraw %}</h3>
            <p class="value-description">{% raw %}{{ value.description }}{% endraw %}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Team Section -->
    <section class="team-section">
      <div class="container">
        <div class="section-header">
          <h2 class="section-title">Meet Our Team</h2>
          <p class="section-description">
            Passionate professionals dedicated to your success
          </p>
        </div>
        
        <div class="team-grid">
          <div v-for="member in teamMembers" :key="member.name" class="team-card">
            <div class="member-avatar">
              <img v-if="member.avatar" :src="member.avatar" :alt="member.name">
              <div v-else class="avatar-placeholder">
                {% raw %}{{ getInitials(member.name) }}{% endraw %}
              </div>
            </div>
            <h3 class="member-name">{% raw %}{{ member.name }}{% endraw %}</h3>
            <p class="member-role">{% raw %}{{ member.role }}{% endraw %}</p>
            <p class="member-bio">{% raw %}{{ member.bio }}{% endraw %}</p>
            <div class="member-social">
              <a v-for="social in member.socials" :key="social.platform" :href="social.url" class="social-link">
                <svg class="social-icon" fill="currentColor" viewBox="0 0 24 24">
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
      <div class="container">
        <div class="stats-grid">
          <div v-for="stat in stats" :key="stat.label" class="stat-card">
            <div class="stat-value">{% raw %}{{ stat.value }}{% endraw %}</div>
            <div class="stat-label">{% raw %}{{ stat.label }}{% endraw %}</div>
          </div>
        </div>
      </div>
    </section>

    <!-- Timeline Section -->
    <section class="timeline-section">
      <div class="container">
        <div class="section-header">
          <h2 class="section-title">Our Journey</h2>
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
    <section class="cta-section">
      <div class="container">
        <div class="cta-content">
          <h2 class="cta-title">Ready to Build Something Amazing?</h2>
          <p class="cta-description">
            Join our community and start building your next project today
          </p>
          <div class="cta-buttons">
            <router-link to="/auth/register" class="btn btn-primary btn-lg">
              Get Started Free
            </router-link>
            <router-link to="/contact" class="btn btn-outline btn-lg">
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

<style scoped>
.about-view {
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
  margin: 0 0 1rem 0;
  line-height: 1.2;
}

.hero-description {
  font-size: 1.25rem;
  opacity: 0.95;
}

/* Mission Section */
.mission-section {
  padding: 5rem 0;
  background: white;
}

.mission-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  align-items: center;
}

.section-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #1a202c;
  margin: 0 0 1.5rem 0;
}

.mission-text {
  color: #4a5568;
  font-size: 1.125rem;
  line-height: 1.8;
  margin-bottom: 1.5rem;
}

.mission-image {
  display: flex;
  justify-content: center;
}

.image-placeholder {
  width: 300px;
  height: 300px;
  background: linear-gradient(135deg, #667eea20 0%, #764ba220 100%);
  border-radius: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.image-placeholder svg {
  width: 100px;
  height: 100px;
  color: #667eea;
}

/* Values Section */
.values-section {
  padding: 5rem 0;
  background: #f7fafc;
}

.section-header {
  text-align: center;
  margin-bottom: 3rem;
}

.section-description {
  font-size: 1.125rem;
  color: #718096;
}

.values-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
}

.value-card {
  text-align: center;
  padding: 2rem;
}

.value-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto 1.5rem;
  border-radius: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.value-icon svg {
  width: 40px;
  height: 40px;
  color: white;
}

.value-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1a202c;
  margin: 0 0 0.75rem 0;
}

.value-description {
  color: #718096;
  line-height: 1.6;
}

/* Team Section */
.team-section {
  padding: 5rem 0;
  background: white;
}

.team-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 3rem;
  margin-top: 3rem;
}

.team-card {
  text-align: center;
}

.member-avatar {
  width: 120px;
  height: 120px;
  margin: 0 auto 1.5rem;
}

.member-avatar img {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: cover;
}

.avatar-placeholder {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 2.5rem;
  font-weight: 600;
}

.member-name {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1a202c;
  margin: 0 0 0.25rem 0;
}

.member-role {
  color: #667eea;
  font-weight: 500;
  margin-bottom: 1rem;
}

.member-bio {
  color: #718096;
  line-height: 1.6;
  margin-bottom: 1.5rem;
}

.member-social {
  display: flex;
  justify-content: center;
  gap: 1rem;
}

.social-link {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: #f7fafc;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
}

.social-link:hover {
  background: #667eea;
  transform: translateY(-2px);
}

.social-icon {
  width: 18px;
  height: 18px;
  color: #718096;
}

.social-link:hover .social-icon {
  color: white;
}

/* Stats Section */
.stats-section {
  padding: 5rem 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 2rem;
}

.stat-card {
  text-align: center;
  color: white;
}

.stat-value {
  font-size: 3rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.stat-label {
  font-size: 1.125rem;
  opacity: 0.9;
}

/* Timeline Section */
.timeline-section {
  padding: 5rem 0;
  background: #f7fafc;
}

.timeline {
  position: relative;
  max-width: 800px;
  margin: 3rem auto 0;
  padding: 0 2rem;
}

.timeline:before {
  content: '';
  position: absolute;
  left: 50%;
  top: 0;
  bottom: 0;
  width: 2px;
  background: #e2e8f0;
  transform: translateX(-50%);
}

.timeline-item {
  position: relative;
  margin-bottom: 3rem;
}

.timeline-item:nth-child(even) .timeline-content {
  margin-left: auto;
  text-align: right;
}

.timeline-marker {
  position: absolute;
  left: 50%;
  top: 0;
  width: 16px;
  height: 16px;
  background: white;
  border: 3px solid #667eea;
  border-radius: 50%;
  transform: translateX(-50%);
  z-index: 1;
}

.timeline-content {
  width: calc(50% - 3rem);
  background: white;
  padding: 1.5rem;
  border-radius: 0.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.timeline-date {
  color: #667eea;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.timeline-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1a202c;
  margin: 0 0 0.5rem 0;
}

.timeline-description {
  color: #718096;
  line-height: 1.6;
}

/* CTA Section */
.cta-section {
  padding: 5rem 0;
  background: white;
}

.cta-content {
  text-align: center;
  max-width: 600px;
  margin: 0 auto;
}

.cta-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #1a202c;
  margin: 0 0 1rem 0;
}

.cta-description {
  font-size: 1.125rem;
  color: #718096;
  margin-bottom: 2rem;
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
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
}

.btn-outline {
  background: white;
  color: #667eea;
  border-color: #667eea;
}

.btn-outline:hover {
  background: #667eea;
  color: white;
}

/* Responsive */
@media (max-width: 1024px) {
  .mission-grid {
    grid-template-columns: 1fr;
    text-align: center;
  }
  
  .timeline:before {
    left: 2rem;
  }
  
  .timeline-marker {
    left: 2rem;
  }
  
  .timeline-content {
    width: calc(100% - 4rem);
    margin-left: 4rem !important;
    text-align: left !important;
  }
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 2rem;
  }
  
  .section-title {
    font-size: 1.75rem;
  }
  
  .stat-value {
    font-size: 2rem;
  }
  
  .team-grid {
    grid-template-columns: 1fr;
  }
  
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>