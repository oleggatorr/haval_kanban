<template>
  <div class="kanban-board">
    <!-- Защита: если board нет, показываем заглушку -->
    <div v-if="!board" class="empty-state">
      <p>Загрузка данных или доска пуста...</p>
    </div>

    <template v-else>
      <div class="board-header">
        <h2>{{ board.name }}</h2>
        <button class="btn-primary" @click="$emit('add-column')">+ Новая колонка</button>
      </div>

      <div class="columns-container">
        <!-- Итерируемся прямо по board.columns -->
        <div v-for="column in board.columns" :key="column.id" class="column">
          <div class="column-header">
            <h3>{{ column.name }}</h3>
            <div class="column-actions">
              <button class="icon-btn" @click="$emit('column-menu', column)">⋮</button>
              <button class="icon-btn delete" @click="$emit('delete-column', column.id)">🗑️</button>
            </div>
          </div>

          <div class="tasks-list">
            <div v-for="task in column.tasks" :key="task.id" class="task-card">
              <div class="task-header">
                <span class="task-name">{{ task.name }}</span>
                <button class="icon-btn small" @click="$emit('delete-task', task.id)">✕</button>
              </div>

              <div class="subtasks-list">
                <div v-for="subtask in task.subtasks" :key="subtask.id" class="subtask-item">
                  <label class="checkbox-label">
                    <input
                      type="checkbox"
                      :checked="false"
                      @change="$emit('subtask-complete', subtask.id, $event.target.checked)"
                    />
                    <span>{{ subtask.name }}</span>
                  </label>
                </div>
              </div>

              <button class="btn-small" @click="$emit('add-subtask', task.id)">+ Подзадача</button>
            </div>
          </div>

          <button class="btn-add-task" @click="$emit('add-task', column.id)">
            + Добавить задачу
          </button>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import type { Board } from '@/types' // Убедитесь, что путь к типам верный

// Принимаем только board, колонки берем из него
defineProps<{
  board: Board | null
}>()

defineEmits<{
  (e: 'add-column'): void
  (e: 'delete-column', id: number): void
  (e: 'add-task', columnId: number): void
  (e: 'delete-task', taskId: number): void
  (e: 'add-subtask', taskId: number): void
  (e: 'subtask-complete', subtaskId: number, isComplete: boolean): void
  (e: 'delete-subtask', subtaskId: number): void
  (e: 'column-menu', item: any): void
  (e: 'task-menu', item: any): void
  (e: 'subtask-edit', item: any): void
  (e: 'assign-subtask-user', item: any): void
}>()
</script>

<style scoped>
.kanban-board {
  display: flex;
  flex-direction: column;
  height: 100%;
  background-color: #f8f9fa;
}

.board-header {
  padding: 1rem 2rem;
  background: white;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.columns-container {
  display: flex;
  gap: 1.5rem;
  overflow-x: auto;
  padding: 2rem;
  height: 100%;
  align-items: flex-start;
}

.column {
  min-width: 300px;
  max-width: 300px;
  background: #ffffff;
  border-radius: 12px;
  padding: 1rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  max-height: 100%;
}

.column-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #f3f4f6;
}

.column-header h3 {
  margin: 0;
  font-size: 1.1rem;
  color: #1f2937;
}

.tasks-list {
  flex-grow: 1;
  overflow-y: auto;
  margin-bottom: 1rem;
  min-height: 50px;
}

.task-card {
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  padding: 0.75rem;
  margin-bottom: 0.75rem;
  border-radius: 8px;
  transition: transform 0.2s;
}

.task-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.task-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}

.task-name {
  font-weight: 500;
  color: #374151;
}

.subtasks-list {
  margin-top: 0.5rem;
  padding-left: 0.5rem;
}

.subtask-item {
  font-size: 0.9rem;
  color: #6b7280;
  margin-bottom: 0.25rem;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

/* Кнопки */
.btn-primary {
  background-color: #3b82f6;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
}

.btn-add-task {
  width: 100%;
  padding: 0.5rem;
  background: transparent;
  border: 1px dashed #d1d5db;
  color: #6b7280;
  border-radius: 6px;
  cursor: pointer;
}

.btn-add-task:hover {
  background: #f3f4f6;
  color: #374151;
}

.btn-small {
  font-size: 0.8rem;
  color: #3b82f6;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
  margin-top: 0.5rem;
}

.icon-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.2rem;
  padding: 0.2rem;
  opacity: 0.6;
}

.icon-btn:hover {
  opacity: 1;
}

.icon-btn.delete:hover {
  color: #ef4444;
}

.empty-state {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  color: #9ca3af;
}
</style>
