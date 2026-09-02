<!-- src/components/KanbanBoard.vue -->
<template>
  <div class="kanban-board">
    <KanbanColumn
      v-for="column in columns"
      :key="column.id"
      :column="column"
      :init-sortable="initSortable"
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { Column } from '@/types/kanban'
import KanbanColumn from './KanbanColumn.vue'
import { useDragDrop } from '@/composables/useDragDrop'

const columns = ref<Column[]>([
  {
    id: 'todo',
    name: 'К выполнению',
    color: '#6366f1',
    tasks: [
      {
        id: '1',
        title: 'Разработать API для пользователей',
        description: 'Создать endpoints для CRUD операций',
        priority: 'high',
        tags: ['backend', 'api'],
      },
      {
        id: '2',
        title: 'Настроить Docker',
        priority: 'medium',
        tags: ['devops'],
      },
    ],
  },
  {
    id: 'in-progress',
    name: 'В работе',
    color: '#f59e0b',
    tasks: [
      {
        id: '3',
        title: 'Дизайн главной страницы',
        description: 'Создать макет в Figma',
        priority: 'high',
        tags: ['design', 'ui'],
      },
    ],
  },
  {
    id: 'review',
    name: 'На ревью',
    color: '#8b5cf6',
    tasks: [],
  },
  {
    id: 'done',
    name: 'Готово',
    color: '#10b981',
    tasks: [
      {
        id: '4',
        title: 'Настроить CI/CD',
        priority: 'low',
        tags: ['devops'],
      },
    ],
  },
])

const { initSortable } = useDragDrop(columns)
</script>

<style scoped>
.kanban-board {
  display: flex;
  gap: 16px;
  padding: 24px;
  overflow-x: auto;
  min-height: calc(100vh - 100px);
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
</style>
