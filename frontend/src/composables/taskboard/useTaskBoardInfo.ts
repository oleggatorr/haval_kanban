// src/composables/useProjectInfo.ts
import { ref, computed, onMounted, watch, type Ref } from 'vue'
import { useApi } from '@/composables/useApi'
import type { Project, UserProfile, StatusItem, StatusesResponse } from './types/taskboardTypes'

export function useProjectInfo(projectId: number | string | Ref<number | string>) {
  // --- Состояние ---
  const project = ref<Project | null>(null)
  const members = ref<UserProfile[]>([])
  const statuses = ref<StatusItem[]>([])

  // --- API Клиенты ---
  // Используем отдельные инстансы для каждого ресурса, чтобы изолировать их loading/error
  const projectApi = useApi<Project>()
  const membersApi = useApi<UserProfile[]>()
  const statusesApi = useApi<StatusesResponse>()

  // --- Вычисляемые свойства ---
  const projectName = computed(() => project.value?.name ?? '')
  const isLoaded = computed(() => !!project.value)

  // Нормализация ID (работает и с числом, и с ref)
  const getProjectId = () =>
    typeof projectId === 'object' && 'value' in projectId ? projectId.value : projectId

  // --- Загрузка данных ---
  async function fetchProjectInfo() {
    const currentId = getProjectId()
    if (!currentId) return

    try {
      // Параллельная загрузка всех метаданных проекта
      const [projectData, membersData, statusesData] = await Promise.all([
        projectApi.get(`/project/${currentId}/`),
        membersApi.get(`/project/${currentId}/members/`),
        statusesApi.get(`/task_status/`),
      ])

      if (projectData) project.value = projectData
      if (membersData) members.value = membersData

      // Статусы приходят в объекте { items: [], total: 0 }, берем массив
      if (statusesData) statuses.value = statusesData.items || []
    } catch (e) {
      console.error('[useProjectInfo] Ошибка загрузки информации о проекте:', e)
    }
  }

  // --- Мутации мета-данных ---
  async function updateProjectName(newName: string) {
    if (!project.value) return

    const mutationApi = useApi<Project>()
    const updated = await mutationApi.patch(`/projects/${project.value.id}/`, { name: newName })

    if (updated) {
      project.value = updated
    }
  }

  async function addMember(userId: number) {
    if (!project.value) return

    const mutationApi = useApi<UserProfile>()
    const newMember = await mutationApi.post(`/projects/${project.value.id}/members/`, {
      user_id: userId,
    })

    if (newMember) {
      members.value.push(newMember)
    }
  }

  // --- Жизненный цикл ---
  onMounted(fetchProjectInfo)

  // Если projectId реактивный (ref), следим за его изменением
  if (typeof projectId === 'object' && 'value' in projectId) {
    watch(projectId, (newVal, oldVal) => {
      if (newVal !== oldVal) {
        // Очищаем данные перед загрузкой нового проекта
        project.value = null
        members.value = []
        statuses.value = []
        fetchProjectInfo()
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
    fetchProjectInfo,
    updateProjectName,
    addMember,
  }
}
