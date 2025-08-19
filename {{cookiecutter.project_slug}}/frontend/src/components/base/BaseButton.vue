<template>
  <component
    :is="componentType"
    :type="type"
    :class="buttonClasses"
    :disabled="disabled || loading"
    :to="to"
    :href="href"
    :target="target"
    @click="handleClick"
  >
    <span v-if="loading" class="btn-loader">
      <BaseSpinner :size="size" :color="spinnerColor" />
    </span>
    <span v-if="icon && iconPosition === 'left'" class="btn-icon btn-icon-left">
      <component :is="icon" :size="iconSize" />
    </span>
    <span class="btn-content">
      <slot />
    </span>
    <span v-if="icon && iconPosition === 'right'" class="btn-icon btn-icon-right">
      <component :is="icon" :size="iconSize" />
    </span>
  </component>
</template>

<script setup {% if cookiecutter.use_typescript == 'y' %}lang="ts"{% endif %}>
import { computed{% if cookiecutter.use_typescript == 'y' %}, type PropType{% endif %} } from 'vue'
import { RouterLink } from 'vue-router'
import BaseSpinner from './BaseSpinner.vue'

{% if cookiecutter.use_typescript == 'y' -%}
type ButtonVariant = 'primary' | 'secondary' | 'success' | 'danger' | 'warning' | 'info' | 'light' | 'dark' | 'ghost' | 'link'
type ButtonSize = 'xs' | 'sm' | 'md' | 'lg' | 'xl'
type ButtonType = 'button' | 'submit' | 'reset'
type IconPosition = 'left' | 'right'

interface Props {
  variant?: ButtonVariant
  size?: ButtonSize
  type?: ButtonType
  disabled?: boolean
  loading?: boolean
  block?: boolean
  rounded?: boolean
  outlined?: boolean
  icon?: any
  iconPosition?: IconPosition
  to?: string | object
  href?: string
  target?: string
}
{%- endif %}

const props = defineProps({
  variant: {
    type: String{% if cookiecutter.use_typescript == 'y' %} as PropType<ButtonVariant>{% endif %},
    default: 'primary',
    validator: (value{% if cookiecutter.use_typescript == 'y' %}: string{% endif %}) =>
      ['primary', 'secondary', 'success', 'danger', 'warning', 'info', 'light', 'dark', 'ghost', 'link'].includes(value)
  },
  size: {
    type: String{% if cookiecutter.use_typescript == 'y' %} as PropType<ButtonSize>{% endif %},
    default: 'md',
    validator: (value{% if cookiecutter.use_typescript == 'y' %}: string{% endif %}) => ['xs', 'sm', 'md', 'lg', 'xl'].includes(value)
  },
  type: {
    type: String{% if cookiecutter.use_typescript == 'y' %} as PropType<ButtonType>{% endif %},
    default: 'button',
    validator: (value{% if cookiecutter.use_typescript == 'y' %}: string{% endif %}) => ['button', 'submit', 'reset'].includes(value)
  },
  disabled: {
    type: Boolean,
    default: false
  },
  loading: {
    type: Boolean,
    default: false
  },
  block: {
    type: Boolean,
    default: false
  },
  rounded: {
    type: Boolean,
    default: false
  },
  outlined: {
    type: Boolean,
    default: false
  },
  icon: {
    type: [Object, Function],
    default: null
  },
  iconPosition: {
    type: String{% if cookiecutter.use_typescript == 'y' %} as PropType<IconPosition>{% endif %},
    default: 'left',
    validator: (value{% if cookiecutter.use_typescript == 'y' %}: string{% endif %}) => ['left', 'right'].includes(value)
  },
  to: {
    type: [String, Object],
    default: null
  },
  href: {
    type: String,
    default: null
  },
  target: {
    type: String,
    default: null
  }
})

const emit = defineEmits<{
  click: [event: MouseEvent]
}>()

const componentType = computed(() => {
  if (props.to) return RouterLink
  if (props.href) return 'a'
  return 'button'
})

const buttonClasses = computed(() => {
  const classes = ['btn', `btn-${props.variant}`, `btn-${props.size}`]
  
  if (props.block) classes.push('btn-block')
  if (props.rounded) classes.push('btn-rounded')
  if (props.outlined) classes.push('btn-outlined')
  if (props.loading) classes.push('btn-loading')
  if (props.disabled) classes.push('btn-disabled')
  
  return classes
})

const iconSize = computed(() => {
  const sizes = {
    xs: 14,
    sm: 16,
    md: 18,
    lg: 20,
    xl: 24
  }
  return sizes[props.size] || 18
})

const spinnerColor = computed(() => {
  const darkVariants = ['primary', 'secondary', 'success', 'danger', 'warning', 'info', 'dark']
  return darkVariants.includes(props.variant) ? 'white' : 'currentColor'
})

const handleClick = (event{% if cookiecutter.use_typescript == 'y' %}: MouseEvent{% endif %}) => {
  if (!props.disabled && !props.loading) {
    emit('click', event)
  }
}
</script>

<style scoped>
{% if cookiecutter.css_framework == 'tailwind' -%}
/* Tailwind CSS classes are used inline */
.btn {
  @apply inline-flex items-center justify-center font-medium transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2;
}

/* Size variants */
.btn-xs { @apply px-2 py-1 text-xs; }
.btn-sm { @apply px-3 py-1.5 text-sm; }
.btn-md { @apply px-4 py-2 text-base; }
.btn-lg { @apply px-6 py-3 text-lg; }
.btn-xl { @apply px-8 py-4 text-xl; }

/* Color variants */
.btn-primary { @apply bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-500; }
.btn-secondary { @apply bg-gray-600 text-white hover:bg-gray-700 focus:ring-gray-500; }
.btn-success { @apply bg-green-600 text-white hover:bg-green-700 focus:ring-green-500; }
.btn-danger { @apply bg-red-600 text-white hover:bg-red-700 focus:ring-red-500; }
.btn-warning { @apply bg-yellow-500 text-white hover:bg-yellow-600 focus:ring-yellow-500; }
.btn-info { @apply bg-cyan-500 text-white hover:bg-cyan-600 focus:ring-cyan-500; }
.btn-light { @apply bg-gray-100 text-gray-800 hover:bg-gray-200 focus:ring-gray-300; }
.btn-dark { @apply bg-gray-900 text-white hover:bg-gray-800 focus:ring-gray-700; }
.btn-ghost { @apply bg-transparent text-gray-700 hover:bg-gray-100 focus:ring-gray-300; }
.btn-link { @apply bg-transparent text-blue-600 hover:text-blue-700 underline focus:ring-blue-500; }

/* Outlined variants */
.btn-outlined.btn-primary { @apply bg-transparent text-blue-600 border-2 border-blue-600 hover:bg-blue-600 hover:text-white; }
.btn-outlined.btn-secondary { @apply bg-transparent text-gray-600 border-2 border-gray-600 hover:bg-gray-600 hover:text-white; }
.btn-outlined.btn-success { @apply bg-transparent text-green-600 border-2 border-green-600 hover:bg-green-600 hover:text-white; }
.btn-outlined.btn-danger { @apply bg-transparent text-red-600 border-2 border-red-600 hover:bg-red-600 hover:text-white; }

/* States */
.btn-block { @apply w-full; }
.btn-rounded { @apply rounded-full; }
.btn-disabled { @apply opacity-50 cursor-not-allowed; }
.btn-loading { @apply cursor-wait; }

/* Icon spacing */
.btn-icon-left { @apply mr-2; }
.btn-icon-right { @apply ml-2; }

/* Loader */
.btn-loader { @apply mr-2; }
{% else -%}
/* Custom CSS implementation */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-weight: 500;
  transition: all 0.2s ease;
  border: none;
  cursor: pointer;
  text-decoration: none;
  outline: none;
  position: relative;
}

.btn:focus {
  box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.5);
}

/* Size variants */
.btn-xs { padding: 0.25rem 0.5rem; font-size: 0.75rem; }
.btn-sm { padding: 0.375rem 0.75rem; font-size: 0.875rem; }
.btn-md { padding: 0.5rem 1rem; font-size: 1rem; }
.btn-lg { padding: 0.75rem 1.5rem; font-size: 1.125rem; }
.btn-xl { padding: 1rem 2rem; font-size: 1.25rem; }

/* Color variants */
.btn-primary { background-color: #3b82f6; color: white; }
.btn-primary:hover { background-color: #2563eb; }
.btn-secondary { background-color: #6b7280; color: white; }
.btn-secondary:hover { background-color: #4b5563; }
.btn-success { background-color: #10b981; color: white; }
.btn-success:hover { background-color: #059669; }
.btn-danger { background-color: #ef4444; color: white; }
.btn-danger:hover { background-color: #dc2626; }
.btn-warning { background-color: #f59e0b; color: white; }
.btn-warning:hover { background-color: #d97706; }
.btn-info { background-color: #06b6d4; color: white; }
.btn-info:hover { background-color: #0891b2; }
.btn-light { background-color: #f3f4f6; color: #1f2937; }
.btn-light:hover { background-color: #e5e7eb; }
.btn-dark { background-color: #1f2937; color: white; }
.btn-dark:hover { background-color: #111827; }
.btn-ghost { background-color: transparent; color: #4b5563; }
.btn-ghost:hover { background-color: #f3f4f6; }
.btn-link { background-color: transparent; color: #3b82f6; text-decoration: underline; }
.btn-link:hover { color: #2563eb; }

/* Outlined variants */
.btn-outlined { background-color: transparent; border: 2px solid; }
.btn-outlined.btn-primary { color: #3b82f6; border-color: #3b82f6; }
.btn-outlined.btn-primary:hover { background-color: #3b82f6; color: white; }

/* States */
.btn-block { width: 100%; }
.btn-rounded { border-radius: 9999px; }
.btn-disabled { opacity: 0.5; cursor: not-allowed; }
.btn-loading { cursor: wait; }

/* Icon spacing */
.btn-icon { display: inline-flex; align-items: center; }
.btn-icon-left { margin-right: 0.5rem; }
.btn-icon-right { margin-left: 0.5rem; }

/* Loader */
.btn-loader { margin-right: 0.5rem; display: inline-flex; }
{%- endif %}
</style>