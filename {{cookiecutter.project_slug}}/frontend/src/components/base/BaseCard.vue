<template>
  <component
    :is="interactive ? 'button' : 'div'"
    class="card"
    :class="cardClasses"
    @click="handleClick"
  >
    <div v-if="image || $slots.image" class="card-image">
      <slot name="image">
        <img :src="image" :alt="imageAlt" />
      </slot>
    </div>
    
    <div v-if="header || cardTitle || $slots.header" class="card-header">
      <slot name="header">
        <h3 v-if="cardTitle" class="card-title">{% raw %}{{ cardTitle }}{% endraw %}</h3>
        <p v-if="subtitle" class="card-subtitle">{% raw %}{{ subtitle }}{% endraw %}</p>
      </slot>
    </div>
    
    <div v-if="$slots.default" class="card-body">
      <slot />
    </div>
    
    <div v-if="$slots.footer" class="card-footer">
      <slot name="footer" />
    </div>
  </component>
</template>

<script setup {% if cookiecutter.use_typescript == 'y' %}lang="ts"{% endif %}>
import { computed{% if cookiecutter.use_typescript == 'y' %}, type PropType{% endif %} } from 'vue'

{% if cookiecutter.use_typescript == 'y' -%}
type CardVariant = 'default' | 'bordered' | 'elevated' | 'flat'
type CardPadding = 'none' | 'sm' | 'md' | 'lg'

interface Props {
  cardTitle?: string
  subtitle?: string
  image?: string
  imageAlt?: string
  header?: boolean
  variant?: CardVariant
  padding?: CardPadding
  hoverable?: boolean
  interactive?: boolean
  loading?: boolean
}
{%- endif %}

const props = defineProps({
  cardTitle: {
    type: String,
    default: null
  },
  subtitle: {
    type: String,
    default: null
  },
  image: {
    type: String,
    default: null
  },
  imageAlt: {
    type: String,
    default: ''
  },
  header: {
    type: Boolean,
    default: false
  },
  variant: {
    type: String{% if cookiecutter.use_typescript == 'y' %} as PropType<CardVariant>{% endif %},
    default: 'default',
    validator: (value{% if cookiecutter.use_typescript == 'y' %}: string{% endif %}) => ['default', 'bordered', 'elevated', 'flat'].includes(value)
  },
  padding: {
    type: String{% if cookiecutter.use_typescript == 'y' %} as PropType<CardPadding>{% endif %},
    default: 'md',
    validator: (value{% if cookiecutter.use_typescript == 'y' %}: string{% endif %}) => ['none', 'sm', 'md', 'lg'].includes(value)
  },
  hoverable: {
    type: Boolean,
    default: false
  },
  interactive: {
    type: Boolean,
    default: false
  },
  loading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits<{
  click: [event: MouseEvent]
}>()

const cardClasses = computed(() => {
  return [
    `card-${props.variant}`,
    `card-padding-${props.padding}`,
    {
      'card-hoverable': props.hoverable,
      'card-interactive': props.interactive,
      'card-loading': props.loading
    }
  ]
})

const handleClick = (event{% if cookiecutter.use_typescript == 'y' %}: MouseEvent{% endif %}) => {
  if (props.interactive) {
    emit('click', event)
  }
}
</script>

<style scoped>
{% if cookiecutter.css_framework == 'tailwind' -%}
.card {
  @apply bg-white rounded-lg overflow-hidden transition-all duration-200;
}

/* Variants */
.card-default {
  @apply shadow-sm;
}

.card-bordered {
  @apply border border-gray-200;
}

.card-elevated {
  @apply shadow-lg;
}

.card-flat {
  @apply shadow-none;
}

/* Padding */
.card-padding-none .card-header,
.card-padding-none .card-body,
.card-padding-none .card-footer {
  @apply p-0;
}

.card-padding-sm .card-header,
.card-padding-sm .card-body,
.card-padding-sm .card-footer {
  @apply p-3;
}

.card-padding-md .card-header,
.card-padding-md .card-body,
.card-padding-md .card-footer {
  @apply p-4;
}

.card-padding-lg .card-header,
.card-padding-lg .card-body,
.card-padding-lg .card-footer {
  @apply p-6;
}

/* Image */
.card-image {
  @apply relative overflow-hidden;
}

.card-image img {
  @apply w-full h-full object-cover;
}

/* Header */
.card-header {
  @apply border-b border-gray-100;
}

.card-title {
  @apply text-lg font-semibold text-gray-900;
}

.card-subtitle {
  @apply text-sm text-gray-500 mt-1;
}

/* Body */
.card-body {
  @apply text-gray-700;
}

/* Footer */
.card-footer {
  @apply border-t border-gray-100 flex items-center justify-between;
}

/* States */
.card-hoverable {
  @apply hover:shadow-lg hover:-translate-y-1;
}

.card-interactive {
  @apply cursor-pointer focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2;
}

.card-loading {
  @apply animate-pulse;
}

.card-loading .card-body {
  @apply opacity-50;
}
{% else -%}
.card {
  background-color: white;
  border-radius: 0.5rem;
  overflow: hidden;
  transition: all 0.2s;
}

/* Variants */
.card-default {
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
}

.card-bordered {
  border: 1px solid #e5e7eb;
}

.card-elevated {
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

.card-flat {
  box-shadow: none;
}

/* Padding */
.card-padding-none .card-header,
.card-padding-none .card-body,
.card-padding-none .card-footer {
  padding: 0;
}

.card-padding-sm .card-header,
.card-padding-sm .card-body,
.card-padding-sm .card-footer {
  padding: 0.75rem;
}

.card-padding-md .card-header,
.card-padding-md .card-body,
.card-padding-md .card-footer {
  padding: 1rem;
}

.card-padding-lg .card-header,
.card-padding-lg .card-body,
.card-padding-lg .card-footer {
  padding: 1.5rem;
}

/* Image */
.card-image {
  position: relative;
  overflow: hidden;
}

.card-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* Header */
.card-header {
  border-bottom: 1px solid #f3f4f6;
}

.card-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #111827;
  margin: 0;
}

.card-subtitle {
  font-size: 0.875rem;
  color: #6b7280;
  margin-top: 0.25rem;
}

/* Body */
.card-body {
  color: #374151;
}

/* Footer */
.card-footer {
  border-top: 1px solid #f3f4f6;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

/* States */
.card-hoverable:hover {
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  transform: translateY(-0.25rem);
}

.card-interactive {
  cursor: pointer;
}

.card-interactive:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.5);
}

.card-loading {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}
{%- endif %}
</style>