import { httpClient } from './api'
import type { Department } from '@/types/department'

export const departmentService = {
  /**
   * Получить информацию о департаменте по GUID
   * @param guid - GUID департамента
   */
  async getDepartmentByGuid(guid: string): Promise<Department> {
    return await httpClient.get<Department>(`/departments/${guid}`)
  },

  /**
   * Получить список всех департаментов (опционально)
   */
  async getAllDepartments(): Promise<Department[]> {
    return await httpClient.get<Department[]>('/departments')
  },

  /**
   * Получить дочерние департаменты (опционально)
   * @param parentGuid - GUID родительского департамента
   */
  async getChildDepartments(parentGuid: string): Promise<Department[]> {
    return await httpClient.get<Department[]>(`/departments?parent_guid=${parentGuid}`)
  },
}
