<template>
  <div class="pricing-view">
    <!-- Hero Section -->
    <section class="bg-gradient-to-br from-emerald-500 to-teal-600 dark:from-emerald-600 dark:to-teal-700 text-white py-20 pb-32">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center max-w-4xl mx-auto">
          <h1 class="text-5xl font-bold mb-4">Simple, Transparent Pricing</h1>
          <p class="text-xl opacity-95">
            Choose the perfect plan for your needs. Always flexible to scale up or down.
          </p>
          <div class="mt-8 flex items-center justify-center gap-4">
            <span :class="[!isAnnual ? 'text-white font-semibold' : 'text-white/70']">Monthly</span>
            <label class="relative inline-block w-14 h-7">
              <input type="checkbox" v-model="isAnnual" class="sr-only peer">
              <span class="absolute cursor-pointer inset-0 bg-white/30 rounded-full transition-colors peer-checked:bg-white/50"></span>
              <span class="absolute left-1 top-1 w-5 h-5 bg-white rounded-full transition-transform peer-checked:translate-x-7"></span>
            </label>
            <span :class="[isAnnual ? 'text-white font-semibold' : 'text-white/70']">
              Annual
              <span class="ml-2 px-2 py-1 bg-green-100 text-green-800 dark:bg-green-900/50 dark:text-green-200 text-xs font-semibold rounded-full">Save 20%</span>
            </span>
          </div>
        </div>
      </div>
    </section>

    <!-- Pricing Cards -->
    <section class="py-0 pb-20 -mt-16">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8 max-w-6xl mx-auto">
          <div 
            v-for="plan in pricingPlans" 
            :key="plan.id"
            :class="[
              'relative bg-white dark:bg-gray-800 rounded-lg shadow-lg border transition-all duration-200',
              plan.featured 
                ? 'border-emerald-500 dark:border-emerald-400 ring-2 ring-emerald-500 dark:ring-emerald-400 shadow-xl transform scale-105' 
                : 'border-gray-200 dark:border-gray-700 hover:shadow-xl'
            ]"
          >
            <div v-if="plan.featured" class="absolute -top-4 left-1/2 transform -translate-x-1/2 bg-gradient-to-r from-emerald-500 to-teal-600 text-white px-6 py-1 rounded-full text-sm font-semibold shadow-lg">
              Most Popular
            </div>
            
            <div class="p-8">
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
                  <svg class="w-5 h-5 text-emerald-500 dark:text-emerald-400 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                  </svg>
                  {% raw %}{{ feature }}{% endraw %}
                </li>
              </ul>
              
              <button 
                @click="selectPlan(plan)"
                :class="[
                  'w-full px-6 py-3 rounded-lg font-medium transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2',
                  plan.featured 
                    ? 'bg-emerald-600 text-white hover:bg-emerald-700 focus:ring-emerald-500 dark:bg-emerald-500 dark:hover:bg-emerald-600 dark:focus:ring-emerald-400' 
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200 focus:ring-gray-500 dark:bg-gray-700 dark:text-gray-200 dark:hover:bg-gray-600 dark:focus:ring-gray-400'
                ]"
              >
                {% raw %}{{ plan.cta }}{% endraw %}
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Enterprise Section -->
    <section class="py-20 bg-gray-50 dark:bg-gray-900">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 overflow-hidden">
          <div class="p-8 lg:p-12 grid lg:grid-cols-3 gap-8 items-center">
            <div class="lg:col-span-2">
              <h2 class="text-3xl font-bold text-gray-900 dark:text-gray-100 mb-4">Need a Custom Solution?</h2>
              <p class="text-gray-600 dark:text-gray-400 mb-6 leading-relaxed">
                Our Enterprise plan offers unlimited flexibility with custom features, 
                dedicated support, and SLA guarantees tailored to your organization's needs.
              </p>
              <ul class="grid grid-cols-1 md:grid-cols-2 gap-3">
                <li class="flex items-center gap-2 text-gray-600 dark:text-gray-400">
                  <svg class="w-5 h-5 text-emerald-500 dark:text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                  </svg>
                  Custom pricing based on your needs
                </li>
                <li class="flex items-center gap-2 text-gray-600 dark:text-gray-400">
                  <svg class="w-5 h-5 text-emerald-500 dark:text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                  </svg>
                  Dedicated account manager
                </li>
                <li class="flex items-center gap-2 text-gray-600 dark:text-gray-400">
                  <svg class="w-5 h-5 text-emerald-500 dark:text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                  </svg>
                  99.9% uptime SLA
                </li>
                <li class="flex items-center gap-2 text-gray-600 dark:text-gray-400">
                  <svg class="w-5 h-5 text-emerald-500 dark:text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                  </svg>
                  Priority support & training
                </li>
              </ul>
            </div>
            <div class="text-center">
              <router-link 
                to="/contact" 
                class="inline-block bg-emerald-600 text-white hover:bg-emerald-700 dark:bg-emerald-500 dark:hover:bg-emerald-600 px-8 py-4 text-lg rounded-lg font-medium transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-emerald-500 dark:focus:ring-emerald-400"
              >
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
            class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 hover:shadow-lg transition-all duration-200 cursor-pointer mb-4"
            @click="toggleFaq(index)"
          >
            <div class="p-6 flex justify-between items-center">
              <h3 class="font-medium text-gray-900 dark:text-gray-100 pr-4">{% raw %}{{ faq.question }}{% endraw %}</h3>
              <svg :class="['w-5 h-5 text-gray-600 dark:text-gray-400 transition-transform flex-shrink-0', { 'rotate-180': activeFaq === index }]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
              </svg>
            </div>
            <div v-if="activeFaq === index" class="px-6 pb-6 text-gray-600 dark:text-gray-400 leading-relaxed border-t border-gray-200 dark:border-gray-700">
              <p class="pt-4">{% raw %}{{ faq.answer }}{% endraw %}</p>
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
            <svg class="w-10 h-10 text-emerald-600 dark:text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
            </svg>
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

