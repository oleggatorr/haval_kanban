<!-- components/modals/EditTaskModal.vue -->
<template>
  <BaseModal v-model="isOpen" title="Редактирование задачи" width="600px">
    <form @submit.prevent="handleSave" class="task-form">
      <div class="form-group">
        <label>Название задачи</label>
        <input v-model="form.name" class="input-field" required placeholder="Введите название" />
      </div>

      <div class="form-group">
        <label>Описание</label>
        <textarea
          v-model="form.description"
          class="input-field textarea"
          rows="5"
          placeholder="Подробное описание задачи..."
        ></textarea>
      </div>

      <div class="form-row">
        <div class="form-group half">
          <label>Статус</label>
          <select v-model="form.status_id" class="input-field">
            <option :value="null">Не выбран</option>
            <option :value="1">Новая</option>
            <option :value="2">В работе</option>
            <option :value="3">На проверке</option>
            <option :value="4">Завершено</option>
          </select>
        </div>

        <!-- Можно добавить выбор даты или исполнителей -->
        <div class="form-group half">
          <label>Планируемая дата окончания</label>
          <input type="date" v-model="form.planing_date_time_end" class="input-field" />
        </div>
      </div>
    </form>

    <template #footer>
      <button type="button" class="btn btn-secondary" @click="isOpen = false">Отмена</button>
      <button type="button" class="btn btn-primary" @click="handleSave">Сохранить</button>
    </template>
  </BaseModal>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import BaseModal from '@/components/ui/BaseModal.vue'

interface TaskData {
  id: number
  name: string
  description: string | null
  status_id: number | null
  planing_date_time_end: string | null
}

const props = defineProps<{
  modelValue: boolean
  task?: TaskData | null
}>()

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
  save: [data: TaskData]
}>()

const isOpen = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val),
})

const form = ref<TaskData>({
  id: 0,
  name: '',
  description: '',
  status_id: null,
  planing_date_time_end: null,
})

watch(
  () => props.task,
  (newVal) => {
    if (newVal) {
      // Приводим дату к формату YYYY-MM-DD для input type="date"
      const dateStr = newVal.planing_date_time_end
        ? new Date(newVal.planing_date_time_end).toISOString().split('T')[0]
        : null

      form.value = {
        ...newVal,
        planing_date_time_end: dateStr,
      }
    }
  },
  { immediate: true },
)

const handleSave = () => {
  emit('save', { ...form.value })
  isOpen.value = false
}
</script>

<style scoped>
/* Стили аналогичны EditSubtaskModal */
.task-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.form-row {
  display: flex;
  gap: 16px;
}
.half {
  flex: 1;
}
.form-group label {
  font-size: 13px;
  font-weight: 600;
  color: #4a5568;
}
.input-field {
  padding: 10px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 14px;
  outline: none;
}
.input-field:focus {
  border-color: #168be5;
}
.textarea {
  resize: vertical;
  font-family: inherit;
}
.btn {
  padding: 8px 16px;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  border: none;
  font-weight: 500;
}
.btn-primary {
  background: #168be5;
  color: white;
}
.btn-secondary {
  background: #edf2f7;
  color: #4a5568;
}
</style>
