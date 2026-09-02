<!-- src/components/ui/ActionButton.vue -->
<template>
  <button class="action-btn" :title="tooltip" @click="$emit('click', $event)">
    <span class="icon">{{ icon }}</span>
  </button>
</template>

<script setup lang="ts">
defineProps<{
  icon: string
  tooltip?: string
}>()

defineEmits<{
  (e: 'click', event: MouseEvent): void // ✅ Добавляем event в сигнатуру
}>()
</script>

<style scoped>
.action-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  border: none;
  background: transparent;
  border-radius: 4px;
  cursor: pointer;
  color: #5e6c84;
  transition: all 0.2s;
}

.action-btn:hover {
  background-color: rgba(9, 30, 66, 0.08);
  color: #172b4d;
}

.icon {
  font-size: 16px;
  line-height: 1;
}
</style>
