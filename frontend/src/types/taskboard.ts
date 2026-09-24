// types.ts
export interface Board {
  id: number
  project_id: number
  name: string
  description: string | null
  last_activity_at: string | null
}

export interface Column {
  id: number
  board_id: number
  name: string
  description: string | null
  position: number
  flags: string[]
}

export interface TaskUser {
  id: number
  name: string
}

export interface Task {
  id: number
  column_id: number
  name: string
  description: string | null
  position: number
  status_id: number | null
  date_time_start: string | null
  date_time_end: string | null
  planing_date_time_start: string | null
  planing_date_time_end: string | null
  data: unknown | null
  users: TaskUser[]
  subtasks_count: number
  completed_subtasks_count: number
}

export interface Subtask {
  id: number
  parent_task_id: number
  name: string
  description: string | null
  status_id: number | null
  date_time_start: string | null
  date_time_end: string | null
  users: TaskUser[]
}

export interface FullBoardResponse {
  board: Board
  columns: Column[]
  tasks: Task[]
  subtasks: Subtask[]
}
