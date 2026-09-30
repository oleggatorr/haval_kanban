<!-- src\views\test2\task_board_components\SubtaskItem.vue -->
<template>
  <div class="subtask-container" :class="{ 'is-expanded': isExpanded }">
    <!-- Основная карточка подзадачи -->
    <div class="subtask" :class="{ 'is-active': subtask.is_active }" @click="toggleExpand">
      <div class="subtask-header">
        <div class="subtask-title-wrap">
          <!-- Стрелочка для индикации раскрытия -->
          <span v-if="hasChildren" class="expand-icon">
            {{ isExpanded ? '▼' : '▶' }}
          </span>

          <button
            class="status-toggle"
            @click.stop="toggleComplete"
            :title="isCompleted ? 'Отметить как невыполненную' : 'Отметить как выполненную'"
          >
            <span class="status-icon" :class="{ completed: isCompleted }">
              {{ isCompleted ? '✅' : '⭕' }}
            </span>
          </button>

          <span class="subtask-name" :class="{ completed: isCompleted }">
            {{ subtask.name }}
          </span>
        </div>

        <div class="subtask-actions">
          <DropdownMenu align="right">
            <!-- Добавил console.log для проверки клика -->
            <div class="menu-item" @click.stop="openEditModal">✏️ Редактировать</div>
            <div class="menu-item" @click.stop="$emit('add-task', column?.id)">⬆️ Сдвинуть</div>
            <div class="menu-item" @click.stop="$emit('add-task', column?.id)">⬇️ Сдвинуть</div>
          </DropdownMenu>
        </div>
      </div>

      <!-- Описание -->
      <div v-if="subtask.description" class="subtask-description">
        {{ subtask.description }}
      </div>

      <!-- Мета-информация -->
      <div class="subtask-meta">
        <div v-if="hasPlanningDates" class="meta-item planning">
          <span class="icon">📅</span>
          <span>{{
            formatDateRange(subtask.planing_date_time_start, subtask.planing_date_time_end)
          }}</span>
        </div>
        <div v-if="hasActualDates" class="meta-item actual">
          <span class="icon">🕐</span>
          <span>{{ formatDateRange(subtask.date_time_start, subtask.date_time_end) }}</span>
        </div>
        <div class="meta-item users">
          <div class="user-avatars">
            <span
              v-for="user in subtask.users.slice(0, 3)"
              :key="user.id"
              class="mini-avatar"
              :title="user.name"
            >
              {{ getUserInitials(user.name) }}
            </span>
          </div>
        </div>
        <div v-if="showPosition" class="meta-item position">
          <span class="icon">↕️</span>
          <span>#{{ subtask.position }}</span>
        </div>
      </div>

      <div v-if="subtask.status_id" class="status-badge">
        <span class="dot" :style="{ background: getStatusColor() }"></span>
        <span>{{ getStatusName() }}</span>
      </div>
    </div>

    <!-- ВЛОЖЕННЫЕ ПОДЗАДАЧИ -->
    <div v-if="hasChildren && isExpanded" class="nested-subtasks">
      <SubtaskItem
        v-for="child in children"
        :key="child.id"
        :subtask="child"
        :show-position="showPosition"
        :column="column"
        @complete="$emit('complete', $event)"
        @edit="$emit('edit', $event)"
        @add-task="$emit('add-task', $event)"
      />
    </div>

    <!-- Модальное окно редактирования -->
    <EditSubtaskModal v-model="isEditModalOpen" :subtask="subtask" @save="handleSubtaskUpdate" />
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import DropdownMenu from '@/components/ui/DropdownMenu.vue'
// Проверьте путь! Если файл лежит в той же папке, то './EditSubtaskModal.vue'
import EditSubtaskModal from './edit_forms/EditSubtaskModal.vue'
import SubtaskItem from './SubtaskItem.vue' // Рекурсивный импорт

interface User {
  id: number
  name: string
}

interface Subtask {
  id: number
  name: string
  description: string | null
  position: number
  date_time_start: string | null
  date_time_end: string | null
  planing_date_time_start: string | null
  planing_date_time_end: string | null
  parent_task_id: number
  status_id: number | null
  create_at: string
  update_at: string | null
  is_active: boolean
  users: User[]
  children?: Subtask[]
}

const props = defineProps<{
  subtask: Subtask
  showPosition?: boolean
  column?: any
}>()

const emit = defineEmits<{
  (e: 'complete', subtaskId: number): void
  (e: 'edit', subtask: Subtask): void
  (e: 'status-change', subtask: Subtask): void
  (e: 'delete', subtask: Subtask): void
  (e: 'assign-user', subtask: Subtask): void
  (e: 'add-task', columnId: number): void
}>()

const isEditModalOpen = ref(false)
const isExpanded = ref(false)

// Функция-обертка для отладки
const openEditModal = () => {
  console.log('Открытие модалки для:', props.subtask.name)
  isEditModalOpen.value = true
}

const hasChildren = computed(() => {
  return props.subtask.children && props.subtask.children.length > 0
})

const children = computed(() => props.subtask.children || [])

const handleSubtaskUpdate = (updatedData: any) => {
  console.log('Тестовое сохранение:', updatedData)
  // Здесь пока ничего не делаем, просто закрываем окно (это делает сама модалка)
  emit('edit', { ...props.subtask, ...updatedData })
}

const toggleExpand = () => {
  if (hasChildren.value) {
    isExpanded.value = !isExpanded.value
  }
}

const isCompleted = computed(() => !!props.subtask.date_time_end)
const hasPlanningDates = computed(
  () => !!(props.subtask.planing_date_time_start || props.subtask.planing_date_time_end),
)
const hasActualDates = computed(
  () => !!(props.subtask.date_time_start || props.subtask.date_time_end),
)

const toggleComplete = () => emit('complete', props.subtask.id)

const formatDate = (dateString: string | null): string => {
  if (!dateString) return ''
  return new Date(dateString).toLocaleDateString('ru-RU', { day: 'numeric', month: 'short' })
}

const formatDateRange = (start: string | null, end: string | null): string => {
  if (!start && !end) return ''
  if (start && end) return `${formatDate(start)} - ${formatDate(end)}`
  return formatDate(start || end || '')
}

const getUserInitials = (name: string): string => {
  const parts = name.split(' ')
  if (parts.length >= 2) return `${parts[0][0]}${parts[1][0]}`.toUpperCase()
  return name.substring(0, 2).toUpperCase()
}

const getStatusColor = (): string => {
  const colors: Record<number, string> = { 1: '#168be5', 2: '#ff9f43', 3: '#2ecc71' }
  return colors[props.subtask.status_id!] || '#95a5a6'
}

const getStatusName = (): string => {
  const names: Record<number, string> = { 1: 'В работе', 2: 'На проверке', 3: 'Завершено' }
  return names[props.subtask.status_id!] || 'Статус'
}
</script>

<style scoped>
/* Стили остались без изменений */
.subtask-container {
  margin-bottom: 8px;
}
.subtask {
  background: #ffffff;
  border: 1px solid #e8ecf1;
  border-radius: 8px;
  padding: 12px;
  transition: all 0.2s ease;
  cursor: pointer;
}
.subtask:hover {
  border-color: #168be5;
  box-shadow: 0 2px 8px rgba(22, 139, 229, 0.1);
}
.subtask.is-active {
  border-left: 3px solid #168be5;
}
.nested-subtasks {
  margin-left: 20px;
  margin-top: 8px;
  border-left: 2px solid #e2e8f0;
  padding-left: 10px;
}
.expand-icon {
  font-size: 10px;
  color: #a0aec0;
  width: 16px;
  display: inline-block;
  text-align: center;
  margin-right: 4px;
}
.subtask-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 8px;
}
.subtask-title-wrap {
  display: flex;
  align-items: center;
  gap: 4px;
  flex: 1;
}
.status-toggle {
  background: transparent;
  border: none;
  padding: 0;
  cursor: pointer;
  display: flex;
  align-items: center;
  font-size: 18px;
  line-height: 1;
}
.subtask-name {
  font-size: 14px;
  font-weight: 500;
  color: #2d3748;
}
.subtask-name.completed {
  text-decoration: line-through;
  color: #a0aec0;
}
.menu-item {
  padding: 8px 16px;
  font-size: 13px;
  cursor: pointer;
  color: #4a5568;
}
.menu-item:hover {
  background: #f7fafc;
  color: #168be5;
}
.subtask-description {
  font-size: 13px;
  color: #718096;
  margin-bottom: 8px;
  line-height: 1.5;
}
.subtask-meta {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
  font-size: 12px;
}
.meta-item {
  display: flex;
  align-items: center;
  gap: 4px;
  color: #718096;
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
.status-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  margin-top: 8px;
  padding: 4px 8px;
  background: #f7fafc;
  border-radius: 12px;
  font-size: 11px;
  color: #4a5568;
}
.dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
}
</style>
