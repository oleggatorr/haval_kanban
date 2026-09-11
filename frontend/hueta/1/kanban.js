document.addEventListener('DOMContentLoaded', () => {
  const board = document.querySelector('.board')
  if (!board) return

  let draggedCard = null
  let placeholder = null
  let sourceColumn = null

  const hint = document.createElement('div')
  hint.className = 'drag-hint'
  hint.textContent = 'Перетащите карточку в нужную колонку'
  document.body.appendChild(hint)

  function showHint() {
    hint.classList.add('show')
  }

  function hideHint() {
    hint.classList.remove('show')
  }

  function getDropTarget(container, y) {
    const cards = [...container.querySelectorAll('.card:not(.dragging)')]

    let closest = null
    let closestOffset = Number.NEGATIVE_INFINITY

    for (const card of cards) {
      const box = card.getBoundingClientRect()
      const offset = y - box.top - box.height / 2

      if (offset < 0 && offset > closestOffset) {
        closestOffset = offset
        closest = card
      }
    }

    return closest
  }

  function createPlaceholder() {
    if (!placeholder) {
      placeholder = document.createElement('div')
      placeholder.className = 'drop-placeholder'
    }
    return placeholder
  }

  function clearDragState() {
    document.querySelectorAll('.column.drag-over').forEach((col) => {
      col.classList.remove('drag-over')
    })

    document.querySelectorAll('.card.dragging').forEach((card) => {
      card.classList.remove('dragging')
    })

    if (placeholder && placeholder.parentNode) {
      placeholder.parentNode.removeChild(placeholder)
    }

    placeholder = null
    draggedCard = null
    sourceColumn = null
    hideHint()
  }

  // Подключаем карточки к Drag & Drop.
  document.querySelectorAll('.card').forEach((card) => {
    card.setAttribute('draggable', 'true')

    card.addEventListener('dragstart', (event) => {
      draggedCard = card
      sourceColumn = card.closest('.column')

      card.classList.add('dragging')
      event.dataTransfer.effectAllowed = 'move'
      event.dataTransfer.setData('text/plain', '')

      // Небольшая задержка нужна, чтобы браузер корректно создал drag-preview.
      requestAnimationFrame(() => showHint())
    })

    card.addEventListener('dragend', () => {
      clearDragState()
    })
  })

  // Каждая колонка принимает карточки.
  document.querySelectorAll('.column').forEach((column) => {
    const cardsContainer = column.querySelector('.cards')

    column.addEventListener('dragover', (event) => {
      if (!draggedCard) return

      event.preventDefault()
      event.dataTransfer.dropEffect = 'move'

      document.querySelectorAll('.column.drag-over').forEach((col) => {
        if (col !== column) col.classList.remove('drag-over')
      })
      column.classList.add('drag-over')

      const target = getDropTarget(cardsContainer, event.clientY)
      const ph = createPlaceholder()

      if (target) {
        cardsContainer.insertBefore(ph, target)
      } else {
        cardsContainer.appendChild(ph)
      }
    })

    column.addEventListener('dragenter', (event) => {
      if (!draggedCard) return
      event.preventDefault()
      column.classList.add('drag-over')
    })

    column.addEventListener('dragleave', (event) => {
      // Не убираем подсветку при переходе между дочерними элементами колонки.
      const rect = column.getBoundingClientRect()
      const outside =
        event.clientX < rect.left ||
        event.clientX > rect.right ||
        event.clientY < rect.top ||
        event.clientY > rect.bottom

      if (outside) {
        column.classList.remove('drag-over')
      }
    })

    column.addEventListener('drop', (event) => {
      if (!draggedCard) return

      event.preventDefault()

      const oldColumn = sourceColumn
      const target = getDropTarget(cardsContainer, event.clientY)

      if (target) {
        cardsContainer.insertBefore(draggedCard, target)
      } else {
        cardsContainer.appendChild(draggedCard)
      }

      updateColumnCounts()
      updateCompletionState(draggedCard, column)
      saveBoardState()

      if (oldColumn !== column) {
        notifyMove(draggedCard, column)
      }

      clearDragState()
    })
  })

  // Не даём браузеру открыть карточку как файл при случайном drop вне колонок.
  document.addEventListener('dragover', (event) => {
    if (draggedCard) event.preventDefault()
  })

  document.addEventListener('drop', (event) => {
    if (draggedCard && !event.target.closest('.column')) {
      event.preventDefault()
      clearDragState()
    }
  })

  function updateColumnCounts() {
    document.querySelectorAll('.column').forEach((column) => {
      const count = column.querySelector('.cards').querySelectorAll('.card').length
      const badge = column.querySelector('.count')
      if (badge) badge.textContent = count
    })
  }

  function updateCompletionState(card, column) {
    const priority = card.querySelector('.priority')
    const progress = card.querySelector('.progress')
    const progressBar = progress ? progress.querySelector('span') : null

    if (column.classList.contains('done')) {
      if (priority) {
        priority.classList.remove('high', 'medium', 'low')
        priority.classList.add('completed')
        priority.textContent = 'Завершено'
      }

      if (progressBar) {
        progressBar.style.width = '100%'
        progressBar.style.background = '#18c99a'
      }
    } else if (priority && priority.classList.contains('completed')) {
      priority.classList.remove('completed')
      priority.classList.add('medium')
      priority.textContent = 'Нормальный'

      if (progressBar) {
        progressBar.style.background = ''
        progressBar.style.width = '60%'
      }
    }
  }

  function notifyMove(card, column) {
    const title = card.querySelector('h3')?.textContent.trim() || 'Карточка'
    const status = column.querySelector('.column-title')?.textContent.trim() || 'новую колонку'
    hint.textContent = `«${title}» → ${status}`
    hint.classList.add('show')

    clearTimeout(notifyMove.timer)
    notifyMove.timer = setTimeout(() => {
      hint.textContent = 'Перетащите карточку в нужную колонку'
      hideHint()
    }, 1700)
  }

  // Сохраняем порядок карточек и их колонку в localStorage.
  // Это можно заменить AJAX-запросом к PHP/API.
  function saveBoardState() {
    const state = [...document.querySelectorAll('.column')].map((column, columnIndex) => ({
      column: columnIndex,
      title: column.querySelector('.column-title')?.textContent.trim() || '',
      cards: [...column.querySelectorAll('.card h3')].map((title) => title.textContent.trim()),
    }))

    localStorage.setItem('kanban-board-state', JSON.stringify(state))
  }

  // Восстанавливаем порядок после перезагрузки страницы.
  function restoreBoardState() {
    const saved = localStorage.getItem('kanban-board-state')
    if (!saved) return

    try {
      const state = JSON.parse(saved)
      const columns = [...document.querySelectorAll('.column')]

      state.forEach((savedColumn, index) => {
        const column = columns[index]
        if (!column) return

        const cardsContainer = column.querySelector('.cards')
        const cards = [...document.querySelectorAll('.card')]

        savedColumn.cards.forEach((title) => {
          const card = cards.find((item) => item.querySelector('h3')?.textContent.trim() === title)

          if (card) cardsContainer.appendChild(card)
        })
      })

      updateColumnCounts()
    } catch (error) {
      console.warn('Не удалось восстановить состояние Kanban:', error)
      localStorage.removeItem('kanban-board-state')
    }
  }

  restoreBoardState()
  updateColumnCounts()
})
