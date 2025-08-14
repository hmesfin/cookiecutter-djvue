<template>
  <div class="contact-view">
    <!-- Hero Section -->
    <section class="hero-section">
      <div class="container">
        <div class="hero-content">
          <h1 class="hero-title">Get in Touch</h1>
          <p class="hero-description">
            We'd love to hear from you. Send us a message and we'll respond as soon as possible.
          </p>
        </div>
      </div>
    </section>

    <!-- Contact Content -->
    <section class="contact-section">
      <div class="container">
        <div class="contact-grid">
          <!-- Contact Form -->
          <div class="contact-form-bg-white rounded-lg shadow-md p-6">
            <h2 class="text-xl font-semibold text-gray-900 mb-2">Send us a Message</h2>
            <form @submit.prevent="handleSubmit" class="contact-form">
              <div class="form-row">
                <div class="mb-6">
                  <label for="firstName">First Name</label>
                  <input 
                    id="firstName"
                    v-model="form.firstName"
                    type="text"
                    class="form-input"
                    required
                  >
                </div>
                <div class="mb-6">
                  <label for="lastName">Last Name</label>
                  <input 
                    id="lastName"
                    v-model="form.lastName"
                    type="text"
                    class="form-input"
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
                  class="form-input"
                  required
                >
              </div>
              
              <div class="mb-6">
                <label for="company">Company (Optional)</label>
                <input 
                  id="company"
                  v-model="form.company"
                  type="text"
                  class="form-input"
                >
              </div>
              
              <div class="mb-6">
                <label for="subject">Subject</label>
                <select 
                  id="subject"
                  v-model="form.subject"
                  class="form-input"
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
                  class="form-input"
                  required
                ></textarea>
              </div>
              
              <div class="mb-6">
                <label class="checkbox-label">
                  <input 
                    v-model="form.subscribe"
                    type="checkbox"
                    class="checkbox-input"
                  >
                  <span>I'd like to receive updates and newsletters</span>
                </label>
              </div>
              
              <button type="submit" class="btn btn-primary btn-lg" :disabled="isSubmitting">
                <span v-if="!isSubmitting">Send Message</span>
                <span v-else>Sending...</span>
              </button>
              
              <div v-if="submitMessage" :class="['submit-message', submitStatus]">
                {% raw %}{{ submitMessage }}{% endraw %}
              </div>
            </form>
          </div>
          
          <!-- Contact Information -->
          <div class="contact-info">
            <div class="info-bg-white rounded-lg shadow-md p-6">
              <h3 class="info-title">Contact Information</h3>
              <p class="info-description">
                Feel free to reach out through any of these channels:
              </p>
              
              <div class="info-items">
                <div class="info-item">
                  <div class="info-icon">
                    <IconLucideMail class="w-5 h-5" />
                  </div>
                  <div>
                    <div class="info-label">Email</div>
                    <a href="mailto:hello@{{ cookiecutter.domain_name }}" class="info-value">
                      hello@{{ cookiecutter.domain_name }}
                    </a>
                  </div>
                </div>
                
                <div class="info-item">
                  <div class="info-icon">
                    <IconLucidePhone class="w-6 h-6" />
                  </div>
                  <div>
                    <div class="info-label">Phone</div>
                    <a href="tel:+1234567890" class="info-value">
                      +1 (234) 567-890
                    </a>
                  </div>
                </div>
                
                <div class="info-item">
                  <div class="info-icon">
                    <IconLucideMapPin class="w-6 h-6" />
                  </div>
                  <div>
                    <div class="info-label">Office</div>
                    <div class="info-value">
                      123 Business Ave<br>
                      Suite 100<br>
                      San Francisco, CA 94107
                    </div>
                  </div>
                </div>
                
                <div class="info-item">
                  <div class="info-icon">
                    <IconLucideClock class="w-5 h-5" />
                  </div>
                  <div>
                    <div class="info-label">Business Hours</div>
                    <div class="info-value">
                      Monday - Friday: 9:00 AM - 6:00 PM<br>
                      Saturday: 10:00 AM - 4:00 PM<br>
                      Sunday: Closed
                    </div>
                  </div>
                </div>
              </div>
              
              <div class="social-section">
                <h4 class="social-title">Follow Us</h4>
                <div class="social-links">
                  <a href="#" class="social-link" title="Twitter">
                    <svg fill="currentColor" viewBox="0 0 24 24">
                      <path d="M23 3a10.9 10.9 0 01-3.14 1.53 4.48 4.48 0 00-7.86 3v1A10.66 10.66 0 013 4s-4 9 5 13a11.64 11.64 0 01-7 2c9 5 20 0 20-11.5a4.5 4.5 0 00-.08-.83A7.72 7.72 0 0023 3z"></path>
                    </svg>
                  </a>
                  <a href="#" class="social-link" title="LinkedIn">
                    <svg fill="currentColor" viewBox="0 0 24 24">
                      <path d="M16 8a6 6 0 016 6v7h-4v-7a2 2 0 00-2-2 2 2 0 00-2 2v7h-4v-7a6 6 0 016-6zM2 9h4v12H2z M4 6a2 2 0 100-4 2 2 0 000 4z"></path>
                    </svg>
                  </a>
                  <a href="#" class="social-link" title="GitHub">
                    <svg fill="currentColor" viewBox="0 0 24 24">
                      <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"></path>
                    </svg>
                  </a>
                </div>
              </div>
            </div>
            
            <!-- FAQ Card -->
            <div class="info-bg-white rounded-lg shadow-md p-6">
              <h3 class="info-title">Frequently Asked Questions</h3>
              <div class="faq-items">
                <div class="faq-item">
                  <h4>What is your response time?</h4>
                  <p>We typically respond within 24 hours during business days.</p>
                </div>
                <div class="faq-item">
                  <h4>Do you offer phone support?</h4>
                  <p>Yes, phone support is available for enterprise customers.</p>
                </div>
                <div class="faq-item">
                  <h4>Can I schedule a demo?</h4>
                  <p>Absolutely! Select "Sales Question" in the form and mention you'd like a demo.</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Map Section -->
    <section class="map-section">
      <div class="map-placeholder">
        <div class="map-overlay">
          <div class="map-content">
            <IconLucideMapPin class="w-6 h-6" />
            <h3>Visit Our Office</h3>
            <p>123 Business Ave, Suite 100<br>San Francisco, CA 94107</p>
            <a href="#" class="btn btn-white">Get Directions</a>
          </div>
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

<style scoped>
.contact-view {
  min-height: 100vh;
}

/* Hero Section */
.hero-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 5rem 0;
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
}

/* Contact Section */
.contact-section {
  padding: 5rem 0;
  background: #f7fafc;
}

.contact-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 3rem;
}

.contact-form-card {
  background: white;
  padding: 2.5rem;
  border-radius: 1rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
}

.section-title {
  font-size: 1.75rem;
  font-weight: 700;
  color: #1a202c;
  margin: 0 0 2rem 0;
}

.contact-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-size: 0.875rem;
  font-weight: 500;
  color: #4a5568;
}

.dark .form-group label {
  color: #d1d5db;
}

.form-input {
  padding: 0.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.375rem;
  font-size: 1rem;
  transition: all 0.3s;
  background-color: white;
  color: #1a202c;
}

.dark .form-input {
  background-color: #374151;
  border-color: #4b5563;
  color: #f3f4f6;
}

.form-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.dark .form-input:focus {
  border-color: #818cf8;
  box-shadow: 0 0 0 3px rgba(129, 140, 248, 0.1);
}

.form-input::placeholder {
  color: #a0aec0;
}

.dark .form-input::placeholder {
  color: #6b7280;
}

textarea.form-input {
  resize: vertical;
  min-height: 120px;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  font-size: 0.875rem;
  color: #4a5568;
}

.checkbox-input {
  width: 18px;
  height: 18px;
  cursor: pointer;
}

.btn {
  padding: 0.75rem 2rem;
  border-radius: 0.5rem;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s;
  display: inline-block;
  border: none;
  cursor: pointer;
}

.btn-lg {
  padding: 1rem 2.5rem;
  font-size: 1.125rem;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-white {
  background: white;
  color: #667eea;
}

.btn-white:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(255, 255, 255, 0.3);
}

.submit-message {
  padding: 1rem;
  border-radius: 0.375rem;
  text-align: center;
  font-weight: 500;
}

.submit-message.success {
  background: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.submit-message.error {
  background: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

/* Contact Information */
.contact-info {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.info-card {
  background: white;
  padding: 2rem;
  border-radius: 1rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
}

.info-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1a202c;
  margin: 0 0 0.75rem 0;
}

.info-description {
  color: #718096;
  margin-bottom: 1.5rem;
}

.info-items {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.info-item {
  display: flex;
  gap: 1rem;
}

.info-icon {
  width: 40px;
  height: 40px;
  border-radius: 0.5rem;
  background: linear-gradient(135deg, #667eea20 0%, #764ba220 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.info-icon svg {
  width: 20px;
  height: 20px;
  color: #667eea;
}

.info-label {
  font-size: 0.875rem;
  color: #718096;
  margin-bottom: 0.25rem;
}

.info-value {
  color: #2d3748;
  text-decoration: none;
}

.info-value:hover {
  color: #667eea;
}

/* Social Section */
.social-section {
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid #e2e8f0;
}

.social-title {
  font-size: 1rem;
  font-weight: 600;
  color: #1a202c;
  margin: 0 0 1rem 0;
}

.social-links {
  display: flex;
  gap: 1rem;
}

.social-link {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #f7fafc;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
}

.social-link:hover {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  transform: translateY(-2px);
}

.social-link svg {
  width: 20px;
  height: 20px;
  color: #718096;
}

.social-link:hover svg {
  color: white;
}

/* FAQ Items */
.faq-items {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.faq-item h4 {
  font-size: 1rem;
  font-weight: 600;
  color: #2d3748;
  margin: 0 0 0.5rem 0;
}

.faq-item p {
  color: #718096;
  font-size: 0.875rem;
  line-height: 1.6;
}

/* Map Section */
.map-section {
  height: 400px;
  position: relative;
}

.map-placeholder {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #e2e8f0 0%, #cbd5e0 100%);
  position: relative;
}

.map-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
}

.map-content {
  text-align: center;
  color: white;
}

.map-icon {
  width: 60px;
  height: 60px;
  margin: 0 auto 1rem;
}

.map-content h3 {
  font-size: 1.5rem;
  margin: 0 0 1rem 0;
}

.map-content p {
  margin-bottom: 1.5rem;
  opacity: 0.95;
}

/* Responsive */
@media (max-width: 1024px) {
  .contact-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 2rem;
  }
  
  .section-title {
    font-size: 1.5rem;
  }
  
  .form-row {
    grid-template-columns: 1fr;
  }
  
  .contact-form-card {
    padding: 1.5rem;
  }
  
  .info-card {
    padding: 1.5rem;
  }
}
</style>