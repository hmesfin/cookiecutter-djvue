<template>
  <div class="p-8 max-w-7xl mx-auto">
    <div class="page-header">
      <h1 class="page-title">Orders</h1>
      <div class="header-actions">
        <button @click="exportOrders" class="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg font-medium hover:bg-gray-300 transition-colors dark:bg-gray-700 dark:text-gray-300">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path>
          </svg>
          Export
        </button>
        <router-link to="/dashboard/orders/new" class="px-4 py-2 bg-indigo-600 text-white rounded-lg font-medium hover:bg-indigo-700 transition-colors">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
          </svg>
          New Order
        </router-link>
      </div>
    </div>

    <!-- Stats Cards -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <div class="bg-white rounded-lg shadow-md p-6 dark:bg-gray-900 dark:shadow-xl dark:shadow-gray-900/40">
        <div class="stat-icon pending">
          <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
          </svg>
        </div>
        <div class="stat-content">
          <div class="text-3xl font-bold text-gray-900 dark:text-gray-100">{% raw %}{{ stats.pending }}{% endraw %}</div>
          <div class="text-sm font-medium text-gray-600 mb-2 dark:text-gray-400">Pending Orders</div>
        </div>
      </div>
      
      <div class="bg-white rounded-lg shadow-md p-6 dark:bg-gray-900 dark:shadow-xl dark:shadow-gray-900/40">
        <div class="stat-icon processing">
          <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
          </svg>
        </div>
        <div class="stat-content">
          <div class="text-3xl font-bold text-gray-900 dark:text-gray-100">{% raw %}{{ stats.processing }}{% endraw %}</div>
          <div class="text-sm font-medium text-gray-600 mb-2 dark:text-gray-400">Processing</div>
        </div>
      </div>
      
      <div class="bg-white rounded-lg shadow-md p-6 dark:bg-gray-900 dark:shadow-xl dark:shadow-gray-900/40">
        <div class="stat-icon completed">
          <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
          </svg>
        </div>
        <div class="stat-content">
          <div class="text-3xl font-bold text-gray-900 dark:text-gray-100">{% raw %}{{ stats.completed }}{% endraw %}</div>
          <div class="text-sm font-medium text-gray-600 mb-2 dark:text-gray-400">Completed Today</div>
        </div>
      </div>
      
      <div class="bg-white rounded-lg shadow-md p-6 dark:bg-gray-900 dark:shadow-xl dark:shadow-gray-900/40">
        <div class="stat-icon revenue">
          <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
          </svg>
        </div>
        <div class="stat-content">
          <div class="text-3xl font-bold text-gray-900 dark:text-gray-100">${% raw %}{{ stats.revenue.toLocaleString() }}{% endraw %}</div>
          <div class="text-sm font-medium text-gray-600 mb-2 dark:text-gray-400">Today's Revenue</div>
        </div>
      </div>
    </div>

    <!-- Filters and Search -->
    <div class="filters-section">
      <div class="search-box">
        <svg class="search-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
        </svg>
        <input 
          v-model="searchQuery"
          type="text"
          placeholder="Search orders by ID, customer, or product..."
          class="search-input"
        >
      </div>
      
      <div class="filters">
        <select v-model="statusFilter" class="filter-select">
          <option value="">All Status</option>
          <option value="pending">Pending</option>
          <option value="processing">Processing</option>
          <option value="shipped">Shipped</option>
          <option value="delivered">Delivered</option>
          <option value="cancelled">Cancelled</option>
        </select>
        
        <select v-model="dateFilter" class="filter-select">
          <option value="">All Time</option>
          <option value="today">Today</option>
          <option value="yesterday">Yesterday</option>
          <option value="week">This Week</option>
          <option value="month">This Month</option>
        </select>
      </div>
    </div>

    <!-- Orders Table -->
    <div class="orders-table-card">
      <div class="table-wrapper">
        <table class="orders-table">
          <thead>
            <tr>
              <th>Order ID</th>
              <th>Customer</th>
              <th>Products</th>
              <th>Total</th>
              <th>Status</th>
              <th>Payment</th>
              <th>Date</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="order in paginatedOrders" :key="order.id">
              <td>
                <a href="#" class="order-id">#{% raw %}{{ order.id }}{% endraw %}</a>
              </td>
              <td>
                <div class="customer-info">
                  <div class="customer-name">{% raw %}{{ order.customer.name }}{% endraw %}</div>
                  <div class="customer-email">{% raw %}{{ order.customer.email }}{% endraw %}</div>
                </div>
              </td>
              <td>
                <div class="products-list">
                  <div v-for="(product, index) in order.products.slice(0, 2)" :key="index" class="product-item">
                    {% raw %}{{ product.name }}{% endraw %} (x{% raw %}{{ product.quantity }}{% endraw %})
                  </div>
                  <div v-if="order.products.length > 2" class="more-products">
                    +{% raw %}{{ order.products.length - 2 }}{% endraw %} more
                  </div>
                </div>
              </td>
              <td class="order-total">${% raw %}{{ order.total.toFixed(2) }}{% endraw %}</td>
              <td>
                <span :class="['status-badge', `status-${order.status}`]">
                  {% raw %}{{ order.status }}{% endraw %}
                </span>
              </td>
              <td>
                <span :class="['payment-badge', `payment-${order.payment.status}`]">
                  {% raw %}{{ order.payment.status }}{% endraw %}
                </span>
              </td>
              <td class="order-date">{% raw %}{{ formatDate(order.createdAt) }}{% endraw %}</td>
              <td>
                <div class="action-menu">
                  <button @click="toggleMenu(order.id)" class="action-btn">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 5v.01M12 12v.01M12 19v.01M12 6a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2z"></path>
                    </svg>
                  </button>
                  <div v-if="activeMenu === order.id" class="dropdown-menu">
                    <button @click="viewOrder(order)" class="dropdown-item">
                      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
                      </svg>
                      View Details
                    </button>
                    <button @click="editOrder(order)" class="dropdown-item">
                      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
                      </svg>
                      Edit
                    </button>
                    <button @click="printInvoice(order)" class="dropdown-item">
                      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z"></path>
                      </svg>
                      Print Invoice
                    </button>
                    <button @click="cancelOrder(order)" class="dropdown-item danger">
                      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                      </svg>
                      Cancel Order
                    </button>
                  </div>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination -->
      <div class="pagination">
        <div class="pagination-info">
          Showing {% raw %}{{ startIndex + 1 }}{% endraw %} to {% raw %}{{ endIndex }}{% endraw %} of {% raw %}{{ filteredOrders.length }}{% endraw %} orders
        </div>
        <div class="pagination-controls">
          <button 
            @click="currentPage--"
            :disabled="currentPage === 1"
            class="pagination-btn"
          >
            Previous
          </button>
          <button
            v-for="page in visiblePages"
            :key="page"
            @click="currentPage = page"
            :class="['pagination-btn', { active: currentPage === page }]"
          >
            {% raw %}{{ page }}{% endraw %}
          </button>
          <button 
            @click="currentPage++"
            :disabled="currentPage === totalPages"
            class="pagination-btn"
          >
            Next
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup{% if cookiecutter.use_typescript == 'y' %} lang="ts"{% endif %}>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

{% if cookiecutter.use_typescript == 'y' -%}
interface Customer {
  name: string
  email: string
}

interface Product {
  name: string
  quantity: number
  price: number
}

interface Payment {
  method: string
  status: 'paid' | 'pending' | 'failed'
}

interface Order {
  id: string
  customer: Customer
  products: Product[]
  total: number
  status: 'pending' | 'processing' | 'shipped' | 'delivered' | 'cancelled'
  payment: Payment
  createdAt: Date
}

interface Stats {
  pending: number
  processing: number
  completed: number
  revenue: number
}
{%- endif %}

const router = useRouter()

const searchQuery = ref('')
const statusFilter = ref('')
const dateFilter = ref('')
const currentPage = ref(1)
const itemsPerPage = 10
const activeMenu = ref(null)

const stats = ref({% if cookiecutter.use_typescript == 'y' %}<Stats>{% endif %}{
  pending: 12,
  processing: 8,
  completed: 24,
  revenue: 15847
})

const orders = ref({% if cookiecutter.use_typescript == 'y' %}<Order[]>{% endif %}[
  {
    id: '10234',
    customer: {
      name: 'John Doe',
      email: 'john.doe@example.com'
    },
    products: [
      { name: 'Premium Widget', quantity: 2, price: 49.99 },
      { name: 'Standard Package', quantity: 1, price: 29.99 }
    ],
    total: 129.97,
    status: 'pending',
    payment: {
      method: 'credit_card',
      status: 'paid'
    },
    createdAt: new Date('2024-01-15T10:30:00')
  },
  {
    id: '10235',
    customer: {
      name: 'Jane Smith',
      email: 'jane.smith@example.com'
    },
    products: [
      { name: 'Basic Bundle', quantity: 3, price: 19.99 },
      { name: 'Pro Edition', quantity: 1, price: 99.99 },
      { name: 'Starter Kit', quantity: 2, price: 14.99 }
    ],
    total: 189.95,
    status: 'processing',
    payment: {
      method: 'paypal',
      status: 'paid'
    },
    createdAt: new Date('2024-01-15T09:15:00')
  },
  {
    id: '10236',
    customer: {
      name: 'Bob Johnson',
      email: 'bob.johnson@example.com'
    },
    products: [
      { name: 'Enterprise Suite', quantity: 1, price: 299.99 }
    ],
    total: 299.99,
    status: 'shipped',
    payment: {
      method: 'bank_transfer',
      status: 'pending'
    },
    createdAt: new Date('2024-01-14T14:20:00')
  },
  {
    id: '10237',
    customer: {
      name: 'Alice Williams',
      email: 'alice.williams@example.com'
    },
    products: [
      { name: 'Premium Widget', quantity: 5, price: 49.99 }
    ],
    total: 249.95,
    status: 'delivered',
    payment: {
      method: 'credit_card',
      status: 'paid'
    },
    createdAt: new Date('2024-01-13T11:45:00')
  },
  {
    id: '10238',
    customer: {
      name: 'Charlie Brown',
      email: 'charlie.brown@example.com'
    },
    products: [
      { name: 'Standard Package', quantity: 2, price: 29.99 },
      { name: 'Basic Bundle', quantity: 1, price: 19.99 }
    ],
    total: 79.97,
    status: 'cancelled',
    payment: {
      method: 'credit_card',
      status: 'failed'
    },
    createdAt: new Date('2024-01-12T16:30:00')
  }
])

const filteredOrders = computed(() => {
  let result = [...orders.value]
  
  // Search filter
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(order => 
      order.id.includes(query) ||
      order.customer.name.toLowerCase().includes(query) ||
      order.customer.email.toLowerCase().includes(query) ||
      order.products.some(p => p.name.toLowerCase().includes(query))
    )
  }
  
  // Status filter
  if (statusFilter.value) {
    result = result.filter(order => order.status === statusFilter.value)
  }
  
  // Date filter
  if (dateFilter.value) {
    const now = new Date()
    const today = new Date(now.getFullYear(), now.getMonth(), now.getDate())
    const yesterday = new Date(today)
    yesterday.setDate(yesterday.getDate() - 1)
    const weekAgo = new Date(today)
    weekAgo.setDate(weekAgo.getDate() - 7)
    const monthAgo = new Date(today)
    monthAgo.setMonth(monthAgo.getMonth() - 1)
    
    switch (dateFilter.value) {
      case 'today':
        result = result.filter(order => order.createdAt >= today)
        break
      case 'yesterday':
        result = result.filter(order => order.createdAt >= yesterday && order.createdAt < today)
        break
      case 'week':
        result = result.filter(order => order.createdAt >= weekAgo)
        break
      case 'month':
        result = result.filter(order => order.createdAt >= monthAgo)
        break
    }
  }
  
  return result
})

const totalPages = computed(() => Math.ceil(filteredOrders.value.length / itemsPerPage))
const startIndex = computed(() => (currentPage.value - 1) * itemsPerPage)
const endIndex = computed(() => Math.min(startIndex.value + itemsPerPage, filteredOrders.value.length))
const paginatedOrders = computed(() => filteredOrders.value.slice(startIndex.value, endIndex.value))

const visiblePages = computed(() => {
  const pages = []
  const maxVisible = 5
  let start = Math.max(1, currentPage.value - Math.floor(maxVisible / 2))
  let end = Math.min(totalPages.value, start + maxVisible - 1)
  
  if (end - start < maxVisible - 1) {
    start = Math.max(1, end - maxVisible + 1)
  }
  
  for (let i = start; i <= end; i++) {
    pages.push(i)
  }
  
  return pages
})

const formatDate = (date{% if cookiecutter.use_typescript == 'y' %}: Date{% endif %}) => {
  return date.toLocaleDateString('en-US', { 
    month: 'short', 
    day: 'numeric', 
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const toggleMenu = (orderId{% if cookiecutter.use_typescript == 'y' %}: string | null{% endif %}) => {
  activeMenu.value = activeMenu.value === orderId ? null : orderId
}

const viewOrder = (order{% if cookiecutter.use_typescript == 'y' %}: Order{% endif %}) => {
  console.log('View order:', order)
  activeMenu.value = null
}

const editOrder = (order{% if cookiecutter.use_typescript == 'y' %}: Order{% endif %}) => {
  console.log('Edit order:', order)
  activeMenu.value = null
}

const printInvoice = (order{% if cookiecutter.use_typescript == 'y' %}: Order{% endif %}) => {
  console.log('Print invoice for order:', order)
  activeMenu.value = null
}

const cancelOrder = (order{% if cookiecutter.use_typescript == 'y' %}: Order{% endif %}) => {
  if (confirm(`Are you sure you want to cancel order #${order.id}?`)) {
    order.status = 'cancelled'
    activeMenu.value = null
  }
}

const exportOrders = () => {
  console.log('Exporting orders...')
}
</script>

