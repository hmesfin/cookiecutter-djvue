{% raw %}<template>
  <component
    :is="interactive ? 'button' : 'div'"
    class="card overflow-hidden transition-all duration-200"
    :class="cardClasses"
    @click="handleClick"
  >
    <div v-if="image || $slots.image" class="relative overflow-hidden">
      <slot name="image">
        <img :src="image" :alt="imageAlt" class="w-full h-full object-cover" />
      </slot>
    </div>
    
    <div v-if="header || cardTitle || $slots.header" :class="headerClasses">
      <slot name="header">
        <h3 v-if="cardTitle" class="text-lg font-semibold text-gray-900 dark:text-gray-100">{{ cardTitle }}</h3>
        <p v-if="subtitle" class="text-sm text-gray-500 dark:text-gray-400 mt-1">{{ subtitle }}</p>
      </slot>
    </div>
    
    <div v-if="$slots.default" :class="bodyClasses">
      <slot />
    </div>
    
    <div v-if="$slots.footer" :class="footerClasses">
      <slot name="footer" />
    </div>
  </component>
</template>{% endraw %}

<script setup {% if cookiecutter.use_typescript == 'y' %}lang="ts"{% endif %}>
import { computed{% if cookiecutter.use_typescript == 'y' %}, type PropType{% endif %} } from 'vue'

{% if cookiecutter.use_typescript == 'y' -%}
type CardVariant = 'default' | 'bordered' | 'elevated' | 'flat'
type CardPadding = 'none' | 'sm' | 'md' | 'lg'

interface Props {
  cardTitle?: string
  subtitle?: string
  image?: string
  imageAlt?: string
  header?: boolean
  variant?: CardVariant
  padding?: CardPadding
  hoverable?: boolean
  interactive?: boolean
  loading?: boolean
}
{%- endif %}

const props = defineProps({
  cardTitle: {
    type: String,
    default: null
  },
  subtitle: {
    type: String,
    default: null
  },
  image: {
    type: String,
    default: null
  },
  imageAlt: {
    type: String,
    default: ''
  },
  header: {
    type: Boolean,
    default: false
  },
  variant: {
    type: String{% if cookiecutter.use_typescript == 'y' %} as PropType<CardVariant>{% endif %},
    default: 'default',
    validator: (value{% if cookiecutter.use_typescript == 'y' %}: string{% endif %}) => ['default', 'bordered', 'elevated', 'flat'].includes(value)
  },
  padding: {
    type: String{% if cookiecutter.use_typescript == 'y' %} as PropType<CardPadding>{% endif %},
    default: 'md',
    validator: (value{% if cookiecutter.use_typescript == 'y' %}: string{% endif %}) => ['none', 'sm', 'md', 'lg'].includes(value)
  },
  hoverable: {
    type: Boolean,
    default: false
  },
  interactive: {
    type: Boolean,
    default: false
  },
  loading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits<{
  click: [event: MouseEvent]
}>()

const cardClasses = computed(() => {
  const variantClasses = {
    default: 'shadow-sm',
    bordered: 'border border-gray-200 dark:border-gray-700 shadow-none',
    elevated: 'shadow-lg',
    flat: 'shadow-none'
  }
  
  return [
    variantClasses[props.variant],
    {
      'hover-lift cursor-pointer': props.hoverable,
      'cursor-pointer focus-primary': props.interactive,
      'animate-pulse': props.loading
    }
  ]
})

const paddingClasses = computed(() => {
  const paddingMap = {
    none: 'p-0',
    sm: 'p-3',
    md: 'p-4', 
    lg: 'p-6'
  }
  return paddingMap[props.padding]
})

const headerClasses = computed(() => {
  return [
    'card-header',
    paddingClasses.value
  ]
})

const bodyClasses = computed(() => {
  return [
    'card-body text-gray-700 dark:text-gray-300',
    paddingClasses.value,
    {
      'opacity-50': props.loading
    }
  ]
})

const footerClasses = computed(() => {
  return [
    'card-footer flex items-center justify-between',
    paddingClasses.value
  ]
})

const handleClick = (event{% if cookiecutter.use_typescript == 'y' %}: MouseEvent{% endif %}) => {
  if (props.interactive) {
    emit('click', event)
  }
}
</script>

