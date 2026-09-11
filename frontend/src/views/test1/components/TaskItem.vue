<template>
  <div class="task-item" :class="{ 'has-subtasks': task.subtasks && task.subtasks.length }">
    <div class="task-content">
      <div class="task-header">
        <h4>{{ task.name }}</h4>
        <div class="task-actions">
          <button @click="$emit('edit-task', task)">✏️</button>
          <button @click="$emit('delete-task', task.id)">🗑️</button>
          <button @click="toggleSubtasks">➕ Подзадача</button>
        </div>
      </div>
      <p v-if="task.description">{{ task.description }}</p>

      <!-- Рекурсивный вызов для подзадач -->
      <div v-if="showSubtasks && task.subtasks" class="subtasks-list">
        <TaskItem
          v-for="sub in task.subtasks"
          :key="sub.id"
          :task="sub"
          @edit-task="$emit('edit-task', $event)"
          @delete-task="$emit('delete-task', $event)"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

interface Task {
  id: number
  name: string
  description?: string
  subtasks?: Task[]
}

const props = defineProps<{ task: Task }>()
const emit = defineEmits(['edit-task', 'delete-task'])

const showSubtasks = ref(false)

const toggleSubtasks = () => {
  showSubtasks.value = !showSubtasks.value
}
</script>
