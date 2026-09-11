<template>
  <article
    class="task-card"
    :class="{ featured: hasSubtasks, 'is-clicked': isClicked }"
    @mousedown="handleMouseDown"
    @mouseup="handleMouseUp"
    @mouseleave="handleMouseUp"
  >
    <div class="task-top">
      <h3>{{ title }}</h3>
      <button
        class="card-button"
        @click.stop="$emit('open')"
        @mousedown="handleButtonPress"
        @mouseup="handleButtonRelease"
        @mouseleave="handleButtonRelease"
      >
        <svg viewBox="0 0 24 24">
          <path d="M6 4h12v16H6z" />
          <path d="M9 9h6M9 13h6" />
        </svg>
      </button>
    </div>

    <span :class="['tag', tagClass]">{{ tag }}</span>

    <!-- Подзадачи -->
    <SubtaskList v-if="hasSubtasks" :subtasks="subtasksList" @add-subtask="$emit('add-subtask')" />

    <!-- Мета-информация -->
    <div class="task-meta" v-if="!hasSubtasks">
      <span class="meta-item">
        <span class="meta-icon comment"></span>
        {{ comments }}
      </span>
      <span class="meta-item">
        <span class="meta-icon subtask"></span>
        {{ subtasksCount }}
      </span>
      <span v-if="done" class="done-icon">✓</span>
    </div>
  </article>
</template>

<script setup>
import { ref } from 'vue'
import SubtaskList from './SubtaskList.vue'

const props = defineProps({
  title: { type: String, required: true },
  tag: { type: String, default: 'Задача' },
  tagClass: { type: String, default: 'purple' },
  comments: { type: [String, Number], default: 0 },
  subtasks: { type: [String, Number, Array], default: 0 },
  done: { type: Boolean, default: false },
})

defineEmits(['open', 'add-subtask'])

const isClicked = ref(false)

const handleMouseDown = () => {
  isClicked.value = true
}

const handleMouseUp = () => {
  setTimeout(() => {
    isClicked.value = false
  }, 150)
}

const handleButtonPress = (e) => {
  e.target.classList.add('is-pressed')
}

const handleButtonRelease = (e) => {
  e.target.classList.remove('is-pressed')
}

// Проверяем, есть ли подзадачи (массив или число > 0)
const hasSubtasks = ref(Array.isArray(props.subtasks) && props.subtasks.length > 0)

const subtasksList = ref(Array.isArray(props.subtasks) ? props.subtasks : [])

const subtasksCount = ref(typeof props.subtasks === 'number' ? props.subtasks : 0)
</script>

<style scoped>
.task-card {
  border-radius: 15px;
  padding: 16px;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.16), rgba(255, 255, 255, 0.07));
  border: 1px solid rgba(255, 255, 255, 0.22);
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.12),
    0 8px 25px rgba(20, 25, 60, 0.08);
  min-height: 137px;
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
  overflow: hidden;
}

.task-card::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.25);
  transform: translate(-50%, -50%);
  transition:
    width 0.5s,
    height 0.5s;
  pointer-events: none;
}

.task-card:active::before {
  width: 250px;
  height: 250px;
}

.task-card:hover {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.22), rgba(255, 255, 255, 0.12));
  border-color: rgba(255, 255, 255, 0.3);
  transform: translateY(-3px);
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.2),
    0 12px 32px rgba(20, 25, 60, 0.15);
}

/* Уменьшенный эффект клика для карточки */
.task-card.is-clicked {
  transform: scale(0.995) translateY(-1px);
  box-shadow:
    inset 0 1px 3px rgba(0, 0, 0, 0.08),
    0 4px 12px rgba(20, 25, 60, 0.1);
}

.task-card.featured {
  min-height: 250px;
}

.task-top {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 8px;
}

.task-card h3 {
  margin: 0 0 14px;
  font-size: 14px;
  line-height: 1.35;
  font-weight: 500;
}

.card-button {
  width: 24px;
  height: 24px;
  padding: 0;
  border: 0;
  background: transparent;
  color: rgba(255, 255, 255, 0.72);
  flex-shrink: 0;
  cursor: pointer;
  transition: all 0.15s ease;
  border-radius: 6px;
}

.card-button:hover {
  color: rgba(255, 255, 255, 1);
  transform: scale(1.12);
  background: rgba(255, 255, 255, 0.08);
}

/* Уменьшенный эффект клика для кнопки карточки */
.card-button:active,
.card-button.is-pressed {
  transform: scale(0.95);
  background: rgba(255, 255, 255, 0.15);
}

.card-button svg {
  width: 18px;
  height: 18px;
  fill: none;
  stroke: currentColor;
  stroke-width: 1.5;
}

.tag {
  display: inline-flex;
  align-items: center;
  height: 24px;
  padding: 0 9px;
  border-radius: 7px;
  font-size: 11px;
  font-weight: 500;
  background: rgba(255, 255, 255, 0.18);
  transition: all 0.2s ease;
  cursor: pointer;
}

.tag:hover {
  transform: scale(1.05);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

/* Уменьшенный эффект клика для тега */
.tag:active {
  transform: scale(0.97);
}

.tag.purple {
  background: rgba(139, 119, 255, 0.65);
}
.tag.pink {
  background: rgba(184, 102, 221, 0.65);
}
.tag.blue {
  background: rgba(76, 178, 224, 0.65);
}
.tag.green {
  background: rgba(85, 175, 119, 0.65);
}
.tag.orange {
  background: rgba(194, 139, 85, 0.7);
}

.task-meta {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-top: 17px;
  color: rgba(255, 255, 255, 0.72);
  font-size: 12px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 5px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.meta-item:hover {
  color: rgba(255, 255, 255, 0.95);
  transform: scale(1.05);
}

/* Уменьшенный эффект клика для мета-элементов */
.meta-item:active {
  transform: scale(0.97);
}

.meta-icon {
  width: 15px;
  height: 15px;
  border: 1.4px solid currentColor;
  display: inline-block;
}

.meta-icon.comment {
  border-radius: 50%;
  position: relative;
}

.meta-icon.comment::after {
  content: '';
  position: absolute;
  right: -2px;
  bottom: -2px;
  width: 4px;
  height: 4px;
  border-left: 1px solid currentColor;
  transform: rotate(-20deg);
}

.meta-icon.subtask {
  border-radius: 4px;
}

.done-icon {
  margin-left: auto;
  width: 21px;
  height: 21px;
  border: 1px solid rgba(255, 255, 255, 0.7);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.done-icon:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: scale(1.08);
}

/* Уменьшенный эффект клика для иконки выполнения */
.done-icon:active {
  transform: scale(0.95);
}
</style>
