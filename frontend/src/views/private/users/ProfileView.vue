<script setup lang="ts">
import { useAuth } from '@/composables/useAuth'
import { useDepartment } from '@/composables/useDepartment' // Импортируем новый composable
import { computed } from 'vue'

const auth = useAuth()

// Получаем GUID департамента из профиля пользователя
// Важно: передаем computed-ссылку, чтобы composable следил за изменениями
const departmentGuid = computed(() => auth.user?.department_guid || null)

// Используем composable для загрузки данных департамента
const { department: deptInfo, loading: deptLoading } = useDepartment(departmentGuid)

// Форматирование даты
const formatDate = (dateString: string | null | undefined): string => {
  if (!dateString) return '—'
  const date = new Date(dateString)
  if (isNaN(date.getTime())) return '—'

  return date.toLocaleDateString('ru-RU', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
}

// Форматирование даты и времени
const formatDateTime = (dateString: string | null | undefined): string => {
  if (!dateString) return '—'
  const date = new Date(dateString)
  if (isNaN(date.getTime())) return '—'

  return date.toLocaleString('ru-RU', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

const currentUser = computed(() => auth.user)

const fullNameRu = computed(() => {
  const user = currentUser.value
  if (!user) return ''
  return `${user.last_name || ''} ${user.first_name || ''} ${user.middle_name || ''}`.trim()
})

const fullNameEn = computed(() => {
  const user = currentUser.value
  if (!user) return ''
  return `${user.last_name_en || ''} ${user.first_name_en || ''} ${user.middle_name_en || ''}`.trim()
})

const permissionsList = computed(() => {
  const user = currentUser.value
  if (!user?.permissions) return []
  return Object.keys(user.permissions)
})

const statusText = computed(() => {
  return auth.isActive.value ? 'Активен' : 'Неактивен'
})

const statusClass = computed(() => {
  return auth.isActive.value ? 'status-active' : 'status-inactive'
})

const handleRefresh = async () => {
  try {
    await auth.refreshUserData()
  } catch (e) {
    console.error('Ошибка обновления:', e)
  }
}
</script>

<template>
  <div class="profile-page">
    <div class="profile-header">
      <h1>Профиль пользователя</h1>
      <button @click="handleRefresh" :disabled="auth.loading" class="refresh-btn">
        {{ auth.loading ? 'Обновление...' : 'Обновить данные' }}
      </button>
    </div>

    <div v-if="auth.error" class="error-message">
      {{ auth.error }}
    </div>

    <div v-if="currentUser" class="profile-content">
      <!-- Основная информация -->
      <section class="profile-section">
        <h2>Основная информация</h2>
        <div class="info-grid">
          <div class="info-item">
            <label>ФИО (русский):</label>
            <span>{{ fullNameRu }}</span>
          </div>
          <div class="info-item">
            <label>ФИО (английский):</label>
            <span>{{ fullNameEn }}</span>
          </div>
          <div class="info-item">
            <label>Логин:</label>
            <span>{{ currentUser.login }}</span>
          </div>
          <div class="info-item">
            <label>ID сотрудника:</label>
            <span>{{ currentUser.employee_id }}</span>
          </div>
          <div class="info-item">
            <label>Статус:</label>
            <span :class="statusClass">{{ statusText }}</span>
          </div>
        </div>
      </section>

      <!-- Контактная информация -->
      <section class="profile-section">
        <h2>Контактная информация</h2>
        <div class="info-grid">
          <div class="info-item">
            <label>Email:</label>
            <span>{{ currentUser.email }}</span>
          </div>
          <div class="info-item">
            <label>Телефон:</label>
            <span>{{ currentUser.phone }}</span>
          </div>
        </div>
      </section>

      <!-- Даты -->
      <section class="profile-section">
        <h2>Даты</h2>
        <div class="info-grid">
          <div class="info-item">
            <label>Дата рождения:</label>
            <span>{{ formatDate(currentUser.birth_date) }}</span>
          </div>
          <div class="info-item">
            <label>Дата приема на работу:</label>
            <span>{{ formatDate(currentUser.employment_date) }}</span>
          </div>
          <div class="info-item">
            <label>Дата увольнения:</label>
            <span>{{ formatDate(currentUser.dismissal_date) }}</span>
          </div>
          <div class="info-item">
            <label>Последний вход:</label>
            <span>{{ formatDateTime(currentUser.last_login) }}</span>
          </div>
          <div class="info-item">
            <label>Дата создания записи:</label>
            <span>{{ formatDateTime(currentUser.created_at) }}</span>
          </div>
          <div class="info-item">
            <label>Последнее обновление:</label>
            <span>{{ formatDateTime(currentUser.updated_at) }}</span>
          </div>
        </div>
      </section>

      <!-- Идентификаторы -->
      <section class="profile-section">
        <h2>Идентификаторы</h2>
        <div class="info-grid">
          <div class="info-item">
            <label>GUID пользователя:</label>
            <span class="guid">{{ currentUser.guid }}</span>
          </div>
          <div class="info-item">
            <label>GUID персоны:</label>
            <span class="guid">{{ currentUser.guid_person }}</span>
          </div>
          <div class="info-item">
            <label>GUID должности:</label>
            <span class="guid">{{ currentUser.position_guid }}</span>
          </div>

          <!-- ИЗМЕНЕННАЯ ЧАСТЬ: Вывод названия департамента -->
          <div class="info-item">
            <label>Департамент:</label>
            <span v-if="deptLoading" class="loading-text">Загрузка...</span>
            <span v-else-if="deptInfo">
              {{ deptInfo.name }}
              <small>({{ deptInfo.short_name }})</small>
            </span>
            <span v-else-if="currentUser.department_guid">
              {{ currentUser.department_guid }}
            </span>
            <span v-else>—</span>
          </div>
        </div>
      </section>

      <!-- Разрешения -->
      <section class="profile-section">
        <h2>Разрешения ({{ permissionsList.length }})</h2>
        <div v-if="permissionsList.length > 0" class="permissions-list">
          <div v-for="permission in permissionsList" :key="permission" class="permission-item">
            {{ permission }}
          </div>
        </div>
        <div v-else class="no-permissions">Нет назначенных разрешений</div>
      </section>
    </div>

    <div v-else-if="auth.loading" class="loading-state">
      <p>Загрузка данных профиля...</p>
    </div>

    <div v-else class="loading-state">
      <p>Данные пользователя недоступны. Пожалуйста, войдите в систему.</p>
    </div>
  </div>
</template>

<style scoped>
/* Стили остались без изменений */
.profile-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.profile-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #e0e0e0;
}

.profile-header h1 {
  margin: 0;
  color: #333;
}

.refresh-btn {
  padding: 0.5rem 1.5rem;
  background-color: #4a90d9;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.2s;
}

.refresh-btn:hover:not(:disabled) {
  background-color: #357abd;
}

.refresh-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.error-message {
  background-color: #fee;
  color: #c33;
  padding: 1rem;
  border-radius: 4px;
  margin-bottom: 1.5rem;
  border-left: 4px solid #c33;
}

.profile-content {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.profile-section {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.profile-section h2 {
  margin-top: 0;
  margin-bottom: 1.5rem;
  color: #444;
  font-size: 1.25rem;
  border-bottom: 1px solid #eee;
  padding-bottom: 0.5rem;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1rem;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.info-item label {
  font-weight: 600;
  color: #666;
  font-size: 0.875rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.info-item span {
  color: #333;
  font-size: 1rem;
  word-break: break-word;
}

.guid {
  font-family: 'Courier New', monospace;
  font-size: 0.875rem;
  background-color: #f5f5f5;
  padding: 0.25rem 0.5rem;
  border-radius: 3px;
}

.status-active {
  color: #2e7d32;
  font-weight: 600;
}

.status-inactive {
  color: #c62828;
  font-weight: 600;
}

.permissions-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.permission-item {
  background-color: #e3f2fd;
  color: #1565c0;
  padding: 0.5rem 1rem;
  border-radius: 16px;
  font-size: 0.875rem;
  font-family: 'Courier New', monospace;
}

.no-permissions {
  color: #999;
  font-style: italic;
}

.loading-state {
  text-align: center;
  padding: 3rem;
  color: #666;
  font-size: 1.125rem;
}
</style>
