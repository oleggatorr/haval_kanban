<!-- src\views\test2\task_board_components\KanbanBoard.vue -->
<template>
  <div class="kanban-board">
    <div v-if="!board" class="empty-state">
      <p>Загрузка доски...</p>
    </div>

    <template v-else>
      <!-- Уменьшенная шапка -->
      <div class="board-header">
        <h2>{{ board.name }}</h2>

        <DropdownMenu align="right">
          <div class="menu-item" @click.stop="isCreateColumnOpen = true">➕ Добавить колонку</div>
          <div class="menu-item" @click.stop="isEditBoardOpen = true">⚙️ Настройки доски</div>
        </DropdownMenu>
      </div>

      <div class="columns-container">
        <KanbanColumn
          v-for="column in columns"
          :key="column.id"
          :column="column"
          :tasks="getTasksByColumn(column.id)"
          :subtasks="getAllSubtasks"
          @delete-column="(id) => $emit('delete-column', id)"
          @column-menu="(col) => $emit('column-menu', col)"
          @add-task="(colId) => $emit('add-task', colId)"
          @delete-task="(taskId) => $emit('delete-task', taskId)"
          @task-menu="(task) => $emit('task-menu', task)"
          @add-subtask="(taskId) => $emit('add-subtask', taskId)"
          @subtask-complete="(id, checked) => $emit('subtask-complete', id, checked)"
          @subtask-edit="(sub) => $emit('subtask-edit', sub)"
          @assign-subtask-user="(sub) => $emit('assign-subtask-user', sub)"
        />

        <div class="spacer"></div>
      </div>
    </template>

    <!-- Модальное окно создания колонки -->
    <CreateColumnModal
      v-model="isCreateColumnOpen"
      @save="(data) => $emit('create-column-with-data', data)"
    />

    <!-- Модальное окно редактирования доски -->
    <EditBoardModal
      v-model="isEditBoardOpen"
      :board="board"
      @save="(data) => $emit('update-board', data)"
    />
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import KanbanColumn from './KanbanColumn.vue'
import DropdownMenu from '@/components/ui/DropdownMenu.vue'
import CreateColumnModal from './create_forms/CreateColumnModal.vue'
import EditBoardModal from './edit_forms/EditBoardModal.vue'
import type { Board, Column, Task, Subtask } from '@/types/taskboard'

const props = defineProps<{
  board: Board | null
  columns: Column[]
  tasks: Task[]
  subtasks: Subtask[]
}>()

defineEmits<{
  (e: 'add-column'): void // Оставляем для совместимости, если нужно
  (e: 'delete-column', id: number): void
  (e: 'add-task', columnId: number): void
  (e: 'delete-task', taskId: number): void
  (e: 'add-subtask', taskId: number): void
  (e: 'subtask-complete', subtaskId: number, isComplete: boolean): void
  (e: 'delete-subtask', subtaskId: number): void
  (e: 'column-menu', item: Column): void
  (e: 'task-menu', item: Task): void
  (e: 'subtask-edit', item: Subtask): void
  (e: 'assign-subtask-user', item: Subtask): void
  // Новые события для обработки данных из модалок
  (e: 'create-column-with-data', data: { name: string }): void
  (e: 'update-board', data: Partial<Board>): void
}>()

// Состояния модальных окон
const isCreateColumnOpen = ref(false)
const isEditBoardOpen = ref(false)

// Фильтруем задачи для конкретной колонки
const getTasksByColumn = (columnId: number) => {
  return props.tasks.filter((t) => t.column_id === columnId)
}

// Передаем все подзадачи вниз
const getAllSubtasks = computed(() => props.subtasks)
</script>

<style scoped>
.kanban-board {
  display: flex;
  flex-direction: column;
  height: 100%;
  background-color: #f8f9fa;
}

/* Уменьшенная шапка */
.board-header {
  padding: 0.75rem 2rem; /* Было 1rem */
  background: white;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-shrink: 0;
  height: 60px; /* Фиксированная небольшая высота */
}

.board-header h2 {
  font-size: 1.25rem; /* Чуть меньше шрифт заголовка */
  margin: 0;
}

.columns-container {
  display: flex;
  gap: 1.5rem;
  overflow-x: auto;
  padding: 2rem;
  height: calc(100% - 60px); /* Вычитаем высоту шапки */
  align-items: flex-start;
}

.spacer {
  min-width: 2rem;
}

.menu-item {
  padding: 8px 16px;
  font-size: 13px;
  cursor: pointer;
  color: #4a5568;
  transition: background 0.2s;
  display: flex;
  align-items: center;
  gap: 8px;
}

.menu-item:hover {
  background: #f7fafc;
  color: #168be5;
}

.empty-state {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  color: #9ca3af;
}
</style>
