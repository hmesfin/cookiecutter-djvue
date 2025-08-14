<template>
  <div class="mb-8">
    <div class="flex items-center justify-between">
      <div class="flex-1">
        <div v-if="showBack" class="mb-2">
          <router-link 
            :to="backLink" 
            class="inline-flex items-center gap-2 text-sm font-medium text-gray-600 hover:text-gray-900 transition-colors"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path>
            </svg>
            {% raw %}{{ backText }}{% endraw %}
          </router-link>
        </div>
        <h1 class="text-3xl font-bold text-gray-900">{% raw %}{{ title }}{% endraw %}</h1>
        <p v-if="description" class="mt-2 text-gray-600">{% raw %}{{ description }}{% endraw %}</p>
      </div>
      <div v-if="$slots.actions" class="flex items-center gap-3">
        <slot name="actions"></slot>
      </div>
    </div>
  </div>
</template>

<script setup{% if cookiecutter.use_typescript == 'y' %} lang="ts"{% endif %}>
{% if cookiecutter.use_typescript == 'y' -%}
interface Props {
  title: string
  description?: string
  showBack?: boolean
  backLink?: string
  backText?: string
}
{% endif %}

const props = defineProps({% if cookiecutter.use_typescript == 'y' %}<Props>{% endif %}{
  title: {
    type: String,
    required: true
  },
  description: {
    type: String,
    default: ''
  },
  showBack: {
    type: Boolean,
    default: false
  },
  backLink: {
    type: String,
    default: '/'
  },
  backText: {
    type: String,
    default: 'Back'
  }
})
</script>