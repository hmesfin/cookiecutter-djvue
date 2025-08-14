<template>
  <button
    @click="toggleDarkMode"
    class="dark-mode-toggle"
    :aria-label="isDark ? 'Switch to light mode' : 'Switch to dark mode'"
  >
    <svg v-if="!isDark" class="icon sun-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"></path>
    </svg>
    <svg v-else class="icon moon-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"></path>
    </svg>
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