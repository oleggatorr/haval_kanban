// useApi.ts
import { readonly, ref, shallowRef } from 'vue'
import { createApiService } from './service'
import type { ApiConfig, ApiError } from './types'

export function useApi(config: ApiConfig = { baseUrl: '' }) {
  const service = createApiService(config)

  const loading = ref(false)
  const error = shallowRef<ApiError | null>(null)

  /** Обёртка над любым вызовом сервиса — включает loading/error */
  async function call<T>(fn: () => Promise<T>): Promise<T> {
    loading.value = true
    error.value = null
    try {
      return await fn()
    } catch (e) {
      error.value = e as ApiError
      throw e
    } finally {
      loading.value = false
    }
  }

  return {
    get: <T = unknown>(...args: Parameters<typeof service.get>) =>
      call(() => service.get<T>(...args)),
    post: <T = unknown, B = unknown>(...args: Parameters<typeof service.post>) =>
      call(() => service.post<T, B>(...args)),
    put: <T = unknown, B = unknown>(...args: Parameters<typeof service.put>) =>
      call(() => service.put<T, B>(...args)),
    patch: <T = unknown, B = unknown>(...args: Parameters<typeof service.patch>) =>
      call(() => service.patch<T, B>(...args)),
    delete: <T = unknown>(...args: Parameters<typeof service.delete>) =>
      call(() => service.delete<T>(...args)),

    // прямой доступ к сервису, если нужно без loading
    service,
    loading: readonly(loading),
    error: readonly(error),
  }
}
