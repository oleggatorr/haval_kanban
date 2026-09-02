<!-- src/components/kanban/KanbanTab.vue -->
<template>
  <div v-if="tab" class="tab-content">
    <div class="columns-container">
      <!-- Существующие колонки -->
      <KanbanColumn
        v-for="column in tab.columns"
        :key="column.id"
        :column="column"
        @create-task="$emit('create-task', $event)"
        @delete-column="$emit('delete-column', $event)"
        @delete-task="$emit('delete-task', $event)"
        @create-subtask="$emit('create-subtask', $event)"
        @delete-subtask="$emit('delete-subtask', $event)"
        @toggle-task="$emit('toggle-task', $event, $event)"
      />

      <!-- Кнопка добавления колонки -->
      <div class="add-column-wrapper">
        <button class="add-column-btn" @click="handleAddColumn">
          <span class="plus-icon">+</span>
          <span>Добавить колонку</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Tab } from '@/composables/useKanbanBoard'
import KanbanColumn from './KanbanColumn.vue'

const props = defineProps<{
  tab: Tab | null
}>()

const emit = defineEmits<{
  (e: 'create-column', tabId: number): void
  (e: 'create-task', columnId: number): void
  (e: 'delete-column', columnId: number): void
  (e: 'delete-task', taskId: number): void
  (e: 'create-subtask', taskId: number): void
  (e: 'delete-subtask', subtaskId: number): void
  (e: 'toggle-task', taskId: number, isComplit: boolean): void
}>()

const handleAddColumn = () => {
  if (props.tab?.id) {
    emit('create-column', props.tab.id)
  }
}
</script>

<style scoped>
.tab-content {
  height: calc(100vh - 160px);
  overflow-x: auto;
  overflow-y: hidden;
}

.columns-container {
  display: flex;
  gap: 12px;
  height: 100%;
  padding-bottom: 8px;
  align-items: flex-start;
}

/* Стили для кнопки добавления колонки */
.add-column-wrapper {
  flex-shrink: 0;
  min-width: 240px;
  height: 100%;
  padding-top: 2px;
}

.add-column-btn {
  width: 100%;
  min-height: 60px;
  padding: 12px 16px;
  background-color: #f4f5f7;
  border: 2px dashed #d0d4d9;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 500;
  color: #5e6c84;
  transition: all 0.2s ease;
}

.add-column-btn:hover {
  background-color: #ebecf0;
  border-color: #b3b9c4;
  color: #172b4d;
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.add-column-btn:active {
  transform: translateY(0);
}

.plus-icon {
  font-size: 20px;
  line-height: 1;
  font-weight: 300;
}
</style>
