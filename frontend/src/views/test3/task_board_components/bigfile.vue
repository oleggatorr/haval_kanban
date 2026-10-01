<template>
  <div class="kanban-board">
    <div v-if="!board" class="empty-state">
      <p>Загрузка доски...</p>
    </div>

    <template v-else>
      <!-- Шапка доски -->
      <div class="board-header">
        <h2>{{ board.name }}</h2>
        <DropdownMenu align="right">
          <div class="menu-item" @click.stop="isCreateColumnOpen = true">➕ Добавить колонку</div>
          <div class="menu-item" @click.stop="isEditBoardOpen = true">⚙️ Настройки доски</div>
        </DropdownMenu>
      </div>

      <!-- Контейнер колонок -->
      <div class="columns-container">
        <section v-for="column in sortedColumns" :key="column.id" class="column">
          <!-- Заголовок колонки -->
          <div class="column-head">
            <div class="column-title">
              <span class="dot" :style="{ background: columnColor(column.position) }"></span>
              <h2>
                {{ column.name }}
                <span class="count">{{ getTasksByColumn(column.id).length }}</span>
              </h2>
            </div>

            <DropdownMenu align="right">
              <div class="menu-item" @click="moveColumn({ column, direction: 'left' })">
                ⬅️ Сдвинуть влево
              </div>
              <div class="menu-item" @click="moveColumn({ column, direction: 'right' })">
                Сдвинуть вправо ➡️
              </div>
              <div class="menu-item" @click.stop="openCreateTask(column.id)">➕ Создать задачу</div>
              <div class="menu-item" @click.stop="openColumnSettings(column)">⚙️ Настроить</div>
            </DropdownMenu>
          </div>

          <!-- Список задач -->
          <div class="column-content">
            <article
              v-for="task in getTasksByColumn(column.id)"
              :key="task.id"
              class="card"
              :class="{ 'is-active': task.is_active }"
            >
              <div class="card-top">
                <span class="tag">{{ getStatusName(task.status_id) }}</span>
                <DropdownMenu align="right">
                  <div class="menu-item" @click.stop="openTaskSettings(task)">✏️ Редактировать</div>
                  <div class="menu-item" @click.stop="moveTaskToAnotherColumn(task)">
                    ↔️ Переместить в...
                  </div>
                  <div class="menu-item" @click.stop="openCreateSubtask(task.id)">
                    ➕ Добавить подзадачу
                  </div>
                  <div class="menu-item" @click="deleteTask(task.id)">🗑️ Удалить</div>
                </DropdownMenu>
              </div>

              <h3 class="card-title">{{ task.name }}</h3>
              <div v-if="task.description" class="card-desc">{{ task.description }}</div>

              <!-- Даты задачи -->
              <div class="task-dates">
                <span v-if="task.planing_date_time_start" class="date-small">
                  🟢 {{ formatDate(task.planing_date_time_start) }}
                </span>
                <span v-if="task.planing_date_time_end" class="date-small">
                  🔴 {{ formatDate(task.planing_date_time_end) }}
                </span>
              </div>

              <!-- Прогресс подзадач -->
              <div v-if="task.subtasks_count > 0" class="progress-section">
                <div class="progress-info">
                  <span
                    >{{ task.completed_subtasks_count }}/{{ task.subtasks_count }} подзадач</span
                  >
                  <span>{{ getTaskProgress(task) }}%</span>
                </div>
                <div class="progress-bar">
                  <div class="progress-fill" :style="{ width: getTaskProgress(task) + '%' }"></div>
                </div>
              </div>

              <!-- Подзадачи (упрощенный вид) -->
              <div v-if="getSubtasksForTask(task.id).length > 0" class="subtasks-preview">
                <button class="subtasks-toggle" @click.stop="toggleSubtasks(task.id)">
                  <span class="toggle-icon">{{ isTaskExpanded(task.id) ? '▼' : '▶' }}</span>
                  <span>Подзадачи</span>
                </button>

                <Transition name="slide">
                  <div v-show="isTaskExpanded(task.id)" class="subtasks-list">
                    <div
                      v-for="subtask in getSubtasksForTask(task.id)"
                      :key="subtask.id"
                      class="subtask-item"
                    >
                      <div class="subtask-row">
                        <button
                          class="status-check"
                          @click.stop="toggleSubtaskComplete(subtask.id)"
                        >
                          {{ subtask.date_time_end ? '✅' : '⭕' }}
                        </button>
                        <span :class="{ 'is-done': !!subtask.date_time_end }">{{
                          subtask.name
                        }}</span>
                        <DropdownMenu align="right">
                          <div class="menu-item" @click.stop="openSubtaskSettings(subtask)">
                            ✏️ Изменить
                          </div>
                          <div class="menu-item" @click="deleteSubtask(subtask.id)">🗑️ Удалить</div>
                        </DropdownMenu>
                      </div>
                    </div>
                  </div>
                </Transition>
              </div>

              <div class="card-foot">
                <div class="meta">
                  <div v-if="task.users && task.users.length > 0" class="user-avatars">
                    <span
                      v-for="user in task.users.slice(0, 3)"
                      :key="user.id"
                      class="mini-avatar"
                      :title="user.name || user.login"
                    >
                      {{ getUserInitials(user) }}
                    </span>
                  </div>
                </div>
              </div>
            </article>

            <div class="scroll-spacer"></div>
          </div>
        </section>

        <div class="spacer"></div>
      </div>
    </template>

    <!-- ==================== МОДАЛЬНЫЕ ОКНА ==================== -->

    <!-- Создание/Редактирование Колонки -->
    <div
      v-if="isCreateColumnOpen || isEditColumnModalOpen"
      class="modal-overlay"
      @click.self="closeColumnModal"
    >
      <div class="modal">
        <h3>{{ isCreateColumnOpen ? 'Создать колонку' : 'Настройки колонки' }}</h3>
        <input v-model="editColumnName" placeholder="Название колонки" />
        <div class="modal-actions">
          <button @click="closeColumnModal">Отмена</button>
          <button
            v-if="isEditColumnModalOpen"
            class="danger"
            @click="confirmDeleteColumn(editingColumn?.id)"
          >
            🗑️ Удалить
          </button>
          <button
            class="primary"
            @click="isCreateColumnOpen ? handleCreateColumn() : handleUpdateColumn()"
          >
            Сохранить
          </button>
        </div>
      </div>
    </div>

    <!-- Создание/Редактирование Задачи -->
    <div
      v-if="isCreateTaskOpen || isEditTaskModalOpen"
      class="modal-overlay"
      @click.self="closeTaskModal"
    >
      <div class="modal modal-lg">
        <h3>{{ isCreateTaskOpen ? 'Создать задачу' : 'Редактировать задачу' }}</h3>

        <div class="form-grid">
          <div class="form-group full">
            <label>Название</label>
            <input v-model="editTaskName" placeholder="Название задачи" />
          </div>

          <div class="form-group full">
            <label>Описание</label>
            <textarea v-model="editTaskDescription" placeholder="Описание"></textarea>
          </div>

          <div class="form-group">
            <label>Статус</label>
            <select v-model="editTaskStatusId">
              <option :value="null">Без статуса</option>
              <option v-for="s in statuses" :key="s.id" :value="s.id">{{ s.name }}</option>
            </select>
          </div>

          <div class="form-group">
            <label>План. начало</label>
            <input type="datetime-local" v-model="editTaskPlanStart" />
          </div>

          <div class="form-group">
            <label>План. конец</label>
            <input type="datetime-local" v-model="editTaskPlanEnd" />
          </div>
        </div>

        <div class="modal-actions">
          <button @click="closeTaskModal">Отмена</button>
          <button
            v-if="isEditTaskModalOpen"
            class="danger"
            @click="confirmDeleteTask(editingTask?.id)"
          >
            🗑️ Удалить
          </button>
          <button
            class="primary"
            @click="isCreateTaskOpen ? handleCreateTask() : handleUpdateTask()"
          >
            Сохранить
          </button>
        </div>
      </div>
    </div>

    <!-- Создание/Редактирование Подзадачи -->
    <div
      v-if="isCreateSubtaskOpen || isEditSubtaskModalOpen"
      class="modal-overlay"
      @click.self="closeSubtaskModal"
    >
      <div class="modal">
        <h3>{{ isCreateSubtaskOpen ? 'Создать подзадачу' : 'Редактировать подзадачу' }}</h3>

        <div class="form-grid">
          <div class="form-group full">
            <label>Название</label>
            <input v-model="editSubtaskName" placeholder="Название подзадачи" />
          </div>

          <div class="form-group full">
            <label>Описание</label>
            <textarea v-model="editSubtaskDescription" placeholder="Описание"></textarea>
          </div>

          <div class="form-group">
            <label>Статус</label>
            <select v-model="editSubtaskStatusId">
              <option :value="null">Без статуса</option>
              <option v-for="s in statuses" :key="s.id" :value="s.id">{{ s.name }}</option>
            </select>
          </div>
        </div>

        <div class="modal-actions">
          <button @click="closeSubtaskModal">Отмена</button>
          <button
            v-if="isEditSubtaskModalOpen"
            class="danger"
            @click="confirmDeleteSubtask(editingSubtask?.id)"
          >
            🗑️ Удалить
          </button>
          <button
            class="primary"
            @click="isCreateSubtaskOpen ? handleCreateSubtask() : handleUpdateSubtask()"
          >
            Сохранить
          </button>
        </div>
      </div>
    </div>

    <!-- Перемещение задачи -->
    <div v-if="isMoveTaskOpen" class="modal-overlay" @click.self="isMoveTaskOpen = false">
      <div class="modal">
        <h3>Переместить "{{ movingTask?.name }}"</h3>
        <div class="column-list">
          <div
            v-for="col in sortedColumns"
            :key="col.id"
            class="column-option"
            :class="{ 'is-current': col.id === movingTask?.column_id }"
            @click="handleMoveTaskConfirm(col.id)"
          >
            <span class="dot" :style="{ background: columnColor(col.position) }"></span>
            <span>{{ col.name }}</span>
          </div>
        </div>
        <div class="modal-actions">
          <button @click="isMoveTaskOpen = false">Отмена</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import DropdownMenu from '@/components/ui/DropdownMenu.vue'

// ==================== ТИПЫ ====================

interface TaskUser {
  id: number
  name?: string
  login?: string
}

interface StatusItem {
  id: number
  name: string
  description: string
  is_default: boolean
  is_final: boolean
  is_active: boolean
}

interface Subtask {
  id: number
  parent_task_id: number
  name: string
  description: string
  status_id: number | null
  date_time_start: string | null
  date_time_end: string | null
  users: TaskUser[]
}

interface Task {
  id: number
  column_id: number
  name: string
  description: string
  position: number
  status_id: number | null
  date_time_start: string | null
  date_time_end: string | null
  planing_date_time_start: string | null
  planing_date_time_end: string | null
  data: any | null
  users: TaskUser[]
  subtasks_count: number
  completed_subtasks_count: number
  is_active?: boolean // Для стилизации
}

interface Column {
  id: number
  name: string
  description: string | null
  flags: any[]
  position: number
  board_id: number
  create_at: string
  update_at: string | null
  is_active: boolean
  remove_at: string | null
}

interface Board {
  id: number
  name: string
  [key: string]: any
}

// ==================== PROPS & EMITS ====================

const props = defineProps<{
  board: Board | null
  columns: Column[]
  tasks: Task[]
  subtasks: Subtask[]
  statuses: StatusItem[]
}>()

const emit = defineEmits<{
  (e: 'update-board', data: Partial<Board>): void
  (e: 'create-column', name: string): void
  (e: 'update-column', data: Partial<Column> & { id: number }): void
  (e: 'delete-column', id: number): void
  (e: 'create-task', payload: { columnId: number; data: Partial<Task> }): void
  (e: 'update-task', data: Partial<Task> & { id: number }): void
  (e: 'delete-task', taskId: number): void
  (e: 'create-subtask', payload: { taskId: number; data: Partial<Subtask> }): void
  (e: 'update-subtask', data: Partial<Subtask> & { id: number }): void
  (e: 'delete-subtask', subtaskId: number): void
  (e: 'subtask-complete', subtaskId: number): void
}>()

// ==================== ЛОКАЛЬНОЕ СОСТОЯНИЕ ====================

const isCreateColumnOpen = ref(false)
const isEditBoardOpen = ref(false)
const isEditColumnModalOpen = ref(false)
const isCreateTaskOpen = ref(false)
const isEditTaskModalOpen = ref(false)
const isCreateSubtaskOpen = ref(false)
const isEditSubtaskModalOpen = ref(false)
const isMoveTaskOpen = ref(false)

const editingColumn = ref<Column | null>(null)
const editingTask = ref<Task | null>(null)
const editingSubtask = ref<Subtask | null>(null)
const movingTask = ref<Task | null>(null)
const activeColumnId = ref<number | null>(null)
const activeTaskId = ref<number | null>(null)

// Поля форм
const newColumnName = ref('')
const editBoardName = ref('')
const editColumnName = ref('')

const newTaskName = ref('')
const newTaskDescription = ref('')
const editTaskName = ref('')
const editTaskDescription = ref('')
const editTaskStatusId = ref<number | null>(null)
const editTaskPlanStart = ref<string>('')
const editTaskPlanEnd = ref<string>('')

const newSubtaskName = ref('')
const newSubtaskDescription = ref('')
const editSubtaskName = ref('')
const editSubtaskDescription = ref('')
const editSubtaskStatusId = ref<number | null>(null)

const expandedTaskIds = ref<Set<number>>(new Set())

// ==================== ВЫЧИСЛЯЕМЫЕ СВОЙСТВА ====================

const sortedColumns = computed(() => [...props.columns].sort((a, b) => a.position - b.position))

// ==================== МЕТОДЫ ====================

// --- Утилиты ---

const getTasksByColumn = (columnId: number): Task[] => {
  return props.tasks.filter((t) => t.column_id === columnId).sort((a, b) => a.position - b.position)
}

const getSubtasksForTask = (taskId: number): Subtask[] => {
  return props.subtasks.filter((s) => s.parent_task_id === taskId).sort((a, b) => a.id - b.id)
}

const getTaskProgress = (task: Task): number => {
  if (!task.subtasks_count) return 0
  return Math.round((task.completed_subtasks_count / task.subtasks_count) * 100)
}

const columnColor = (position: number): string => {
  const colors = ['#168be5', '#ff9f43', '#2ecc71', '#9b59b6', '#e74c3c']
  return colors[position % colors.length] || '#cbd5e0'
}

const formatDate = (dateString: string | null): string => {
  if (!dateString) return ''
  return new Date(dateString).toLocaleDateString('ru-RU', { day: 'numeric', month: 'short' })
}

const getUserInitials = (user: TaskUser): string => {
  const name = user.name || user.login || ''
  const parts = name.split(' ')
  return parts.length >= 2
    ? `${parts[0][0]}${parts[1][0]}`.toUpperCase()
    : name.substring(0, 2).toUpperCase()
}

const getStatusName = (statusId: number | null): string => {
  if (!statusId) return 'Новая'
  const status = props.statuses.find((s) => s.id === statusId)
  return status ? status.name : 'Статус'
}

// --- UI взаимодействия ---

const toggleSubtasks = (taskId: number) => {
  if (expandedTaskIds.value.has(taskId)) {
    expandedTaskIds.value.delete(taskId)
  } else {
    expandedTaskIds.value.add(taskId)
  }
}

const isTaskExpanded = (taskId: number): boolean => expandedTaskIds.value.has(taskId)

// --- Колонки ---

const openColumnSettings = (column: Column) => {
  editingColumn.value = column
  editColumnName.value = column.name
  isEditColumnModalOpen.value = true
}

const closeColumnModal = () => {
  isCreateColumnOpen.value = false
  isEditColumnModalOpen.value = false
  editingColumn.value = null
  editColumnName.value = ''
}

const handleCreateColumn = () => {
  if (!editColumnName.value.trim()) return
  emit('create-column', editColumnName.value.trim())
  closeColumnModal()
}

const handleUpdateColumn = () => {
  if (!editingColumn.value) return
  emit('update-column', {
    id: editingColumn.value.id,
    name: editColumnName.value.trim(),
  })
  closeColumnModal()
}

const confirmDeleteColumn = (id?: number) => {
  if (!id) return
  if (confirm('Удалить колонку?')) {
    emit('delete-column', id)
    closeColumnModal()
  }
}

const moveColumn = (payload: { column: Column; direction: 'left' | 'right' }) => {
  const { column, direction } = payload
  const index = sortedColumns.value.findIndex((c) => c.id === column.id)
  if (index === -1) return
  const newIndex = direction === 'left' ? index - 1 : index + 1
  if (newIndex < 0 || newIndex >= sortedColumns.value.length) return
  const targetColumn = sortedColumns.value[newIndex]
  emit('update-column', { id: column.id, position: newIndex })
  emit('update-column', { id: targetColumn.id, position: index })
}

// --- Доска ---

const handleUpdateBoard = () => {
  emit('update-board', { name: editBoardName.value.trim() })
  isEditBoardOpen.value = false
}

// --- Задачи ---

const openCreateTask = (columnId: number) => {
  activeColumnId.value = columnId
  newTaskName.value = ''
  newTaskDescription.value = ''
  isCreateTaskOpen.value = true
}

const closeTaskModal = () => {
  isCreateTaskOpen.value = false
  isEditTaskModalOpen.value = false
  editingTask.value = null
}

const handleCreateTask = () => {
  if (!activeColumnId.value || !newTaskName.value.trim()) return
  emit('create-task', {
    columnId: activeColumnId.value,
    data: {
      name: newTaskName.value.trim(),
      description: newTaskDescription.value.trim() || '',
    },
  })
  closeTaskModal()
}

const openTaskSettings = (task: Task) => {
  editingTask.value = task
  editTaskName.value = task.name
  editTaskDescription.value = task.description || ''
  editTaskStatusId.value = task.status_id
  editTaskPlanStart.value = task.planing_date_time_start
    ? task.planing_date_time_start.slice(0, 16)
    : ''
  editTaskPlanEnd.value = task.planing_date_time_end ? task.planing_date_time_end.slice(0, 16) : ''
  isEditTaskModalOpen.value = true
}

const handleUpdateTask = () => {
  if (!editingTask.value) return
  emit('update-task', {
    id: editingTask.value.id,
    name: editTaskName.value.trim(),
    description: editTaskDescription.value.trim() || '',
    status_id: editTaskStatusId.value,
    planing_date_time_start: editTaskPlanStart.value || null,
    planing_date_time_end: editTaskPlanEnd.value || null,
  })
  closeTaskModal()
}

const confirmDeleteTask = (id?: number) => {
  if (!id) return
  if (confirm('Удалить задачу?')) {
    emit('delete-task', id)
    closeTaskModal()
  }
}

const deleteTask = (taskId: number) => {
  if (confirm('Удалить задачу?')) emit('delete-task', taskId)
}

const moveTaskToAnotherColumn = (task: Task) => {
  movingTask.value = task
  isMoveTaskOpen.value = true
}

const handleMoveTaskConfirm = (targetColumnId: number) => {
  if (!movingTask.value || movingTask.value.column_id === targetColumnId) {
    isMoveTaskOpen.value = false
    return
  }
  emit('update-task', {
    id: movingTask.value.id,
    column_id: targetColumnId,
  })
  isMoveTaskOpen.value = false
}

// --- Подзадачи ---

const openCreateSubtask = (taskId: number) => {
  activeTaskId.value = taskId
  newSubtaskName.value = ''
  newSubtaskDescription.value = ''
  isCreateSubtaskOpen.value = true
}

const closeSubtaskModal = () => {
  isCreateSubtaskOpen.value = false
  isEditSubtaskModalOpen.value = false
  editingSubtask.value = null
}

const handleCreateSubtask = () => {
  if (!activeTaskId.value || !newSubtaskName.value.trim()) return
  emit('create-subtask', {
    taskId: activeTaskId.value,
    data: {
      name: newSubtaskName.value.trim(),
      description: newSubtaskDescription.value.trim() || '',
    },
  })
  closeSubtaskModal()
}

const openSubtaskSettings = (subtask: Subtask) => {
  editingSubtask.value = subtask
  editSubtaskName.value = subtask.name
  editSubtaskDescription.value = subtask.description || ''
  editSubtaskStatusId.value = subtask.status_id
  isEditSubtaskModalOpen.value = true
}

const handleUpdateSubtask = () => {
  if (!editingSubtask.value) return
  emit('update-subtask', {
    id: editingSubtask.value.id,
    name: editSubtaskName.value.trim(),
    description: editSubtaskDescription.value.trim() || '',
    status_id: editSubtaskStatusId.value,
  })
  closeSubtaskModal()
}

const confirmDeleteSubtask = (id?: number) => {
  if (!id) return
  if (confirm('Удалить подзадачу?')) {
    emit('delete-subtask', id)
    closeSubtaskModal()
  }
}

const deleteSubtask = (subtaskId: number) => {
  if (confirm('Удалить подзадачу?')) emit('delete-subtask', subtaskId)
}

const toggleSubtaskComplete = (subtaskId: number) => {
  emit('subtask-complete', subtaskId)
}

watch(
  () => props.board,
  (newBoard) => {
    if (newBoard) editBoardName.value = newBoard.name
  },
  { immediate: true },
)
</script>

<style scoped>
/* ... (Ваши основные стили остаются без изменений, добавляем новые для форм) ... */

.kanban-board {
  display: flex;
  flex-direction: column;
  height: 100%;
  background-color: #f8f9fa;
}
.board-header {
  padding: 0.75rem 2rem;
  background: white;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-shrink: 0;
  height: 60px;
}
.board-header h2 {
  font-size: 1.25rem;
  margin: 0;
}
.columns-container {
  display: flex;
  gap: 1.5rem;
  overflow-x: auto;
  padding: 2rem;
  height: calc(100% - 60px);
  align-items: flex-start;
}
.spacer {
  min-width: 2rem;
}
.empty-state {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  color: #9ca3af;
}

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
.scroll-spacer {
  height: 100px;
  width: 100%;
}

.card {
  background: #ffffff;
  border: 1px solid #e8ecf1;
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 12px;
  transition: all 0.2s ease;
  cursor: default;
  position: relative;
}
.card:hover {
  border-color: #168be5;
  box-shadow: 0 4px 12px rgba(22, 139, 229, 0.1);
}
.card.is-active {
  border-left: 3px solid #168be5;
}
.card-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 10px;
}
.tag {
  font-size: 11px;
  font-weight: 600;
  padding: 4px 10px;
  border-radius: 20px;
  background: #e7f5ff;
  color: #168be5;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
.card-title {
  font-size: 15px;
  font-weight: 600;
  color: #2d3748;
  margin: 0 0 8px 0;
  line-height: 1.4;
}
.card-desc {
  font-size: 13px;
  color: #718096;
  margin-bottom: 12px;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.task-dates {
  display: flex;
  gap: 8px;
  margin-bottom: 8px;
  font-size: 11px;
  color: #64748b;
}
.date-small {
  display: flex;
  align-items: center;
  gap: 4px;
}

.progress-section {
  margin-bottom: 12px;
}
.progress-info {
  display: flex;
  justify-content: space-between;
  font-size: 11px;
  color: #718096;
  margin-bottom: 4px;
}
.progress-bar {
  height: 6px;
  background: #edf2f7;
  border-radius: 3px;
  overflow: hidden;
}
.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #168be5, #2ecc71);
  border-radius: 3px;
  transition: width 0.3s ease;
}

.subtasks-preview {
  border-top: 1px solid #edf2f7;
  padding-top: 8px;
}
.subtasks-toggle {
  display: flex;
  align-items: center;
  gap: 6px;
  background: transparent;
  border: none;
  padding: 4px 0;
  cursor: pointer;
  font-size: 12px;
  font-weight: 500;
  color: #4a5568;
  width: 100%;
  text-align: left;
}
.subtasks-list {
  margin-top: 8px;
}
.subtask-item {
  margin-bottom: 4px;
}
.subtask-row {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 4px 8px;
  background: #f8fafc;
  border-radius: 6px;
  font-size: 13px;
}
.status-check {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 14px;
  padding: 0;
}
.is-done {
  text-decoration: line-through;
  color: #94a3b8;
}

.card-foot {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 12px;
  padding-top: 10px;
  border-top: 1px solid #edf2f7;
}
.meta {
  display: flex;
  align-items: center;
  gap: 10px;
}
.user-avatars {
  display: flex;
  align-items: center;
}
.mini-avatar {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 10px;
  font-weight: 600;
  border: 2px solid white;
  margin-right: -6px;
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

.slide-enter-active,
.slide-leave-active {
  transition: all 0.2s ease;
  overflow: hidden;
}
.slide-enter-from,
.slide-leave-to {
  opacity: 0;
  max-height: 0;
}
.slide-enter-to,
.slide-leave-from {
  opacity: 1;
  max-height: 500px;
}

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}
.modal {
  background: white;
  border-radius: 12px;
  padding: 24px;
  min-width: 400px;
  max-width: 500px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}
.modal-lg {
  max-width: 600px;
}
.modal h3 {
  margin: 0 0 16px 0;
  font-size: 18px;
  color: #2d3748;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-bottom: 16px;
}
.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.form-group.full {
  grid-column: span 2;
}
.form-group label {
  font-size: 12px;
  font-weight: 600;
  color: #64748b;
}

.modal input,
.modal textarea,
.modal select {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 14px;
  box-sizing: border-box;
  font-family: inherit;
}
.modal input:focus,
.modal textarea:focus,
.modal select:focus {
  outline: none;
  border-color: #168be5;
  box-shadow: 0 0 0 3px rgba(22, 139, 229, 0.1);
}
.modal textarea {
  min-height: 80px;
  resize: vertical;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  margin-top: 8px;
}
.modal-actions button {
  padding: 8px 16px;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
  background: white;
  color: #4a5568;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s;
}
.modal-actions button:hover {
  background: #f7fafc;
}
.modal-actions button.primary {
  background: #168be5;
  color: white;
  border-color: #168be5;
}
.modal-actions button.primary:hover {
  background: #1370b8;
}
.modal-actions button.danger {
  background: #fee2e2;
  color: #ef4444;
  border-color: #fecaca;
}
.modal-actions button.danger:hover {
  background: #fecaca;
  color: #dc2626;
}

.column-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 16px;
  max-height: 300px;
  overflow-y: auto;
}
.column-option {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}
.column-option:hover {
  background-color: #f7fafc;
  border-color: #168be5;
}
.column-option.is-current {
  background-color: #f0f9ff;
  border-color: #bae6fd;
  cursor: default;
}
</style>
