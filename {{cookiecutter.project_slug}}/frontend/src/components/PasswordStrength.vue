<template>
  <div v-if="password" class="password-strength">
    <div class="strength-meter">
      <div 
        class="strength-meter-fill" 
        :class="strengthClass"
        :style="{ width: `${strength.score * 25}%` }"
      ></div>
    </div>
    <div class="strength-info">
      <span class="strength-label" :class="strengthClass">
        {% raw %}{{ strength.label }}{% endraw %}
      </span>
      <ul v-if="strength.suggestions.length > 0" class="strength-suggestions">
        <li v-for="(suggestion, index) in strength.suggestions" :key="index">
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

<style scoped>
.password-strength {
  margin-top: 0.5rem;
}

.strength-meter {
  height: 4px;
  background: #e5e7eb;
  border-radius: 2px;
  overflow: hidden;
}

.dark .strength-meter {
  background: #374151;
}

.strength-meter-fill {
  height: 100%;
  transition: width 0.3s ease, background-color 0.3s ease;
}

.strength-meter-fill.strength-very-weak {
  background: #ef4444;
}

.strength-meter-fill.strength-weak {
  background: #f59e0b;
}

.strength-meter-fill.strength-fair {
  background: #eab308;
}

.strength-meter-fill.strength-good {
  background: #84cc16;
}

.strength-meter-fill.strength-strong {
  background: #10b981;
}

.strength-info {
  margin-top: 0.25rem;
}

.strength-label {
  font-size: 0.75rem;
  font-weight: 500;
}

.strength-label.strength-very-weak {
  color: #ef4444;
}

.strength-label.strength-weak {
  color: #f59e0b;
}

.strength-label.strength-fair {
  color: #eab308;
}

.strength-label.strength-good {
  color: #84cc16;
}

.strength-label.strength-strong {
  color: #10b981;
}

.strength-suggestions {
  margin: 0.5rem 0 0 0;
  padding-left: 1.25rem;
  font-size: 0.75rem;
  color: #6b7280;
}

.dark .strength-suggestions {
  color: #9ca3af;
}

.strength-suggestions li {
  margin-bottom: 0.25rem;
}
</style>