<template>
  <RouterView />
</template>

<script setup{% if cookiecutter.use_typescript == 'y' %} lang="ts"{% endif %}>
import { RouterView } from 'vue-router'
</script>

<style scoped>
</style>