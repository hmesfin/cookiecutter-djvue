<template>
  <div class="privacy-view">
    <div class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title">Privacy Policy</h1>
        <p class="hero-subtitle">Last updated: {% raw %}{{ lastUpdated }}{% endraw %}</p>
      </div>
    </div>

    <div class="content-section">
      <div class="content-container">
        <section class="policy-section">
          <h2>Introduction</h2>
          <p>
            At {{ cookiecutter.project_name }}, we take your privacy seriously. This Privacy Policy explains how we collect, 
            use, disclose, and safeguard your information when you use our service. Please read this privacy policy carefully.
          </p>
        </section>

        <section class="policy-section">
          <h2>Information We Collect</h2>
          <h3>Personal Information</h3>
          <p>
            We may collect personal information that you voluntarily provide to us when you register on the platform, 
            express an interest in obtaining information about us or our products and services, when you participate in 
            activities on the platform, or otherwise when you contact us.
          </p>
          <ul>
            <li>Name and Contact Data: First and last name, email address, postal address, phone number, and other similar contact data.</li>
            <li>Credentials: Passwords, password hints, and similar security information used for authentication and account access.</li>
            <li>Payment Data: Data necessary to process your payment if you make purchases, such as your payment instrument number and the security code associated with your payment instrument.</li>
            <li>Profile Data: Your username, interests, preferences, feedback and survey responses.</li>
          </ul>

          <h3>Information Automatically Collected</h3>
          <p>
            When you access our platform, we automatically collect certain information about your device, including information 
            about your web browser, IP address, time zone, and some of the cookies that are installed on your device.
          </p>
          <ul>
            <li>Log and Usage Data: Service-related, diagnostic, usage and performance information our servers automatically collect when you access or use our platform.</li>
            <li>Device Data: Information about your device such as your IP address, browser and device characteristics, operating system, language preferences, referring URLs, device name, country, location.</li>
            <li>Cookie Data: Information collected through cookies and similar tracking technologies to maintain session state, analyze trends, administer the site, track users' movements, and gather demographic information.</li>
          </ul>
        </section>

        <section class="policy-section">
          <h2>How We Use Your Information</h2>
          <p>We use the information we collect or receive:</p>
          <ul>
            <li><strong>To facilitate account creation and authentication</strong> and otherwise manage user accounts.</li>
            <li><strong>To deliver and facilitate delivery of services</strong> to the user.</li>
            <li><strong>To respond to user inquiries</strong> and offer support to users.</li>
            <li><strong>To send administrative information</strong> such as changes to our terms, conditions, and policies.</li>
            <li><strong>To protect our services</strong> by identifying and preventing fraud, abuse, and other harmful activities.</li>
            <li><strong>To enforce our terms, conditions and policies</strong> for business purposes, to comply with legal and regulatory requirements.</li>
            <li><strong>To respond to legal requests</strong> and prevent harm as legally required.</li>
            <li><strong>For other business purposes</strong> such as data analysis, identifying usage trends, determining the effectiveness of our promotional campaigns.</li>
          </ul>
        </section>

        <section class="policy-section">
          <h2>Information Sharing and Disclosure</h2>
          <p>We may share or disclose your information in the following situations:</p>
          <ul>
            <li><strong>With Service Providers:</strong> We may share your information with third-party vendors, service providers, contractors or agents who perform services for us or on our behalf.</li>
            <li><strong>For Business Transfers:</strong> We may share or transfer your information in connection with, or during negotiations of, any merger, sale of company assets, financing, or acquisition of all or a portion of our business to another company.</li>
            <li><strong>With Affiliates:</strong> We may share your information with our affiliates, in which case we will require those affiliates to honor this privacy policy.</li>
            <li><strong>With Business Partners:</strong> We may share your information with our business partners to offer you certain products, services or promotions.</li>
            <li><strong>With your Consent:</strong> We may disclose your personal information for any other purpose with your consent.</li>
            <li><strong>For Legal Purposes:</strong> To comply with legal obligations, respond to legal requests, or protect our rights.</li>
          </ul>
        </section>

        <section class="policy-section">
          <h2>Data Security</h2>
          <p>
            We implement appropriate technical and organizational security measures designed to protect the security of any 
            personal information we process. However, despite our safeguards and efforts to secure your information, no 
            electronic transmission over the Internet or information storage technology can be guaranteed to be 100% secure.
          </p>
          <p>
            We cannot guarantee the absolute security of your personal information. Any transmission of personal information 
            is at your own risk. We are not responsible for circumvention of any privacy settings or security measures 
            contained on the platform.
          </p>
        </section>

        <section class="policy-section">
          <h2>Data Retention</h2>
          <p>
            We will retain your personal information only for as long as is necessary for the purposes set out in this 
            Privacy Policy. We will retain and use your personal information to the extent necessary to comply with our 
            legal obligations, resolve disputes, and enforce our legal agreements and policies.
          </p>
        </section>

        <section class="policy-section">
          <h2>Your Privacy Rights</h2>
          <p>Depending on your location, you may have the following rights regarding your personal information:</p>
          <ul>
            <li><strong>Access:</strong> The right to request copies of your personal information.</li>
            <li><strong>Rectification:</strong> The right to request that we correct any information you believe is inaccurate or complete information you believe is incomplete.</li>
            <li><strong>Erasure:</strong> The right to request that we erase your personal information, under certain conditions.</li>
            <li><strong>Restrict Processing:</strong> The right to request that we restrict the processing of your personal information, under certain conditions.</li>
            <li><strong>Object to Processing:</strong> The right to object to our processing of your personal information, under certain conditions.</li>
            <li><strong>Data Portability:</strong> The right to request that we transfer the data that we have collected to another organization, or directly to you, under certain conditions.</li>
          </ul>
        </section>

        <section class="policy-section">
          <h2>Children's Privacy</h2>
          <p>
            Our service does not address anyone under the age of 13. We do not knowingly collect personally identifiable 
            information from anyone under the age of 13. If you are a parent or guardian and you are aware that your child 
            has provided us with personal data, please contact us.
          </p>
        </section>

        <section class="policy-section">
          <h2>Updates to This Policy</h2>
          <p>
            We may update this privacy policy from time to time. The updated version will be indicated by an updated 
            "Last updated" date and the updated version will be effective as soon as it is accessible. We encourage you 
            to review this privacy policy frequently to be informed of how we are protecting your information.
          </p>
        </section>

        <section class="policy-section">
          <h2>Contact Us</h2>
          <p>If you have questions or comments about this policy, you may contact us at:</p>
          <div class="contact-info">
            <p><strong>{{ cookiecutter.project_name }}</strong></p>
            <p>Email: privacy@{{ cookiecutter.domain_name }}</p>
            <p>Address: [Your Company Address]</p>
            <p>Phone: [Your Phone Number]</p>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup{% if cookiecutter.use_typescript == 'y' %} lang="ts"{% endif %}>
import { computed } from 'vue'

const lastUpdated = computed(() => {
  const date = new Date()
  return date.toLocaleDateString('en-US', { 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric' 
  })
})
</script>

<style scoped>
.privacy-view {
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

.policy-section {
  background: white;
  padding: 2rem;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.policy-section h2 {
  font-size: 1.875rem;
  font-weight: 600;
  color: #1a202c;
  margin: 0 0 1.5rem 0;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid #e2e8f0;
}

.policy-section h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #2d3748;
  margin: 1.5rem 0 1rem 0;
}

.policy-section p {
  color: #4a5568;
  line-height: 1.75;
  margin-bottom: 1rem;
}

.policy-section ul {
  color: #4a5568;
  line-height: 1.75;
  margin-left: 2rem;
  margin-bottom: 1rem;
}

.policy-section ul li {
  margin-bottom: 0.5rem;
}

.policy-section ul li strong {
  color: #2d3748;
  font-weight: 600;
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
  
  .policy-section {
    padding: 1.5rem;
  }
  
  .policy-section h2 {
    font-size: 1.5rem;
  }
}
</style>