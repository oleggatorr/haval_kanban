// src/composables/useKanbanBoard.ts
import { ref, computed, watch, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import { httpClient } from '@/services/api'

// --- Типы ---

interface Subtask {
  id: number
  tasks_id: number
  name: string
  order_id: number
}

interface Task {
  id: number
  name: string
  order_id: number
  is_complit: boolean
  column_id: number
  assignees: string[]
  subtasks: Subtask[]
}

interface Column {
  id: number
  name: string
  order_id: number
  is_start: boolean
  is_final: boolean
  is_active: boolean
  tab_id: number
  tasks?: Task[]
}

interface Tab {
  id: number
  name: string
  order_id: number
  project_id: number
  columns: Column[]
}

interface ProjectResponse {
  id: number
  name: string
  description: string
  updated_at: string
  tabs: Tab[]
}

// Интерфейс для ответа check_update
interface CheckUpdateResponse {
  id: number
  updated_at: string
}

// --- Payloads для создания ---

interface NewTabPayload {
  name: string
  order_id: number
  project_id: number
}

interface NewColumnPayload {
  name: string
  order_id: number
  tab_id: number
  is_start?: boolean
  is_final?: boolean
  is_active?: boolean
}

interface NewTaskPayload {
  name: string
  order_id: number
  column_id: number
  assignees?: string[]
}

interface NewSubtaskPayload {
  name: string
  order_id: number
  tasks_id: number
}

// --- Типы для ответов ---

interface ColumnResponse {
  id: number
  name: string
  order_id: number
  is_start: boolean
  is_final: boolean
  is_active: boolean
  tab_id: number
}

interface TaskResponse {
  id: number
  name: string
  order_id: number
  is_complit: boolean
  column_id: number
  assignees: string[]
  subtasks: Subtask[]
}

interface SubtaskResponse {
  id: number
  tasks_id: number
  name: string
  order_id: number
}

interface UseKanbanBoardReturn {
  loading: typeof loading
  error: typeof error
  projectName: typeof projectName
  tabs: typeof tabs
  activeTabId: typeof activeTabId
  activeTab: ReturnType<typeof activeTab>
  tabsWithCount: ReturnType<typeof tabsWithCount>
  fetchBoard: () => Promise<void>
  setActiveTab: (tabId: number) => void
  createTab: () => Promise<void>
  deleteTab: (tabId: number) => Promise<void>
  createColumn: (tabId: number, name?: string) => Promise<void>
  deleteColumn: (columnId: number) => Promise<void>
  createTask: (columnId: number, name?: string) => Promise<void>
  deleteTask: (taskId: number) => Promise<void>
  updateTaskStatus: (taskId: number, isComplit: boolean) => Promise<void>
  createSubtask: (taskId: number, name?: string) => Promise<void>
  deleteSubtask: (subtaskId: number) => Promise<void>
}

export function useKanbanBoard(): UseKanbanBoardReturn {
  const route = useRoute()

  // Состояния
  const loading = ref(true)
  const error = ref<string | null>(null)
  const projectName = ref<string>('')
  const tabs = ref<Tab[]>([])
  const activeTabId = ref<number | null>(null)

  // Храним последнюю известную дату обновления
  const lastUpdatedAt = ref<string | null>(null)

  // Переменная для интервала опроса
  let updateInterval: number | null = null

  // Вычисляемые свойства
  const activeTab = computed(() => {
    if (!activeTabId.value) return null
    return tabs.value.find((tab) => tab.id === activeTabId.value) || null
  })

  const tabsWithCount = computed(() => {
    return tabs.value.map((tab) => ({
      ...tab,
      taskCount: tab.columns.reduce((sum, col) => sum + (col.tasks?.length || 0), 0),
    }))
  })

  const getProjectId = (): number | null => {
    const id = route.params.project_id
    if (!id) return null
    const parsedId = Number(id)
    return isNaN(parsedId) ? null : parsedId
  }

  const sortData = (tabsData: Tab[]) => {
    const sortedTabs = tabsData.sort((a, b) => a.order_id - b.order_id)
    sortedTabs.forEach((tab) => {
      tab.columns = (tab.columns || []).sort((a, b) => a.order_id - b.order_id)
      tab.columns.forEach((column) => {
        column.tasks = (column.tasks || []).sort((a, b) => a.order_id - b.order_id)
        column.tasks?.forEach((task) => {
          task.subtasks = (task.subtasks || []).sort((a, b) => a.order_id - b.order_id)
        })
      })
    })
    return sortedTabs
  }

  // Вспомогательная функция для поиска колонки по ID
  const findColumnById = (columnId: number): { tab: Tab; column: Column } | null => {
    for (const tab of tabs.value) {
      const column = tab.columns.find((c) => c.id === columnId)
      if (column) {
        return { tab, column }
      }
    }
    return null
  }

  // Вспомогательная функция для поиска задачи по ID
  const findTaskById = (taskId: number): { tab: Tab; column: Column; task: Task } | null => {
    for (const tab of tabs.value) {
      for (const column of tab.columns) {
        const task = column.tasks?.find((t) => t.id === taskId)
        if (task) {
          return { tab, column, task }
        }
      }
    }
    return null
  }

  // Вспомогательная функция для поиска подзадачи по ID
  const findSubtaskById = (
    subtaskId: number,
  ): { tab: Tab; column: Column; task: Task; subtask: Subtask } | null => {
    for (const tab of tabs.value) {
      for (const column of tab.columns) {
        for (const task of column.tasks || []) {
          const subtask = task.subtasks.find((s) => s.id === subtaskId)
          if (subtask) {
            return { tab, column, task, subtask }
          }
        }
      }
    }
    return null
  }

  // Основная загрузка доски
  const fetchBoard = async () => {
    const projectId = getProjectId()
    if (!projectId) {
      error.value = 'Неверный ID проекта'
      loading.value = false
      return
    }

    // Не показываем лоадер при фоновом обновлении, если данные уже есть
    const isInitialLoad = tabs.value.length === 0
    if (isInitialLoad) {
      loading.value = true
    }
    error.value = null

    try {
      const url = `/project/${projectId}/deep`
      const response = await httpClient.get<ProjectResponse>(url)

      if (response) {
        projectName.value = response.name || 'Без названия'
        lastUpdatedAt.value = response.updated_at

        const rawTabs = response.tabs || []
        tabs.value = sortData(rawTabs)

        if (tabs.value.length > 0) {
          if (!activeTabId.value || !tabs.value.find((t) => t.id === activeTabId.value)) {
            activeTabId.value = tabs.value[0].id
          }
        } else {
          activeTabId.value = null
        }
      } else {
        throw new Error('Пустой ответ от сервера')
      }
    } catch (err) {
      console.error('Ошибка при загрузке канбан-доски:', err)
      if (isInitialLoad) {
        error.value = `Не удалось загрузить данные: ${err instanceof Error ? err.message : 'Неизвестная ошибка'}`
      }
    } finally {
      if (isInitialLoad) {
        loading.value = false
      }
    }
  }

  // Проверка обновлений
  const checkForUpdates = async () => {
    const projectId = getProjectId()
    if (!projectId) return

    try {
      const response = await httpClient.get<CheckUpdateResponse>(
        `/project/check_update/${projectId}`,
      )

      if (response && response.updated_at) {
        if (lastUpdatedAt.value !== response.updated_at) {
          console.log('🔄 Обнаружены изменения на сервере, обновляем доску...')
          await fetchBoard()
        }
      }
    } catch (err) {
      console.warn('Не удалось проверить обновления:', err)
    }
  }

  // Запуск и остановка поллинга
  const startPolling = () => {
    stopPolling()
    checkForUpdates()
    updateInterval = window.setInterval(checkForUpdates, 20000)
  }

  const stopPolling = () => {
    if (updateInterval) {
      clearInterval(updateInterval)
      updateInterval = null
    }
  }

  const setActiveTab = (tabId: number) => {
    activeTabId.value = tabId
  }

  // ========== CRUD для вкладок ==========

  const createTab = async () => {
    const projectId = getProjectId()
    if (!projectId) return

    const name = prompt('Введите название новой вкладки:')
    if (!name) return

    try {
      const maxOrder = tabs.value.length > 0 ? Math.max(...tabs.value.map((t) => t.order_id)) : -1

      const payload: NewTabPayload = {
        name,
        order_id: maxOrder + 1,
        project_id: projectId,
      }

      const response = await httpClient.post<Tab>('/tab/', payload)

      if (response) {
        tabs.value.push(response)
        tabs.value = sortData(tabs.value)
        activeTabId.value = response.id
      }
    } catch (err) {
      console.error('Ошибка при создании вкладки:', err)
      alert('Не удалось создать вкладку')
    }
  }

  const deleteTab = async (tabId: number) => {
    if (!confirm('Вы уверены, что хотите удалить эту вкладку? Все задачи внутри будут удалены.')) {
      return
    }

    try {
      await httpClient.delete(`/tab/${tabId}`)

      tabs.value = tabs.value.filter((t) => t.id !== tabId)

      if (activeTabId.value === tabId) {
        activeTabId.value = tabs.value.length > 0 ? tabs.value[0].id : null
      }
    } catch (err) {
      console.error('Ошибка при удалении вкладки:', err)
      alert('Не удалось удалить вкладку')
    }
  }

  // ========== CRUD для колонок ==========

  const createColumn = async (tabId: number, name?: string) => {
    const tab = tabs.value.find((t) => t.id === tabId)
    if (!tab) {
      alert('Вкладка не найдена')
      return
    }

    const columnName = name || prompt('Введите название колонки:')
    if (!columnName) return

    try {
      const maxOrder = tab.columns.length > 0 ? Math.max(...tab.columns.map((c) => c.order_id)) : -1

      const payload: NewColumnPayload = {
        name: columnName,
        order_id: maxOrder + 1,
        tab_id: tabId,
        is_active: true,
      }

      const response = await httpClient.post<ColumnResponse>('/column/', payload)

      if (response) {
        const newColumn: Column = {
          ...response,
          tasks: [],
        }
        tab.columns.push(newColumn)
        tab.columns = tab.columns.sort((a, b) => a.order_id - b.order_id)
      }
    } catch (err) {
      console.error('Ошибка при создании колонки:', err)
      alert('Не удалось создать колонку')
    }
  }

  const deleteColumn = async (columnId: number) => {
    if (!confirm('Вы уверены, что хотите удалить эту колонку? Все задачи внутри будут удалены.')) {
      return
    }

    try {
      await httpClient.delete(`/column/${columnId}`)

      // Удаляем колонку из всех вкладок
      for (const tab of tabs.value) {
        const index = tab.columns.findIndex((c) => c.id === columnId)
        if (index !== -1) {
          tab.columns.splice(index, 1)
          break
        }
      }
    } catch (err) {
      console.error('Ошибка при удалении колонки:', err)
      alert('Не удалось удалить колонку')
    }
  }

  // ========== CRUD для задач ==========

  const createTask = async (columnId: number, name?: string) => {
    const result = findColumnById(columnId)
    if (!result) {
      alert('Колонка не найдена')
      return
    }

    const taskName = name || prompt('Введите название задачи:')
    if (!taskName) return

    try {
      const maxOrder = result.column.tasks?.length
        ? Math.max(...result.column.tasks.map((t) => t.order_id))
        : -1

      const payload: NewTaskPayload = {
        name: taskName,
        order_id: maxOrder + 1,
        column_id: columnId,
        assignees: [],
      }

      const response = await httpClient.post<TaskResponse>('/task/', payload)

      if (response) {
        if (!result.column.tasks) {
          result.column.tasks = []
        }
        const newTask: Task = {
          ...response,
          subtasks: response.subtasks || [],
        }
        result.column.tasks.push(newTask)
        result.column.tasks = result.column.tasks.sort((a, b) => a.order_id - b.order_id)
      }
    } catch (err) {
      console.error('Ошибка при создании задачи:', err)
      alert('Не удалось создать задачу')
    }
  }

  const deleteTask = async (taskId: number) => {
    if (!confirm('Вы уверены, что хотите удалить эту задачу?')) {
      return
    }

    try {
      await httpClient.delete(`/task/${taskId}`)

      const result = findTaskById(taskId)
      if (result) {
        const taskIndex = result.column.tasks?.findIndex((t) => t.id === taskId) ?? -1
        if (taskIndex !== -1) {
          result.column.tasks?.splice(taskIndex, 1)
        }
      }
    } catch (err) {
      console.error('Ошибка при удалении задачи:', err)
      alert('Не удалось удалить задачу')
    }
  }

  const updateTaskStatus = async (taskId: number, isComplit: boolean) => {
    try {
      await httpClient.patch(`/task/${taskId}`, { is_complit: isComplit })

      const result = findTaskById(taskId)
      if (result) {
        result.task.is_complit = isComplit
      }
    } catch (err) {
      console.error('Ошибка при обновлении статуса задачи:', err)
      alert('Не удалось обновить статус задачи')
    }
  }

  // ========== CRUD для подзадач ==========

  const createSubtask = async (taskId: number, name?: string) => {
    const result = findTaskById(taskId)
    if (!result) {
      alert('Задача не найдена')
      return
    }

    const subtaskName = name || prompt('Введите название подзадачи:')
    if (!subtaskName) return

    try {
      const maxOrder =
        result.task.subtasks.length > 0
          ? Math.max(...result.task.subtasks.map((s) => s.order_id))
          : -1

      const payload: NewSubtaskPayload = {
        name: subtaskName,
        order_id: maxOrder + 1,
        tasks_id: taskId,
      }

      const response = await httpClient.post<SubtaskResponse>('/sub_task/', payload)

      if (response) {
        const newSubtask: Subtask = {
          id: response.id,
          tasks_id: response.tasks_id,
          name: response.name,
          order_id: response.order_id,
        }
        result.task.subtasks.push(newSubtask)
        result.task.subtasks = result.task.subtasks.sort((a, b) => a.order_id - b.order_id)
      }
    } catch (err) {
      console.error('Ошибка при создании подзадачи:', err)
      alert('Не удалось создать подзадачу')
    }
  }

  const deleteSubtask = async (subtaskId: number) => {
    if (!confirm('Вы уверены, что хотите удалить эту подзадачу?')) {
      return
    }

    try {
      await httpClient.delete(`/sub_task/${subtaskId}`)

      const result = findSubtaskById(subtaskId)
      if (result) {
        const subtaskIndex = result.task.subtasks.findIndex((s) => s.id === subtaskId)
        if (subtaskIndex !== -1) {
          result.task.subtasks.splice(subtaskIndex, 1)
        }
      }
    } catch (err) {
      console.error('Ошибка при удалении подзадачи:', err)
      alert('Не удалось удалить подзадачу')
    }
  }

  // Следим за изменением project_id в маршруте
  watch(
    () => route.params.project_id,
    (newId, oldId) => {
      if (newId !== oldId) {
        stopPolling()
        lastUpdatedAt.value = null
        fetchBoard()
        startPolling()
      }
    },
    { immediate: true },
  )

  // Очищаем интервал при уничтожении компонента
  onUnmounted(() => {
    stopPolling()
  })

  return {
    loading,
    error,
    projectName,
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
    updateTaskStatus,
    createSubtask,
    deleteSubtask,
  }
}
