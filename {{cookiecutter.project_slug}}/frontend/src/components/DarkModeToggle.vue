<template>
  <button
    @click="toggleDarkMode"
    class="p-2 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-md transition-all"
    :aria-label="isDark ? 'Switch to light mode' : 'Switch to dark mode'"
  >
    <IconLucideSun v-if="!isDark" class="w-5 h-5 text-amber-500" />
    <IconLucideMoon v-else class="w-5 h-5 text-blue-400" />
  </button>
</template>

<script setup{% if cookiecutter.use_typescript == 'y' %} lang="ts"{% endif %}>
import { useDarkMode } from '@/composables/useDarkMode'

const { isDark, toggleDarkMode } = useDarkMode()
</script>