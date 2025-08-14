<template>
  <div class="p-8 max-w-6xl mx-auto">
        <PageHeader
      title="Create New Order" :show-back="true" back-link="/dashboard/orders" back-text="Back to Orders"
    />

    <form @submit.prevent="handleSubmit" class="space-y-6">
      <div class="space-y-6">
        <!-- Customer Information -->
        <div class="bg-white rounded-lg shadow-md p-6 mb-6">
          <h2 class="text-xl font-semibold text-gray-900 mb-2 dark:text-gray-100">Customer Information</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="mb-6">
              <label for="customerName">Customer Name *</label>
              <input 
                id="customerName"
                v-model="orderForm.customer.name"
                type="text"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 dark:border-gray-600 dark:focus:ring-indigo-400 dark:focus:border-indigo-400"
                required
                placeholder="John Doe"
              >
            </div>
            <div class="mb-6">
              <label for="customerEmail">Email Address *</label>
              <input 
                id="customerEmail"
                v-model="orderForm.customer.email"
                type="email"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 dark:border-gray-600 dark:focus:ring-indigo-400 dark:focus:border-indigo-400"
                required
                placeholder="john@example.com"
              >
            </div>
            <div class="mb-6">
              <label for="customerPhone">Phone Number</label>
              <input 
                id="customerPhone"
                v-model="orderForm.customer.phone"
                type="tel"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 dark:border-gray-600 dark:focus:ring-indigo-400 dark:focus:border-indigo-400"
                placeholder="+1 234 567 8900"
              >
            </div>
            <div class="mb-6">
              <label for="customerCompany">Company</label>
              <input 
                id="customerCompany"
                v-model="orderForm.customer.company"
                type="text"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 dark:border-gray-600 dark:focus:ring-indigo-400 dark:focus:border-indigo-400"
                placeholder="Acme Corp"
              >
            </div>
          </div>
        </div>

        <!-- Shipping Address -->
        <div class="bg-white rounded-lg shadow-md p-6 mb-6">
          <h2 class="text-xl font-semibold text-gray-900 mb-2 dark:text-gray-100">Shipping Address</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="mb-6 md:col-span-2">
              <label for="shippingAddress">Street Address *</label>
              <input 
                id="shippingAddress"
                v-model="orderForm.shipping.address"
                type="text"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 dark:border-gray-600 dark:focus:ring-indigo-400 dark:focus:border-indigo-400"
                required
                placeholder="123 Main Street"
              >
            </div>
            <div class="mb-6">
              <label for="shippingCity">City *</label>
              <input 
                id="shippingCity"
                v-model="orderForm.shipping.city"
                type="text"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 dark:border-gray-600 dark:focus:ring-indigo-400 dark:focus:border-indigo-400"
                required
                placeholder="New York"
              >
            </div>
            <div class="mb-6">
              <label for="shippingState">State/Province *</label>
              <input 
                id="shippingState"
                v-model="orderForm.shipping.state"
                type="text"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 dark:border-gray-600 dark:focus:ring-indigo-400 dark:focus:border-indigo-400"
                required
                placeholder="NY"
              >
            </div>
            <div class="mb-6">
              <label for="shippingZip">ZIP/Postal Code *</label>
              <input 
                id="shippingZip"
                v-model="orderForm.shipping.zip"
                type="text"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 dark:border-gray-600 dark:focus:ring-indigo-400 dark:focus:border-indigo-400"
                required
                placeholder="10001"
              >
            </div>
            <div class="mb-6">
              <label for="shippingCountry">Country *</label>
              <select 
                id="shippingCountry"
                v-model="orderForm.shipping.country"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 dark:border-gray-600 dark:focus:ring-indigo-400 dark:focus:border-indigo-400"
                required
              >
                <option value="">Select Country</option>
                <option value="US">United States</option>
                <option value="CA">Canada</option>
                <option value="GB">United Kingdom</option>
                <option value="AU">Australia</option>
                <option value="DE">Germany</option>
                <option value="FR">France</option>
              </select>
            </div>
          </div>
        </div>

        <!-- Products -->
        <div class="bg-white rounded-lg shadow-md p-6 mb-6">
          <div class="mb-6">
            <h2 class="text-xl font-semibold text-gray-900 mb-2 dark:text-gray-100">Products</h2>
            <button type="button" @click="addProduct" class="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg font-medium hover:bg-gray-300 transition-colors dark:bg-gray-700 dark:text-gray-300">
              <IconLucidePlus class="w-5 h-5" />
              Add Product
            </button>
          </div>
          
          <div class="bg-white rounded-lg shadow-md p-6">
            <table>
              <thead>
                <tr>
                  <th>Product</th>
                  <th>SKU</th>
                  <th>Quantity</th>
                  <th>Price</th>
                  <th>Total</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(product, index) in orderForm.products" :key="index">
                  <td>
                    <select 
                      v-model="product.name"
                      class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 dark:border-gray-600 dark:focus:ring-indigo-400 dark:focus:border-indigo-400"
                      required
                      @change="updateProductDetails(index)"
                    >
                      <option value="">Select Product</option>
                      <option v-for="p in availableProducts" :key="p.id" :value="p.name">
                        {% raw %}{{ p.name }}{% endraw %}
                      </option>
                    </select>
                  </td>
                  <td>
                    <input 
                      v-model="product.sku"
                      type="text"
                      class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 dark:border-gray-600 dark:focus:ring-indigo-400 dark:focus:border-indigo-400"
                      readonly
                    >
                  </td>
                  <td>
                    <input 
                      v-model.number="product.quantity"
                      type="number"
                      min="1"
                      class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 dark:border-gray-600 dark:focus:ring-indigo-400 dark:focus:border-indigo-400"
                      required
                      @input="calculateTotals"
                    >
                  </td>
                  <td>
                    <input 
                      v-model.number="product.price"
                      type="number"
                      step="0.01"
                      min="0"
                      class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 dark:border-gray-600 dark:focus:ring-indigo-400 dark:focus:border-indigo-400"
                      required
                      @input="calculateTotals"
                    >
                  </td>
                  <td class="font-semibold text-gray-900">
                    ${% raw %}{{ (product.quantity * product.price).toFixed(2) }}{% endraw %}
                  </td>
                  <td>
                    <button 
                      type="button"
                      @click="removeProduct(index)"
                      class="p-2 hover:bg-gray-100 rounded-lg transition-colors danger"
                      title="Remove"
                    >
                      <IconLucideTrash2 class="w-5 h-5" />
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Order Summary -->
        <div class="bg-white rounded-lg shadow-md p-6 mb-6">
          <h2 class="text-xl font-semibold text-gray-900 mb-2 dark:text-gray-100">Order Summary</h2>
          <div class="bg-gray-50 rounded-lg p-4 space-y-2">
            <div class="flex justify-between">
              <span class="text-gray-600">Subtotal:</span>
              <span class="font-semibold text-gray-900">${% raw %}{{ orderSummary.subtotal.toFixed(2) }}{% endraw %}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">Tax ({% raw %}{{ orderSummary.taxRate }}{% endraw %}%):</span>
              <span class="font-semibold text-gray-900">${% raw %}{{ orderSummary.tax.toFixed(2) }}{% endraw %}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">Shipping:</span>
              <span class="font-semibold text-gray-900">${% raw %}{{ orderSummary.shipping.toFixed(2) }}{% endraw %}</span>
            </div>
            <div class="flex justify-between">
              <label for="discount" class="text-gray-600">Discount:</label>
              <input 
                id="discount"
                v-model.number="orderSummary.discount"
                type="number"
                step="0.01"
                min="0"
                class="form-input small"
                @input="calculateTotals"
              >
            </div>
            <div class="flex justify-between total">
              <span class="text-gray-600">Total:</span>
              <span class="font-semibold text-gray-900">${% raw %}{{ orderSummary.total.toFixed(2) }}{% endraw %}</span>
            </div>
          </div>
        </div>

        <!-- Payment & Notes -->
        <div class="bg-white rounded-lg shadow-md p-6 mb-6">
          <h2 class="text-xl font-semibold text-gray-900 mb-2 dark:text-gray-100">Payment & Notes</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="mb-6">
              <label for="paymentMethod">Payment Method *</label>
              <select 
                id="paymentMethod"
                v-model="orderForm.payment.method"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 dark:border-gray-600 dark:focus:ring-indigo-400 dark:focus:border-indigo-400"
                required
              >
                <option value="">Select Payment Method</option>
                <option value="credit_card">Credit Card</option>
                <option value="paypal">PayPal</option>
                <option value="bank_transfer">Bank Transfer</option>
                <option value="cash">Cash</option>
              </select>
            </div>
            <div class="mb-6">
              <label for="paymentStatus">Payment Status *</label>
              <select 
                id="paymentStatus"
                v-model="orderForm.payment.status"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 dark:border-gray-600 dark:focus:ring-indigo-400 dark:focus:border-indigo-400"
                required
              >
                <option value="pending">Pending</option>
                <option value="paid">Paid</option>
                <option value="partial">Partial</option>
              </select>
            </div>
            <div class="mb-6 md:col-span-2">
              <label for="orderNotes">Order Notes</label>
              <textarea 
                id="orderNotes"
                v-model="orderForm.notes"
                rows="4"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 dark:border-gray-600 dark:focus:ring-indigo-400 dark:focus:border-indigo-400"
                placeholder="Add any special instructions or notes..."
              ></textarea>
            </div>
          </div>
        </div>
      </div>

      <!-- Form Actions -->
      <div class="flex justify-end gap-3 mt-8">
        <router-link to="/dashboard/orders" class="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg font-medium hover:bg-gray-300 transition-colors dark:bg-gray-700 dark:text-gray-300">
          Cancel
        </router-link>
        <button type="submit" class="px-4 py-2 bg-indigo-600 text-white rounded-lg font-medium hover:bg-indigo-700 transition-colors" :disabled="loading">
          {% raw %}{{ loading ? 'Creating...' : 'Create Order' }}{% endraw %}
        </button>
      </div>
    </form>
  </div>
</template>

<script setup{% if cookiecutter.use_typescript == 'y' %} lang="ts"{% endif %}>
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'

{% if cookiecutter.use_typescript == 'y' -%}
interface Product {
  id: string
  name: string
  sku: string
  price: number
  stock: number
}

interface OrderProduct {
  name: string
  sku: string
  quantity: number
  price: number
}

interface OrderForm {
  customer: {
    name: string
    email: string
    phone: string
    company: string
  }
  shipping: {
    address: string
    city: string
    state: string
    zip: string
    country: string
  }
  products: OrderProduct[]
  payment: {
    method: string
    status: string
  }
  notes: string
}

interface OrderSummary {
  subtotal: number
  taxRate: number
  tax: number
  shipping: number
  discount: number
  total: number
}
{%- endif %}

const router = useRouter()
const loading = ref(false)

const availableProducts = ref({% if cookiecutter.use_typescript == 'y' %}<Product[]>{% endif %}[
  { id: '1', name: 'Premium Widget', sku: 'PW-001', price: 49.99, stock: 100 },
  { id: '2', name: 'Standard Package', sku: 'SP-002', price: 29.99, stock: 50 },
  { id: '3', name: 'Basic Bundle', sku: 'BB-003', price: 19.99, stock: 200 },
  { id: '4', name: 'Pro Edition', sku: 'PE-004', price: 99.99, stock: 25 },
  { id: '5', name: 'Starter Kit', sku: 'SK-005', price: 14.99, stock: 150 },
  { id: '6', name: 'Enterprise Suite', sku: 'ES-006', price: 299.99, stock: 10 }
])

const orderForm = reactive({% if cookiecutter.use_typescript == 'y' %}<OrderForm>{% endif %}{
  customer: {
    name: '',
    email: '',
    phone: '',
    company: ''
  },
  shipping: {
    address: '',
    city: '',
    state: '',
    zip: '',
    country: ''
  },
  products: [
    {
      name: '',
      sku: '',
      quantity: 1,
      price: 0
    }
  ],
  payment: {
    method: '',
    status: 'pending'
  },
  notes: ''
})

const orderSummary = reactive({% if cookiecutter.use_typescript == 'y' %}<OrderSummary>{% endif %}{
  subtotal: 0,
  taxRate: 8.5,
  tax: 0,
  shipping: 10,
  discount: 0,
  total: 0
})

const addProduct = () => {
  orderForm.products.push({
    name: '',
    sku: '',
    quantity: 1,
    price: 0
  })
}

const removeProduct = (index{% if cookiecutter.use_typescript == 'y' %}: number{% endif %}) => {
  if (orderForm.products.length > 1) {
    orderForm.products.splice(index, 1)
    calculateTotals()
  }
}

const updateProductDetails = (index{% if cookiecutter.use_typescript == 'y' %}: number{% endif %}) => {
  const productName = orderForm.products[index].name
  const product = availableProducts.value.find(p => p.name === productName)
  
  if (product) {
    orderForm.products[index].sku = product.sku
    orderForm.products[index].price = product.price
    calculateTotals()
  }
}

const calculateTotals = () => {
  // Calculate subtotal
  orderSummary.subtotal = orderForm.products.reduce((total, product) => {
    return total + (product.quantity * product.price)
  }, 0)
  
  // Calculate tax
  orderSummary.tax = orderSummary.subtotal * (orderSummary.taxRate / 100)
  
  // Calculate total
  orderSummary.total = orderSummary.subtotal + orderSummary.tax + orderSummary.shipping - orderSummary.discount
}

const handleSubmit = async () => {
  loading.value = true
  
  try {
    // Validate that at least one product is selected
    const hasProducts = orderForm.products.some(p => p.name && p.quantity > 0)
    if (!hasProducts) {
      alert('Please add at least one product to the order')
      return
    }
    
    // In a real app, send order data to API
    const orderData = {
      ...orderForm,
      summary: { ...orderSummary }
    }
    
    console.log('Creating order:', orderData)
    
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1500))
    
    alert('Order created successfully!')
    router.push('/dashboard/orders')
  } catch (error) {
    console.error('Error creating order:', error)
    alert('Failed to create order. Please try again.')
  } finally {
    loading.value = false
  }
}

// Calculate initial totals
calculateTotals()
</script>

