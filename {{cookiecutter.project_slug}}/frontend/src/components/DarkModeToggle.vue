<template>
  <button
    @click="toggleDarkMode"
    class="dark-mode-toggle"
    :aria-label="isDark ? 'Switch to light mode' : 'Switch to dark mode'"
  >
    <IconLucideSun v-if="!isDark" class="icon sun-icon" />
    <IconLucideMoon v-else class="icon moon-icon" />
  </button>
</template>

<script setup{% if cookiecutter.use_typescript == 'y' %} lang="ts"{% endif %}>
import { useDarkMode } from '@/composables/useDarkMode'

const { isDark, toggleDarkMode } = useDarkMode()
</script>

<style scoped>
.dark-mode-toggle {
  padding: 0.5rem;
  border: none;
  background: transparent;
  color: #6b7280;
  cursor: pointer;
  border-radius: 0.375rem;
  transition: all 0.2s;
}

.dark-mode-toggle:hover {
  color: #374151;
  background: #f3f4f6;
}

.dark .dark-mode-toggle {
  color: #9ca3af;
}

.dark .dark-mode-toggle:hover {
  color: #f3f4f6;
  background: #4b5563;
}

.icon {
  width: 20px;
  height: 20px;
}

.sun-icon {
  color: #f59e0b;
}

.moon-icon {
  color: #60a5fa;
}
</style>