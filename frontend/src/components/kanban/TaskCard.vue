<!-- src/components/kanban/TaskCard.vue -->
<template>
  <div v-if="task" class="task-card" :class="{ 'completed-task': task.is_complit }">
    <div class="task-header">
      <div class="task-title-wrapper">
        <span
          :class="['task-status', task.is_complit ? 'completed' : 'active']"
          @click="toggleTask"
          :title="task.is_complit ? 'Отметить как невыполненную' : 'Отметить как выполненную'"
        >
          {{ task.is_complit ? '✓' : '○' }}
        </span>
        <span class="task-name" :class="{ completed: task.is_complit }">
          {{ task.name }}
        </span>
      </div>

      <div class="task-actions">
        <!-- Бургер-меню вместо отдельных кнопок -->
        <BurgerMenu
          :items="menuItems"
          :title="`Действия: ${task.name}`"
          placement="bottom-end"
          @select="handleMenuSelect"
        />
      </div>
    </div>

    <!-- Подзадачи -->
    <div v-if="task.subtasks && task.subtasks.length > 0" class="subtasks">
      <div v-for="subtask in task.subtasks" :key="subtask.id" class="subtask-item">
        <span class="subtask-bullet">•</span>
        <span class="subtask-name">{{ subtask.name }}</span>
        <ActionButton
          icon="✕"
          tooltip="Удалить подзадачу"
          @click.stop="$emit('delete-subtask', subtask.id)"
          class="mini-action delete-subtask"
        />
      </div>
    </div>

    <!-- Назначенные исполнители -->
    <div v-if="task.assignees && task.assignees.length > 0" class="assignees">
      <span class="assignees-label">Исполнители:</span>
      <span class="assignees-list">{{ task.assignees.join(', ') }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, inject } from 'vue'
import type { Task } from '@/composables/useKanbanBoard'
import type { MenuItem } from '@/components/ui/BurgerMenu.vue'
import ActionButton from '@/components/ui/ActionButton.vue'
import BurgerMenu from '@/components/ui/BurgerMenu.vue'

const props = defineProps<{
  task: Task
}>()

const emit = defineEmits<{
  (e: 'delete-task', id: number): void
  (e: 'create-subtask', id: number): void
  (e: 'delete-subtask', id: number): void
  (e: 'toggle-task', id: number, isComplit: boolean): void
  (e: 'move-task', taskId: number, columnId: string): void
}>()

// Получаем список колонок из родительского компонента (через provide/inject)
const boardColumns = inject<Array<{ id: string; title: string }>>('boardColumns', [])

// Создаем подменю для перемещения
const getMoveSubmenu = (task: Task): MenuItem[] => {
  return boardColumns.map((column) => ({
    id: `move-to-${column.id}`,
    label: `Переместить в "${column.title}"`,
    icon: '📌',
    action: () => {
      emit('move-task', task.id, column.id)
    },
  }))
}

// Используем функцию вместо computed для создания пунктов меню
const getMenuItems = (task: Task): MenuItem[] => {
  return [
    {
      id: 'toggle-status',
      label: task.is_complit ? 'Отметить как невыполненную' : 'Отметить как выполненную',
      icon: task.is_complit ? '↩️' : '✅',
      shortcut: 'Space',
      action: () => toggleTask(),
    },
    {
      id: 'add-subtask',
      label: 'Добавить подзадачу',
      icon: '➕',
      shortcut: 'Ctrl+Shift+N',
      action: () => emit('create-subtask', task.id),
    },
    {
      id: 'divider-1',
      label: '──────────',
      disabled: true,
      icon: '',
    },
    {
      id: 'move-task',
      label: 'Переместить',
      icon: '🚀',
      shortcut: 'Ctrl+M',
      // Подменю с колонками
      children: getMoveSubmenu(task),
    },
    {
      id: 'edit-task',
      label: 'Редактировать',
      icon: '✏️',
      shortcut: 'Ctrl+E',
      action: () => {
        console.log('Редактировать задачу:', task.id)
      },
    },
    {
      id: 'duplicate-task',
      label: 'Дублировать',
      icon: '📋',
      shortcut: 'Ctrl+D',
      action: () => {
        console.log('Дублировать задачу:', task.id)
      },
    },
    {
      id: 'divider-2',
      label: '──────────',
      disabled: true,
      icon: '',
    },
    {
      id: 'delete-task',
      label: 'Удалить задачу',
      icon: '🗑️',
      danger: true,
      shortcut: 'Del',
      action: () => {
        if (confirm(`Удалить задачу "${task.name}"?`)) {
          emit('delete-task', task.id)
        }
      },
    },
  ]
}

// Используем computed с правильной зависимостью от props.task
const menuItems = computed(() => {
  // Проверяем, что task существует
  if (!props.task) return []
  return getMenuItems(props.task)
})

// Переключение статуса задачи
const toggleTask = () => {
  if (props.task) {
    emit('toggle-task', props.task.id, !props.task.is_complit)
  }
}

// Обработчик выбора пункта меню
const handleMenuSelect = (item: MenuItem) => {
  console.log('Выбран пункт меню для задачи:', item.label)
}
</script>

<style scoped>
.task-card {
  background-color: white;
  border-radius: 6px;
  padding: 12px 14px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.06);
  transition:
    box-shadow 0.2s,
    background-color 0.2s;
}

.task-card:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.task-card.completed-task {
  background-color: #f8fafc;
}

.task-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 10px;
}

.task-title-wrapper {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  flex: 1;
  min-width: 0;
}

.task-name {
  font-size: 14px;
  font-weight: 500;
  color: #172b4d;
  word-break: break-word;
  line-height: 1.4;
  flex: 1;
}

.task-name.completed {
  text-decoration: line-through;
  color: #8c9aa8;
}

.task-status {
  font-size: 18px;
  flex-shrink: 0;
  cursor: pointer;
  transition:
    transform 0.2s,
    color 0.2s;
  user-select: none;
  line-height: 1;
  margin-top: 1px;
}

.task-status:hover {
  transform: scale(1.2);
}

.task-status.active {
  color: #5e6c84;
}

.task-status.active:hover {
  color: #0052cc;
}

.task-status.completed {
  color: #36b37e;
}

.task-status.completed:hover {
  color: #00875a;
}

.task-actions {
  display: flex;
  align-items: center;
  gap: 2px;
  opacity: 0;
  transition: opacity 0.2s;
  flex-shrink: 0;
}

.task-card:hover .task-actions {
  opacity: 1;
}

.mini-action {
  width: 20px;
  height: 20px;
  font-size: 12px;
}

.mini-action .icon {
  font-size: 12px;
}

.subtasks {
  margin-top: 8px;
  padding-top: 8px;
  border-top: 1px solid #f4f5f7;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.subtask-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: #5e6c84;
  padding: 2px 4px;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.subtask-item:hover {
  background-color: #f8f9fa;
}

.subtask-bullet {
  color: #97a0af;
  font-size: 14px;
}

.subtask-name {
  word-break: break-word;
  flex: 1;
}

.delete-subtask {
  opacity: 0;
  transition: opacity 0.2s;
}

.subtask-item:hover .delete-subtask {
  opacity: 1;
}

.delete-subtask .icon {
  font-size: 10px;
  color: #b3b9c4;
}

.delete-subtask:hover .icon {
  color: #de350b;
}

.assignees {
  margin-top: 8px;
  padding-top: 8px;
  border-top: 1px solid #f4f5f7;
  font-size: 12px;
  color: #5e6c84;
}

.assignees-label {
  font-weight: 500;
  color: #42526e;
}

.assignees-list {
  color: #172b4d;
}

/* Адаптация под мобильные устройства */
@media (max-width: 640px) {
  .task-actions {
    opacity: 1;
  }

  .task-card {
    padding: 10px 12px;
  }
}
</style>
