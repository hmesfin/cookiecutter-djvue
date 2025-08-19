<template>
  <div class="select-wrapper" :class="wrapperClasses">
    <label v-if="label" :for="selectId" class="select-label">
      {% raw %}{{ label }}{% endraw %}
      <span v-if="required" class="select-required">*</span>
    </label>
    
    <div class="select-container">
      <select
        :id="selectId"
        ref="selectRef"
        v-model="modelValue"
        :name="name"
        :disabled="disabled"
        :required="required"
        :multiple="multiple"
        class="select-field"
        :class="selectClasses"
        @change="handleChange"
        @blur="handleBlur"
        @focus="handleFocus"
      >
        <option v-if="placeholder && !multiple" :value="null" disabled>
          {% raw %}{{ placeholder }}{% endraw %}
        </option>
        <option
          v-for="option in normalizedOptions"
          :key="option.value"
          :value="option.value"
          :disabled="option.disabled"
        >
          {% raw %}{{ option.label }}{% endraw %}
        </option>
      </select>
      
      <span class="select-icon">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <path d="M19 9l-7 7-7-7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </span>
    </div>
    
    <div v-if="hint || error" class="select-message">
      <span v-if="error" class="select-error">{% raw %}{{ error }}{% endraw %}</span>
      <span v-else-if="hint" class="select-hint">{% raw %}{{ hint }}{% endraw %}</span>
    </div>
  </div>
</template>

<script setup {% if cookiecutter.use_typescript == 'y' %}lang="ts"{% endif %}>
import { ref, computed{% if cookiecutter.use_typescript == 'y' %}, type PropType{% endif %} } from 'vue'

{% if cookiecutter.use_typescript == 'y' -%}
type SelectSize = 'sm' | 'md' | 'lg'
type SelectVariant = 'default' | 'filled' | 'outlined'

interface SelectOption {
  label: string
  value: string | number
  disabled?: boolean
}

interface Props {
  modelValue?: string | number | Array<string | number> | null
  options?: Array<SelectOption | string | number>
  name?: string
  label?: string
  placeholder?: string
  size?: SelectSize
  variant?: SelectVariant
  disabled?: boolean
  required?: boolean
  multiple?: boolean
  error?: string
  hint?: string
}
{%- endif %}

const props = defineProps({
  modelValue: {
    type: [String, Number, Array]{% if cookiecutter.use_typescript == 'y' %} as PropType<string | number | Array<string | number> | null>{% endif %},
    default: null
  },
  options: {
    type: Array{% if cookiecutter.use_typescript == 'y' %} as PropType<Array<SelectOption | string | number>>{% endif %},
    default: () => []
  },
  name: {
    type: String,
    default: null
  },
  label: {
    type: String,
    default: null
  },
  placeholder: {
    type: String,
    default: 'Select an option'
  },
  size: {
    type: String{% if cookiecutter.use_typescript == 'y' %} as PropType<SelectSize>{% endif %},
    default: 'md',
    validator: (value{% if cookiecutter.use_typescript == 'y' %}: string{% endif %}) => ['sm', 'md', 'lg'].includes(value)
  },
  variant: {
    type: String{% if cookiecutter.use_typescript == 'y' %} as PropType<SelectVariant>{% endif %},
    default: 'default',
    validator: (value{% if cookiecutter.use_typescript == 'y' %}: string{% endif %}) => ['default', 'filled', 'outlined'].includes(value)
  },
  disabled: {
    type: Boolean,
    default: false
  },
  required: {
    type: Boolean,
    default: false
  },
  multiple: {
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
  'update:modelValue': [value: string | number | Array<string | number> | null]
  'change': [value: string | number | Array<string | number> | null]
  'blur': [event: FocusEvent]
  'focus': [event: FocusEvent]
}>()

const selectRef = ref<HTMLSelectElement>()
const selectId = computed(() => `select-${Math.random().toString(36).substr(2, 9)}`)

const modelValue = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const normalizedOptions = computed(() => {
  return props.options.map(option => {
    if (typeof option === 'object' && option !== null && 'label' in option) {
      return option as {% if cookiecutter.use_typescript == 'y' %}SelectOption{% else %}any{% endif %}
    }
    return {
      label: String(option),
      value: option,
      disabled: false
    }
  })
})

const wrapperClasses = computed(() => {
  return [
    `select-wrapper-${props.size}`,
    `select-wrapper-${props.variant}`,
    {
      'select-wrapper-disabled': props.disabled,
      'select-wrapper-error': props.error
    }
  ]
})

const selectClasses = computed(() => {
  return [
    `select-${props.size}`,
    `select-${props.variant}`,
    {
      'select-error': props.error,
      'select-disabled': props.disabled
    }
  ]
})

const handleChange = (event{% if cookiecutter.use_typescript == 'y' %}: Event{% endif %}) => {
  const target = event.target as HTMLSelectElement
  let value{% if cookiecutter.use_typescript == 'y' %}: string | number | Array<string | number> | null{% endif %}
  
  if (props.multiple) {
    value = Array.from(target.selectedOptions).map(option => {
      const val = option.value
      return isNaN(Number(val)) ? val : Number(val)
    })
  } else {
    value = target.value === 'null' ? null : (isNaN(Number(target.value)) ? target.value : Number(target.value))
  }
  
  emit('change', value)
}

const handleBlur = (event{% if cookiecutter.use_typescript == 'y' %}: FocusEvent{% endif %}) => {
  emit('blur', event)
}

const handleFocus = (event{% if cookiecutter.use_typescript == 'y' %}: FocusEvent{% endif %}) => {
  emit('focus', event)
}

// Expose methods for parent components
defineExpose({
  focus: () => selectRef.value?.focus(),
  blur: () => selectRef.value?.blur()
})
</script>

<style scoped>
{% if cookiecutter.css_framework == 'tailwind' -%}
.select-wrapper {
  @apply relative;
}

.select-label {
  @apply block text-sm font-medium text-gray-700 mb-1;
}

.select-required {
  @apply text-red-500 ml-1;
}

.select-container {
  @apply relative;
}

.select-field {
  @apply w-full border rounded-md shadow-sm transition-colors duration-200 appearance-none pr-10;
  @apply focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500;
}

/* Size variants */
.select-sm { @apply px-3 py-1.5 text-sm; }
.select-md { @apply px-4 py-2 text-base; }
.select-lg { @apply px-4 py-3 text-lg; }

/* Style variants */
.select-default { @apply bg-white border-gray-300; }
.select-filled { @apply bg-gray-100 border-gray-300; }
.select-outlined { @apply bg-transparent border-gray-300 border-2; }

/* States */
.select-error { @apply border-red-500 focus:ring-red-500 focus:border-red-500; }
.select-disabled { @apply bg-gray-100 cursor-not-allowed opacity-60; }

/* Icon */
.select-icon {
  @apply absolute right-2 top-1/2 -translate-y-1/2 pointer-events-none text-gray-400;
}

/* Messages */
.select-message {
  @apply mt-1 text-sm;
}

.select-error { @apply text-red-600; }
.select-hint { @apply text-gray-500; }
{% else -%}
.select-wrapper {
  position: relative;
  margin-bottom: 1rem;
}

.select-label {
  display: block;
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
  margin-bottom: 0.25rem;
}

.select-required {
  color: #ef4444;
  margin-left: 0.25rem;
}

.select-container {
  position: relative;
}

.select-field {
  width: 100%;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  transition: all 0.2s;
  appearance: none;
  padding-right: 2.5rem;
  background-color: white;
}

.select-field:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

/* Size variants */
.select-sm { padding: 0.375rem 0.75rem; font-size: 0.875rem; }
.select-md { padding: 0.5rem 1rem; font-size: 1rem; }
.select-lg { padding: 0.75rem 1rem; font-size: 1.125rem; }

/* Style variants */
.select-filled { background-color: #f9fafb; }
.select-outlined { background-color: transparent; border-width: 2px; }

/* States */
.select-error { border-color: #ef4444; }
.select-error:focus { border-color: #ef4444; box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1); }
.select-disabled { background-color: #f3f4f6; cursor: not-allowed; opacity: 0.6; }

/* Icon */
.select-icon {
  position: absolute;
  right: 0.5rem;
  top: 50%;
  transform: translateY(-50%);
  pointer-events: none;
  color: #9ca3af;
}

/* Messages */
.select-message { margin-top: 0.25rem; font-size: 0.875rem; }
.select-error { color: #ef4444; }
.select-hint { color: #6b7280; }
{%- endif %}
</style>