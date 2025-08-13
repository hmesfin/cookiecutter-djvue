<template>
  <div class="analytics-view">
    <div class="page-header">
      <h1 class="page-title">Analytics</h1>
      <div class="header-actions">
        <select v-model="selectedPeriod" class="period-selector">
          <option value="7d">Last 7 days</option>
          <option value="30d">Last 30 days</option>
          <option value="90d">Last 90 days</option>
          <option value="1y">Last year</option>
        </select>
        <button class="btn btn-primary">
          <svg class="icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path>
          </svg>
          Export
        </button>
      </div>
    </div>

    <!-- Key Metrics -->
    <div class="metrics-grid">
      <div v-for="metric in keyMetrics" :key="metric.id" class="metric-card">
        <div class="metric-header">
          <span class="metric-label">{% raw %}{{ metric.label }}{% endraw %}</span>
          <span :class="['metric-trend', metric.trend > 0 ? 'positive' : 'negative']">
            <svg class="trend-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path v-if="metric.trend > 0" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path>
              <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 17h8m0 0V9m0 8l-8-8-4 4-6-6"></path>
            </svg>
            {% raw %}{{ Math.abs(metric.trend) }}%{% endraw %}
          </span>
        </div>
        <div class="metric-value">{% raw %}{{ metric.value }}{% endraw %}</div>
        <div class="metric-comparison">{% raw %}{{ metric.comparison }}{% endraw %}</div>
      </div>
    </div>

    <!-- Charts -->
    <div class="charts-grid">
      <!-- Revenue Chart -->
      <div class="chart-card">
        <div class="chart-header">
          <h3 class="chart-title">Revenue Overview</h3>
          <div class="chart-legend">
            <span class="legend-item">
              <span class="legend-dot" style="background: #4299e1"></span>
              Revenue
            </span>
            <span class="legend-item">
              <span class="legend-dot" style="background: #48bb78"></span>
              Profit
            </span>
          </div>
        </div>
        <div class="chart-container">
          <canvas ref="revenueChart"></canvas>
        </div>
      </div>

      <!-- Traffic Sources -->
      <div class="chart-card">
        <div class="chart-header">
          <h3 class="chart-title">Traffic Sources</h3>
        </div>
        <div class="chart-container">
          <canvas ref="trafficChart"></canvas>
        </div>
        <div class="traffic-legend">
          <div v-for="source in trafficSources" :key="source.name" class="traffic-item">
            <div class="traffic-info">
              <span class="traffic-dot" :style="{ background: source.color }"></span>
              <span class="traffic-name">{% raw %}{{ source.name }}{% endraw %}</span>
            </div>
            <span class="traffic-value">{% raw %}{{ source.value }}%{% endraw %}</span>
          </div>
        </div>
      </div>

      <!-- User Activity -->
      <div class="chart-card full-width">
        <div class="chart-header">
          <h3 class="chart-title">User Activity</h3>
          <div class="chart-tabs">
            <button 
              v-for="tab in activityTabs" 
              :key="tab"
              @click="activeActivityTab = tab"
              :class="['tab-btn', { active: activeActivityTab === tab }]"
            >
              {% raw %}{{ tab }}{% endraw %}
            </button>
          </div>
        </div>
        <div class="chart-container">
          <canvas ref="activityChart"></canvas>
        </div>
      </div>
    </div>

    <!-- Top Products Table -->
    <div class="table-card">
      <div class="table-header">
        <h3 class="table-title">Top Products</h3>
        <button class="btn-text">View All</button>
      </div>
      <div class="table-wrapper">
        <table class="data-table">
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

<script setup>
{% if cookiecutter.use_typescript == 'y' -%}
import { ref, onMounted, watch } from 'vue'
import Chart from 'chart.js/auto'

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
{% else -%}
import { ref, onMounted, watch } from 'vue'
import Chart from 'chart.js/auto'
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

<style scoped>
.analytics-view {
  padding: 2rem;
  max-width: 1600px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.page-title {
  font-size: 2rem;
  font-weight: 700;
  color: #1a202c;
  margin: 0;
}

.header-actions {
  display: flex;
  gap: 1rem;
}

.period-selector {
  padding: 0.5rem 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.375rem;
  background: white;
  font-size: 0.875rem;
  cursor: pointer;
}

.btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
}

.btn-primary {
  background: #4299e1;
  color: white;
}

.btn-primary:hover {
  background: #3182ce;
}

.icon {
  width: 16px;
  height: 16px;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.metric-card {
  background: white;
  padding: 1.5rem;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
}

.metric-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.metric-label {
  font-size: 0.875rem;
  color: #718096;
  font-weight: 500;
}

.metric-trend {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.75rem;
  font-weight: 500;
}

.metric-trend.positive {
  color: #48bb78;
}

.metric-trend.negative {
  color: #f56565;
}

.trend-icon {
  width: 16px;
  height: 16px;
}

.metric-value {
  font-size: 2rem;
  font-weight: 700;
  color: #1a202c;
  margin-bottom: 0.25rem;
}

.metric-comparison {
  font-size: 0.75rem;
  color: #a0aec0;
}

.charts-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.chart-card {
  background: white;
  padding: 1.5rem;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
}

.chart-card.full-width {
  grid-column: span 2;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.chart-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1a202c;
  margin: 0;
}

.chart-legend {
  display: flex;
  gap: 1rem;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: #4a5568;
}

.legend-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.chart-container {
  position: relative;
  height: 300px;
}

.chart-tabs {
  display: flex;
  gap: 0.5rem;
}

.tab-btn {
  padding: 0.25rem 0.75rem;
  border: none;
  background: transparent;
  color: #718096;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  border-radius: 0.25rem;
  transition: all 0.2s;
}

.tab-btn:hover {
  background: #f7fafc;
}

.tab-btn.active {
  background: #edf2f7;
  color: #4299e1;
}

.traffic-legend {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-top: 1.5rem;
}

.traffic-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.traffic-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.traffic-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.traffic-name {
  font-size: 0.875rem;
  color: #4a5568;
}

.traffic-value {
  font-size: 0.875rem;
  font-weight: 500;
  color: #1a202c;
}

.table-card {
  background: white;
  padding: 1.5rem;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.table-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1a202c;
  margin: 0;
}

.btn-text {
  background: none;
  border: none;
  color: #4299e1;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: color 0.2s;
}

.btn-text:hover {
  color: #3182ce;
}

.table-wrapper {
  overflow-x: auto;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th {
  text-align: left;
  padding: 0.75rem;
  border-bottom: 1px solid #e2e8f0;
  font-size: 0.75rem;
  font-weight: 600;
  color: #718096;
  text-transform: uppercase;
}

.data-table td {
  padding: 0.75rem;
  border-bottom: 1px solid #f7fafc;
  font-size: 0.875rem;
  color: #2d3748;
}

.product-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.product-image {
  width: 40px;
  height: 40px;
  border-radius: 0.375rem;
  object-fit: cover;
}

.growth-badge {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  font-weight: 500;
}

.growth-badge.positive {
  background: #c6f6d5;
  color: #22543d;
}

.growth-badge.negative {
  background: #fed7d7;
  color: #742a2a;
}

@media (max-width: 1024px) {
  .charts-grid {
    grid-template-columns: 1fr;
  }
  
  .chart-card.full-width {
    grid-column: span 1;
  }
}

@media (max-width: 768px) {
  .analytics-view {
    padding: 1rem;
  }
  
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .metrics-grid {
    grid-template-columns: 1fr;
  }
  
  .table-wrapper {
    overflow-x: scroll;
  }
}
</style>