<!-- src\views\test1\components\TaskCard.vue -->

<template>
  <article class="card">
    <div class="card-top">
      <span class="tag">Задача</span>
      <div class="card-actions">
        <iconify-icon icon="solar:pen-outline" @click="$emit('edit', task)"></iconify-icon>
        <iconify-icon
          icon="solar:trash-bin-outline"
          @click="$emit('delete', task.id)"
        ></iconify-icon>
      </div>
    </div>

    <h3>{{ task.name }}</h3>
    <div v-if="task.description" class="desc">{{ task.description }}</div>

    <!-- Отображение подзадач -->
    <div v-if="task.subtasks && task.subtasks.length" class="subtasks">
      <div v-for="sub in task.subtasks" :key="sub.id" class="subtask-item">
        <iconify-icon icon="solar:check-circle-outline"></iconify-icon>
        <span>{{ sub.name }}</span>
      </div>
    </div>

    <div class="card-foot">
      <div class="meta">
        <iconify-icon icon="solar:calendar-outline"></iconify-icon>
        {{ new Date(task.date_time_start).toLocaleDateString() }}
      </div>
      <button class="btn-small" @click="$emit('add-subtask', task)">+ Подзадача</button>
    </div>
  </article>
</template>

<script setup lang="ts">
defineProps<{ task: any }>()
defineEmits(['edit', 'delete', 'add-subtask'])
</script>

<style scoped>
.card {
  background: white;
  border-radius: 8px;
  padding: 12px;
  margin-bottom: 10px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
  border: 1px solid #e5e7eb;
}
.card-actions {
  display: flex;
  gap: 8px;
  color: #9ca3af;
}
.card-actions iconify-icon {
  cursor: pointer;
}
.card-actions iconify-icon:hover {
  color: #168be5;
}
.subtasks {
  margin: 8px 0;
  font-size: 13px;
  color: #4b5563;
}
.subtask-item {
  display: flex;
  align-items: center;
  gap: 4px;
  margin-bottom: 4px;
}
.card-foot {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 10px;
  font-size: 12px;
  color: #6b7280;
}
.btn-small {
  background: #f3f4f6;
  border: none;
  border-radius: 4px;
  padding: 2px 6px;
  cursor: pointer;
  font-size: 11px;
}
</style>
