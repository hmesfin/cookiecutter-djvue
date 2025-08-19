{% raw %}<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="modelValue" class="modal-backdrop" @click="handleOverlayClick">
        <div class="fixed inset-0 flex items-center justify-center p-4" :class="{ 'items-start pt-16': !centered }">
          <div class="modal-content flex flex-col max-h-[90vh]" :class="modalClasses" @click.stop>
            <div v-if="showHeader" class="modal-header">
              <slot name="header">
                <h2 v-if="modalTitle" class="text-xl font-semibold text-gray-900 dark:text-gray-100">{{ modalTitle }}</h2>
              </slot>
              <button
                v-if="closable"
                type="button"
                class="p-1 rounded-lg text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors focus:outline-none focus:ring-2 focus:ring-emerald-500 dark:focus:ring-emerald-400"
                @click="close"
              >
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path d="M18 6L6 18M6 6l12 12" stroke-width="2" stroke-linecap="round"/>
                </svg>
              </button>
            </div>
            
            <div class="modal-body flex-1 overflow-auto" :class="{ 'overflow-y-auto': scrollable }">
              <slot />
            </div>
            
            <div v-if="$slots.footer || showFooter" class="modal-footer">
              <slot name="footer">
                <BaseButton
                  v-if="showCancel"
                  variant="secondary"
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
      </div>
    </Transition>
  </Teleport>
</template>{% endraw %}

<script setup {% if cookiecutter.use_typescript == 'y' %}lang="ts"{% endif %}>
import { computed, watch, onMounted, onUnmounted{% if cookiecutter.use_typescript == 'y' %}, type PropType{% endif %} } from 'vue'
import BaseButton from './BaseButton.vue'

{% if cookiecutter.use_typescript == 'y' -%}
type ModalSize = 'sm' | 'md' | 'lg' | 'xl' | 'full'
type ButtonVariant = 'primary' | 'secondary' | 'success' | 'danger' | 'warning' | 'info'

interface Props {
  modelValue?: boolean
  modalTitle?: string
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
  modalTitle: {
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
  const sizeClasses = {
    sm: 'max-w-sm w-full',
    md: 'max-w-md w-full', 
    lg: 'max-w-lg w-full',
    xl: 'max-w-xl w-full',
    full: 'max-w-full w-full h-full max-h-full rounded-none'
  }
  
  return [
    sizeClasses[props.size]
  ]
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

<style>
/* Transition animations */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 200ms ease-in-out;
}

.modal-enter-active .modal-content,
.modal-leave-active .modal-content {
  transition: all 200ms ease-in-out;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-from .modal-content,
.modal-leave-to .modal-content {
  transform: scale(0.95);
  opacity: 0;
}
</style>