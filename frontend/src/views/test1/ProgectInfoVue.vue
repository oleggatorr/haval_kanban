<template>
  <div class="project-page">
    <!-- HEADER С НАВИГАЦИЕЙ -->
    <header class="page-header">
      <div class="header-left">
        <router-link to="/list" class="back-link">
          <Icon icon="solar:arrow-left-outline" />
          <span>К списку проектов</span>
        </router-link>

        <div v-if="loading" class="skeleton-title">Загрузка...</div>
        <h1 v-else class="project-title">
          {{ project?.name || 'Без названия' }}
          <span v-if="project?.is_active" class="status-badge">Активен</span>
        </h1>
      </div>

      <div class="header-actions">
        <router-link :to="`/project/${projectId}/board`" class="btn-primary">
          <Icon icon="solar:kanban-board-outline" />
          Перейти к доске
        </router-link>
      </div>
    </header>

    <!-- ОСНОВНОЙ КОНТЕНТ -->
    <main v-if="!loading && project" class="content-grid">
      <!-- ЛЕВАЯ КОЛОНКА: ОПИСАНИЕ -->
      <section class="card description-card">
        <div class="card-header">
          <h2>Описание проекта</h2>
          <!-- Здесь можно добавить кнопку редактирования в будущем -->
        </div>
        <div class="card-body">
          <p v-if="project.data?.big_description" class="description-text">
            {{ project.data.big_description }}
          </p>
          <p v-else class="text-muted">Описание отсутствует.</p>

          <div class="meta-info">
            <div class="meta-item">
              <span class="label">ID Проекта:</span>
              <span class="value">#{{ project.id }}</span>
            </div>
            <div class="meta-item">
              <span class="label">Создан:</span>
              <span class="value">{{ formatDate(project.create_at) }}</span>
            </div>
            <div class="meta-item">
              <span class="label">Обновлен:</span>
              <span class="value">{{
                project.update_at ? formatDate(project.update_at) : '—'
              }}</span>
            </div>
          </div>
        </div>
      </section>

      <!-- ПРАВАЯ КОЛОНКА: ФАЙЛЫ -->
      <aside class="files-sidebar">
        <div class="card files-card">
          <div class="card-header">
            <h2>Документы</h2>
            <span class="count-badge">{{ documents.length }}</span>
          </div>

          <div v-if="loadingDocs" class="loading-small">Загрузка файлов...</div>

          <div v-else-if="documents.length === 0" class="empty-files">
            <Icon icon="solar:folder-open-outline" class="empty-icon" />
            <p>Нет загруженных файлов</p>
          </div>

          <div v-else class="file-list">
            <div v-for="doc in documents" :key="doc.id" class="file-item">
              <div class="file-icon-wrapper" :class="getFileColor(doc.mime_type)">
                <Icon :icon="getFileIcon(doc.mime_type)" />
              </div>
              <div class="file-info">
                <div class="file-name" :title="doc.original_name">{{ doc.original_name }}</div>
                <div class="file-meta">
                  {{ formatFileSize(doc.file_size) }} • {{ formatDate(doc.created_at) }}
                </div>
              </div>
              <a
                :href="`/api/files/${doc.stored_name}`"
                target="_blank"
                class="file-download-btn"
                title="Скачать"
              >
                <Icon icon="solar:download-outline" />
              </a>
            </div>
          </div>
        </div>
      </aside>
    </main>

    <!-- Состояние загрузки всей страницы -->
    <div v-else-if="loading" class="full-loader">
      <Icon icon="solar:loader-outline" class="spinner" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Icon } from '@iconify/vue'
import { useApi } from '@/composables/useApi'
import { useRoute } from 'vue-router'

// --- Типы данных (согласно вашему JSON) ---
interface ProjectData {
  big_description: string | null
  id: number
  project_id: number
  create_at: string
  update_at: string | null
  is_active: boolean
  remove_at: string | null
}

interface Project {
  name: string
  id: number
  create_at: string
  update_at: string | null
  is_active: boolean
  remove_at: string | null
  data: ProjectData | null
}

interface ProjectFile {
  original_name: string
  file_metadata: Record<string, any>
  id: number
  project_id: number
  stored_name: string
  file_size: number
  mime_type: string
  created_at: string
}

// --- Setup ---
const route = useRoute()
const projectId = Number(route.params.projectId) // Берем ID из URL

const project = ref<Project | null>(null)
const documents = ref<ProjectFile[]>([])
const loading = ref(true)
const loadingDocs = ref(false)

const projectApi = useApi<Project>()
const filesApi = useApi<ProjectFile[]>()

// --- Методы ---

async function loadData() {
  try {
    // Параллельная загрузка для скорости
    const [projData, docsData] = await Promise.all([
      projectApi.get(`/project/${projectId}`),
      filesApi.get(`/projects/${projectId}/attachments/`),
    ])

    if (projData) project.value = projData
    if (docsData) documents.value = docsData
  } catch (e) {
    console.error('Ошибка загрузки:', e)
  } finally {
    loading.value = false
    loadingDocs.value = false
  }
}

// Форматирование даты
function formatDate(dateString: string | null): string {
  if (!dateString) return '—'
  return new Date(dateString).toLocaleDateString('ru-RU', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
  })
}

// Размер файла
function formatFileSize(bytes: number): string {
  if (!bytes) return '0 Б'
  const k = 1024
  const sizes = ['Б', 'КБ', 'МБ', 'ГБ']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i]
}

// Иконки для файлов
function getFileIcon(mime: string): string {
  if (mime.includes('pdf')) return 'solar:file-text-outline'
  if (mime.includes('image')) return 'solar:image-outline'
  if (mime.includes('word') || mime.includes('document')) return 'solar:file-text-outline'
  if (mime.includes('excel') || mime.includes('sheet')) return 'solar:table-outline'
  return 'solar:file-outline'
}

function getFileColor(mime: string): string {
  if (mime.includes('pdf')) return 'color-red'
  if (mime.includes('image')) return 'color-blue'
  if (mime.includes('word') || mime.includes('document')) return 'color-blue-dark'
  if (mime.includes('excel')) return 'color-green'
  return 'color-gray'
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.project-page {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  min-height: 100vh;
  background-color: #f8fafc;
}

/* Header */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 2rem;
  border-bottom: 1px solid #e2e8f0;
  padding-bottom: 1.5rem;
}

.header-left {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.back-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  color: #64748b;
  font-size: 0.9rem;
  text-decoration: none;
  transition: color 0.2s;
}

.back-link:hover {
  color: #2563eb;
}

.project-title {
  font-size: 2rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 12px;
}

.status-badge {
  font-size: 0.75rem;
  background: #dcfce7;
  color: #166534;
  padding: 4px 10px;
  border-radius: 20px;
  font-weight: 600;
  text-transform: uppercase;
}

.btn-primary {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: #2563eb;
  color: white;
  padding: 10px 20px;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 500;
  transition: background 0.2s;
}

.btn-primary:hover {
  background: #1d4ed8;
}

/* Grid Layout */
.content-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 2rem;
}

@media (max-width: 900px) {
  .content-grid {
    grid-template-columns: 1fr;
  }
}

/* Cards */
.card {
  background: white;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  overflow: hidden;
}

.card-header {
  padding: 1.25rem;
  border-bottom: 1px solid #f1f5f9;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h2 {
  margin: 0;
  font-size: 1.1rem;
  color: #334155;
}

.card-body {
  padding: 1.25rem;
}

/* Description */
.description-text {
  line-height: 1.6;
  color: #475569;
  white-space: pre-wrap; /* Сохраняет переносы строк */
  margin-bottom: 2rem;
}

.text-muted {
  color: #94a3b8;
  font-style: italic;
}

.meta-info {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #f1f5f9;
}

.meta-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.meta-item .label {
  font-size: 0.8rem;
  color: #94a3b8;
}

.meta-item .value {
  font-size: 0.95rem;
  color: #334155;
  font-weight: 500;
}

/* Files Sidebar */
.count-badge {
  background: #f1f5f9;
  color: #64748b;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 600;
}

.file-list {
  display: flex;
  flex-direction: column;
}

.file-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 1.25rem;
  border-bottom: 1px solid #f1f5f9;
  transition: background 0.2s;
}

.file-item:last-child {
  border-bottom: none;
}

.file-item:hover {
  background: #f8fafc;
}

.file-icon-wrapper {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
}

.color-red {
  background: #fee2e2;
  color: #ef4444;
}
.color-blue {
  background: #e0f2fe;
  color: #0ea5e9;
}
.color-blue-dark {
  background: #dbeafe;
  color: #2563eb;
}
.color-green {
  background: #dcfce7;
  color: #22c55e;
}
.color-gray {
  background: #f1f5f9;
  color: #64748b;
}

.file-info {
  flex: 1;
  overflow: hidden;
}

.file-name {
  font-size: 0.9rem;
  font-weight: 500;
  color: #334155;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.file-meta {
  font-size: 0.75rem;
  color: #94a3b8;
  margin-top: 2px;
}

.file-download-btn {
  color: #94a3b8;
  padding: 6px;
  border-radius: 6px;
  transition: all 0.2s;
}

.file-download-btn:hover {
  background: #e2e8f0;
  color: #2563eb;
}

.empty-files {
  padding: 2rem;
  text-align: center;
  color: #94a3b8;
}

.empty-icon {
  font-size: 2rem;
  margin-bottom: 0.5rem;
  opacity: 0.5;
}

.loading-small {
  padding: 1rem;
  text-align: center;
  color: #64748b;
  font-size: 0.9rem;
}

.full-loader {
  display: flex;
  justify-content: center;
  padding: 4rem;
}

.spinner {
  font-size: 2rem;
  color: #2563eb;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
