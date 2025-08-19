<template>
  <div class="checkbox-wrapper" :class="wrapperClasses">
    <label class="checkbox-label">
      <input
        ref="checkboxRef"
        v-model="modelValue"
        type="checkbox"
        :name="name"
        :value="value"
        :disabled="disabled"
        :required="required"
        :indeterminate="indeterminate"
        class="checkbox-input"
        @change="handleChange"
      />
      <span class="checkbox-box">
        <svg v-if="checked" class="checkbox-icon" viewBox="0 0 24 24">
          <path v-if="indeterminate" d="M5 12h14" stroke="currentColor" stroke-width="3" stroke-linecap="round"/>
          <path v-else d="M5 13l4 4L19 7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
        </svg>
      </span>
      <span v-if="label || $slots.default" class="checkbox-text">
        <slot>{% raw %}{{ label }}{% endraw %}</slot>
      </span>
    </label>
    <div v-if="hint || error" class="checkbox-message">
      <span v-if="error" class="checkbox-error">{% raw %}{{ error }}{% endraw %}</span>
      <span v-else-if="hint" class="checkbox-hint">{% raw %}{{ hint }}{% endraw %}</span>
    </div>
  </div>
</template>

<script setup {% if cookiecutter.use_typescript == 'y' %}lang="ts"{% endif %}>
import { ref, computed, watch{% if cookiecutter.use_typescript == 'y' %}, type PropType{% endif %} } from 'vue'

{% if cookiecutter.use_typescript == 'y' -%}
type CheckboxSize = 'sm' | 'md' | 'lg'

interface Props {
  modelValue?: boolean | Array<any>
  value?: any
  name?: string
  label?: string
  size?: CheckboxSize
  disabled?: boolean
  required?: boolean
  indeterminate?: boolean
  error?: string
  hint?: string
}
{%- endif %}

const props = defineProps({
  modelValue: {
    type: [Boolean, Array]{% if cookiecutter.use_typescript == 'y' %} as PropType<boolean | Array<any>>{% endif %},
    default: false
  },
  value: {
    type: null,
    default: null
  },
  name: {
    type: String,
    default: null
  },
  label: {
    type: String,
    default: null
  },
  size: {
    type: String{% if cookiecutter.use_typescript == 'y' %} as PropType<CheckboxSize>{% endif %},
    default: 'md',
    validator: (value{% if cookiecutter.use_typescript == 'y' %}: string{% endif %}) => ['sm', 'md', 'lg'].includes(value)
  },
  disabled: {
    type: Boolean,
    default: false
  },
  required: {
    type: Boolean,
    default: false
  },
  indeterminate: {
    type: Boolean,
    default: false
  },
  error: {
    type: String,
    default: null
  },
  hint: {
    type: String,
    default: null
  }
})

const emit = defineEmits<{
  'update:modelValue': [value: boolean | Array<any>]
  'change': [value: boolean | Array<any>]
}>()

const checkboxRef = ref<HTMLInputElement>()

const modelValue = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const checked = computed(() => {
  if (Array.isArray(props.modelValue)) {
    return props.modelValue.includes(props.value)
  }
  return props.modelValue
})

const wrapperClasses = computed(() => {
  return [
    `checkbox-${props.size}`,
    {
      'checkbox-disabled': props.disabled,
      'checkbox-error': props.error
    }
  ]
})

const handleChange = (event{% if cookiecutter.use_typescript == 'y' %}: Event{% endif %}) => {
  const target = event.target as HTMLInputElement
  let value{% if cookiecutter.use_typescript == 'y' %}: boolean | Array<any>{% endif %}
  
  if (Array.isArray(props.modelValue)) {
    const arr = [...props.modelValue]
    const index = arr.indexOf(props.value)
    if (target.checked && index === -1) {
      arr.push(props.value)
    } else if (!target.checked && index > -1) {
      arr.splice(index, 1)
    }
    value = arr
  } else {
    value = target.checked
  }
  
  emit('change', value)
}

// Set indeterminate state
watch(() => props.indeterminate, (val) => {
  if (checkboxRef.value) {
    checkboxRef.value.indeterminate = val
  }
}, { immediate: true })

// Expose methods
defineExpose({
  focus: () => checkboxRef.value?.focus()
})
</script>

<style scoped>
{% if cookiecutter.css_framework == 'tailwind' -%}
.checkbox-wrapper {
  @apply relative;
}

.checkbox-label {
  @apply flex items-center cursor-pointer;
}

.checkbox-input {
  @apply sr-only;
}

.checkbox-box {
  @apply relative inline-flex items-center justify-center border-2 border-gray-300 rounded transition-all;
  @apply bg-white;
}

.checkbox-input:checked ~ .checkbox-box {
  @apply bg-blue-600 border-blue-600;
}

.checkbox-input:focus ~ .checkbox-box {
  @apply ring-2 ring-blue-500 ring-offset-2;
}

.checkbox-input:disabled ~ .checkbox-box {
  @apply bg-gray-100 border-gray-300 cursor-not-allowed opacity-60;
}

/* Size variants */
.checkbox-sm .checkbox-box { @apply w-4 h-4; }
.checkbox-md .checkbox-box { @apply w-5 h-5; }
.checkbox-lg .checkbox-box { @apply w-6 h-6; }

.checkbox-sm .checkbox-text { @apply text-sm ml-2; }
.checkbox-md .checkbox-text { @apply text-base ml-2; }
.checkbox-lg .checkbox-text { @apply text-lg ml-3; }

/* Icon */
.checkbox-icon {
  @apply absolute inset-0 text-white;
}

/* Text */
.checkbox-text {
  @apply select-none;
}

.checkbox-disabled .checkbox-text {
  @apply opacity-60;
}

/* Messages */
.checkbox-message {
  @apply mt-1 text-sm ml-7;
}

.checkbox-error { @apply text-red-600; }
.checkbox-hint { @apply text-gray-500; }

/* Error state */
.checkbox-error .checkbox-box {
  @apply border-red-500;
}
{% else -%}
.checkbox-wrapper {
  position: relative;
  margin-bottom: 0.5rem;
}

.checkbox-label {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.checkbox-input {
  position: absolute;
  opacity: 0;
  width: 0;
  height: 0;
}

.checkbox-box {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border: 2px solid #d1d5db;
  border-radius: 0.25rem;
  background-color: white;
  transition: all 0.2s;
}

.checkbox-input:checked ~ .checkbox-box {
  background-color: #3b82f6;
  border-color: #3b82f6;
}

.checkbox-input:focus ~ .checkbox-box {
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.checkbox-input:disabled ~ .checkbox-box {
  background-color: #f3f4f6;
  border-color: #d1d5db;
  cursor: not-allowed;
  opacity: 0.6;
}

/* Size variants */
.checkbox-sm .checkbox-box { width: 1rem; height: 1rem; }
.checkbox-md .checkbox-box { width: 1.25rem; height: 1.25rem; }
.checkbox-lg .checkbox-box { width: 1.5rem; height: 1.5rem; }

.checkbox-sm .checkbox-text { font-size: 0.875rem; margin-left: 0.5rem; }
.checkbox-md .checkbox-text { font-size: 1rem; margin-left: 0.5rem; }
.checkbox-lg .checkbox-text { font-size: 1.125rem; margin-left: 0.75rem; }

/* Icon */
.checkbox-icon {
  position: absolute;
  inset: 0;
  color: white;
}

/* Text */
.checkbox-text {
  user-select: none;
}

.checkbox-disabled .checkbox-text {
  opacity: 0.6;
}

/* Messages */
.checkbox-message {
  margin-top: 0.25rem;
  font-size: 0.875rem;
  margin-left: 1.75rem;
}

.checkbox-error { color: #ef4444; }
.checkbox-hint { color: #6b7280; }
{%- endif %}
</style>