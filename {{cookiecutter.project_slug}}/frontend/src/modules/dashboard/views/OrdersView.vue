<template>
  <div class="p-8 max-w-7xl mx-auto">
    <PageHeader
      title="Orders" 
      description="Manage and track all customer orders"
    >
      <template #actions>
        <button @click="router.push('/dashboard/orders/new')" class="px-4 py-2 bg-indigo-600 text-white rounded-lg font-medium hover:bg-indigo-700 transition-colors">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
          </svg>
          New Order
        </button>
      </template>
    </PageHeader>

    <!-- Stats Cards -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Pending Orders</p>
            <p class="text-2xl font-bold text-gray-900 dark:text-gray-100">{% raw %}{{ stats.pending }}{% endraw %}</p>
          </div>
          <div class="p-3 bg-yellow-100 rounded-full">
            <svg class="w-6 h-6 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
          </div>
        </div>
      </div>

      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Processing</p>
            <p class="text-2xl font-bold text-gray-900 dark:text-gray-100">{% raw %}{{ stats.processing }}{% endraw %}</p>
          </div>
          <div class="p-3 bg-blue-100 rounded-full">
            <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"></path>
            </svg>
          </div>
        </div>
      </div>

      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Completed</p>
            <p class="text-2xl font-bold text-gray-900 dark:text-gray-100">{% raw %}{{ stats.completed }}{% endraw %}</p>
          </div>
          <div class="p-3 bg-green-100 rounded-full">
            <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
          </div>
        </div>
      </div>

      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Revenue</p>
            <p class="text-2xl font-bold text-gray-900 dark:text-gray-100">${% raw %}{{ stats.revenue.toLocaleString() }}{% endraw %}</p>
          </div>
          <div class="p-3 bg-indigo-100 rounded-full">
            <svg class="w-6 h-6 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
          </div>
        </div>
      </div>
    </div>

    <!-- Filters -->
    <div class="flex gap-4 mb-6">
      <div class="relative flex-1">
        <svg class="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
        </svg>
        <input 
          v-model="searchQuery"
          type="text"
          placeholder="Search orders..."
          class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
        >
      </div>
      
      <select 
        v-model="statusFilter"
        class="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
      >
        <option value="">All Status</option>
        <option value="pending">Pending</option>
        <option value="processing">Processing</option>
        <option value="shipped">Shipped</option>
        <option value="delivered">Delivered</option>
        <option value="cancelled">Cancelled</option>
      </select>
      
      <select 
        v-model="dateFilter"
        class="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
      >
        <option value="">All Time</option>
        <option value="today">Today</option>
        <option value="yesterday">Yesterday</option>
        <option value="week">This Week</option>
        <option value="month">This Month</option>
      </select>
      
      <button @click="exportOrders" class="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg font-medium hover:bg-gray-300 transition-colors dark:bg-gray-700 dark:text-gray-300">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
        </svg>
        Export
      </button>
    </div>

    <!-- Orders Table -->
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead>
            <tr class="border-b border-gray-200">
              <th class="text-left py-3 px-4 font-medium text-gray-700 dark:text-gray-400">Order ID</th>
              <th class="text-left py-3 px-4 font-medium text-gray-700 dark:text-gray-400">Customer</th>
              <th class="text-left py-3 px-4 font-medium text-gray-700 dark:text-gray-400">Products</th>
              <th class="text-left py-3 px-4 font-medium text-gray-700 dark:text-gray-400">Total</th>
              <th class="text-left py-3 px-4 font-medium text-gray-700 dark:text-gray-400">Status</th>
              <th class="text-left py-3 px-4 font-medium text-gray-700 dark:text-gray-400">Payment</th>
              <th class="text-left py-3 px-4 font-medium text-gray-700 dark:text-gray-400">Date</th>
              <th class="text-left py-3 px-4 font-medium text-gray-700 dark:text-gray-400">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="order in paginatedOrders" :key="order.id" class="border-b border-gray-100 hover:bg-gray-50">
              <td class="py-3 px-4">
                <span class="font-medium text-gray-900">#{% raw %}{{ order.id }}{% endraw %}</span>
              </td>
              <td class="py-3 px-4">
                <div>
                  <div class="font-medium text-gray-900 dark:text-gray-100">{% raw %}{{ order.customer.name }}{% endraw %}</div>
                  <div class="text-sm text-gray-500 dark:text-gray-400">{% raw %}{{ order.customer.email }}{% endraw %}</div>
                </div>
              </td>
              <td class="py-3 px-4">
                <div class="text-sm">
                  <div v-for="(product, idx) in order.products.slice(0, 2)" :key="idx" class="text-gray-900 dark:text-gray-100">
                    {% raw %}{{ product.quantity }}{% endraw %}x {% raw %}{{ product.name }}{% endraw %}
                  </div>
                  <div v-if="order.products.length > 2" class="text-gray-500 dark:text-gray-400">
                    +{% raw %}{{ order.products.length - 2 }}{% endraw %} more
                  </div>
                </div>
              </td>
              <td class="py-3 px-4">
                <span class="font-semibold text-gray-900 dark:text-gray-100">${% raw %}{{ order.total.toFixed(2) }}{% endraw %}</span>
              </td>
              <td class="py-3 px-4">
                <span 
                  :class="[
                    'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
                    order.status === 'pending' ? 'bg-yellow-100 text-yellow-800' :
                    order.status === 'processing' ? 'bg-blue-100 text-blue-800' :
                    order.status === 'shipped' ? 'bg-purple-100 text-purple-800' :
                    order.status === 'delivered' ? 'bg-green-100 text-green-800' :
                    'bg-red-100 text-red-800'
                  ]"
                >
                  {% raw %}{{ order.status }}{% endraw %}
                </span>
              </td>
              <td class="py-3 px-4">
                <div class="flex items-center gap-2">
                  <span 
                    :class="[
                      'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
                      order.payment.status === 'paid' ? 'bg-green-100 text-green-800' :
                      order.payment.status === 'pending' ? 'bg-yellow-100 text-yellow-800' :
                      'bg-red-100 text-red-800'
                    ]"
                  >
                    {% raw %}{{ order.payment.status }}{% endraw %}
                  </span>
                </div>
              </td>
              <td class="py-3 px-4 text-sm text-gray-500 dark:text-gray-400">
                {% raw %}{{ formatDate(order.createdAt) }}{% endraw %}
              </td>
              <td class="py-3 px-4">
                <div class="relative">
                  <button 
                    @click="toggleMenu(order.id)"
                    class="p-2 hover:bg-gray-100 rounded-lg transition-colors"
                  >
                    <svg class="w-5 h-5 text-gray-500 dark:text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 5v.01M12 12v.01M12 19v.01M12 6a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2z"></path>
                    </svg>
                  </button>
                  
                  <div 
                    v-if="activeMenu === order.id"
                    class="absolute right-0 mt-2 w-48 bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 z-10"
                  >
                    <button 
                      @click="viewOrder(order)"
                      class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 dark:text-gray-400 dark:hover:bg-gray-700"
                    >
                      View Details
                    </button>
                    <button 
                      @click="editOrder(order)"
                      class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 dark:text-gray-400 dark:hover:bg-gray-700"
                    >
                      Edit Order
                    </button>
                    <button 
                      @click="printInvoice(order)"
                      class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 dark:text-gray-400 dark:hover:bg-gray-700"
                    >
                      Print Invoice
                    </button>
                    <hr class="my-1">
                    <button 
                      @click="cancelOrder(order)"
                      class="block w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50"
                    >
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
      <div class="flex items-center justify-between mt-6">
        <div class="text-sm text-gray-600 dark:text-gray-400">
          Showing {% raw %}{{ startIndex + 1 }}{% endraw %} to {% raw %}{{ endIndex }}{% endraw %} of {% raw %}{{ filteredOrders.length }}{% endraw %} orders
        </div>
        <div class="flex gap-2">
          <button 
            @click="currentPage--"
            :disabled="currentPage === 1"
            class="px-3 py-1 border border-gray-300 dark:border-gray-600 rounded-lg text-sm font-medium text-gray-700 dark:text-gray-400 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Previous
          </button>
          <button
            v-for="page in visiblePages"
            :key="page"
            @click="currentPage = page"
            :class="[
              'px-3 py-1 border rounded-lg text-sm font-medium',
              currentPage === page 
                ? 'bg-indigo-600 text-white border-indigo-600' 
                : 'border-gray-300 text-gray-700 dark:border-gray-600 dark:text-gray-400 dark:hover:bg-gray-700'
            ]"
          >
            {% raw %}{{ page }}{% endraw %}
          </button>
          <button 
            @click="currentPage++"
            :disabled="currentPage === totalPages"
            class="px-3 py-1 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 dark:hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed"
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
import PageHeader from '@/components/PageHeader.vue'

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