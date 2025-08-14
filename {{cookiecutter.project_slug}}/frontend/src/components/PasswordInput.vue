  <template>
    <div class="w-full">
      <div class="relative">
        <input
          :id="id"
          :type="showPassword ? 'text' : 'password'"
          :value="modelValue"
          @input="$emit('update:modelValue', $event.target.value)"
          :placeholder="placeholder"
          :required="required"
          :autocomplete="autocomplete"
          class="w-full px-3 py-2 pr-10 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500
   bg-white dark:bg-gray-700 dark:border-gray-600 dark:text-gray-100 dark:focus:ring-indigo-400 dark:focus:border-indigo-400"
        >
        <button
          type="button"
          @click="togglePassword"
          class="absolute right-2 top-1/2 -translate-y-1/2 p-1 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 rounded
  hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors"
          :aria-label="showPassword ? 'Hide password' : 'Show password'"
        >
          <IconLucideEye v-if="!showPassword" class="w-5 h-5" />
          <IconLucideEyeOff v-else class="w-5 h-5" />
        </button>
      </div>
      <PasswordStrength v-if="showStrength" :password="modelValue" class="mt-2" />
    </div>
  </template>

<script setup{% if cookiecutter.use_typescript == 'y' %} lang="ts"{% endif %}>
import { ref } from 'vue'
import PasswordStrength from './PasswordStrength.vue'

{% if cookiecutter.use_typescript == 'y' -%}
interface Props {
  modelValue: string
  id?: string
  placeholder?: string
  required?: boolean
  autocomplete?: string
  showStrength?: boolean
}
{%- endif %}

const props = defineProps({% if cookiecutter.use_typescript == 'y' %}<Props>{% endif %}{
  modelValue: {
    type: String,
    required: true
  },
  id: {
    type: String,
    default: 'password'
  },
  placeholder: {
    type: String,
    default: 'Enter password'
  },
  required: {
    type: Boolean,
    default: false
  },
  autocomplete: {
    type: String,
    default: 'current-password'
  },
  showStrength: {
    type: Boolean,
    default: false
  }
})

defineEmits(['update:modelValue'])

const showPassword = ref(false)

const togglePassword = () => {
  showPassword.value = !showPassword.value
}
</script>