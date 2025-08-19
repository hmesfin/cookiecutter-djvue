<template>
  <div class="terms-view">
    <div class="bg-gradient-to-br from-emerald-500 to-teal-600 dark:from-emerald-600 dark:to-teal-700 text-white py-20">
      <div class="text-center max-w-4xl mx-auto px-4">
        <h1 class="text-5xl font-bold mb-4">Terms of Service</h1>
        <p class="text-xl opacity-95">Effective Date: {% raw %}{{ effectiveDate }}{% endraw %}</p>
      </div>
    </div>

    <div class="py-20 bg-white dark:bg-gray-900">
      <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="prose prose-lg max-w-none dark:prose-invert">
          <section class="mb-12">
            <h2 class="text-3xl font-bold text-gray-900 dark:text-gray-100 mb-4">1. Acceptance of Terms</h2>
            <p class="text-gray-600 dark:text-gray-400 leading-relaxed mb-4">
              By accessing and using {{ cookiecutter.project_name }} ("Service"), you accept and agree to be bound by the terms 
              and provision of this agreement. If you do not agree to abide by the above, please do not use this service.
            </p>
            <p class="text-gray-600 dark:text-gray-400 leading-relaxed">
              These Terms of Service apply to all users of the Service, including without limitation users who are browsers, 
              vendors, customers, merchants, and/or contributors of content.
            </p>
          </section>

          <section class="mb-12">
            <h2 class="text-3xl font-bold text-gray-900 dark:text-gray-100 mb-4">2. Use License</h2>
            <p class="text-gray-600 dark:text-gray-400 leading-relaxed mb-4">
              Permission is granted to temporarily access the materials (information or software) on {{ cookiecutter.project_name }} 
              for personal, non-commercial transitory viewing only. This is the grant of a license, not a transfer of title, 
              and under this license you may not:
            </p>
            <ul class="list-disc pl-6 space-y-2 text-gray-600 dark:text-gray-400 mb-4">
              <li>Modify or copy the materials</li>
              <li>Use the materials for any commercial purpose or for any public display (commercial or non-commercial)</li>
              <li>Attempt to decompile or reverse engineer any software contained on our service</li>
              <li>Remove any copyright or other proprietary notations from the materials</li>
              <li>Transfer the materials to another person or "mirror" the materials on any other server</li>
            </ul>
            <p class="text-gray-600 dark:text-gray-400 leading-relaxed">
              This license shall automatically terminate if you violate any of these restrictions and may be terminated by 
              {{ cookiecutter.project_name }} at any time. Upon terminating your viewing of these materials or upon the 
              termination of this license, you must destroy any downloaded materials in your possession whether in electronic 
              or printed format.
            </p>
          </section>

          <section class="mb-12">
            <h2 class="text-3xl font-bold text-gray-900 dark:text-gray-100 mb-4">3. Account Registration</h2>
            <p class="text-gray-600 dark:text-gray-400 leading-relaxed mb-4">
              To use certain features of our Service, you may be required to register for an account. When you register for 
              an account, you agree to:
            </p>
            <ul class="list-disc pl-6 space-y-2 text-gray-600 dark:text-gray-400 mb-4">
              <li>Provide accurate, current, and complete information during the registration process</li>
              <li>Maintain and promptly update your account information to keep it accurate, current, and complete</li>
              <li>Maintain the security and confidentiality of your login credentials</li>
              <li>Accept all risks of unauthorized access to your account and the information you provide</li>
              <li>Immediately notify us of any unauthorized use of your account or any other breach of security</li>
            </ul>
            <p class="text-gray-600 dark:text-gray-400 leading-relaxed">
              You are responsible for all activities that occur under your account. We reserve the right to suspend or 
              terminate your account if any information provided during the registration process or thereafter proves to 
              be inaccurate, false, or misleading.
            </p>
          </section>

          <section class="mb-12">
            <h2 class="text-3xl font-bold text-gray-900 dark:text-gray-100 mb-4">4. Prohibited Uses</h2>
            <p class="text-gray-600 dark:text-gray-400 leading-relaxed mb-4">
              In addition to other prohibitions as set forth in the Terms of Service, you are prohibited from using the 
              Service or its content:
            </p>
            <ul class="list-disc pl-6 space-y-2 text-gray-600 dark:text-gray-400">
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

          <section class="mb-12">
            <h2 class="text-3xl font-bold text-gray-900 dark:text-gray-100 mb-4">5. Content and Intellectual Property</h2>
            
            <h3 class="text-xl font-semibold text-gray-800 dark:text-gray-200 mb-3 mt-6">5.1 Your Content</h3>
            <p class="text-gray-600 dark:text-gray-400 leading-relaxed mb-4">
              Our Service may allow you to post, link, store, share and otherwise make available certain information, text, 
              graphics, videos, or other material ("Content"). You are responsible for the Content that you post to the Service, 
              including its legality, reliability, and appropriateness.
            </p>
            <p class="text-gray-600 dark:text-gray-400 leading-relaxed mb-4">
              By posting Content to the Service, you grant us the right and license to use, modify, publicly perform, publicly 
              display, reproduce, and distribute such Content on and through the Service. You retain any and all of your rights 
              to any Content you submit, post or display on or through the Service and you are responsible for protecting those rights.
            </p>

            <h3 class="text-xl font-semibold text-gray-800 dark:text-gray-200 mb-3 mt-6">5.2 Our Intellectual Property</h3>
            <p class="text-gray-600 dark:text-gray-400 leading-relaxed">
              The Service and its original content (excluding Content provided by users), features and functionality are and 
              will remain the exclusive property of {{ cookiecutter.project_name }} and its licensors. The Service is protected 
              by copyright, trademark, and other laws. Our trademarks and trade dress may not be used in connection with any 
              product or service without our prior written consent.
            </p>
          </section>

          <section class="mb-12">
            <h2 class="text-3xl font-bold text-gray-900 dark:text-gray-100 mb-4">6. Privacy Policy</h2>
            <p class="text-gray-600 dark:text-gray-400 leading-relaxed">
              Your use of the Service is also governed by our Privacy Policy. Please review our Privacy Policy, which also 
              governs the Site and informs users of our data collection practices. By using the Service, you consent to 
              all actions taken by us with respect to your information in compliance with the Privacy Policy.
            </p>
          </section>

          <section class="mb-12">
            <h2 class="text-3xl font-bold text-gray-900 dark:text-gray-100 mb-4">7. Termination</h2>
            <p class="text-gray-600 dark:text-gray-400 leading-relaxed mb-4">
              We may terminate or suspend your account and bar access to the Service immediately, without prior notice or 
              liability, under our sole discretion, for any reason whatsoever and without limitation, including but not 
              limited to a breach of the Terms.
            </p>
            <p class="text-gray-600 dark:text-gray-400 leading-relaxed mb-4">
              If you wish to terminate your account, you may simply discontinue using the Service or contact us to request 
              account deletion.
            </p>
            <p class="text-gray-600 dark:text-gray-400 leading-relaxed">
              All provisions of the Terms which by their nature should survive termination shall survive termination, including, 
              without limitation, ownership provisions, warranty disclaimers, indemnity and limitations of liability.
            </p>
          </section>

          <section class="mb-12">
            <h2 class="text-3xl font-bold text-gray-900 dark:text-gray-100 mb-4">8. Disclaimer</h2>
            <p class="text-gray-600 dark:text-gray-400 leading-relaxed mb-4">
              The information on the Service is provided on an "as is" basis. To the fullest extent permitted by law, this 
              Service:
            </p>
            <ul class="list-disc pl-6 space-y-2 text-gray-600 dark:text-gray-400 mb-4">
              <li>Excludes all representations and warranties relating to this Service and its contents</li>
              <li>Excludes all liability for damages arising out of or in connection with your use of this Service</li>
            </ul>
            <p class="text-gray-600 dark:text-gray-400 leading-relaxed">
              This includes, without limitation, direct loss, loss of business or profits (whether or not the loss of such 
              profits was foreseeable, arose in the normal course of things or you have advised us of the possibility of 
              such potential loss), damage caused to your computer, computer software, systems and programs and the data 
              thereon or any other direct or indirect, consequential and incidental damages.
            </p>
          </section>

          <section class="mb-12">
            <h2 class="text-3xl font-bold text-gray-900 dark:text-gray-100 mb-4">9. Limitation of Liability</h2>
            <p class="text-gray-600 dark:text-gray-400 leading-relaxed mb-4">
              In no event shall {{ cookiecutter.project_name }}, nor its directors, employees, partners, agents, suppliers, 
              or affiliates, be liable for any indirect, incidental, special, consequential, or punitive damages, including 
              without limitation, loss of profits, data, use, goodwill, or other intangible losses, resulting from:
            </p>
            <ul class="list-disc pl-6 space-y-2 text-gray-600 dark:text-gray-400">
              <li>Your use or inability to use the Service</li>
              <li>Any unauthorized access to or use of our servers and/or any personal information stored therein</li>
              <li>Any interruption or cessation of transmission to or from the Service</li>
              <li>Any bugs, viruses, trojan horses, or the like that may be transmitted to or through our Service by any third party</li>
              <li>Any errors or omissions in any content or for any loss or damage incurred as a result of the use of any content</li>
            </ul>
          </section>

          <section class="mb-12">
            <h2 class="text-3xl font-bold text-gray-900 dark:text-gray-100 mb-4">10. Indemnification</h2>
            <p class="text-gray-600 dark:text-gray-400 leading-relaxed">
              You agree to defend, indemnify, and hold harmless {{ cookiecutter.project_name }}, its affiliates, licensors, 
              and service providers, and its and their respective officers, directors, employees, contractors, agents, licensors, 
              suppliers, successors, and assigns from and against any claims, liabilities, damages, judgments, awards, losses, 
              costs, expenses, or fees (including reasonable attorneys' fees) arising out of or relating to your violation 
              of these Terms of Service or your use of the Service.
            </p>
          </section>

          <section class="mb-12">
            <h2 class="text-3xl font-bold text-gray-900 dark:text-gray-100 mb-4">11. Governing Law</h2>
            <p class="text-gray-600 dark:text-gray-400 leading-relaxed mb-4">
              These Terms shall be governed and construed in accordance with the laws of [Your Jurisdiction], without regard 
              to its conflict of law provisions. Our failure to enforce any right or provision of these Terms will not be 
              considered a waiver of those rights.
            </p>
            <p class="text-gray-600 dark:text-gray-400 leading-relaxed">
              If any provision of these Terms is held to be invalid or unenforceable by a court, the remaining provisions of 
              these Terms will remain in effect. These Terms constitute the entire agreement between us regarding our Service, 
              and supersede and replace any prior agreements we might have had between us regarding the Service.
            </p>
          </section>

          <section class="mb-12">
            <h2 class="text-3xl font-bold text-gray-900 dark:text-gray-100 mb-4">12. Changes to Terms</h2>
            <p class="text-gray-600 dark:text-gray-400 leading-relaxed mb-4">
              We reserve the right, at our sole discretion, to modify or replace these Terms at any time. If a revision is 
              material, we will provide at least 30 days notice prior to any new terms taking effect. What constitutes a 
              material change will be determined at our sole discretion.
            </p>
            <p class="text-gray-600 dark:text-gray-400 leading-relaxed">
              By continuing to access or use our Service after any revisions become effective, you agree to be bound by the 
              revised terms. If you do not agree to the new terms, you are no longer authorized to use the Service.
            </p>
          </section>

          <section class="mb-12">
            <h2 class="text-3xl font-bold text-gray-900 dark:text-gray-100 mb-4">13. Contact Information</h2>
            <p class="text-gray-600 dark:text-gray-400 leading-relaxed mb-6">If you have any questions about these Terms of Service, please contact us at:</p>
            <div class="bg-gray-50 dark:bg-gray-800 rounded-lg p-6 space-y-3">
              <p class="text-gray-800 dark:text-gray-200"><strong>{{ cookiecutter.project_name }}</strong></p>
              <p class="text-gray-600 dark:text-gray-400">Email: legal@{{ cookiecutter.domain_name }}</p>
              <p class="text-gray-600 dark:text-gray-400">Address: [Your Company Address]</p>
              <p class="text-gray-600 dark:text-gray-400">Phone: [Your Phone Number]</p>
            </div>
          </section>

          <div class="mt-12 p-6 bg-gray-50 dark:bg-gray-800 rounded-lg text-sm text-gray-600 dark:text-gray-400">
            <p>
              By using this Service, you signify your acceptance of these Terms of Service. If you do not agree to these 
              Terms of Service, please do not use our Service. Your continued use of the Service following the posting of 
              changes to these terms will be deemed your acceptance of those changes.
            </p>
          </div>
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

