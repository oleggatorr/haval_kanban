<!-- src/components/kanban/KanbanColumn.vue -->
<template>
  <div class="column">
    <div class="column-header">
      <h3>{{ column.name }}</h3>
      <div class="column-actions">
        <span class="column-badge">{{ column.tasks?.length || 0 }}</span>

        <!-- Бургер-меню вместо отдельных кнопок -->
        <BurgerMenu
          :items="menuItems"
          :title="`Действия: ${column.name}`"
          placement="bottom-end"
          @select="handleMenuSelect"
        />
      </div>
    </div>

    <div class="tasks-list">
      <TaskCard
        v-for="task in column.tasks || []"
        :key="task.id"
        :task="task"
        :columns="allColumns"
        @delete-task="$emit('delete-task', $event)"
        @create-subtask="$emit('create-subtask', $event)"
        @delete-subtask="$emit('delete-subtask', $event)"
        @toggle-task="$emit('toggle-task', $event, $event)"
        @move-task="$emit('move-task', $event, $event)"
      />

      <div v-if="!column.tasks || column.tasks.length === 0" class="empty-column">Нет задач</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { Column } from '@/composables/useKanbanBoard'
import type { MenuItem } from '@/components/ui/BurgerMenu.vue'
import TaskCard from './TaskCard.vue'
import BurgerMenu from '@/components/ui/BurgerMenu.vue'

const props = defineProps<{
  column: Column
  allColumns?: Column[] // Список всех колонок для перемещения задач
}>()

const emit = defineEmits<{
  (e: 'create-task', columnId: number): void
  (e: 'delete-column', columnId: number): void
  (e: 'delete-task', taskId: number): void
  (e: 'create-subtask', taskId: number): void
  (e: 'delete-subtask', subtaskId: number): void
  (e: 'toggle-task', taskId: number, isComplit: boolean): void
  (e: 'move-task', taskId: number, columnId: string): void
}>()

// Все колонки для передачи в TaskCard
const allColumns = computed(() => props.allColumns || [])

// Пункты меню для колонки
const menuItems = computed<MenuItem[]>(() => [
  {
    id: 'add-task',
    label: 'Добавить задачу',
    icon: '➕',
    shortcut: 'Ctrl+N',
    action: () => emit('create-task', props.column.id),
  },
  {
    id: 'divider-1',
    label: '──────────',
    disabled: true,
    icon: '',
  },
  {
    id: 'rename-column',
    label: 'Переименовать',
    icon: '✏️',
    shortcut: 'Ctrl+R',
    action: () => {
      // Можно добавить логику переименования
      console.log('Переименовать колонку:', props.column.id)
    },
  },
  {
    id: 'clear-tasks',
    label: 'Очистить задачи',
    icon: '🧹',
    action: () => {
      if (confirm(`Удалить все задачи из колонки "${props.column.name}"?`)) {
        props.column.tasks?.forEach((task) => {
          emit('delete-task', task.id)
        })
      }
    },
  },
  {
    id: 'divider-2',
    label: '──────────',
    disabled: true,
    icon: '',
  },
  {
    id: 'delete-column',
    label: 'Удалить колонку',
    icon: '🗑️',
    danger: true,
    shortcut: 'Del',
    action: () => {
      if (confirm(`Удалить колонку "${props.column.name}"?`)) {
        emit('delete-column', props.column.id)
      }
    },
  },
])

// Обработчик выбора пункта меню
const handleMenuSelect = (item: MenuItem) => {
  // Дополнительная логика при выборе пункта
  console.log('Выбран пункт меню:', item.label)
}
</script>

<style scoped>
.column {
  min-width: 280px;
  max-width: 320px;
  flex-shrink: 0;
  background-color: #ebecf0;
  border-radius: 8px;
  padding: 8px;
  display: flex;
  flex-direction: column;
  max-height: 100%;
}

.column-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 10px 12px;
  flex-shrink: 0;
}

.column-header h3 {
  margin: 0;
  font-size: 14px;
  font-weight: 600;
  color: #172b4d;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 160px;
}

.column-actions {
  display: flex;
  align-items: center;
  gap: 4px;
  opacity: 0.5;
  transition: opacity 0.2s;
}

.column:hover .column-actions {
  opacity: 1;
}

.column-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background-color: rgba(9, 30, 66, 0.08);
  color: #5e6c84;
  font-size: 12px;
  font-weight: 500;
  padding: 0 8px;
  border-radius: 12px;
  height: 20px;
  min-width: 20px;
}

.tasks-list {
  flex: 1;
  overflow-y: auto;
  padding: 0 4px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.tasks-list::-webkit-scrollbar {
  width: 6px;
}

.tasks-list::-webkit-scrollbar-track {
  background: transparent;
}

.tasks-list::-webkit-scrollbar-thumb {
  background: #c1c7d0;
  border-radius: 3px;
}

.empty-column {
  padding: 16px;
  text-align: center;
  color: #97a0af;
  font-size: 13px;
  background-color: rgba(255, 255, 255, 0.5);
  border-radius: 6px;
  border: 1px dashed #d0d4db;
}
</style>
