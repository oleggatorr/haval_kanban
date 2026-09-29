// src/composables/useProjectBoard.ts
import { ref, computed, onMounted, watch, type Ref } from 'vue'
import { useApi } from '@/composables/useApi'
import type { Project, UserProfile, StatusItem } from './types/taskboardTypes'

export function useProjectBoard(projectId: number | string | Ref<number | string>) {
  // --- Состояние ---
  const project = ref<Project | null>(null)
  const members = ref<UserProfile[]>([])
  const statuses = ref<StatusItem[]>([])

  // --- API Клиенты ---
  // Для каждого ресурса свой экземпляр, чтобы не смешивать loading/error
  const projectApi = useApi<Project>()
  const membersApi = useApi<UserProfile[]>()
  const statusesApi = useApi<StatusItem[]>()

  // --- Вычисляемые свойства ---
  const projectName = computed(() => project.value?.name ?? '')

  // Проверяем загрузку хотя бы основных данных
  const isLoaded = computed(() => !!project.value)

  // Нормализация ID (работает и с числом, и с ref)
  const getProjectId = () =>
    typeof projectId === 'object' && 'value' in projectId ? projectId.value : projectId

  // --- Загрузка данных ---
  async function fetchProjectContext() {
    const currentId = getProjectId()
    if (!currentId) return

    try {
      // Параллельная загрузка: Проект + Участники + Статусы
      // Мы НЕ грузим здесь задачи и колонки, это дело useKanbanBoard
      const [projectData, membersData, statusesData] = await Promise.all([
        projectApi.get(`/projects/${currentId}/`),
        membersApi.get(`/projects/${currentId}/members/`),
        statusesApi.get(`/projects/${currentId}/statuses/`),
      ])

      if (projectData) project.value = projectData
      if (membersData) members.value = membersData
      if (statusesData) statuses.value = statusesData
    } catch (e) {
      console.error('[useProjectBoard] Ошибка загрузки контекста проекта:', e)
    }
  }

  // --- Мутации мета-данных ---
  async function updateProjectName(newName: string) {
    if (!project.value) return

    // Создаем временный инстанс для мутации, чтобы не сбивать основной loading
    const mutationApi = useApi<Project>()
    const updated = await mutationApi.patch(`/projects/${project.value.id}/`, { name: newName })

    if (updated) {
      project.value = updated
    }
  }

  async function addMember(userId: number) {
    if (!project.value) return

    const mutationApi = useApi<UserProfile>()
    // Предполагаем, что API возвращает объект добавленного пользователя
    const newMember = await mutationApi.post(`/projects/${project.value.id}/members/`, {
      user_id: userId,
    })

    if (newMember) {
      members.value.push(newMember)
    }
  }
  //   async function edit_board(params: type) {}

  //   async function add_column(params: type) {}

  //   async function edit_column(params: type) {}

  //   async function remove_column(params: type) {}

  //   async function reorder_column(params: type) {}

  //   async function add_task(params: type) {}

  //   async function edit_task(params: type) {}

  //   async function remove_task(params: type) {}

  //   async function reorder_task(params: type) {}

  //   async function move_task(params: type) {}

  //   async function add_subtask(params: type) {}

  //   async function edit_subtask(params: type) {}

  //   async function remove_subtask(params: type) {}

  //   async function reorder_subtask(params: type) {}

  //   async function change_status_subtask(params: type) {}

  // --- Жизненный цикл ---
  onMounted(fetchProjectContext)

  // Если projectId реактивный (ref), следим за его изменением
  if (typeof projectId === 'object' && 'value' in projectId) {
    watch(projectId, (newVal, oldVal) => {
      if (newVal !== oldVal) {
        // Очищаем данные перед загрузкой нового проекта
        project.value = null
        members.value = []
        statuses.value = []
        fetchProjectContext()
      }
    })
  }

  return {
    // Данные
    project,
    members,
    statuses,

    // Хелперы
    projectName,
    isLoaded,

    // Статусы запросов (объединяем все три источника)
    loading: computed(
      () => projectApi.loading.value || membersApi.loading.value || statusesApi.loading.value,
    ),
    error: computed(
      () => projectApi.error.value || membersApi.error.value || statusesApi.error.value,
    ),

    // Действия
    fetchProjectContext,
    updateProjectName,
    addMember,
  }
}
