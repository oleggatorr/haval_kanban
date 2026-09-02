import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router' // Используем роутер для навигации
import { httpClient } from '@/services/api'
import type { UserProfile } from '@/types/user'
import type { LoginResponse } from '@/types/auth'

export const useAuthStore = defineStore('auth', () => {
  const router = useRouter() // Получаем экземпляр роутера

  // ==================== СОСТОЯНИЕ ====================
  const user = ref<UserProfile | null>(null)
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  // Вычисляемое свойство: авторизован ли пользователь
  const isAuthenticated = computed(() => !!user.value)

  // ==================== МЕТОДЫ ====================

  /**
   * Инициализация состояния из localStorage
   * Вызывайте этот метод в main.ts или App.vue при старте
   */
  const initFromStorage = () => {
    const userData = localStorage.getItem('user_data')
    if (userData) {
      try {
        user.value = JSON.parse(userData)
      } catch (e) {
        console.error('Ошибка парсинга user_data:', e)
        clearStorage()
      }
    }
  }

  /**
   * Очистка хранилища
   */
  const clearStorage = () => {
    localStorage.removeItem('auth_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user_data')
    user.value = null
    error.value = null
  }

  /**
   * Вход в систему
   */
  const login = async (credentials: { username: string; password: string }): Promise<void> => {
    isLoading.value = true
    error.value = null

    try {
      // httpClient сам подставит Content-Type и обработает ошибки
      const response = await httpClient.post<LoginResponse>('/auth/login', credentials)

      // Сохраняем токены (httpClient интерцепторы будут их использовать)
      localStorage.setItem('auth_token', response.access_token)
      localStorage.setItem('refresh_token', response.refresh_token)

      // Обновляем реактивное состояние
      user.value = response.user

      // Сохраняем профиль для персистентности после перезагрузки
      localStorage.setItem('user_data', JSON.stringify(response.user))
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Ошибка входа'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Загрузка актуальных данных пользователя с сервера (/auth/me)
   */
  const loadUserData = async (): Promise<void> => {
    // Проверка наличия токена перед запросом
    if (!localStorage.getItem('auth_token')) {
      throw new Error('Токен отсутствует')
    }

    isLoading.value = true
    try {
      // httpClient сам добавит заголовок Authorization!
      const response = await httpClient.get<UserProfile>('/auth/me')

      user.value = response
      localStorage.setItem('user_data', JSON.stringify(response))
    } catch (err: any) {
      console.error('Ошибка загрузки данных пользователя:', err)
      // Если ошибка критическая (например, 401 и refresh не помог), выходим
      logout()
      throw err
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Выход из системы
   */
  const logout = () => {
    clearStorage()

    // Используем роутер для плавного перехода без перезагрузки страницы
    if (router.currentRoute.value.path !== '/login') {
      router.push('/login')
    }
  }

  /**
   * Проверка валидности сессии (опционально, если нужно проверить токен без загрузки профиля)
   */
  const validateSession = async (): Promise<boolean> => {
    const token = localStorage.getItem('auth_token')
    if (!token) return false

    try {
      // httpClient сам добавит заголовок
      await httpClient.get('/auth/validate_token')
      return true
    } catch {
      return false
    }
  }

  return {
    user,
    isAuthenticated,
    isLoading,
    error,
    login,
    logout,
    loadUserData,
    validateSession,
    initFromStorage,
  }
})
