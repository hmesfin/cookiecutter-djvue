<template>
  <Teleport to="body">
    <div class="notification-container">
      <TransitionGroup name="notification" tag="div">
        <div
          v-for="notification in notifications"
          :key="notification.id"
          :class="['notification', `notification-${notification.type}`]"
        >
          <div class="notification-icon">
            <svg v-if="notification.type === 'success'" class="icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            <svg v-else-if="notification.type === 'error'" class="icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            <svg v-else-if="notification.type === 'warning'" class="icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
            </svg>
            <svg v-else class="icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
          </div>
          <div class="notification-content">
            <h4 class="notification-title">{% raw %}{{ notification.title }}{% endraw %}</h4>
            <p v-if="notification.message" class="notification-message">{% raw %}{{ notification.message }}{% endraw %}</p>
            <div v-if="notification.actions" class="notification-actions">
              <button
                v-for="action in notification.actions"
                :key="action.label"
                @click="handleAction(action.handler, notification.id)"
                class="notification-action"
              >
                {% raw %}{{ action.label }}{% endraw %}
              </button>
            </div>
          </div>
          <button @click="notificationStore.remove(notification.id)" class="notification-close">
            <svg class="icon-sm" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
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
.notification-container {
  position: fixed;
  top: 1rem;
  right: 1rem;
  z-index: 9999;
  pointer-events: none;
}

.notification {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  min-width: 300px;
  max-width: 400px;
  padding: 1rem;
  margin-bottom: 0.75rem;
  background: white;
  border-radius: 0.5rem;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  pointer-events: auto;
}

.dark .notification {
  background: #1f2937;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3), 0 4px 6px -2px rgba(0, 0, 0, 0.2);
}

.notification-icon {
  flex-shrink: 0;
}

.icon {
  width: 24px;
  height: 24px;
}

.icon-sm {
  width: 16px;
  height: 16px;
}

.notification-success .notification-icon {
  color: #10b981;
}

.notification-error .notification-icon {
  color: #ef4444;
}

.notification-warning .notification-icon {
  color: #f59e0b;
}

.notification-info .notification-icon {
  color: #3b82f6;
}

.notification-content {
  flex: 1;
}

.notification-title {
  margin: 0 0 0.25rem 0;
  font-weight: 600;
  font-size: 0.875rem;
  color: #111827;
}

.dark .notification-title {
  color: #f3f4f6;
}

.notification-message {
  margin: 0;
  font-size: 0.875rem;
  color: #6b7280;
}

.dark .notification-message {
  color: #9ca3af;
}

.notification-actions {
  display: flex;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.notification-action {
  padding: 0.25rem 0.5rem;
  border: none;
  background: transparent;
  color: #3b82f6;
  font-size: 0.75rem;
  font-weight: 500;
  cursor: pointer;
  border-radius: 0.25rem;
  transition: background-color 0.2s;
}

.notification-action:hover {
  background: #eff6ff;
}

.dark .notification-action:hover {
  background: #1e3a8a;
}

.notification-close {
  flex-shrink: 0;
  padding: 0.25rem;
  border: none;
  background: transparent;
  color: #9ca3af;
  cursor: pointer;
  border-radius: 0.25rem;
  transition: all 0.2s;
}

.notification-close:hover {
  color: #6b7280;
  background: #f3f4f6;
}

.dark .notification-close:hover {
  color: #d1d5db;
  background: #374151;
}

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