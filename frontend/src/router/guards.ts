// src/router/guards.ts
import type { Router, RouteLocationNormalizedGeneric } from 'vue-router'
import { tokenService } from '@/services/tokenService'
import { authService } from '@/services/auth'

/**
 * Guard для проверки аутентификации
 */
export function setupAuthGuards(router: Router) {
  router.beforeEach(async (to, from) => {
    // Устанавливаем заголовок страницы
    if (to.meta.title) {
      document.title = `${to.meta.title} | My Project`
    } else {
      document.title = 'My Project'
    }

    // Проверяем требуется ли аутентификация
    if (to.meta.requiresAuth) {
      // Проверяем наличие и валидность токенов
      const hasValidToken = await validateAuth()

      if (!hasValidToken) {
        // Сохраняем путь для возврата после логина
        return {
          name: 'login',
          query: { redirect: to.fullPath },
        }
      }
    }

    // Если пользователь уже авторизован и пытается зайти на login
    if (to.name === 'login' && tokenService.hasTokens()) {
      const isValid = await validateAuth()
      if (isValid) {
        // Перенаправляем на сохраненный путь или на главную
        const redirect = (to.query.redirect as string) || '/'
        return { path: redirect }
      }
    }

    // Разрешаем навигацию
    return true
  })
}

/**
 * Проверка валидности токена с возможностью обновления
 */
async function validateAuth(): Promise<boolean> {
  // Нет токенов вообще
  if (!tokenService.hasTokens()) {
    return false
  }

  // Access token валиден
  if (!tokenService.isAccessTokenExpired()) {
    return true
  }

  // Access token истек, пробуем обновить
  try {
    const refresh = tokenService.refreshToken.value

    if (!refresh) {
      throw new Error('No refresh token')
    }

    // Импортируем httpClient динамически чтобы избежать циклических зависимостей
    const { httpClient } = await import('@/services/api')

    const response = await httpClient.post<{
      access_token: string
      refresh_token?: string
      expires_in?: number
    }>('/auth/refresh', {
      refresh_token: refresh,
    })

    // Сохраняем новые токены
    const expiresIn = response.data.expires_in || 3600
    tokenService.setTokens(
      response.data.access_token,
      response.data.refresh_token || refresh,
      expiresIn,
    )

    return true
  } catch (error) {
    console.error('Failed to refresh token:', error)

    // Очистка при ошибке
    tokenService.clearTokens()
    authService.clearUserData()

    return false
  }
}
