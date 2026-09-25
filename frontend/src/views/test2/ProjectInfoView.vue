<template>
  <div class="app">
    <!-- =========================================
       SIDEBAR
    ========================================== -->
    <aside class="sidebar">
      <nav class="nav">
        <a class="active" href="#">
          <iconify-icon class="icon" icon="solar:folder-with-files-outline"></iconify-icon>
          <span>Проекты</span>
          <span class="nav-counter">3</span>
        </a>
        <a href="#">
          <iconify-icon class="icon" icon="solar:checklist-minimalistic-outline"></iconify-icon>
          <span>Мои задачи</span>
          <span class="nav-counter">15</span>
        </a>
        <a href="#">
          <iconify-icon class="icon" icon="solar:kanban-board-outline"></iconify-icon>
          <span>Канбан</span>
        </a>
        <a href="#">
          <iconify-icon class="icon" icon="solar:calendar-outline"></iconify-icon>
          <span>Календарь</span>
        </a>
        <a href="#">
          <iconify-icon class="icon" icon="solar:chart-2-outline"></iconify-icon>
          <span>Отчёты</span>
        </a>
        <a href="#">
          <iconify-icon class="icon" icon="solar:settings-outline"></iconify-icon>
          <span>Настройки</span>
        </a>
      </nav>
      <div class="sidebar-user">
        <div class="avatar">
          <img src="https://i.pravatar.cc/100?img=12" alt="" />
        </div>
        <div class="user-meta">
          Иван Петров
          <small>Frontend Developer</small>
        </div>
      </div>
    </aside>

    <!-- =========================================
       MAIN
    ========================================== -->
    <main class="main">
      <!-- TOPBAR -->
      <header class="topbar">
        <div class="search-wrap">
          <iconify-icon icon="solar:magnifer-outline"></iconify-icon>
          <input class="search" placeholder="Поиск задач, проектов..." />
        </div>
        <button class="icon-btn" aria-label="Уведомления">
          <iconify-icon icon="solar:bell-outline"></iconify-icon>
        </button>
        <button class="icon-btn" aria-label="Приложения">
          <iconify-icon icon="solar:widget-2-outline"></iconify-icon>
        </button>
        <div class="profile">
          <img src="https://i.pravatar.cc/100?img=12" alt="" />
        </div>
      </header>

      <section class="content">
        <!-- PROJECT HEADER -->
        <div class="project-head">
          <div>
            <router-link to="/projects" class="crumb">
              <iconify-icon icon="solar:arrow-left-outline"></iconify-icon>
              Назад к проектам
            </router-link>

            <!-- Показываем скелетон или текст пока грузится проект -->
            <h1 v-if="loadingProject">Загрузка проекта...</h1>
            <h1 v-else>
              {{ project?.name || 'Без названия' }}
              <span
                v-if="project?.is_active"
                style="
                  font-size: 11px;
                  background: #e7f5ff;
                  color: #168be5;
                  padding: 5px 9px;
                  border-radius: 20px;
                  vertical-align: middle;
                "
              >
                В работе
              </span>
            </h1>

            <div class="subtitle" v-if="!loadingProject">ID проекта: {{ project?.id }}</div>
          </div>

          <div class="head-actions" v-if="!loadingProject">
            <button class="btn">
              <iconify-icon icon="solar:pen-outline"></iconify-icon>
              Редактировать
            </button>
            <button class="btn btn-more" aria-label="Дополнительно">
              <iconify-icon icon="solar:menu-dots-outline"></iconify-icon>
            </button>
            <button class="btn primary">
              <iconify-icon icon="solar:add-circle-outline"></iconify-icon>
              Добавить задачу
            </button>
          </div>
        </div>

        <!-- META -->
        <section class="project-meta" v-if="!loadingProject && project">
          <div class="meta-item">
            <iconify-icon class="meta-icon" icon="solar:calendar-outline"></iconify-icon>
            <div class="meta-content">
              <div class="meta-value">{{ formatDate(project.create_at) }}</div>
              <div class="meta-label">Дата создания</div>
            </div>
          </div>
          <div class="meta-item">
            <iconify-icon class="meta-icon" icon="solar:refresh-outline"></iconify-icon>
            <div class="meta-content">
              <div class="meta-value">
                {{ project.update_at ? formatDate(project.update_at) : 'Нет изменений' }}
              </div>
              <div class="meta-label">Последнее обновление</div>
            </div>
          </div>
          <div class="meta-item">
            <iconify-icon class="meta-icon" icon="solar:document-text-outline"></iconify-icon>
            <div class="meta-content">
              <div class="meta-value">{{ documents.length }}</div>
              <div class="meta-label">Документов</div>
            </div>
          </div>
          <div class="meta-item">
            <iconify-icon class="meta-icon" icon="solar:wallet-money-outline"></iconify-icon>
            <div class="meta-content">
              <div class="meta-value">—</div>
              <div class="meta-label">Бюджет</div>
            </div>
          </div>
        </section>

        <!-- TABS -->
        <div class="tabs" v-if="!loadingProject">
          <a href="#" class="tab active">Обзор</a>
          <a href="#" class="tab">Задачи</a>
          <a href="#" class="tab"
            >Документация <span class="tab-count">{{ documents.length }}</span></a
          >
          <a href="#" class="tab">Команда</a>
        </div>

        <!-- CONTENT GRID -->
        <div class="content-grid" v-if="!loadingProject && project">
          <!-- LEFT -->
          <div class="left-column">
            <!-- DESCRIPTION -->
            <section class="card">
              <div class="card-header">
                <div class="card-title">
                  <iconify-icon icon="solar:document-text-outline"></iconify-icon>
                  Описание проекта
                </div>
                <div class="card-edit">
                  <iconify-icon icon="solar:pen-outline"></iconify-icon>
                  Редактировать
                </div>
              </div>
              <div class="description">
                <p v-if="project.data?.big_description">
                  {{ project.data.big_description }}
                </p>
                <p v-else class="text-muted">
                  Описание отсутствует. Нажмите "Редактировать", чтобы добавить информацию о
                  проекте.
                </p>
              </div>
            </section>

            <!-- DOCUMENTATION -->
            <section class="card">
              <div class="card-header docs-header">
                <div class="card-title">
                  <iconify-icon icon="solar:file-text-outline"></iconify-icon>
                  Документация
                </div>
                <button class="upload-btn">
                  <iconify-icon icon="solar:upload-outline"></iconify-icon>
                  Загрузить файл
                </button>
              </div>

              <div v-if="loadingDocs" class="loading-state">Загрузка документов...</div>

              <div v-else-if="documents.length === 0" class="empty-state">
                Нет загруженных документов
              </div>

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
                    <div class="file-icon" :class="getFileIconClass(doc.mime_type)">
                      <iconify-icon :icon="getFileIconName(doc.mime_type)"></iconify-icon>
                    </div>
                    <span>{{ doc.original_name }}</span>
                  </div>
                  <div class="doc-cell">{{ getDocTypeLabel(doc.mime_type) }}</div>
                  <div class="doc-cell">{{ formatFileSize(doc.file_size) }}</div>
                  <div class="doc-cell hide-mobile">{{ formatDate(doc.created_at) }}</div>
                  <iconify-icon class="doc-more" icon="solar:menu-dots-outline"></iconify-icon>
                </div>
              </div>
            </section>
          </div>

          <!-- RIGHT -->
          <aside class="right-column">
            <!-- STATUS CARD -->
            <section class="card right-card">
              <div class="card-header">
                <div class="card-title">
                  <iconify-icon icon="solar:activity-outline"></iconify-icon>
                  Статус системы
                </div>
              </div>
              <div class="deadline-content">
                <div class="deadline-info">
                  <div class="deadline-item">
                    <div class="deadline-label">Активен</div>
                    <div
                      class="deadline-value"
                      :style="{ color: project.is_active ? '#10b981' : '#ef4444' }"
                    >
                      {{ project.is_active ? 'Да' : 'Нет' }}
                    </div>
                  </div>
                  <div class="deadline-item">
                    <div class="deadline-label">ID в системе</div>
                    <div class="deadline-value">#{{ project.id }}</div>
                  </div>
                </div>
              </div>
            </section>

            <!-- QUICK ACTIONS -->
            <section class="card right-card">
              <div class="card-header">
                <div class="card-title">
                  <iconify-icon icon="solar:bolt-outline"></iconify-icon>
                  Быстрые действия
                </div>
              </div>
              <div class="quick-list">
                <div class="quick-item">
                  <iconify-icon icon="solar:add-circle-outline"></iconify-icon>
                  Добавить задачу
                  <iconify-icon
                    class="quick-arrow"
                    icon="solar:alt-arrow-right-outline"
                  ></iconify-icon>
                </div>
                <div class="quick-item">
                  <iconify-icon icon="solar:upload-outline"></iconify-icon>
                  Загрузить документацию
                  <iconify-icon
                    class="quick-arrow"
                    icon="solar:alt-arrow-right-outline"
                  ></iconify-icon>
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
import { ref, onMounted } from 'vue'
import { useApi } from '@/composables/useApi'
import '@/assets/styles/ProgectInfoVue.css'

// --- Типы ---
interface ProjectData {
  big_description: string
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
  data: ProjectData
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

// --- Props ---
const props = defineProps<{
  projectId: number | string
}>()

// --- State ---
const project = ref<Project | null>(null)
const documents = ref<ProjectFile[]>([])
const loadingProject = ref(false)
const loadingDocs = ref(false)

// --- API Instances ---
// Создаем экземпляры API для разных типов данных
const projectApi = useApi<Project>()
const filesApi = useApi<ProjectFile[]>()

// --- Methods ---

const formatDate = (dateString: string | null) => {
  if (!dateString) return '—'
  return new Date(dateString).toLocaleDateString('ru-RU', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
  })
}

const formatFileSize = (bytes: number) => {
  if (bytes === 0) return '0 Б'
  const k = 1024
  const sizes = ['Б', 'КБ', 'МБ', 'ГБ']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i]
}

const getDocTypeLabel = (mime: string) => {
  if (mime.includes('pdf')) return 'PDF'
  if (mime.includes('word') || mime.includes('document')) return 'DOCX'
  if (mime.includes('excel') || mime.includes('sheet')) return 'XLSX'
  if (mime.includes('image')) return 'IMG'
  return 'FILE'
}

const getFileIconName = (mime: string) => {
  if (mime.includes('pdf')) return 'solar:file-text-outline'
  if (mime.includes('word') || mime.includes('document')) return 'solar:file-text-outline'
  if (mime.includes('excel') || mime.includes('sheet')) return 'solar:file-text-outline'
  if (mime.includes('image')) return 'solar:image-outline'
  return 'solar:file-outline'
}

const getFileIconClass = (mime: string) => {
  if (mime.includes('pdf')) return 'file-pdf'
  if (mime.includes('word') || mime.includes('document')) return 'file-word'
  if (mime.includes('excel') || mime.includes('sheet')) return 'file-excel'
  if (mime.includes('image')) return 'file-image'
  return ''
}

/**
 * Основная функция загрузки всех данных
 */
const loadData = async () => {
  loadingProject.value = true
  loadingDocs.value = true

  try {
    // 1. Загрузка информации о проекте
    // Эндпоинт: /project/{project_id}
    const projectData = await projectApi.get(`/project/${props.projectId}`)
    if (projectData) {
      project.value = projectData
    }

    // 2. Загрузка документов (параллельно или последовательно)
    // Эндпоинт: /projects/{project_id}/attachments/
    const docsData = await filesApi.get(`/projects/${props.projectId}/attachments/`)
    if (docsData) {
      documents.value = docsData
    }
  } catch (e) {
    console.error('Ошибка загрузки данных проекта:', e)
  } finally {
    loadingProject.value = false
    loadingDocs.value = false
  }
}

onMounted(() => {
  loadData()
})
</script>
