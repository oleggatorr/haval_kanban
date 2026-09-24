<template>
  <div class="dropdown-wrapper" ref="wrapperRef">
    <!-- Кнопка-триггер -->
    <button class="trigger-btn" @click.stop="toggle" :class="{ active: isOpen }" aria-label="Меню">
      ⋮
    </button>

    <!-- Само меню -->
    <Teleport to="body">
      <Transition name="fade">
        <div v-if="isOpen" class="dropdown-menu" :style="menuStyle" @click.stop>
          <div class="menu-content">
            <slot></slot>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

const props = defineProps<{
  // 'left' - меню растет вправо от левого края кнопки
  // 'right' - меню растет влево от правого края кнопки
  align?: 'left' | 'right'
}>()

const emit = defineEmits(['close'])

const isOpen = ref(false)
const wrapperRef = ref<HTMLElement | null>(null)
const menuStyle = ref<any>({})

// Ширина меню
const MENU_WIDTH = 220

const toggle = () => {
  isOpen.value = !isOpen.value
  if (isOpen.value) calculatePosition()
}

const close = () => {
  isOpen.value = false
  emit('close')
}

const calculatePosition = () => {
  if (!wrapperRef.value) return

  const rect = wrapperRef.value.getBoundingClientRect()
  const viewportWidth = window.innerWidth

  // По умолчанию выравниваем по ЛЕВОМУ краю кнопки (меню идет вправо)
  let leftPos = rect.left

  // Если явно просим выровнять по правому краю (меню идет влево)
  if (props.align === 'right') {
    leftPos = rect.right - MENU_WIDTH
  }

  // ПРОВЕРКА: Не выходит ли меню за ПРАВЫЙ край экрана?
  if (leftPos + MENU_WIDTH > viewportWidth) {
    // Если выходит, прижимаем к правому краю экрана
    leftPos = viewportWidth - MENU_WIDTH - 16
  }

  // ПРОВЕРКА: Не выходит ли меню за ЛЕВЫЙ край экрана?
  if (leftPos < 0) {
    leftPos = 16
  }

  menuStyle.value = {
    top: `${rect.bottom + 8}px`,
    left: `${leftPos}px`,
    position: 'fixed',
    zIndex: 9999,
    width: `${MENU_WIDTH}px`,
  }
}

const handleClickOutside = (event: MouseEvent) => {
  if (wrapperRef.value && !wrapperRef.value.contains(event.target as Node)) {
    close()
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  window.addEventListener('scroll', close, true)
  window.addEventListener('resize', close, true)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
  window.removeEventListener('scroll', close, true)
  window.removeEventListener('resize', close, true)
})

defineExpose({ close })
</script>

<style scoped>
.trigger-btn {
  background: transparent;
  border: none;
  cursor: pointer;
  color: #a0aec0;
  font-size: 24px;
  padding: 6px;
  border-radius: 6px;
  line-height: 1;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.trigger-btn:hover,
.trigger-btn.active {
  background: #edf2f7;
  color: #2d3748;
}

.dropdown-menu {
  background: white;
  border-radius: 12px;
  box-shadow:
    0 10px 25px -5px rgba(0, 0, 0, 0.1),
    0 8px 10px -6px rgba(0, 0, 0, 0.1);
  padding: 8px 0;
  border: 1px solid #e2e8f0;
  overflow: hidden;
}

.menu-content {
  display: flex;
  flex-direction: column;
}

.fade-enter-active,
.fade-leave-active {
  transition:
    opacity 0.2s ease,
    transform 0.2s cubic-bezier(0.16, 1, 0.3, 1);
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-8px) scale(0.98);
}
</style>
