<!-- src/components/ui/BurgerMenu.vue -->
<template>
  <div class="burger-wrapper" ref="wrapperRef">
    <!-- Кнопка-бургер -->
    <button
      class="burger-btn"
      :title="label"
      @click="toggleMenu"
      @keydown.esc="closeMenu"
      aria-haspopup="true"
      :aria-expanded="isOpen"
    >
      <span class="burger-icon" :class="{ 'is-active': isOpen }">
        <span class="line"></span>
        <span class="line"></span>
        <span class="line"></span>
      </span>
    </button>

    <!-- Выпадающее меню (как контекстное) -->
    <Teleport to="body">
      <Transition name="menu-fade">
        <div
          v-if="isOpen"
          ref="menuRef"
          class="context-menu"
          :style="menuStyles"
          role="menu"
          @click.stop
        >
          <div class="menu-header" v-if="title">
            <span class="menu-title">{{ title }}</span>
            <button class="close-btn" @click="closeMenu">✕</button>
          </div>

          <div class="menu-items">
            <button
              v-for="item in items"
              :key="item.id || item.label"
              class="menu-item"
              :class="{ 'is-danger': item.danger, 'is-disabled': item.disabled }"
              :disabled="item.disabled"
              role="menuitem"
              @click="handleItemClick(item)"
            >
              <span class="item-icon" v-if="item.icon">{{ item.icon }}</span>
              <span class="item-label">{{ item.label }}</span>
              <span class="item-shortcut" v-if="item.shortcut">{{ item.shortcut }}</span>
            </button>
          </div>

          <div class="menu-footer" v-if="footer">
            {{ footer }}
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, nextTick, type PropType } from 'vue'

export interface MenuItem {
  id?: string | number
  label: string
  icon?: string
  shortcut?: string
  danger?: boolean
  disabled?: boolean
  action?: () => void
}

const props = defineProps({
  items: {
    type: Array as PropType<MenuItem[]>,
    required: true,
    validator: (value: MenuItem[]) => value.length > 0,
  },
  title: {
    type: String,
    default: '',
  },
  footer: {
    type: String,
    default: '',
  },
  label: {
    type: String,
    default: 'Открыть меню',
  },
  placement: {
    type: String as PropType<'bottom-start' | 'bottom-end' | 'top-start' | 'top-end'>,
    default: 'bottom-start',
  },
  offset: {
    type: Number,
    default: 4,
  },
  closeOnClick: {
    type: Boolean,
    default: true,
  },
})

const emit = defineEmits<{
  (e: 'open'): void
  (e: 'close'): void
  (e: 'select', item: MenuItem): void
}>()

const isOpen = ref(false)
const wrapperRef = ref<HTMLElement | null>(null)
const menuRef = ref<HTMLElement | null>(null)
const menuPosition = ref({ x: 0, y: 0 })

// Вычисляем стили для позиционирования меню
const menuStyles = computed(() => {
  const pos = menuPosition.value
  return {
    left: pos.x + 'px',
    top: pos.y + 'px',
  }
})

// Переключение меню
const toggleMenu = async (event?: MouseEvent) => {
  if (isOpen.value) {
    closeMenu()
  } else {
    await openMenu(event)
  }
}

// Открытие меню
const openMenu = async (event?: MouseEvent) => {
  if (!wrapperRef.value) return

  // Определяем позицию для меню
  const rect = wrapperRef.value.getBoundingClientRect()
  let x = rect.left
  let y = rect.bottom + props.offset

  // Если передан event (клик по кнопке), используем его позицию
  if (event) {
    x = event.clientX
    y = event.clientY
  }

  // Корректируем позицию, чтобы меню не выходило за экран
  await nextTick()

  // Получаем размеры меню после рендера
  const menuEl = menuRef.value
  if (menuEl) {
    const menuRect = menuEl.getBoundingClientRect()
    const viewportWidth = window.innerWidth
    const viewportHeight = window.innerHeight

    // Если меню выходит за правый край
    if (x + menuRect.width > viewportWidth - 10) {
      x = viewportWidth - menuRect.width - 10
    }

    // Если меню выходит за нижний край
    if (y + menuRect.height > viewportHeight - 10) {
      y = rect.top - menuRect.height - props.offset
    }

    // Если меню выходит за левый край
    if (x < 10) {
      x = 10
    }

    // Если меню выходит за верхний край
    if (y < 10) {
      y = 10
    }
  }

  menuPosition.value = { x, y }
  isOpen.value = true
  emit('open')

  // Добавляем обработчики для закрытия
  document.addEventListener('click', handleOutsideClick)
  document.addEventListener('keydown', handleKeydown)
  window.addEventListener('resize', closeMenu)
}

// Закрытие меню
const closeMenu = () => {
  if (!isOpen.value) return
  isOpen.value = false
  emit('close')

  document.removeEventListener('click', handleOutsideClick)
  document.removeEventListener('keydown', handleKeydown)
  window.removeEventListener('resize', closeMenu)
}

// Обработка клика вне меню
const handleOutsideClick = (event: MouseEvent) => {
  const target = event.target as HTMLElement
  if (wrapperRef.value && !wrapperRef.value.contains(target)) {
    closeMenu()
  }
}

// Обработка клавиш
const handleKeydown = (event: KeyboardEvent) => {
  if (event.key === 'Escape') {
    closeMenu()
  }

  // Навигация по меню с помощью стрелок
  if (event.key === 'ArrowDown' || event.key === 'ArrowUp') {
    event.preventDefault()
    const items = menuRef.value?.querySelectorAll('.menu-item:not(.is-disabled)')
    if (!items?.length) return

    const currentIndex = Array.from(items).findIndex((el) => el === document.activeElement)
    const nextIndex =
      event.key === 'ArrowDown'
        ? (currentIndex + 1) % items.length
        : (currentIndex - 1 + items.length) % items.length

    ;(items[nextIndex] as HTMLElement)?.focus()
  }
}

// Обработка клика по пункту меню
const handleItemClick = (item: MenuItem) => {
  if (item.disabled) return

  emit('select', item)
  if (item.action) {
    item.action()
  }

  if (props.closeOnClick) {
    closeMenu()
  }
}

// Открытие по правой кнопке мыши (контекстное меню)
const handleContextMenu = (event: MouseEvent) => {
  event.preventDefault()
  event.stopPropagation()
  openMenu(event)
}

// Открытие по левой кнопке (опционально)
const handleClick = (event: MouseEvent) => {
  // Можно закомментировать, если нужен только правый клик
  // toggleMenu(event)
}

// Монтирование и размонтирование
onMounted(() => {
  if (wrapperRef.value) {
    wrapperRef.value.addEventListener('contextmenu', handleContextMenu)
    wrapperRef.value.addEventListener('click', handleClick)
  }
})

onUnmounted(() => {
  if (wrapperRef.value) {
    wrapperRef.value.removeEventListener('contextmenu', handleContextMenu)
    wrapperRef.value.removeEventListener('click', handleClick)
  }
  closeMenu()
})

// Экспортируем методы для родителя
defineExpose({
  open: openMenu,
  close: closeMenu,
  toggle: toggleMenu,
})
</script>

<style scoped>
.burger-wrapper {
  display: inline-block;
  position: relative;
}

/* Кнопка-бургер */
.burger-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border: none;
  background: transparent;
  border-radius: 4px;
  cursor: pointer;
  color: #5e6c84;
  transition: all 0.2s;
  padding: 0;
}

.burger-btn:hover {
  background-color: rgba(9, 30, 66, 0.08);
  color: #172b4d;
}

.burger-btn:focus-visible {
  outline: 2px solid #0052cc;
  outline-offset: 2px;
}

/* Иконка бургера */
.burger-icon {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  width: 18px;
  height: 14px;
  transition: all 0.3s ease;
}

.burger-icon .line {
  display: block;
  width: 100%;
  height: 2px;
  background: currentColor;
  border-radius: 2px;
  transition: all 0.3s ease;
  transform-origin: center;
}

/* Анимация превращения в крестик */
.burger-icon.is-active .line:nth-child(1) {
  transform: translateY(6px) rotate(45deg);
}

.burger-icon.is-active .line:nth-child(2) {
  opacity: 0;
  transform: scaleX(0);
}

.burger-icon.is-active .line:nth-child(3) {
  transform: translateY(-6px) rotate(-45deg);
}

/* Выпадающее меню (контекстное) */
.context-menu {
  position: fixed;
  min-width: 200px;
  max-width: 320px;
  background: white;
  border-radius: 8px;
  box-shadow:
    0 8px 24px rgba(9, 30, 66, 0.25),
    0 0 0 1px rgba(9, 30, 66, 0.08);
  padding: 6px 0;
  z-index: 9999;
  overflow: hidden;
  animation: menuSlideIn 0.15s ease;
}

.menu-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 12px;
  border-bottom: 1px solid rgba(9, 30, 66, 0.08);
  margin-bottom: 4px;
}

.menu-title {
  font-size: 12px;
  font-weight: 600;
  color: #172b4d;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.close-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 20px;
  height: 20px;
  border: none;
  background: transparent;
  border-radius: 3px;
  cursor: pointer;
  color: #5e6c84;
  font-size: 14px;
  padding: 0;
  transition: all 0.2s;
}

.close-btn:hover {
  background: rgba(9, 30, 66, 0.08);
  color: #172b4d;
}

.menu-items {
  display: flex;
  flex-direction: column;
  gap: 1px;
}

.menu-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 12px;
  border: none;
  background: transparent;
  cursor: pointer;
  color: #172b4d;
  font-size: 14px;
  font-family: inherit;
  text-align: left;
  width: 100%;
  transition: all 0.15s;
  min-height: 32px;
}

.menu-item:hover:not(.is-disabled) {
  background: rgba(9, 30, 66, 0.06);
}

.menu-item:focus-visible:not(.is-disabled) {
  outline: 2px solid #0052cc;
  outline-offset: -2px;
  background: rgba(9, 30, 66, 0.04);
}

.menu-item.is-danger {
  color: #de350b;
}

.menu-item.is-danger:hover:not(.is-disabled) {
  background: rgba(222, 53, 11, 0.08);
}

.menu-item.is-disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.item-icon {
  font-size: 16px;
  line-height: 1;
  flex-shrink: 0;
  width: 20px;
  text-align: center;
}

.item-label {
  flex: 1;
}

.item-shortcut {
  font-size: 12px;
  color: #5e6c84;
  margin-left: auto;
  padding-left: 16px;
}

.menu-footer {
  padding: 8px 12px;
  border-top: 1px solid rgba(9, 30, 66, 0.08);
  margin-top: 4px;
  font-size: 12px;
  color: #5e6c84;
}

/* Анимация появления */
.menu-fade-enter-active,
.menu-fade-leave-active {
  transition: all 0.15s ease;
}

.menu-fade-enter-from,
.menu-fade-leave-to {
  opacity: 0;
  transform: scale(0.95) translateY(-4px);
}

@keyframes menuSlideIn {
  from {
    opacity: 0;
    transform: scale(0.95) translateY(-4px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}
</style>
