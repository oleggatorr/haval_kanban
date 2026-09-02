// src/composables/useLocalStorage.ts

import { ref, watch, onMounted, onUnmounted, type Ref } from 'vue'
import { storageService, STORAGE_KEYS, type StorageKey } from '@/services/storage'

/**
 * Опции для useLocalStorage
 */
interface UseLocalStorageOptions<T> {
  /** Значение по умолчанию, если в хранилище ничего нет */
  defaultValue?: T
  /** Сериализатор (по умолчанию JSON.stringify) */
  serializer?: {
    read: (value: string) => T
    write: (value: T) => string
  }
  /** Синхронизировать изменения между вкладками/окнами */
  syncAcrossTabs?: boolean
  /** Глубокое наблюдение за изменениями (для объектов) */
  deep?: boolean
  /** Событие для синхронизации между вкладками */
  storageEvent?: string
}

/**
 * Реактивная работа с localStorage
 *
 * @example
 * // Базовое использование
 * const token = useLocalStorage(STORAGE_KEYS.AUTH_TOKEN, '')
 * token.value = 'new-token' // автоматически сохраняется
 *
 * @example
 * // С объектом
 * const user = useLocalStorage<UserProfile>(STORAGE_KEYS.USER_DATA, { id: 0, name: '' })
 * user.value = { id: 1, name: 'John' }
 *
 * @example
 * // С синхронизацией между вкладками
 * const theme = useLocalStorage(STORAGE_KEYS.THEME, 'light', { syncAcrossTabs: true })
 */
export function useLocalStorage<T = any>(
  key: StorageKey,
  defaultValue?: T,
  options: UseLocalStorageOptions<T> = {},
): Ref<T> {
  const {
    defaultValue: defaultVal,
    serializer = {
      read: (value: string) => JSON.parse(value) as T,
      write: (value: T) => JSON.stringify(value),
    },
    syncAcrossTabs = false,
    deep = true,
    storageEvent = 'storage',
  } = options

  // Создаем реактивную ссылку
  const data = ref<T>(defaultVal as T) as Ref<T>

  /**
   * Загрузить данные из localStorage
   */
  const loadFromStorage = (): void => {
    try {
      const stored = storageService.get<string>(key)

      if (stored !== null && stored !== undefined) {
        try {
          data.value = serializer.read(stored)
        } catch (parseError) {
          console.warn(`[useLocalStorage] Ошибка парсинга ${key}:`, parseError)
          // Если парсинг не удался, используем значение по умолчанию
          if (defaultVal !== undefined) {
            data.value = defaultVal as T
          }
        }
      } else if (defaultVal !== undefined) {
        // Если в хранилище ничего нет, устанавливаем значение по умолчанию
        data.value = defaultVal as T
        // И сразу сохраняем его
        saveToStorage(data.value)
      }
    } catch (error) {
      console.error(`[useLocalStorage] Ошибка загрузки ${key}:`, error)
    }
  }

  /**
   * Сохранить данные в localStorage
   */
  const saveToStorage = (value: T): void => {
    try {
      if (value === undefined || value === null) {
        // Если значение undefined/null, удаляем ключ
        storageService.remove(key)
        return
      }

      const serialized = serializer.write(value)
      storageService.set(key, serialized)
    } catch (error) {
      console.error(`[useLocalStorage] Ошибка сохранения ${key}:`, error)
    }
  }

  /**
   * Обработчик события storage (для синхронизации между вкладками)
   */
  const handleStorageEvent = (event: StorageEvent): void => {
    if (!syncAcrossTabs) return

    // Проверяем, что изменился нужный ключ
    if (event.key === key) {
      try {
        if (event.newValue === null) {
          // Ключ был удален
          if (defaultVal !== undefined) {
            data.value = defaultVal as T
          }
          return
        }

        // Парсим новое значение
        data.value = serializer.read(event.newValue)
      } catch (error) {
        console.warn(`[useLocalStorage] Ошибка синхронизации ${key}:`, error)
      }
    }
  }

  /**
   * Обработчик кастомного события для синхронизации
   */
  const handleCustomEvent = (event: CustomEvent): void => {
    if (!syncAcrossTabs) return

    try {
      const { key: eventKey, value } = event.detail || {}
      if (eventKey === key && value !== undefined) {
        data.value = value
      }
    } catch (error) {
      console.warn(`[useLocalStorage] Ошибка кастомного события:`, error)
    }
  }

  // Загружаем данные при монтировании
  onMounted(() => {
    loadFromStorage()
  })

  // Следим за изменениями и сохраняем их
  watch(
    data,
    (newValue) => {
      saveToStorage(newValue)

      // Если включена синхронизация, отправляем событие в другие вкладки
      if (syncAcrossTabs) {
        try {
          // Используем BroadcastChannel для кросс-табной коммуникации
          if (typeof BroadcastChannel !== 'undefined') {
            const channel = new BroadcastChannel('local-storage-sync')
            channel.postMessage({ key, value: newValue })
            // Закрываем канал после отправки
            setTimeout(() => channel.close(), 100)
          }

          // Альтернатива - кастомное событие (работает в том же окне)
          window.dispatchEvent(
            new CustomEvent('local-storage-change', {
              detail: { key, value: newValue },
            }),
          )
        } catch (error) {
          // Игнорируем ошибки синхронизации
        }
      }
    },
    { deep },
  )

  // Подписываемся на события storage (другие вкладки)
  onMounted(() => {
    if (syncAcrossTabs) {
      window.addEventListener('storage', handleStorageEvent)
      window.addEventListener('local-storage-change', handleCustomEvent as EventListener)

      // Подписка на BroadcastChannel
      if (typeof BroadcastChannel !== 'undefined') {
        const channel = new BroadcastChannel('local-storage-sync')
        channel.onmessage = (event) => {
          const { key: eventKey, value } = event.data || {}
          if (eventKey === key) {
            data.value = value
          }
        }
        // Сохраняем канал для очистки
        ;(window as any).__broadcastChannel = channel
      }
    }
  })

  // Очищаем подписки при размонтировании
  onUnmounted(() => {
    if (syncAcrossTabs) {
      window.removeEventListener('storage', handleStorageEvent)
      window.removeEventListener('local-storage-change', handleCustomEvent as EventListener)

      if (typeof BroadcastChannel !== 'undefined' && (window as any).__broadcastChannel) {
        ;(window as any).__broadcastChannel.close()
        delete (window as any).__broadcastChannel
      }
    }
  })

  return data
}

/**
 * Утилита для создания композабла с типизированным ключом
 *
 * @example
 * const useAuthToken = createLocalStorageHook(STORAGE_KEYS.AUTH_TOKEN, '')
 * const token = useAuthToken() // Ref<string>
 */
export function createLocalStorageHook<T = any>(
  key: StorageKey,
  defaultValue?: T,
  options?: UseLocalStorageOptions<T>,
) {
  return () => useLocalStorage<T>(key, defaultValue, options)
}

/**
 * Хуки для часто используемых ключей (готовые к использованию)
 */
export const useAuthToken = createLocalStorageHook<string>(STORAGE_KEYS.AUTH_TOKEN, '')
export const useRefreshToken = createLocalStorageHook<string>(STORAGE_KEYS.REFRESH_TOKEN, '')
export const useUserProfile = createLocalStorageHook<UserProfile | null>(
  STORAGE_KEYS.USER_DATA,
  null,
)
export const useTheme = createLocalStorageHook<'light' | 'dark' | 'system'>(
  STORAGE_KEYS.THEME,
  'light',
  { syncAcrossTabs: true },
)
export const useLanguage = createLocalStorageHook<'ru' | 'en'>(STORAGE_KEYS.LANGUAGE, 'ru', {
  syncAcrossTabs: true,
})
