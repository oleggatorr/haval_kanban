// src\composables\useApi.ts

import { ref } from 'vue'
import { httpClient } from '@/services/api'
import type { AxiosRequestConfig } from 'axios'

// Универсальный интерфейс для результата запроса
interface UseApiResult<T> {
  data: T | null
  loading: boolean
  error: string | null
  execute: (...args: any[]) => Promise<T | void>
}

export function useApi<T = any>() {
  const data = ref<T | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  /**
   * Универсальная функция выполнения запроса
   * @param method - метод httpClient (get, post, put, patch, delete)
   * @param url - URL endpoint
   * @param options - опции запроса (data, config)
   */
  const execute = async (
    method: 'get' | 'post' | 'put' | 'patch' | 'delete',
    url: string,
    options?: {
      payload?: unknown
      config?: AxiosRequestConfig
    },
  ): Promise<T | void> => {
    loading.value = true
    error.value = null

    try {
      let response: T

      // Динамический вызов метода httpClient
      switch (method) {
        case 'get':
          response = await httpClient.get<T>(url, options?.config)
          break
        case 'post':
          response = await httpClient.post<T>(url, options?.payload, options?.config)
          break
        case 'put':
          response = await httpClient.put<T>(url, options?.payload, options?.config)
          break
        case 'patch':
          response = await httpClient.patch<T>(url, options?.payload, options?.config)
          break
        case 'delete':
          response = await httpClient.delete<T>(url, options?.config)
          break
        default:
          throw new Error(`Unsupported method: ${method}`)
      }

      data.value = response
      return response
    } catch (e: any) {
      // Безопасное получение сообщения об ошибке
      error.value =
        e.response?.data?.detail || e.message || 'Произошла ошибка при выполнении запроса'
      throw e // Пробрасываем ошибку дальше, чтобы компонент мог её обработать если нужно
    } finally {
      loading.value = false
    }
  }

  // Хелперы для конкретных методов (для удобства использования)
  const get = (url: string, config?: AxiosRequestConfig) => execute('get', url, { config })

  const post = (url: string, payload?: unknown, config?: AxiosRequestConfig) =>
    execute('post', url, { payload, config })

  const put = (url: string, payload?: unknown, config?: AxiosRequestConfig) =>
    execute('put', url, { payload, config })

  const patch = (url: string, payload?: unknown, config?: AxiosRequestConfig) =>
    execute('patch', url, { payload, config })

  const del = (url: string, config?: AxiosRequestConfig) => execute('delete', url, { config })

  return {
    data,
    loading,
    error,
    execute,
    get,
    post,
    put,
    patch,
    del,
  }
}
