<template>
  <section class="board">
    <KanbanColumn
      v-for="column in columns"
      :key="column.id"
      :title="column.title"
      :tasks="column.tasks"
      @settings="$emit('column-settings', column)"
      @add-task="$emit('add-task', column.id)"
      @open-task="$emit('open-task', $event)"
      @add-subtask="$emit('add-subtask', $event)"
    />
  </section>
</template>

<script setup>
import KanbanColumn from './KanbanColumn.vue'

defineProps({
  columns: {
    type: Array,
    required: true,
    // Формат: [{ id: 'backlog', title: 'Бэклог', tasks: [...] }]
  },
})

defineEmits(['column-settings', 'add-task', 'open-task', 'add-subtask'])
</script>

<style scoped>
.board {
  display: grid;
  grid-template-columns: repeat(4, minmax(240px, 1fr));
  gap: 14px;
  min-height: calc(100vh - 178px);
}

@media (max-width: 1000px) {
  .board {
    grid-template-columns: repeat(2, minmax(260px, 1fr));
    overflow-y: auto;
  }
}

@media (max-width: 700px) {
  .board {
    grid-template-columns: 1fr;
  }
}
</style>
