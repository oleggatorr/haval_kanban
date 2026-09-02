// src/composables/useAuth.ts
import { ref, computed, readonly } from 'vue'
import { authService } from '@/services/auth'
import { tokenService } from '@/services/tokenService'
import { storageService, STORAGE_KEYS } from '@/services/storage'
import type { UserProfile } from '@/types/user'
import type { LoginCredentials, LoginCredentials_ById, LoginResponse } from '@/types/auth'

export function useAuth() {
  // Реактивные состояния
  const user = ref<UserProfile | null>(authService.getCurrentUser())
  const isLoading = ref(false)
  const error = ref<string | null>(null)
  const isInitialized = ref(false)

  // Вычисляемые свойства
  const isAuthenticated = computed(() => {
    return tokenService.hasTokens() && !tokenService.isAccessTokenExpired()
  })

  const accessToken = computed(() => tokenService.accessToken.value)
  const refreshTokenValue = computed(() => tokenService.refreshToken.value) // ← переименовано

  // Приватные методы
  const handleAuthResponse = (response: LoginResponse) => {
    authService.saveAuthData(response)
    user.value = response.user || null
    error.value = null
  }

  const setError = (err: unknown) => {
    if (err instanceof Error) {
      error.value = err.message
    } else if (typeof err === 'string') {
      error.value = err
    } else {
      error.value = 'Произошла неизвестная ошибка'
    }
  }

  // Публичные методы
  /**
   * Вход в систему по логину/паролю
   */
  const login = async (credentials: LoginCredentials): Promise<boolean> => {
    isLoading.value = true
    error.value = null

    try {
      const response = await authService.login(credentials)
      handleAuthResponse(response)
      return true
    } catch (err) {
      setError(err)
      return false
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Вход по ID
   */
  const loginById = async (credentials: LoginCredentials_ById): Promise<boolean> => {
    isLoading.value = true
    error.value = null

    try {
      const response = await authService.loginById(credentials)
      handleAuthResponse(response)
      return true
    } catch (err) {
      setError(err)
      return false
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Выход из системы
   */
  const logout = async (redirectToLogin = true): Promise<void> => {
    isLoading.value = true
    error.value = null

    try {
      await authService.logout()
      user.value = null
    } catch (err) {
      setError(err)
    } finally {
      isLoading.value = false
      if (redirectToLogin && typeof window !== 'undefined') {
        window.location.href = '/login'
      }
    }
  }

  /**
   * Обновление токена
   */
  const refreshTokens = async (): Promise<boolean> => {
    // ← переименовано в refreshTokens
    isLoading.value = true
    error.value = null

    try {
      const refresh = tokenService.refreshToken.value
      if (!refresh) {
        throw new Error('Refresh token отсутствует')
      }

      // Используем httpClient напрямую, чтобы избежать цикла
      const { httpClient } = await import('@/services/api')
      const response = await httpClient.post<{
        access_token: string
        refresh_token?: string
        expires_in?: number
      }>('/auth/refresh', { refresh_token: refresh })

      const expiresIn = response.expires_in || 3600
      tokenService.setTokens(response.access_token, response.refresh_token || refresh, expiresIn)

      return true
    } catch (err) {
      setError(err)
      // Если обновление не удалось, разлогиниваем
      await logout(false)
      return false
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Загрузка профиля пользователя с сервера
   */
  const fetchUserProfile = async (): Promise<UserProfile | null> => {
    if (!isAuthenticated.value) return null

    isLoading.value = true
    error.value = null

    try {
      const profile = await authService.getCurrentUserFromServer()
      user.value = profile
      return profile
    } catch (err) {
      setError(err)
      return null
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Проверка валидности токена
   */
  const validateToken = async (): Promise<boolean> => {
    if (!isAuthenticated.value) return false

    try {
      const isValid = await authService.validateToken()
      if (!isValid) {
        // Если токен невалидный, пробуем обновить
        return await refreshTokens() // ← обновлено имя
      }
      return true
    } catch (err) {
      setError(err)
      return false
    }
  }

  /**
   * Проверка и автоматическое обновление токена при необходимости
   */
  const ensureValidToken = async (): Promise<boolean> => {
    if (!tokenService.hasTokens()) return false

    if (tokenService.isAccessTokenExpired()) {
      return await refreshTokens() // ← обновлено имя
    }

    return true
  }

  /**
   * Очистка ошибок
   */
  const clearError = () => {
    error.value = null
  }

  /**
   * Инициализация - проверка состояния при загрузке приложения
   */
  const initialize = async (): Promise<void> => {
    if (isInitialized.value) return

    isLoading.value = true

    try {
      // Проверяем, есть ли токены
      if (tokenService.hasTokens()) {
        // Если токен истек, пробуем обновить
        if (tokenService.isAccessTokenExpired()) {
          await refreshTokens() // ← обновлено имя
        }

        // Загружаем профиль пользователя
        await fetchUserProfile()
      }
    } catch (err) {
      console.error('Ошибка инициализации аутентификации:', err)
      // При ошибке очищаем все
      tokenService.clearTokens()
      storageService.remove(STORAGE_KEYS.USER_DATA)
      user.value = null
    } finally {
      isLoading.value = false
      isInitialized.value = true
    }
  }

  return {
    // Состояния
    user: readonly(user),
    isLoading: readonly(isLoading),
    error: readonly(error),
    isInitialized: readonly(isInitialized),
    isAuthenticated,

    // Токены (данные)
    accessToken,
    refreshToken: refreshTokenValue, // ← возвращаем переименованное значение

    // Методы
    login,
    loginById,
    logout,
    refreshTokens, // ← метод с новым именем
    fetchUserProfile,
    validateToken,
    ensureValidToken,
    clearError,
    initialize,
  }
}
