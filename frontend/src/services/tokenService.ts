// src/services/tokenService.ts
import { storageService, STORAGE_KEYS } from './storage'
import { ref } from 'vue'

const ACCESS_TOKEN_KEY = STORAGE_KEYS.AUTH_TOKEN
const REFRESH_TOKEN_KEY = STORAGE_KEYS.REFRESH_TOKEN
const TOKEN_EXPIRY_KEY = STORAGE_KEYS.TOKEN_EXPIRY

// Реактивные обертки
const accessToken = ref<string | null>(storageService.get(ACCESS_TOKEN_KEY))
const refreshToken = ref<string | null>(storageService.get(REFRESH_TOKEN_KEY))
const tokenExpiry = ref<number | null>(storageService.get(TOKEN_EXPIRY_KEY))

// Синхронизация между вкладками
if (typeof window !== 'undefined') {
  window.addEventListener('storage', (e) => {
    if (e.key === ACCESS_TOKEN_KEY) {
      accessToken.value = storageService.get(ACCESS_TOKEN_KEY)
    }
    if (e.key === REFRESH_TOKEN_KEY) {
      refreshToken.value = storageService.get(REFRESH_TOKEN_KEY)
    }
    if (e.key === TOKEN_EXPIRY_KEY) {
      tokenExpiry.value = storageService.get(TOKEN_EXPIRY_KEY)
    }
  })
}

export const tokenService = {
  accessToken,
  refreshToken,
  tokenExpiry,

  hasTokens: () => !!accessToken.value && !!refreshToken.value,

  isAccessTokenExpired: () => {
    if (!tokenExpiry.value) return true
    return Date.now() >= tokenExpiry.value - 60000
  },

  setTokens: (access: string, refresh: string, expiresInSec: number) => {
    const expiry = Date.now() + expiresInSec * 1000

    accessToken.value = access
    refreshToken.value = refresh
    tokenExpiry.value = expiry

    storageService.set(ACCESS_TOKEN_KEY, access)
    storageService.set(REFRESH_TOKEN_KEY, refresh)
    storageService.set(TOKEN_EXPIRY_KEY, expiry)
  },

  clearTokens: () => {
    accessToken.value = null
    refreshToken.value = null
    tokenExpiry.value = null

    storageService.remove(ACCESS_TOKEN_KEY)
    storageService.remove(REFRESH_TOKEN_KEY)
    storageService.remove(TOKEN_EXPIRY_KEY)
  },

  getAuthHeader: () => {
    return accessToken.value ? `Bearer ${accessToken.value}` : ''
  },
}
