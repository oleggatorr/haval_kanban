// src/composables/useToast.ts

import { ref } from 'vue'

export interface Toast {
  id: number
  message: string
  type: 'success' | 'error' | 'info' | 'warning'
}

const toasts = ref<Toast[]>([])
let nextId = 0

export function useToast() {
  const addToast = (message: string, type: Toast['type'] = 'info', duration = 3000) => {
    const id = nextId++
    toasts.value.push({ id, message, type })

    // Автоматическое удаление через указанное время
    setTimeout(() => {
      removeToast(id)
    }, duration)
  }

  const removeToast = (id: number) => {
    toasts.value = toasts.value.filter((t) => t.id !== id)
  }

  // Удобные обертки для разных типов сообщений
  const success = (message: string) => addToast(message, 'success')
  const error = (message: string) => addToast(message, 'error')
  const info = (message: string) => addToast(message, 'info')
  const warning = (message: string) => addToast(message, 'warning')

  return {
    toasts,
    addToast,
    removeToast,
    success,
    error,
    info,
    warning,
  }
}
