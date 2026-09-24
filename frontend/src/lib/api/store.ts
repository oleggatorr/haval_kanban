// store.ts
import { ref, shallowRef } from 'vue'
import type { ApiService } from './service'
import type { ApiError, RequestState, ResourceKey } from './types'

/**
 * Фабрика хранилища для одного типа сущностей.
 * Не зависит от Pinia напрямую — можно встроить в любой setup-store.
 */
export function createResourceStore<T, TBody = Partial<T>>(service: ApiService, basePath: string) {
  /** Кэш по ключу (id → state) */
  const cache = new Map<ResourceKey, RequestState<T>>()
  /** Состояние списка */
  const listState = createState<T[]>()
  /** Последний запрошенный ключ (для отладки) */
  const lastKey = ref<ResourceKey | null>(null)

  function createState<D>(): RequestState<D> {
    return {
      data: shallowRef<D | null>(null),
      loading: ref(false),
      error: shallowRef<ApiError | null>(null),
      loaded: ref(false),
      requestId: ref(0),
    }
  }

  function ensure(key: ResourceKey): RequestState<T> {
    if (!cache.has(key)) cache.set(key, createState<T>())
    return cache.get(key)!
  }

  /** Универсальный раннер — защита от race-condition */
  async function run<D>(state: RequestState<D>, fn: () => Promise<D>): Promise<D> {
    const id = ++state.requestId.value
    state.loading.value = true
    state.error.value = null
    try {
      const result = await fn()
      // Ответ устарел — игнорируем
      if (id !== state.requestId.value) return result
      state.data.value = result
      state.loaded.value = true
      return result
    } catch (e) {
      if (id === state.requestId.value) state.error.value = e as ApiError
      throw e
    } finally {
      if (id === state.requestId.value) state.loading.value = false
    }
  }

  return {
    // ——— Список ———
    list: listState,
    async fetchList(query?: Record<string, unknown>) {
      return run(listState, () => service.get<T[]>(basePath, { query: query as never }))
    },

    // ——— Один ресурс ———
    ensure,
    get(key: ResourceKey) {
      return ensure(key)
    },
    async fetchOne(key: ResourceKey) {
      const state = ensure(key)
      lastKey.value = key
      return run(state, () => service.get<T>(`${basePath}/${key}`))
    },

    // ——— Мутации ———
    async create(body: TBody) {
      const created = await service.post<T, TBody>(basePath, body)
      // Обновляем кэш и список
      const id = (created as { id?: ResourceKey }).id
      if (id !== undefined) ensure(id).data.value = created
      if (listState.data.value) listState.data.value = [...listState.data.value, created]
      return created
    },
    async update(key: ResourceKey, body: TBody) {
      const state = ensure(key)
      const updated = await run(state, () => service.patch<T, TBody>(`${basePath}/${key}`, body))
      if (listState.data.value) {
        listState.data.value = listState.data.value.map((item) =>
          (item as { id?: ResourceKey }).id === key ? updated : item,
        )
      }
      return updated
    },
    async remove(key: ResourceKey) {
      await service.delete(`${basePath}/${key}`)
      cache.delete(key)
      if (listState.data.value) {
        listState.data.value = listState.data.value.filter(
          (item) => (item as { id?: ResourceKey }).id !== key,
        )
      }
    },

    /** Сброс кэша */
    reset() {
      cache.clear()
      Object.assign(listState, createState<T[]>())
    },
  }
}

export type ResourceStore<T, TBody = Partial<T>> = ReturnType<typeof createResourceStore<T, TBody>>
