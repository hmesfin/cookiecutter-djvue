<template>
  <div class="pricing-view">
    <!-- Hero Section -->
    <section class="hero-section">
      <div class="container">
        <div class="hero-content">
          <h1 class="hero-title">Simple, Transparent Pricing</h1>
          <p class="hero-description">
            Choose the perfect plan for your needs. Always flexible to scale up or down.
          </p>
          <div class="billing-toggle">
            <span :class="{ active: !isAnnual }">Monthly</span>
            <label class="toggle">
              <input type="checkbox" v-model="isAnnual">
              <span class="toggle-slider"></span>
            </label>
            <span :class="{ active: isAnnual }">
              Annual
              <span class="badge">Save 20%</span>
            </span>
          </div>
        </div>
      </div>
    </section>

    <!-- Pricing Cards -->
    <section class="pricing-section">
      <div class="container">
        <div class="pricing-grid">
          <div 
            v-for="plan in pricingPlans" 
            :key="plan.id"
            :class="['pricing-bg-white rounded-lg shadow-md p-6', { featured: plan.featured }]"
          >
            <div v-if="plan.featured" class="featured-badge">Most Popular</div>
            
            <div class="plan-header">
              <h3 class="plan-name">{% raw %}{{ plan.name }}{% endraw %}</h3>
              <p class="plan-description">{% raw %}{{ plan.description }}{% endraw %}</p>
            </div>
            
            <div class="plan-price">
              <span class="currency">$</span>
              <span class="amount">{% raw %}{{ isAnnual ? plan.annualPrice : plan.monthlyPrice }}{% endraw %}</span>
              <span class="period">/{% raw %}{{ isAnnual ? 'year' : 'month' }}{% endraw %}</span>
            </div>
            
            <div v-if="isAnnual && plan.monthlyPrice > 0" class="savings">
              Save {% raw %}{{ '$' + (plan.monthlyPrice * 12 - plan.annualPrice).toFixed(0) }}{% endraw %} per year
            </div>
            
            <ul class="features-list">
              <li v-for="feature in plan.features" :key="feature" class="feature-item">
                <IconLucideCheck class="check-icon" />
                {% raw %}{{ feature }}{% endraw %}
              </li>
            </ul>
            
            <button 
              @click="selectPlan(plan)"
              :class="['btn', plan.featured ? 'btn-primary' : 'btn-outline']"
            >
              {% raw %}{{ plan.cta }}{% endraw %}
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- Enterprise Section -->
    <section class="enterprise-section">
      <div class="container">
        <div class="enterprise-bg-white rounded-lg shadow-md p-6">
          <div class="enterprise-content">
            <h2 class="enterprise-title">Need a Custom Solution?</h2>
            <p class="enterprise-description">
              Our Enterprise plan offers unlimited flexibility with custom features, 
              dedicated support, and SLA guarantees tailored to your organization's needs.
            </p>
            <ul class="enterprise-features">
              <li>Custom pricing based on your needs</li>
              <li>Dedicated account manager</li>
              <li>99.9% uptime SLA</li>
              <li>Priority support & training</li>
            </ul>
          </div>
          <div class="enterprise-action">
            <router-link to="/contact" class="btn btn-primary btn-lg">
              Contact Sales
            </router-link>
            <p class="enterprise-note">Let's discuss your specific requirements</p>
          </div>
        </div>
      </div>
    </section>

    <!-- FAQ Section -->
    <section class="faq-section">
      <div class="container">
        <div class="mb-6">
          <h2 class="text-xl font-semibold text-gray-900 mb-2">Frequently Asked Questions</h2>
        </div>
        
        <div class="faq-grid">
          <div 
            v-for="(faq, index) in faqs" 
            :key="index"
            class="faq-item"
            @click="toggleFaq(index)"
          >
            <div class="faq-question">
              <h3>{% raw %}{{ faq.question }}{% endraw %}</h3>
              <IconLucideChevronDown class="['chevron-icon', { rotated: activeFaq === index }]" />
            </div>
            <div v-if="activeFaq === index" class="faq-answer">
              <p>{% raw %}{{ faq.answer }}{% endraw %}</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Guarantee Section -->
    <section class="guarantee-section">
      <div class="container">
        <div class="guarantee-content">
          <div class="guarantee-icon">
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path>
            </svg>
          </div>
          <h2 class="guarantee-title">30-Day Money-Back Guarantee</h2>
          <p class="guarantee-description">
            Try any plan risk-free for 30 days. If you're not completely satisfied, 
            we'll refund your payment—no questions asked.
          </p>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup{% if cookiecutter.use_typescript == 'y' %} lang="ts"{% endif %}>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

{% if cookiecutter.use_typescript == 'y' -%}
interface PricingPlan {
  id: string
  name: string
  description: string
  monthlyPrice: number
  annualPrice: number
  features: string[]
  featured: boolean
  cta: string
}

interface FAQ {
  question: string
  answer: string
}
{%- endif %}

const router = useRouter()
const isAnnual = ref(false)
const activeFaq = ref({% if cookiecutter.use_typescript == 'y' %}<number | null>{% endif %}null)

const pricingPlans = ref({% if cookiecutter.use_typescript == 'y' %}<PricingPlan[]>{% endif %}[
  {
    id: 'starter',
    name: 'Starter',
    description: 'Perfect for individuals and small projects',
    monthlyPrice: 0,
    annualPrice: 0,
    features: [
      'Up to 3 users',
      '5 projects',
      '2GB storage',
      'Basic support',
      'Core features',
      'Mobile app access'
    ],
    featured: false,
    cta: 'Start Free'
  },
  {
    id: 'professional',
    name: 'Professional',
    description: 'Ideal for growing teams and businesses',
    monthlyPrice: 29,
    annualPrice: 278,
    features: [
      'Up to 20 users',
      'Unlimited projects',
      '100GB storage',
      'Priority support',
      'Advanced features',
      'API access',
      'Custom integrations',
      'Analytics dashboard'
    ],
    featured: true,
    cta: 'Start Free Trial'
  },
  {
    id: 'business',
    name: 'Business',
    description: 'For larger teams with advanced needs',
    monthlyPrice: 99,
    annualPrice: 950,
    features: [
      'Up to 100 users',
      'Unlimited everything',
      '1TB storage',
      '24/7 phone support',
      'All features',
      'Advanced security',
      'Custom workflows',
      'Dedicated account manager',
      'SLA guarantee'
    ],
    featured: false,
    cta: 'Start Free Trial'
  }
])

const faqs = ref({% if cookiecutter.use_typescript == 'y' %}<FAQ[]>{% endif %}[
  {
    question: 'Can I change my plan later?',
    answer: 'Yes! You can upgrade or downgrade your plan at any time. Changes take effect immediately, and we\'ll prorate any difference in price.'
  },
  {
    question: 'What payment methods do you accept?',
    answer: 'We accept all major credit cards (Visa, MasterCard, American Express), PayPal, and wire transfers for annual plans.'
  },
  {
    question: 'Is there a setup fee?',
    answer: 'No, there are no setup fees or hidden charges. You only pay the subscription price shown above.'
  },
  {
    question: 'Can I cancel my subscription?',
    answer: 'Yes, you can cancel your subscription at any time. You\'ll continue to have access until the end of your current billing period.'
  },
  {
    question: 'Do you offer discounts for non-profits?',
    answer: 'Yes! We offer a 50% discount for registered non-profit organizations. Contact our sales team with your proof of non-profit status.'
  },
  {
    question: 'What happens to my data if I cancel?',
    answer: 'Your data remains available for download for 30 days after cancellation. After that, it\'s permanently deleted from our servers.'
  }
])

const selectPlan = (plan{% if cookiecutter.use_typescript == 'y' %}: PricingPlan{% endif %}) => {
  if (plan.monthlyPrice === 0) {
    router.push('/auth/register')
  } else {
    router.push({
      path: '/auth/register',
      query: { plan: plan.id, billing: isAnnual.value ? 'annual' : 'monthly' }
    })
  }
}

const toggleFaq = (index{% if cookiecutter.use_typescript == 'y' %}: number{% endif %}) => {
  activeFaq.value = activeFaq.value === index ? null : index
}
</script>

<style scoped>
.pricing-view {
  min-height: 100vh;
}

/* Hero Section */
.hero-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 5rem 0 3rem;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1.5rem;
}

.hero-content {
  text-align: center;
  max-width: 600px;
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
  margin-bottom: 2rem;
}

/* Billing Toggle */
.billing-toggle {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  font-size: 1rem;
}

.billing-toggle span {
  color: rgba(255, 255, 255, 0.7);
  transition: color 0.3s;
}

.billing-toggle span.active {
  color: white;
  font-weight: 600;
}

.toggle {
  position: relative;
  display: inline-block;
  width: 60px;
  height: 30px;
}

.toggle input {
  opacity: 0;
  width: 0;
  height: 0;
}

.toggle-slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(255, 255, 255, 0.3);
  transition: 0.4s;
  border-radius: 30px;
}

.toggle-slider:before {
  position: absolute;
  content: "";
  height: 22px;
  width: 22px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  transition: 0.4s;
  border-radius: 50%;
}

.toggle input:checked + .toggle-slider {
  background-color: rgba(255, 255, 255, 0.5);
}

.toggle input:checked + .toggle-slider:before {
  transform: translateX(30px);
}

.badge {
  background: #48bb78;
  color: white;
  padding: 0.125rem 0.5rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 600;
  margin-left: 0.5rem;
}

/* Pricing Section */
.pricing-section {
  padding: 0 0 5rem;
  margin-top: -3rem;
}

.pricing-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 2rem;
  max-width: 1100px;
  margin: 0 auto;
}

.pricing-card {
  background: white;
  border-radius: 1rem;
  padding: 2.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
  position: relative;
  transition: transform 0.3s, box-shadow 0.3s;
}

.pricing-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
}

.pricing-card.featured {
  border: 2px solid #667eea;
  transform: scale(1.05);
}

.featured-badge {
  position: absolute;
  top: -1px;
  left: 50%;
  transform: translateX(-50%);
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 0.375rem 1.5rem;
  border-radius: 0 0 0.5rem 0.5rem;
  font-size: 0.875rem;
  font-weight: 600;
}

.plan-header {
  text-align: center;
  margin-bottom: 2rem;
}

.plan-name {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1a202c;
  margin: 0 0 0.5rem 0;
}

.plan-description {
  color: #718096;
  font-size: 0.875rem;
}

.plan-price {
  text-align: center;
  margin-bottom: 0.5rem;
}

.currency {
  font-size: 1.5rem;
  color: #718096;
  vertical-align: top;
}

.amount {
  font-size: 3.5rem;
  font-weight: 700;
  color: #1a202c;
}

.period {
  font-size: 1.125rem;
  color: #718096;
}

.savings {
  text-align: center;
  color: #48bb78;
  font-size: 0.875rem;
  font-weight: 600;
  margin-bottom: 2rem;
}

.features-list {
  list-style: none;
  padding: 0;
  margin: 0 0 2rem 0;
}

.feature-item {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  margin-bottom: 1rem;
  color: #4a5568;
}

.check-icon {
  width: 20px;
  height: 20px;
  color: #48bb78;
  flex-shrink: 0;
  margin-top: 0.125rem;
}

.btn {
  width: 100%;
  padding: 0.875rem;
  border-radius: 0.5rem;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s;
  border: 2px solid transparent;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(102, 126, 234, 0.4);
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

/* Enterprise Section */
.enterprise-section {
  padding: 5rem 0;
  background: #f7fafc;
}

.enterprise-card {
  background: white;
  border-radius: 1rem;
  padding: 3rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 3rem;
  align-items: center;
}

.enterprise-title {
  font-size: 2rem;
  font-weight: 700;
  color: #1a202c;
  margin: 0 0 1rem 0;
}

.enterprise-description {
  color: #718096;
  margin-bottom: 1.5rem;
  line-height: 1.6;
}

.enterprise-features {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

.enterprise-features li {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #4a5568;
}

.enterprise-features li:before {
  content: '✓';
  color: #48bb78;
  font-weight: bold;
}

.enterprise-action {
  text-align: center;
}

.btn-lg {
  padding: 1rem 2.5rem;
  font-size: 1.125rem;
}

.enterprise-note {
  margin-top: 1rem;
  color: #718096;
  font-size: 0.875rem;
}

/* FAQ Section */
.faq-section {
  padding: 5rem 0;
  background: white;
}

.section-header {
  text-align: center;
  margin-bottom: 3rem;
}

.section-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #1a202c;
  margin: 0;
}

.faq-grid {
  max-width: 800px;
  margin: 0 auto;
}

.faq-item {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  margin-bottom: 1rem;
  overflow: hidden;
  transition: box-shadow 0.3s;
}

.faq-item:hover {
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
}

.faq-question {
  padding: 1.25rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
}

.faq-question h3 {
  margin: 0;
  font-size: 1.125rem;
  font-weight: 600;
  color: #1a202c;
}

.chevron-icon {
  width: 20px;
  height: 20px;
  color: #718096;
  transition: transform 0.3s;
}

.chevron-icon.rotated {
  transform: rotate(180deg);
}

.faq-answer {
  padding: 0 1.25rem 1.25rem;
  color: #718096;
  line-height: 1.6;
}

/* Guarantee Section */
.guarantee-section {
  padding: 5rem 0;
  background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
}

.guarantee-content {
  text-align: center;
  max-width: 600px;
  margin: 0 auto;
}

.guarantee-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto 1.5rem;
  background: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
}

.guarantee-icon svg {
  width: 40px;
  height: 40px;
  color: #48bb78;
}

.guarantee-title {
  font-size: 2rem;
  font-weight: 700;
  color: #1a202c;
  margin: 0 0 1rem 0;
}

.guarantee-description {
  color: #4a5568;
  font-size: 1.125rem;
  line-height: 1.6;
}

/* Responsive */
@media (max-width: 1024px) {
  .pricing-grid {
    grid-template-columns: 1fr;
    max-width: 400px;
  }
  
  .pricing-card.featured {
    transform: scale(1);
  }
  
  .enterprise-card {
    grid-template-columns: 1fr;
    text-align: center;
  }
  
  .enterprise-features {
    grid-template-columns: 1fr;
    text-align: left;
    max-width: 400px;
    margin: 0 auto;
  }
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 2rem;
  }
  
  .section-title {
    font-size: 1.75rem;
  }
  
  .amount {
    font-size: 2.5rem;
  }
}
</style>