<!-- src/views/LoginView.vue -->
<template>
  <div class="login-container">
    <div class="login-card">
      <h1>Вход в систему</h1>

      <!-- Переключатель вкладок -->
      <div class="tabs">
        <button
          :class="['tab-btn', { active: loginMode === 'standard' }]"
          @click="switchMode('standard')"
        >
          По логину
        </button>
        <button
          :class="['tab-btn', { active: loginMode === 'by_id' }]"
          @click="switchMode('by_id')"
        >
          По ID сотрудника
        </button>
      </div>

      <form @submit.prevent="handleLogin" class="login-form">
        <!-- Режим: Стандартный вход (Логин + Пароль) -->
        <template v-if="loginMode === 'standard'">
          <AppInput
            v-model="credentials.username"
            label="Имя пользователя"
            placeholder="Введите логин"
            :error="errors.username"
            required
            autocomplete="username"
            :disabled="isLoading"
          >
            <template #prefix>👤</template>
          </AppInput>
        </template>

        <!-- Режим: Вход по ID (ID + Пароль) -->
        <template v-else>
          <AppInput
            v-model="credentials.employee_id"
            label="ID сотрудника"
            placeholder="Введите ID (например: gw07012345  |  000012345)"
            :error="errors.employee_id"
            required
            autocomplete="username"
            :disabled="isLoading"
            type="text"
          >
            <template #prefix>🆔</template>
          </AppInput>
        </template>

        <!-- Поле Пароля (общее для обоих режимов) -->
        <AppInput
          v-model="credentials.password"
          :type="showPassword ? 'text' : 'password'"
          label="Пароль"
          placeholder="Введите пароль"
          :error="errors.password"
          required
          autocomplete="current-password"
          :disabled="isLoading"
        >
          <template #suffix>
            <button
              type="button"
              @click="togglePasswordVisibility"
              class="password-toggle"
              title="Показать/скрыть пароль"
              :disabled="isLoading"
            >
              {{ showPassword ? '🙈' : '🙉' }}
            </button>
          </template>
        </AppInput>

        <!-- Кнопка входа -->
        <AppButton
          type="submit"
          variant="primary"
          size="lg"
          :loading="isLoading"
          class="submit-btn"
        >
          Войти в систему
        </AppButton>

        <!-- Сообщение об ошибке -->
        <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuth } from '@/composables/useAuth'
import AppInput from '@/components/common/AppInput.vue'
import AppButton from '@/components/common/AppButton.vue'

const router = useRouter()
const route = useRoute()

// Используем композабл
const { login, loginById, isLoading, error, clearError, fetchUserProfile, isAuthenticated } =
  useAuth()

// Типы входа
type LoginMode = 'standard' | 'by_id'

// Состояния формы
const loginMode = ref<LoginMode>('standard')
const showPassword = ref(false)

// Ошибки полей
const errors = ref<{
  username?: string
  employee_id?: string
  password?: string
}>({})

// Данные формы (реактивный объект)
const credentials = reactive({
  username: '',
  employee_id: '',
  password: '',
})

// Вычисляемое сообщение об ошибке
const errorMessage = computed(() => {
  // Если есть ошибка от композабла, показываем её
  if (error.value) {
    return error.value
  }

  // Локальные ошибки валидации
  if (errors.value.username || errors.value.employee_id || errors.value.password) {
    return 'Пожалуйста, исправьте ошибки в форме'
  }

  return ''
})

const togglePasswordVisibility = () => {
  showPassword.value = !showPassword.value
}

// Переключение вкладок с очисткой полей
const switchMode = (mode: LoginMode) => {
  loginMode.value = mode
  errors.value = {}
  clearError()
  credentials.username = ''
  credentials.employee_id = ''
  credentials.password = ''
}

// Валидация формы
const validateForm = (): boolean => {
  errors.value = {}
  let isValid = true

  if (loginMode.value === 'standard') {
    if (!credentials.username.trim()) {
      errors.value.username = 'Логин обязателен'
      isValid = false
    }
  } else {
    if (!credentials.employee_id.trim()) {
      errors.value.employee_id = 'ID сотрудника обязателен'
      isValid = false
    }
  }

  if (!credentials.password) {
    errors.value.password = 'Пароль обязателен'
    isValid = false
  }

  return isValid
}

// Обработка входа
const handleLogin = async () => {
  // Очищаем предыдущие ошибки
  errors.value = {}
  clearError()

  // Валидация
  if (!validateForm()) return

  let success = false

  try {
    if (loginMode.value === 'standard') {
      // Стандартный вход
      success = await login({
        login: credentials.username.trim(),
        password: credentials.password,
      })
    } else {
      // Вход по ID
      success = await loginById({
        employee_id: credentials.employee_id.trim(),
        password: credentials.password,
      })
    }

    if (success) {
      // Загружаем данные пользователя
      await fetchUserProfile()

      // Перенаправляем пользователя
      const redirectPath = (route.query.redirect as string) || '/dashboard'
      await router.push(redirectPath)
    }
  } catch (err) {
    // Ошибки обрабатываются внутри композабла
    // Дополнительная обработка для конкретных случаев
    if (err instanceof Error) {
      // Можно добавить специфичную обработку
      console.error('Login error:', err.message)
    }
  }
}

// Проверка, авторизован ли пользователь при загрузке
// Если да - перенаправляем на главную
if (isAuthenticated.value) {
  router.replace('/dashboard')
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 70vh;
  /* background-color: #f5f7fa; */
}

.login-card {
  background: white;
  padding: 2.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  width: 100%;
  max-width: 420px;
}

h1 {
  text-align: center;
  margin-bottom: 1.5rem;
  color: #333;
}

.tabs {
  display: flex;
  margin-bottom: 1.5rem;
  border-bottom: 2px solid #eee;
}

.tab-btn {
  flex: 1;
  padding: 10px;
  background: none;
  border: none;
  cursor: pointer;
  font-weight: 600;
  color: #888;
  transition: all 0.3s;
  border-bottom: 2px solid transparent;
  margin-bottom: -2px;
}

.tab-btn.active {
  color: #4a90d9;
  border-bottom-color: #4a90d9;
}

.tab-btn:hover:not(.active) {
  color: #555;
  background-color: #f9f9f9;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.password-toggle {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 16px;
  padding: 0;
  opacity: 0.7;
}

.password-toggle:hover {
  opacity: 1;
}

.submit-btn {
  margin-top: 10px;
  height: 30px;
}

.error-message {
  color: #dc2626;
  text-align: center;
  font-size: 0.9rem;
  margin-top: 10px;
  background-color: #fee2e2;
  padding: 8px;
  border-radius: 4px;
}
</style>
