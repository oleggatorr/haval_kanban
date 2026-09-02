// src\types\auth.ts

import type { UserProfile } from '@/types/user'

export interface LoginCredentials {
  login: string
  password: string
}

export interface LoginCredentials_ById {
  employee_id: string
  password: string
}

export interface LoginResponse {
  access_token: string
  refresh_token: string
  user: UserProfile
}
