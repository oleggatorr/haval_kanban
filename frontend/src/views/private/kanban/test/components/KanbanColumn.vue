<template>
  <div class="column glass">
    <div class="column-header">
      <div>
        <span class="column-title">{{ title }}</span>
        <span
          class="count"
          @mousedown="handleCountPress"
          @mouseup="handleCountRelease"
          @mouseleave="handleCountRelease"
        >
          {{ tasks.length }}
        </span>
      </div>
      <button
        class="column-settings"
        @click="$emit('settings')"
        @mousedown="handleSettingsPress"
        @mouseup="handleSettingsRelease"
        @mouseleave="handleSettingsRelease"
      >
        •••
      </button>
    </div>

    <div class="cards">
      <TaskCard
        v-for="task in tasks"
        :key="task.id"
        :title="task.title"
        :tag="task.tag"
        :tag-class="task.tagClass"
        :comments="task.comments"
        :subtasks="task.subtasks"
        :done="task.done"
        @open="$emit('open-task', task)"
        @add-subtask="$emit('add-subtask', task)"
      />
    </div>

    <button
      class="add-task"
      @click="$emit('add-task')"
      @mousedown="handleAddPress"
      @mouseup="handleAddRelease"
      @mouseleave="handleAddRelease"
    >
      ＋ &nbsp; Добавить задачу
    </button>
  </div>
</template>

<script setup>
import TaskCard from './TaskCard.vue'

defineProps({
  title: { type: String, required: true },
  tasks: { type: Array, default: () => [] },
})

defineEmits(['settings', 'add-task', 'open-task', 'add-subtask'])

const handleCountPress = (e) => {
  e.target.classList.add('is-pressed')
}

const handleCountRelease = (e) => {
  e.target.classList.remove('is-pressed')
}

const handleSettingsPress = (e) => {
  e.target.classList.add('is-pressed')
}

const handleSettingsRelease = (e) => {
  e.target.classList.remove('is-pressed')
}

const handleAddPress = (e) => {
  e.target.classList.add('is-pressed')
}

const handleAddRelease = (e) => {
  e.target.classList.remove('is-pressed')
}
</script>

<style scoped>
.column {
  border-radius: 20px;
  padding: 14px;
  display: flex;
  flex-direction: column;
  min-width: 0;
  transition: all 0.3s ease;
}

.column:hover {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.18), rgba(255, 255, 255, 0.08));
  border-color: rgba(255, 255, 255, 0.25);
}

.column-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 44px;
  padding: 0 5px 8px;
}

.column-header > div {
  display: flex;
  align-items: center;
  gap: 8px;
}

.column-title {
  font-size: 16px;
  font-weight: 500;
}

.count {
  min-width: 25px;
  height: 25px;
  padding: 0 7px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.12);
  border: 1px solid rgba(255, 255, 255, 0.1);
  font-size: 12px;
  color: rgba(255, 255, 255, 0.75);
  transition: all 0.15s ease;
  cursor: pointer;
}

.count:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: scale(1.08);
}

/* Уменьшенный эффект клика для счетчика */
.count:active,
.count.is-pressed {
  transform: scale(0.96);
  background: rgba(255, 255, 255, 0.22);
}

.column-settings {
  border: 0;
  background: transparent;
  color: rgba(255, 255, 255, 0.75);
  font-size: 17px;
  letter-spacing: 2px;
  cursor: pointer;
  transition: all 0.15s ease;
  padding: 4px 8px;
  border-radius: 6px;
}

.column-settings:hover {
  color: rgba(255, 255, 255, 1);
  background: rgba(255, 255, 255, 0.08);
}

/* Уменьшенный эффект клика для настроек колонки */
.column-settings:active,
.column-settings.is-pressed {
  transform: scale(0.96);
  background: rgba(255, 255, 255, 0.15);
}

.cards {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.add-task {
  width: 100%;
  margin-top: auto;
  padding-top: 17px;
  border: 0;
  background: transparent;
  color: rgba(255, 255, 255, 0.75);
  font-size: 13px;
  text-align: center;
  cursor: pointer;
  transition: all 0.15s ease;
  padding: 12px;
  border-radius: 10px;
}

.add-task:hover {
  color: rgba(255, 255, 255, 1);
  background: rgba(255, 255, 255, 0.06);
}

/* Уменьшенный эффект клика для кнопки добавления задачи */
.add-task:active,
.add-task.is-pressed {
  transform: scale(0.995);
  background: rgba(255, 255, 255, 0.12);
}
</style>
