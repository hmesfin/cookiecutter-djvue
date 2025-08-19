<template>
  <div class="privacy-view">
    <div class="bg-gradient-to-br from-emerald-500 to-teal-600 dark:from-emerald-600 dark:to-teal-700 text-white py-20">
      <div class="text-center max-w-4xl mx-auto px-4">
        <h1 class="text-5xl font-bold mb-4">Privacy Policy</h1>
        <p class="text-xl opacity-95">Last updated: {% raw %}{{ lastUpdated }}{% endraw %}</p>
      </div>
    </div>

    <div class="py-20 bg-white dark:bg-gray-900">
      <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="prose prose-lg max-w-none dark:prose-invert">
          <section class="mb-12">
            <h2 class="text-3xl font-bold text-gray-900 dark:text-gray-100 mb-4">Introduction</h2>
            <p class="text-gray-600 dark:text-gray-400 leading-relaxed">
              At {{ cookiecutter.project_name }}, we take your privacy seriously. This Privacy Policy explains how we collect, 
              use, disclose, and safeguard your information when you use our service. Please read this privacy policy carefully.
            </p>
          </section>

          <section class="mb-12">
            <h2 class="text-3xl font-bold text-gray-900 dark:text-gray-100 mb-4">Information We Collect</h2>
            <h3 class="text-xl font-semibold text-gray-800 dark:text-gray-200 mb-3 mt-6">Personal Information</h3>
            <p class="text-gray-600 dark:text-gray-400 leading-relaxed mb-4">
              We may collect personal information that you voluntarily provide to us when you register on the platform, 
              express an interest in obtaining information about us or our products and services, when you participate in 
              activities on the platform, or otherwise when you contact us.
            </p>
            <ul class="list-disc pl-6 space-y-2 text-gray-600 dark:text-gray-400">
              <li><strong class="text-gray-800 dark:text-gray-200">Name and Contact Data:</strong> First and last name, email address, postal address, phone number, and other similar contact data.</li>
              <li><strong class="text-gray-800 dark:text-gray-200">Credentials:</strong> Passwords, password hints, and similar security information used for authentication and account access.</li>
              <li><strong class="text-gray-800 dark:text-gray-200">Payment Data:</strong> Data necessary to process your payment if you make purchases, such as your payment instrument number and the security code associated with your payment instrument.</li>
              <li><strong class="text-gray-800 dark:text-gray-200">Profile Data:</strong> Your username, interests, preferences, feedback and survey responses.</li>
            </ul>

            <h3 class="text-xl font-semibold text-gray-800 dark:text-gray-200 mb-3 mt-6">Information Automatically Collected</h3>
            <p class="text-gray-600 dark:text-gray-400 leading-relaxed mb-4">
              When you access our platform, we automatically collect certain information about your device, including information 
              about your web browser, IP address, time zone, and some of the cookies that are installed on your device.
            </p>
            <ul class="list-disc pl-6 space-y-2 text-gray-600 dark:text-gray-400">
              <li><strong class="text-gray-800 dark:text-gray-200">Log and Usage Data:</strong> Service-related, diagnostic, usage and performance information our servers automatically collect when you access or use our platform.</li>
              <li><strong class="text-gray-800 dark:text-gray-200">Device Data:</strong> Information about your device such as your IP address, browser and device characteristics, operating system, language preferences, referring URLs, device name, country, location.</li>
              <li><strong class="text-gray-800 dark:text-gray-200">Cookie Data:</strong> Information collected through cookies and similar tracking technologies to maintain session state, analyze trends, administer the site, track users' movements, and gather demographic information.</li>
            </ul>
          </section>

          <section class="mb-12">
            <h2 class="text-3xl font-bold text-gray-900 dark:text-gray-100 mb-4">How We Use Your Information</h2>
            <p class="text-gray-600 dark:text-gray-400 leading-relaxed mb-4">We use the information we collect or receive:</p>
            <ul class="list-disc pl-6 space-y-2 text-gray-600 dark:text-gray-400">
              <li><strong class="text-gray-800 dark:text-gray-200">To facilitate account creation and authentication</strong> and otherwise manage user accounts.</li>
              <li><strong class="text-gray-800 dark:text-gray-200">To deliver and facilitate delivery of services</strong> to the user.</li>
              <li><strong class="text-gray-800 dark:text-gray-200">To respond to user inquiries</strong> and offer support to users.</li>
              <li><strong class="text-gray-800 dark:text-gray-200">To send administrative information</strong> such as changes to our terms, conditions, and policies.</li>
              <li><strong class="text-gray-800 dark:text-gray-200">To protect our services</strong> by identifying and preventing fraud, abuse, and other harmful activities.</li>
              <li><strong class="text-gray-800 dark:text-gray-200">To enforce our terms, conditions and policies</strong> for business purposes, to comply with legal and regulatory requirements.</li>
              <li><strong class="text-gray-800 dark:text-gray-200">To respond to legal requests</strong> and prevent harm as legally required.</li>
              <li><strong class="text-gray-800 dark:text-gray-200">For other business purposes</strong> such as data analysis, identifying usage trends, determining the effectiveness of our promotional campaigns.</li>
            </ul>
          </section>

          <section class="mb-12">
            <h2 class="text-3xl font-bold text-gray-900 dark:text-gray-100 mb-4">Information Sharing and Disclosure</h2>
            <p class="text-gray-600 dark:text-gray-400 leading-relaxed mb-4">We may share or disclose your information in the following situations:</p>
            <ul class="list-disc pl-6 space-y-2 text-gray-600 dark:text-gray-400">
              <li><strong class="text-gray-800 dark:text-gray-200">With Service Providers:</strong> We may share your information with third-party vendors, service providers, contractors or agents who perform services for us or on our behalf.</li>
              <li><strong class="text-gray-800 dark:text-gray-200">For Business Transfers:</strong> We may share or transfer your information in connection with, or during negotiations of, any merger, sale of company assets, financing, or acquisition of all or a portion of our business to another company.</li>
              <li><strong class="text-gray-800 dark:text-gray-200">With Affiliates:</strong> We may share your information with our affiliates, in which case we will require those affiliates to honor this privacy policy.</li>
              <li><strong class="text-gray-800 dark:text-gray-200">With Business Partners:</strong> We may share your information with our business partners to offer you certain products, services or promotions.</li>
              <li><strong class="text-gray-800 dark:text-gray-200">With your Consent:</strong> We may disclose your personal information for any other purpose with your consent.</li>
              <li><strong class="text-gray-800 dark:text-gray-200">For Legal Purposes:</strong> To comply with legal obligations, respond to legal requests, or protect our rights.</li>
            </ul>
          </section>

          <section class="mb-12">
            <h2 class="text-3xl font-bold text-gray-900 dark:text-gray-100 mb-4">Data Security</h2>
            <p class="text-gray-600 dark:text-gray-400 leading-relaxed mb-4">
              We implement appropriate technical and organizational security measures designed to protect the security of any 
              personal information we process. However, despite our safeguards and efforts to secure your information, no 
              electronic transmission over the Internet or information storage technology can be guaranteed to be 100% secure.
            </p>
            <p class="text-gray-600 dark:text-gray-400 leading-relaxed">
              We cannot guarantee the absolute security of your personal information. Any transmission of personal information 
              is at your own risk. We are not responsible for circumvention of any privacy settings or security measures 
              contained on the platform.
            </p>
          </section>

          <section class="mb-12">
            <h2 class="text-3xl font-bold text-gray-900 dark:text-gray-100 mb-4">Data Retention</h2>
            <p class="text-gray-600 dark:text-gray-400 leading-relaxed">
              We will retain your personal information only for as long as is necessary for the purposes set out in this 
              Privacy Policy. We will retain and use your personal information to the extent necessary to comply with our 
              legal obligations, resolve disputes, and enforce our legal agreements and policies.
            </p>
          </section>

          <section class="mb-12">
            <h2 class="text-3xl font-bold text-gray-900 dark:text-gray-100 mb-4">Your Privacy Rights</h2>
            <p class="text-gray-600 dark:text-gray-400 leading-relaxed mb-4">Depending on your location, you may have the following rights regarding your personal information:</p>
            <ul class="list-disc pl-6 space-y-2 text-gray-600 dark:text-gray-400">
              <li><strong class="text-gray-800 dark:text-gray-200">Access:</strong> The right to request copies of your personal information.</li>
              <li><strong class="text-gray-800 dark:text-gray-200">Rectification:</strong> The right to request that we correct any information you believe is inaccurate or complete information you believe is incomplete.</li>
              <li><strong class="text-gray-800 dark:text-gray-200">Erasure:</strong> The right to request that we erase your personal information, under certain conditions.</li>
              <li><strong class="text-gray-800 dark:text-gray-200">Restrict Processing:</strong> The right to request that we restrict the processing of your personal information, under certain conditions.</li>
              <li><strong class="text-gray-800 dark:text-gray-200">Object to Processing:</strong> The right to object to our processing of your personal information, under certain conditions.</li>
              <li><strong class="text-gray-800 dark:text-gray-200">Data Portability:</strong> The right to request that we transfer the data that we have collected to another organization, or directly to you, under certain conditions.</li>
            </ul>
          </section>

          <section class="mb-12">
            <h2 class="text-3xl font-bold text-gray-900 dark:text-gray-100 mb-4">Children's Privacy</h2>
            <p class="text-gray-600 dark:text-gray-400 leading-relaxed">
              Our service does not address anyone under the age of 13. We do not knowingly collect personally identifiable 
              information from anyone under the age of 13. If you are a parent or guardian and you are aware that your child 
              has provided us with personal data, please contact us.
            </p>
          </section>

          <section class="mb-12">
            <h2 class="text-3xl font-bold text-gray-900 dark:text-gray-100 mb-4">Updates to This Policy</h2>
            <p class="text-gray-600 dark:text-gray-400 leading-relaxed">
              We may update this privacy policy from time to time. The updated version will be indicated by an updated 
              "Last updated" date and the updated version will be effective as soon as it is accessible. We encourage you 
              to review this privacy policy frequently to be informed of how we are protecting your information.
            </p>
          </section>

          <section class="mb-12">
            <h2 class="text-3xl font-bold text-gray-900 dark:text-gray-100 mb-4">Contact Us</h2>
            <p class="text-gray-600 dark:text-gray-400 leading-relaxed mb-6">If you have questions or comments about this policy, you may contact us at:</p>
            <div class="bg-gray-50 dark:bg-gray-800 rounded-lg p-6 space-y-3">
              <p class="text-gray-800 dark:text-gray-200"><strong>{{ cookiecutter.project_name }}</strong></p>
              <p class="text-gray-600 dark:text-gray-400">Email: privacy@{{ cookiecutter.domain_name }}</p>
              <p class="text-gray-600 dark:text-gray-400">Address: [Your Company Address]</p>
              <p class="text-gray-600 dark:text-gray-400">Phone: [Your Phone Number]</p>
            </div>
          </section>
        </div>
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