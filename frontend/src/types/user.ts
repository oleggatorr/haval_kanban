// types/user.ts

export interface UserProfile {
  employee_id: string
  login: string
  permissions: Record<string, unknown> // или можно уточнить структуру permissions
  is_active: boolean
  last_login: string // ISO 8601 формат даты
  created_at: string // ISO 8601 формат даты
  updated_at: string // ISO 8601 формат даты
  guid: string // UUID
  guid_person: string // UUID
  last_name: string
  first_name: string
  middle_name: string
  last_name_en: string
  first_name_en: string
  middle_name_en: string
  birth_date: string // формат YYYY-MM-DD
  employment_date: string // формат YYYY-MM-DD
  dismissal_date: string | null // может быть null
  phone: string
  email: string
  position_guid: string // UUID
  department_guid: string
}
