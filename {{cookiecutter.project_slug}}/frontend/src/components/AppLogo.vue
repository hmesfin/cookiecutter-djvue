<template>
  <div class="app-logo">
    <img 
      v-if="isDark"
      :src="logoDark"
      :alt="alt"
      :class="['logo', sizeClass]"
    />
    <img 
      v-else
      :src="logoLight"
      :alt="alt"
      :class="['logo', sizeClass]"
    />
  </div>
</template>

<script setup{% if cookiecutter.use_typescript == 'y' %} lang="ts"{% endif %}>
import { computed } from 'vue'
import { useDarkMode } from '@/composables/useDarkMode'
import logoLight from '@/assets/images/logo-light.png'
import logoDark from '@/assets/images/logo-dark.png'

{% if cookiecutter.use_typescript == 'y' -%}
interface Props {
  size?: 'sm' | 'md' | 'lg' | 'xl'
  alt?: string
}
{%- endif %}

const props = defineProps({% if cookiecutter.use_typescript == 'y' %}<Props>{% endif %}{
  size: {
    type: String,
    default: 'md',
    validator: (value{% if cookiecutter.use_typescript == 'y' %}: string{% endif %}) => ['sm', 'md', 'lg', 'xl'].includes(value)
  },
  alt: {
    type: String,
    default: '{{ cookiecutter.project_name }}'
  }
})

const { isDark } = useDarkMode()

const sizeClass = computed(() => {
  const sizes = {
    sm: 'h-8',
    md: 'h-10',
    lg: 'h-12',
    xl: 'h-16'
  }
  return sizes[props.size] || sizes.md
})
</script>

<style scoped>
.app-logo {
  display: inline-flex;
  align-items: center;
}

.logo {
  width: auto;
  object-fit: contain;
}
</style>