// src/services/auth.service.ts
import { httpClient } from './api'
import { tokenService } from './tokenService'
import { storageService, STORAGE_KEYS } from './storage'
import type { UserProfile } from '@/types/user'
import type { LoginResponse, LoginCredentials, LoginCredentials_ById } from '@/types/auth'

export const authService = {
  async login(credentials: LoginCredentials): Promise<LoginResponse> {
    // Логируем отправляемые данные
    console.log('🔐 Login credentials:', credentials)
    console.log('📋 Login credentials type:', typeof credentials)
    console.log('📋 Login credentials keys:', Object.keys(credentials))
    const response = await httpClient.post<LoginResponse>('/auth/login', credentials)
    this.saveAuthData(response)
    return response
  },

  async loginById(credentials: LoginCredentials_ById): Promise<LoginResponse> {
    console.log('🔐 Login by ID credentials:', credentials)
    console.log('📋 Login by ID credentials type:', typeof credentials)
    console.log('📋 Login by ID credentials keys:', Object.keys(credentials))
    const response = await httpClient.post<LoginResponse>('/auth/login_by_id', credentials)
    this.saveAuthData(response)
    return response
  },

  async logout(): Promise<void> {
    try {
      if (tokenService.hasTokens()) {
        await httpClient.post('/auth/logout')
      }
    } catch (e) {
      console.warn('Ошибка при выходе:', e)
    } finally {
      this.clearAuthData()
      if (typeof window !== 'undefined') {
        window.location.href = '/login'
      }
    }
  },

  saveAuthData(response: LoginResponse): void {
    // Используем tokenService для сохранения токенов
    // Предполагаем, что expires_in приходит с бэка
    const expiresIn = response.expires_in || 3600
    tokenService.setTokens(response.access_token, response.refresh_token, expiresIn)

    if (response.user) {
      storageService.set(STORAGE_KEYS.USER_DATA, response.user)
    }
  },

  getCurrentUser(): UserProfile | null {
    return storageService.get<UserProfile>(STORAGE_KEYS.USER_DATA)
  },

  isAuthenticated(): boolean {
    return tokenService.hasTokens() && !tokenService.isAccessTokenExpired()
  },

  async validateToken(): Promise<boolean> {
    if (!tokenService.hasTokens()) return false

    try {
      await httpClient.get('/auth/validate_token')
      return true
    } catch {
      return false
    }
  },

  async getCurrentUserFromServer(): Promise<UserProfile | null> {
    if (!this.isAuthenticated()) return null

    try {
      const response = await httpClient.get<UserProfile>('/auth/me')
      storageService.set(STORAGE_KEYS.USER_DATA, response)
      return response
    } catch (error) {
      console.error('Ошибка получения пользователя:', error)
      return null
    }
  },

  getAccessToken(): string | null {
    return tokenService.accessToken.value
  },

  getRefreshToken(): string | null {
    return tokenService.refreshToken.value
  },

  clearAuthData(): void {
    tokenService.clearTokens()
    storageService.remove(STORAGE_KEYS.USER_DATA)
  },
}
