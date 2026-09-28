<template>
  <div class="projects-page">
    <!-- HEADER -->
    <header class="page-header">
      <h1>Проекты</h1>
      <button class="btn-primary" @click="$emit('create-project')">
        <Icon icon="solar:add-circle-outline" />
        Создать проект
      </button>
    </header>

    <!-- LOADING STATE -->
    <div v-if="isLoading" class="loading-state">
      <Icon icon="solar:loader-outline" class="spinner" />
      <span>Загрузка проектов...</span>
    </div>

    <!-- ERROR STATE -->
    <div v-else-if="localError" class="error-state">
      <Icon icon="solar:danger-triangle-outline" class="error-icon" />
      <h3>Ошибка загрузки</h3>
      <p>{{ localError }}</p>
      <button class="btn-secondary" @click="fetchProjects">Попробовать снова</button>
    </div>

    <!-- EMPTY STATE -->
    <div v-else-if="!projects.length" class="empty-state">
      <Icon icon="solar:folder-open-outline" class="empty-icon" />
      <h3>Проектов пока нет</h3>
      <p>Создайте первый проект, чтобы начать работу.</p>
      <button class="btn-secondary" @click="$emit('create-project')">Создать проект</button>
    </div>

    <!-- PROJECTS LIST (VERTICAL) -->
    <div v-else class="projects-list">
      <div v-for="project in projects" :key="project.id" class="project-card">
        <div class="card-header">
          <div class="status-badge" :class="{ active: project.is_active }">
            {{ project.is_active ? 'Активен' : 'Архив' }}
          </div>
          <div class="card-actions">
            <button
              class="icon-btn-sm"
              title="Редактировать"
              @click.stop="$emit('edit-project', project)"
            >
              <Icon icon="solar:pen-outline" />
            </button>
            <button
              class="icon-btn-sm danger"
              title="Удалить"
              @click.stop="$emit('delete-project', project)"
            >
              <Icon icon="solar:trash-bin-trash-outline" />
            </button>
          </div>
        </div>

        <!-- Ссылка на доску проекта -->
        <router-link :to="`/test3/${project.id}`" class="card-body-link">
          <div class="card-body">
            <h3 class="project-title">{{ project.name }}</h3>
            <div class="project-id">ID: {{ project.id }}</div>

            <div class="project-meta">
              <div class="meta-row">
                <Icon icon="solar:calendar-outline" />
                <span>Создан: {{ formatDate(project.create_at) }}</span>
              </div>
              <div v-if="project.update_at" class="meta-row">
                <Icon icon="solar:refresh-outline" />
                <span>Обновлен: {{ formatDate(project.update_at) }}</span>
              </div>
            </div>

            <div v-if="project.data?.big_description" class="project-desc">
              {{ truncateText(project.data.big_description, 100) }}
            </div>

            <div class="card-footer">
              <span class="more-link">Открыть доску &rarr;</span>
            </div>
          </div>
        </router-link>
      </div>
    </div>

    <!-- PAGINATION INFO -->
    <div v-if="total > 0 && !isLoading" class="pagination-info">
      Показано {{ projects.length }} из {{ total }} проектов
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Icon } from '@iconify/vue'
import { useApi } from '@/composables/useApi'

// --- TYPES ---
interface ProjectData {
  big_description: string | null
  id: number
  project_id: number
  create_at: string
  update_at: string | null
  is_active: boolean
  remove_at: string | null
}

interface ProjectItem {
  name: string
  id: number
  create_at: string
  update_at: string | null
  is_active: boolean
  remove_at: string | null
  data: ProjectData | null
}

interface ProjectsResponse {
  items: ProjectItem[]
  total: number
  page: number
  page_size: number
}

// --- COMPOSABLE SETUP ---
const api = useApi<ProjectsResponse>()

// Локальные состояния для UI
const projects = ref<ProjectItem[]>([])
const total = ref(0)
const isLoading = ref(false)
const localError = ref<string | null>(null)

// --- EMITS ---
const emit = defineEmits(['create-project', 'edit-project', 'delete-project', 'open-project'])

// --- METHODS ---
async function fetchProjects() {
  isLoading.value = true
  localError.value = null

  try {
    const responseData = await api.get('/project/', {
      params: {
        page: 1,
        page_size: 10,
      },
    })

    if (responseData) {
      projects.value = responseData.items || []
      total.value = responseData.total || 0
    } else {
      localError.value = 'Получен пустой ответ от сервера'
    }
  } catch (err: any) {
    console.error('Fetch failed', err)
    localError.value = err.message || 'Не удалось загрузить проекты'
  } finally {
    isLoading.value = false
  }
}

// Helpers
function formatDate(dateString: string | null): string {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return new Intl.DateTimeFormat('ru-RU', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  }).format(date)
}

function truncateText(text: string | null | undefined, length: number): string {
  if (!text) return ''
  if (text.length <= length) return text
  return text.substring(0, length) + '...'
}

onMounted(() => {
  fetchProjects()
})

defineExpose({ fetchProjects })
</script>

<style scoped>
.projects-page {
  padding: 20px;
  max-width: 900px; /* Уменьшил ширину для вертикального списка */
  margin: 0 auto;
  font-family: 'Inter', sans-serif;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.page-header h1 {
  font-size: 24px;
  color: #1a1a1a;
  margin: 0;
}

.btn-primary {
  background-color: #2563eb;
  color: white;
  border: none;
  padding: 10px 16px;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 500;
  transition: background 0.2s;
}

.btn-primary:hover {
  background-color: #1d4ed8;
}

.btn-secondary {
  background-color: #f3f4f6;
  color: #374151;
  border: 1px solid #d1d5db;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
  margin-top: 10px;
}

/* Вертикальный список */
.projects-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.project-card {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  overflow: hidden;
  transition:
    transform 0.2s,
    box-shadow 0.2s,
    border-color 0.2s;
  display: flex;
  flex-direction: column;
}

.project-card:hover {
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  border-color: #bfdbfe;
}

.card-header {
  padding: 12px 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #f3f4f6;
  background: #f9fafb;
}

.status-badge {
  font-size: 12px;
  padding: 4px 8px;
  border-radius: 12px;
  background: #fee2e2;
  color: #991b1b;
  font-weight: 600;
}

.status-badge.active {
  background: #dcfce7;
  color: #166534;
}

.card-actions {
  display: flex;
  gap: 4px;
}

.icon-btn-sm {
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  color: #6b7280;
  display: flex;
  align-items: center;
}

.icon-btn-sm:hover {
  background: #e5e7eb;
  color: #111827;
}

.icon-btn-sm.danger:hover {
  background: #fee2e2;
  color: #dc2626;
}

/* Стили для ссылки-карточки */
.card-body-link {
  text-decoration: none;
  color: inherit;
  display: block;
}

.card-body {
  padding: 16px;
  cursor: pointer;
}

.card-body:hover .project-title {
  color: #2563eb;
}

.project-title {
  margin: 0 0 4px 0;
  font-size: 18px;
  color: #111827;
  transition: color 0.2s;
}

.project-id {
  font-size: 12px;
  color: #9ca3af;
  margin-bottom: 12px;
}

.project-meta {
  margin-bottom: 12px;
  font-size: 13px;
  color: #4b5563;
}

.meta-row {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 4px;
}

.project-desc {
  font-size: 13px;
  color: #6b7280;
  line-height: 1.4;
  margin-top: 8px;
}

.card-footer {
  padding: 12px 16px 0 16px; /* Убрал нижний паддинг, так как ссылка занимает все место */
  text-align: right;
}

.more-link {
  font-size: 13px;
  color: #2563eb;
  font-weight: 500;
}

.loading-state,
.empty-state,
.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  color: #6b7280;
  text-align: center;
}

.spinner {
  font-size: 32px;
  animation: spin 1s linear infinite;
  margin-bottom: 10px;
  color: #2563eb;
}

.empty-icon,
.error-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.error-icon {
  color: #ef4444;
}

.empty-icon {
  color: #d1d5db;
}

.pagination-info {
  margin-top: 20px;
  text-align: center;
  font-size: 13px;
  color: #9ca3af;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>
