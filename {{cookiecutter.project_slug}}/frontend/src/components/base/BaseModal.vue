<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="modelValue" class="modal-overlay" @click="handleOverlayClick">
        <div class="modal-container" :class="modalClasses" @click.stop>
          <div v-if="showHeader" class="modal-header">
            <slot name="header">
              <h2 v-if="title" class="modal-title">{{ title }}</h2>
            </slot>
            <button
              v-if="closable"
              type="button"
              class="modal-close"
              @click="close"
            >
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M18 6L6 18M6 6l12 12" stroke-width="2" stroke-linecap="round"/>
              </svg>
            </button>
          </div>
          
          <div class="modal-body" :class="bodyClasses">
            <slot />
          </div>
          
          <div v-if="$slots.footer || showFooter" class="modal-footer">
            <slot name="footer">
              <BaseButton
                v-if="showCancel"
                variant="ghost"
                @click="cancel"
              >
                {{ cancelText }}
              </BaseButton>
              <BaseButton
                v-if="showConfirm"
                :variant="confirmVariant"
                :loading="loading"
                @click="confirm"
              >
                {{ confirmText }}
              </BaseButton>
            </slot>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup {% if cookiecutter.use_typescript == 'y' %}lang="ts"{% endif %}>
import { computed, watch, onMounted, onUnmounted{% if cookiecutter.use_typescript == 'y' %}, type PropType{% endif %} } from 'vue'
import BaseButton from './BaseButton.vue'

{% if cookiecutter.use_typescript == 'y' -%}
type ModalSize = 'sm' | 'md' | 'lg' | 'xl' | 'full'
type ButtonVariant = 'primary' | 'secondary' | 'success' | 'danger' | 'warning' | 'info'

interface Props {
  modelValue?: boolean
  title?: string
  size?: ModalSize
  closable?: boolean
  closeOnOverlay?: boolean
  closeOnEsc?: boolean
  showHeader?: boolean
  showFooter?: boolean
  showCancel?: boolean
  showConfirm?: boolean
  cancelText?: string
  confirmText?: string
  confirmVariant?: ButtonVariant
  loading?: boolean
  scrollable?: boolean
  centered?: boolean
}
{%- endif %}

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  title: {
    type: String,
    default: null
  },
  size: {
    type: String{% if cookiecutter.use_typescript == 'y' %} as PropType<ModalSize>{% endif %},
    default: 'md',
    validator: (value{% if cookiecutter.use_typescript == 'y' %}: string{% endif %}) => ['sm', 'md', 'lg', 'xl', 'full'].includes(value)
  },
  closable: {
    type: Boolean,
    default: true
  },
  closeOnOverlay: {
    type: Boolean,
    default: true
  },
  closeOnEsc: {
    type: Boolean,
    default: true
  },
  showHeader: {
    type: Boolean,
    default: true
  },
  showFooter: {
    type: Boolean,
    default: false
  },
  showCancel: {
    type: Boolean,
    default: true
  },
  showConfirm: {
    type: Boolean,
    default: true
  },
  cancelText: {
    type: String,
    default: 'Cancel'
  },
  confirmText: {
    type: String,
    default: 'Confirm'
  },
  confirmVariant: {
    type: String{% if cookiecutter.use_typescript == 'y' %} as PropType<ButtonVariant>{% endif %},
    default: 'primary'
  },
  loading: {
    type: Boolean,
    default: false
  },
  scrollable: {
    type: Boolean,
    default: false
  },
  centered: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
  'close': []
  'confirm': []
  'cancel': []
}>()

const modalClasses = computed(() => {
  return [
    `modal-${props.size}`,
    {
      'modal-centered': props.centered
    }
  ]
})

const bodyClasses = computed(() => {
  return {
    'modal-body-scrollable': props.scrollable
  }
})

const close = () => {
  emit('update:modelValue', false)
  emit('close')
}

const confirm = () => {
  emit('confirm')
}

const cancel = () => {
  emit('cancel')
  close()
}

const handleOverlayClick = () => {
  if (props.closeOnOverlay && props.closable) {
    close()
  }
}

const handleEscKey = (event{% if cookiecutter.use_typescript == 'y' %}: KeyboardEvent{% endif %}) => {
  if (event.key === 'Escape' && props.closeOnEsc && props.closable && props.modelValue) {
    close()
  }
}

// Lock body scroll when modal is open
watch(() => props.modelValue, (isOpen) => {
  if (isOpen) {
    document.body.style.overflow = 'hidden'
  } else {
    document.body.style.overflow = ''
  }
})

// Handle ESC key
onMounted(() => {
  document.addEventListener('keydown', handleEscKey)
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleEscKey)
  document.body.style.overflow = ''
})
</script>

<style scoped>
{% if cookiecutter.css_framework == 'tailwind' -%}
.modal-overlay {
  @apply fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4;
}

.modal-container {
  @apply bg-white rounded-lg shadow-xl max-h-[90vh] flex flex-col;
}

/* Size variants */
.modal-sm { @apply max-w-sm w-full; }
.modal-md { @apply max-w-md w-full; }
.modal-lg { @apply max-w-lg w-full; }
.modal-xl { @apply max-w-xl w-full; }
.modal-full { @apply max-w-full w-full h-full max-h-full rounded-none; }

/* Centered */
.modal-centered {
  @apply my-auto;
}

/* Header */
.modal-header {
  @apply flex items-center justify-between p-4 border-b border-gray-200;
}

.modal-title {
  @apply text-xl font-semibold text-gray-900;
}

.modal-close {
  @apply p-1 rounded-lg text-gray-400 hover:text-gray-600 hover:bg-gray-100 transition-colors;
  @apply focus:outline-none focus:ring-2 focus:ring-blue-500;
}

/* Body */
.modal-body {
  @apply flex-1 p-4 overflow-auto;
}

.modal-body-scrollable {
  @apply overflow-y-auto;
}

/* Footer */
.modal-footer {
  @apply flex items-center justify-end gap-2 p-4 border-t border-gray-200;
}

/* Transition */
.modal-enter-active,
.modal-leave-active {
  @apply transition-opacity duration-200;
}

.modal-enter-active .modal-container,
.modal-leave-active .modal-container {
  @apply transition-all duration-200;
}

.modal-enter-from,
.modal-leave-to {
  @apply opacity-0;
}

.modal-enter-from .modal-container,
.modal-leave-to .modal-container {
  @apply transform scale-95 opacity-0;
}
{% else -%}
.modal-overlay {
  position: fixed;
  inset: 0;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 50;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
}

.modal-container {
  background-color: white;
  border-radius: 0.5rem;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  max-height: 90vh;
  display: flex;
  flex-direction: column;
}

/* Size variants */
.modal-sm { max-width: 24rem; width: 100%; }
.modal-md { max-width: 28rem; width: 100%; }
.modal-lg { max-width: 32rem; width: 100%; }
.modal-xl { max-width: 36rem; width: 100%; }
.modal-full { max-width: 100%; width: 100%; height: 100%; max-height: 100%; border-radius: 0; }

/* Header */
.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem;
  border-bottom: 1px solid #e5e7eb;
}

.modal-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #111827;
  margin: 0;
}

.modal-close {
  padding: 0.25rem;
  border-radius: 0.5rem;
  color: #9ca3af;
  background: transparent;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
}

.modal-close:hover {
  color: #4b5563;
  background-color: #f3f4f6;
}

.modal-close:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

/* Body */
.modal-body {
  flex: 1;
  padding: 1rem;
  overflow: auto;
}

/* Footer */
.modal-footer {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 0.5rem;
  padding: 1rem;
  border-top: 1px solid #e5e7eb;
}

/* Transition */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.2s;
}

.modal-enter-active .modal-container,
.modal-leave-active .modal-container {
  transition: all 0.2s;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-from .modal-container,
.modal-leave-to .modal-container {
  transform: scale(0.95);
  opacity: 0;
}
{%- endif %}
</style>