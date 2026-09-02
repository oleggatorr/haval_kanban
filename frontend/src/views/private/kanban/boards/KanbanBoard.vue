<!-- src/components/layout/KanbanBoard.vue -->
<template>
  <div class="kanban-container">
    <div v-if="loading" class="loading"><p>Загрузка канбан-доски...</p></div>

    <div v-else-if="error" class="error">
      <p>{{ error }}</p>
      <button @click="fetchBoard">Повторить попытку</button>
    </div>

    <div v-else-if="tabs.length > 0" class="kanban-board">
      <!-- Навигация по табам -->
      <div class="tabs-navigation">
        <div v-for="tab in tabsWithCount" :key="tab.id" class="tab-wrapper">
          <button
            :class="['tab-btn', { active: activeTabId === tab.id }]"
            @click="setActiveTab(tab.id)"
          >
            {{ tab.name }}
            <span class="tab-badge">{{ tab.taskCount }}</span>
          </button>

          <!-- Кнопка удаления таба -->
          <ActionButton
            v-if="activeTabId === tab.id"
            icon="🗑️"
            tooltip="Удалить вкладку"
            @click.stop="deleteTab(tab.id)"
            class="delete-tab-btn"
          />
        </div>

        <ActionButton icon="+" tooltip="Создать вкладку" @click="createTab" class="add-tab-btn" />
      </div>

      <!-- Активный таб -->
      <KanbanTab
        v-if="activeTab"
        :tab="activeTab"
        @create-column="handleCreateColumn"
        @delete-column="handleDeleteColumn"
        @create-task="handleCreateTask"
        @delete-task="handleDeleteTask"
        @create-subtask="handleCreateSubtask"
        @delete-subtask="handleDeleteSubtask"
        @toggle-task="handleToggleTask"
        @task-moved="handleTaskMoved"
        @move-task="handleMoveTask"
      />
    </div>

    <!-- Пустое состояние с кнопкой создания -->
    <div v-else class="empty-state">
      <div class="empty-state-content">
        <div class="empty-state-icon">📋</div>
        <h2 class="empty-state-title">Нет вкладок</h2>
        <p class="empty-state-description">Создайте первую вкладку, чтобы начать работу с доской</p>
        <button class="empty-state-btn" @click="createTab">
          <span class="btn-icon">+</span>
          Создать вкладку
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useKanbanBoard } from '@/composables/useKanbanBoard'
import KanbanTab from '@/components/kanban/KanbanTab.vue'
import ActionButton from '@/components/ui/ActionButton.vue'

const {
  loading,
  error,
  tabs,
  activeTabId,
  activeTab,
  tabsWithCount,
  fetchBoard,
  setActiveTab,
  createTab,
  deleteTab,
  createColumn,
  deleteColumn,
  createTask,
  deleteTask,
  createSubtask,
  deleteSubtask,
  toggleTask,
} = useKanbanBoard()

// Обработчики событий
const handleCreateColumn = (tabId: number) => createColumn(tabId)
const handleDeleteColumn = (columnId: number) => deleteColumn(columnId)
const handleCreateTask = (columnId: number) => createTask(columnId)
const handleDeleteTask = (taskId: number) => deleteTask(taskId)
const handleCreateSubtask = (taskId: number) => createSubtask(taskId)
const handleDeleteSubtask = (subtaskId: number) => deleteSubtask(subtaskId)
const handleToggleTask = (taskId: number, isComplit: boolean) => toggleTask(taskId, isComplit)
</script>

<style scoped>
.kanban-container {
  padding: 20px;
  height: 100%;
}

.loading,
.error {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 400px;
  color: #5e6c84;
}

.error button {
  margin-top: 12px;
  padding: 8px 20px;
  background-color: #0052cc;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.error button:hover {
  background-color: #0047b3;
}

.tabs-navigation {
  display: flex;
  gap: 4px;
  margin-bottom: 20px;
  background-color: white;
  border-radius: 8px;
  padding: 4px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  overflow-x: auto;
  flex-wrap: wrap;
  align-items: center;
}

.tab-wrapper {
  display: flex;
  align-items: center;
  position: relative;
}

.tab-btn {
  padding: 10px 20px;
  border: none;
  background: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  color: #5e6c84;
  transition: all 0.2s;
  white-space: nowrap;
  display: flex;
  align-items: center;
  gap: 8px;
}

.tab-btn:hover {
  background-color: #ebecf0;
  color: #172b4d;
}

.tab-btn.active {
  background-color: #0052cc;
  color: white;
}

.tab-btn.active .tab-badge {
  background-color: rgba(255, 255, 255, 0.2);
  color: white;
}

.delete-tab-btn {
  margin-left: 4px;
  opacity: 0;
  transition: opacity 0.2s;
}

.tab-wrapper:hover .delete-tab-btn {
  opacity: 1;
}

.tab-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background-color: #ebecf0;
  color: #5e6c84;
  font-size: 11px;
  font-weight: 600;
  padding: 0 8px;
  border-radius: 12px;
  height: 20px;
  min-width: 20px;
}

.add-tab-btn {
  margin-left: 8px;
}

/* Стили для пустого состояния */
.empty-state {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 500px;
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.empty-state-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 40px;
  max-width: 400px;
}

.empty-state-icon {
  font-size: 64px;
  margin-bottom: 16px;
  opacity: 0.5;
}

.empty-state-title {
  font-size: 24px;
  font-weight: 600;
  color: #172b4d;
  margin: 0 0 8px 0;
}

.empty-state-description {
  font-size: 16px;
  color: #5e6c84;
  margin: 0 0 24px 0;
  line-height: 1.5;
}

.empty-state-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background-color: #0052cc;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.empty-state-btn:hover {
  background-color: #0047b3;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 82, 204, 0.3);
}

.empty-state-btn:active {
  transform: translateY(0);
}

.btn-icon {
  font-size: 20px;
  font-weight: 300;
}
</style>
