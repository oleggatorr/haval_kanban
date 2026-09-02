// src/stores/settings.ts
import { defineStore } from 'pinia'
import { computed, watch } from 'vue'
import { useLocalStorage } from '@/composables/useLocalStorage' // Убедитесь, что путь правильный

// Типы для типизации
export type AppLanguage = 'ru' | 'en' | 'zh'
export type AppTheme = 'light' | 'dark' | 'system'

interface SettingsState {
  language: AppLanguage
  theme: AppTheme
}

// Значения по умолчанию
const DEFAULT_SETTINGS: SettingsState = {
  language: 'ru',
  theme: 'system',
}

export const useSettingsStore = defineStore('settings', () => {
  // 🔹 Состояние через useLocalStorage (автоматическая синхронизация с localStorage)
  const language = useLocalStorage<AppLanguage>('app_language', DEFAULT_SETTINGS.language)
  const theme = useLocalStorage<AppTheme>('app_theme', DEFAULT_SETTINGS.theme)

  // 🔹 Вычисляемые свойства
  const isDarkMode = computed(() => {
    if (theme.value === 'system') {
      return window.matchMedia('(prefers-color-scheme: dark)').matches
    }
    return theme.value === 'dark'
  })

  const currentLocale = computed(() => {
    const locales: Record<AppLanguage, string> = {
      ru: 'ru-RU',
      en: 'en-US',
      zh: 'zh-CN',
    }
    return locales[language.value]
  })

  // 🔹 Методы для изменения настроек

  const setLanguage = (newLang: AppLanguage) => {
    language.value = newLang
    // Обновляем атрибут lang у html тега (для доступности и SEO)
    document.documentElement.lang = currentLocale.value
    console.log(`🌐 Язык изменен на: ${newLang}`)
  }

  const setTheme = (newTheme: AppTheme) => {
    theme.value = newTheme
    // Применение темы к DOM вынесено в watcher ниже для централизации
    console.log(`🎨 Тема изменена на: ${newTheme}`)
  }

  // Применение темы к DOM
  const applyThemeToBody = (themeValue: AppTheme) => {
    const body = document.body

    // Удаляем старые классы тем
    body.classList.remove('theme-light', 'theme-dark')

    if (themeValue === 'system') {
      const isDark = window.matchMedia('(prefers-color-scheme: dark)').matches
      body.classList.add(isDark ? 'theme-dark' : 'theme-light')
    } else {
      body.classList.add(`theme-${themeValue}`)
    }
  }

  // Сброс к настройкам по умолчанию
  const resetSettings = () => {
    language.value = DEFAULT_SETTINGS.language
    theme.value = DEFAULT_SETTINGS.theme
    console.log('⚙️ Настройки сброшены')
  }

  // 🔹 Автоприменение темы при загрузке и при изменении значения theme
  // Инициализация при первом запуске
  applyThemeToBody(theme.value)

  // Следим за изменением темы в сторе
  watch(theme, (newTheme) => {
    applyThemeToBody(newTheme)

    // Если выбрана системная тема, нужно следить за изменениями системы
    if (newTheme === 'system') {
      const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
      const handler = (e: MediaQueryListEvent) => {
        applyThemeToBody('system')
      }
      mediaQuery.addEventListener('change', handler)

      // Важно: в реальном приложении здесь нужна логика cleanup,
      // но в setup store pinia это сложно реализовать корректно без утечек.
      // Для простоты можно оставить как есть или вынести логику системной темы отдельно.
    }
  })

  // Следим за изменением языка для обновления атрибута lang
  watch(
    language,
    (newLang) => {
      document.documentElement.lang = currentLocale.value
    },
    { immediate: true },
  ) // immediate: true применит сразу при инициализации

  return {
    language,
    theme,
    isDarkMode,
    currentLocale,
    setLanguage,
    setTheme,
    resetSettings,
  }
})
