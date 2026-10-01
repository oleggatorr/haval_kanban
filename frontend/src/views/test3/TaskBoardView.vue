<!-- src\views\test3\TaskBoardView.vue -->
<template>
  <div class="project-board-container">
    <div v-if="isLoading" class="loading-overlay">
      <div class="spinner"></div>
      <p>Загрузка проекта и доски...</p>
    </div>

    <div v-else-if="hasError" class="error-overlay">
      <h3>Произошла ошибка</h3>
      <p>{{ errorMessage }}</p>
      <button @click="reloadAll" class="retry-btn">Попробовать снова</button>
    </div>

    <div v-else class="board-content">
      <KanbanBoard
        :statuses="projectInfo.statuses.value"
        :board="taskBoard.board.value"
        :columns="taskBoard.columns.value"
        :tasks="taskBoard.tasks.value"
        :subtasks="taskBoard.subtasks.value"
        @update-board="(data) => taskBoard.updateBoard(data)"
        @create-column="(name) => taskBoard.createColumn({ name })"
        @update-column="(data) => taskBoard.updateColumn(data)"
        @delete-column="(id) => taskBoard.deleteColumn(id)"
        @create-task="(payload) => taskBoard.createTask(payload.columnId, payload.data)"
        @update-task="(data) => taskBoard.updateTask(data)"
        @delete-task="(id) => taskBoard.deleteTask(id)"
        @create-subtask="(payload) => taskBoard.createSubtask(payload.taskId, payload.data)"
        @update-subtask="(data) => taskBoard.updateSubtask(data)"
        @delete-subtask="(id) => taskBoard.deleteSubtask(id)"
        @subtask-complete="(id) => taskBoard.toggleSubtaskStatus(id, true)"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, provide, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useProjectInfo } from '@/composables/taskboard/useTaskBoardInfo'
import { useTaskBoard } from '@/composables/taskboard/useTaskBoard'
import KanbanBoard from './task_board_components/bigfile.vue' // Или KanbanBoardUnified.vue

const route = useRoute()
const projectId = Number(route.params.projectId)

const projectInfo = useProjectInfo(projectId)
const taskBoard = useTaskBoard(projectId)

const isLoading = computed(() => projectInfo.loading.value || taskBoard.loading.value)
const hasError = computed(() => !!projectInfo.error.value || !!taskBoard.error.value)
const errorMessage = computed(() => projectInfo.error.value || taskBoard.error.value)

const reloadAll = async () => {
  await Promise.all([projectInfo.fetchProjectInfo(), taskBoard.fetchBoard()])
}

// Provide оставляем как было, если другие компоненты используют его
provide('projectContext', {
  project: projectInfo.project,
  members: projectInfo.members,
  statuses: projectInfo.statuses,
})
</script>

<style scoped>
/* Ваши стили остаются без изменений */
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
