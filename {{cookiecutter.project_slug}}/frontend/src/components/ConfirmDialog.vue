<template>
  <Teleport to="body">
    <Transition name="modal">
      <div 
        v-if="isOpen" 
        class="fixed inset-0 bg-black/50 flex items-center justify-center z-50" 
        @click="cancel"
      >
        <div 
          class="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-md w-[90%] mx-4"
          @click.stop
        >
          <div class="p-6 border-b border-gray-200 dark:border-gray-700">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100">
              {% raw %}{{ title }}{% endraw %}
            </h3>
          </div>
          <div class="p-6">
            <p class="text-gray-600 dark:text-gray-400">
              {% raw %}{{ message }}{% endraw %}
            </p>
          </div>
          <div class="flex justify-end gap-3 p-6 border-t border-gray-200 dark:border-gray-700">
            <button 
              @click="cancel" 
              class="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 rounded-md transition-colors"
            >
              {% raw %}{{ cancelText }}{% endraw %}
            </button>
            <button 
              @click="confirm" 
              :class="[
                'px-4 py-2 text-sm font-medium rounded-md transition-colors',
                confirmClass === 'btn-danger' 
                  ? 'bg-red-600 hover:bg-red-700 text-white' 
                  : 'bg-emerald-600 hover:bg-emerald-700 text-white'
              ]"
            >
              {% raw %}{{ confirmText }}{% endraw %}
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup{% if cookiecutter.use_typescript == 'y' %} lang="ts"{% endif %}>
import { ref } from 'vue'

{% if cookiecutter.use_typescript == 'y' -%}
interface DialogOptions {
  title?: string
  message?: string
  confirmText?: string
  cancelText?: string
  confirmClass?: string
}
{%- endif %}

const isOpen = ref(false)
const title = ref('Confirm')
const message = ref('Are you sure?')
const confirmText = ref('Confirm')
const cancelText = ref('Cancel')
const confirmClass = ref('btn-primary')

let resolvePromise{% if cookiecutter.use_typescript == 'y' %}: ((value: boolean) => void) | null{% endif %} = null

const open = (options{% if cookiecutter.use_typescript == 'y' %}?: DialogOptions{% endif %}) => {
  title.value = options?.title || 'Confirm'
  message.value = options?.message || 'Are you sure?'
  confirmText.value = options?.confirmText || 'Confirm'
  cancelText.value = options?.cancelText || 'Cancel'
  confirmClass.value = options?.confirmClass || 'btn-primary'
  
  isOpen.value = true
  
  return new Promise((resolve) => {
    resolvePromise = resolve
  })
}

const confirm = () => {
  isOpen.value = false
  if (resolvePromise) {
    resolvePromise(true)
    resolvePromise = null
  }
}

const cancel = () => {
  isOpen.value = false
  if (resolvePromise) {
    resolvePromise(false)
    resolvePromise = null
  }
}

// Expose for use via ref
defineExpose({
  open
})
</script>

<style scoped>
/* Transition animations */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-active > div,
.modal-leave-active > div {
  transition: transform 0.3s ease;
}

.modal-enter-from > div,
.modal-leave-to > div {
  transform: scale(0.9);
}
</style>