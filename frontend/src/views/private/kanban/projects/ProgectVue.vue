<!-- src/views/ProjectPage.vue -->
<template>
  <div class="project-page">
    <!-- Загрузка -->
    <div v-if="loading" class="loading">
      <p>Загрузка проекта...</p>
    </div>

    <!-- Ошибка -->
    <div v-else-if="error" class="error">
      <p>{{ error }}</p>
      <button @click="$router.push('/projects')">Вернуться к списку</button>
    </div>

    <!-- Детали проекта -->
    <div v-else-if="project" class="project-content">
      <!-- Шапка с навигацией -->
      <div class="project-header">
        <button @click="$router.push('/projects')" class="back-btn">← Назад к списку</button>
        <div class="header-actions">
          <button @click="goToBoard" class="board-btn">📊 Открыть доску</button>
          <button @click="editMode = !editMode" class="edit-toggle-btn">
            {{ editMode ? 'Отмена' : 'Редактировать' }}
          </button>
          <button @click="deleteProject" class="delete-btn">Удалить проект</button>
        </div>
      </div>

      <!-- Информация о проекте -->
      <div class="project-info">
        <!-- Режим редактирования -->
        <div v-if="editMode" class="edit-form">
          <h2>Редактирование проекта</h2>
          <div class="form-group">
            <label>Название проекта</label>
            <input v-model="editProject.name" type="text" />
          </div>
          <div class="form-group">
            <label>Описание</label>
            <textarea v-model="editProject.description" rows="4"></textarea>
          </div>
          <button @click="saveProject" class="save-btn">Сохранить изменения</button>
        </div>

        <!-- Режим просмотра -->
        <div v-else>
          <div class="project-title">
            <h1>{{ project.name }}</h1>
            <span :class="['status-badge', project.status || 'active']">
              {{ getStatusText(project.status || 'active') }}
            </span>
          </div>

          <div class="project-meta">
            <p><strong>ID:</strong> {{ project.id }}</p>
            <p><strong>Создан:</strong> {{ formatDate(project.createdAt) }}</p>
            <p v-if="project.completedAt">
              <strong>Завершен:</strong> {{ formatDate(project.completedAt) }}
            </p>
          </div>

          <div class="project-description" v-if="project.description">
            <h3>Описание</h3>
            <p>{{ project.description }}</p>
          </div>

          <!-- Кнопка перехода на доску в режиме просмотра -->
          <div class="board-shortcut">
            <button @click="goToBoard" class="board-shortcut-btn">
              <span class="board-icon">📋</span>
              <span>Перейти к канбан-доске</span>
              <span class="arrow-icon">→</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { httpClient } from '@/services/api'

// Типы
interface Project {
  id: number
  name: string
  description?: string
  status?: 'active' | 'completed' | 'paused'
  createdAt?: string
  completedAt?: string | null
}

interface Task {
  id: number
  text: string
  completed: boolean
}

// Composables
const route = useRoute()
const router = useRouter()

// Состояния
const loading = ref(true)
const error = ref<string | null>(null)
const project = ref<Project | null>(null)
const tasks = ref<Task[]>([])
const editMode = ref(false)
const newTaskText = ref('')

// Редактируемый проект
const editProject = ref<Project>({
  id: 0,
  name: '',
  description: '',
  status: 'active',
})

// Вычисляемые свойства
const completedTasksCount = computed(() => {
  return tasks.value.filter((t) => t.completed).length
})

// Методы
const getProjectId = (): number => {
  const id = route.params.id
  return typeof id === 'string' ? parseInt(id, 10) : Number(id)
}

const goToBoard = () => {
  if (!project.value) return
  // Переход на страницу доски с ID проекта
  router.push(`/project/${project.value.id}/board`)
}

const fetchProject = async (id: number) => {
  loading.value = true
  error.value = null

  try {
    // Получаем проект с сервера
    const response = await httpClient.get<Project>(`/project/${id}`)

    project.value = {
      ...response,
      status: response.status || 'active',
      createdAt: response.createdAt || new Date().toISOString(),
    }

    // Копируем в редактируемую версию
    editProject.value = { ...project.value }

    // Загружаем задачи (если есть отдельный эндпоинт)
    await fetchTasks(id)

    console.log('✅ Проект загружен:', project.value)
  } catch (err) {
    console.error('❌ Ошибка загрузки проекта:', err)

    if (err instanceof Error && err.message.includes('404')) {
      error.value = 'Проект не найден'
    } else {
      error.value = 'Не удалось загрузить проект'
    }
  } finally {
    loading.value = false
  }
}

const fetchTasks = async (projectId: number) => {
  try {
    // Если есть эндпоинт для задач проекта
    // const response = await httpClient.get<Task[]>(`/project/${projectId}/tasks`)
    // tasks.value = response

    // Пока используем тестовые данные
    tasks.value = [
      { id: 1, text: 'Создать дизайн', completed: true },
      { id: 2, text: 'Написать код', completed: false },
      { id: 3, text: 'Протестировать', completed: false },
    ]
  } catch (err) {
    console.error('Ошибка загрузки задач:', err)
    tasks.value = []
  }
}

const saveProject = async () => {
  if (!project.value) return

  loading.value = true
  error.value = null

  try {
    // Отправляем обновленные данные на сервер
    const updatedProject = await httpClient.put<Project>(`/project/${project.value.id}`, {
      name: editProject.value.name,
      description: editProject.value.description,
      status: editProject.value.status,
    })

    // Обновляем локальный проект
    project.value = {
      ...project.value,
      ...updatedProject,
    }

    editMode.value = false
    console.log('✅ Проект обновлен:', project.value)
  } catch (err) {
    console.error('❌ Ошибка обновления проекта:', err)
    error.value = 'Не удалось сохранить изменения'
  } finally {
    loading.value = false
  }
}

const deleteProject = async () => {
  if (!project.value) return

  if (!confirm('Вы уверены, что хотите удалить этот проект?')) {
    return
  }

  loading.value = true
  error.value = null

  try {
    await httpClient.delete(`/project/${project.value.id}`)
    console.log('✅ Проект удален:', project.value.id)
    router.push('/projects')
  } catch (err) {
    console.error('❌ Ошибка удаления проекта:', err)
    error.value = 'Не удалось удалить проект'
    loading.value = false
  }
}

const addTask = async () => {
  if (!newTaskText.value.trim() || !project.value) return

  try {
    // Отправляем запрос на создание задачи
    // const newTask = await httpClient.post<Task>(`/project/${project.value.id}/tasks`, {
    //   text: newTaskText.value.trim(),
    // })
    // tasks.value.push(newTask)

    // Временное решение без бэкенда
    tasks.value.push({
      id: Date.now(),
      text: newTaskText.value.trim(),
      completed: false,
    })

    newTaskText.value = ''
    console.log('✅ Задача добавлена')
  } catch (err) {
    console.error('❌ Ошибка добавления задачи:', err)
    error.value = 'Не удалось добавить задачу'
  }
}

const deleteTask = async (taskId: number) => {
  try {
    // Отправляем запрос на удаление задачи
    // await httpClient.delete(`/tasks/${taskId}`)

    tasks.value = tasks.value.filter((t) => t.id !== taskId)
    console.log('✅ Задача удалена:', taskId)
  } catch (err) {
    console.error('❌ Ошибка удаления задачи:', err)
    error.value = 'Не удалось удалить задачу'
  }
}

const updateTask = async (task: Task) => {
  try {
    // Отправляем запрос на обновление задачи
    // await httpClient.patch(`/tasks/${task.id}`, {
    //   completed: task.completed,
    // })
    console.log('✅ Задача обновлена:', task)
  } catch (err) {
    console.error('❌ Ошибка обновления задачи:', err)
    error.value = 'Не удалось обновить задачу'
  }
}

const getStatusText = (status: string): string => {
  const map: Record<string, string> = {
    active: 'Активный',
    completed: 'Завершен',
    paused: 'Приостановлен',
  }
  return map[status] || status
}

const formatDate = (dateString?: string | null): string => {
  if (!dateString) return '—'
  try {
    const date = new Date(dateString)
    return date.toLocaleDateString('ru-RU', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    })
  } catch {
    return '—'
  }
}

// Жизненный цикл
onMounted(() => {
  const id = getProjectId()
  if (id) {
    fetchProject(id)
  } else {
    error.value = 'Неверный ID проекта'
    loading.value = false
  }
})
</script>

<style scoped>
.project-page {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
}

.loading,
.error {
  text-align: center;
  padding: 40px;
  font-size: 18px;
}

.error {
  color: #e74c3c;
}

.error button {
  margin-top: 20px;
  padding: 10px 20px;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.error button:hover {
  background-color: #2980b9;
}

.project-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #ecf0f1;
}

.back-btn {
  padding: 8px 16px;
  background-color: #ecf0f1;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.back-btn:hover {
  background-color: #d5dbdb;
}

.header-actions {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  align-items: center;
}

.board-btn {
  padding: 8px 16px;
  background-color: #6c5ce7;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.2s;
  display: flex;
  align-items: center;
  gap: 6px;
}

.board-btn:hover {
  background-color: #5a4bd1;
}

.edit-toggle-btn {
  padding: 8px 16px;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.edit-toggle-btn:hover {
  background-color: #2980b9;
}

.delete-btn {
  padding: 8px 16px;
  background-color: #e74c3c;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.delete-btn:hover {
  background-color: #c0392b;
}

.project-info {
  background-color: #f8f9fa;
  padding: 24px;
  border-radius: 8px;
  margin-bottom: 30px;
}

.project-title {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 20px;
}

.project-title h1 {
  margin: 0;
  color: #2c3e50;
}

.status-badge {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: bold;
  text-transform: uppercase;
}

.status-badge.active {
  background-color: #27ae60;
  color: white;
}

.status-badge.completed {
  background-color: #3498db;
  color: white;
}

.status-badge.paused {
  background-color: #f39c12;
  color: white;
}

.project-meta {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 10px;
  margin-bottom: 20px;
}

.project-meta p {
  margin: 0;
  color: #7f8c8d;
}

.project-description {
  margin-top: 15px;
  padding-top: 15px;
  border-top: 1px solid #ecf0f1;
}

.project-description h3 {
  margin: 0 0 10px 0;
  color: #2c3e50;
}

.project-description p {
  margin: 0;
  line-height: 1.6;
  color: #34495e;
}

/* Кнопка перехода на доску */
.board-shortcut {
  margin-top: 24px;
  padding-top: 20px;
  border-top: 2px dashed #d5dbdb;
}

.board-shortcut-btn {
  width: 100%;
  padding: 16px 24px;
  background: linear-gradient(135deg, #6c5ce7, #a29bfe);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
  font-weight: 500;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  transition: all 0.3s ease;
}

.board-shortcut-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(108, 92, 231, 0.4);
}

.board-shortcut-btn:active {
  transform: translateY(0);
}

.board-icon {
  font-size: 24px;
}

.arrow-icon {
  font-size: 20px;
  transition: transform 0.3s ease;
}

.board-shortcut-btn:hover .arrow-icon {
  transform: translateX(4px);
}

/* Режим редактирования */
.edit-form {
  max-width: 500px;
}

.edit-form h2 {
  margin: 0 0 20px 0;
  color: #2c3e50;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
  color: #2c3e50;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  font-family: inherit;
}

.form-group textarea {
  resize: vertical;
}

.save-btn {
  padding: 10px 24px;
  background-color: #27ae60;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

.save-btn:hover {
  background-color: #229954;
}

/* Задачи */
.project-tasks {
  background-color: #f8f9fa;
  padding: 24px;
  border-radius: 8px;
}

.project-tasks h3 {
  margin: 0 0 20px 0;
  color: #2c3e50;
}

.add-task {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.add-task input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.add-task input:disabled {
  background-color: #f5f5f5;
  cursor: not-allowed;
}

.add-task button {
  padding: 10px 20px;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.add-task button:hover:not(:disabled) {
  background-color: #35a372;
}

.add-task button:disabled {
  background-color: #a0c4b0;
  cursor: not-allowed;
}

.tasks-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.task-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 14px;
  background-color: white;
  border-radius: 4px;
  border: 1px solid #ecf0f1;
}

.task-item input[type='checkbox'] {
  width: 18px;
  height: 18px;
  cursor: pointer;
}

.task-item span {
  flex: 1;
  font-size: 14px;
}

.task-item span.completed {
  text-decoration: line-through;
  color: #95a5a6;
}

.task-delete-btn {
  background: none;
  border: none;
  color: #e74c3c;
  cursor: pointer;
  font-size: 18px;
  padding: 0 5px;
}

.task-delete-btn:hover {
  color: #c0392b;
}

.empty-tasks {
  text-align: center;
  color: #95a5a6;
  font-style: italic;
}

.tasks-stats {
  margin-top: 15px;
  padding-top: 15px;
  border-top: 1px solid #ecf0f1;
  color: #7f8c8d;
  font-size: 14px;
}

/* Адаптивность */
@media (max-width: 600px) {
  .project-header {
    flex-direction: column;
    gap: 10px;
    align-items: stretch;
  }

  .header-actions {
    flex-direction: column;
  }

  .project-title {
    flex-direction: column;
    align-items: flex-start;
  }

  .project-meta {
    grid-template-columns: 1fr;
  }

  .add-task {
    flex-direction: column;
  }

  .board-shortcut-btn {
    font-size: 14px;
    padding: 14px 20px;
  }
}
</style>
