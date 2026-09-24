# Работа с API и хранилищем

Документация по использованию HTTP-сервиса, composable-обёртки и ресурсного хранилища (опционально с Pinia).

## Содержание

- [Архитектура](#архитектура)
- [Быстрый старт](#быстрый-старт)
- [Переменные окружения](#переменные-окружения)
- [Слой 1. Сервис (`createApiService`)](#слой-1-сервис-createapiservice)
- [Слой 2. Composable (`useApi`)](#слой-2-composable-useapi)
- [Слой 3. Хранилище (`createResourceStore`)](#слой-3-хранилище-createresourcestore)
- [Слой 4. Pinia-фабрика (`defineResourcePiniaStore`)](#слой-4-pinia-фабрика-defineresourcepiniastore)
- [Работа с токеном](#работа-с-токеном)
- [Обработка ошибок](#обработка-ошибок)
- [Отмена запросов и таймауты](#отмена-запросов-и-таймауты)
- [Частые рецепты](#частые-рецепты)
- [FAQ](#faq)

---

## Архитектура

```
Компонент
   │
   ▼
useUsersStore (useStore.ts)      ← Pinia-стор (опционально)
   │
   ▼
useApi (useApi.ts)               ← общий loading/error
   │
   ▼
createApiService (service.ts)    ← fetch + env + токен + таймаут
   │
   ▼
createResourceStore (store.ts)   ← кэш, race-condition, список + сущности
   │
   ▼
types.ts                         ← общие типы
```

Каждый слой можно использовать независимо:

| Задача                                        | Что использовать           |
| --------------------------------------------- | -------------------------- |
| Разовый запрос без состояния                  | `createApiService`         |
| Запрос + общий `loading`/`error` в компоненте | `useApi`                   |
| CRUD-сущность с кэшем и списком               | `createResourceStore`      |
| Полноценный Pinia-стор                        | `defineResourcePiniaStore` |

---

## Быстрый старт

### 1. Установить env-переменные

См. [Переменные окружения](#переменные-окружения).

### 2. Создать Pinia-стор для сущности

```ts
// stores/users.ts
import { defineResourcePiniaStore } from '@/api/useStore'
import type { User } from '@/types'

export const useUsersStore = defineResourcePiniaStore<User>('users', '/users')
```

### 3. Использовать в компоненте

```vue
<script setup lang="ts">
import { onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { useUsersStore } from '@/stores/users'

const users = useUsersStore()
const { list } = storeToRefs(users)

onMounted(() => {
  users.fetchList({ page: 1, limit: 20 })
})
</script>

<template>
  <div v-if="list.loading.value">Загрузка…</div>
  <div v-else-if="list.error.value">Ошибка: {{ list.error.value.message }}</div>
  <ul v-else>
    <li v-for="u in list.data.value" :key="u.id">{{ u.name }}</li>
  </ul>
</template>
```

---

## Переменные окружения

Все переменные читаются из `import.meta.env` (Vite).

| Переменная                   | По умолчанию    | Назначение                                            |
| ---------------------------- | --------------- | ----------------------------------------------------- |
| `VITE_API_URL`               | `''`            | Базовый URL API (например, `https://api.example.com`) |
| `VITE_API_PREFIX`            | `/api`          | Префикс всех путей                                    |
| `VITE_API_TIMEOUT`           | `15000`         | Таймаут запроса в мс                                  |
| `VITE_API_TOKEN_HEADER`      | `Authorization` | Имя заголовка для токена                              |
| `VITE_API_TOKEN_STORAGE_KEY` | `token`         | Ключ `localStorage` для дефолтного `getToken`         |

Пример `.env`:

```env
VITE_API_URL=https://api.example.com
VITE_API_PREFIX=/v1
VITE_API_TIMEOUT=20000
VITE_API_TOKEN_HEADER=Authorization
VITE_API_TOKEN_STORAGE_KEY=access_token
```

Итоговый URL собирается так:

```
{baseUrl}{prefix}/{path}
https://api.example.com/v1/users
```

Абсолютные пути (`http://...`, `https://...`) используются как есть, без префикса.

---

## Слой 1. Сервис (`createApiService`)

Низкоуровневый HTTP-клиент. Создаётся один раз и переиспользуется.

### Создание

```ts
import { createApiService } from '@/api/service'

const service = createApiService({
  baseUrl: 'https://api.example.com',
  prefix: '/v1',
  timeout: 10000,
  getToken: () => localStorage.getItem('token'),
  headers: { 'X-Client': 'web' },
})
```

Все поля `ApiConfig` опциональны, кроме `baseUrl` (но и он может быть взят из env).

### Методы

```ts
service.get<T>(path, opts?)
service.post<T, B>(path, body?, opts?)
service.put<T, B>(path, body?, opts?)
service.patch<T, B>(path, body?, opts?)
service.delete<T>(path, opts?)
service.request<T, B>(method, path, opts?)   // универсальный
```

### Примеры

```ts
// GET /v1/users?page=1&tags=a&tags=b
const users = await service.get<User[]>('/users', {
  query: { page: 1, tags: ['a', 'b'] },
})

// POST /v1/users
const created = await service.post<User, UserCreate>('/users', {
  name: 'Alice',
  email: 'a@example.com',
})

// PATCH с кастомным заголовком
await service.patch<User>(
  '/users/1',
  { name: 'Bob' },
  {
    headers: { 'X-Trace-Id': 'abc' },
  },
)

// Публичный эндпоинт без токена
await service.post('/auth/login', creds, { skipAuth: true })

// Отмена
const ac = new AbortController()
service.get('/slow', { signal: ac.signal })
ac.abort()
```

### Опции запроса (`RequestOptions`)

| Поле       | Тип                          | Описание                                  |
| ---------- | ---------------------------- | ----------------------------------------- |
| `query`    | `Record<string, QueryValue>` | Query-параметры (поддерживают массивы)    |
| `headers`  | `Record<string, string>`     | Доп. заголовки (мержатся с дефолтными)    |
| `body`     | `TBody`                      | JSON-тело (или `FormData`/`Blob`)         |
| `signal`   | `AbortSignal`                | Отмена запроса                            |
| `timeout`  | `number`                     | Переопределить таймаут для одного запроса |
| `skipAuth` | `boolean`                    | Не добавлять токен                        |

### FormData

```ts
const fd = new FormData()
fd.append('file', file)
await service.post('/upload', fd)
// Content-Type: multipart/form-data; boundary=... выставится автоматически
```

---

## Слой 2. Composable (`useApi`)

Обёртка над сервисом с общим `loading`/`error`. Удобно в одиночных компонентах.

### Использование

```ts
import { useApi } from '@/api/useApi'

const api = useApi({ getToken: () => auth.accessToken })

async function load() {
  try {
    const users = await api.get<User[]>('/users')
    console.log(users)
  } catch (e) {
    // api.error уже установлен
  }
}
```

### Что возвращает

| Поле                        | Тип                               | Описание                            |
| --------------------------- | --------------------------------- | ----------------------------------- |
| `get/post/put/patch/delete` | функции                           | Обёрнутые методы сервиса            |
| `service`                   | `ApiService`                      | Прямой доступ без `loading`/`error` |
| `loading`                   | `Readonly<Ref<boolean>>`          | Идёт ли запрос                      |
| `error`                     | `Readonly<Ref<ApiError \| null>>` | Последняя ошибка                    |

> `loading` и `error` разделяются между всеми вызовами `api.*` — если нужно параллельно отслеживать несколько запросов, используйте `createResourceStore`.

---

## Слой 3. Хранилище (`createResourceStore`)

Фабрика стора для одной сущности: кэш по ключу, список, защита от race-condition, оптимистичное обновление после мутаций. **Не зависит от Pinia.**

### Создание

```ts
import { createApiService } from '@/api/service'
import { createResourceStore } from '@/api/store'

const service = createApiService({ baseUrl: '' })
const users = createResourceStore<User, UserInput>(service, '/users')
```

### API

#### Состояние

| Поле   | Тип                    | Описание         |
| ------ | ---------------------- | ---------------- |
| `list` | `RequestState<User[]>` | Состояние списка |

`RequestState<T>`:

| Поле        | Тип                     | Описание                   |
| ----------- | ----------------------- | -------------------------- |
| `data`      | `Ref<T \| null>`        | Данные                     |
| `loading`   | `Ref<boolean>`          | Загрузка                   |
| `error`     | `Ref<ApiError \| null>` | Ошибка                     |
| `loaded`    | `Ref<boolean>`          | Был ли успешный ответ      |
| `requestId` | `Ref<number>`           | Счётчик для race-condition |

#### Методы

| Метод               | Описание                                     |
| ------------------- | -------------------------------------------- |
| `fetchList(query?)` | Загрузить список (GET `basePath`)            |
| `ensure(key)`       | Получить (или создать) состояние по ключу    |
| `get(key)`          | То же, что `ensure`                          |
| `fetchOne(key)`     | Загрузить одну сущность (GET `basePath/key`) |
| `create(body)`      | POST; добавляет в кэш и список               |
| `update(key, body)` | PATCH; обновляет кэш и элемент в списке      |
| `remove(key)`       | DELETE; удаляет из кэша и списка             |
| `reset()`           | Полный сброс                                 |

### Пример

```ts
// Список
await users.fetchList({ page: 1 })
users.list.data.value // User[]

// Одна сущность
await users.fetchOne(42)
users.get(42).data.value // User | null

// Создание
const created = await users.create({ name: 'Alice' })
// кэш по created.id + список обновлены автоматически

// Обновление
await users.update(42, { name: 'Bob' })

// Удаление
await users.remove(42)

// Сброс
users.reset()
```

### Особенности

- **Race-condition:** если запустить `fetchOne(1)`, затем `fetchOne(2)` — ответ по `1` не перезапишет состояние.
- **Обновление списка:** `create`/`update`/`remove` автоматически правят `list.data`, если список уже загружен.
- **Ключ сущности:** берётся из поля `id`. Если у сущности другой ключ — нужно расширить `store.ts` (см. FAQ).

---

## Слой 4. Pinia-фабрика (`defineResourcePiniaStore`)

Готовая обёртка: Pinia-стор + `useApi` + `createResourceStore`.

### Создание

```ts
// stores/users.ts
import { defineResourcePiniaStore } from '@/api/useStore'
import type { User } from '@/types'

export const useUsersStore = defineResourcePiniaStore<User>('users', '/users')
```

### Использование в компоненте

```vue
<script setup lang="ts">
import { onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { useUsersStore } from '@/stores/users'

const users = useUsersStore()
const { list } = storeToRefs(users)

onMounted(() => users.fetchList())

async function onCreate() {
  await users.create({ name: 'Alice' })
}
</script>

<template>
  <button :disabled="list.loading.value" @click="onCreate">Добавить</button>
  <ul>
    <li v-for="u in list.data.value ?? []" :key="u.id">
      {{ u.name }}
      <button @click="users.remove(u.id)">×</button>
    </li>
  </ul>
  <p v-if="list.error.value">{{ list.error.value.message }}</p>
</template>
```

### Экспортируемое из стора

`list`, `fetchList`, `get`, `fetchOne`, `create`, `update`, `remove`, `reset`.

---

## Работа с токеном

### Как добавляется

Токен попадает в заголовок `VITE_API_TOKEN_HEADER` (по умолчанию `Authorization`) в формате:

```
Authorization: Bearer <token>
```

Если токен уже начинается с `Bearer ` — префикс не дублируется.

### Источник токена

Приоритет:

1. `config.getToken` — если передан явно.
2. `localStorage[VITE_API_TOKEN_STORAGE_KEY]` (по умолчанию `token`) — дефолт.

### Примеры

**Из `localStorage` (дефолт):**

```ts
localStorage.setItem('token', 'abc123')
const service = createApiService({ baseUrl: '' })
// все запросы автоматически с Authorization: Bearer abc123
```

**Из Pinia-стора:**

```ts
const auth = useAuthStore()
const api = useApi({ getToken: () => auth.accessToken })
```

**Асинхронный источник:**

```ts
const api = useApi({
  getToken: async () => await keycloak.getToken(),
})
```

**Публичный эндпоинт (без токена):**

```ts
await api.post('/auth/login', creds, { skipAuth: true })
```

### Что НЕ делает сервис

- ❌ Не делает refresh токена при `401`.
- ❌ Не разлогинивает при истечении сессии.
- ❌ Не кэширует токен между запросами.

Обработку `401` нужно добавлять самостоятельно — см. [Частые рецепты](#частые-рецепты).

---

## Обработка ошибок

Все ошибки нормализуются в `ApiError`:

```ts
interface ApiError extends Error {
  status?: number
  statusText?: string
  payload?: unknown
}
```

### Пример

```ts
try {
  await api.post('/users', body)
} catch (e) {
  const err = e as ApiError
  if (err.status === 422) {
    console.error('Валидация:', err.payload)
  } else if (err.name === 'AbortError') {
    console.log('Запрос отменён')
  } else {
    console.error(err.message)
  }
}
```

### В хранилище

Ошибка пишется в `state.error`:

```vue
<template>
  <p v-if="list.error.value">{{ list.error.value.status }}: {{ list.error.value.message }}</p>
</template>
```

---

## Отмена запросов и таймауты

### Таймаут

Глобально — `VITE_API_TIMEOUT`. Для одного запроса:

```ts
await api.get('/slow', { timeout: 5000 })
```

По истечении — `AbortError`.

### Отмена

```ts
const ac = new AbortController()
api.get('/long', { signal: ac.signal })

// где-то позже
ac.abort()
```

В `onUnmounted` компонента:

```ts
onUnmounted(() => ac.abort())
```

---

## Частые рецепты

### Обработка 401 (refresh / logout)

Оберните `service.request` или используйте глобальный хук:

```ts
// api/setup.ts
import { createApiService } from './service'
import { useAuthStore } from '@/stores/auth'

const service = createApiService({ baseUrl: '' })

const originalRequest = service.request
service.request = async (...args) => {
  try {
    return await originalRequest(...args)
  } catch (e) {
    const err = e as ApiError
    if (err.status === 401) {
      const auth = useAuthStore()
      await auth.refresh()
      return await originalRequest(...args) // повтор
    }
    throw e
  }
}

export { service }
```

### Кастомный ключ сущности (не `id`)

В `store.ts` замените все `(item as { id?: ResourceKey }).id` на своё поле, либо параметризуйте `createResourceStore`:

```ts
export function createResourceStore<T, TBody = Partial<T>>(
  service: ApiService,
  basePath: string,
  getId: (item: T) => ResourceKey = (item) => (item as any).id,
) {
  /* ... */
}
```

### Параллельные запросы с отдельными `loading`

Используйте `createResourceStore` — там `loading` на каждый ключ свой.

### Загрузка файла

```ts
const fd = new FormData()
fd.append('file', file)
await api.post('/upload', fd)
```

### Инвалидация кэша после мутации

```ts
await users.update(42, body)
await users.fetchList() // принудительно обновить список
```

Или вручную:

```ts
users.get(42).data.value = null
users.get(42).loaded.value = false
```

---

## FAQ

**Где хранится токен?**
По умолчанию — `localStorage[VITE_API_TOKEN_STORAGE_KEY]`. Можно переопределить через `getToken`.

**Что если токена нет?**
Заголовок не добавляется, запрос уходит без него.

**Как сделать запрос без токена?**
Передать `{ skipAuth: true }` в опции запроса.

**Почему `Content-Type` не JSON при `FormData`?**
Сервис автоматически удаляет `Content-Type`, чтобы `fetch` выставил `boundary` для multipart.

**Можно ли использовать без Pinia?**
Да, `createApiService` и `createResourceStore` не зависят от Pinia.

**Что такое `requestId` в `RequestState`?**
Счётчик для защиты от race-condition: если ответ устарел — он игнорируется.

**Как сбросить всё состояние стора?**
`users.reset()` очищает кэш и список.

**Как добавить заголовок только одному запросу?**
`api.get('/x', { headers: { 'X-Foo': 'bar' } })`.

**Где менять формат токена (не `Bearer`)?**
В `resolveHeaders` в `service.ts`.

**Как обрабатывать 422 с ошибками валидации?**
`err.payload` содержит тело ответа — обычно там `{ errors: {...} }`.

---

## Чек-лист интеграции

- [ ] Заданы env-переменные (`.env`)
- [ ] Настроен источник токена (`getToken` или `localStorage`)
- [ ] Создан сервис / `useApi` / Pinia-стор
- [ ] Обработан `401` (refresh или logout)
- [ ] Настроены таймауты под специфику API
- [ ] Добавлена обработка `ApiError` в UI
- [ ] Отмена запросов в `onUnmounted`
