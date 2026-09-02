// src/composables/useDragDrop.ts

import { ref, onBeforeUnmount } from 'vue' // onMounted тут не нужен
import Sortable from 'sortablejs'
import type { Ref } from 'vue'
import type { Column } from '@/types/kanban'

export function useDragDrop(columns: Ref<Column[]>) {
  const sortables = ref<Map<string, Sortable>>(new Map())

  function initSortable(columnId: string, element: HTMLElement) {
    if (sortables.value.has(columnId)) {
      sortables.value.get(columnId)?.destroy()
    }

    const sortable = Sortable.create(element, {
      group: 'kanban-tasks',
      animation: 150,
      ghostClass: 'sortable-ghost',
      chosenClass: 'sortable-chosen',
      dragClass: 'sortable-drag',

      // ВАЖНО: Отключаем стандартное поведение Vue по перемещению элементов
      // чтобы не было конфликта между Sortable и Vue
      setData: () => {},

      onEnd: (evt) => {
        const taskId = evt.item?.dataset.taskId
        const sourceColumnId = evt.from?.dataset.columnId
        const targetColumnId = evt.to?.dataset.columnId

        // newIndex - это позиция, куда упала задача
        const newIndex = evt.newIndex
        const oldIndex = evt.oldIndex

        if (!taskId || !sourceColumnId || !targetColumnId || newIndex === undefined) return

        updateTaskPosition(taskId, sourceColumnId, targetColumnId, oldIndex, newIndex)
      },
    })

    sortables.value.set(columnId, sortable)
  }

  function updateTaskPosition(
    taskId: string,
    sourceColumnId: string,
    targetColumnId: string,
    oldIndex: number,
    newIndex: number,
  ) {
    const sourceColumn = columns.value.find((c) => c.id === sourceColumnId)
    const targetColumn = columns.value.find((c) => c.id === targetColumnId)

    if (!sourceColumn || !targetColumn) return

    // 1. Удаляем задачу из старой позиции
    const [task] = sourceColumn.tasks.splice(oldIndex, 1)

    // 2. Вставляем в новую позицию
    // Если колонки разные, newIndex уже корректен.
    // Если колонка та же, newIndex тоже корректен, т.к. мы только что удалили элемент по oldIndex
    targetColumn.tasks.splice(newIndex, 0, task)

    console.log('✅ Данные обновлены:', {
      taskId,
      from: sourceColumnId,
      to: targetColumnId,
      newIndex,
    })
  }

  onBeforeUnmount(() => {
    sortables.value.forEach((sortable) => sortable.destroy())
  })

  return {
    initSortable,
  }
}
