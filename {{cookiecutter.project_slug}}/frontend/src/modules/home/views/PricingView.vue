<template>
  <div class="pricing-view">
    <!-- Hero Section -->
    <section class="bg-gradient-to-br from-indigo-500 to-purple-600 text-white py-20">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center max-w-4xl mx-auto">
          <h1 class="text-5xl font-bold mb-4">Simple, Transparent Pricing</h1>
          <p class="text-xl opacity-95">
            Choose the perfect plan for your needs. Always flexible to scale up or down.
          </p>
          <div class="mt-8 flex items-center justify-center gap-4">
            <span :class="[!isAnnual ? 'text-gray-900 dark:text-gray-100 font-semibold' : 'text-gray-500 dark:text-gray-400']">Monthly</span>
            <label class="relative inline-block w-14 h-7">
              <input type="checkbox" v-model="isAnnual" class="sr-only peer">
              <span class="absolute cursor-pointer inset-0 bg-gray-300 rounded-full transition-colors peer-checked:bg-emerald-600 dark:bg-gray-600"></span>
            </label>
            <span :class="[isAnnual ? 'text-gray-900 dark:text-gray-100 font-semibold' : 'text-gray-500 dark:text-gray-400']">
              Annual
              <span class="ml-2 px-2 py-1 bg-green-100 text-green-800 text-xs font-semibold rounded-full">Save 20%</span>
            </span>
          </div>
        </div>
      </div>
    </section>

    <!-- Pricing Cards -->
    <section class="py-0 pb-20 -mt-12">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8 max-w-6xl mx-auto">
          <div 
            v-for="plan in pricingPlans" 
            :key="plan.id"
            :class="['card relative', { 'ring-2 ring-emerald-500 shadow-xl': plan.featured }]"
          >
            <div v-if="plan.featured" class="absolute -top-px left-1/2 transform -translate-x-1/2 bg-gradient-to-r from-emerald-500 to-teal-600 text-white px-6 py-1 rounded-b-lg text-sm font-semibold">Most Popular</div>
            
            <div class="card-body">
              <div class="text-center mb-8">
              <h3 class="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-2">{% raw %}{{ plan.name }}{% endraw %}</h3>
              <p class="text-gray-600 dark:text-gray-400 text-sm">{% raw %}{{ plan.description }}{% endraw %}</p>
            </div>
            
            <div class="text-center mb-2">
              <span class="text-2xl text-gray-600 dark:text-gray-400 align-top">$</span>
              <span class="text-6xl font-bold text-gray-900 dark:text-gray-100">{% raw %}{{ isAnnual ? plan.annualPrice : plan.monthlyPrice }}{% endraw %}</span>
              <span class="text-lg text-gray-600 dark:text-gray-400">/{% raw %}{{ isAnnual ? 'year' : 'month' }}{% endraw %}</span>
            </div>
            
            <div v-if="isAnnual && plan.monthlyPrice > 0" class="text-center text-green-600 dark:text-green-400 text-sm font-semibold mb-8">
              Save {% raw %}{{ '$' + (plan.monthlyPrice * 12 - plan.annualPrice).toFixed(0) }}{% endraw %} per year
            </div>
            
            <ul class="space-y-3 mb-8">
              <li v-for="feature in plan.features" :key="feature" class="flex items-start gap-3 text-gray-600 dark:text-gray-400">
                <IconLucideCheck class="w-5 h-5 text-green-500 flex-shrink-0 mt-0.5" />
                {% raw %}{{ feature }}{% endraw %}
              </li>
            </ul>
            
            <button 
              @click="selectPlan(plan)"
              :class="['btn w-full', plan.featured ? 'btn-primary' : 'btn-secondary']"
            >
              {% raw %}{{ plan.cta }}{% endraw %}
            </button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Enterprise Section -->
    <section class="py-20 bg-gray-50 dark:bg-gray-800">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="card">
          <div class="card-body grid lg:grid-cols-3 gap-8 items-center">
            <div class="lg:col-span-2">
            <h2 class="text-3xl font-bold text-gray-900 dark:text-gray-100 mb-4">Need a Custom Solution?</h2>
            <p class="text-gray-600 dark:text-gray-400 mb-6 leading-relaxed">
              Our Enterprise plan offers unlimited flexibility with custom features, 
              dedicated support, and SLA guarantees tailored to your organization's needs.
            </p>
            <ul class="grid grid-cols-1 md:grid-cols-2 gap-3 text-gray-600 dark:text-gray-400">
              <li>Custom pricing based on your needs</li>
              <li>Dedicated account manager</li>
              <li>99.9% uptime SLA</li>
              <li>Priority support & training</li>
            </ul>
            </div>
            <div class="text-center">
            <router-link to="/contact" class="btn bg-emerald-600 text-white hover:bg-emerald-700 px-8 py-4 text-lg rounded-lg font-medium transition-all duration-200">
              Contact Sales
            </router-link>
            <p class="mt-3 text-gray-600 dark:text-gray-400 text-sm">Let's discuss your specific requirements</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- FAQ Section -->
    <section class="py-20 bg-white dark:bg-gray-900">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-12">
          <h2 class="text-3xl font-bold text-gray-900 mb-4 dark:text-gray-100">Frequently Asked Questions</h2>
          <p class="text-lg text-gray-600 dark:text-gray-400">Everything you need to know about our pricing</p>
        </div>
        
        <div class="max-w-3xl mx-auto">
          <div 
            v-for="(faq, index) in faqs" 
            :key="index"
            class="card hover-lift cursor-pointer mb-4"
            @click="toggleFaq(index)"
          >
            <div class="card-body flex justify-between items-center">
              <h3 class="font-medium text-gray-900 dark:text-gray-100">{% raw %}{{ faq.question }}{% endraw %}</h3>
              <IconLucideChevronDown :class="['w-5 h-5 text-gray-600 dark:text-gray-400 transition-transform', { 'rotate-180': activeFaq === index }]" />
            </div>
            <div v-if="activeFaq === index" class="px-6 pb-6 text-gray-600 dark:text-gray-400 leading-relaxed border-t border-gray-200 dark:border-gray-700 mt-4 pt-4">
              <p>{% raw %}{{ faq.answer }}{% endraw %}</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Guarantee Section -->
    <section class="py-20 bg-gradient-to-br from-green-50 to-green-100 dark:from-green-900/20 dark:to-green-800/20">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center max-w-2xl mx-auto">
          <div class="w-20 h-20 mx-auto mb-6 bg-white dark:bg-gray-800 rounded-full flex items-center justify-center shadow-lg">
            <IconLucideShieldCheck class="w-10 h-10 text-emerald-600 dark:text-emerald-400" />
          </div>
          <h2 class="text-3xl font-bold text-gray-900 dark:text-gray-100 mb-4">30-Day Money-Back Guarantee</h2>
          <p class="text-gray-600 dark:text-gray-400 text-lg leading-relaxed">
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

