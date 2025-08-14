<template>
  <div class="terms-view">
    <div class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title">Terms of Service</h1>
        <p class="hero-subtitle">Effective Date: {% raw %}{{ effectiveDate }}{% endraw %}</p>
      </div>
    </div>

    <div class="content-section">
      <div class="content-container">
        <section class="terms-section">
          <h2>1. Acceptance of Terms</h2>
          <p>
            By accessing and using {{ cookiecutter.project_name }} ("Service"), you accept and agree to be bound by the terms 
            and provision of this agreement. If you do not agree to abide by the above, please do not use this service.
          </p>
          <p>
            These Terms of Service apply to all users of the Service, including without limitation users who are browsers, 
            vendors, customers, merchants, and/or contributors of content.
          </p>
        </section>

        <section class="terms-section">
          <h2>2. Use License</h2>
          <p>
            Permission is granted to temporarily access the materials (information or software) on {{ cookiecutter.project_name }} 
            for personal, non-commercial transitory viewing only. This is the grant of a license, not a transfer of title, 
            and under this license you may not:
          </p>
          <ul>
            <li>Modify or copy the materials</li>
            <li>Use the materials for any commercial purpose or for any public display (commercial or non-commercial)</li>
            <li>Attempt to decompile or reverse engineer any software contained on our service</li>
            <li>Remove any copyright or other proprietary notations from the materials</li>
            <li>Transfer the materials to another person or "mirror" the materials on any other server</li>
          </ul>
          <p>
            This license shall automatically terminate if you violate any of these restrictions and may be terminated by 
            {{ cookiecutter.project_name }} at any time. Upon terminating your viewing of these materials or upon the 
            termination of this license, you must destroy any downloaded materials in your possession whether in electronic 
            or printed format.
          </p>
        </section>

        <section class="terms-section">
          <h2>3. Account Registration</h2>
          <p>
            To use certain features of our Service, you may be required to register for an account. When you register for 
            an account, you agree to:
          </p>
          <ul>
            <li>Provide accurate, current, and complete information during the registration process</li>
            <li>Maintain and promptly update your account information to keep it accurate, current, and complete</li>
            <li>Maintain the security and confidentiality of your login credentials</li>
            <li>Accept all risks of unauthorized access to your account and the information you provide</li>
            <li>Immediately notify us of any unauthorized use of your account or any other breach of security</li>
          </ul>
          <p>
            You are responsible for all activities that occur under your account. We reserve the right to suspend or 
            terminate your account if any information provided during the registration process or thereafter proves to 
            be inaccurate, false, or misleading.
          </p>
        </section>

        <section class="terms-section">
          <h2>4. Prohibited Uses</h2>
          <p>
            In addition to other prohibitions as set forth in the Terms of Service, you are prohibited from using the 
            Service or its content:
          </p>
          <ul>
            <li>For any unlawful purpose or to solicit others to perform or participate in any unlawful acts</li>
            <li>To violate any international, federal, provincial, or state regulations, rules, laws, or local ordinances</li>
            <li>To infringe upon or violate our intellectual property rights or the intellectual property rights of others</li>
            <li>To harass, abuse, insult, harm, defame, slander, disparage, intimidate, or discriminate</li>
            <li>To submit false or misleading information</li>
            <li>To upload or transmit viruses or any other type of malicious code</li>
            <li>To collect or track the personal information of others</li>
            <li>To spam, phish, pharm, pretext, spider, crawl, or scrape</li>
            <li>For any obscene or immoral purpose</li>
            <li>To interfere with or circumvent the security features of the Service</li>
          </ul>
        </section>

        <section class="terms-section">
          <h2>5. Content and Intellectual Property</h2>
          
          <h3>5.1 Your Content</h3>
          <p>
            Our Service may allow you to post, link, store, share and otherwise make available certain information, text, 
            graphics, videos, or other material ("Content"). You are responsible for the Content that you post to the Service, 
            including its legality, reliability, and appropriateness.
          </p>
          <p>
            By posting Content to the Service, you grant us the right and license to use, modify, publicly perform, publicly 
            display, reproduce, and distribute such Content on and through the Service. You retain any and all of your rights 
            to any Content you submit, post or display on or through the Service and you are responsible for protecting those rights.
          </p>

          <h3>5.2 Our Intellectual Property</h3>
          <p>
            The Service and its original content (excluding Content provided by users), features and functionality are and 
            will remain the exclusive property of {{ cookiecutter.project_name }} and its licensors. The Service is protected 
            by copyright, trademark, and other laws. Our trademarks and trade dress may not be used in connection with any 
            product or service without our prior written consent.
          </p>
        </section>

        <section class="terms-section">
          <h2>6. Privacy Policy</h2>
          <p>
            Your use of the Service is also governed by our Privacy Policy. Please review our Privacy Policy, which also 
            governs the Site and informs users of our data collection practices. By using the Service, you consent to 
            all actions taken by us with respect to your information in compliance with the Privacy Policy.
          </p>
        </section>

        <section class="terms-section">
          <h2>7. Termination</h2>
          <p>
            We may terminate or suspend your account and bar access to the Service immediately, without prior notice or 
            liability, under our sole discretion, for any reason whatsoever and without limitation, including but not 
            limited to a breach of the Terms.
          </p>
          <p>
            If you wish to terminate your account, you may simply discontinue using the Service or contact us to request 
            account deletion.
          </p>
          <p>
            All provisions of the Terms which by their nature should survive termination shall survive termination, including, 
            without limitation, ownership provisions, warranty disclaimers, indemnity and limitations of liability.
          </p>
        </section>

        <section class="terms-section">
          <h2>8. Disclaimer</h2>
          <p>
            The information on the Service is provided on an "as is" basis. To the fullest extent permitted by law, this 
            Service:
          </p>
          <ul>
            <li>Excludes all representations and warranties relating to this Service and its contents</li>
            <li>Excludes all liability for damages arising out of or in connection with your use of this Service</li>
          </ul>
          <p>
            This includes, without limitation, direct loss, loss of business or profits (whether or not the loss of such 
            profits was foreseeable, arose in the normal course of things or you have advised us of the possibility of 
            such potential loss), damage caused to your computer, computer software, systems and programs and the data 
            thereon or any other direct or indirect, consequential and incidental damages.
          </p>
        </section>

        <section class="terms-section">
          <h2>9. Limitation of Liability</h2>
          <p>
            In no event shall {{ cookiecutter.project_name }}, nor its directors, employees, partners, agents, suppliers, 
            or affiliates, be liable for any indirect, incidental, special, consequential, or punitive damages, including 
            without limitation, loss of profits, data, use, goodwill, or other intangible losses, resulting from:
          </p>
          <ul>
            <li>Your use or inability to use the Service</li>
            <li>Any unauthorized access to or use of our servers and/or any personal information stored therein</li>
            <li>Any interruption or cessation of transmission to or from the Service</li>
            <li>Any bugs, viruses, trojan horses, or the like that may be transmitted to or through our Service by any third party</li>
            <li>Any errors or omissions in any content or for any loss or damage incurred as a result of the use of any content</li>
          </ul>
        </section>

        <section class="terms-section">
          <h2>10. Indemnification</h2>
          <p>
            You agree to defend, indemnify, and hold harmless {{ cookiecutter.project_name }}, its affiliates, licensors, 
            and service providers, and its and their respective officers, directors, employees, contractors, agents, licensors, 
            suppliers, successors, and assigns from and against any claims, liabilities, damages, judgments, awards, losses, 
            costs, expenses, or fees (including reasonable attorneys' fees) arising out of or relating to your violation 
            of these Terms of Service or your use of the Service.
          </p>
        </section>

        <section class="terms-section">
          <h2>11. Governing Law</h2>
          <p>
            These Terms shall be governed and construed in accordance with the laws of [Your Jurisdiction], without regard 
            to its conflict of law provisions. Our failure to enforce any right or provision of these Terms will not be 
            considered a waiver of those rights.
          </p>
          <p>
            If any provision of these Terms is held to be invalid or unenforceable by a court, the remaining provisions of 
            these Terms will remain in effect. These Terms constitute the entire agreement between us regarding our Service, 
            and supersede and replace any prior agreements we might have had between us regarding the Service.
          </p>
        </section>

        <section class="terms-section">
          <h2>12. Changes to Terms</h2>
          <p>
            We reserve the right, at our sole discretion, to modify or replace these Terms at any time. If a revision is 
            material, we will provide at least 30 days notice prior to any new terms taking effect. What constitutes a 
            material change will be determined at our sole discretion.
          </p>
          <p>
            By continuing to access or use our Service after any revisions become effective, you agree to be bound by the 
            revised terms. If you do not agree to the new terms, you are no longer authorized to use the Service.
          </p>
        </section>

        <section class="terms-section">
          <h2>13. Contact Information</h2>
          <p>If you have any questions about these Terms of Service, please contact us at:</p>
          <div class="contact-info">
            <p><strong>{{ cookiecutter.project_name }}</strong></p>
            <p>Email: legal@{{ cookiecutter.domain_name }}</p>
            <p>Address: [Your Company Address]</p>
            <p>Phone: [Your Phone Number]</p>
          </div>
        </section>

        <div class="acknowledgment">
          <p>
            By using this Service, you signify your acceptance of these Terms of Service. If you do not agree to these 
            Terms of Service, please do not use our Service. Your continued use of the Service following the posting of 
            changes to these terms will be deemed your acceptance of those changes.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup{% if cookiecutter.use_typescript == 'y' %} lang="ts"{% endif %}>
import { computed } from 'vue'

const effectiveDate = computed(() => {
  const date = new Date()
  return date.toLocaleDateString('en-US', { 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric' 
  })
})
</script>

<style scoped>
.terms-view {
  min-height: 100vh;
  background: #f7fafc;
}

.hero-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 4rem 1rem;
}

.hero-content {
  max-width: 1200px;
  margin: 0 auto;
  text-align: center;
}

.hero-title {
  font-size: 3rem;
  font-weight: 700;
  margin: 0 0 1rem 0;
}

.hero-subtitle {
  font-size: 1.125rem;
  opacity: 0.9;
}

.content-section {
  padding: 4rem 1rem;
}

.content-container {
  max-width: 900px;
  margin: 0 auto;
}

.terms-section {
  background: white;
  padding: 2rem;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.terms-section h2 {
  font-size: 1.875rem;
  font-weight: 600;
  color: #1a202c;
  margin: 0 0 1.5rem 0;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid #e2e8f0;
}

.terms-section h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #2d3748;
  margin: 1.5rem 0 1rem 0;
}

.terms-section p {
  color: #4a5568;
  line-height: 1.75;
  margin-bottom: 1rem;
}

.terms-section ul {
  color: #4a5568;
  line-height: 1.75;
  margin-left: 2rem;
  margin-bottom: 1rem;
}

.terms-section ul li {
  margin-bottom: 0.5rem;
}

.contact-info {
  background: #f7fafc;
  padding: 1.5rem;
  border-radius: 0.375rem;
  margin-top: 1rem;
}

.contact-info p {
  margin: 0.5rem 0;
}

.acknowledgment {
  background: #edf2f7;
  padding: 2rem;
  border-radius: 0.5rem;
  border-left: 4px solid #4299e1;
  margin-top: 2rem;
}

.acknowledgment p {
  color: #2d3748;
  line-height: 1.75;
  margin: 0;
  font-weight: 500;
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 2rem;
  }
  
  .hero-section {
    padding: 3rem 1rem;
  }
  
  .content-section {
    padding: 2rem 1rem;
  }
  
  .terms-section {
    padding: 1.5rem;
  }
  
  .terms-section h2 {
    font-size: 1.5rem;
  }
}
</style>