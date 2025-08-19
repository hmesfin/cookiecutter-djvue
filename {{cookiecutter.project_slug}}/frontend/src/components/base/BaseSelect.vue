<template>
  <div class="w-full">
    <label v-if="label" :for="selectId" class="form-label">
      {% raw %}{{ label }}{% endraw %}
      <span v-if="required" class="text-red-500 dark:text-red-400">*</span>
    </label>
    <div class="relative">
      <select
        :id="selectId"
        ref="selectRef"
        v-model="selectValue"
        :name="name"
        :disabled="disabled"
        :required="required"
        :multiple="multiple"
        :size="size"
        :class="selectClasses"
        @change="handleChange"
        @blur="handleBlur"
        @focus="handleFocus"
      >
        <option v-if="placeholder && !multiple" value="" disabled selected>
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
      <div class="absolute inset-y-0 right-0 flex items-center pr-2 pointer-events-none">
        <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
        </svg>
      </div>
      <div v-if="loading" class="absolute inset-y-0 right-8 flex items-center pr-3 pointer-events-none">
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
import { ref, computed, watch{% if cookiecutter.use_typescript == 'y' %}, type PropType{% endif %} } from 'vue'
import BaseSpinner from './BaseSpinner.vue'

{% if cookiecutter.use_typescript == 'y' -%}
interface SelectOption {
  label: string
  value: string | number
  disabled?: boolean
}

interface Props {
  modelValue?: string | number | string[] | number[] | null
  options?: (string | SelectOption)[]
  label?: string
  name?: string
  placeholder?: string
  disabled?: boolean
  required?: boolean
  multiple?: boolean
  size?: number
  error?: string
  hint?: string
  loading?: boolean
}
{%- endif %}

const props = defineProps({
  modelValue: {
    type: [String, Number, Array],
    default: null
  },
  options: {
    type: Array{% if cookiecutter.use_typescript == 'y' %} as PropType<(string | SelectOption)[]>{% endif %},
    default: () => []
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
    default: 'Select an option'
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
  size: {
    type: Number,
    default: null
  },
  error: {
    type: String,
    default: null
  },
  hint: {
    type: String,
    default: null
  },
  loading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits<{
  'update:modelValue': [value: string | number | string[] | number[] | null]
  change: [value: string | number | string[] | number[] | null]
  blur: [event: FocusEvent]
  focus: [event: FocusEvent]
}>()

const selectRef = ref<HTMLSelectElement>()
const selectValue = ref(props.modelValue)
const selectId = computed(() => props.name || `select-${Math.random().toString(36).substr(2, 9)}`)

const normalizedOptions = computed(() => {
  return props.options.map(option => {
    if (typeof option === 'string') {
      return { label: option, value: option, disabled: false }
    }
    return option
  })
})

const selectClasses = computed(() => {
  const classes = [
    'w-full',
    'px-3',
    'py-2',
    'pr-10',
    'border',
    'rounded-lg',
    'transition-colors',
    'duration-200',
    'bg-white',
    'dark:bg-gray-800',
    'text-gray-900',
    'dark:text-gray-100',
    'focus:outline-none',
    'focus:ring-2',
    'focus:ring-emerald-500',
    'dark:focus:ring-emerald-400',
    'disabled:opacity-50',
    'disabled:cursor-not-allowed',
    'disabled:bg-gray-50',
    'dark:disabled:bg-gray-900',
    'appearance-none',
    'cursor-pointer'
  ]
  
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
  selectValue.value = newValue
})

watch(selectValue, (newValue) => {
  emit('update:modelValue', newValue)
})

const handleChange = (event{% if cookiecutter.use_typescript == 'y' %}: Event{% endif %}) => {
  const target = event.target as HTMLSelectElement
  let value{% if cookiecutter.use_typescript == 'y' %}: string | number | string[] | number[] | null{% endif %}
  
  if (props.multiple) {
    value = Array.from(target.selectedOptions).map(option => option.value)
  } else {
    value = target.value || null
  }
  
  selectValue.value = value
  emit('change', value)
}

const handleBlur = (event{% if cookiecutter.use_typescript == 'y' %}: FocusEvent{% endif %}) => {
  emit('blur', event)
}

const handleFocus = (event{% if cookiecutter.use_typescript == 'y' %}: FocusEvent{% endif %}) => {
  emit('focus', event)
}

const focus = () => {
  selectRef.value?.focus()
}

const blur = () => {
  selectRef.value?.blur()
}

defineExpose({
  focus,
  blur,
  selectRef
})
</script>

{% if cookiecutter.css_framework == 'tailwind' -%}
<!-- Using only Tailwind utility classes, no custom CSS needed -->
{%- endif %}