// src/types/taskboardTypes.ts

export interface ProjectData {
  id: number
  project_id: number
  big_description: string | null
  create_at: string
  update_at: string | null
  is_active: boolean
  remove_at: string | null
}

export interface Project {
  id: number
  name: string
  create_at: string
  update_at: string | null
  is_active: boolean
  remove_at: string | null
  data: ProjectData | null
}

export interface BoardMeta {
  id: number
  project_id: number
  name: string
  description: string
  last_activity_at: string | null
}

export interface Column {
  id: number
  board_id: number
  name: string
  description: string
  position: number
  flags: any[] // Можно уточнить тип флагов, если он известен
}

export interface TaskUser {
  id: number
  name: string
  // Дополнительные поля пользователя, если они есть в ответе API
}

export interface Task {
  id: number
  column_id: number
  name: string
  description: string
  position: number
  status_id: number | null
  date_time_start: string | null
  date_time_end: string | null
  planing_date_time_start: string | null
  planing_date_time_end: string | null
  data: any | null
  users: TaskUser[]
  subtasks_count: number
  completed_subtasks_count: number
}

export interface Subtask {
  id: number
  parent_task_id: number
  name: string
  description: string
  status_id: number | null
  date_time_start: string | null
  date_time_end: string | null
  users: TaskUser[]
}

export interface FullBoardResponse {
  board: BoardMeta
  columns: Column[]
  tasks: Task[]
  subtasks: Subtask[]
}

export interface StatusItem {
  id: number
  name: string
  description: string
  is_default: boolean
  is_final: boolean
  is_active: boolean
  create_at: string
  update_at: string | null
  remove_at: string | null
}

export interface StatusesResponse {
  items: StatusItem[]
  total: number
}

export interface UserProfile {
  id?: number // ID может отсутствовать в кратком списке, но нужен для мутаций
  name: string
  email?: string
  avatar?: string
}
