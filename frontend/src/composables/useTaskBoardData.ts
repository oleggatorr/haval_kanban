// useKanbanData.ts
import { ref, computed } from 'vue'
import type { Board, Column, Task, Subtask } from '@/types/taskboard'

export function useKanbanData() {
  const currentBoard = ref<Board>({
    /* ... */
  })
  const columns = ref<Column[]>([
    /* ... */
  ])
  const tasks = ref<Task[]>([
    /* ... */
  ])
  const subtasks = ref<Subtask[]>([
    /* ... */
  ])

  // Получение задач для конкретной колонки
  const getTasksByColumn = (columnId: number) => {
    return computed(() => tasks.value.filter((task) => task.column_id === columnId))
  }

  // Получение подзадач для конкретной задачи
  const getSubtasksByTask = (taskId: number) => {
    return computed(() => subtasks.value.filter((subtask) => subtask.parent_task_id === taskId))
  }

  // Добавление новой колонки
  const addColumn = (name: string) => {
    const newCol: Column = {
      name,
      description: null,
      flags: [],
      position: columns.value.length,
      id: Date.now(),
      board_id: currentBoard.value.id,
      create_at: new Date().toISOString(),
      update_at: null,
      is_active: true,
      remove_at: null,
    }
    columns.value.push(newCol)
  }

  // Добавление задачи
  const addTask = (columnId: number, taskData: Partial<Task>) => {
    const newTask: Task = {
      name: taskData.name || 'Новая задача',
      description: taskData.description || null,
      position: getTasksByColumn(columnId).value.length,
      date_time_start: null,
      date_time_end: null,
      planing_date_time_start: null,
      planing_date_time_end: null,
      id: Date.now(),
      column_id: columnId,
      status_id: 1,
      create_at: new Date().toISOString(),
      update_at: null,
      is_active: true,
      data: null,
      users: [],
    }
    tasks.value.push(newTask)
  }

  // Добавление подзадачи
  const addSubtask = (parentTaskId: number, subtaskData: Partial<Subtask>) => {
    const newSubtask: Subtask = {
      name: subtaskData.name || 'Новая подзадача',
      description: subtaskData.description || null,
      position: getSubtasksByTask(parentTaskId).value.length,
      date_time_start: null,
      date_time_end: null,
      planing_date_time_start: null,
      planing_date_time_end: null,
      id: Date.now(),
      parent_task_id: parentTaskId,
      status_id: 1,
      create_at: new Date().toISOString(),
      update_at: null,
      is_active: true,
      users: [],
    }
    subtasks.value.push(newSubtask)
  }

  // Переключение статуса подзадачи
  const toggleSubtaskStatus = (subtaskId: number) => {
    const subtask = subtasks.value.find((s) => s.id === subtaskId)
    if (subtask) {
      if (subtask.date_time_end) {
        subtask.date_time_end = null
        subtask.status_id = 1
      } else {
        subtask.date_time_end = new Date().toISOString()
        subtask.status_id = 3
      }
    }
  }

  return {
    currentBoard,
    columns,
    tasks,
    subtasks,
    getTasksByColumn,
    getSubtasksByTask,
    addColumn,
    addTask,
    addSubtask,
    toggleSubtaskStatus,
  }
}
