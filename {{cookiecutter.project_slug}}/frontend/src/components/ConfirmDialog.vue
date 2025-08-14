<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="isOpen" class="modal-overlay" @click="cancel">
        <div class="modal-container" @click.stop>
          <div class="modal-header">
            <h3 class="modal-title">{% raw %}{{ title }}{% endraw %}</h3>
          </div>
          <div class="modal-body">
            <p>{% raw %}{{ message }}{% endraw %}</p>
          </div>
          <div class="modal-footer">
            <button @click="cancel" class="btn btn-secondary">
              {% raw %}{{ cancelText }}{% endraw %}
            </button>
            <button @click="confirm" :class="['btn', confirmClass]">
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
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9998;
}

.modal-container {
  background: white;
  border-radius: 0.5rem;
  max-width: 400px;
  width: 90%;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

.dark .modal-container {
  background: #1f2937;
}

.modal-header {
  padding: 1.5rem;
  border-bottom: 1px solid #e5e7eb;
}

.dark .modal-header {
  border-bottom-color: #374151;
}

.modal-title {
  margin: 0;
  font-size: 1.125rem;
  font-weight: 600;
  color: #111827;
}

.dark .modal-title {
  color: #f3f4f6;
}

.modal-body {
  padding: 1.5rem;
}

.modal-body p {
  margin: 0;
  color: #6b7280;
}

.dark .modal-body p {
  color: #9ca3af;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  padding: 1.5rem;
  border-top: 1px solid #e5e7eb;
}

.dark .modal-footer {
  border-top-color: #374151;
}

.btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 0.375rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-secondary {
  background: #f3f4f6;
  color: #374151;
}

.btn-secondary:hover {
  background: #e5e7eb;
}

.dark .btn-secondary {
  background: #374151;
  color: #d1d5db;
}

.dark .btn-secondary:hover {
  background: #4b5563;
}

.btn-primary {
  background: #3b82f6;
  color: white;
}

.btn-primary:hover {
  background: #2563eb;
}

.btn-danger {
  background: #ef4444;
  color: white;
}

.btn-danger:hover {
  background: #dc2626;
}

/* Transition animations */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-active .modal-container,
.modal-leave-active .modal-container {
  transition: transform 0.3s ease;
}

.modal-enter-from .modal-container,
.modal-leave-to .modal-container {
  transform: scale(0.9);
}
</style>