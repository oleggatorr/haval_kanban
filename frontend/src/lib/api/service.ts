// service.ts
import type { ApiConfig, ApiError, HttpMethod, QueryValue, RequestOptions } from './types'

/** Читаем env (Vite) с дефолтами */
function readEnv() {
  const env = import.meta.env as Record<string, string | undefined>
  return {
    baseUrl: (env.VITE_API_URL ?? '').replace(/\/+$/, ''),
    prefix: (env.VITE_API_PREFIX ?? '/api').replace(/\/+$/, ''),
    timeout: Number(env.VITE_API_TIMEOUT ?? 15000),
    tokenHeader: env.VITE_API_TOKEN_HEADER ?? 'Authorization',
    tokenStorageKey: env.VITE_API_TOKEN_STORAGE_KEY ?? 'token',
  }
}

/** Дефолтный источник токена — localStorage (если не передан config.getToken) */
function createDefaultGetToken(storageKey: string) {
  return (): string | null => {
    try {
      return localStorage.getItem(storageKey)
    } catch {
      return null
    }
  }
}

/** Сериализация query (с массивами) */
function buildQuery(query?: Record<string, QueryValue>): string {
  if (!query) return ''
  const params = new URLSearchParams()
  for (const [key, value] of Object.entries(query)) {
    if (value === undefined || value === null) continue
    if (Array.isArray(value)) value.forEach((v) => params.append(key, String(v)))
    else params.append(key, String(value))
  }
  const s = params.toString()
  return s ? `?${s}` : ''
}

/** Нормализация ошибки */
function toApiError(e: unknown): ApiError {
  if (e instanceof DOMException && e.name === 'AbortError') {
    const err = new Error('Request aborted') as ApiError
    err.name = 'AbortError'
    return err
  }
  if (e instanceof Error) return e as ApiError
  return new Error(String(e)) as ApiError
}

/**
 * Ядро сервиса. Возвращает объект с методами.
 * Можно создать один раз и переиспользовать, либо обернуть в composable.
 */
export function createApiService(config: ApiConfig = { baseUrl: '' }) {
  const env = readEnv()
  const baseUrl = (config.baseUrl || env.baseUrl).replace(/\/+$/, '')
  const prefix = (config.prefix ?? env.prefix).replace(/\/+$/, '')
  const timeout = config.timeout ?? env.timeout

  // 👇 Всегда есть функция получения токена: конфиг → localStorage
  const getToken = config.getToken ?? createDefaultGetToken(env.tokenStorageKey)

  const defaultHeaders = {
    'Content-Type': 'application/json',
    Accept: 'application/json',
    ...(config.headers ?? {}),
  }

  function resolveUrl(path: string): string {
    if (/^https?:\/\//i.test(path)) return path
    return `${baseUrl}${prefix}/${path.replace(/^\/+/, '')}`
  }

  async function resolveHeaders(
    extra?: Record<string, string>,
    skipAuth = false,
  ): Promise<Record<string, string>> {
    const headers: Record<string, string> = { ...defaultHeaders, ...extra }

    // 👇 токен добавляется всегда, когда он есть, кроме skipAuth
    if (!skipAuth) {
      const token = await getToken()
      if (token) {
        headers[env.tokenHeader] = token.startsWith('Bearer ') ? token : `Bearer ${token}`
      }
    }
    return headers
  }

  async function parse<T>(res: Response): Promise<T> {
    const ct = res.headers.get('content-type') ?? ''
    if (ct.includes('application/json')) return res.json()
    const text = await res.text()
    if (!text) return null as T
    try {
      return JSON.parse(text)
    } catch {
      return text as unknown as T
    }
  }

  async function request<TRes = unknown, TBody = unknown>(
    method: HttpMethod,
    path: string,
    opts: RequestOptions<TBody> = {},
  ): Promise<TRes> {
    const controller = new AbortController()
    const ms = opts.timeout ?? timeout
    const timeoutId = ms ? setTimeout(() => controller.abort(), ms) : undefined

    if (opts.signal) {
      if (opts.signal.aborted) controller.abort()
      else opts.signal.addEventListener('abort', () => controller.abort(), { once: true })
    }

    try {
      const isFormData = typeof FormData !== 'undefined' && opts.body instanceof FormData

      const headers = await resolveHeaders(opts.headers, opts.skipAuth)
      // Не мешаем fetch самому выставить Content-Type с boundary для FormData
      if (isFormData) delete headers['Content-Type']

      const body: BodyInit | undefined =
        opts.body === undefined
          ? undefined
          : isFormData
            ? (opts.body as unknown as BodyInit)
            : JSON.stringify(opts.body)

      const res = await fetch(resolveUrl(path) + buildQuery(opts.query), {
        method,
        headers,
        body,
        signal: controller.signal,
      })

      const data = await parse<TRes>(res)

      if (!res.ok) {
        const err: ApiError = Object.assign(new Error(`HTTP ${res.status} ${res.statusText}`), {
          status: res.status,
          statusText: res.statusText,
          payload: data,
        })
        throw err
      }

      return data
    } catch (e) {
      throw toApiError(e)
    } finally {
      if (timeoutId) clearTimeout(timeoutId)
    }
  }

  return {
    request,
    get: <T = unknown>(path: string, opts?: Omit<RequestOptions, 'body'>) =>
      request<T>('GET', path, opts),
    post: <T = unknown, B = unknown>(path: string, body?: B, opts?: RequestOptions<B>) =>
      request<T, B>('POST', path, { ...opts, body }),
    put: <T = unknown, B = unknown>(path: string, body?: B, opts?: RequestOptions<B>) =>
      request<T, B>('PUT', path, { ...opts, body }),
    patch: <T = unknown, B = unknown>(path: string, body?: B, opts?: RequestOptions<B>) =>
      request<T, B>('PATCH', path, { ...opts, body }),
    delete: <T = unknown>(path: string, opts?: Omit<RequestOptions, 'body'>) =>
      request<T>('DELETE', path, opts),
  }
}

export type ApiService = ReturnType<typeof createApiService>
