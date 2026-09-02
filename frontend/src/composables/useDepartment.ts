import { ref, watch, onMounted } from 'vue'
import { departmentService } from '@/services/departmentService'
import type { Department } from '@/types/department'

export function useDepartment(guidRef: Ref<string | null>) {
  const department = ref<Department | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetchDepartment() {
    const guid = guidRef.value
    if (!guid) {
      department.value = null
      return
    }

    loading.value = true
    error.value = null

    try {
      department.value = await departmentService.getDepartmentByGuid(guid)
    } catch (err: any) {
      console.error('Ошибка загрузки департамента:', err)
      error.value = 'Не удалось загрузить данные'
    } finally {
      loading.value = false
    }
  }

  // Следим за изменением GUID. Если GUID поменялся — перезагружаем данные
  watch(guidRef, () => {
    fetchDepartment()
  })

  onMounted(() => {
    fetchDepartment()
  })

  return {
    department,
    loading,
    error,
  }
}
