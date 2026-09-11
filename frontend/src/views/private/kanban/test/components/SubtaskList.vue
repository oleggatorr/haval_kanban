<template>
  <div class="subtasks-container">
    <div class="subtasks">
      <div
        v-for="(subtask, index) in subtasks"
        :key="index"
        class="subtask"
        :class="{ 'is-checked': subtask.completed, 'is-clicked': clickedIndex === index }"
        @click="handleSubtaskClick(index)"
        @mousedown="handleSubtaskDown(index)"
        @mouseup="handleSubtaskUp"
        @mouseleave="handleSubtaskUp"
      >
        <span class="checkbox" :class="{ checked: subtask.completed }"></span>
        <span>{{ subtask.title }}</span>
      </div>
    </div>
    <button
      class="add-subtask"
      @click="$emit('add-subtask')"
      @mousedown="handleAddPress"
      @mouseup="handleAddRelease"
      @mouseleave="handleAddRelease"
    >
      ＋ Добавить подзадачу
    </button>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  subtasks: {
    type: Array,
    default: () => [],
  },
})

const emit = defineEmits(['toggle-subtask', 'add-subtask'])

const clickedIndex = ref(null)

const handleSubtaskClick = (index) => {
  emit('toggle-subtask', index)
}

const handleSubtaskDown = (index) => {
  clickedIndex.value = index
}

const handleSubtaskUp = () => {
  setTimeout(() => {
    clickedIndex.value = null
  }, 150)
}

const handleAddPress = (e) => {
  e.target.classList.add('is-pressed')
}

const handleAddRelease = (e) => {
  e.target.classList.remove('is-pressed')
}
</script>

<style scoped>
.subtasks-container {
  margin-top: 14px;
}

.subtasks {
  border: 1px solid rgba(255, 255, 255, 0.13);
  border-radius: 10px;
  overflow: hidden;
  background: rgba(255, 255, 255, 0.04);
}

.subtask {
  height: 39px;
  padding: 0 11px;
  display: flex;
  align-items: center;
  gap: 9px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.74);
  font-size: 12px;
  cursor: pointer;
  transition: all 0.15s ease;
  position: relative;
  overflow: hidden;
}

.subtask::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  height: 100%;
  width: 0;
  background: rgba(255, 255, 255, 0.08);
  transition: width 0.25s ease;
}

.subtask:hover::before {
  width: 100%;
}

.subtask:hover {
  padding-left: 14px;
}

/* Уменьшенный эффект клика для подзадач */
.subtask.is-clicked {
  background: rgba(255, 255, 255, 0.12);
  transform: scale(0.995);
}

.subtask:last-child {
  border-bottom: 0;
}

.checkbox {
  width: 18px;
  height: 18px;
  border: 1px solid rgba(255, 255, 255, 0.65);
  border-radius: 50%;
  transition: all 0.2s ease;
  flex-shrink: 0;
  position: relative;
}

.checkbox.checked {
  background: rgba(255, 255, 255, 0.3);
  border-color: rgba(255, 255, 255, 0.9);
  animation: checkBounce 0.3s ease;
}

@keyframes checkBounce {
  0%,
  100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.15);
  }
}

.checkbox.checked::after {
  content: '✓';
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  color: white;
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.checkbox:hover {
  border-color: rgba(255, 255, 255, 1);
  background: rgba(255, 255, 255, 0.1);
  transform: scale(1.08);
}

/* Уменьшенный эффект клика для чекбокса */
.checkbox:active {
  transform: scale(0.95);
}

.add-subtask {
  margin-top: 10px;
  border: 0;
  background: transparent;
  color: rgba(255, 255, 255, 0.75);
  font-size: 12px;
  cursor: pointer;
  transition: all 0.15s ease;
  width: 100%;
  text-align: left;
  padding: 8px 11px;
  border-radius: 8px;
}

.add-subtask:hover {
  color: rgba(255, 255, 255, 1);
  background: rgba(255, 255, 255, 0.06);
  transform: translateX(3px);
}

/* Уменьшенный эффект клика для кнопки добавления */
.add-subtask:active,
.add-subtask.is-pressed {
  transform: translateX(2px) scale(0.995);
  background: rgba(255, 255, 255, 0.12);
}
</style>
