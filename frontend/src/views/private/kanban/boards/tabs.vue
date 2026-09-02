<!-- src/views/KanbanView.vue -->
<template>
  <div class="kanban-wrapper">
    <!-- Шапка -->
    <header class="kanban-header">
      <h1>📋 Kanban Доска</h1>
      <div class="header-actions">
        <button class="add-board-btn" @click="addNewBoard">+ Новая доска</button>
      </div>
    </header>

    <!-- Вкладки -->
    <div class="tabs-container">
      <div class="tabs">
        <button
          v-for="board in boards"
          :key="board.id"
          class="tab"
          :class="{
            active: activeBoardId === board.id,
            'tab-new': board.isNew,
          }"
          @click="switchBoard(board.id)"
        >
          <span class="tab-icon">{{ board.icon }}</span>
          <span class="tab-name">{{ board.name }}</span>
          <span v-if="board.taskCount !== undefined" class="tab-count">
            {{ board.taskCount }}
          </span>
          <button v-if="boards.length > 1" class="tab-close" @click.stop="deleteBoard(board.id)">
            ✕
          </button>
        </button>

        <!-- Кнопка добавления вкладки -->
        <button class="tab-add" @click="addNewBoard">+</button>
      </div>
    </div>

    <!-- Контент - Kanban доска -->
    <div class="kanban-content">
      <KanbanBoard
        v-if="activeBoard"
        :key="activeBoard.id"
        :columns="activeBoard.columns"
        @update-columns="updateBoardColumns"
        @move-task="handleMoveTask"
      />

      <!-- Пустое состояние -->
      <div v-else class="empty-state">
        <div class="empty-icon">📭</div>
        <h2>Нет досок</h2>
        <p>Создайте новую доску для работы</p>
        <button @click="addNewBoard" class="create-board-btn">Создать доску</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import KanbanBoard from '@/components/layout/KanbanBoard.vue'
import type { Column, Task } from '@/types/kanban'

// Тип для доски
interface Board {
  id: string
  name: string
  icon: string
  columns: Column[]
  isNew?: boolean
  taskCount?: number
}

// Начальные колонки для доски
const createDefaultColumns = (): Column[] => [
  {
    id: 'todo',
    name: 'К выполнению',
    color: '#6366f1',
    tasks: [],
  },
  {
    id: 'in-progress',
    name: 'В работе',
    color: '#f59e0b',
    tasks: [],
  },
  {
    id: 'review',
    name: 'На ревью',
    color: '#8b5cf6',
    tasks: [],
  },
  {
    id: 'done',
    name: 'Готово',
    color: '#10b981',
    tasks: [],
  },
]

// Тестовые данные для демонстрации
const createDemoColumns = (): Column[] => [
  {
    id: 'todo',
    name: 'К выполнению',
    color: '#6366f1',
    tasks: [
      {
        id: '1',
        title: 'Разработать API для пользователей',
        description: 'Создать endpoints для CRUD операций',
        priority: 'high',
        tags: ['backend', 'api'],
      },
      {
        id: '2',
        title: 'Настроить Docker',
        priority: 'medium',
        tags: ['devops'],
      },
    ],
  },
  {
    id: 'in-progress',
    name: 'В работе',
    color: '#f59e0b',
    tasks: [
      {
        id: '3',
        title: 'Дизайн главной страницы',
        description: 'Создать макет в Figma',
        priority: 'high',
        tags: ['design', 'ui'],
      },
    ],
  },
  {
    id: 'review',
    name: 'На ревью',
    color: '#8b5cf6',
    tasks: [],
  },
  {
    id: 'done',
    name: 'Готово',
    color: '#10b981',
    tasks: [
      {
        id: '4',
        title: 'Настроить CI/CD',
        priority: 'low',
        tags: ['devops'],
      },
    ],
  },
]

// Состояние
const boards = ref<Board[]>([
  {
    id: 'board-1',
    name: 'Основная',
    icon: '📊',
    columns: createDemoColumns(),
  },
])

const activeBoardId = ref<string>('board-1')
let boardCounter = 1

// Вычисляемые свойства
const activeBoard = computed(() => {
  return boards.value.find((b) => b.id === activeBoardId.value)
})

// Методы
const switchBoard = (boardId: string) => {
  activeBoardId.value = boardId
  // Убираем флаг isNew
  const board = boards.value.find((b) => b.id === boardId)
  if (board) {
    board.isNew = false
  }
}

const addNewBoard = () => {
  boardCounter++
  const newBoard: Board = {
    id: `board-${boardCounter}`,
    name: `Доска ${boardCounter}`,
    icon: getRandomIcon(),
    columns: createDefaultColumns(),
    isNew: true,
    taskCount: 0,
  }
  boards.value.push(newBoard)
  activeBoardId.value = newBoard.id

  // Автоматически переименовываем новую доску
  setTimeout(() => {
    const board = boards.value.find((b) => b.id === newBoard.id)
    if (board) {
      board.isNew = false
    }
  }, 2000)
}

const deleteBoard = (boardId: string) => {
  if (boards.value.length <= 1) {
    alert('Нельзя удалить последнюю доску')
    return
  }

  if (confirm(`Удалить доску "${boards.value.find((b) => b.id === boardId)?.name}"?`)) {
    const index = boards.value.findIndex((b) => b.id === boardId)
    boards.value.splice(index, 1)

    if (activeBoardId.value === boardId) {
      activeBoardId.value = boards.value[0]?.id || ''
    }
  }
}

const updateBoardColumns = (columns: Column[]) => {
  const board = boards.value.find((b) => b.id === activeBoardId.value)
  if (board) {
    board.columns = columns
    // Обновляем количество задач
    board.taskCount = columns.reduce((sum, col) => sum + col.tasks.length, 0)
  }
}

const handleMoveTask = (taskId: string, targetColumnId: string) => {
  const board = boards.value.find((b) => b.id === activeBoardId.value)
  if (!board) return

  let taskToMove: Task | null = null
  let sourceColumnId: string | null = null

  // Находим задачу и исходную колонку
  for (const column of board.columns) {
    const taskIndex = column.tasks.findIndex((t) => t.id === taskId)
    if (taskIndex !== -1) {
      taskToMove = column.tasks[taskIndex]
      sourceColumnId = column.id
      // Удаляем задачу из исходной колонки
      column.tasks.splice(taskIndex, 1)
      break
    }
  }

  if (!taskToMove || !sourceColumnId) return

  // Добавляем задачу в целевую колонку
  const targetColumn = board.columns.find((col) => col.id === targetColumnId)
  if (targetColumn) {
    targetColumn.tasks.push(taskToMove)
  }

  // Обновляем количество задач
  board.taskCount = board.columns.reduce((sum, col) => sum + col.tasks.length, 0)
}

const getRandomIcon = () => {
  const icons = ['🚀', '💡', '🎯', '⚡', '🌟', '🎨', '🔧', '📱', '💻', '🎮']
  return icons[Math.floor(Math.random() * icons.length)]
}

// Функция для получения количества задач в доске
const getBoardTaskCount = (board: Board): number => {
  return board.columns.reduce((sum, col) => sum + col.tasks.length, 0)
}
</script>

<style scoped>
.kanban-wrapper {
  min-height: 100vh;
  background: #f0f2f5;
  display: flex;
  flex-direction: column;
}

/* Шапка */
.kanban-header {
  background: white;
  padding: 16px 32px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  flex-shrink: 0;
}

.kanban-header h1 {
  margin: 0;
  font-size: 24px;
  color: #1a1a2e;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.add-board-btn {
  padding: 8px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition:
    transform 0.2s,
    box-shadow 0.2s;
}

.add-board-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

/* Вкладки */
.tabs-container {
  background: white;
  border-bottom: 1px solid #e8ecf1;
  flex-shrink: 0;
  overflow-x: auto;
}

.tabs {
  display: flex;
  align-items: center;
  padding: 0 32px;
  gap: 4px;
  min-height: 48px;
}

.tab {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  background: transparent;
  border: none;
  border-bottom: 3px solid transparent;
  cursor: pointer;
  font-size: 14px;
  color: #6b7280;
  transition: all 0.2s;
  white-space: nowrap;
  position: relative;
}

.tab:hover {
  color: #1a1a2e;
  background: #f3f4f6;
  border-radius: 6px 6px 0 0;
}

.tab.active {
  color: #667eea;
  border-bottom-color: #667eea;
  font-weight: 500;
}

.tab.active .tab-icon {
  color: #667eea;
}

.tab-icon {
  font-size: 16px;
}

.tab-name {
  max-width: 120px;
  overflow: hidden;
  text-overflow: ellipsis;
}

.tab-count {
  background: #e8ecf1;
  color: #6b7280;
  font-size: 11px;
  padding: 1px 8px;
  border-radius: 12px;
  font-weight: 500;
}

.tab.active .tab-count {
  background: #e0e7ff;
  color: #667eea;
}

.tab-close {
  background: transparent;
  border: none;
  color: #9ca3af;
  cursor: pointer;
  font-size: 14px;
  padding: 0 4px;
  border-radius: 4px;
  transition: all 0.2s;
}

.tab-close:hover {
  color: #ef4444;
  background: #fee2e2;
}

.tab-add {
  padding: 8px 12px;
  background: transparent;
  border: 2px dashed #d1d5db;
  border-radius: 6px;
  cursor: pointer;
  font-size: 18px;
  color: #9ca3af;
  transition: all 0.2s;
  margin-left: 8px;
}

.tab-add:hover {
  border-color: #667eea;
  color: #667eea;
  background: #f3f4f6;
}

/* Анимация для новых вкладок */
.tab-new {
  animation: tabPulse 1s ease;
}

@keyframes tabPulse {
  0% {
    background: rgba(102, 126, 234, 0.2);
  }
  50% {
    background: rgba(102, 126, 234, 0.1);
  }
  100% {
    background: transparent;
  }
}

/* Контент */
.kanban-content {
  flex: 1;
  overflow: hidden;
  position: relative;
}

.kanban-content :deep(.kanban-board) {
  height: 100%;
  padding: 24px 32px;
  background: transparent;
  min-height: calc(100vh - 140px);
}

/* Пустое состояние */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  min-height: 400px;
  color: #6b7280;
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 16px;
}

.empty-state h2 {
  margin: 0 0 8px 0;
  color: #1a1a2e;
}

.empty-state p {
  margin: 0 0 24px 0;
  color: #9ca3af;
}

.create-board-btn {
  padding: 12px 32px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
  font-weight: 500;
  transition:
    transform 0.2s,
    box-shadow 0.2s;
}

.create-board-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(102, 126, 234, 0.4);
}

/* Адаптивность */
@media (max-width: 768px) {
  .kanban-header {
    padding: 12px 16px;
    flex-direction: column;
    gap: 12px;
  }

  .kanban-header h1 {
    font-size: 20px;
  }

  .tabs {
    padding: 0 16px;
  }

  .tab {
    padding: 8px 12px;
    font-size: 13px;
  }

  .tab-name {
    max-width: 80px;
  }

  .kanban-content :deep(.kanban-board) {
    padding: 16px;
  }
}
</style>
