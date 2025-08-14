<template>
  <div id="app">
    <RouterView />
    <NotificationContainer />
  </div>
</template>

<script setup{% if cookiecutter.use_typescript == 'y' %} lang="ts"{% endif %}>
import { RouterView } from 'vue-router'
import { onMounted } from 'vue'
import NotificationContainer from '@/components/NotificationContainer.vue'
import { useDarkMode } from '@/composables/useDarkMode'

// Initialize dark mode
const { initDarkMode } = useDarkMode()
onMounted(() => {
  initDarkMode()
})
</script>

<style scoped>
</style>