// src/services/api.ts
import axios, {
  type AxiosError,
  type AxiosInstance,
  type AxiosRequestConfig,
  type AxiosResponse,
  type InternalAxiosRequestConfig,
} from 'axios'

import { tokenService } from './tokenService'

// Интерфейс для расширения конфига запроса
interface RetryRequestConfig extends InternalAxiosRequestConfig {
  _retry?: boolean
}

// Тип для очереди ожидающих запросов
type QueueItem = {
  resolve: (token: string) => void
  reject: (error: unknown) => void
}

class HttpClient {
  private client: AxiosInstance
  private isRefreshing = false
  private failedQueue: QueueItem[] = []

  constructor(baseURL: string) {
    this.client = axios.create({
      baseURL,
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json',
      },
    })

    this.setupInterceptors()
  }

  // --- Helpers для очереди ---
  private addToFailedQueue(item: QueueItem): void {
    this.failedQueue.push(item)
  }

  private processQueue(error?: unknown, token?: string): void {
    this.failedQueue.forEach(({ resolve, reject }) => {
      if (error) {
        reject(error)
      } else if (token) {
        resolve(token)
      }
    })
    this.failedQueue = []
  }

  // --- Логика обновления токена ---
  private async refreshAuthToken(): Promise<string> {
    // Берем refresh токен из сервиса
    const refreshToken = tokenService.refreshToken.value

    if (!refreshToken) {
      throw new Error('No refresh token available')
    }

    // Делаем запрос на обновление.
    // Важно: создаем отдельный инстанс или используем глобальный axios,
    // чтобы не попасть в рекурсию интерцепторов этого класса.
    const response = await axios.post(
      `${this.client.defaults.baseURL}/auth/refresh`,
      { refresh_token: refreshToken },
      {
        headers: { 'Content-Type': 'application/json' },
      },
    )

    const { access_token, refresh_token: newRefreshToken } = response.data

    // Предполагаем, что бэкенд возвращает expires_in (в секундах).
    // Если нет, можно поставить дефолтное значение, например 3600.
    const expiresIn = response.data.expires_in || 3600

    // Сохраняем через сервис (это обновит localStorage и реактивные переменные)
    tokenService.setTokens(access_token, newRefreshToken || refreshToken, expiresIn)

    return access_token
  }

  // --- Настройка интерцепторов ---
  private setupInterceptors(): void {
    // Request Interceptor
    this.client.interceptors.request.use(
      (config) => {
        // Берем токен из сервиса
        const token = tokenService.accessToken.value

        if (token) {
          config.headers.Authorization = `Bearer ${token}`
        }
        return config
      },
      (error) => Promise.reject(error),
    )

    // Response Interceptor
    this.client.interceptors.response.use(
      (response: AxiosResponse) => response,
      async (error: AxiosError) => {
        const originalRequest = error.config as RetryRequestConfig | undefined

        const isAuthError = error.response?.status === 401
        const isNotRetry = originalRequest && !originalRequest._retry
        // Проверяем, что это не запрос на refresh, чтобы избежать цикла
        const isNotRefreshCall =
          originalRequest?.url && !originalRequest.url.includes('/auth/refresh')

        if (isAuthError && isNotRetry && isNotRefreshCall) {
          originalRequest._retry = true

          if (this.isRefreshing) {
            return new Promise<string>((resolve, reject) => {
              this.addToFailedQueue({ resolve, reject })
            }).then((token) => {
              originalRequest.headers.set('Authorization', `Bearer ${token}`)
              return this.client(originalRequest)
            })
          }

          this.isRefreshing = true

          try {
            const newToken = await this.refreshAuthToken()
            this.processQueue(undefined, newToken)

            originalRequest.headers.set('Authorization', `Bearer ${newToken}`)
            return this.client(originalRequest)
          } catch (refreshError) {
            this.processQueue(refreshError)

            // Если refresh не удался, очищаем токены через сервис
            tokenService.clearTokens()

            // Пробрасываем ошибку дальше, чтобы её поймал глобальный обработчик или компонент
            throw refreshError
          } finally {
            this.isRefreshing = false
          }
        }

        return Promise.reject(error)
      },
    )
  }

  // --- Методы API ---
  async get<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.get<T>(url, config)
    return response.data
  }

  async post<T>(url: string, data?: unknown, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.post<T>(url, data, config)
    return response.data
  }

  async put<T>(url: string, data?: unknown, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.put<T>(url, data, config)
    return response.data
  }

  async patch<T>(url: string, data?: unknown, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.patch<T>(url, data, config)
    return response.data
  }

  async delete<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.delete<T>(url, config)
    return response.data
  }
}

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/kanban/'

export const httpClient = new HttpClient(API_BASE_URL)
