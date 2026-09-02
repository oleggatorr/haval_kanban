<!-- src/views/ProjectsList.vue -->
<template>
  <div class="projects-container">
    <h1>Список проектов</h1>

    <!-- Индикатор загрузки -->
    <div v-if="isLoading" class="loading">Загрузка проектов...</div>

    <!-- Форма добавления нового проекта -->
    <div class="add-project">
      <input
        v-model="newProjectName"
        placeholder="Название проекта"
        @keyup.enter="addProject"
        :disabled="isLoading"
      />
      <input
        v-model="newProjectDescription"
        placeholder="Описание проекта"
        @keyup.enter="addProject"
        :disabled="isLoading"
      />
      <button @click="addProject" :disabled="isLoading">Добавить</button>
    </div>

    <!-- Список проектов -->
    <div v-if="projects.length > 0 && !isLoading" class="projects-list">
      <div v-for="project in projects" :key="project.id" class="project-item">
        <!-- Ссылка на проект -->
        <router-link :to="`/project/${project.id}`" class="project-link">
          <div class="project-info">
            <span class="project-name">{{ project.name }}</span>
            <span v-if="project.description" class="project-description">
              {{ project.description }}
            </span>
            <span class="project-id">ID: {{ project.id }}</span>
          </div>
        </router-link>

        <div class="project-actions">
          <button @click="toggleStatus(project.id)" class="status-btn">
            {{ project.status === 'active' ? 'Приостановить' : 'Активировать' }}
          </button>
          <button @click="deleteProject(project.id)" class="delete-btn">Удалить</button>
        </div>
      </div>
    </div>

    <!-- Сообщение, если проектов нет -->
    <p v-if="projects.length === 0 && !isLoading" class="empty-message">Нет проектов</p>

    <!-- Сообщение об ошибке -->
    <p v-if="error" class="error-message">{{ error }}</p>

    <!-- Статистика -->
    <div class="stats" v-if="projects.length > 0 && !isLoading">
      <p>Всего: {{ projects.length }}</p>
      <p>Активных: {{ activeProjectsCount }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { httpClient } from '@/services/api'

// Типы
interface Project {
  id: number
  name: string
  description?: string
  status?: 'active' | 'completed'
}

// Состояния
const projects = ref<Project[]>([])
const isLoading = ref(false)
const error = ref<string | null>(null)
const newProjectName = ref('')
const newProjectDescription = ref('')

// Вычисляемые свойства
const activeProjectsCount = computed(() => {
  return projects.value.filter((p) => p.status === 'active').length
})

// Методы
const fetchProjects = async () => {
  isLoading.value = true
  error.value = null

  try {
    const response = await httpClient.get<Project[]>('/project/')

    projects.value = response.map((project) => ({
      ...project,
      status: project.status || 'active',
    }))

    console.log('✅ Проекты загружены:', projects.value)
  } catch (err) {
    console.error('❌ Ошибка загрузки проектов:', err)
    error.value = 'Не удалось загрузить список проектов'
    projects.value = []
  } finally {
    isLoading.value = false
  }
}

const addProject = async () => {
  if (!newProjectName.value.trim()) {
    error.value = 'Название проекта обязательно'
    return
  }

  isLoading.value = true
  error.value = null

  try {
    const newProject = await httpClient.post<Project>('/project/', {
      name: newProjectName.value.trim(),
      description: newProjectDescription.value.trim() || undefined,
    })

    projects.value.push({
      ...newProject,
      status: 'active',
    })

    newProjectName.value = ''
    newProjectDescription.value = ''

    console.log('✅ Проект создан:', newProject)
  } catch (err) {
    console.error('❌ Ошибка создания проекта:', err)
    error.value = 'Не удалось создать проект'
  } finally {
    isLoading.value = false
  }
}

const deleteProject = async (id: number) => {
  if (!confirm('Вы уверены, что хотите удалить этот проект?')) {
    return
  }

  isLoading.value = true
  error.value = null

  try {
    await httpClient.delete(`/project/${id}`)
    projects.value = projects.value.filter((p) => p.id !== id)
    console.log('✅ Проект удален:', id)
  } catch (err) {
    console.error('❌ Ошибка удаления проекта:', err)
    error.value = 'Не удалось удалить проект'
  } finally {
    isLoading.value = false
  }
}

const toggleStatus = async (id: number) => {
  const project = projects.value.find((p) => p.id === id)
  if (!project) return

  const newStatus = project.status === 'active' ? 'completed' : 'active'

  isLoading.value = true
  error.value = null

  try {
    await httpClient.patch(`/project/${id}`, {
      status: newStatus,
    })

    project.status = newStatus
    console.log('✅ Статус обновлен:', { id, newStatus })
  } catch (err) {
    console.error('❌ Ошибка обновления статуса:', err)
    error.value = 'Не удалось обновить статус проекта'
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  fetchProjects()
})
</script>

<style scoped>
.projects-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
}

h1 {
  color: #2c3e50;
  text-align: center;
  margin-bottom: 24px;
}

.loading {
  text-align: center;
  padding: 20px;
  color: #7f8c8d;
}

.error-message {
  color: #dc2626;
  text-align: center;
  font-size: 0.9rem;
  margin: 10px 0;
  padding: 10px;
  background-color: #fee2e2;
  border-radius: 4px;
}

.add-project {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.add-project input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.add-project input:disabled {
  background-color: #f5f5f5;
  cursor: not-allowed;
}

.add-project button {
  padding: 10px 20px;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  white-space: nowrap;
}

.add-project button:hover:not(:disabled) {
  background-color: #35a372;
}

.add-project button:disabled {
  background-color: #a0c4b0;
  cursor: not-allowed;
}

.projects-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.project-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background-color: #f8f9fa;
  border-radius: 4px;
  border-left: 4px solid #42b983;
  transition: all 0.2s ease;
}

.project-item:hover {
  background-color: #eef2f7;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

/* Стили для ссылки */
.project-link {
  flex: 1;
  text-decoration: none;
  color: inherit;
  display: block;
  cursor: pointer;
}

.project-link:hover .project-name {
  color: #3498db;
}

.project-item .project-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.project-item .project-name {
  font-size: 16px;
  font-weight: 500;
  color: #2c3e50;
  transition: color 0.2s ease;
}

.project-item .project-description {
  font-size: 14px;
  color: #7f8c8d;
}

.project-item .project-id {
  font-size: 12px;
  color: #95a5a6;
  font-weight: 400;
}

.project-actions {
  display: flex;
  gap: 8px;
  flex-shrink: 0;
  margin-left: 16px;
}

.project-actions button {
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
  transition: all 0.2s ease;
}

.project-actions button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.status-btn {
  background-color: #3498db;
  color: white;
}

.status-btn:hover:not(:disabled) {
  background-color: #2980b9;
  transform: scale(1.05);
}

.delete-btn {
  background-color: #e74c3c;
  color: white;
}

.delete-btn:hover:not(:disabled) {
  background-color: #c0392b;
  transform: scale(1.05);
}

.empty-message {
  text-align: center;
  color: #7f8c8d;
  font-style: italic;
  padding: 40px 0;
}

.stats {
  margin-top: 20px;
  padding: 15px;
  background-color: #ecf0f1;
  border-radius: 4px;
  display: flex;
  gap: 20px;
  justify-content: center;
}

.stats p {
  margin: 0;
  font-size: 14px;
  color: #2c3e50;
}

/* Адаптивность для мобильных устройств */
@media (max-width: 600px) {
  .add-project {
    flex-direction: column;
  }

  .project-item {
    flex-direction: column;
    align-items: stretch;
    padding: 12px;
  }

  .project-link {
    margin-bottom: 8px;
  }

  .project-actions {
    margin-left: 0;
    margin-top: 8px;
    justify-content: flex-end;
  }

  .stats {
    flex-direction: column;
    align-items: center;
  }
}
</style>
