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
    <BaseSpinner 
      v-if="loading" 
      :size="size === 'sm' || size === 'xs' ? 'sm' : 'md'"
      class="mr-2"
    />
    <span v-if="icon && iconPosition === 'left'" class="mr-2">
      <component :is="icon" :class="iconClasses" />
    </span>
    <span>
      <slot />
    </span>
    <span v-if="icon && iconPosition === 'right'" class="ml-2">
      <component :is="icon" :class="iconClasses" />
    </span>
  </component>
</template>

<script setup {% if cookiecutter.use_typescript == 'y' %}lang="ts"{% endif %}>
import { computed{% if cookiecutter.use_typescript == 'y' %}, type PropType{% endif %} } from 'vue'
import { RouterLink } from 'vue-router'
import BaseSpinner from './BaseSpinner.vue'

{% if cookiecutter.use_typescript == 'y' -%}
type ButtonVariant = 'primary' | 'secondary' | 'danger' | 'ghost' | 'link'
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
      ['primary', 'secondary', 'danger', 'ghost', 'link'].includes(value)
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
  const classes = [
    'inline-flex',
    'items-center',
    'justify-center',
    'font-medium',
    'transition-all',
    'duration-200',
    'focus:outline-none',
    'focus:ring-2',
    'focus:ring-offset-2',
    'disabled:opacity-50',
    'disabled:cursor-not-allowed'
  ]
  
  // Size classes
  const sizeClasses = {
    xs: ['px-2', 'py-1', 'text-xs'],
    sm: ['px-3', 'py-1.5', 'text-sm'],
    md: ['px-4', 'py-2', 'text-base'],
    lg: ['px-6', 'py-3', 'text-lg'],
    xl: ['px-8', 'py-4', 'text-xl']
  }
  classes.push(...sizeClasses[props.size])
  
  // Rounded
  if (props.rounded) {
    classes.push('rounded-full')
  } else {
    classes.push('rounded-lg')
  }
  
  // Block
  if (props.block) {
    classes.push('w-full')
  }
  
  // Variant classes
  if (props.outlined) {
    // Outlined variants
    const outlinedVariants = {
      primary: [
        'bg-transparent',
        'text-emerald-600',
        'border-2',
        'border-emerald-600',
        'hover:bg-emerald-600',
        'hover:text-white',
        'focus:ring-emerald-500',
        'dark:text-emerald-400',
        'dark:border-emerald-400',
        'dark:hover:bg-emerald-500',
        'dark:focus:ring-emerald-400'
      ],
      secondary: [
        'bg-transparent',
        'text-gray-700',
        'border-2',
        'border-gray-300',
        'hover:bg-gray-100',
        'focus:ring-gray-500',
        'dark:text-gray-300',
        'dark:border-gray-600',
        'dark:hover:bg-gray-800',
        'dark:focus:ring-gray-400'
      ],
      danger: [
        'bg-transparent',
        'text-red-600',
        'border-2',
        'border-red-600',
        'hover:bg-red-600',
        'hover:text-white',
        'focus:ring-red-500',
        'dark:text-red-400',
        'dark:border-red-400',
        'dark:hover:bg-red-500',
        'dark:focus:ring-red-400'
      ],
      ghost: [
        'bg-transparent',
        'text-gray-600',
        'border-2',
        'border-transparent',
        'hover:bg-gray-100',
        'focus:ring-gray-500',
        'dark:text-gray-400',
        'dark:hover:bg-gray-800',
        'dark:focus:ring-gray-400'
      ],
      link: [
        'bg-transparent',
        'text-emerald-600',
        'border-transparent',
        'hover:text-emerald-700',
        'underline',
        'focus:ring-emerald-500',
        'dark:text-emerald-400',
        'dark:hover:text-emerald-300',
        'dark:focus:ring-emerald-400'
      ]
    }
    classes.push(...(outlinedVariants[props.variant] || outlinedVariants.primary))
  } else {
    // Solid variants
    const solidVariants = {
      primary: [
        'bg-emerald-600',
        'text-white',
        'hover:bg-emerald-700',
        'focus:ring-emerald-500',
        'dark:bg-emerald-500',
        'dark:hover:bg-emerald-600',
        'dark:focus:ring-emerald-400'
      ],
      secondary: [
        'bg-gray-100',
        'text-gray-700',
        'hover:bg-gray-200',
        'focus:ring-gray-500',
        'dark:bg-gray-700',
        'dark:text-gray-200',
        'dark:hover:bg-gray-600',
        'dark:focus:ring-gray-400'
      ],
      danger: [
        'bg-red-600',
        'text-white',
        'hover:bg-red-700',
        'focus:ring-red-500',
        'dark:bg-red-500',
        'dark:hover:bg-red-600',
        'dark:focus:ring-red-400'
      ],
      ghost: [
        'bg-transparent',
        'text-gray-600',
        'hover:text-gray-900',
        'hover:bg-gray-100',
        'focus:ring-gray-500',
        'dark:text-gray-400',
        'dark:hover:text-gray-100',
        'dark:hover:bg-gray-800',
        'dark:focus:ring-gray-400'
      ],
      link: [
        'bg-transparent',
        'text-emerald-600',
        'hover:text-emerald-700',
        'underline',
        'focus:ring-emerald-500',
        'dark:text-emerald-400',
        'dark:hover:text-emerald-300',
        'dark:focus:ring-emerald-400'
      ]
    }
    classes.push(...(solidVariants[props.variant] || solidVariants.primary))
  }
  
  // Loading state
  if (props.loading) {
    classes.push('cursor-wait')
  }
  
  // Focus offset for dark mode
  classes.push('dark:focus:ring-offset-gray-900')
  
  return classes
})

const iconClasses = computed(() => {
  const sizes = {
    xs: 'w-3 h-3',
    sm: 'w-4 h-4',
    md: 'w-5 h-5',
    lg: 'w-6 h-6',
    xl: 'w-7 h-7'
  }
  return sizes[props.size] || sizes.md
})

const handleClick = (event{% if cookiecutter.use_typescript == 'y' %}: MouseEvent{% endif %}) => {
  if (!props.disabled && !props.loading) {
    emit('click', event)
  }
}
</script>

{% if cookiecutter.css_framework == 'tailwind' -%}
<!-- Using only Tailwind utility classes, no custom CSS needed -->
{%- endif %}