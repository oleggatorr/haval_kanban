<!-- src/components/TaskCard.vue -->
<template>
  <div class="task-card" :class="`priority-${task.priority}`" :data-task-id="task.id">
    <div class="task-header">
      <h4 class="task-title">{{ task.title }}</h4>
      <span class="priority-badge">{{ getPriorityLabel(task.priority) }}</span>
    </div>

    <p v-if="task.description" class="task-description">
      {{ task.description }}
    </p>

    <div v-if="task.tags.length" class="task-tags">
      <span v-for="tag in task.tags" :key="tag" class="tag">
        {{ tag }}
      </span>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Task } from '@/types/kanban'

defineProps<{
  task: Task
}>()

function getPriorityLabel(priority: string): string {
  const labels = {
    low: 'Низкий',
    medium: 'Средний',
    high: 'Высокий',
  }
  return labels[priority as keyof typeof labels] || priority
}
</script>

<style scoped>
.task-card {
  background: white;
  border-radius: 8px;
  padding: 12px;
  margin-bottom: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  cursor: grab;
  transition: all 0.2s ease;
  border-left: 4px solid transparent;
}

.task-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.task-card.sortable-ghost {
  opacity: 0.4;
  background: #e0e7ff;
}

.task-card.sortable-chosen {
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
  transform: scale(1.02);
}

.task-card.sortable-drag {
  cursor: grabbing;
}

/* Остальные стили такие же как раньше */
.task-header {
  display: flex;
  justify-content: space-between;
  align-items: start;
  margin-bottom: 8px;
}

.task-title {
  font-size: 14px;
  font-weight: 600;
  color: #1f2937;
  margin: 0;
  flex: 1;
}

.priority-badge {
  font-size: 10px;
  padding: 2px 6px;
  border-radius: 12px;
  background: #f3f4f6;
  color: #6b7280;
  white-space: nowrap;
}

.task-description {
  font-size: 12px;
  color: #6b7280;
  margin: 0 0 8px 0;
  line-height: 1.4;
}

.task-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.tag {
  font-size: 10px;
  padding: 2px 8px;
  background: #e0e7ff;
  color: #4f46e5;
  border-radius: 12px;
}

.task-card.priority-low {
  border-left-color: #10b981;
}

.task-card.priority-medium {
  border-left-color: #f59e0b;
}

.task-card.priority-high {
  border-left-color: #ef4444;
}
</style>
