// src/services/storage.ts

import type { UserProfile } from '@/types/user'

// Константы ключей - единственное место для их изменения
export const STORAGE_KEYS = {
  AUTH_TOKEN: 'auth_access_token', // ← единый ключ
  REFRESH_TOKEN: 'auth_refresh_token', // ← единый ключ
  TOKEN_EXPIRY: 'auth_token_expiry', // ← добавить
  USER_DATA: 'user_data',
  THEME: 'app_theme',
  LANGUAGE: 'app_language',
} as const

// Типы для ключей (для type safety)
export type StorageKey = (typeof STORAGE_KEYS)[keyof typeof STORAGE_KEYS]

/**
 * Базовый сервис для работы с localStorage
 * - Все операции безопасны (try-catch)
 * - Единая обработка ошибок
 * - Работает в SSR (проверка доступности)
 */
class StorageService {
  private isAvailable: boolean = false

  constructor() {
    this.checkAvailability()
  }

  /**
   * Проверка доступности localStorage
   */
  private checkAvailability(): void {
    try {
      if (typeof window === 'undefined') {
        this.isAvailable = false
        return
      }

      const testKey = '__storage_test__'
      localStorage.setItem(testKey, 'test')
      localStorage.removeItem(testKey)
      this.isAvailable = true
    } catch {
      this.isAvailable = false
      console.warn('localStorage недоступен')
    }
  }

  /**
   * Получить значение по ключу
   */
  get<T = any>(key: StorageKey): T | null {
    if (!this.isAvailable) return null

    try {
      const data = localStorage.getItem(key)
      if (!data) return null

      // Пытаемся распарсить как JSON
      try {
        return JSON.parse(data) as T
      } catch {
        // Если не JSON, возвращаем как строку
        return data as unknown as T
      }
    } catch (error) {
      console.error(`Ошибка чтения ${key}:`, error)
      return null
    }
  }

  /**
   * Сохранить значение по ключу
   */
  set<T = any>(key: StorageKey, value: T): boolean {
    if (!this.isAvailable) return false

    try {
      const data = typeof value === 'string' ? value : JSON.stringify(value)
      localStorage.setItem(key, data)
      return true
    } catch (error) {
      console.error(`Ошибка записи ${key}:`, error)
      return false
    }
  }

  /**
   * Удалить значение по ключу
   */
  remove(key: StorageKey): boolean {
    if (!this.isAvailable) return false

    try {
      localStorage.removeItem(key)
      return true
    } catch (error) {
      console.error(`Ошибка удаления ${key}:`, error)
      return false
    }
  }

  /**
   * Очистить все ключи сервиса
   */
  clear(): boolean {
    if (!this.isAvailable) return false

    try {
      Object.values(STORAGE_KEYS).forEach((key) => {
        localStorage.removeItem(key)
      })
      return true
    } catch (error) {
      console.error('Ошибка очистки storage:', error)
      return false
    }
  }

  /**
   * Проверить существование ключа
   */
  has(key: StorageKey): boolean {
    if (!this.isAvailable) return false
    return localStorage.getItem(key) !== null
  }

  /**
   * Получить все ключи сервиса
   */
  getKeys(): StorageKey[] {
    return Object.values(STORAGE_KEYS) as StorageKey[]
  }
}

// Единственный экземпляр сервиса (Singleton)
export const storageService = new StorageService()
