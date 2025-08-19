<template>
  <div class="contact-view">
    <!-- Hero Section -->
    <section class="bg-gradient-to-br from-emerald-500 to-teal-600 dark:from-emerald-600 dark:to-teal-700 text-white py-20">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center max-w-4xl mx-auto">
          <h1 class="text-5xl font-bold mb-4">Get in Touch</h1>
          <p class="text-xl opacity-95">
            We'd love to hear from you. Send us a message and we'll respond as soon as possible.
          </p>
        </div>
      </div>
    </section>

    <!-- Contact Content -->
    <section class="py-20 bg-white dark:bg-gray-900">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-12">
          <!-- Contact Form -->
          <div class="card">
            <div class="card-body">
              <h2 class="text-2xl font-semibold text-gray-900 mb-6 dark:text-gray-100">Send us a Message</h2>
              <form @submit.prevent="handleSubmit" class="space-y-6">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div class="mb-6">
                  <label for="firstName">First Name</label>
                  <input 
                    id="firstName"
                    v-model="form.firstName"
                    type="text"
                    class="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500 dark:focus:ring-emerald-400 focus:border-emerald-600 dark:focus:border-emerald-400 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 dark:bg-gray-900"
                    required
                  >
                </div>
                <div class="mb-6">
                  <label for="lastName">Last Name</label>
                  <input 
                    id="lastName"
                    v-model="form.lastName"
                    type="text"
                    class="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500 dark:focus:ring-emerald-400 focus:border-emerald-600 dark:focus:border-emerald-400 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 dark:bg-gray-900"
                    required
                  >
                </div>
              </div>
              
              <div class="mb-6">
                <label for="email">Email</label>
                <input 
                  id="email"
                  v-model="form.email"
                  type="email"
                  class="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500 dark:focus:ring-emerald-400 focus:border-emerald-600 dark:focus:border-emerald-400 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 dark:bg-gray-900"
                  required
                >
              </div>
              
              <div class="mb-6">
                <label for="company">Company (Optional)</label>
                <input 
                  id="company"
                  v-model="form.company"
                  type="text"
                  class="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500 dark:focus:ring-emerald-400 focus:border-emerald-600 dark:focus:border-emerald-400 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 dark:bg-gray-900"
                >
              </div>
              
              <div class="mb-6">
                <label for="subject">Subject</label>
                <select 
                  id="subject"
                  v-model="form.subject"
                  class="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500 dark:focus:ring-emerald-400 focus:border-emerald-600 dark:focus:border-emerald-400 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 dark:bg-gray-900"
                  required
                >
                  <option value="">Select a subject</option>
                  <option value="general">General Inquiry</option>
                  <option value="support">Technical Support</option>
                  <option value="sales">Sales Question</option>
                  <option value="partnership">Partnership Opportunity</option>
                  <option value="feedback">Feedback</option>
                </select>
              </div>
              
              <div class="mb-6">
                <label for="message">Message</label>
                <textarea 
                  id="message"
                  v-model="form.message"
                  rows="6"
                  class="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500 dark:focus:ring-emerald-400 focus:border-emerald-600 dark:focus:border-emerald-400 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 dark:bg-gray-900"
                  required
                ></textarea>
              </div>
              
              <div class="mb-6">
                <label class="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400">
                  <input 
                    v-model="form.subscribe"
                    type="checkbox"
                    class="w-4 h-4 text-emerald-600 border-gray-300 rounded focus:ring-emerald-500 dark:border-gray-600 dark:focus:ring-emerald-400"
                  >
                  <span>I'd like to receive updates and newsletters</span>
                </label>
              </div>
              
              <button type="submit" class="btn bg-emerald-600 text-white hover:bg-emerald-700 px-8 py-4 text-lg rounded-lg font-medium transition-all duration-200" :disabled="isSubmitting">
                <span v-if="!isSubmitting">Send Message</span>
                <span v-else>Sending...</span>
              </button>
              
              <div v-if="submitMessage" :class="['mt-4 p-3 rounded-lg text-sm', submitStatus === 'success' ? 'bg-green-50 text-green-800 border border-green-200 dark:bg-green-900/20 dark:text-green-400 dark:border-green-800' : 'bg-red-50 text-red-800 border border-red-200 dark:bg-red-900/20 dark:text-red-400 dark:border-red-800']">
                {% raw %}{{ submitMessage }}{% endraw %}
              </div>
              </form>
            </div>
          </div>
          
          <!-- Contact Information -->
          <div class="space-y-8">
            <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 p-6">
              <h3 class="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-4">Contact Information</h3>
              <p class="text-gray-600 dark:text-gray-400 mb-6">
                Feel free to reach out through any of these channels:
              </p>
              
              <div class="space-y-4">
                <div class="flex items-start gap-3">
                  <svg class="w-5 h-5 text-emerald-600 dark:text-emerald-400 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                  </svg>
                  <div>
                    <div class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">Email</div>
                    <a href="mailto:hello@{{ cookiecutter.domain_name }}" class="text-gray-900 dark:text-gray-100 hover:text-emerald-600 dark:hover:text-emerald-400 transition-colors">
                      hello@{{ cookiecutter.domain_name }}
                    </a>
                  </div>
                </div>
                
                <div class="flex items-start gap-3">
                  <svg class="w-5 h-5 text-emerald-600 dark:text-emerald-400 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                  </svg>
                  <div>
                    <div class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">Phone</div>
                    <a href="tel:+1234567890" class="text-gray-900 dark:text-gray-100 hover:text-emerald-600 dark:hover:text-emerald-400 transition-colors">
                      +1 (234) 567-890
                    </a>
                  </div>
                </div>
                
                <div class="flex items-start gap-3">
                  <svg class="w-5 h-5 text-emerald-600 dark:text-emerald-400 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                  <div>
                    <div class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">Office</div>
                    <div class="text-gray-900 dark:text-gray-100">
                      123 Business Ave<br>
                      Suite 100<br>
                      San Francisco, CA 94107
                    </div>
                  </div>
                </div>
                
                <div class="flex items-start gap-3">
                  <svg class="w-5 h-5 text-emerald-600 dark:text-emerald-400 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <div>
                    <div class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">Business Hours</div>
                    <div class="text-gray-900 dark:text-gray-100">
                      Monday - Friday: 9:00 AM - 6:00 PM<br>
                      Saturday: 10:00 AM - 4:00 PM<br>
                      Sunday: Closed
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Social Media Card -->
            <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 p-6">
              <h4 class="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-4">Follow Us</h4>
              <div class="flex gap-4">
                <a href="#" class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors" title="Twitter">
                  <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M23 3a10.9 10.9 0 01-3.14 1.53 4.48 4.48 0 00-7.86 3v1A10.66 10.66 0 013 4s-4 9 5 13a11.64 11.64 0 01-7 2c9 5 20 0 20-11.5a4.5 4.5 0 00-.08-.83A7.72 7.72 0 0023 3z"></path>
                  </svg>
                </a>
                <a href="#" class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors" title="LinkedIn">
                  <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M16 8a6 6 0 016 6v7h-4v-7a2 2 0 00-2-2 2 2 0 00-2 2v7h-4v-7a6 6 0 016-6zM2 9h4v12H2z M4 6a2 2 0 100-4 2 2 0 000 4z"></path>
                  </svg>
                </a>
                <a href="#" class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors" title="GitHub">
                  <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"></path>
                  </svg>
                </a>
              </div>
            </div>
            
            <!-- FAQ Card -->
            <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 p-6">
              <h3 class="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-4">Frequently Asked Questions</h3>
              <div class="space-y-3">
                <div class="pb-3 border-b border-gray-200 dark:border-gray-700">
                  <h4 class="font-medium text-gray-900 dark:text-gray-100 mb-1">What is your response time?</h4>
                  <p class="text-sm text-gray-600 dark:text-gray-400">We typically respond within 24 hours during business days.</p>
                </div>
                <div class="pb-3 border-b border-gray-200 dark:border-gray-700">
                  <h4 class="font-medium text-gray-900 dark:text-gray-100 mb-1">Do you offer phone support?</h4>
                  <p class="text-sm text-gray-600 dark:text-gray-400">Yes, phone support is available for enterprise customers.</p>
                </div>
                <div>
                  <h4 class="font-medium text-gray-900 dark:text-gray-100 mb-1">Can I schedule a demo?</h4>
                  <p class="text-sm text-gray-600 dark:text-gray-400">Absolutely! Select "Sales Question" in the form and mention you'd like a demo.</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Map Section -->
    <section class="relative h-96 bg-gradient-to-br from-emerald-500 to-teal-600 dark:from-emerald-600 dark:to-teal-700">
      <div class="absolute inset-0 flex items-center justify-center">
        <div class="text-center text-white">
          <svg class="w-12 h-12 mb-4 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
          <h3 class="text-2xl font-bold mb-3">Visit Our Office</h3>
          <p class="mb-6">123 Business Ave, Suite 100<br>San Francisco, CA 94107</p>
          <a href="#" class="inline-block bg-white text-emerald-600 hover:bg-gray-100 px-6 py-3 rounded-lg font-medium transition-all duration-200">
            Get Directions
          </a>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup{% if cookiecutter.use_typescript == 'y' %} lang="ts"{% endif %}>
import { ref, reactive } from 'vue'

{% if cookiecutter.use_typescript == 'y' -%}
interface ContactForm {
  firstName: string
  lastName: string
  email: string
  company: string
  subject: string
  message: string
  subscribe: boolean
}
{%- endif %}

const form = reactive({% if cookiecutter.use_typescript == 'y' %}<ContactForm>{% endif %}{
  firstName: '',
  lastName: '',
  email: '',
  company: '',
  subject: '',
  message: '',
  subscribe: false
})

const isSubmitting = ref(false)
const submitMessage = ref('')
const submitStatus = ref('')

const handleSubmit = async () => {
  isSubmitting.value = true
  submitMessage.value = ''
  
  try {
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    // Reset form
    Object.keys(form).forEach(key => {
      if (key === 'subscribe') {
        form[key] = false
      } else {
        form[key] = ''
      }
    })
    
    submitMessage.value = 'Thank you for your message! We\'ll get back to you soon.'
    submitStatus.value = 'success'
  } catch (error) {
    submitMessage.value = 'Something went wrong. Please try again later.'
    submitStatus.value = 'error'
  } finally {
    isSubmitting.value = false
    
    // Clear message after 5 seconds
    setTimeout(() => {
      submitMessage.value = ''
      submitStatus.value = ''
    }, 5000)
  }
}
</script>

