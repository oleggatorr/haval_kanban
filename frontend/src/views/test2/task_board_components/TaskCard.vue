<template>
  <article class="card" :class="{ 'is-active': task.is_active }">
    <!-- Верхняя часть карточки -->
    <div class="card-top">
      <span class="tag">{{ getTagName() }}</span>

      <DropdownMenu align="right">
        <div class="menu-item" @click.stop="isEditModalOpen = true">✏️ Редактировать</div>

        <div class="menu-item" @click="$emit('move-task', task)">Переместить задачу</div>

        <!-- ИЗМЕНЕНО: Открываем модалку создания подзадачи -->
        <div class="menu-item" @click.stop="isCreateSubtaskOpen = true">Добавить подзадачу</div>

        <div class="menu-item" @click="$emit('move-task', { task, direction: 'up' })">
          ⬆️ Сдвинуть
        </div>
        <div class="menu-item" @click="$emit('move-task', { task, direction: 'down' })">
          ⬇️ Сдвинуть
        </div>
      </DropdownMenu>
    </div>

    <!-- Заголовок и описание -->
    <h3 class="card-title">{{ task.name }}</h3>
    <div v-if="task.description" class="card-desc">{{ task.description }}</div>

    <!-- Прогресс выполнения подзадач -->
    <div v-if="subtasks.length > 0" class="progress-section">
      <div class="progress-info">
        <span>{{ completedSubtasks }}/{{ subtasks.length }} подзадач</span>
        <span>{{ progressPercent }}%</span>
      </div>
      <div class="progress-bar">
        <div class="progress-fill" :style="{ width: progressPercent + '%' }"></div>
      </div>
    </div>

    <!-- Список подзадач -->
    <div v-if="subtasks.length > 0" class="subtasks-section">
      <button class="subtasks-toggle" @click.stop="toggleSubtasks">
        <span class="toggle-icon">{{ showSubtasks ? '▼' : '▶' }}</span>
        <span>Подзадачи ({{ subtasks.length }})</span>
      </button>

      <Transition name="slide">
        <div v-show="showSubtasks" class="subtasks-list">
          <SubtaskItem
            v-for="subtask in sortedSubtasks"
            :key="subtask.id"
            :subtask="subtask"
            :show-position="true"
            :column="column"
            @complete="(id) => $emit('subtask-complete', id)"
            @edit="(s) => $emit('subtask-edit', s)"
            @add-task="(colId) => $emit('add-task', colId)"
          />
        </div>
      </Transition>
    </div>

    <!-- Футер карточки -->
    <div class="card-foot">
      <div class="meta">
        <div v-if="task.users && task.users.length > 0" class="user-avatars">
          <span
            v-for="user in task.users.slice(0, 3)"
            :key="user.id"
            class="mini-avatar"
            :title="getUserName(user)"
          >
            {{ getUserInitials(user) }}
          </span>
          <span v-if="task.users.length > 3" class="more-users">
            +{{ task.users.length - 3 }}
          </span>
        </div>
        <span v-if="hasDates" class="date-info">
          📅 {{ formatDate(task.planing_date_time_end || task.date_time_end) }}
        </span>
      </div>

      <span v-if="task.status_id" class="priority" :class="getPriorityClass()">
        {{ getStatusName() }}
      </span>
    </div>

    <!-- Модальное окно редактирования ЗАДАЧИ -->
    <EditTaskModal v-model="isEditModalOpen" :task="task" @save="handleTaskUpdate" />

    <!-- Модальное окно создания подзадачи -->
    <CreateSubtaskModal v-model="isCreateSubtaskOpen" @save="handleCreateSubtask" />
  </article>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import SubtaskItem from './SubtaskItem.vue'
import DropdownMenu from '@/components/ui/DropdownMenu.vue'
import EditTaskModal from './edit_forms/EditTaskModal.vue'
import CreateSubtaskModal from './create_forms/CreateSubtaskModal.vue' // Импорт нового компонента

interface User {
  id: number
  name?: string
  login?: string
  initials?: string
}

interface Subtask {
  id: number
  parent_task_id: number
  date_time_end: string | null
  position: number
  name: string
  description: string | null
  date_time_start: string | null
  planing_date_time_start: string | null
  planing_date_time_end: string | null
  status_id: number | null
  create_at: string
  update_at: string | null
  is_active: boolean
  users: User[]
}

interface Task {
  id: number
  name: string
  description: string | null
  position: number
  date_time_start: string | null
  date_time_end: string | null
  planing_date_time_start: string | null
  planing_date_time_end: string | null
  column_id: number
  status_id: number | null
  create_at: string
  update_at: string | null
  is_active: boolean
  data: any
  users: User[]
}

const props = defineProps<{
  task: Task
  subtasks?: Subtask[]
  column?: any
}>()

const emit = defineEmits<{
  (e: 'menu', task: Task): void
  (e: 'add-subtask', taskId: number): void
  (e: 'subtask-complete', subtaskId: number): void
  (e: 'subtask-edit', subtask: Subtask): void
  (e: 'edit', task: Task): void
  (e: 'move-task', payload: any): void
  (e: 'add-task', columnId: number): void
  // Новое событие для создания подзадачи с данными
  (e: 'create-subtask-with-data', payload: { taskId: number; data: any }): void
}>()

const showSubtasks = ref(false)
const isEditModalOpen = ref(false)
const isCreateSubtaskOpen = ref(false) // Состояние для модалки создания подзадачи

const subtasks = computed(() => props.subtasks || [])
const sortedSubtasks = computed(() => [...subtasks.value].sort((a, b) => a.position - b.position))
const completedSubtasks = computed(() => subtasks.value.filter((s) => !!s.date_time_end).length)
const progressPercent = computed(() =>
  subtasks.value.length ? Math.round((completedSubtasks.value / subtasks.value.length) * 100) : 0,
)
const hasDates = computed(() => !!(props.task.planing_date_time_end || props.task.date_time_end))

const toggleSubtasks = () => {
  showSubtasks.value = !showSubtasks.value
}

const handleTaskUpdate = (updatedData: any) => {
  console.log('Обновление задачи:', updatedData)
  emit('edit', { ...props.task, ...updatedData })
}

const handleCreateSubtask = (data: any) => {
  console.log('Создание подзадачи:', data)
  emit('create-subtask-with-data', {
    taskId: props.task.id,
    data,
  })
}

const getTagName = (): string => {
  const tags: Record<number, string> = {
    1: 'Задача',
    2: 'В работе',
    3: 'Тестирование',
    4: 'Готово',
  }
  return tags[props.task.column_id] || 'Задача'
}

const formatDate = (dateString: string | null): string => {
  if (!dateString) return ''
  return new Date(dateString).toLocaleDateString('ru-RU', { day: 'numeric', month: 'short' })
}

const getUserName = (user: User): string => user.name || user.login || 'Пользователь'

const getUserInitials = (user: User): string => {
  if (user.initials) return user.initials
  const name = user.name || user.login || ''
  const parts = name.split(' ')
  return parts.length >= 2
    ? `${parts[0][0]}${parts[1][0]}`.toUpperCase()
    : name.substring(0, 2).toUpperCase()
}

const getStatusName = (): string => {
  const names: Record<number, string> = {
    1: 'Новая',
    2: 'В работе',
    3: 'На проверке',
    4: 'Завершено',
  }
  return names[props.task.status_id!] || 'Статус'
}

const getPriorityClass = (): string => {
  const classes: Record<number, string> = { 1: 'low', 2: 'medium', 3: 'high', 4: 'completed' }
  return classes[props.task.status_id!] || ''
}
</script>

<style scoped>
/* Стили остаются без изменений */
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
.subtasks-section {
  margin-bottom: 12px;
  border-top: 1px solid #edf2f7;
  padding-top: 10px;
}
.subtasks-toggle {
  display: flex;
  align-items: center;
  gap: 6px;
  background: transparent;
  border: none;
  padding: 6px 0;
  cursor: pointer;
  font-size: 12px;
  font-weight: 500;
  color: #4a5568;
  transition: color 0.2s ease;
  width: 100%;
  text-align: left;
}
.subtasks-toggle:hover {
  color: #168be5;
}
.toggle-icon {
  font-size: 10px;
  transition: transform 0.2s ease;
}
.subtasks-list {
  margin-top: 8px;
  padding-left: 4px;
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
.more-users {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: #e8ecf1;
  color: #718096;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 9px;
  font-weight: 600;
  border: 2px solid white;
  margin-left: 4px;
}
.date-info {
  font-size: 12px;
  color: #718096;
}
.priority {
  font-size: 11px;
  font-weight: 600;
  padding: 4px 10px;
  border-radius: 20px;
}
.priority.low {
  background: #f0fff4;
  color: #2ecc71;
}
.priority.medium {
  background: #fffbeb;
  color: #f59e0b;
}
.priority.high {
  background: #fef2f2;
  color: #ef4444;
}
.priority.completed {
  background: #f0fdf4;
  color: #22c55e;
}
</style>
