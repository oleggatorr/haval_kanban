<template>
  <section class="column">
    <!-- Заголовок колонки -->
    <div class="column-head">
      <div class="column-title">
        <span class="dot" :style="{ background: columnColor }"></span>
        <h2>
          {{ column.name }} <span class="count">{{ tasks.length }}</span>
        </h2>
      </div>

      <!-- Используем DropdownMenu -->
      <DropdownMenu align="right">
        <div class="menu-item" @click="$emit('move-column', { column, direction: 'left' })">
          ⬅️ Сдвинуть влево
        </div>
        <div class="menu-item" @click="$emit('move-column', { column, direction: 'right' })">
          Сдвинуть вправо ➡️
        </div>

        <!-- ИЗМЕНЕНО: Открываем модалку создания задачи -->
        <div class="menu-item" @click.stop="isCreateTaskOpen = true">➕ Создать задачу</div>

        <div class="menu-item" @click.stop="openColumnSettings">⚙️ Настроить</div>
      </DropdownMenu>
    </div>

    <!-- Список задач -->
    <div class="column-content">
      <TaskCard
        v-for="task in tasks"
        :key="task.id"
        :task="task"
        :subtasks="getSubtasksForTask(task.id)"
        :column="column"
        @menu="(t) => $emit('task-menu', t)"
        @add-subtask="(id) => $emit('add-subtask', id)"
        @subtask-complete="(id) => $emit('subtask-complete', id)"
        @subtask-edit="(s) => $emit('subtask-edit', s)"
        @edit="(t) => $emit('task-edit', t)"
        @delete="(t) => $emit('task-delete', t)"
        @move-task="(payload) => $emit('move-task', payload)"
      />

      <!-- ИЗМЕНЕНО: Открываем модалку создания задачи -->
      <!-- <button class="add-task-btn" @click="isCreateTaskOpen = true">➕ Добавить задачу</button> -->

      <div class="scroll-spacer"></div>
    </div>

    <!-- Модальное окно редактирования колонки -->
    <EditColumnModal v-model="isEditColumnModalOpen" :column="column" @save="handleColumnUpdate" />

    <!-- Модальное окно создания задачи -->
    <CreateTaskModal v-model="isCreateTaskOpen" @save="handleCreateTask" />
  </section>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import TaskCard from './TaskCard.vue'
import DropdownMenu from '@/components/ui/DropdownMenu.vue'
import EditColumnModal from './edit_forms/EditColumnModal.vue'
import CreateTaskModal from './create_forms/CreateTaskModal.vue' // Импорт нового компонента

interface Column {
  name: string
  description: string | null
  flags: any[]
  position: number
  id: number
  board_id: number
  create_at: string
  update_at: string | null
  is_active: boolean
  remove_at: string | null
}

interface Task {
  id: number
  column_id: number
  [key: string]: any
}

interface Subtask {
  id: number
  parent_task_id: number
  [key: string]: any
}

const props = defineProps<{
  column: Column
  tasks: Task[]
  allSubtasks: Subtask[]
}>()

const emit = defineEmits<{
  (e: 'menu', column: Column): void
  (e: 'rename-column', column: Column): void
  (e: 'delete-column', column: Column): void
  (e: 'settings-column', column: Column): void
  (e: 'move-column', payload: { column: Column; direction: string }): void
  (e: 'create-task', columnId: number): void
  (e: 'task-menu', task: Task): void
  (e: 'task-edit', task: Task): void
  (e: 'task-delete', task: Task): void
  (e: 'move-task', payload: any): void
  (e: 'add-subtask', taskId: number): void
  (e: 'subtask-complete', subtaskId: number): void
  (e: 'subtask-edit', subtask: Subtask): void
  (e: 'update-column', data: Partial<Column> & { id: number }): void
  // Новое событие для создания задачи с данными
  (e: 'create-task-with-data', payload: { columnId: number; data: any }): void
}>()

// --- ЛОГИКА МОДАЛЬНЫХ ОКОН ---
const isEditColumnModalOpen = ref(false)
const isCreateTaskOpen = ref(false) // Состояние для модалки создания задачи

const openColumnSettings = () => {
  isEditColumnModalOpen.value = true
}

const handleColumnUpdate = (updatedData: any) => {
  console.log('Сохранение колонки:', updatedData)
  emit('update-column', { ...props.column, ...updatedData })
}

const handleCreateTask = (data: any) => {
  console.log('Создание задачи:', data)
  emit('create-task-with-data', {
    columnId: props.column.id,
    data,
  })
}
// -----------------------------

const columnColor = computed(() => {
  const colors = ['#168be5', '#ff9f43', '#2ecc71', '#9b59b6', '#e74c3c']
  return colors[props.column.position % colors.length] || '#cbd5e0'
})

const getSubtasksForTask = (taskId: number) => {
  return props.allSubtasks.filter((s) => s.parent_task_id === taskId)
}
</script>

<style scoped>
/* Стили без изменений */
.column {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 16px;
  width: 390px;
  min-width: 380px;
  max-width: 400px;
  flex-grow: 0;
  flex-shrink: 0;
  flex-basis: 340px;
  display: flex;
  flex-direction: column;
  height: 100%;
  box-sizing: border-box;
}

.column-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
  padding: 0 4px;
  flex-shrink: 0;
}

.column-title {
  display: flex;
  align-items: center;
  gap: 8px;
}

.column-title h2 {
  margin: 0;
  font-size: 15px;
  font-weight: 600;
  color: #4a5568;
  display: flex;
  align-items: center;
  gap: 8px;
}

.count {
  background: #e2e8f0;
  color: #4a5568;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
}

.dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
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

.column-content {
  overflow-y: auto;
  flex: 1;
  padding-right: 4px;
  margin-right: -4px;
}

.column-content::-webkit-scrollbar {
  width: 6px;
}
.column-content::-webkit-scrollbar-track {
  background: transparent;
}
.column-content::-webkit-scrollbar-thumb {
  background-color: #cbd5e0;
  border-radius: 3px;
}
.column-content::-webkit-scrollbar-thumb:hover {
  background-color: #a0aec0;
}

.add-task-btn {
  width: 100%;
  padding: 10px;
  margin-top: 8px;
  background: transparent;
  border: 1px dashed #cbd5e0;
  border-radius: 8px;
  color: #718096;
  cursor: pointer;
  font-size: 13px;
  transition: all 0.2s;
  text-align: left;
}

.add-task-btn:hover {
  background: #edf2f7;
  border-color: #168be5;
  color: #168be5;
}

.scroll-spacer {
  height: 100px;
  width: 100%;
}
</style>
