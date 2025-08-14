<template>
  <div v-if="password" class="mt-2">
    <div class="h-1 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
      <div 
        class="h-full transition-all duration-300 ease-out rounded-full"
        :class="{
          'bg-red-500': strengthClass === 'strength-very-weak',
          'bg-amber-500': strengthClass === 'strength-weak',
          'bg-yellow-500': strengthClass === 'strength-fair',
          'bg-lime-500': strengthClass === 'strength-good',
          'bg-green-500': strengthClass === 'strength-strong'
        }"
        :style="{ width: `${strength.score * 25}%` }"
      ></div>
    </div>
    <div class="mt-1">
      <span 
        class="text-xs font-medium"
        :class="{
          'text-red-500': strengthClass === 'strength-very-weak',
          'text-amber-500': strengthClass === 'strength-weak',
          'text-yellow-500': strengthClass === 'strength-fair',
          'text-lime-500': strengthClass === 'strength-good',
          'text-green-500': strengthClass === 'strength-strong'
        }"
      >
        {% raw %}{{ strength.label }}{% endraw %}
      </span>
      <ul v-if="strength.suggestions.length > 0" class="mt-2 pl-5 text-xs text-gray-500 dark:text-gray-400 list-disc">
        <li v-for="(suggestion, index) in strength.suggestions" :key="index" class="mb-1">
          {% raw %}{{ suggestion }}{% endraw %}
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup{% if cookiecutter.use_typescript == 'y' %} lang="ts"{% endif %}>
import { computed } from 'vue'

{% if cookiecutter.use_typescript == 'y' -%}
interface Props {
  password: string
}

interface StrengthResult {
  score: number
  label: string
  suggestions: string[]
}
{%- endif %}

const props = defineProps({% if cookiecutter.use_typescript == 'y' %}<Props>{% endif %}{
  password: {
    type: String,
    required: true
  }
})

const calculateStrength = (password{% if cookiecutter.use_typescript == 'y' %}: string{% endif %}){% if cookiecutter.use_typescript == 'y' %}: StrengthResult{% endif %} => {
  let score = 0
  const suggestions = []

  if (!password) {
    return { score: 0, label: 'No password', suggestions: [] }
  }

  // Length check
  if (password.length >= 8) score++
  if (password.length >= 12) score++
  if (password.length < 8) {
    suggestions.push('Use at least 8 characters')
  }

  // Character variety checks
  const hasLower = /[a-z]/.test(password)
  const hasUpper = /[A-Z]/.test(password)
  const hasNumber = /\d/.test(password)
  const hasSpecial = /[!@#$%^&*(),.?":{}|<>]/.test(password)

  if (hasLower) score += 0.5
  if (hasUpper) score += 0.5
  if (hasNumber) score += 0.5
  if (hasSpecial) score += 0.5

  // Suggestions
  if (!hasLower || !hasUpper) {
    suggestions.push('Mix uppercase and lowercase letters')
  }
  if (!hasNumber) {
    suggestions.push('Add numbers')
  }
  if (!hasSpecial) {
    suggestions.push('Include special characters (!@#$%^&*)')
  }

  // Common patterns to avoid
  const hasSequential = /123|234|345|456|567|678|789|890|abc|bcd|cde|def/i.test(password)
  const hasRepeating = /(.)\1{2,}/.test(password)
  
  if (hasSequential) {
    score -= 0.5
    suggestions.push('Avoid sequential characters')
  }
  if (hasRepeating) {
    score -= 0.5
    suggestions.push('Avoid repeating characters')
  }

  // Determine label
  let label = 'Very Weak'
  if (score >= 4) label = 'Strong'
  else if (score >= 3) label = 'Good'
  else if (score >= 2) label = 'Fair'
  else if (score >= 1) label = 'Weak'

  return {
    score: Math.min(Math.max(score, 0), 4),
    label,
    suggestions: suggestions.slice(0, 3) // Limit to 3 suggestions
  }
}

const strength = computed(() => calculateStrength(props.password))

const strengthClass = computed(() => {
  const score = strength.value.score
  if (score >= 4) return 'strength-strong'
  if (score >= 3) return 'strength-good'
  if (score >= 2) return 'strength-fair'
  if (score >= 1) return 'strength-weak'
  return 'strength-very-weak'
})
</script>