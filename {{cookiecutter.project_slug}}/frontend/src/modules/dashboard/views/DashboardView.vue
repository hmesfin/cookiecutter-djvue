<template>
  <div class="dashboard">
    {% if cookiecutter.css_framework == 'tailwindcss' -%}
    <div class="space-y-6">
      <!-- Welcome Section -->
      <div class="bg-white overflow-hidden shadow rounded-lg dark:bg-gray-900 dark:shadow-xl dark:shadow-gray-900/30">
        <div class="px-4 py-5 sm:p-6">
          <h1 class="text-2xl font-bold text-gray-900 dark:text-gray-100">Welcome back, {% raw %}{{ userName }}{% endraw %}!</h1>
          <p class="mt-1 text-sm text-gray-600 dark:text-gray-400">
            Here's what's happening with your account today.
          </p>
        </div>
      </div>

      <!-- Stats Grid -->
      <div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        {% raw %}<div
          v-for="stat in stats"
          :key="stat.name"
          class="bg-white overflow-hidden shadow rounded-lg dark:bg-gray-900 dark:shadow-xl dark:shadow-gray-900/30"
        >
          <div class="px-4 py-5 sm:p-6">
            <dt class="text-sm font-medium text-gray-500 truncate dark:text-gray-500">
              {{ stat.name }}
            </dt>
            <dd class="mt-1 text-3xl font-semibold text-gray-900 dark:text-gray-100">
              {{ stat.value }}
            </dd>
            <dd class="mt-2 flex items-center text-sm">
              <span
                class="font-medium"
                :class="stat.changeType === 'increase' ? 'text-green-600' : 'text-red-600'"
              >
                {{ stat.change }}
              </span>
              <span class="ml-2 text-gray-500 dark:text-gray-500">from last month</span>
            </dd>
          </div>
        </div>{% endraw %}
      </div>

      <!-- Recent Activity -->
      <div class="bg-white shadow rounded-lg dark:bg-gray-900 dark:shadow-xl dark:shadow-gray-900/30">
        <div class="px-4 py-5 sm:px-6 border-b border-gray-200 dark:border-gray-700">
          <h3 class="text-lg font-medium text-gray-900 dark:text-gray-100">Recent Activity</h3>
        </div>
        <div class="px-4 py-5 sm:p-6">
          <div class="flow-root">
            <ul class="-mb-8">
              {% raw %}<li v-for="(activity, idx) in activities" :key="activity.id">
                <div class="relative pb-8">
                  <span
                    v-if="idx !== activities.length - 1"
                    class="absolute top-4 left-4 -ml-px h-full w-0.5 bg-gray-200 dark:bg-gray-700"
                  />
                  <div class="relative flex space-x-3">
                    <div>
                      <span
                        class="h-8 w-8 rounded-full flex items-center justify-center ring-8 ring-white"
                        :class="activity.bgColor"
                      >
                        <component :is="activity.icon" class="h-5 w-5 text-white" />
                      </span>
                    </div>
                    <div class="flex min-w-0 flex-1 justify-between space-x-4 pt-1.5">
                      <div>
                        <p class="text-sm text-gray-500 dark:text-gray-500">
                          {{ activity.content }}
                        </p>
                      </div>
                      <div class="whitespace-nowrap text-right text-sm text-gray-500 dark:text-gray-500">
                        <time :datetime="activity.datetime">{{ activity.date }}</time>
                      </div>
                    </div>
                  </div>
                </div>
              </li>{% endraw %}
            </ul>
          </div>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="bg-white shadow rounded-lg dark:bg-gray-900 dark:shadow-xl dark:shadow-gray-900/30">
        <div class="px-4 py-5 sm:px-6 border-b border-gray-200 dark:border-gray-700">
          <h3 class="text-lg font-medium text-gray-900 dark:text-gray-100">Quick Actions</h3>
        </div>
        <div class="px-4 py-5 sm:p-6">
          <div class="grid grid-cols-1 gap-4 sm:grid-cols-3">
            {% raw %}<button
              v-for="action in quickActions"
              :key="action.name"
              @click="action.onClick"
              class="relative rounded-lg border border-gray-300 bg-white px-6 py-4 shadow-sm hover:border-gray-400 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:ring-offset-2 dark:border-gray-600 dark:bg-gray-900 dark:shadow-lg dark:shadow-gray-900/30 dark:hover:border-gray-500 dark:focus:ring-emerald-400"
            >
              <div>
                <span class="block text-sm font-medium text-gray-900 dark:text-gray-100">
                  {{ action.name }}
                </span>
                <span class="mt-1 block text-sm text-gray-500 dark:text-gray-500">
                  {{ action.description }}
                </span>
              </div>
            </button>{% endraw %}
          </div>
        </div>
      </div>
    </div>
    {% else -%}
    <div class="dashboard-content">
      <!-- Welcome Section -->
      <div class="welcome-bg-white rounded-lg shadow-md p-6 dark:shadow-xl dark:shadow-gray-900/40">
        <h1>Welcome back, {% raw %}{{ userName }}{% endraw %}!</h1>
        <p>Here's what's happening with your account today.</p>
      </div>

      <!-- Stats Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {% raw %}<div v-for="stat in stats" :key="stat.name" class="stat-bg-white rounded-lg shadow-md p-6 dark:shadow-xl dark:shadow-gray-900/40">
          <div class="stat-name">{{ stat.name }}</div>
          <div class="text-3xl font-bold text-gray-900 dark:text-gray-100">{{ stat.value }}</div>
          <div class="stat-change">
            <span :class="stat.changeType">
              {{ stat.change }}
            </span>
            <span>from last month</span>
          </div>
        </div>{% endraw %}
      </div>

      <!-- Recent Activity -->
      <div class="activity-bg-white rounded-lg shadow-md p-6 dark:shadow-xl dark:shadow-gray-900/40">
        <h3>Recent Activity</h3>
        <div class="activity-list">
          {% raw %}<div v-for="activity in activities" :key="activity.id" class="activity-item">
            <div class="activity-content">{{ activity.content }}</div>
            <div class="activity-date">{{ activity.date }}</div>
          </div>{% endraw %}
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="actions-bg-white rounded-lg shadow-md p-6 dark:shadow-xl dark:shadow-gray-900/40">
        <h3>Quick Actions</h3>
        <div class="actions-grid">
          {% raw %}<button
            v-for="action in quickActions"
            :key="action.name"
            @click="action.onClick"
            class="action-button"
          >
            <div class="action-name">{{ action.name }}</div>
            <div class="action-description">{{ action.description }}</div>
          </button>{% endraw %}
        </div>
      </div>
    </div>
    {%- endif %}
  </div>
</template>

<script setup{% if cookiecutter.use_typescript == 'y' %} lang="ts"{% endif %}>
import { computed, ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const userName = computed(() => {
  const user = authStore.user
  if (user?.first_name && user?.last_name) {
    return `${user.first_name} ${user.last_name}`
  }
  return user?.username || 'User'
})

const stats = ref([
  { name: 'Total Revenue', value: '$12,456', change: '+12.5%', changeType: 'increase' },
  { name: 'Active Users', value: '2,456', change: '+5.4%', changeType: 'increase' },
  { name: 'New Orders', value: '89', change: '-2.1%', changeType: 'decrease' },
  { name: 'Conversion Rate', value: '3.2%', change: '+0.5%', changeType: 'increase' },
])

const activities = ref([
  {
    id: 1,
    content: 'You updated your profile information',
    date: '2 hours ago',
    datetime: '2024-01-15T10:00:00',
    icon: 'UserIcon',
    bgColor: 'bg-gray-400',
  },
  {
    id: 2,
    content: 'New order #12345 was created',
    date: '5 hours ago',
    datetime: '2024-01-15T07:00:00',
    icon: 'ShoppingCartIcon',
    bgColor: 'bg-emerald-600',
  },
  {
    id: 3,
    content: 'Payment received for invoice #678',
    date: '1 day ago',
    datetime: '2024-01-14T15:00:00',
    icon: 'CreditCardIcon',
    bgColor: 'bg-green-500',
  },
])

const quickActions = ref([
  {
    name: 'Create New Order',
    description: 'Start a new order process',
    onClick: () => router.push('/dashboard/orders/new'),
  },
  {
    name: 'View Reports',
    description: 'Access analytics and reports',
    onClick: () => router.push('/dashboard/analytics'),
  },
  {
    name: 'Manage Users',
    description: 'Add or edit user accounts',
    onClick: () => router.push('/dashboard/users'),
  },
])
</script>

<style scoped>
{% if cookiecutter.css_framework == 'none' -%}
.dashboard-content {
  max-width: 1200px;
  margin: 0 auto;
}

.welcome-card {
  background: white;
  padding: 2rem;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.welcome-card h1 {
  margin: 0 0 0.5rem;
  font-size: 1.875rem;
}

.welcome-card p {
  color: #666;
  margin: 0;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  padding: 1.5rem;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.stat-name {
  font-size: 0.875rem;
  color: #666;
  margin-bottom: 0.5rem;
}

.stat-value {
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
}

.stat-change {
  font-size: 0.875rem;
  color: #666;
}

.stat-change .increase {
  color: #22c55e;
  font-weight: 500;
}

.stat-change .decrease {
  color: #ef4444;
  font-weight: 500;
}

.activity-card,
.actions-card {
  background: white;
  padding: 1.5rem;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.activity-card h3,
.actions-card h3 {
  margin: 0 0 1rem;
  font-size: 1.125rem;
}

.activity-list {
  space-y: 1rem;
}

.activity-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 0;
  border-bottom: 1px solid #e5e7eb;
}

.activity-item:last-child {
  border-bottom: none;
}

.activity-content {
  color: #666;
  font-size: 0.875rem;
}

.activity-date {
  color: #999;
  font-size: 0.75rem;
  white-space: nowrap;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.action-button {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
  padding: 1rem;
  text-align: left;
  cursor: pointer;
  transition: all 0.2s;
}

.action-button:hover {
  border-color: #9ca3af;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.action-name {
  font-weight: 500;
  margin-bottom: 0.25rem;
}

.action-description {
  font-size: 0.875rem;
  color: #666;
}
{%- endif %}
</style>