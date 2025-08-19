<template>
  <div class="w-full">
    <label v-if="label" :for="inputId" class="form-label">
      {% raw %}{{ label }}{% endraw %}
      <span v-if="required" class="text-red-500 dark:text-red-400">*</span>
    </label>
    <div class="relative">
      <div v-if="$slots.prefix || prefix" class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
        <slot name="prefix">{% raw %}{{ prefix }}{% endraw %}</slot>
      </div>
      <input
        :id="inputId"
        ref="inputRef"
        v-model="inputValue"
        :type="type"
        :name="name"
        :placeholder="placeholder"
        :disabled="disabled"
        :readonly="readonly"
        :required="required"
        :min="min"
        :max="max"
        :step="step"
        :minlength="minlength"
        :maxlength="maxlength"
        :pattern="pattern"
        :autocomplete="autocomplete"
        :autofocus="autofocus"
        :class="inputClasses"
        @input="handleInput"
        @change="handleChange"
        @blur="handleBlur"
        @focus="handleFocus"
        @keydown="handleKeydown"
      />
      <div v-if="clearable && inputValue" class="absolute inset-y-0 right-0 flex items-center pr-3">
        <button
          type="button"
          class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 focus:outline-none"
          @click="clearInput"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
      <div v-else-if="$slots.suffix || suffix" class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
        <slot name="suffix">{% raw %}{{ suffix }}{% endraw %}</slot>
      </div>
      <div v-if="loading" class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
        <BaseSpinner size="sm" color="gray" />
      </div>
    </div>
    <div v-if="error || hint" class="mt-1">
      <span v-if="error" class="form-error">{% raw %}{{ error }}{% endraw %}</span>
      <span v-else-if="hint" class="form-helper">{% raw %}{{ hint }}{% endraw %}</span>
    </div>
  </div>
</template>

<script setup {% if cookiecutter.use_typescript == 'y' %}lang="ts"{% endif %}>
import { ref, computed, watch, onMounted{% if cookiecutter.use_typescript == 'y' %}, type PropType{% endif %} } from 'vue'
import BaseSpinner from './BaseSpinner.vue'

{% if cookiecutter.use_typescript == 'y' -%}
type InputType = 'text' | 'email' | 'password' | 'number' | 'tel' | 'url' | 'search' | 'date' | 'time' | 'datetime-local' | 'month' | 'week' | 'color'

interface Props {
  modelValue?: string | number | null
  type?: InputType
  label?: string
  name?: string
  placeholder?: string
  disabled?: boolean
  readonly?: boolean
  required?: boolean
  error?: string
  hint?: string
  prefix?: string
  suffix?: string
  clearable?: boolean
  loading?: boolean
  autofocus?: boolean
  autocomplete?: string
  min?: string | number
  max?: string | number
  step?: string | number
  minlength?: number
  maxlength?: number
  pattern?: string
}
{%- endif %}

const props = defineProps({
  modelValue: {
    type: [String, Number],
    default: ''
  },
  type: {
    type: String{% if cookiecutter.use_typescript == 'y' %} as PropType<InputType>{% endif %},
    default: 'text',
    validator: (value{% if cookiecutter.use_typescript == 'y' %}: string{% endif %}) => 
      ['text', 'email', 'password', 'number', 'tel', 'url', 'search', 'date', 'time', 'datetime-local', 'month', 'week', 'color'].includes(value)
  },
  label: {
    type: String,
    default: null
  },
  name: {
    type: String,
    default: null
  },
  placeholder: {
    type: String,
    default: null
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
  clearable: {
    type: Boolean,
    default: false
  },
  loading: {
    type: Boolean,
    default: false
  },
  autofocus: {
    type: Boolean,
    default: false
  },
  autocomplete: {
    type: String,
    default: 'off'
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
  minlength: {
    type: Number,
    default: null
  },
  maxlength: {
    type: Number,
    default: null
  },
  pattern: {
    type: String,
    default: null
  }
})

const emit = defineEmits<{
  'update:modelValue': [value: string | number]
  input: [value: string | number]
  change: [value: string | number]
  blur: [event: FocusEvent]
  focus: [event: FocusEvent]
  keydown: [event: KeyboardEvent]
  clear: []
}>()

const inputRef = ref<HTMLInputElement>()
const inputValue = ref(props.modelValue)
const inputId = computed(() => props.name || `input-${Math.random().toString(36).substr(2, 9)}`)

const inputClasses = computed(() => {
  const classes = [
    'w-full',
    'px-3',
    'py-2',
    'border',
    'rounded-lg',
    'transition-colors',
    'duration-200',
    'bg-white',
    'dark:bg-gray-800',
    'text-gray-900',
    'dark:text-gray-100',
    'placeholder-gray-400',
    'dark:placeholder-gray-500',
    'focus:outline-none',
    'focus:ring-2',
    'focus:ring-emerald-500',
    'dark:focus:ring-emerald-400',
    'disabled:opacity-50',
    'disabled:cursor-not-allowed',
    'disabled:bg-gray-50',
    'dark:disabled:bg-gray-900'
  ]
  
  // Add padding for prefix/suffix
  if (props.prefix || props.$slots.prefix) {
    classes.push('pl-10')
  }
  if (props.suffix || props.$slots.suffix || props.clearable || props.loading) {
    classes.push('pr-10')
  }
  
  // Error state
  if (props.error) {
    classes.push(
      'border-red-500',
      'dark:border-red-400',
      'focus:border-red-500',
      'dark:focus:border-red-400',
      'focus:ring-red-500',
      'dark:focus:ring-red-400'
    )
  } else {
    classes.push(
      'border-gray-300',
      'dark:border-gray-600',
      'focus:border-emerald-500',
      'dark:focus:border-emerald-400'
    )
  }
  
  return classes
})

watch(() => props.modelValue, (newValue) => {
  inputValue.value = newValue
})

watch(inputValue, (newValue) => {
  emit('update:modelValue', newValue)
})

const handleInput = (event{% if cookiecutter.use_typescript == 'y' %}: Event{% endif %}) => {
  const target = event.target as HTMLInputElement
  inputValue.value = target.value
  emit('input', target.value)
}

const handleChange = (event{% if cookiecutter.use_typescript == 'y' %}: Event{% endif %}) => {
  const target = event.target as HTMLInputElement
  emit('change', target.value)
}

const handleBlur = (event{% if cookiecutter.use_typescript == 'y' %}: FocusEvent{% endif %}) => {
  emit('blur', event)
}

const handleFocus = (event{% if cookiecutter.use_typescript == 'y' %}: FocusEvent{% endif %}) => {
  emit('focus', event)
}

const handleKeydown = (event{% if cookiecutter.use_typescript == 'y' %}: KeyboardEvent{% endif %}) => {
  emit('keydown', event)
}

const clearInput = () => {
  inputValue.value = ''
  emit('clear')
  inputRef.value?.focus()
}

const focus = () => {
  inputRef.value?.focus()
}

const blur = () => {
  inputRef.value?.blur()
}

onMounted(() => {
  if (props.autofocus) {
    focus()
  }
})

defineExpose({
  focus,
  blur,
  inputRef
})
</script>

{% if cookiecutter.css_framework == 'tailwind' -%}
<!-- Using only Tailwind utility classes, no custom CSS needed -->
{%- endif %}