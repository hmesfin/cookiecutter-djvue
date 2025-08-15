<template>
  <div class="p-8 max-w-7xl mx-auto">
        <PageHeader
      title="Analytics Dashboard" description="Track performance metrics and user engagement"
    />

    <!-- Key Metrics -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <div v-for="metric in keyMetrics" :key="metric.id" class="bg-white rounded-lg shadow-md p-6 dark:bg-gray-900 dark:shadow-xl dark:shadow-gray-900/40">
        <div class="flex items-center justify-between mb-2">
          <span class="text-sm font-medium text-gray-600 dark:text-gray-400">{% raw %}{{ metric.label }}{% endraw %}</span>
          <span :class="[
            'flex items-center gap-1 text-xs font-medium',
            metric.trend > 0 ? 'text-green-600' : 'text-red-600'
          ]">
            <IconLucideTrendingUp v-if="metric.trend > 0" class="w-4 h-4" />
            <IconLucideTrendingDown v-else class="w-4 h-4" />
            {% raw %}{{ Math.abs(metric.trend) }}%{% endraw %}
          </span>
        </div>
        <div class="text-3xl font-bold text-gray-900 dark:text-gray-100">{% raw %}{{ metric.value }}{% endraw %}</div>
        <div class="text-sm text-gray-500 dark:text-gray-400 dark:text-gray-500">{% raw %}{{ metric.comparison }}{% endraw %}</div>
      </div>
    </div>

    <!-- Charts -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
      <!-- Revenue Chart -->
      <div class="bg-white rounded-lg shadow-md p-6 dark:bg-gray-900 dark:shadow-xl dark:shadow-gray-900/40">
        <div class="mb-4">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100">Revenue Overview</h3>
          <div class="flex gap-4 mt-2">
            <span class="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400">
              <span class="w-3 h-3 rounded-full" style="background: #4299e1"></span>
              Revenue
            </span>
            <span class="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400">
              <span class="w-3 h-3 rounded-full" style="background: #48bb78"></span>
              Profit
            </span>
          </div>
        </div>
        <div class="relative h-64">
          <canvas ref="revenueChart"></canvas>
        </div>
      </div>

      <!-- Traffic Sources -->
      <div class="bg-white rounded-lg shadow-md p-6 dark:bg-gray-900 dark:shadow-xl dark:shadow-gray-900/40">
        <div class="mb-4">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100">Traffic Sources</h3>
        </div>
        <div class="relative h-64">
          <canvas ref="trafficChart"></canvas>
        </div>
        <div class="mt-4 space-y-2">
          <div v-for="source in trafficSources" :key="source.name" class="flex items-center justify-between">
            <div class="flex items-center gap-2">
              <span class="w-3 h-3 rounded-full" :style="{ background: source.color }"></span>
              <span class="text-sm text-gray-600 dark:text-gray-400">{% raw %}{{ source.name }}{% endraw %}</span>
            </div>
            <span class="text-sm font-medium text-gray-900 dark:text-gray-100">{% raw %}{{ source.value }}%{% endraw %}</span>
          </div>
        </div>
      </div>

      <!-- User Activity -->
      <div class="bg-white rounded-lg shadow-md p-6 md:col-span-2 dark:bg-gray-900 dark:shadow-xl dark:shadow-gray-900/40">
        <div class="mb-4">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100">User Activity</h3>
          <div class="flex gap-2 mt-2">
            <button 
              v-for="tab in activityTabs" 
              :key="tab"
              @click="activeActivityTab = tab"
              :class="[
                'px-3 py-1 text-sm font-medium rounded-md transition-colors',
                activeActivityTab === tab 
                  ? 'bg-emerald-100 text-emerald-700 dark:bg-indigo-900 dark:text-indigo-300'
                  : 'text-gray-600 hover:text-gray-900 dark:text-gray-400 dark:hover:text-gray-100'
              ]"
            >
              {% raw %}{{ tab }}{% endraw %}
            </button>
          </div>
        </div>
        <div class="relative h-64">
          <canvas ref="activityChart"></canvas>
        </div>
      </div>
    </div>

    <!-- Top Products Table -->
    <div class="bg-white rounded-lg shadow-md p-6 dark:bg-gray-900 dark:shadow-xl dark:shadow-gray-900/40">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100">Top Products</h3>
        <button class="text-sm font-medium text-emerald-600 hover:text-emerald-600 transition-colors dark:text-emerald-400 dark:hover:text-indigo-300">View All</button>
      </div>
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
          <thead>
            <tr>
              <th>Product</th>
              <th>Sales</th>
              <th>Revenue</th>
              <th>Growth</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="product in topProducts" :key="product.id">
              <td>
                <div class="product-info">
                  <img :src="product.image" :alt="product.name" class="product-image">
                  <span>{% raw %}{{ product.name }}{% endraw %}</span>
                </div>
              </td>
              <td>{% raw %}{{ product.sales }}{% endraw %}</td>
              <td>${% raw %}{{ product.revenue.toLocaleString() }}{% endraw %}</td>
              <td>
                <span :class="['growth-badge', product.growth > 0 ? 'positive' : 'negative']">
                  {% raw %}{{ product.growth > 0 ? '+' : '' }}{{ product.growth }}%{% endraw %}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup{% if cookiecutter.use_typescript == 'y' %} lang="ts"{% endif %}>
import { ref, onMounted, watch } from 'vue'
import Chart from 'chart.js/auto'

{% if cookiecutter.use_typescript == 'y' -%}
interface Metric {
  id: string
  label: string
  value: string
  trend: number
  comparison: string
}

interface TrafficSource {
  name: string
  value: number
  color: string
}

interface Product {
  id: string
  name: string
  image: string
  sales: number
  revenue: number
  growth: number
}
{%- endif %}

const selectedPeriod = ref('30d')
const activeActivityTab = ref('Daily')
const revenueChart = ref(null)
const trafficChart = ref(null)
const activityChart = ref(null)

const activityTabs = ['Daily', 'Weekly', 'Monthly']

const keyMetrics = ref({% if cookiecutter.use_typescript == 'y' %}<Metric[]>{% endif %}[
  {
    id: 'revenue',
    label: 'Total Revenue',
    value: '$48,574',
    trend: 12.5,
    comparison: 'vs last period'
  },
  {
    id: 'orders',
    label: 'Total Orders',
    value: '1,284',
    trend: 8.2,
    comparison: 'vs last period'
  },
  {
    id: 'customers',
    label: 'New Customers',
    value: '356',
    trend: -3.1,
    comparison: 'vs last period'
  },
  {
    id: 'conversion',
    label: 'Conversion Rate',
    value: '3.24%',
    trend: 5.7,
    comparison: 'vs last period'
  }
])

const trafficSources = ref({% if cookiecutter.use_typescript == 'y' %}<TrafficSource[]>{% endif %}[
  { name: 'Direct', value: 35, color: '#4299e1' },
  { name: 'Organic Search', value: 30, color: '#48bb78' },
  { name: 'Social Media', value: 20, color: '#ed8936' },
  { name: 'Referral', value: 10, color: '#9f7aea' },
  { name: 'Email', value: 5, color: '#f56565' }
])

const topProducts = ref({% if cookiecutter.use_typescript == 'y' %}<Product[]>{% endif %}[
  {
    id: '1',
    name: 'Premium Widget',
    image: 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect fill="%234299e1" width="100" height="100"/></svg>',
    sales: 543,
    revenue: 27150,
    growth: 15.3
  },
  {
    id: '2',
    name: 'Standard Package',
    image: 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect fill="%2348bb78" width="100" height="100"/></svg>',
    sales: 412,
    revenue: 16480,
    growth: 8.7
  },
  {
    id: '3',
    name: 'Basic Bundle',
    image: 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect fill="%23ed8936" width="100" height="100"/></svg>',
    sales: 329,
    revenue: 9870,
    growth: -2.4
  },
  {
    id: '4',
    name: 'Pro Edition',
    image: 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect fill="%239f7aea" width="100" height="100"/></svg>',
    sales: 287,
    revenue: 14350,
    growth: 12.1
  },
  {
    id: '5',
    name: 'Starter Kit',
    image: 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect fill="%23f56565" width="100" height="100"/></svg>',
    sales: 198,
    revenue: 3960,
    growth: 6.5
  }
])

let chartInstances = {
  revenue: null,
  traffic: null,
  activity: null
}

const initCharts = () => {
  // Revenue Chart
  if (revenueChart.value) {
    const ctx = revenueChart.value.getContext('2d')
    if (chartInstances.revenue) {
      chartInstances.revenue.destroy()
    }
    chartInstances.revenue = new Chart(ctx, {
      type: 'line',
      data: {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        datasets: [
          {
            label: 'Revenue',
            data: [30000, 35000, 32000, 40000, 38000, 48574],
            borderColor: '#4299e1',
            backgroundColor: 'rgba(66, 153, 225, 0.1)',
            tension: 0.4
          },
          {
            label: 'Profit',
            data: [12000, 15000, 13000, 18000, 16000, 22000],
            borderColor: '#48bb78',
            backgroundColor: 'rgba(72, 187, 120, 0.1)',
            tension: 0.4
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            ticks: {
              callback: function(value) {
                return '$' + value.toLocaleString()
              }
            }
          }
        }
      }
    })
  }

  // Traffic Chart (Doughnut)
  if (trafficChart.value) {
    const ctx = trafficChart.value.getContext('2d')
    if (chartInstances.traffic) {
      chartInstances.traffic.destroy()
    }
    chartInstances.traffic = new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: trafficSources.value.map(s => s.name),
        datasets: [{
          data: trafficSources.value.map(s => s.value),
          backgroundColor: trafficSources.value.map(s => s.color)
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false
          }
        }
      }
    })
  }

  // Activity Chart
  if (activityChart.value) {
    const ctx = activityChart.value.getContext('2d')
    if (chartInstances.activity) {
      chartInstances.activity.destroy()
    }
    chartInstances.activity = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        datasets: [{
          label: 'Active Users',
          data: [1200, 1900, 1500, 2100, 2300, 1800, 2000],
          backgroundColor: '#4299e1'
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false
          }
        },
        scales: {
          y: {
            beginAtZero: true
          }
        }
      }
    })
  }
}

onMounted(() => {
  initCharts()
})

watch([selectedPeriod, activeActivityTab], () => {
  // In a real app, fetch new data based on selection
  // For now, just reinitialize charts
  initCharts()
})
</script>

