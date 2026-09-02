// src/types/kanban.ts

export interface Task {
  id: string
  title: string
  description?: string
  priority: 'low' | 'medium' | 'high'
  tags: string[]
}

export interface Column {
  id: string
  name: string
  color: string
  tasks: Task[]
}
