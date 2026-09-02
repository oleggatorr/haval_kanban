<!-- src\components\common\AppButton.vue -->
<template>
  <button
    class="app-btn"
    :class="[`app-btn--${variant}`, `app-btn--${size}`]"
    :disabled="disabled || loading"
    @click="$emit('click')"
  >
    <span v-if="loading" class="spinner"></span>
    <slot v-else />
  </button>
</template>

<script setup lang="ts">
defineProps<{
  variant?: 'primary' | 'secondary' | 'danger'
  size?: 'sm' | 'md' | 'lg'
  disabled?: boolean
  loading?: boolean
}>()

defineEmits(['click'])
</script>

<style scoped>
.app-btn {
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.2s;
}

.app-btn--primary {
  background: #42b983;
  color: white;
}
.app-btn--danger {
  background: #ff4d4f;
  color: white;
}
.app-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
/* Добавьте стили для размеров */
</style>
