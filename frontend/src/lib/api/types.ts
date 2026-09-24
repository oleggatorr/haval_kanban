import type { Ref } from 'vue'

// types.ts
export type HttpMethod = 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE'

export type QueryValue =
  | string
  | number
  | boolean
  | null
  | undefined
  | (string | number | boolean)[]

export interface RequestOptions<TBody = unknown> {
  /** Query-параметры */
  query?: Record<string, QueryValue>
  /** Доп. заголовки */
  headers?: Record<string, string>
  /** JSON-тело (поддерживает вложенность) */
  body?: TBody
  /** AbortSignal для отмены */
  signal?: AbortSignal
  /** Таймаут в мс */
  timeout?: number
  /** Не добавлять токен (для login/register и т.п.) */
  skipAuth?: boolean
}

export interface ApiError extends Error {
  status?: number
  statusText?: string
  payload?: unknown
}

export interface ApiConfig {
  baseUrl: string
  prefix?: string
  headers?: Record<string, string>
  getToken?: () => string | null | Promise<string | null>
  timeout?: number
  /** Ключ localStorage по умолчанию (если getToken не передан) */
  tokenStorageKey?: string
}

export interface RequestState<T> {
  data: Ref<T | null>
  loading: Ref<boolean>
  error: Ref<ApiError | null>
  /** Был ли хоть один успешный ответ */
  loaded: Ref<boolean>
  /** Кол-во запросов (для race-condition) */
  requestId: Ref<number>
}

/** Ключ ресурса: id + опциональные параметры */
export type ResourceKey = string | number

/** Настройки store */
export interface ResourceStoreOptions {
  /** Инвалидация кэша в мс (0 = никогда) */
  ttl?: number
  /** Хранить массив сущностей */
  many?: boolean
}
