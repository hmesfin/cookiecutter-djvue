<template>
  <BaseModal
    v-model="isOpen"
    :modal-title="title"
    :show-footer="true"
    :cancel-text="cancelText"
    :confirm-text="confirmText"
    :confirm-variant="confirmVariant"
    @confirm="confirm"
    @cancel="cancel"
    size="sm"
  >
    <p class="text-gray-600 dark:text-gray-400">
      {% raw %}{{ message }}{% endraw %}
    </p>
  </BaseModal>
</template>

<script setup{% if cookiecutter.use_typescript == 'y' %} lang="ts"{% endif %}>
import { ref } from 'vue'
import { BaseModal } from '@/components/base'

{% if cookiecutter.use_typescript == 'y' -%}
interface DialogOptions {
  title?: string
  message?: string
  confirmText?: string
  cancelText?: string
  confirmVariant?: 'primary' | 'secondary' | 'success' | 'danger' | 'warning' | 'info'
}
{%- endif %}

const isOpen = ref(false)
const title = ref('Confirm')
const message = ref('Are you sure?')
const confirmText = ref('Confirm')
const cancelText = ref('Cancel')
const confirmVariant = ref{% if cookiecutter.use_typescript == 'y' %}<'primary' | 'danger'>{% endif %}('primary')

let resolvePromise{% if cookiecutter.use_typescript == 'y' %}: ((value: boolean) => void) | null{% endif %} = null

const open = (options{% if cookiecutter.use_typescript == 'y' %}?: DialogOptions{% endif %}) => {
  title.value = options?.title || 'Confirm'
  message.value = options?.message || 'Are you sure?'
  confirmText.value = options?.confirmText || 'Confirm'
  cancelText.value = options?.cancelText || 'Cancel'
  confirmVariant.value = options?.confirmVariant || 'primary'
  
  isOpen.value = true
  
  return new Promise{% if cookiecutter.use_typescript == 'y' %}<boolean>{% endif %}((resolve) => {
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