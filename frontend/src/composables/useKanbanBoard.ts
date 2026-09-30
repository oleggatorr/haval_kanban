// src/composables/useKanbanBoard.ts
import { computed, ref, watch, onMounted, type Ref } from 'vue'
import { useApi } from '@/composables/useApi'
import type { Board, Column, Task, Subtask, FullBoardResponse } from '@/types/taskboard'

export function useKanbanBoard(projectId: number | string | Ref<number | string>) {
  // Инициализируем API для загрузки всей доски
  const api = useApi<FullBoardResponse>()

  // Нормализуем projectId
  const getProjectId = () => {
    return typeof projectId === 'object' && 'value' in projectId ? projectId.value : projectId
  }

  const board = ref<Board | null>(null)
  const columns = ref<Column[]>([])
  const tasks = ref<Task[]>([])
  const subtasks = ref<Subtask[]>([])

  const projectName = computed(() => board.value?.name ?? '')

  async function fetchBoard() {
    const currentId = getProjectId()
    if (!currentId || Number.isNaN(Number(currentId))) {
      console.warn('[useKanbanBoard] fetchBoard пропущен: некорректный projectId', currentId)
      return
    }

    try {
      // Эндпоинт остался прежним, так как он работал
      const path = `/project/${currentId}/full-board/`
      const data = await api.get(path)

      if (data) {
        board.value = data.board ?? null
        columns.value = data.columns ?? []
        tasks.value = data.tasks ?? []
        subtasks.value = data.subtasks ?? []
      }
    } catch (e) {
      console.error('[useKanbanBoard] Ошибка загрузки доски:', e)
      board.value = null
      columns.value = []
      tasks.value = []
      subtasks.value = []
    }
  }

  // --- Мутации (Исправлены URL согласно документации API) ---

  async function createColumn(payload: { name: string; description?: string | null }) {
    if (!board.value?.id) throw new Error('Board not loaded')

    const mutationApi = useApi<Column>()
    // Исправлен путь на /task_columns/ и добавлен board_id в тело запроса
    const created = await mutationApi.post(`/task_columns/`, {
      name: payload.name,
      description: payload.description ?? '',
      position: columns.value.length,
      flags: [],
      board_id: board.value.id,
    })

    if (created) columns.value.push(created)
    return created
  }

  async function deleteColumn(columnId: number) {
    const mutationApi = useApi()
    // Предположительно удаление тоже идет через task_columns/{id}
    await mutationApi.del(`/task_columns/${columnId}/`)
    columns.value = columns.value.filter((c) => c.id !== columnId)
    tasks.value = tasks.value.filter((t) => t.column_id !== columnId)
  }

  async function createTask(columnId: number, payload: Partial<Task>) {
    const mutationApi = useApi<Task>()
    // Исправлен путь на /task/
    const created = await mutationApi.post(`/task/`, {
      name: payload.name ?? 'Новая задача',
      description: payload.description ?? '',
      position: getTasksByColumn(columnId).length,
      status_id: payload.status_id ?? null,
      column_id: columnId, // Обязательно указываем колонку
      users: [],
      ...payload,
    })

    if (created) tasks.value.push(created)
    return created
  }

  async function deleteTask(taskId: number) {
    const mutationApi = useApi()
    // Предположительно /task/{id}/
    await mutationApi.del(`/task/${taskId}/`)
    tasks.value = tasks.value.filter((t) => t.id !== taskId)
    subtasks.value = subtasks.value.filter((s) => s.parent_task_id !== taskId)
  }

  async function updateTaskStatus(taskId: number, statusId: number | null) {
    const mutationApi = useApi<Task>()
    const updated = await mutationApi.patch(`/task/${taskId}/`, { status_id: statusId })
    if (updated) {
      tasks.value = tasks.value.map((t) => (t.id === taskId ? updated : t))
    }
    return updated
  }

  async function createSubtask(parentTaskId: number, payload: Partial<Subtask>) {
    const mutationApi = useApi<Subtask>()
    // Исправлен путь на /subtasks/
    const created = await mutationApi.post(`/subtasks/`, {
      name: payload.name ?? 'Новая подзадача',
      description: payload.description ?? '',
      status_id: payload.status_id ?? null,
      parent_task_id: parentTaskId,
      users: [],
      ...payload,
    })

    if (created) {
      subtasks.value.push(created)
      tasks.value = tasks.value.map((t) =>
        t.id === parentTaskId ? { ...t, subtasks_count: (t.subtasks_count ?? 0) + 1 } : t,
      )
    }
    return created
  }

  async function deleteSubtask(subtaskId: number) {
    const subtask = subtasks.value.find((s) => s.id === subtaskId)
    const mutationApi = useApi()
    await mutationApi.del(`/subtasks/${subtaskId}/`)

    subtasks.value = subtasks.value.filter((s) => s.id !== subtaskId)
    if (subtask) {
      tasks.value = tasks.value.map((t) =>
        t.id === subtask.parent_task_id
          ? { ...t, subtasks_count: Math.max(0, (t.subtasks_count ?? 1) - 1) }
          : t,
      )
    }
  }

  async function toggleSubtaskStatus(subtaskId: number, isCompleted: boolean) {
    const mutationApi = useApi<Subtask>()
    // Используем patch /subtasks/{id}/
    const updated = await mutationApi.patch(`/subtasks/${subtaskId}/`, {
      status_id: isCompleted ? 3 : 1, // Убедись, что ID статусов верные
      date_time_end: isCompleted ? new Date().toISOString() : null,
    })

    if (updated) {
      subtasks.value = subtasks.value.map((s) => (s.id === subtaskId ? updated : s))

      const parentId = updated.parent_task_id
      const completed = subtasks.value.filter(
        (s) => s.parent_task_id === parentId && s.date_time_end !== null,
      ).length

      tasks.value = tasks.value.map((t) =>
        t.id === parentId ? { ...t, completed_subtasks_count: completed } : t,
      )
    }
    return updated
  }

  // --- Утилиты ---
  function getSubtasksByTask(taskId: number): Subtask[] {
    return subtasks.value.filter((s) => s.parent_task_id === taskId)
  }

  function getTasksByColumn(columnId: number): Task[] {
    return tasks.value.filter((t) => t.column_id === columnId)
  }

  // --- Жизненный цикл ---
  onMounted(() => {
    fetchBoard()
  })

  if (typeof projectId === 'object' && 'value' in projectId) {
    watch(projectId, (newId, oldId) => {
      if (newId !== oldId) fetchBoard()
    })
  }

  return {
    loading: api.loading,
    error: api.error,
    projectName,
    board,
    columns,
    tasks,
    subtasks,
    fetchBoard,
    getTasksByColumn,
    getSubtasksByTask,
    createColumn,
    deleteColumn,
    createTask,
    deleteTask,
    updateTaskStatus,
    createSubtask,
    deleteSubtask,
    toggleSubtaskStatus,
  }
}
