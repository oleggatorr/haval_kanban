// useStore.ts
import { defineStore } from 'pinia'
import { useApi } from './useApi'
import { createResourceStore } from './store'

/**
 * Фабрика Pinia-стора для сущности.
 *
 * @example
 * export const useUsersStore = defineResourcePiniaStore<User>('users', '/users')
 */
export function defineResourcePiniaStore<T, TBody = Partial<T>>(id: string, basePath: string) {
  return defineStore(id, () => {
    const api = useApi({
      getToken: () => localStorage.getItem('token'),
    })

    const resource = createResourceStore<T, TBody>(api.service, basePath)

    return {
      // состояние
      list: resource.list,
      // методы списка
      fetchList: resource.fetchList,
      // методы одного
      get: resource.get,
      fetchOne: resource.fetchOne,
      // мутации
      create: resource.create,
      update: resource.update,
      remove: resource.remove,
      // утилиты
      reset: resource.reset,
    }
  })
}
