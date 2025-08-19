<template>
  <span class="spinner" :class="spinnerClasses" :style="spinnerStyles">
    <svg
      class="spinner-svg"
      :width="size"
      :height="size"
      viewBox="0 0 24 24"
      xmlns="http://www.w3.org/2000/svg"
    >
      <circle
        class="spinner-circle"
        cx="12"
        cy="12"
        r="10"
        stroke="currentColor"
        stroke-width="3"
        fill="none"
      />
    </svg>
  </span>
</template>

<script setup {% if cookiecutter.use_typescript == 'y' %}lang="ts"{% endif %}>
import { computed{% if cookiecutter.use_typescript == 'y' %}, type PropType{% endif %} } from 'vue'

{% if cookiecutter.use_typescript == 'y' -%}
type SpinnerSize = 'xs' | 'sm' | 'md' | 'lg' | 'xl' | number
type SpinnerColor = 'primary' | 'secondary' | 'success' | 'danger' | 'warning' | 'info' | 'white' | 'currentColor' | string

interface Props {
  size?: SpinnerSize
  color?: SpinnerColor
  thickness?: number
  speed?: number
}
{%- endif %}

const props = defineProps({
  size: {
    type: [String, Number]{% if cookiecutter.use_typescript == 'y' %} as PropType<SpinnerSize>{% endif %},
    default: 'md'
  },
  color: {
    type: String{% if cookiecutter.use_typescript == 'y' %} as PropType<SpinnerColor>{% endif %},
    default: 'primary'
  },
  thickness: {
    type: Number,
    default: 3
  },
  speed: {
    type: Number,
    default: 1
  }
})

const sizeValue = computed(() => {
  if (typeof props.size === 'number') return props.size
  
  const sizes = {
    xs: 12,
    sm: 16,
    md: 20,
    lg: 24,
    xl: 32
  }
  return sizes[props.size] || 20
})

const spinnerClasses = computed(() => {
  return [`spinner-${props.color}`]
})

const spinnerStyles = computed(() => {
  return {
    '--spinner-speed': `${props.speed}s`
  }
})
</script>

<style scoped>
.spinner {
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.spinner-svg {
  animation: spin var(--spinner-speed, 1s) linear infinite;
}

.spinner-circle {
  stroke-dasharray: 62.83185307179586;
  stroke-dashoffset: 15.707963267948966;
  stroke-linecap: round;
  animation: spinner-dash var(--spinner-speed, 1s) ease-in-out infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

@keyframes spinner-dash {
  0% {
    stroke-dashoffset: 62.83185307179586;
  }
  50% {
    stroke-dashoffset: 15.707963267948966;
  }
  100% {
    stroke-dashoffset: 62.83185307179586;
  }
}

{% if cookiecutter.css_framework == 'tailwind' -%}
/* Color variants using Tailwind utilities */
.spinner-primary { @apply text-blue-600; }
.spinner-secondary { @apply text-gray-600; }
.spinner-success { @apply text-green-600; }
.spinner-danger { @apply text-red-600; }
.spinner-warning { @apply text-yellow-500; }
.spinner-info { @apply text-cyan-500; }
.spinner-white { @apply text-white; }
.spinner-currentColor { color: currentColor; }
{% else -%}
/* Color variants */
.spinner-primary { color: #3b82f6; }
.spinner-secondary { color: #6b7280; }
.spinner-success { color: #10b981; }
.spinner-danger { color: #ef4444; }
.spinner-warning { color: #f59e0b; }
.spinner-info { color: #06b6d4; }
.spinner-white { color: white; }
.spinner-currentColor { color: currentColor; }
{%- endif %}
</style>