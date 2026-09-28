<template>
  <div class="app">
    <!-- LOADING STATE -->
    <div v-if="isLoading" class="loading-overlay">
      <Icon icon="solar:loader-outline" class="spinner" />
      <span>Загрузка информации о проекте...</span>
    </div>

    <!-- ERROR STATE -->
    <div v-else-if="localError" class="error-state">
      <Icon icon="solar:danger-triangle-outline" class="error-icon" />
      <h3>Ошибка загрузки</h3>
      <p>{{ localError }}</p>
      <button class="btn-secondary" @click="fetchData">Попробовать снова</button>
    </div>

    <!-- MAIN CONTENT -->
    <main v-else class="main">
      <!-- TOPBAR -->
      <header class="topbar">
        <div class="search-wrap">
          <Icon icon="solar:magnifer-outline"></Icon>
          <input v-model="searchQuery" class="search" placeholder="Поиск задач, проектов..." />
        </div>
        <button class="icon-btn" aria-label="Уведомления">
          <Icon icon="solar:bell-outline"></Icon>
        </button>
        <button class="icon-btn" aria-label="Приложения">
          <Icon icon="solar:widget-2-outline"></Icon>
        </button>
        <div class="profile">
          <img src="https://ui-avatars.com/api/?name=User&background=random" alt="User" />
        </div>
      </header>

      <section class="content">
        <!-- PROJECT HEADER -->
        <div class="project-head">
          <div>
            <router-link to="/projects" class="crumb">
              <Icon icon="solar:arrow-left-outline"></Icon>
              Назад к проектам
            </router-link>
            <h1>
              {{ projectData.title }}
              <span class="status-badge" :class="{ active: projectData.isActive }">
                {{ projectData.status }}
              </span>
            </h1>
            <div class="subtitle">{{ projectData.subtitle }}</div>
          </div>
          <div class="head-actions">
            <button class="btn" @click="$emit('edit')">
              <Icon icon="solar:pen-outline"></Icon>
              Редактировать
            </button>
            <button class="btn btn-more" aria-label="Дополнительно">
              <Icon icon="solar:menu-dots-outline"></Icon>
            </button>
            <button class="btn primary" @click="$emit('add-task')">
              <Icon icon="solar:add-circle-outline"></Icon>
              Добавить задачу
            </button>
          </div>
        </div>

        <!-- META -->
        <section class="project-meta">
          <div v-for="item in projectMeta" :key="item.label" class="meta-item">
            <Icon class="meta-icon" :icon="item.icon"></Icon>
            <div class="meta-content">
              <div class="meta-value">{{ item.value }}</div>
              <div class="meta-label">{{ item.label }}</div>
            </div>
          </div>
        </section>

        <!-- CONTENT GRID -->
        <div class="content-grid">
          <!-- LEFT -->
          <div class="left-column">
            <!-- DESCRIPTION -->
            <section class="card">
              <div class="card-header">
                <div class="card-title">
                  <Icon icon="solar:document-text-outline"></Icon>
                  Описание проекта
                </div>
                <div class="card-edit" @click="$emit('edit-description')">
                  <Icon icon="solar:pen-outline"></Icon>
                  Редактировать
                </div>
              </div>
              <div class="description">
                <p>{{ projectData.description || 'Описание отсутствует' }}</p>
              </div>
            </section>

            <!-- DOCUMENTATION / ATTACHMENTS -->
            <section class="card">
              <div class="card-header docs-header">
                <div class="card-title">
                  <Icon icon="solar:file-text-outline"></Icon>
                  Документация и файлы
                </div>
                <button class="upload-btn" @click="$emit('upload')">
                  <Icon icon="solar:upload-outline"></Icon>
                  Загрузить файл
                </button>
              </div>

              <div v-if="documents.length === 0" class="empty-docs">Нет прикрепленных файлов</div>

              <div v-else class="documents">
                <div class="doc-row header">
                  <div>Название</div>
                  <div>Тип</div>
                  <div>Размер</div>
                  <div class="hide-mobile">Дата загрузки</div>
                  <div></div>
                </div>
                <div v-for="doc in documents" :key="doc.id" class="doc-row">
                  <div class="doc-name">
                    <div :class="['file-icon', getFileColorClass(doc.mime_type)]">
                      <Icon :icon="getFileIcon(doc.mime_type)"></Icon>
                    </div>
                    <span>{{ doc.original_name }}</span>
                  </div>
                  <div class="doc-cell">{{ getShortType(doc.mime_type) }}</div>
                  <div class="doc-cell">{{ formatFileSize(doc.file_size) }}</div>
                  <div class="doc-cell hide-mobile">{{ formatDate(doc.created_at) }}</div>

                  <!-- Кнопка скачивания -->
                  <button
                    class="download-btn"
                    title="Скачать"
                    @click="downloadFile(doc.id, doc.original_name)"
                    :disabled="isDownloading === doc.id"
                  >
                    <Icon
                      :icon="
                        isDownloading === doc.id ? 'solar:loader-outline' : 'solar:download-outline'
                      "
                      :class="{ spinning: isDownloading === doc.id }"
                    ></Icon>
                  </button>
                </div>
              </div>
            </section>

            <!-- COSTS -->
            <section class="card">
              <div class="card-header">
                <div class="card-title">
                  <Icon icon="solar:wallet-money-outline"></Icon>
                  Затраты
                </div>
                <div class="card-edit" @click="$emit('edit-costs')">
                  <Icon icon="solar:pen-outline"></Icon>
                  Редактировать
                </div>
              </div>
              <div class="costs-content">
                <div class="total-cost">
                  <div class="total-label">Общие затраты</div>
                  <div class="total-value">{{ formatMoney(totalCost) }}</div>
                </div>
                <div class="cost-chart">
                  <div class="bar">
                    <div
                      v-for="cost in costs"
                      :key="cost.name"
                      class="bar-part"
                      :class="cost.barClass"
                    ></div>
                  </div>
                  <div class="cost-list">
                    <div v-for="cost in costs" :key="cost.name" class="cost-row">
                      <div class="cost-name">
                        <span class="cost-dot" :class="cost.dotClass"></span>
                        {{ cost.name }}
                      </div>
                      <div class="cost-amount">{{ formatMoney(cost.amount) }}</div>
                    </div>
                  </div>
                </div>
              </div>
            </section>
          </div>

          <!-- RIGHT -->
          <aside class="right-column">
            <!-- DEADLINE & STATUS -->
            <section class="card right-card">
              <div class="card-header">
                <div class="card-title">
                  <Icon icon="solar:calendar-outline"></Icon>
                  Сроки и статус
                </div>
              </div>
              <div class="deadline-content">
                <div class="progress-top">
                  <div class="progress" style="width: 100%">
                    <div
                      class="progress-value"
                      :style="{ width: projectData.progress + '%' }"
                    ></div>
                  </div>
                </div>
                <div class="progress-percent-wrap">
                  <span class="progress-percent">{{ projectData.progress }}%</span>
                </div>
                <div class="deadline-info">
                  <div class="deadline-item">
                    <div class="deadline-label">Создан</div>
                    <div class="deadline-value">{{ formatDate(projectData.create_at) }}</div>
                  </div>
                  <div class="deadline-item">
                    <div class="deadline-label">Обновлен</div>
                    <div class="deadline-value">{{ formatDate(projectData.update_at) }}</div>
                  </div>
                  <div class="deadline-item">
                    <div class="deadline-label">Статус</div>
                    <div class="deadline-value">
                      {{ projectData.isActive ? 'Активен' : 'Архив' }}
                    </div>
                  </div>
                </div>
              </div>
            </section>

            <!-- QUICK ACTIONS -->
            <section class="card right-card">
              <div class="card-header">
                <div class="card-title">
                  <Icon icon="solar:bolt-outline"></Icon>
                  Быстрые действия
                </div>
              </div>
              <div class="quick-list">
                <div
                  v-for="action in quickActions"
                  :key="action.label"
                  class="quick-item"
                  @click="$emit(action.event)"
                >
                  <Icon :icon="action.icon"></Icon>
                  {{ action.label }}
                  <Icon class="quick-arrow" icon="solar:alt-arrow-right-outline"></Icon>
                </div>
              </div>
            </section>
          </aside>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { Icon } from '@iconify/vue'
import { useApi } from '@/composables/useApi'
import axios from 'axios' // Импортируем axios напрямую для blob-запросов
import '@/assets/styles/ProgectInfoVue.css'

// --- TYPES ---
interface ProjectResponse {
  name: string
  id: number
  create_at: string
  update_at: string | null
  is_active: boolean
  remove_at: string | null
  data: {
    big_description: string | null
    id: number
    project_id: number
    create_at: string
    update_at: string | null
    is_active: boolean
    remove_at: string | null
  }
}

interface Attachment {
  original_name: string
  file_metadata: any
  id: number
  project_id: number
  stored_name: string
  file_size: number
  mime_type: string
  created_at: string
}

// --- SETUP ---
const route = useRoute()
const projectId = route.params.id as string

const projectApi = useApi<ProjectResponse>()
const attachmentsApi = useApi<Attachment[]>()

const isLoading = ref(false)
const localError = ref<string | null>(null)
const searchQuery = ref('')
const isDownloading = ref<number | null>(null) // ID файла, который сейчас скачивается

const projectRaw = ref<ProjectResponse | null>(null)
const attachments = ref<Attachment[]>([])

// Computed Project Data
const projectData = computed(() => {
  if (!projectRaw.value)
    return {
      title: '',
      status: '',
      subtitle: '',
      description: '',
      startDate: '-',
      endDate: '-',
      daysLeft: 0,
      progress: 0,
      isActive: false,
      create_at: '',
      update_at: '',
    }

  const p = projectRaw.value
  return {
    title: p.name,
    status: p.is_active ? 'В работе' : 'Завершен',
    subtitle: `ID проекта: ${p.id}`,
    description: p.data?.big_description || 'Нет подробного описания',
    startDate: formatDate(p.create_at),
    endDate: '-',
    daysLeft: 0,
    progress: 35,
    isActive: p.is_active,
    create_at: p.create_at,
    update_at: p.update_at,
  }
})

const projectMeta = computed(() => [
  {
    icon: 'solar:calendar-outline',
    value: `${projectData.value.startDate} – ${projectData.value.endDate}`,
    label: 'Срок выполнения',
  },
  {
    icon: 'solar:database-outline',
    value: formatMoney(totalCost.value),
    label: 'Затраты на разработку',
  },
  { icon: 'solar:users-group-rounded-outline', value: '5', label: 'Исполнители' },
  { icon: 'solar:user-outline', value: 'Не указан', label: 'Инициатор' },
  { icon: 'solar:user-check-outline', value: 'Не указан', label: 'Менеджер проекта' },
])

const documents = computed(() =>
  attachments.value.map((att) => ({
    ...att,
    type: getShortType(att.mime_type),
    uploadedAt: formatDate(att.created_at),
    author: 'Система',
  })),
)

const costs = [
  { name: 'Разработка', amount: 1_850_000, barClass: 'bar-development', dotClass: 'dot-blue' },
  { name: 'Тестирование', amount: 450_000, barClass: 'bar-testing', dotClass: 'dot-green' },
  { name: 'Внедрение', amount: 250_000, barClass: 'bar-implementation', dotClass: 'dot-green2' },
  { name: 'Прочее', amount: 102_000, barClass: 'bar-other', dotClass: 'dot-purple' },
]
const totalCost = computed(() => costs.reduce((sum, c) => sum + c.amount, 0))

const quickActions = [
  { icon: 'solar:refresh-outline', label: 'Изменить статус проекта', event: 'change-status' },
  { icon: 'solar:add-circle-outline', label: 'Добавить задачу', event: 'add-task' },
  { icon: 'solar:upload-outline', label: 'Загрузить документацию', event: 'upload-docs' },
  { icon: 'solar:wallet-money-outline', label: 'Добавить затраты', event: 'add-cost' },
]

// --- METHODS ---

async function fetchData() {
  isLoading.value = true
  localError.value = null

  try {
    const projectRes = await projectApi.get(`/project/${projectId}/`)
    if (projectRes) {
      projectRaw.value = projectRes
    }

    const attachRes = await attachmentsApi.get(`/projects/${projectId}/attachments/`)
    if (attachRes) {
      attachments.value = attachRes
    }
  } catch (err: any) {
    console.error(err)
    localError.value = err.message || 'Ошибка загрузки данных'
  } finally {
    isLoading.value = false
  }
}

// Функция скачивания файла
async function downloadFile(attachmentId: number, fileName: string) {
  isDownloading.value = attachmentId
  try {
    // Используем прямой вызов axios для получения blob, так как useApi может быть настроен на JSON
    const response = await axios.get(
      `/projects/${projectId}/attachments/${attachmentId}/download`,
      {
        responseType: 'blob',
        // Если нужен токен авторизации, он должен быть добавлен интерцептором httpClient
        // или вручную через headers, если httpClient экспортирует instance
      },
    )

    // Создаем ссылку для скачивания
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', fileName)
    document.body.appendChild(link)
    link.click()

    // Очистка
    link.remove()
    window.URL.revokeObjectURL(url)
  } catch (err) {
    console.error('Ошибка скачивания:', err)
    alert('Не удалось скачать файл')
  } finally {
    isDownloading.value = null
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
  }).format(date)
}

function formatMoney(value: number): string {
  return new Intl.NumberFormat('ru-RU').format(value) + ' ₽'
}

function formatFileSize(bytes: number): string {
  if (bytes === 0) return '0 Б'
  const k = 1024
  const sizes = ['Б', 'КБ', 'МБ', 'ГБ']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i]
}

function getShortType(mime: string): string {
  if (mime.includes('pdf')) return 'PDF'
  if (mime.includes('word') || mime.includes('document')) return 'DOC'
  if (mime.includes('excel') || mime.includes('sheet')) return 'XLS'
  if (mime.includes('image')) return 'IMG'
  if (mime.includes('zip') || mime.includes('rar') || mime.includes('archive')) return 'ARCH'
  if (mime.includes('text')) return 'TXT'
  return 'FILE'
}

function getFileIcon(mime: string): string {
  if (mime.includes('pdf')) return 'solar:file-pdf-outline'
  if (mime.includes('word') || mime.includes('document')) return 'solar:file-word-outline'
  if (mime.includes('excel') || mime.includes('sheet')) return 'solar:file-excel-outline'
  if (mime.includes('image')) return 'solar:file-image-outline'
  if (mime.includes('zip') || mime.includes('rar') || mime.includes('7z'))
    return 'solar:archive-outline'
  if (mime.includes('text')) return 'solar:file-text-outline'
  return 'solar:file-text-outline'
}

function getFileColorClass(mime: string): string {
  if (mime.includes('pdf')) return 'file-pdf-color'
  if (mime.includes('word') || mime.includes('document')) return 'file-word-color'
  if (mime.includes('excel') || mime.includes('sheet')) return 'file-excel-color'
  if (mime.includes('image')) return 'file-image-color'
  if (mime.includes('zip') || mime.includes('rar')) return 'file-archive-color'
  return 'file-default-color'
}

defineEmits([
  'edit',
  'edit-description',
  'edit-costs',
  'add-task',
  'add-member',
  'upload',
  'change-status',
  'upload-docs',
  'add-cost',
])

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
/* Локальные стили для цветов иконок файлов */
.file-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 6px;
  margin-right: 12px;
  font-size: 20px;
  background: #f3f4f6; /* Default bg */
}

/* Цвета иконок */
.file-pdf-color {
  color: #dc2626;
  background: #fee2e2;
}
.file-word-color {
  color: #2563eb;
  background: #dbeafe;
}
.file-excel-color {
  color: #16a34a;
  background: #dcfce7;
}
.file-image-color {
  color: #9333ea;
  background: #f3e8ff;
}
.file-archive-color {
  color: #d97706;
  background: #fef3c7;
}
.file-default-color {
  color: #4b5563;
  background: #f3f4f6;
}

/* Остальные стили */
.loading-overlay,
.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  color: #6b7280;
}
.spinner {
  font-size: 48px;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
  color: #2563eb;
}
.error-icon {
  font-size: 48px;
  color: #ef4444;
  margin-bottom: 16px;
}
.btn-secondary {
  margin-top: 16px;
  padding: 8px 16px;
  background: #f3f4f6;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  cursor: pointer;
}

.status-badge {
  font-size: 11px;
  background: #e7f5ff;
  color: #168be5;
  padding: 5px 9px;
  border-radius: 20px;
  vertical-align: middle;
  margin-left: 8px;
}
.status-badge.active {
  background: #dcfce7;
  color: #166534;
}

.progress-percent-wrap {
  display: flex;
  justify-content: flex-end;
  margin-top: -25px;
  margin-bottom: 10px;
}

.empty-docs {
  padding: 20px;
  text-align: center;
  color: #9ca3af;
  font-style: italic;
}

.doc-row.header {
  font-weight: 600;
  color: #374151;
  border-bottom: 1px solid #e5e7eb;
  padding-bottom: 8px;
  margin-bottom: 8px;
}

.doc-row {
  display: flex;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid #f3f4f6;
}
.doc-row:last-child {
  border-bottom: none;
}
.doc-name {
  display: flex;
  align-items: center;
  flex: 2;
  min-width: 200px;
}
.doc-cell {
  flex: 1;
  color: #6b7280;
  font-size: 13px;
}

.download-btn {
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 6px;
  border-radius: 4px;
  color: #6b7280;
  display: flex;
  align-items: center;
  transition: all 0.2s;
}

.download-btn:hover:not(:disabled) {
  background: #e5e7eb;
  color: #2563eb;
}

.download-btn:disabled {
  opacity: 0.5;
  cursor: wait;
}

.spinning {
  animation: spin 1s linear infinite;
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
