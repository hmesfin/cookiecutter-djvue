<template>
  <div class="password-input-wrapper">
    <div class="password-input-container">
      <input
        :id="id"
        :type="showPassword ? 'text' : 'password'"
        :value="modelValue"
        @input="$emit('update:modelValue', $event.target.value)"
        :placeholder="placeholder"
        :required="required"
        :autocomplete="autocomplete"
        class="password-input"
        :class="{ 'has-icon': true }"
      >
      <button
        type="button"
        @click="togglePassword"
        class="password-toggle"
        :aria-label="showPassword ? 'Hide password' : 'Show password'"
      >
        <svg v-if="!showPassword" class="icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
        </svg>
        <svg v-else class="icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21"></path>
        </svg>
      </button>
    </div>
    <PasswordStrength v-if="showStrength" :password="modelValue" />
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

<style scoped>
.password-input-wrapper {
  width: 100%;
}

.password-input-container {
  position: relative;
  width: 100%;
}

.password-input {
  width: 100%;
  padding: 0.5rem 2.5rem 0.5rem 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  transition: all 0.2s;
}

.password-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.dark .password-input {
  background: #374151;
  border-color: #4b5563;
  color: #f3f4f6;
}

.dark .password-input:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
}

.password-toggle {
  position: absolute;
  right: 0.5rem;
  top: 50%;
  transform: translateY(-50%);
  padding: 0.25rem;
  border: none;
  background: transparent;
  color: #6b7280;
  cursor: pointer;
  border-radius: 0.25rem;
  transition: all 0.2s;
}

.password-toggle:hover {
  color: #374151;
  background: #f3f4f6;
}

.dark .password-toggle {
  color: #9ca3af;
}

.dark .password-toggle:hover {
  color: #d1d5db;
  background: #4b5563;
}

.icon {
  width: 20px;
  height: 20px;
}
</style>