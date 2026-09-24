// composables/useKanbanBoard.ts
import { computed, ref } from 'vue'
import { createApiService } from '@/lib/api/service'
import type { Board, Column, Task, Subtask, FullBoardResponse } from '@/types/taskboard'
import type { ApiError } from '@/lib/api/types'

const service = createApiService({ baseUrl: '' })

export function useKanbanBoard(projectId: number) {
  const loading = ref(false)
  const error = ref<string | null>(null)

  const board = ref<Board | null>(null)
  const columns = ref<Column[]>([])
  const tasks = ref<Task[]>([])
  const subtasks = ref<Subtask[]>([])

  const projectName = computed(() => board.value?.name ?? '')

  /** GET /project/{projectId}/full-board */
  async function fetchBoard() {
    loading.value = true
    error.value = null
    try {
      const data = await service.get<FullBoardResponse>(`/project/${projectId}/full-board`)
      board.value = data.board
      columns.value = data.columns ?? []
      tasks.value = data.tasks ?? []
      subtasks.value = data.subtasks ?? []
    } catch (e) {
      const err = e as ApiError
      error.value = err.message || 'Не удалось загрузить доску'
      board.value = null
      columns.value = []
      tasks.value = []
      subtasks.value = []
    } finally {
      loading.value = false
    }
  }

  // ——— Утилиты ———

  /** Подзадачи конкретной задачи */
  function getSubtasksByTask(taskId: number): Subtask[] {
    return subtasks.value.filter((s) => s.parent_task_id === taskId)
  }

  /** Задачи конкретной колонки */
  function getTasksByColumn(columnId: number): Task[] {
    return tasks.value.filter((t) => t.column_id === columnId)
  }

  // ——— Мутации (заглушки, подставьте свои эндпоинты) ———

  async function createColumn(payload: { name: string; description?: string | null }) {
    const created = await service.post<Column>(`/board/${board.value?.id}/columns`, {
      name: payload.name,
      description: payload.description ?? null,
      position: columns.value.length,
      flags: [],
    })
    columns.value.push(created)
    return created
  }

  async function deleteColumn(columnId: number) {
    await service.delete(`/columns/${columnId}`)
    columns.value = columns.value.filter((c) => c.id !== columnId)
    tasks.value = tasks.value.filter((t) => t.column_id !== columnId)
  }

  async function createTask(columnId: number, payload: Partial<Task>) {
    const created = await service.post<Task>(`/columns/${columnId}/tasks`, {
      name: payload.name ?? 'Новая задача',
      description: payload.description ?? null,
      position: getTasksByColumn(columnId).length,
      status_id: payload.status_id ?? null,
      ...payload,
    })
    tasks.value.push(created)
    return created
  }

  async function deleteTask(taskId: number) {
    await service.delete(`/tasks/${taskId}`)
    tasks.value = tasks.value.filter((t) => t.id !== taskId)
    subtasks.value = subtasks.value.filter((s) => s.parent_task_id !== taskId)
  }

  async function updateTaskStatus(taskId: number, statusId: number | null) {
    const updated = await service.patch<Task>(`/tasks/${taskId}`, {
      status_id: statusId,
    })
    tasks.value = tasks.value.map((t) => (t.id === taskId ? updated : t))
    return updated
  }

  async function createSubtask(parentTaskId: number, payload: Partial<Subtask>) {
    const created = await service.post<Subtask>(`/tasks/${parentTaskId}/subtasks`, {
      name: payload.name ?? 'Новая подзадача',
      description: payload.description ?? null,
      status_id: payload.status_id ?? null,
      ...payload,
    })
    subtasks.value.push(created)

    // обновим счётчики у родительской задачи
    tasks.value = tasks.value.map((t) =>
      t.id === parentTaskId ? { ...t, subtasks_count: t.subtasks_count + 1 } : t,
    )
    return created
  }

  async function deleteSubtask(subtaskId: number) {
    const subtask = subtasks.value.find((s) => s.id === subtaskId)
    await service.delete(`/subtasks/${subtaskId}`)
    subtasks.value = subtasks.value.filter((s) => s.id !== subtaskId)

    if (subtask) {
      tasks.value = tasks.value.map((t) =>
        t.id === subtask.parent_task_id
          ? { ...t, subtasks_count: Math.max(0, t.subtasks_count - 1) }
          : t,
      )
    }
  }

  /** Совместимо с шаблоном: (subtaskId, isCompleted) */
  async function toggleSubtaskStatus(subtaskId: number, isCompleted: boolean) {
    const updated = await service.patch<Subtask>(`/subtasks/${subtaskId}`, {
      status_id: isCompleted ? 3 : 1,
      date_time_end: isCompleted ? new Date().toISOString() : null,
    })
    subtasks.value = subtasks.value.map((s) => (s.id === subtaskId ? updated : s))

    // обновим completed_subtasks_count у родительской задачи
    const parentId = updated.parent_task_id
    const completed = subtasks.value.filter(
      (s) => s.parent_task_id === parentId && s.date_time_end !== null,
    ).length
    tasks.value = tasks.value.map((t) =>
      t.id === parentId ? { ...t, completed_subtasks_count: completed } : t,
    )
    return updated
  }

  return {
    // состояние
    loading,
    error,
    projectName,
    board,
    columns,
    tasks,
    subtasks,
    // методы
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
