export interface ApiResponse<T = any> {
  data: T
  status: number
  message?: string
}

export interface ApiError {
  status: number
  message: string
  errors?: Record<string, string[]>
}

export interface RequestConfig {
  headers?: Record<string, string>
  params?: Record<string, any>
  timeout?: number
}
