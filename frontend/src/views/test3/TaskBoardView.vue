<template>
  <div class="project-board-container">
    <!-- Индикатор загрузки -->
    <div v-if="isLoading" class="loading-overlay">
      <div class="spinner"></div>
      <p>Загрузка проекта и доски...</p>
    </div>

    <!-- Сообщение об ошибке -->
    <div v-else-if="hasError" class="error-overlay">
      <h3>Произошла ошибка</h3>
      <p>{{ errorMessage }}</p>
      <button @click="reloadAll" class="retry-btn">Попробовать снова</button>
    </div>

    <!-- Основной контент -->
    <div v-else class="board-content">
      <!-- Подключаем компонент доски -->
      <KanbanBoard
        :board="taskBoard.board.value"
        :columns="taskBoard.columns.value"
        :tasks="taskBoard.tasks.value"
        :subtasks="taskBoard.subtasks.value"
        @create-column="taskBoard.createColumn"
        @delete-column="taskBoard.deleteColumn"
        @add-task="handleAddTask"
        @delete-task="taskBoard.deleteTask"
        @subtask-complete="handleSubtaskComplete"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, provide, watch } from 'vue'
import { useRoute } from 'vue-router'
// Убедись, что пути к композаблам верные!
import { useProjectInfo } from '@/composables/taskboard/useTaskBoardInfo'
import { useTaskBoard } from '@/composables/taskboard/useTaskBoard'

// Импорт компонента доски
import KanbanBoard from './task_board_components/KanbanBoard.vue'

const route = useRoute()
const projectId = Number(route.params.projectId)

console.log('[ProjectBoardContainer] Инициализация. Project ID:', projectId)

// 1. Инициализируем композаблы
const projectInfo = useProjectInfo(projectId)
const taskBoard = useTaskBoard(projectId)

// 2. Объединяем состояния
const isLoading = computed(() => projectInfo.loading.value || taskBoard.loading.value)
const hasError = computed(() => !!projectInfo.error.value || !!taskBoard.error.value)
const errorMessage = computed(() => projectInfo.error.value || taskBoard.error.value)

// 3. Перезагрузка
const reloadAll = () => {
  console.log('[ProjectBoardContainer] Ручная перезагрузка...')
  projectInfo.fetchProjectInfo()
  taskBoard.fetchBoard()
}

// 4. Хелперы для обработки событий
const handleAddTask = (columnId: number) => {
  // Создаем задачу с дефолтным именем
  taskBoard.createTask(columnId, { name: 'Новая задача' })
}

const handleSubtaskComplete = (subtaskId: number, isCompleted: boolean) => {
  taskBoard.toggleSubtaskStatus(subtaskId, isCompleted)
}

// 5. Provide для глубоких компонентов
provide('projectContext', {
  project: projectInfo.project,
  members: projectInfo.members,
  statuses: projectInfo.statuses,
})

provide('boardActions', {
  board: taskBoard.board,
  columns: taskBoard.columns,
  tasks: taskBoard.tasks,
  subtasks: taskBoard.subtasks,
  createColumn: taskBoard.createColumn,
  deleteColumn: taskBoard.deleteColumn,
  createTask: taskBoard.createTask,
  updateTask: taskBoard.updateTask,
  moveTask: taskBoard.moveTask,
  deleteTask: taskBoard.deleteTask,
  toggleSubtask: taskBoard.toggleSubtaskStatus,
  getTasksByColumn: taskBoard.getTasksByColumn,
  getSubtasksByTask: taskBoard.getSubtasksByTask,
})

// Логирование изменений
watch([projectInfo.project, taskBoard.board], ([newProject, newBoard]) => {
  if (newProject) console.log('[ProjectBoardContainer] Проект загружен:', newProject.name)
  if (newBoard) console.log('[ProjectBoardContainer] Доска загружена:', newBoard.id)
})
</script>

<style scoped>
.project-board-container {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.loading-overlay,
.error-overlay {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100%;
  gap: 1rem;
}

.retry-btn {
  padding: 8px 16px;
  background-color: #3b82f6;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.board-content {
  flex-grow: 1;
  overflow: hidden;
  position: relative;
}
</style>
