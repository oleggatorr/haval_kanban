<!-- src/components/KanbanColumn.vue -->
<template>
  <div class="column">
    <div class="column-header" :style="{ backgroundColor: column.color }">
      <h3 class="column-title">{{ column.name }}</h3>
      <span class="task-count">{{ column.tasks.length }}</span>
    </div>

    <!-- ДОБАВЬ data-column-id СЮДА -->
    <div ref="taskListRef" class="column-body" :data-column-id="column.id">
      <TaskCard v-for="task in column.tasks" :key="task.id" :task="task" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import type { Column } from '@/types/kanban'
import TaskCard from './TaskCard.vue'

const props = defineProps<{
  column: Column
  initSortable: (columnId: string, element: HTMLElement) => void
}>()

const taskListRef = ref<HTMLElement>()

onMounted(() => {
  if (taskListRef.value) {
    props.initSortable(props.column.id, taskListRef.value)
  }
})
</script>

<style scoped>
.column {
  min-width: 280px;
  max-width: 280px;
  background: #f9fafb;
  border-radius: 12px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.column-header {
  padding: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.column-title {
  font-size: 16px;
  font-weight: 600;
  color: white;
  margin: 0;
}

.task-count {
  background: rgba(255, 255, 255, 0.3);
  color: white;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
}

.column-body {
  padding: 12px;
  flex: 1;
  overflow-y: auto;
  min-height: 200px;
}
</style>
