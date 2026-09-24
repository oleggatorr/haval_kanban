<template>
  <div class="app-layout">
    <main class="main-content">
      <header class="top-bar">
        <div class="breadcrumbs">
          <span>Проекты</span> / <span v-if="board">№{{ board.project_id }}</span> /
          <b>{{ projectName || 'Загрузка...' }}</b>
        </div>
        <div class="user-profile">
          <span class="avatar">ОФ</span>
          <span>Олег Фещенко</span>
        </div>
      </header>

      <!-- Состояние загрузки -->
      <div v-if="loading" class="loading-container">
        <p>Загрузка доски...</p>
      </div>

      <!-- Состояние ошибки -->
      <div v-else-if="error" class="error-container">
        <p class="error-text">{{ error }}</p>
        <button @click="fetchBoard" class="retry-btn">Повторить попытку</button>
      </div>

      <!-- Рендерим доску ТОЛЬКО если board существует -->
      <div v-else-if="board" class="board-wrapper">
        <KanbanBoard
          :board="board"
          :columns="columns"
          @add-column="createColumn"
          @column-menu="handleMenu"
          @add-task="createTask"
          @task-menu="handleMenu"
          @add-subtask="createSubtask"
          @subtask-complete="toggleSubtaskStatus"
          @subtask-edit="handleMenu"
          @assign-subtask-user="handleAssignUser"
          @delete-column="deleteColumn"
          @delete-task="deleteTask"
          @delete-subtask="deleteSubtask"
        />
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import KanbanBoard from './task_board_components/KanbanBoard.vue'
import { useKanbanBoard } from '@/composables/useKanbanBoard'

const {
  loading,
  error,
  projectName,
  board,
  columns,
  fetchBoard,
  createColumn,
  deleteColumn,
  createTask,
  deleteTask,
  updateTaskStatus,
  createSubtask,
  deleteSubtask,
} = useKanbanBoard()

const handleMenu = (item: any) => {
  console.log('Меню:', item)
}

const handleAssignUser = (subtask: any) => {
  console.log('Назначение пользователя:', subtask)
}

const toggleSubtaskStatus = (subtaskId: number, isCompleted: boolean) => {
  // TODO: Реализовать логику обновления статуса подзадачи через API
  console.log('Toggle subtask', subtaskId, isCompleted)
}
</script>

<style scoped>
.loading-container,
.error-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 300px;
  font-size: 1.2rem;
}
.error-text {
  color: #dc2626;
  margin-bottom: 1rem;
}
.retry-btn {
  padding: 8px 16px;
  background-color: #3b82f6;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.retry-btn:hover {
  background-color: #2563eb;
}
</style>
