{% raw %}<template>
  <div class="relative" :class="wrapperClasses">
    <label class="flex items-center cursor-pointer" :class="{ 'cursor-not-allowed opacity-60': disabled }">
      <input
        ref="checkboxRef"
        v-model="modelValue"
        type="checkbox"
        :name="name"
        :value="value"
        :disabled="disabled"
        :required="required"
        :indeterminate="indeterminate"
        class="form-checkbox transition-colors duration-200"
        :class="[
          sizeClasses,
          {
            'border-red-500 dark:border-red-400': error
          }
        ]"
        @change="handleChange"
      />
      <span v-if="label || $slots.default" class="select-none transition-opacity duration-200" :class="[
        textSizeClasses,
        { 'opacity-60': disabled }
      ]">
        <slot>{{ label }}</slot>
      </span>
    </label>
    <div v-if="hint || error" class="mt-1 text-sm" :class="messageClasses">
      <span v-if="error" class="form-error">{{ error }}</span>
      <span v-else-if="hint" class="form-helper">{{ hint }}</span>
    </div>
  </div>
</template>{% endraw %}

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
  return {
    'mb-2': true
  }
})

const sizeClasses = computed(() => {
  const sizes = {
    sm: 'w-4 h-4',
    md: 'w-5 h-5', 
    lg: 'w-6 h-6'
  }
  return sizes[props.size]
})

const textSizeClasses = computed(() => {
  const sizes = {
    sm: 'text-sm ml-2',
    md: 'text-base ml-2',
    lg: 'text-lg ml-3'
  }
  return sizes[props.size]
})

const messageClasses = computed(() => {
  const margins = {
    sm: 'ml-6',
    md: 'ml-7', 
    lg: 'ml-9'
  }
  return margins[props.size]
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

