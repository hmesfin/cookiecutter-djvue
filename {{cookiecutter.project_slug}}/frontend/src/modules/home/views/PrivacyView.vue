<template>
  <div class="privacy-view">
    <div class="bg-gradient-to-br from-indigo-500 to-purple-600 text-white py-20">
      <div class="text-center max-w-4xl mx-auto">
        <h1 class="text-5xl font-bold mb-4">Privacy Policy</h1>
        <p class="text-xl opacity-95">Last updated: {% raw %}{{ lastUpdated }}{% endraw %}</p>
      </div>
    </div>

    <div class="py-20 bg-white dark:bg-gray-900">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <section class="mb-12">
          <h2>Introduction</h2>
          <p>
            At {{ cookiecutter.project_name }}, we take your privacy seriously. This Privacy Policy explains how we collect, 
            use, disclose, and safeguard your information when you use our service. Please read this privacy policy carefully.
          </p>
        </section>

        <section class="mb-12">
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

        <section class="mb-12">
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

        <section class="mb-12">
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

        <section class="mb-12">
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

        <section class="mb-12">
          <h2>Data Retention</h2>
          <p>
            We will retain your personal information only for as long as is necessary for the purposes set out in this 
            Privacy Policy. We will retain and use your personal information to the extent necessary to comply with our 
            legal obligations, resolve disputes, and enforce our legal agreements and policies.
          </p>
        </section>

        <section class="mb-12">
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

        <section class="mb-12">
          <h2>Children's Privacy</h2>
          <p>
            Our service does not address anyone under the age of 13. We do not knowingly collect personally identifiable 
            information from anyone under the age of 13. If you are a parent or guardian and you are aware that your child 
            has provided us with personal data, please contact us.
          </p>
        </section>

        <section class="mb-12">
          <h2>Updates to This Policy</h2>
          <p>
            We may update this privacy policy from time to time. The updated version will be indicated by an updated 
            "Last updated" date and the updated version will be effective as soon as it is accessible. We encourage you 
            to review this privacy policy frequently to be informed of how we are protecting your information.
          </p>
        </section>

        <section class="mb-12">
          <h2>Contact Us</h2>
          <p>If you have questions or comments about this policy, you may contact us at:</p>
          <div class="space-y-8">
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

