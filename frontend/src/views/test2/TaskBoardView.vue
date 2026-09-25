<!-- src\views\test2\TaskBoardView.vue -->

<template>
  <div class="app-layout">
    <main class="main-content">
      <header class="top-bar">
        <div class="breadcrumbs">
          <span>Проекты</span> /
          <!-- Отображаем ID проекта, если доска загружена -->
          <span v-if="board">№{{ board.project_id }}</span> /
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
        <!-- error в useKanbanBoard теперь строка, поэтому выводим напрямую -->
        <p class="error-text">{{ error }}</p>
        <button @click="fetchBoard" class="retry-btn">Повторить попытку</button>
      </div>

      <!-- Рендерим доску ТОЛЬКО если board существует -->
      <div v-else-if="board" class="board-wrapper">
        <!-- Для проверки структуры данных можно временно оставить pre -->
        <!-- <pre>{{ { board, columns, tasks, subtasks } }}</pre> -->

        <KanbanBoard
          :board="board"
          :columns="columns"
          :tasks="tasks"
          :subtasks="subtasks"
          :loading="loading"
          :error="null"
          @add-column="createColumn"
          @delete-column="deleteColumn"
          @add-task="createTask"
          @delete-task="deleteTask"
          @add-subtask="createSubtask"
          @delete-subtask="deleteSubtask"
          @subtask-complete="toggleSubtaskStatus"
          @column-menu="handleMenu"
          @task-menu="handleMenu"
          @subtask-edit="handleMenu"
          @assign-subtask-user="handleAssignUser"
        />
      </div>

      <div v-else class="loading-container">
        <p>Данные не найдены</p>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router' // Импорт для получения параметров URL
import KanbanBoard from './task_board_components/KanbanBoard.vue'
import { useKanbanBoard } from '@/composables/useKanbanBoard'

// 1. Получаем ID из адресной строки (например, /board/1)
const route = useRoute()

// Преобразуем параметр в число. Если параметра нет, используем 1 как fallback
const projectId = computed(() => Number(route.params.id) || 1)

// 2. Инициализируем композабл, передавая ему ref на projectId
// Теперь загрузка произойдет автоматически при монтировании
const {
  loading,
  error,
  projectName,
  board,
  columns,
  tasks,
  subtasks,
  fetchBoard, // Функция для ручного обновления (кнопка "Повторить")
  createColumn,
  deleteColumn,
  createTask,
  deleteTask,
  // updateTaskStatus, // Если нужно будет использовать внутри компонента
  createSubtask,
  deleteSubtask,
  toggleSubtaskStatus,
} = useKanbanBoard(projectId)

// Обработчики событий (заглушки или логика UI)
const handleMenu = (item: any) => {
  console.log('Меню:', item)
}

const handleAssignUser = (subtask: any) => {
  console.log('Назначение пользователя:', subtask)
}
</script>

<style scoped>
.app-layout {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-content {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.top-bar {
  padding: 1rem 2rem;
  background: white;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.breadcrumbs {
  font-size: 0.9rem;
  color: #6b7280;
}

.user-profile {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 500;
}

.avatar {
  width: 32px;
  height: 32px;
  background: #3b82f6;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.8rem;
}

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

.board-wrapper {
  height: 100%;
  overflow: hidden;
}
</style>
