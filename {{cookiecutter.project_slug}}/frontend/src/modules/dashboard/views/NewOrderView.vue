<template>
  <div class="new-order-view">
    <div class="page-header">
      <div class="header-left">
        <router-link to="/dashboard/orders" class="back-link">
          <svg class="icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path>
          </svg>
          Back to Orders
        </router-link>
        <h1 class="page-title">Create New Order</h1>
      </div>
    </div>

    <form @submit.prevent="handleSubmit" class="order-form">
      <div class="form-sections">
        <!-- Customer Information -->
        <div class="form-section">
          <h2 class="section-title">Customer Information</h2>
          <div class="form-grid">
            <div class="form-group">
              <label for="customerName">Customer Name *</label>
              <input 
                id="customerName"
                v-model="orderForm.customer.name"
                type="text"
                class="form-input"
                required
                placeholder="John Doe"
              >
            </div>
            <div class="form-group">
              <label for="customerEmail">Email Address *</label>
              <input 
                id="customerEmail"
                v-model="orderForm.customer.email"
                type="email"
                class="form-input"
                required
                placeholder="john@example.com"
              >
            </div>
            <div class="form-group">
              <label for="customerPhone">Phone Number</label>
              <input 
                id="customerPhone"
                v-model="orderForm.customer.phone"
                type="tel"
                class="form-input"
                placeholder="+1 234 567 8900"
              >
            </div>
            <div class="form-group">
              <label for="customerCompany">Company</label>
              <input 
                id="customerCompany"
                v-model="orderForm.customer.company"
                type="text"
                class="form-input"
                placeholder="Acme Corp"
              >
            </div>
          </div>
        </div>

        <!-- Shipping Address -->
        <div class="form-section">
          <h2 class="section-title">Shipping Address</h2>
          <div class="form-grid">
            <div class="form-group full-width">
              <label for="shippingAddress">Street Address *</label>
              <input 
                id="shippingAddress"
                v-model="orderForm.shipping.address"
                type="text"
                class="form-input"
                required
                placeholder="123 Main Street"
              >
            </div>
            <div class="form-group">
              <label for="shippingCity">City *</label>
              <input 
                id="shippingCity"
                v-model="orderForm.shipping.city"
                type="text"
                class="form-input"
                required
                placeholder="New York"
              >
            </div>
            <div class="form-group">
              <label for="shippingState">State/Province *</label>
              <input 
                id="shippingState"
                v-model="orderForm.shipping.state"
                type="text"
                class="form-input"
                required
                placeholder="NY"
              >
            </div>
            <div class="form-group">
              <label for="shippingZip">ZIP/Postal Code *</label>
              <input 
                id="shippingZip"
                v-model="orderForm.shipping.zip"
                type="text"
                class="form-input"
                required
                placeholder="10001"
              >
            </div>
            <div class="form-group">
              <label for="shippingCountry">Country *</label>
              <select 
                id="shippingCountry"
                v-model="orderForm.shipping.country"
                class="form-input"
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
        <div class="form-section">
          <div class="section-header">
            <h2 class="section-title">Products</h2>
            <button type="button" @click="addProduct" class="btn btn-secondary">
              <svg class="icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
              </svg>
              Add Product
            </button>
          </div>
          
          <div class="products-table">
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
                      class="form-input"
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
                      class="form-input"
                      readonly
                    >
                  </td>
                  <td>
                    <input 
                      v-model.number="product.quantity"
                      type="number"
                      min="1"
                      class="form-input"
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
                      class="form-input"
                      required
                      @input="calculateTotals"
                    >
                  </td>
                  <td class="product-total">
                    ${% raw %}{{ (product.quantity * product.price).toFixed(2) }}{% endraw %}
                  </td>
                  <td>
                    <button 
                      type="button"
                      @click="removeProduct(index)"
                      class="btn-icon danger"
                      title="Remove"
                    >
                      <svg class="icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                      </svg>
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Order Summary -->
        <div class="form-section">
          <h2 class="section-title">Order Summary</h2>
          <div class="summary-grid">
            <div class="summary-row">
              <span class="summary-label">Subtotal:</span>
              <span class="summary-value">${% raw %}{{ orderSummary.subtotal.toFixed(2) }}{% endraw %}</span>
            </div>
            <div class="summary-row">
              <span class="summary-label">Tax ({% raw %}{{ orderSummary.taxRate }}{% endraw %}%):</span>
              <span class="summary-value">${% raw %}{{ orderSummary.tax.toFixed(2) }}{% endraw %}</span>
            </div>
            <div class="summary-row">
              <span class="summary-label">Shipping:</span>
              <span class="summary-value">${% raw %}{{ orderSummary.shipping.toFixed(2) }}{% endraw %}</span>
            </div>
            <div class="summary-row">
              <label for="discount" class="summary-label">Discount:</label>
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
            <div class="summary-row total">
              <span class="summary-label">Total:</span>
              <span class="summary-value">${% raw %}{{ orderSummary.total.toFixed(2) }}{% endraw %}</span>
            </div>
          </div>
        </div>

        <!-- Payment & Notes -->
        <div class="form-section">
          <h2 class="section-title">Payment & Notes</h2>
          <div class="form-grid">
            <div class="form-group">
              <label for="paymentMethod">Payment Method *</label>
              <select 
                id="paymentMethod"
                v-model="orderForm.payment.method"
                class="form-input"
                required
              >
                <option value="">Select Payment Method</option>
                <option value="credit_card">Credit Card</option>
                <option value="paypal">PayPal</option>
                <option value="bank_transfer">Bank Transfer</option>
                <option value="cash">Cash</option>
              </select>
            </div>
            <div class="form-group">
              <label for="paymentStatus">Payment Status *</label>
              <select 
                id="paymentStatus"
                v-model="orderForm.payment.status"
                class="form-input"
                required
              >
                <option value="pending">Pending</option>
                <option value="paid">Paid</option>
                <option value="partial">Partial</option>
              </select>
            </div>
            <div class="form-group full-width">
              <label for="orderNotes">Order Notes</label>
              <textarea 
                id="orderNotes"
                v-model="orderForm.notes"
                rows="4"
                class="form-input"
                placeholder="Add any special instructions or notes..."
              ></textarea>
            </div>
          </div>
        </div>
      </div>

      <!-- Form Actions -->
      <div class="form-actions">
        <router-link to="/dashboard/orders" class="btn btn-secondary">
          Cancel
        </router-link>
        <button type="submit" class="btn btn-primary" :disabled="loading">
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

<style scoped>
.new-order-view {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 2rem;
}

.header-left {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.back-link {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  color: #4299e1;
  font-size: 0.875rem;
  text-decoration: none;
  transition: color 0.2s;
}

.back-link:hover {
  color: #3182ce;
}

.page-title {
  font-size: 2rem;
  font-weight: 700;
  color: #1a202c;
  margin: 0;
}

.order-form {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.form-sections {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.form-section {
  background: white;
  padding: 1.5rem;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.section-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1a202c;
  margin: 0 0 1.5rem 0;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group.full-width {
  grid-column: span 2;
}

.form-group label {
  font-size: 0.875rem;
  font-weight: 500;
  color: #4a5568;
}

.form-input {
  padding: 0.5rem 0.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.375rem;
  font-size: 0.875rem;
}

.form-input:focus {
  outline: none;
  border-color: #4299e1;
  box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.1);
}

.form-input.small {
  width: 120px;
}

textarea.form-input {
  resize: vertical;
  min-height: 100px;
}

.btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
  text-decoration: none;
}

.btn-primary {
  background: #4299e1;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #3182ce;
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-secondary {
  background: #e2e8f0;
  color: #4a5568;
}

.btn-secondary:hover {
  background: #cbd5e0;
}

.icon {
  width: 20px;
  height: 20px;
}

.products-table {
  overflow-x: auto;
}

.products-table table {
  width: 100%;
  border-collapse: collapse;
}

.products-table th {
  text-align: left;
  padding: 0.75rem;
  background: #f7fafc;
  font-size: 0.75rem;
  font-weight: 600;
  color: #718096;
  text-transform: uppercase;
  border-bottom: 1px solid #e2e8f0;
}

.products-table td {
  padding: 0.75rem;
  border-bottom: 1px solid #f7fafc;
}

.products-table .form-input {
  width: 100%;
}

.product-total {
  font-weight: 600;
  color: #1a202c;
}

.btn-icon {
  padding: 0.25rem;
  border: none;
  background: transparent;
  color: #718096;
  cursor: pointer;
  border-radius: 0.25rem;
  transition: all 0.2s;
}

.btn-icon:hover {
  background: #f7fafc;
  color: #4a5568;
}

.btn-icon.danger:hover {
  background: #fee2e2;
  color: #991b1b;
}

.summary-grid {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  max-width: 400px;
  margin-left: auto;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.summary-row.total {
  padding-top: 0.75rem;
  border-top: 2px solid #e2e8f0;
  font-size: 1.125rem;
  font-weight: 600;
}

.summary-label {
  color: #4a5568;
}

.summary-value {
  color: #1a202c;
  font-weight: 500;
}

.summary-row.total .summary-value {
  color: #4299e1;
  font-weight: 700;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  padding-top: 1rem;
}

@media (max-width: 768px) {
  .new-order-view {
    padding: 1rem;
  }
  
  .form-grid {
    grid-template-columns: 1fr;
  }
  
  .form-group.full-width {
    grid-column: span 1;
  }
  
  .products-table {
    overflow-x: scroll;
  }
  
  .summary-grid {
    max-width: 100%;
  }
  
  .form-actions {
    flex-direction: column-reverse;
  }
  
  .btn {
    width: 100%;
    justify-content: center;
  }
}
</style>