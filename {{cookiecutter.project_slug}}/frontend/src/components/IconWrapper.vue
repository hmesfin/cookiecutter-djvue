<template>
  <component :is="iconComponent" v-if="iconComponent" :class="iconClass" />
  <span v-else class="inline-block" :class="iconClass">
    <!-- Fallback icon -->
    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
    </svg>
  </span>
</template>

<script setup{% if cookiecutter.use_typescript == 'y' %} lang="ts"{% endif %}>
import { computed, defineAsyncComponent } from 'vue'

const props = defineProps({
  name: {
    type: String,
    required: true
  },
  size: {
    type: String,
    default: 'md'
  },
  collection: {
    type: String,
    default: 'lucide'
  }
})

// Size mapping
const sizeMap = {
  xs: 'w-3 h-3',
  sm: 'w-4 h-4',
  md: 'w-5 h-5',
  lg: 'w-6 h-6',
  xl: 'w-8 h-8',
  '2xl': 'w-10 h-10'
}

const iconClass = computed(() => sizeMap[props.size] || sizeMap.md)

// Dynamically import icon
const iconComponent = computed(() => {
  try {
    const iconName = props.name.charAt(0).toUpperCase() + props.name.slice(1)
    return defineAsyncComponent(() => 
      import(`~icons/${props.collection}/${props.name}`)
        .catch(() => null)
    )
  } catch {
    return null
  }
})
</script>