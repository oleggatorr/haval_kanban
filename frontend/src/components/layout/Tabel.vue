<template>
  <div class="table-responsive">
    <table class="table table-hover table-striped">
      <!-- Заголовок таблицы -->
      <thead>
        <tr>
          <th
            v-for="(label, key) in columnLabels"
            :key="key"
            @click="handleSort(key)"
            class="sortable-header"
            style="cursor: pointer"
          >
            {{ label }}
            <span v-if="sortBy === key">
              {{ sortOrder === 'asc' ? '▲' : '▼' }}
            </span>
          </th>
        </tr>
      </thead>

      <!-- Тело таблицы -->
      <tbody>
        <tr v-for="(row, index) in sortedData" :key="index">
          <td v-for="(value, key) in row" :key="key">
            <!-- Форматирование значений -->
            <slot :name="`cell-${key}`" :value="value" :row="row">
              {{ formatValue(value) }}
            </slot>
          </td>
        </tr>

        <!-- Сообщение если нет данных -->
        <tr v-if="sortedData.length === 0">
          <td :colspan="Object.keys(columnLabels).length" class="text-center text-muted py-4">
            Нет данных для отображения
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

// Типы данных
type RowData = Record<string, any>

interface Props {
  data: RowData[]
  columns?: string[]
  labels?: Record<string, string>
  sortable?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  columns: () => [],
  labels: () => ({}),
  sortable: true,
})

// Состояние сортировки
const sortBy = ref<string | null>(null)
const sortOrder = ref<'asc' | 'desc'>('asc')

// Определение колонок
const columnKeys = computed(() => {
  if (props.columns.length > 0) {
    return props.columns
  }
  // Если колонки не указаны, берем из первого элемента данных
  if (props.data.length > 0) {
    return Object.keys(props.data[0])
  }
  return []
})

// Метки колонок
const columnLabels = computed(() => {
  const labels: Record<string, string> = {}

  columnKeys.value.forEach((key) => {
    if (props.labels[key]) {
      labels[key] = props.labels[key]
    } else {
      // Преобразуем snake_case в читаемый формат
      labels[key] = key.replace(/_/g, ' ').replace(/\b\w/g, (l) => l.toUpperCase())
    }
  })

  return labels
})

// Сортировка данных
const sortedData = computed(() => {
  if (!props.sortable || !sortBy.value) {
    return props.data
  }

  return [...props.data].sort((a, b) => {
    const valueA = a[sortBy.value!]
    const valueB = b[sortBy.value!]

    // Обработка null/undefined
    if (valueA == null && valueB == null) return 0
    if (valueA == null) return sortOrder.value === 'asc' ? -1 : 1
    if (valueB == null) return sortOrder.value === 'asc' ? 1 : -1

    // Сравнение чисел
    if (typeof valueA === 'number' && typeof valueB === 'number') {
      return sortOrder.value === 'asc' ? valueA - valueB : valueB - valueA
    }

    // Сравнение строк
    const strA = String(valueA).toLowerCase()
    const strB = String(valueB).toLowerCase()

    if (strA < strB) return sortOrder.value === 'asc' ? -1 : 1
    if (strA > strB) return sortOrder.value === 'asc' ? 1 : -1
    return 0
  })
})

// Обработчик сортировки
const handleSort = (key: string) => {
  if (!props.sortable) return

  if (sortBy.value === key) {
    // Переключаем порядок сортировки
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
  } else {
    // Новая колонка для сортировки
    sortBy.value = key
    sortOrder.value = 'asc'
  }
}

// Форматирование значений
const formatValue = (value: any): string => {
  if (value === null || value === undefined) {
    return '—'
  }

  if (typeof value === 'boolean') {
    return value ? 'Да' : 'Нет'
  }

  if (value instanceof Date) {
    return value.toLocaleDateString('ru-RU')
  }

  return String(value)
}

// Экспорт методов для родительского компонента
defineExpose({
  resetSort: () => {
    sortBy.value = null
    sortOrder.value = 'asc'
  },
})
</script>

<style scoped>
.table {
  margin-bottom: 0;
}

.sortable-header:hover {
  background-color: rgba(0, 0, 0, 0.05);
}

th {
  white-space: nowrap;
  user-select: none;
}

td {
  vertical-align: middle;
}
</style>
