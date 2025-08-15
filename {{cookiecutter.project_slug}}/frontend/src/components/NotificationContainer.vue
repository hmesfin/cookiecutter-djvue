<template>
  <Teleport to="body">
    <div class="fixed top-4 right-4 z-[9999] pointer-events-none">
      <TransitionGroup name="notification" tag="div">
        <div
          v-for="notification in notifications"
          :key="notification.id"
          :class="[
            'flex items-start gap-3 min-w-[300px] max-w-[400px] p-4 mb-3',
            'bg-white dark:bg-gray-800 rounded-lg shadow-xl dark:shadow-2xl dark:shadow-gray-900/50',
            'pointer-events-auto'
          ]"
        >
          <div class="flex-shrink-0">
            <IconLucideCheckCircle 
              v-if="notification.type === 'success'" 
              class="w-6 h-6 text-green-500" 
            />
            <IconLucideXCircle 
              v-else-if="notification.type === 'error'" 
              class="w-6 h-6 text-red-500" 
            />
            <IconLucideAlertTriangle 
              v-else-if="notification.type === 'warning'" 
              class="w-6 h-6 text-amber-500" 
            />
            <IconLucideInfo 
              v-else 
              class="w-6 h-6 text-emerald-600" 
            />
          </div>
          <div class="flex-1">
            <h4 class="mb-1 font-semibold text-sm text-gray-900 dark:text-gray-100">
              {% raw %}{{ notification.title }}{% endraw %}
            </h4>
            <p v-if="notification.message" class="text-sm text-gray-600 dark:text-gray-400">
              {% raw %}{{ notification.message }}{% endraw %}
            </p>
            <div v-if="notification.actions" class="flex gap-2 mt-2">
              <button
                v-for="action in notification.actions"
                :key="action.label"
                @click="handleAction(action.handler, notification.id)"
                class="px-2 py-1 text-xs font-medium text-emerald-600 dark:text-emerald-400 hover:bg-emerald-50 dark:hover:bg-blue-900/20 rounded transition-colors"
              >
                {% raw %}{{ action.label }}{% endraw %}
              </button>
            </div>
          </div>
          <button 
            @click="notificationStore.remove(notification.id)" 
            class="flex-shrink-0 p-1 text-gray-400 hover:text-gray-600 dark:text-gray-500 dark:hover:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded transition-all"
          >
            <IconLucideX class="w-4 h-4" />
          </button>
        </div>
      </TransitionGroup>
    </div>
  </Teleport>
</template>

<script setup{% if cookiecutter.use_typescript == 'y' %} lang="ts"{% endif %}>
import { computed } from 'vue'
import { useNotificationStore } from '@/stores/notifications'

const notificationStore = useNotificationStore()
const notifications = computed(() => notificationStore.notifications)

const handleAction = (handler{% if cookiecutter.use_typescript == 'y' %}: () => void{% endif %}, notificationId{% if cookiecutter.use_typescript == 'y' %}: string{% endif %}) => {
  handler()
  notificationStore.remove(notificationId)
}
</script>

<style scoped>
/* Transition animations */
.notification-enter-active,
.notification-leave-active {
  transition: all 0.3s ease;
}

.notification-enter-from {
  transform: translateX(100%);
  opacity: 0;
}

.notification-leave-to {
  transform: translateX(100%);
  opacity: 0;
}

.notification-move {
  transition: transform 0.3s ease;
}
</style>