<template>
  <div class="input-wrapper" :class="wrapperClasses">
    <label v-if="label" :for="inputId" class="input-label">
      {{ label }}
      <span v-if="required" class="input-required">*</span>
    </label>
    
    <div class="input-container">
      <span v-if="prefix || $slots.prefix" class="input-addon input-prefix">
        <slot name="prefix">{{ prefix }}</slot>
      </span>
      
      <input
        :id="inputId"
        ref="inputRef"
        v-model="modelValue"
        :type="type"
        :name="name"
        :placeholder="placeholder"
        :disabled="disabled"
        :readonly="readonly"
        :required="required"
        :min="min"
        :max="max"
        :step="step"
        :maxlength="maxlength"
        :autocomplete="autocomplete"
        :pattern="pattern"
        class="input-field"
        :class="inputClasses"
        @input="handleInput"
        @blur="handleBlur"
        @focus="handleFocus"
        @keydown="handleKeydown"
      />
      
      <span v-if="suffix || $slots.suffix" class="input-addon input-suffix">
        <slot name="suffix">{{ suffix }}</slot>
      </span>
      
      <button
        v-if="clearable && modelValue"
        type="button"
        class="input-clear"
        @click="handleClear"
      >
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <path d="M18 6L6 18M6 6l12 12" stroke-width="2" stroke-linecap="round"/>
        </svg>
      </button>
    </div>
    
    <div v-if="hint || error" class="input-message">
      <span v-if="error" class="input-error">{{ error }}</span>
      <span v-else-if="hint" class="input-hint">{{ hint }}</span>
    </div>
  </div>
</template>

<script setup {% if cookiecutter.use_typescript == 'y' %}lang="ts"{% endif %}>
import { ref, computed, watch{% if cookiecutter.use_typescript == 'y' %}, type PropType{% endif %} } from 'vue'

{% if cookiecutter.use_typescript == 'y' -%}
type InputType = 'text' | 'email' | 'password' | 'number' | 'tel' | 'url' | 'search' | 'date' | 'time' | 'datetime-local'
type InputSize = 'sm' | 'md' | 'lg'
type InputVariant = 'default' | 'filled' | 'outlined'

interface Props {
  modelValue?: string | number | null
  type?: InputType
  name?: string
  label?: string
  placeholder?: string
  size?: InputSize
  variant?: InputVariant
  disabled?: boolean
  readonly?: boolean
  required?: boolean
  clearable?: boolean
  error?: string
  hint?: string
  prefix?: string
  suffix?: string
  min?: string | number
  max?: string | number
  step?: string | number
  maxlength?: string | number
  autocomplete?: string
  pattern?: string
}
{%- endif %}

const props = defineProps({
  modelValue: {
    type: [String, Number]{% if cookiecutter.use_typescript == 'y' %} as PropType<string | number | null>{% endif %},
    default: ''
  },
  type: {
    type: String{% if cookiecutter.use_typescript == 'y' %} as PropType<InputType>{% endif %},
    default: 'text',
    validator: (value{% if cookiecutter.use_typescript == 'y' %}: string{% endif %}) =>
      ['text', 'email', 'password', 'number', 'tel', 'url', 'search', 'date', 'time', 'datetime-local'].includes(value)
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
    default: null
  },
  size: {
    type: String{% if cookiecutter.use_typescript == 'y' %} as PropType<InputSize>{% endif %},
    default: 'md',
    validator: (value{% if cookiecutter.use_typescript == 'y' %}: string{% endif %}) => ['sm', 'md', 'lg'].includes(value)
  },
  variant: {
    type: String{% if cookiecutter.use_typescript == 'y' %} as PropType<InputVariant>{% endif %},
    default: 'default',
    validator: (value{% if cookiecutter.use_typescript == 'y' %}: string{% endif %}) => ['default', 'filled', 'outlined'].includes(value)
  },
  disabled: {
    type: Boolean,
    default: false
  },
  readonly: {
    type: Boolean,
    default: false
  },
  required: {
    type: Boolean,
    default: false
  },
  clearable: {
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
  },
  prefix: {
    type: String,
    default: null
  },
  suffix: {
    type: String,
    default: null
  },
  min: {
    type: [String, Number],
    default: null
  },
  max: {
    type: [String, Number],
    default: null
  },
  step: {
    type: [String, Number],
    default: null
  },
  maxlength: {
    type: [String, Number],
    default: null
  },
  autocomplete: {
    type: String,
    default: 'off'
  },
  pattern: {
    type: String,
    default: null
  }
})

const emit = defineEmits<{
  'update:modelValue': [value: string | number | null]
  'input': [value: string | number | null]
  'blur': [event: FocusEvent]
  'focus': [event: FocusEvent]
  'clear': []
  'keydown': [event: KeyboardEvent]
}>()

const inputRef = ref<HTMLInputElement>()
const inputId = computed(() => `input-${Math.random().toString(36).substr(2, 9)}`)

const modelValue = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const wrapperClasses = computed(() => {
  return [
    `input-wrapper-${props.size}`,
    `input-wrapper-${props.variant}`,
    {
      'input-wrapper-disabled': props.disabled,
      'input-wrapper-error': props.error,
      'input-wrapper-clearable': props.clearable
    }
  ]
})

const inputClasses = computed(() => {
  return [
    `input-${props.size}`,
    `input-${props.variant}`,
    {
      'input-error': props.error,
      'input-disabled': props.disabled,
      'input-readonly': props.readonly
    }
  ]
})

const handleInput = (event{% if cookiecutter.use_typescript == 'y' %}: Event{% endif %}) => {
  const target = event.target as HTMLInputElement
  const value = props.type === 'number' ? Number(target.value) : target.value
  emit('input', value)
}

const handleBlur = (event{% if cookiecutter.use_typescript == 'y' %}: FocusEvent{% endif %}) => {
  emit('blur', event)
}

const handleFocus = (event{% if cookiecutter.use_typescript == 'y' %}: FocusEvent{% endif %}) => {
  emit('focus', event)
}

const handleClear = () => {
  modelValue.value = ''
  emit('clear')
  inputRef.value?.focus()
}

const handleKeydown = (event{% if cookiecutter.use_typescript == 'y' %}: KeyboardEvent{% endif %}) => {
  emit('keydown', event)
}

// Expose methods for parent components
defineExpose({
  focus: () => inputRef.value?.focus(),
  blur: () => inputRef.value?.blur(),
  select: () => inputRef.value?.select()
})
</script>

<style scoped>
{% if cookiecutter.css_framework == 'tailwind' -%}
.input-wrapper {
  @apply relative;
}

.input-label {
  @apply block text-sm font-medium text-gray-700 mb-1;
}

.input-required {
  @apply text-red-500 ml-1;
}

.input-container {
  @apply relative flex items-center;
}

.input-field {
  @apply w-full border rounded-md shadow-sm transition-colors duration-200;
  @apply focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500;
}

/* Size variants */
.input-sm { @apply px-3 py-1.5 text-sm; }
.input-md { @apply px-4 py-2 text-base; }
.input-lg { @apply px-4 py-3 text-lg; }

/* Style variants */
.input-default { @apply bg-white border-gray-300; }
.input-filled { @apply bg-gray-100 border-gray-300; }
.input-outlined { @apply bg-transparent border-gray-300 border-2; }

/* States */
.input-error { @apply border-red-500 focus:ring-red-500 focus:border-red-500; }
.input-disabled { @apply bg-gray-100 cursor-not-allowed opacity-60; }
.input-readonly { @apply bg-gray-50; }

/* Addons */
.input-addon {
  @apply absolute top-0 bottom-0 flex items-center px-3 text-gray-500;
}

.input-prefix { @apply left-0; }
.input-suffix { @apply right-0; }

.input-wrapper-clearable .input-field { @apply pr-10; }
.input-clear {
  @apply absolute right-2 top-1/2 -translate-y-1/2 p-1 text-gray-400 hover:text-gray-600;
  @apply focus:outline-none;
}

/* Messages */
.input-message {
  @apply mt-1 text-sm;
}

.input-error { @apply text-red-600; }
.input-hint { @apply text-gray-500; }

/* With prefix/suffix adjustments */
.input-container:has(.input-prefix) .input-field { @apply pl-10; }
.input-container:has(.input-suffix) .input-field { @apply pr-10; }
{% else -%}
.input-wrapper {
  position: relative;
  margin-bottom: 1rem;
}

.input-label {
  display: block;
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
  margin-bottom: 0.25rem;
}

.input-required {
  color: #ef4444;
  margin-left: 0.25rem;
}

.input-container {
  position: relative;
  display: flex;
  align-items: center;
}

.input-field {
  width: 100%;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  transition: all 0.2s;
}

.input-field:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

/* Size variants */
.input-sm { padding: 0.375rem 0.75rem; font-size: 0.875rem; }
.input-md { padding: 0.5rem 1rem; font-size: 1rem; }
.input-lg { padding: 0.75rem 1rem; font-size: 1.125rem; }

/* Style variants */
.input-default { background-color: white; }
.input-filled { background-color: #f9fafb; }
.input-outlined { background-color: transparent; border-width: 2px; }

/* States */
.input-error { border-color: #ef4444; }
.input-error:focus { border-color: #ef4444; box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1); }
.input-disabled { background-color: #f3f4f6; cursor: not-allowed; opacity: 0.6; }
.input-readonly { background-color: #f9fafb; }

/* Messages */
.input-message { margin-top: 0.25rem; font-size: 0.875rem; }
.input-error { color: #ef4444; }
.input-hint { color: #6b7280; }
{%- endif %}
</style>